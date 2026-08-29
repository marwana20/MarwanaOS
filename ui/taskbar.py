import customtkinter as ctk

from core.window_manager import set_taskbar


def create_taskbar(parent):

    taskbar = ctk.CTkFrame(
        parent,
        height=60,
        fg_color="#0B0B0B",
        corner_radius=0
    )

    taskbar.pack(
        side="bottom",
        fill="x"
    )

    set_taskbar(taskbar)

    return taskbar