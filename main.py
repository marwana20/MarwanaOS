import customtkinter as ctk

from apps.display_guard import open_display_guard
from apps.task_manager import open_task_manager
from apps.system_monitor import open_system_monitor
from apps.file_manager import open_files
from apps.terminal import open_terminal
from apps.settings import open_settings
from apps.ahk_center import open_ahk_center

from core.hotkeys import ShortcutManager

from ui.desktop import create_desktop
from ui.boot import create_boot_screen


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MarwanaOS(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "MarwanaOS"
        )

        self.geometry(
            "1200x750"
        )

        self.minsize(
            1000,
            650
        )

        self.configure(
            fg_color="#050505"
        )

        # ====================================================
        # STATE
        # ====================================================

        self.desktop_started = False


        # ====================================================
        # GLOBAL HOTKEY
        # ====================================================

        self.hotkey_manager = ShortcutManager(
            self,
            self.toggle_marwanaos
        )


        # ====================================================
        # BOOT SCREEN
        # ====================================================

        create_boot_screen(
            self,
            self.start_desktop
        )


    # ========================================================
    # TOGGLE MARWANAOS
    # ========================================================

    def toggle_marwanaos(self):

        # ----------------------------------------------------
        # Nog aan het booten?
        # ----------------------------------------------------

        if not self.desktop_started:

            return


        # ----------------------------------------------------
        # MarwanaOS zichtbaar?
        # ----------------------------------------------------

        if self.state() == "withdrawn":

            self.deiconify()

            self.lift()

            self.focus_force()

        else:

            self.withdraw()


    # ========================================================
    # START DESKTOP
    # ========================================================

    def start_desktop(self):

        if self.desktop_started:

            return


        self.desktop_started = True


        create_desktop(
            self,
            open_display_guard,
            open_task_manager,
            open_system_monitor,
            open_files,
            open_terminal,
            open_settings,
            open_ahk_center
        )


    # ========================================================
    # CLOSE
    # ========================================================

    def destroy(self):

        if hasattr(
            self,
            "hotkey_manager"
        ):

            self.hotkey_manager.stop()

        super().destroy()


def main():

    app = MarwanaOS()

    app.mainloop()


if __name__ == "__main__":

    main()