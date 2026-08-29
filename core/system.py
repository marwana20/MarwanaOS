import os
import psutil
import time


def get_system_stats():

    cpu = psutil.cpu_percent(
        interval=None
    )

    ram = psutil.virtual_memory()

    try:

        disk = psutil.disk_usage(
            os.environ["SystemDrive"] + "\\"
        )

    except Exception:

        disk = None

    boot_time = psutil.boot_time()

    uptime_seconds = (
        time.time() - boot_time
    )

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "uptime": uptime_seconds
    }


def format_uptime(seconds):

    hours = int(
        seconds // 3600
    )

    minutes = int(
        (seconds % 3600) // 60
    )

    seconds = int(
        seconds % 60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


def get_processes():

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info", "status"]
    ):

        try:

            info = process.info

            memory_info = info.get(
                "memory_info"
            )

            if memory_info is None:
                continue

            memory_mb = (
                memory_info.rss
                / (1024 * 1024)
            )

            processes.append({
                "name": info.get("name") or "Unknown",
                "pid": info.get("pid"),
                "memory": memory_mb,
                "status": info.get("status") or "unknown"
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

    processes.sort(
        key=lambda p: p["memory"],
        reverse=True
    )

    return processes