import customtkinter as ctk


OPEN_WINDOWS = {}


def register_window(window, title):

    OPEN_WINDOWS[window] = {
        "title": title,
        "minimized": False,
        "maximized": False,
        "previous_geometry": window.geometry(),
        "taskbar_button": None
    }

    window.protocol(
        "WM_DELETE_WINDOW",
        lambda: close_managed_window(window)
    )

    update_taskbar()


def close_managed_window(window):

    if window not in OPEN_WINDOWS:
        return

    data = OPEN_WINDOWS[window]

    if data["taskbar_button"] is not None:

        try:
            data["taskbar_button"].destroy()
        except Exception:
            pass

    del OPEN_WINDOWS[window]

    try:
        window.destroy()
    except Exception:
        pass

    update_taskbar()


def minimize_window(window):

    if window not in OPEN_WINDOWS:
        return

    OPEN_WINDOWS[window]["minimized"] = True

    window.withdraw()

    update_taskbar()


def restore_window(window):

    if window not in OPEN_WINDOWS:
        return

    OPEN_WINDOWS[window]["minimized"] = False

    window.deiconify()
    window.lift()
    window.focus_force()

    update_taskbar()


def toggle_window(window):

    if window not in OPEN_WINDOWS:
        return

    if OPEN_WINDOWS[window]["minimized"]:

        restore_window(window)

    else:

        minimize_window(window)


def toggle_maximize(window, master):

    if window not in OPEN_WINDOWS:
        return

    data = OPEN_WINDOWS[window]

    if data["maximized"]:

        window.geometry(
            data["previous_geometry"]
        )

        data["maximized"] = False

    else:

        data["previous_geometry"] = (
            window.geometry()
        )

        window.geometry(
            f"{master.winfo_width()}x"
            f"{master.winfo_height()}"
        )

        data["maximized"] = True

    update_taskbar()


def update_taskbar():

    taskbar = globals().get("taskbar")

    if taskbar is None:
        return

    for widget in taskbar.winfo_children():

        if getattr(
            widget,
            "_marwana_window_button",
            False
        ):

            widget.destroy()

    for window, data in OPEN_WINDOWS.items():

        if not window.winfo_exists():
            continue

        button = ctk.CTkButton(
            taskbar,
            text=data["title"],
            width=140,
            height=38,
            corner_radius=7,
            fg_color=(
                "#202020"
                if not data["minimized"]
                else "#111111"
            ),
            hover_color="#292929",
            border_width=1,
            border_color="#303030",
            font=("Consolas", 11),
            command=lambda w=window: toggle_window(w)
        )

        button._marwana_window_button = True

        button.pack(
            side="left",
            padx=3,
            pady=11
        )

        data["taskbar_button"] = button


def set_taskbar(widget):

    globals()["taskbar"] = widget