import customtkinter as ctk
import time


# ============================================================
# MARWANAOS BOOT SEQUENCE
# ============================================================

def create_boot_screen(app, on_complete):

    frame = ctk.CTkFrame(
        app,
        fg_color="#050607",
        corner_radius=0
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # ========================================================
    # HEADER
    # ========================================================

    header = ctk.CTkFrame(
        frame,
        fg_color="transparent"
    )

    header.place(
        x=45,
        y=35
    )

    ctk.CTkLabel(
        header,
        text="MARWANAOS",
        font=ctk.CTkFont(
            family="Arial",
            size=13,
            weight="bold"
        ),
        text_color="#B8B8B8"
    ).pack(
        anchor="w"
    )

    ctk.CTkLabel(
        header,
        text="PERSONAL COMPUTING SYSTEM",
        font=ctk.CTkFont(
            family="Consolas",
            size=9
        ),
        text_color="#555555"
    ).pack(
        anchor="w",
        pady=(2, 0)
    )

    # ========================================================
    # MISSION IDENTIFIER
    # ========================================================

    mission = ctk.CTkLabel(
        frame,
        text="MROW-01  /  SYSTEM BOOT",
        font=ctk.CTkFont(
            family="Consolas",
            size=10
        ),
        text_color="#555555"
    )

    mission.place(
        relx=1.0,
        x=-45,
        y=40,
        anchor="ne"
    )

    # ========================================================
    # CENTER
    # ========================================================

    center = ctk.CTkFrame(
        frame,
        fg_color="transparent"
    )

    center.place(
        relx=0.5,
        rely=0.45,
        anchor="center"
    )

    # Main title

    title = ctk.CTkLabel(
        center,
        text="MARWANAOS",
        font=ctk.CTkFont(
            family="Arial",
            size=46,
            weight="bold"
        ),
        text_color="#F2F2F2"
    )

    title.pack()

    # Thin technical line

    line = ctk.CTkFrame(
        center,
        width=420,
        height=1,
        fg_color="#303030",
        corner_radius=0
    )

    line.pack(
        pady=(14, 12)
    )

    subtitle = ctk.CTkLabel(
        center,
        text="SYSTEM INITIALIZATION",
        font=ctk.CTkFont(
            family="Consolas",
            size=12
        ),
        text_color="#777777"
    )

    subtitle.pack()

    # ========================================================
    # STATUS
    # ========================================================

    status_frame = ctk.CTkFrame(
        center,
        fg_color="transparent"
    )

    status_frame.pack(
        pady=(45, 0)
    )

    status_prefix = ctk.CTkLabel(
        status_frame,
        text="STATUS",
        font=ctk.CTkFont(
            family="Consolas",
            size=9,
            weight="bold"
        ),
        text_color="#555555"
    )

    status_prefix.pack(
        side="left",
        padx=(0, 12)
    )

    status = ctk.CTkLabel(
        status_frame,
        text="INITIALIZING",
        font=ctk.CTkFont(
            family="Consolas",
            size=11
        ),
        text_color="#AAAAAA"
    )

    status.pack(
        side="left"
    )

    # ========================================================
    # PROGRESS
    # ========================================================

    progress_frame = ctk.CTkFrame(
        center,
        fg_color="#151515",
        width=460,
        height=3,
        corner_radius=0
    )

    progress_frame.pack(
        pady=(18, 0)
    )

    progress_frame.pack_propagate(False)

    progress = ctk.CTkProgressBar(
        progress_frame,
        width=460,
        height=3,
        corner_radius=0,
        fg_color="#151515",
        progress_color="#BDBDBD"
    )

    progress.set(0)

    progress.pack(
        fill="both",
        expand=True
    )

    # ========================================================
    # PERCENTAGE
    # ========================================================

    percentage = ctk.CTkLabel(
        center,
        text="00%",
        font=ctk.CTkFont(
            family="Consolas",
            size=10
        ),
        text_color="#666666"
    )

    percentage.pack(
        pady=(10, 0)
    )

    # ========================================================
    # LOWER SYSTEM INFORMATION
    # ========================================================

    info = ctk.CTkFrame(
        frame,
        fg_color="transparent"
    )

    info.place(
        x=45,
        rely=1.0,
        y=-38,
        anchor="sw"
    )

    ctk.CTkLabel(
        info,
        text="CORE 01",
        font=ctk.CTkFont(
            family="Consolas",
            size=9
        ),
        text_color="#444444"
    ).pack(
        side="left",
        padx=(0, 25)
    )

    ctk.CTkLabel(
        info,
        text="DISPLAY ENGINE",
        font=ctk.CTkFont(
            family="Consolas",
            size=9
        ),
        text_color="#444444"
    ).pack(
        side="left",
        padx=(0, 25)
    )

    ctk.CTkLabel(
        info,
        text="SECURITY",
        font=ctk.CTkFont(
            family="Consolas",
            size=9
        ),
        text_color="#444444"
    ).pack(
        side="left"
    )

    # ========================================================
    # VERSION
    # ========================================================

    version = ctk.CTkLabel(
        frame,
        text="BUILD 0.5  •  2026",
        font=ctk.CTkFont(
            family="Consolas",
            size=9
        ),
        text_color="#444444"
    )

    version.place(
        relx=1.0,
        rely=1.0,
        x=-45,
        y=-38,
        anchor="se"
    )

    # ========================================================
    # BOOT STEPS
    # ========================================================

    steps = [
        ("INITIALIZING KERNEL", 0.12),
        ("LOADING SYSTEM CORE", 0.25),
        ("CHECKING MEMORY", 0.38),
        ("INITIALIZING DISPLAY ENGINE", 0.51),
        ("CONNECTING WINDOWS", 0.64),
        ("STARTING SYSTEM MONITOR", 0.77),
        ("LOADING USER INTERFACE", 0.90),
        ("SYSTEM READY", 1.00),
    ]

    # ========================================================
    # BOOT ANIMATION
    # ========================================================

    def run_step(index=0):

        if index >= len(steps):

            status.configure(
                text="SYSTEM READY",
                text_color="#D0D0D0"
            )

            percentage.configure(
                text="100%",
                text_color="#888888"
            )

            # Kleine pauze voordat desktop verschijnt.
            app.after(
                650,
                finish
            )

            return

        text, value = steps[index]

        status.configure(
            text=text
        )

        percentage.configure(
            text=f"{int(value * 100):02d}%"
        )

        progress.set(
            value
        )

        # Kleine variatie zodat het niet mechanisch voelt.
        delays = [
            320,
            360,
            300,
            420,
            340,
            390,
            430,
            500
        ]

        delay = delays[
            min(index, len(delays) - 1)
        ]

        app.after(
            delay,
            lambda: run_step(index + 1)
        )

    # ========================================================
    # FINISH
    # ========================================================

    def finish():

        try:

            frame.pack_forget()

        except Exception:

            pass

        on_complete()

    # ========================================================
    # START
    # ========================================================

    app.after(
        350,
        run_step
    )

    return frame