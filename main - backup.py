import customtkinter as ctk

from ui.desktop import Desktop
from ui.taskbar import create_taskbar
from ui.boot import create_boot_screen
from ui.start_menu import StartMenu

from apps.file_manager import open_files
from apps.terminal import open_terminal
from apps.settings import open_settings
from apps.system_monitor import open_system_monitor
from apps.task_manager import open_task_manager
from apps.display_guard import DisplayGuard
from apps.ahk_center import open_ahk_center


# ============================================================
# MARWANAOS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


app = ctk.CTk()

app.title("MarwanaOS")
app.geometry("1200x750")
app.resizable(False, False)

app.configure(
    fg_color="#050505"
)


# ============================================================
# DESKTOP
# ============================================================

desktop = Desktop(app)


# ============================================================
# APPS
# ============================================================

def launch_display_guard():

    guard = DisplayGuard(app)

    guard.focus_force()
    guard.lift()


# ============================================================
# TASKBAR
# ============================================================

taskbar = create_taskbar(
    desktop.get_frame()
)


# ============================================================
# START MENU
# ============================================================

start_menu = StartMenu(
    desktop.get_frame(),

    lambda: open_files(app),

    lambda: open_terminal(app),

    lambda: open_system_monitor(app),

    lambda: open_ahk_center(app),

    lambda: open_settings(app),

    lambda: open_task_manager(app),

    launch_display_guard
)


start_button = ctk.CTkButton(
    taskbar,
    text="◉  MarwanaOS",
    width=160,
    height=40,
    corner_radius=8,
    fg_color="#151515",
    hover_color="#222222",
    font=("Arial", 14, "bold"),
    command=start_menu.toggle
)

start_button.pack(
    side="left",
    padx=12,
    pady=10
)


# ============================================================
# BOOT
# ============================================================

def finish_boot():

    print(
        "[MarwanaOS] System ready."
    )


boot = create_boot_screen(
    app,
    finish_boot
)


# ============================================================
# START
# ============================================================

app.mainloop()