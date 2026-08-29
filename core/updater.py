import json
import urllib.request

from core.version import get_version


VERSION_URL = (
    "https://raw.githubusercontent.com/"
    "marwana20/MarwanaOS/main/version.json"
)


def get_latest_version():
    """
    Haalt de nieuwste MarwanaOS-versie op vanaf GitHub.
    """

    try:

        with urllib.request.urlopen(
            VERSION_URL,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        return data.get(
            "version",
            None
        )

    except Exception as error:

        print(
            f"[Updater] Could not check for updates: {error}"
        )

        return None


def is_update_available():
    """
    Controleert of er een nieuwere versie beschikbaar is.
    """

    current_version = get_version()
    latest_version = get_latest_version()

    if latest_version is None:
        return False

    try:

        current = tuple(
            int(part)
            for part in current_version.split(".")
        )

        latest = tuple(
            int(part)
            for part in latest_version.split(".")
        )

        return latest > current

    except (ValueError, AttributeError):

        print(
            "[Updater] Invalid version format."
        )

        return False