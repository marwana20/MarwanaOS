import customtkinter as ctk

from core.system import get_system_stats, format_uptime, get_processes
from core.window_manager import register_window


def open_system_monitor(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // SYSTEM MONITOR"
    )

    window.geometry(
        "850x680"
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
        "SYSTEM MONITOR"
    )

    # ========================================================
    # SYSTEM OVERVIEW
    # ========================================================

    info_frame = ctk.CTkFrame(
        window,
        fg_color="#0D0D0D",
        corner_radius=15
    )

    info_frame.pack(
        padx=30,
        pady=20,
        fill="x"
    )

    # ========================================================
    # CPU
    # ========================================================

    cpu_value = ctk.CTkLabel(
        info_frame,
        text="CPU       0.0%",
        font=("Consolas", 14),
        text_color="#AAAAAA"
    )

    cpu_value.pack(
        anchor="w",
        padx=20,
        pady=(15, 3)
    )

    cpu_bar = ctk.CTkProgressBar(
        info_frame,
        width=700
    )

    cpu_bar.pack(
        padx=20,
        pady=(0, 10)
    )

    # ========================================================
    # RAM
    # ========================================================

    ram_value = ctk.CTkLabel(
        info_frame,
        text="RAM       0.0%",
        font=("Consolas", 14),
        text_color="#AAAAAA"
    )

    ram_value.pack(
        anchor="w",
        padx=20,
        pady=3
    )

    ram_bar = ctk.CTkProgressBar(
        info_frame,
        width=700
    )

    ram_bar.pack(
        padx=20,
        pady=(0, 10)
    )

    # ========================================================
    # DISK
    # ========================================================

    disk_value = ctk.CTkLabel(
        info_frame,
        text="DISK      0.0%",
        font=("Consolas", 14),
        text_color="#AAAAAA"
    )

    disk_value.pack(
        anchor="w",
        padx=20,
        pady=3
    )

    disk_bar = ctk.CTkProgressBar(
        info_frame,
        width=700
    )

    disk_bar.pack(
        padx=20,
        pady=(0, 10)
    )

    # ========================================================
    # UPTIME
    # ========================================================

    uptime_value = ctk.CTkLabel(
        info_frame,
        text="UPTIME    --:--:--",
        font=("Consolas", 14),
        text_color="#777777"
    )

    uptime_value.pack(
        anchor="w",
        padx=20,
        pady=(3, 15)
    )

    # ========================================================
    # PROCESSES
    # ========================================================

    process_title = ctk.CTkLabel(
        window,
        text="RUNNING PROCESSES",
        font=("Arial", 18, "bold"),
        text_color="#FFFFFF"
    )

    process_title.pack(
        anchor="w",
        padx=30,
        pady=(5, 8)
    )

    process_frame = ctk.CTkScrollableFrame(
        window,
        width=770,
        height=230,
        fg_color="#0D0D0D",
        corner_radius=12
    )

    process_frame.pack(
        padx=30,
        fill="both",
        expand=True
    )

    # ========================================================
    # PROCESS LIST
    # ========================================================

    def refresh_processes():

        if not window.winfo_exists():
            return

        for widget in process_frame.winfo_children():
            widget.destroy()

        processes = get_processes()

        for process in processes[:30]:

            row = ctk.CTkFrame(
                process_frame,
                fg_color="#111111",
                corner_radius=7,
                height=38
            )

            row.pack(
                fill="x",
                pady=2
            )

            row.pack_propagate(False)

            name_label = ctk.CTkLabel(
                row,
                text=process["name"],
                font=("Consolas", 11),
                text_color="#FFFFFF",
                anchor="w"
            )

            name_label.pack(
                side="left",
                padx=12,
                fill="x",
                expand=True
            )

            pid_label = ctk.CTkLabel(
                row,
                text=f"PID {process['pid']}",
                font=("Consolas", 10),
                text_color="#666666"
            )

            pid_label.pack(
                side="left",
                padx=10
            )

            memory_label = ctk.CTkLabel(
                row,
                text=f"{process['memory']:.1f} MB",
                font=("Consolas", 10),
                text_color="#AAAAAA",
                width=100
            )

            memory_label.pack(
                side="right",
                padx=10
            )

    # ========================================================
    # REFRESH BUTTON
    # ========================================================

    refresh_button = ctk.CTkButton(
        window,
        text="⟳  REFRESH PROCESSES",
        width=220,
        height=38,
        corner_radius=8,
        command=refresh_processes
    )

    refresh_button.pack(
        pady=12
    )

    # ========================================================
    # LIVE SYSTEM STATS
    # ========================================================

    def update_stats():

        if not window.winfo_exists():
            return

        stats = get_system_stats()

        cpu = stats["cpu"]
        ram = stats["ram"]
        disk = stats["disk"]
        uptime = stats["uptime"]

        # CPU

        cpu_value.configure(
            text=f"CPU       {cpu:.1f}%"
        )

        cpu_bar.set(
            cpu / 100
        )

        # RAM

        ram_value.configure(
            text=(
                f"RAM       {ram.percent:.1f}%  "
                f"({ram.used / (1024 ** 3):.1f} GB / "
                f"{ram.total / (1024 ** 3):.1f} GB)"
            )
        )

        ram_bar.set(
            ram.percent / 100
        )

        # DISK

        if disk:

            disk_value.configure(
                text=f"DISK      {disk.percent:.1f}%"
            )

            disk_bar.set(
                disk.percent / 100
            )

        # UPTIME

        uptime_value.configure(
            text=(
                f"UPTIME    "
                f"{format_uptime(uptime)}"
            )
        )

        window.after(
            1000,
            update_stats
        )

    # ========================================================
    # INITIALIZE
    # ========================================================

    refresh_processes()
    update_stats()