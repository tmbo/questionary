import os
import sys
from pathlib import Path
from typing import Optional
from typing import Text

import toml

version_file_path = Path("questionary/version.py")

pyproject_file_path = Path("pyproject.toml")


def get_pyproject_version():
    """Return the project version specified in the poetry build configuration."""
    data = toml.load(pyproject_file_path)
    return data["tool"]["poetry"]["version"]


def get_current_version() -> Text:
    """Return the current library version as specified in the code."""

    if not version_file_path.is_file():
        raise FileNotFoundError(
            f"Failed to find version file at {version_file_path().absolute()}"
        )

    # context in which we evaluate the version py -
    # to be able to access the defined version, it already needs to live in the
    # context passed to exec
    _globals = {"__version__": ""}
    with open(version_file_path) as f:
        exec(f.read(), _globals)

    return _globals["__version__"]


def get_tagged_version() -> Optional[Text]:
    """Return the version specified in a tagged git commit."""
    return os.environ.get("TRAVIS_TAG")


if __name__ == "__main__":
    if get_pyproject_version() != get_current_version():
        print(
            f"Version in {pyproject_file_path} does not correspond "
            f"to the version in {version_file_path}! The version needs to be "
            f"set to the same value in both places."
        )
        sys.exit(1)
    elif get_tagged_version() and get_tagged_version() != get_current_version():
        print(
            f"Tagged version does not correspond to the version "
            f"in {version_file_path}!"
        )
        sys.exit(1)
    elif get_tagged_version() and get_tagged_version() != get_pyproject_version():
        print(
            f"Tagged version does not correspond to the version "
            f"in {pyproject_file_path}!"
        )
        sys.exit(1)
    else:
        print("Versions look good!")
