import customtkinter as ctk
import psutil

from core.window_manager import register_window


def open_task_manager(app):

    window = ctk.CTkToplevel(app)

    window.title(
        "MarwanaOS // TASK MANAGER"
    )

    window.geometry(
        "850x600"
    )

    window.configure(
        fg_color="#090909"
    )

    register_window(
        window,
        "TASK MANAGER"
    )

    # ========================================================
    # TITLE
    # ========================================================

    title = ctk.CTkLabel(
        window,
        text="TASK MANAGER",
        font=("Arial", 22, "bold"),
        text_color="#FFFFFF"
    )

    title.pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    subtitle = ctk.CTkLabel(
        window,
        text="Running processes",
        font=("Arial", 12),
        text_color="#666666"
    )

    subtitle.pack(
        anchor="w",
        padx=30,
        pady=(0, 20)
    )

    # ========================================================
    # PROCESS FRAME
    # ========================================================

    process_frame = ctk.CTkScrollableFrame(
        window,
        fg_color="#0D0D0D"
    )

    process_frame.pack(
        padx=30,
        pady=5,
        fill="both",
        expand=True
    )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh():

        if not window.winfo_exists():
            return

        for widget in process_frame.winfo_children():
            widget.destroy()

        processes = []

        try:

            for process in psutil.process_iter(
                ["pid", "name", "memory_info"]
            ):

                try:

                    memory = (
                        process.info["memory_info"].rss
                        / (1024 * 1024)
                    )

                    processes.append({
                        "pid": process.info["pid"],
                        "name": process.info["name"] or "Unknown",
                        "memory": memory
                    })

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess
                ):
                    continue

        except Exception:
            return

        processes.sort(
            key=lambda x: x["memory"],
            reverse=True
        )

        for process in processes[:50]:

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

            name = ctk.CTkLabel(
                row,
                text=process["name"],
                font=("Consolas", 11),
                text_color="#FFFFFF",
                anchor="w"
            )

            name.pack(
                side="left",
                padx=12,
                fill="x",
                expand=True
            )

            pid = ctk.CTkLabel(
                row,
                text=f"PID {process['pid']}",
                font=("Consolas", 10),
                text_color="#666666"
            )

            pid.pack(
                side="left",
                padx=10
            )

            memory = ctk.CTkLabel(
                row,
                text=f"{process['memory']:.1f} MB",
                font=("Consolas", 10),
                text_color="#AAAAAA",
                width=100
            )

            memory.pack(
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
        command=refresh
    )

    refresh_button.pack(
        pady=15
    )

    # ========================================================
    # INITIAL LOAD
    # ========================================================

    refresh()