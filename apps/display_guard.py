import ctypes
import json
import os
import subprocess
import time
from pathlib import Path

import customtkinter as ctk
import psutil


APP_NAME = "MarwanaOS Display Guard"
CONFIG_PATH = Path.home() / "MarwanaOS_DisplayGuard.json"


# ============================================================
# WINDOWS API
# ============================================================

user32 = ctypes.windll.user32

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

SW_MINIMIZE = 6

SM_CMONITORS = 80
MONITOR_DEFAULTTONEAREST = 2


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", ctypes.c_ulong),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
    ]


# ============================================================
# WINDOWS CALLBACKS
# ============================================================

EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_void_p,
    ctypes.c_void_p
)


MonitorEnumProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.POINTER(RECT),
    ctypes.c_void_p
)


# ============================================================
# DISPLAY ENUMERATION
# ============================================================

def get_monitors():
    """
    Geeft alle actieve Windows-monitors terug.
    """

    monitors = []

    @MonitorEnumProc
    def callback(hmonitor, hdc, rect_ptr, lparam):

        rect = rect_ptr.contents

        monitors.append({
            "handle": hmonitor,
            "left": rect.left,
            "top": rect.top,
            "right": rect.right,
            "bottom": rect.bottom,
            "width": rect.right - rect.left,
            "height": rect.bottom - rect.top
        })

        return True

    user32.EnumDisplayMonitors(
        0,
        0,
        callback,
        0
    )

    return monitors


def get_display_devices():
    """
    Leest de display-adapters/monitors uit Windows.
    Dit is een aanvullende detectie naast EnumDisplayMonitors().
    """

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                """
                Get-CimInstance Win32_DesktopMonitor |
                Select-Object Name, DeviceID, MonitorType, ScreenHeight, ScreenWidth |
                ConvertTo-Json
                """
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        if not result.stdout.strip():
            return []

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            data = [data]

        return data

    except Exception:
        return []

# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def monitor_count():

    return len(get_monitors())


def primary_monitor():

    point = POINT(0, 0)

    return user32.MonitorFromPoint(
        ctypes.byref(point),
        MONITOR_DEFAULTTONEAREST
    )


def get_window_rect(hwnd):

    rect = RECT()

    if user32.GetWindowRect(
        hwnd,
        ctypes.byref(rect)
    ):

        return (
            rect.left,
            rect.top,
            rect.right,
            rect.bottom
        )

    return None


def get_window_text(hwnd):

    length = user32.GetWindowTextLengthW(
        hwnd
    )

    if length <= 0:
        return ""

    buffer = ctypes.create_unicode_buffer(
        length + 1
    )

    user32.GetWindowTextW(
        hwnd,
        buffer,
        length + 1
    )

    return buffer.value


def enum_windows():

    windows = []

    @EnumWindowsProc
    def callback(hwnd, lparam):

        if user32.IsWindowVisible(hwnd):

            title = get_window_text(hwnd)

            if title:

                windows.append(
                    (hwnd, title)
                )

        return True

    user32.EnumWindows(
        callback,
        0
    )

    return windows


def get_process_name(hwnd):

    pid = ctypes.c_ulong()

    user32.GetWindowThreadProcessId(
        hwnd,
        ctypes.byref(pid)
    )

    if not pid.value:
        return ""

    try:

        return psutil.Process(
            pid.value
        ).name()

    except Exception:

        return ""


def is_external_window(
    hwnd,
    primary
):

    rect = get_window_rect(hwnd)

    if not rect:
        return False

    center_x = (
        rect[0] + rect[2]
    ) // 2

    center_y = (
        rect[1] + rect[3]
    ) // 2

    point = POINT(
        center_x,
        center_y
    )

    monitor = user32.MonitorFromPoint(
        ctypes.byref(point),
        MONITOR_DEFAULTTONEAREST
    )

    return monitor != primary


# ============================================================
# POWER PROTECTION
# ============================================================
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

SetThreadExecutionState = kernel32.SetThreadExecutionState
SetThreadExecutionState.argtypes = [ctypes.c_uint]
SetThreadExecutionState.restype = ctypes.c_uint


def set_sleep_protection(enabled):

    if enabled:

        result = SetThreadExecutionState(
            ES_CONTINUOUS
            | ES_SYSTEM_REQUIRED
            | ES_DISPLAY_REQUIRED
        )

    else:

        result = SetThreadExecutionState(
            ES_CONTINUOUS
        )

    return result != 0


