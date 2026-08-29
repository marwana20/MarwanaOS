import customtkinter as ctk


class StartMenu:

    def __init__(
        self,
        desktop,
        open_files,
        open_terminal,
        open_system_monitor,
        open_ahk_center,
        open_settings,
        open_task_manager,
        open_display_guard
    ):

        self.desktop = desktop
        self.menu = None

        self.open_files = open_files
        self.open_terminal = open_terminal
        self.open_system_monitor = open_system_monitor
        self.open_ahk_center = open_ahk_center
        self.open_settings = open_settings
        self.open_task_manager = open_task_manager
        self.open_display_guard = open_display_guard


    def toggle(self):

        if self.menu is not None:

            self.close()

        else:

            self.open()


    def close(self):

        if self.menu is not None:

            try:
                self.menu.destroy()
            except Exception:
                pass

            self.menu = None


    def open(self):

        self.menu = ctk.CTkFrame(
            self.desktop,
            width=330,
            height=470,
            fg_color="#0C0C0C",
            corner_radius=16,
            border_width=1,
            border_color="#292929"
        )

        self.menu.place(
            x=15,
            rely=1.0,
            y=-75,
            anchor="sw"
        )

        title = ctk.CTkLabel(
            self.menu,
            text="MarwanaOS",
            font=("Arial", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(22, 2)
        )

        subtitle = ctk.CTkLabel(
            self.menu,
            text="SYSTEM MENU",
            font=("Consolas", 11),
            text_color="#666666"
        )

        subtitle.pack(
            anchor="w",
            padx=27,
            pady=(0, 15)
        )

        self.add_button(
            "📁   File Manager",
            self.open_files
        )

        self.add_button(
            "⌨   Terminal",
            self.open_terminal
        )

        self.add_button(
            "📊   System Monitor",
            self.open_system_monitor
        )

        self.add_button(
            "⌨   AHK Center",
            self.open_ahk_center
        )

        self.add_button(
            "⚙   Settings",
            self.open_settings
        )

        self.add_button(
            "🛡   Display Guard",
            self.open_display_guard
        )

        self.add_button(
            "🖥   Task Manager",
            self.open_task_manager
        )

        status = ctk.CTkLabel(
            self.menu,
            text="SYSTEM READY  ●",
            font=("Consolas", 10),
            text_color="#55CC88"
        )

        status.pack(
            anchor="w",
            padx=27,
            pady=15
        )


    def add_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.menu,
            text=text,
            anchor="w",
            height=43,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1B1B1B",
            font=("Arial", 13),
            command=lambda: (
                self.close(),
                command()
            )
        )

        button.pack(
            fill="x",
            padx=15,
            pady=2
        )