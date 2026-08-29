import customtkinter as ctk

from core.window_manager import register_window


def open_terminal(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // TERMINAL"
    )

    window.geometry(
        "750x500"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        fg_color="#090909"
    )

    # ========================================================
    # REGISTER WINDOW
    # ========================================================

    register_window(
        window,
        "TERMINAL"
    )

    # ========================================================
    # TERMINAL
    # ========================================================

    terminal = ctk.CTkTextbox(
        window,
        font=("Consolas", 13),
        fg_color="#050505",
        text_color="#AAAAAA"
    )

    terminal.pack(
        padx=30,
        pady=20,
        fill="both",
        expand=True
    )

    terminal.insert(
        "end",
        "MarwanaOS Terminal v0.4\n"
        "=======================\n\n"
        "System online.\n\n"
        "marwana@marwanaos:~$ "
    )

    terminal.configure(
        state="disabled"
    )