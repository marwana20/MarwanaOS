import ctypes
from ctypes import wintypes
import threading

from core.config import load_config, save_config


# ============================================================
# WINDOWS HOTKEY API
# ============================================================

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WM_HOTKEY = 0x0312
WM_QUIT = 0x0012

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000

VK_LWIN = 0x5B
VK_RWIN = 0x5C


class ShortcutManager:

    HOTKEY_ID = 9001


    # ========================================================
    # INIT
    # ========================================================

    def __init__(self, app, callback):

        self.app = app
        self.callback = callback

        config = load_config()

        self.current_shortcut = config.get(
            "hotkey",
            "<Alt-a>"
        )

        self.running = False
        self.registered = False

        self.hotkey_thread = None
        self.thread_id = None

        self.start()


    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.hotkey_thread is not None:
            return

        self.running = True

        self.hotkey_thread = threading.Thread(
            target=self._hotkey_thread,
            daemon=True
        )

        self.hotkey_thread.start()


    # ========================================================
    # PARSE SHORTCUT
    # ========================================================

    def parse_shortcut(self, shortcut):

        if not shortcut:
            raise ValueError(
                "Shortcut is empty."
            )

        shortcut = shortcut.strip()

        # <Alt-a> → Alt-a
        shortcut = shortcut.replace("<", "")
        shortcut = shortcut.replace(">", "")

        # Ctrl+A → Ctrl-A
        shortcut = shortcut.replace("+", "-")

        # Verwijder spaties
        shortcut = shortcut.replace(" ", "")

        parts = shortcut.split("-")

        modifiers = 0
        key = None


        # ====================================================
        # ONDERDELEN VERWERKEN
        # ====================================================

        for part in parts:

            part = part.lower().strip()

            # ------------------------------------------------
            # CONTROL
            # ------------------------------------------------

            if part in (
                "ctrl",
                "control"
            ):

                modifiers |= MOD_CONTROL


            # ------------------------------------------------
            # ALT
            # ------------------------------------------------

            elif part == "alt":

                modifiers |= MOD_ALT


            # ------------------------------------------------
            # SHIFT
            # ------------------------------------------------

            elif part == "shift":

                modifiers |= MOD_SHIFT


            # ------------------------------------------------
            # WINDOWS ALS MODIFIER
            # ------------------------------------------------

            elif part in (
                "win",
                "windows",
                "win_l",
                "win_r",
                "winleft",
                "winright"
            ):

                modifiers |= MOD_WIN

            # ------------------------------------------------
            # NORMALE TOETS
            # ------------------------------------------------

            else:

                if key is not None:

                    raise ValueError(
                        "Shortcut contains multiple keys."
                    )

                key = part


        # ====================================================
        # GEEN TOETS
        # ====================================================

        if key is None or key == "":

            raise ValueError(
                "Shortcut contains no key."
            )


        # ====================================================
        # SPECIALE TOETSEN
        # ====================================================

        key_map = {

            "space": 0x20,

            "enter": 0x0D,
            "return": 0x0D,

            "escape": 0x1B,
            "esc": 0x1B,

            "tab": 0x09,

            "backspace": 0x08,

            "delete": 0x2E,
            "del": 0x2E,

            "insert": 0x2D,
            "ins": 0x2D,

            "home": 0x24,
            "end": 0x23,

            "pageup": 0x21,
            "pagedown": 0x22,

            "up": 0x26,
            "down": 0x28,
            "left": 0x25,
            "right": 0x27,

            # Windows keys
            "win_l": VK_LWIN,
            "win_r": VK_RWIN,
            "winleft": VK_LWIN,
            "winright": VK_RWIN,

            # Function keys
            "f1": 0x70,
            "f2": 0x71,
            "f3": 0x72,
            "f4": 0x73,
            "f5": 0x74,
            "f6": 0x75,
            "f7": 0x76,
            "f8": 0x77,
            "f9": 0x78,
            "f10": 0x79,
            "f11": 0x7A,
            "f12": 0x7B

        }


        # ====================================================
        # KEY → VIRTUAL KEY CODE
        # ====================================================

        if key in key_map:

            vk = key_map[key]

        elif len(key) == 1:

            vk = ord(
                key.upper()
            )

        else:

            raise ValueError(
                f"Unknown key: {key}"
            )


        return (
            modifiers | MOD_NOREPEAT,
            vk
        )


    # ========================================================
    # WINDOWS HOTKEY THREAD
    # ========================================================

    def _hotkey_thread(self):

        self.thread_id = (
            kernel32.GetCurrentThreadId()
        )

        try:

            # ------------------------------------------------
            # Shortcut parsen
            # ------------------------------------------------

            try:

                modifiers, vk = self.parse_shortcut(
                    self.current_shortcut
                )

            except ValueError as error:

                print(
                    "[MarwanaOS] Invalid shortcut:",
                    self.current_shortcut
                )

                print(
                    "[MarwanaOS] Reason:",
                    error
                )

                return


            # ------------------------------------------------
            # Hotkey registreren
            # ------------------------------------------------

            success = user32.RegisterHotKey(
                None,
                self.HOTKEY_ID,
                modifiers,
                vk
            )


            if not success:

                print(
                    "[MarwanaOS] Shortcut unavailable:",
                    self.current_shortcut
                )

                return


            self.registered = True

            print(
                "[MarwanaOS] Global hotkey registered:",
                self.current_shortcut
            )


            # ------------------------------------------------
            # Windows message loop
            # ------------------------------------------------

            msg = wintypes.MSG()

            while self.running:

                result = user32.GetMessageW(
                    ctypes.byref(msg),
                    None,
                    0,
                    0
                )

                if result <= 0:
                    break


                if msg.message == WM_HOTKEY:

                    self.app.after(
                        0,
                        self.callback
                    )


        finally:

            user32.UnregisterHotKey(
                None,
                self.HOTKEY_ID
            )

            self.registered = False


    # ========================================================
    # CHECK AVAILABILITY
    # ========================================================

    def is_shortcut_available(self, shortcut):

        try:

            modifiers, vk = self.parse_shortcut(
                shortcut
            )

        except ValueError as error:

            print(
                "[MarwanaOS] Invalid shortcut:",
                error
            )

            return False


        TEST_ID = 9002


        success = user32.RegisterHotKey(
            None,
            TEST_ID,
            modifiers,
            vk
        )


        if success:

            user32.UnregisterHotKey(
                None,
                TEST_ID
            )

            return True


        return False


    # ========================================================
    # CHANGE SHORTCUT
    # ========================================================

    def set_shortcut(self, shortcut):

        shortcut = shortcut.strip()


        if not shortcut:

            return False


        # ----------------------------------------------------
        # Controleren
        # ----------------------------------------------------

        try:

            self.parse_shortcut(
                shortcut
            )

        except ValueError as error:

            print(
                "[MarwanaOS] Invalid shortcut:",
                error
            )

            return False


        # ----------------------------------------------------
        # Oude hotkey stoppen
        # ----------------------------------------------------

        self.stop_hotkey()


        # ----------------------------------------------------
        # Nieuwe shortcut
        # ----------------------------------------------------

        self.current_shortcut = shortcut


        # ----------------------------------------------------
        # Opslaan
        # ----------------------------------------------------

        config = load_config()

        config["hotkey"] = shortcut

        save_config(
            config
        )


        # ----------------------------------------------------
        # Nieuwe hotkey starten
        # ----------------------------------------------------

        self.running = True
        self.registered = False
        self.hotkey_thread = None
        self.thread_id = None

        self.start()


        print(
            "[MarwanaOS] Hotkey changed:",
            shortcut
        )

        return True


    # ========================================================
    # STOP HOTKEY
    # ========================================================

    def stop_hotkey(self):

        self.running = False


        # ----------------------------------------------------
        # Message loop wakker maken
        # ----------------------------------------------------

        if self.thread_id is not None:

            try:

                user32.PostThreadMessageW(
                    self.thread_id,
                    WM_QUIT,
                    0,
                    0
                )

            except Exception:

                pass


        self.hotkey_thread = None
        self.thread_id = None
        self.registered = False


    # ========================================================
    # GET SHORTCUT
    # ========================================================

    def get_shortcut(self):

        return self.current_shortcut


    # ========================================================
    # SHUTDOWN
    # ========================================================

    def stop(self):

        self.stop_hotkey()
