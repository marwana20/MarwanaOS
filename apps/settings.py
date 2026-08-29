import customtkinter as ctk

from core.window_manager import register_window
from core.version import get_version
from core.updater import (
    get_latest_version,
    is_update_available
)


def open_settings(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // SETTINGS"
    )

    window.geometry(
        "650x650"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        fg_color="#090909"
    )

    register_window(
        window,
        "SETTINGS"
    )


    # ========================================================
    # APPEARANCE
    # ========================================================

    appearance_label = ctk.CTkLabel(
        window,
        text="APPEARANCE",
        font=("Arial", 16, "bold"),
        text_color="#FFFFFF"
    )

    appearance_label.pack(
        anchor="w",
        padx=30,
        pady=(25, 10)
    )


    theme_switch = ctk.CTkSwitch(
        window,
        text="Dark Mode"
    )

    theme_switch.select()

    theme_switch.pack(
        anchor="w",
        padx=30,
        pady=10
    )


    # ========================================================
    # KEYBOARD SHORTCUTS
    # ========================================================

    shortcut_label = ctk.CTkLabel(
        window,
        text="KEYBOARD SHORTCUT",
        font=("Arial", 16, "bold"),
        text_color="#FFFFFF"
    )

    shortcut_label.pack(
        anchor="w",
        padx=30,
        pady=(20, 10)
    )


    shortcut_value = ctk.CTkLabel(
        window,
        text=app.hotkey_manager.get_shortcut(),
        font=("Consolas", 14),
        text_color="#55CC88"
    )

    shortcut_value.pack(
        anchor="w",
        padx=30,
        pady=(0, 10)
    )


    # ========================================================
    # CHANGE BUTTON
    # ========================================================

    changing = False


    def change_shortcut():

        nonlocal changing

        if changing:
            return

        changing = True

        shortcut_value.configure(
            text="PRESS KEY COMBINATION...",
            text_color="#AAAAAA"
        )

        window.focus_force()


        def capture(event):

            nonlocal changing

            # ------------------------------------------------
            # IGNORE SINGLE MODIFIER KEYS
            # ------------------------------------------------

            if event.keysym in (
                "Alt_L",
                "Alt_R",
                "Control_L",
                "Control_R",
                "Shift_L",
                "Shift_R"
            ):

                return


            # ------------------------------------------------
            # BUILD TKINTER SHORTCUT
            # ------------------------------------------------

            modifiers = []

            if event.state & 0x0004:
                modifiers.append("Control")

            if event.state & 0x0001:
                modifiers.append("Shift")

            if event.state & 0x0008:
                modifiers.append("Alt")


            key = event.keysym


            if modifiers:

                shortcut = (
                    "<"
                    + "-".join(modifiers)
                    + "-"
                    + key
                    + ">"
                )

            else:

                shortcut = (
                    "<"
                    + key
                    + ">"
                )


            # ------------------------------------------------
            # SAVE SHORTCUT
            # ------------------------------------------------

            app.hotkey_manager.set_shortcut(
                shortcut
            )


            shortcut_value.configure(
                text=shortcut,
                text_color="#55CC88"
            )


            window.unbind(
                "<Key>"
            )

            changing = False


        window.bind(
            "<Key>",
            capture
        )


    change_button = ctk.CTkButton(
        window,
        text="CHANGE SHORTCUT",
        width=200,
        height=40,
        corner_radius=8,
        fg_color="#151515",
        hover_color="#252525",
        command=change_shortcut
    )

    change_button.pack(
        anchor="w",
        padx=30,
        pady=5
    )


    # ========================================================
    # UPDATES
    # ========================================================

    updates_label = ctk.CTkLabel(
        window,
        text="UPDATES",
        font=("Arial", 16, "bold"),
        text_color="#FFFFFF"
    )

    updates_label.pack(
        anchor="w",
        padx=30,
        pady=(15, 5)
    )


    update_status = ctk.CTkLabel(
        window,
        text=(
            f"Current version: {get_version()}\n"
            "Update status: NOT CHECKED"
        ),
        justify="left",
        font=("Consolas", 13),
        text_color="#888888"
    )

    update_status.pack(
        anchor="w",
        padx=30,
        pady=(0, 10)
    )


    def check_updates():

        update_button.configure(
            text="CHECKING...",
            state="disabled"
        )

        update_status.configure(
            text="Checking GitHub for updates...",
            text_color="#AAAAAA"
        )

        window.update_idletasks()


        latest_version = get_latest_version()


        if latest_version is None:

            update_status.configure(
                text=(
                    "Could not check for updates.\n"
                    "Please check your internet connection."
                ),
                text_color="#CC5555"
            )

        elif is_update_available():

            update_status.configure(
                text=(
                    f"Current version: {get_version()}\n"
                    f"Latest version:  {latest_version}\n\n"
                    "UPDATE AVAILABLE"
                ),
                text_color="#55CC88"
            )

        else:

            update_status.configure(
                text=(
                    f"Current version: {get_version()}\n"
                    f"Latest version:  {latest_version}\n\n"
                    "YOU ARE UP TO DATE"
                ),
                text_color="#55CC88"
            )


        update_button.configure(
            text="CHECK FOR UPDATES",
            state="normal"
        )


    update_button = ctk.CTkButton(
        window,
        text="CHECK FOR UPDATES",
        width=250,
        height=40,
        corner_radius=8,
        fg_color="#151515",
        hover_color="#252525",
        command=check_updates
    )

    update_button.pack(
        anchor="w",
        padx=30,
        pady=5
    )


    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    system_label = ctk.CTkLabel(
        window,
        text=(
            "SYSTEM\n\n"
            f"MarwanaOS v{get_version()}\n"
            "Python Engine: ONLINE\n"
            "GUI Engine: ONLINE\n"
            "System Monitor: ONLINE"
        ),
        justify="left",
        font=("Consolas", 13),
        text_color="#888888"
    )

    system_label.pack(
        anchor="w",
        padx=30,
        pady=20
    )