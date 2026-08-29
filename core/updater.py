import hashlib
import json
import urllib.request
from pathlib import Path

from core.version import get_version


VERSION_URL = (
    "https://raw.githubusercontent.com/"
    "marwana20/MarwanaOS/main/version.json"
)

MANIFEST_URL = (
    "https://raw.githubusercontent.com/"
    "marwana20/MarwanaOS/main/manifest.json"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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


def get_remote_manifest():
    """
    Haalt het update-manifest van GitHub op.
    """

    try:

        with urllib.request.urlopen(
            MANIFEST_URL,
            timeout=5
        ) as response:

            return json.loads(
                response.read().decode("utf-8")
            )

    except Exception as error:

        print(
            f"[Updater] Could not download manifest: {error}"
        )

        return None


def calculate_sha256(file_path):
    """
    Berekent de SHA-256 hash van een lokaal bestand.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def get_update_changes():
    """
    Vergelijkt de lokale bestanden met het GitHub-manifest.

    Geeft terug:
        modified = gewijzigde bestanden
        added    = nieuwe bestanden
        deleted  = verwijderde bestanden
    """

    remote_manifest = get_remote_manifest()

    if remote_manifest is None:
        return None

    remote_files = remote_manifest.get(
        "files",
        {}
    )

    local_files = {}


    # --------------------------------------------------------
    # LOKALE BESTANDEN INLEZEN
    # --------------------------------------------------------

    excluded_dirs = {
        ".git",
        "__pycache__",
        "tools"
    }

    excluded_files = {
        "manifest.json"
    }


    for file_path in PROJECT_ROOT.rglob("*"):

        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(
            PROJECT_ROOT
        )

        if any(
            part in excluded_dirs
            for part in relative_path.parts
        ):
            continue

        if relative_path.name in excluded_files:
            continue

        relative_path = str(
            relative_path
        ).replace(
            "\\",
            "/"
        )

        local_files[relative_path] = (
            calculate_sha256(file_path)
        )


    # --------------------------------------------------------
    # VERGELIJKEN
    # --------------------------------------------------------

    modified = []
    added = []
    deleted = []


    # Bestanden zowel lokaal als online
    for file_path, remote_hash in remote_files.items():

        if file_path not in local_files:

            added.append(
                file_path
            )

        elif local_files[file_path] != remote_hash:

            modified.append(
                file_path
            )


    # Bestanden die lokaal bestaan maar online niet meer
    for file_path in local_files:

        if file_path not in remote_files:

            deleted.append(
                file_path
            )


    return {
        "version": remote_manifest.get(
            "version",
            "0.0.0"
        ),
        "modified": modified,
        "added": added,
        "deleted": deleted
    }