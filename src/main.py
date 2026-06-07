"""Application entry point.

Provides a CLI that starts media file renaming.
"""

import os
import sys

from ffprobe import is_ffprobe_available
from rename import process_existing_files


def main(path: str | None = None) -> int:
    """Rename media files under the given path.

    :param path: Directory to process. Defaults to the current working directory.
    :return: ``1`` if any rename failed, otherwise ``0``.
    """
    if not is_ffprobe_available():
        print(
            "Error: ffprobe not found. Install ffmpeg and ensure ffprobe is on PATH.",
            file=sys.stderr,
        )
        return 1

    target = path if path is not None else os.getcwd()
    print("Start")
    return 1 if process_existing_files(target) else 0


if __name__ == "__main__":
    cli_path = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(main(cli_path))
