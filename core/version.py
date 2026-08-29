import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "version.json"


def get_version():

    try:

        with open(
            VERSION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "version",
            "0.0.0"
        )

    except Exception as error:

        print(
            f"[MarwanaOS] Version error: {error}"
        )

        return "0.0.0"