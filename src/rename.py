"""Rename media files based on extracted metadata.

Embeds timestamp information into filenames and assigns unique names on collision.
"""

import os
import shutil

from media_info import get_media_info
from utils import resolve_unique_path, split_stem_and_ext


def rename_file(file_path: str, *, dry_run: bool = False) -> bool:
    """Rename a single media file.

    :param file_path: Path to the file to rename.
    :param dry_run: When ``True``, preview renames without modifying files.
    :return: ``True`` when processing finishes; ``False`` on exception.
    """
    try:
        dirpath, file = os.path.split(file_path)
        if not dry_run:
            os.chmod(file_path, 0o666)
        media_info = get_media_info(file_path)
        if media_info is None:
            print("NoMediaInfo")
            return True

        stem, _ = split_stem_and_ext(file)
        original_name = f"{stem}.{media_info['ext']}"
        new_name, new_path = resolve_unique_path(
            dirpath,
            media_info["datetime"],
            media_info["milliseconds"],
            original_name,
        )
        print(file + " -> " + new_name)
        if not dry_run:
            shutil.move(file_path, new_path)
        return True
    except Exception:
        return False


def process_existing_files(path: str, *, dry_run: bool = False) -> int:
    """Process all unrenamed files under the given directory.

    :param path: Root directory to walk.
    :param dry_run: When ``True``, preview renames without modifying files.
    :return: Number of files that failed to rename.
    """
    renamed = 0
    failed = 0
    for root, _, files in os.walk(path):
        for filename in sorted(files):
            file_path = os.path.join(root, filename)
            if not os.path.isfile(file_path):
                continue
            if get_media_info(file_path) is None:
                continue
            print(f"Processing: {file_path}")
            if rename_file(file_path, dry_run=dry_run):
                renamed += 1
            else:
                failed += 1
    if dry_run:
        print(f"Done (dry run): {renamed} would rename, {failed} failed")
    else:
        print(f"Done: {renamed} renamed, {failed} failed")
    return failed
