import customtkinter as ctk

from core.window_manager import register_window


def open_ahk_center(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // AHK CENTER"
    )

    window.geometry(
        "700x500"
    )

    window.configure(
        fg_color="#090909"
    )

    register_window(
        window,
        "AHK CENTER"
    )

    # ========================================================
    # TITLE
    # ========================================================

    title = ctk.CTkLabel(
        window,
        text="AHK CENTER",
        font=("Arial", 24, "bold"),
        text_color="#FFFFFF"
    )

    title.pack(
        anchor="w",
        padx=30,
        pady=(30, 5)
    )

    subtitle = ctk.CTkLabel(
        window,
        text="AutoHotkey integration",
        font=("Arial", 12),
        text_color="#666666"
    )

    subtitle.pack(
        anchor="w",
        padx=30,
        pady=(0, 25)
    )

    # ========================================================
    # STATUS
    # ========================================================

    status_frame = ctk.CTkFrame(
        window,
        fg_color="#101010",
        corner_radius=12
    )

    status_frame.pack(
        padx=30,
        fill="x"
    )

    status = ctk.CTkLabel(
        status_frame,
        text="●  AHK ENGINE READY",
        font=("Consolas", 14),
        text_color="#55CC88"
    )

    status.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    # ========================================================
    # INFO
    # ========================================================

    info = ctk.CTkLabel(
        window,
        text=(
            "AutoHotkey integration will be managed here.\n\n"
            "Future features:\n"
            "• Script management\n"
            "• Start / stop scripts\n"
            "• Hotkey profiles\n"
            "• Macro management\n"
            "• MarwanaOS automation"
        ),
        justify="left",
        font=("Consolas", 12),
        text_color="#888888"
    )

    info.pack(
        anchor="w",
        padx=30,
        pady=25
    )