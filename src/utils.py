"""Logic-independent utility functions.

Provides generic helpers such as filename parsing and renamed-file detection.
"""

import os
import re

RENAMED_PREFIX = re.compile(r"^\d{8}_\d{6}\.\d{3}")


def split_stem_and_ext(filename: str) -> tuple[str, str]:
    """Split a filename into stem and extension.

    :param filename: Filename without any directory path.
    :return: ``(stem, ext)`` tuple. ``ext`` is normalized to lowercase.
    """
    *parts, ext = re.split(r"\.", filename)
    stem = ".".join(parts)
    return stem, ext.lower()


def is_already_renamed(stem: str) -> bool:
    """Check whether a filename has already been renamed.

    :param stem: Filename without extension.
    :return: ``True`` if the stem starts with ``YYYYMMDD_HHMMSS.FFF``.
    """
    return RENAMED_PREFIX.match(stem) is not None


def resolve_unique_path(
    dirpath: str,
    datetime_str: str,
    milliseconds: int,
    original_name: str,
) -> tuple[str, str]:
    """Resolve a unique destination filename and path.

    Increments the millisecond counter when a file with the same name already exists.

    :param dirpath: Output directory.
    :param datetime_str: Datetime string in ``YYYYMMDD_HHMMSS`` format.
    :param milliseconds: Initial millisecond value embedded in the filename.
    :param original_name: Original filename including extension.
    :return: ``(new_name, new_path)`` tuple.
    """
    num = milliseconds
    while True:
        new_name = f"{datetime_str}.{str(num).zfill(3)}_{original_name}"
        new_path = os.path.join(dirpath, new_name)
        if not os.path.isfile(new_path):
            return new_name, new_path
        num += 1
