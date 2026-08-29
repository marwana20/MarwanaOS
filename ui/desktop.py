import customtkinter as ctk
from PIL import Image

from core.config import WALLPAPER_PATH


class Desktop:

    def __init__(
        self,
        master,
        open_display_guard,
        open_task_manager,
        open_system_monitor,
        open_files,
        open_terminal,
        open_settings,
        open_ahk_center
    ):

        self.master = master

        self.open_display_guard = open_display_guard
        self.open_task_manager = open_task_manager
        self.open_system_monitor = open_system_monitor
        self.open_files = open_files
        self.open_terminal = open_terminal
        self.open_settings = open_settings
        self.open_ahk_center = open_ahk_center

        self.start_menu = None

        # ====================================================
        # DESKTOP FRAME
        # ====================================================

        self.frame = ctk.CTkFrame(
            master,
            fg_color="#080808",
            corner_radius=0
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # WALLPAPER
        # ====================================================

        self.wallpaper = None

        self.load_wallpaper()

        # ====================================================
        # DESKTOP
        # ====================================================

        self.build_desktop()


    # ========================================================
    # WALLPAPER
    # ========================================================

    def load_wallpaper(self):

        if not WALLPAPER_PATH.exists():

            print(
                "[MarwanaOS] Wallpaper not found:"
                f" {WALLPAPER_PATH}"
            )

            return

        try:

            image = Image.open(
                WALLPAPER_PATH
            )

            self.wallpaper = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(1536, 1024)
            )

            self.wallpaper_label = ctk.CTkLabel(
                self.frame,
                text="",
                image=self.wallpaper
            )

            self.wallpaper_label.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

            self.wallpaper_label.lower()

            print(
                "[MarwanaOS] Wallpaper loaded:"
                f" {image.width}x{image.height}"
            )

        except Exception as error:

            print(
                f"[MarwanaOS] Wallpaper error: {error}"
            )


    # ========================================================
    # DESKTOP UI
    # ========================================================

    def build_desktop(self):

        # ====================================================
        # TITLE
        # ====================================================

        title = ctk.CTkLabel(
            self.frame,
            text="MarwanaOS",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        title.place(
            x=35,
            y=30
        )


        subtitle = ctk.CTkLabel(
            self.frame,
            text="SYSTEM ONLINE",
            font=ctk.CTkFont(
                size=12
            ),
            text_color="#777777"
        )

        subtitle.place(
            x=38,
            y=72
        )


        # ====================================================
        # SYSTEM STATUS
        # ====================================================

        status = ctk.CTkFrame(
            self.frame,
            width=230,
            height=120,
            fg_color="#0D0D0D",
            corner_radius=15
        )

        status.place(
            relx=1.0,
            x=-35,
            y=30,
            anchor="ne"
        )


        ctk.CTkLabel(
            status,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#777777"
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 8)
        )


        ctk.CTkLabel(
            status,
            text="●  CORE ONLINE",
            text_color="#55CC88",
            font=("Consolas", 11)
        ).pack(
            anchor="w",
            padx=18,
            pady=2
        )


        ctk.CTkLabel(
            status,
            text="●  DISPLAY ONLINE",
            text_color="#55CC88",
            font=("Consolas", 11)
        ).pack(
            anchor="w",
            padx=18,
            pady=2
        )


        ctk.CTkLabel(
            status,
            text="●  PYTHON ONLINE",
            text_color="#55CC88",
            font=("Consolas", 11)
        ).pack(
            anchor="w",
            padx=18,
            pady=2
        )


        # ====================================================
        # TASKBAR
        # ====================================================

        self.taskbar = ctk.CTkFrame(
            self.frame,
            height=58,
            fg_color="#0B0B0B",
            corner_radius=0
        )

        self.taskbar.place(
            relx=0,
            rely=1,
            anchor="sw",
            relwidth=1
        )


        # ====================================================
        # MARWANAOS START BUTTON
        # ====================================================

        self.start_button = ctk.CTkButton(
            self.taskbar,
            text="MarwanaOS",
            width=150,
            height=40,
            corner_radius=8,
            fg_color="#151515",
            hover_color="#252525",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.toggle_start_menu
        )

        self.start_button.pack(
            side="left",
            padx=10,
            pady=9
        )


    # ========================================================
    # START MENU
    # ========================================================

    def toggle_start_menu(self):

        # ----------------------------------------------------
        # MENU BESTAAT → SLUITEN
        # ----------------------------------------------------

        if self.start_menu is not None:

            try:

                if self.start_menu.winfo_exists():

                    self.start_menu.destroy()
                    self.start_menu = None

                    return

            except Exception:

                self.start_menu = None


        # ----------------------------------------------------
        # MENU OPENEN
        # ----------------------------------------------------

        self.start_menu = ctk.CTkFrame(
            self.frame,
            width=300,
            height=430,
            fg_color="#0D0D0D",
            corner_radius=15,
            border_width=1,
            border_color="#252525"
        )

        self.start_menu.place(
            x=20,
            rely=1.0,
            y=-70,
            anchor="sw"
        )


        # ====================================================
        # TITLE
        # ====================================================

        ctk.CTkLabel(
            self.start_menu,
            text="MarwanaOS",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="#FFFFFF"
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 2)
        )


        ctk.CTkLabel(
            self.start_menu,
            text="APPLICATIONS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="#666666"
        ).pack(
            anchor="w",
            padx=23,
            pady=(0, 15)
        )


        # ====================================================
        # APPLICATIONS
        # ====================================================

        self.create_start_button(
            "🛡  Display Guard",
            self.open_display_guard
        )

        self.create_start_button(
            "📊  Task Manager",
            self.open_task_manager
        )

        self.create_start_button(
            "📈  System Monitor",
            self.open_system_monitor
        )

        self.create_start_button(
            "📁  File Manager",
            self.open_files
        )

        self.create_start_button(
            "⌨  Terminal",
            self.open_terminal
        )

        self.create_start_button(
            "⚙  Settings",
            self.open_settings
        )

        self.create_start_button(
            "⚡  AHK Center",
            self.open_ahk_center
        )


        # ====================================================
        # STATUS
        # ====================================================

        ctk.CTkLabel(
            self.start_menu,
            text="SYSTEM READY  ●",
            font=("Consolas", 10),
            text_color="#55CC88"
        ).pack(
            anchor="w",
            padx=27,
            pady=15
        )


    # ========================================================
    # START MENU BUTTON
    # ========================================================

    def create_start_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.start_menu,
            text=text,
            height=40,
            corner_radius=8,
            fg_color="#111111",
            hover_color="#1D1D1D",
            anchor="w",
            command=lambda: self.open_app(command)
        )

        button.pack(
            fill="x",
            padx=15,
            pady=3
        )


    # ========================================================
    # OPEN APP
    # ========================================================

    def open_app(
        self,
        command
    ):

        if self.start_menu is not None:

            try:
                self.start_menu.destroy()
            except Exception:
                pass

            self.start_menu = None

        command(self.master)


    # ========================================================
    # FRAME
    # ========================================================

    def get_frame(self):

        return self.frame


# ============================================================
# PUBLIC DESKTOP ENTRY POINT
# ============================================================

def create_desktop(
    master,
    open_display_guard,
    open_task_manager,
    open_system_monitor,
    open_files,
    open_terminal,
    open_settings,
    open_ahk_center
):

    desktop = Desktop(
        master,
        open_display_guard,
        open_task_manager,
        open_system_monitor,
        open_files,
        open_terminal,
        open_settings,
        open_ahk_center
    )

    return desktop