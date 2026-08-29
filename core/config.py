from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "marwanaos.json"

ASSETS_DIR = PROJECT_ROOT / "assets"
WALLPAPER_PATH = ASSETS_DIR / "wallpaper.png"


DEFAULT_CONFIG = {
    "appearance": "dark",

    "wallpaper": "wallpaper.png",

    "hotkey": "<Alt-a>",

    "display_guard": {
        "privacy_enabled": True,
        "power_guard_enabled": True,
        "auto_extend": False,
        "blocked_apps": [
            "WhatsApp",
            "Teams",
            "Discord",
            "Outlook",
            "Telegram",
            "Signal"
        ]
    }
}


def load_config():

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not CONFIG_FILE.exists():

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG.copy()

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        config = DEFAULT_CONFIG.copy()

        config.update(data)

        return config

    except Exception as error:

        print(
            f"[MarwanaOS] Config error: {error}"
        )

        return DEFAULT_CONFIG.copy()


def save_config(config):

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )
