import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "version.json"
MANIFEST_FILE = PROJECT_ROOT / "manifest.json"


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "tools"
}


EXCLUDED_FILES = {
    "manifest.json"
}


def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def generate_manifest():

    with open(
        VERSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        version_data = json.load(file)


    version = version_data.get(
        "version",
        "0.0.0"
    )


    files = {}


    for file_path in PROJECT_ROOT.rglob("*"):

        if not file_path.is_file():
            continue


        relative_path = file_path.relative_to(
            PROJECT_ROOT
        )


        if any(
            part in EXCLUDED_DIRS
            for part in relative_path.parts
        ):
            continue


        if relative_path.name in EXCLUDED_FILES:
            continue


        files[str(relative_path).replace("\\", "/")] = (
            calculate_sha256(file_path)
        )


    manifest = {
        "version": version,
        "files": files
    }


    with open(
        MANIFEST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4
        )


    print(
        f"Manifest generated for MarwanaOS {version}"
    )

    print(
        f"Files tracked: {len(files)}"
    )


if __name__ == "__main__":
    generate_manifest()