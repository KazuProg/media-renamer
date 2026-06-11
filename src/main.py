"""Application entry point.

Provides a CLI that starts media file renaming.
"""

import argparse
import os
import sys

from ffprobe import is_ffprobe_available
from rename import process_existing_files


def main(path: str | None = None, *, dry_run: bool = False) -> int:
    """Rename media files under the given path.

    :param path: Directory to process. Defaults to the current working directory.
    :param dry_run: When ``True``, preview renames without modifying files.
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
    if dry_run:
        print("Dry run")
    return 1 if process_existing_files(target, dry_run=dry_run) else 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rename media files from metadata timestamps.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Directory to process (default: current working directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview renames without modifying files",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(args.path, dry_run=args.dry_run))