# ============================================================
# PRIVACY
# ============================================================

def privacy_scan(
    blocked_apps,
    primary
):

    if not blocked_apps:
        return

    for hwnd, title in enum_windows():

        process = get_process_name(
            hwnd
        ).lower()

        title_lower = title.lower()

        matched = False

        for app in blocked_apps:

            app_name = app.lower().strip()

            if not app_name:
                continue

            if (
                app_name in process
                or app_name in title_lower
            ):

                matched = True
                break

        if matched:

            if is_external_window(
                hwnd,
                primary
            ):

                user32.ShowWindow(
                    hwnd,
                    SW_MINIMIZE
                )


# ============================================================
# CONFIG
# ============================================================

DEFAULT_CONFIG = {

    "privacy_enabled": True,

    "power_guard_enabled": True,

    "auto_extend": False,

    "blocked_apps": [
        "WhatsApp",
        "Teams",
        "Discord",
        "Outlook",
        "Telegram",
        "Signal"
    ]
}


def load_config():

    if not CONFIG_PATH.exists():

        return DEFAULT_CONFIG.copy()

    try:

        data = json.loads(
            CONFIG_PATH.read_text(
                encoding="utf-8"
            )
        )

        config = DEFAULT_CONFIG.copy()

        config.update(data)

        return config

    except Exception:

        return DEFAULT_CONFIG.copy()


def save_config(config):

    CONFIG_PATH.write_text(

        json.dumps(
            config,
            indent=4,
            ensure_ascii=False
        ),

        encoding="utf-8"
    )


# ============================================================
# DISPLAY GUARD WINDOW
# ============================================================

