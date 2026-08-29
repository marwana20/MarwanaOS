import os
import customtkinter as ctk

from core.window_manager import (
    register_window,
    minimize_window,
    toggle_maximize,
    close_managed_window
)


def open_files(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // FILE MANAGER"
    )

    window.geometry(
        "750x500"
    )

    window.configure(
        fg_color="#090909"
    )

    register_window(
        window,
        "FILE MANAGER"
    )

    label = ctk.CTkLabel(
        window,
        text=os.path.expanduser("~"),
        font=("Consolas", 12),
        text_color="#777777"
    )

    label.pack(
        anchor="w",
        padx=30,
        pady=20
    )

    frame = ctk.CTkScrollableFrame(
        window,
        fg_color="#0D0D0D"
    )

    frame.pack(
        padx=30,
        fill="both",
        expand=True
    )

    try:

        for file in os.listdir(
            os.path.expanduser("~")
        ):

            button = ctk.CTkButton(
                frame,
                text=f"📄  {file}",
                anchor="w",
                fg_color="#111111",
                hover_color="#1D1D1D"
            )

            button.pack(
                fill="x",
                pady=3
            )

    except Exception as error:

        ctk.CTkLabel(
            frame,
            text=f"ERROR: {error}",
            text_color="#FF5555"
        ).pack()