class DisplayGuard(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.master = master

        self.cfg = load_config()

        self.running = True

        self.external_connected = (
            monitor_count() > 1
        )

        self.primary = primary_monitor()

        self.last_count = monitor_count()

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.title(
            APP_NAME
        )

        self.geometry(
            "720x570"
        )

        self.minsize(
            650,
            500
        )

        self.configure(
            fg_color="#090909"
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.build_ui()

        self.update_ui()

        # ----------------------------------------------------
        # START MONITOR
        # ----------------------------------------------------

        self.after(
            1000,
            self.monitor_loop
        )


    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            3,
            weight=1
        )

        title = ctk.CTkLabel(

            self,

            text="MARWANAOS DISPLAY GUARD",

            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            padx=25,
            pady=(25, 5),
            sticky="w"
        )


        subtitle = ctk.CTkLabel(

            self,

            text="Automatic presentation & privacy protection",

            font=ctk.CTkFont(
                size=14
            ),

            text_color="#777777"
        )

        subtitle.grid(
            row=1,
            column=0,
            padx=27,
            pady=(0, 20),
            sticky="w"
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color="#101010"
        )

        self.status.grid(
            row=2,
            column=0,
            padx=25,
            pady=5,
            sticky="ew"
        )

        self.status.grid_columnconfigure(
            1,
            weight=1
        )


        ctk.CTkLabel(

            self.status,

            text="DISPLAY STATUS",

            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )

        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=(15, 4),
            sticky="w"
        )


        self.display_label = ctk.CTkLabel(
            self.status,
            text="Detecting..."
        )

        self.display_label.grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 15),
            sticky="w"
        )


        self.mode_label = ctk.CTkLabel(
            self.status,
            text=""
        )

        self.mode_label.grid(
            row=1,
            column=1,
            padx=18,
            pady=(0, 15),
            sticky="e"
        )


        # ----------------------------------------------------
        # CONTROL PANEL
        # ----------------------------------------------------

        panel = ctk.CTkScrollableFrame(

            self,

            label_text="CONTROL PANEL"
        )

        panel.grid(
            row=3,
            column=0,
            padx=25,
            pady=20,
            sticky="nsew"
        )


        # POWER

        self.power_switch = ctk.CTkSwitch(

            panel,

            text="Sleep Protection when external display is connected",

            command=self.save_from_ui
        )

        self.power_switch.pack(
            anchor="w",
            padx=15,
            pady=12
        )

        if self.cfg["power_guard_enabled"]:
            self.power_switch.select()


        # PRIVACY

        self.privacy_switch = ctk.CTkSwitch(

            panel,

            text="Privacy Guard for selected applications",

            command=self.save_from_ui
        )

        self.privacy_switch.pack(
            anchor="w",
            padx=15,
            pady=12
        )

        if self.cfg["privacy_enabled"]:
            self.privacy_switch.select()


        # EXTEND

        self.extend_switch = ctk.CTkSwitch(

            panel,

            text="Automatically switch Windows to 'Extend' mode",

            command=self.save_from_ui
        )

        self.extend_switch.pack(
            anchor="w",
            padx=15,
            pady=12
        )

        if self.cfg["auto_extend"]:
            self.extend_switch.select()


        # APPS

        ctk.CTkLabel(

            panel,

            text=(
                "Apps protected by Privacy Guard\n"
                "(one app/process per line):"
            ),

            justify="left"

        ).pack(
            anchor="w",
            padx=15,
            pady=(20, 5)
        )


        self.apps_box = ctk.CTkTextbox(
            panel,
            height=130
        )

        self.apps_box.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.apps_box.insert(
            "1.0",
            "\n".join(
                self.cfg["blocked_apps"]
            )
        )


        # SAVE

        save_button = ctk.CTkButton(

            panel,

            text="SAVE SETTINGS",

            command=self.save_from_ui,

            height=40
        )

        save_button.pack(
            anchor="w",
            padx=15,
            pady=10
        )

        # ----------------------------------------------------
        # DEBUG DISPLAY SCANNER
        # ----------------------------------------------------

        debug_button = ctk.CTkButton(
            panel,
            text="🔍 SCAN DISPLAYS",
            command=self.debug_displays,
            height=40,
            fg_color="#151515",
            hover_color="#252525"
        )

        debug_button.pack(
            anchor="w",
            padx=15,
            pady=10
        )

        # LOG

        self.log = ctk.CTkTextbox(

            self,

            height=95,

            state="disabled"
        )

        self.log.grid(
            row=4,
            column=0,
            padx=25,
            pady=(0, 20),
            sticky="ew"
        )


        self.write_log(
            "Display Guard initialized."
        )


    # ========================================================
    # LOG
    # ========================================================

    def write_log(self, text):

        try:

            self.log.configure(
                state="normal"
            )

            timestamp = time.strftime(
                "%H:%M:%S"
            )

            self.log.insert(
                "end",
                f"[{timestamp}] {text}\n"
            )

            self.log.see(
                "end"
            )

            self.log.configure(
                state="disabled"
            )

        except Exception:

            pass


    # ========================================================
    # SAVE
    # ========================================================

    def save_from_ui(self):

        apps = [

            x.strip()

            for x in self.apps_box.get("1.0", "end").splitlines()
   	    if x.strip()
        ]

        self.cfg[
            "power_guard_enabled"
        ] = bool(
            self.power_switch.get()
        )

        self.cfg[
            "privacy_enabled"
        ] = bool(
            self.privacy_switch.get()
        )

        self.cfg[
            "auto_extend"
        ] = bool(
            self.extend_switch.get()
        )

        self.cfg[
            "blocked_apps"
        ] = apps

        save_config(
            self.cfg
        )

        self.write_log(
            "Settings saved."
        )

    # ========================================================
    # DEBUG DISPLAY SCANNER
    # ========================================================

    def debug_displays(self):

        # ============================================
        # WINDOWS MONITORS
        # ============================================

        monitors = get_monitors()

        self.write_log(
            f"Windows reports {len(monitors)} active display(s)."
        )

        for i, monitor in enumerate(monitors, 1):

            self.write_log(
                f"DISPLAY {i}: "
                f"{monitor['width']}x{monitor['height']} "
                f"at ({monitor['left']}, {monitor['top']})"
            )

        # ============================================
        # WINDOWS DISPLAY DEVICES
        # ============================================

        devices = get_display_devices()

        self.write_log(
            f"Windows display devices found: {len(devices)}"
        )

        for i, device in enumerate(devices, 1):

            name = device.get(
                "Name",
                "Unknown"
            )

            device_id = device.get(
                "DeviceID",
                "Unknown"
            )

            width = device.get(
                "ScreenWidth",
                "?"
            )

            height = device.get(
                "ScreenHeight",
                "?"
            )

            self.write_log(
                f"DEVICE {i}: "
                f"{name} | "
                f"{width}x{height} | "
                f"{device_id}"
            )

        # ============================================
        # CONSOLE
        # ============================================

        print(
            "\n========== DISPLAY DEBUG =========="
        )

        print(
            f"Active monitors: {len(monitors)}"
        )

        for i, monitor in enumerate(monitors, 1):

            print(
                f"DISPLAY {i}: "
                f"{monitor['width']}x{monitor['height']} "
                f"at "
                f"({monitor['left']}, "
                f"{monitor['top']})"
            )

        print(
            f"\nDisplay devices: {len(devices)}"
        )

        for i, device in enumerate(devices, 1):

            print(
                f"DEVICE {i}: "
                f"{device.get('Name')} | "
                f"{device.get('ScreenWidth')}x"
                f"{device.get('ScreenHeight')} | "
                f"{device.get('DeviceID')}"
            )

        print(
            "===================================\n"
        )

    # ========================================================
    # PRESENTATION MODE
    # ========================================================

    def set_presentation_mode(
        self,
        active
    ):

        if active == self.external_connected:
            return

        self.external_connected = active

        if active:

            self.write_log(
                "External display detected → "
                "Presentation Mode ACTIVE."
            )

            if self.cfg[
                "power_guard_enabled"
            ]:

                if set_sleep_protection(True):

                    self.write_log(
                        "Sleep protection enabled."
                    )

                else:

                    self.write_log(
                        "Could not enable sleep protection."
                    )


            if self.cfg[
                "auto_extend"
            ]:

                try:

                    subprocess.Popen(

                        [
                            "DisplaySwitch.exe",
                            "/extend"
                        ],

                        stdout=subprocess.DEVNULL,

                        stderr=subprocess.DEVNULL
                    )

                    self.write_log(
                        "Requested Windows Extend mode."
                    )

                except Exception as error:

                    self.write_log(
                        f"Display switch error: {error}"
                    )


        else:

            self.write_log(
                "External display disconnected → "
                "Normal Mode."
            )

            set_sleep_protection(
                False
            )

            self.write_log(
                "Windows power settings restored."
            )


    # ========================================================
    # DISPLAY CHECK
    # ========================================================

    def check_display_change(self):

        if not self.running:
            return

        try:

            count = monitor_count()

            active = count > 1

            self.set_presentation_mode(
                active
            )

            self.update_ui()

        except Exception as error:

            self.write_log(
                f"Display detection error: {error}"
            )


    # ========================================================
    # MONITOR LOOP
    # ========================================================

    def monitor_loop(self):

        if not self.running:
            return

        try:

            count = monitor_count()

            # ------------------------------------------------
            # DISPLAY CHANGE
            # ------------------------------------------------

            if count != self.last_count:

                self.last_count = count

                # Geef Windows even tijd om het display
                # volledig te initialiseren.

                self.after(
                    1000,
                    self.check_display_change
                )

            else:

                # ------------------------------------------------
                # PRIVACY
                # ------------------------------------------------

                if (
                    self.external_connected
                    and self.cfg[
                        "privacy_enabled"
                    ]
                ):

                    privacy_scan(

                        self.cfg[
                            "blocked_apps"
                        ],

                        self.primary
                    )


                self.update_ui()


        except Exception as error:

            self.write_log(
                f"Monitor error: {error}"
            )


        # ----------------------------------------------------
        # NEXT CHECK
        # ----------------------------------------------------

        if self.running:

            self.after(
                1000,
                self.monitor_loop
            )


    # ========================================================
    # UPDATE UI
    # ========================================================

    def update_ui(self):

        count = monitor_count()

        if count > 1:

            self.display_label.configure(

                text=f"🟢 {count} displays detected"
            )

            self.mode_label.configure(

                text="🔒 PRESENTATION MODE",

                text_color="#55CC88"
            )

        else:

            self.display_label.configure(

                text="🔵 Laptop display only"
            )

            self.mode_label.configure(

                text="NORMAL WINDOWS MODE",

                text_color="#777777"
            )


    # ========================================================
    # CLOSE
    # ========================================================

    def on_close(self):

        self.running = False

        set_sleep_protection(False)

        save_config(self.cfg)

        self.destroy()


# ============================================================
# PUBLIC APP ENTRY POINT
# ============================================================

def open_display_guard(app):
    return DisplayGuard(app)