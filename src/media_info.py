"""Extract timestamp metadata from media files.

Parses image EXIF and video ffprobe metadata for renaming.
"""

import datetime
import math
import os
from typing import TypedDict

from exif import get_exif_of_image
from ffprobe import probe
from utils import is_already_renamed, split_stem_and_ext


class MediaInfo(TypedDict):
    """Timestamp metadata extracted from a media file.

    :ivar datetime: Datetime string in ``YYYYMMDD_HHMMSS`` format.
    :ivar milliseconds: Millisecond component used to ensure unique filenames.
    :ivar ext: Normalized lowercase file extension.
    """

    datetime: str
    milliseconds: int
    ext: str


def get_media_info(filepath: str) -> MediaInfo | None:
    """Extract timestamp metadata for renaming.

    Returns ``None`` for already-renamed files, unsupported formats,
    or when required metadata is missing.

    :param filepath: Path to the target file.
    :return: Extracted metadata, or ``None`` if unavailable.
    """
    stem, ext = split_stem_and_ext(os.path.basename(filepath))

    if is_already_renamed(stem):
        return None

    if ext in ["jpg", "jpeg"]:
        exif = get_exif_of_image(filepath)

        if "DateTimeOriginal" in exif:
            exif_dt = str(exif["DateTimeOriginal"])
            pic_date = exif_dt.replace(":", "").replace(" ", "_")
            return {"datetime": pic_date, "milliseconds": 0, "ext": "jpg"}

        return None

    if ext in ["mov"]:
        meta = probe(filepath)
        date = (
            meta.get("format", {})
            .get("tags", {})
            .get("com.apple.quicktime.creationdate")
        )

        if date is None:
            return None

        date = date.replace("-", "").replace("T", "_").replace(":", "").split("+")[0]

        return {"datetime": date, "milliseconds": 0, "ext": "mov"}

    if ext in ["mp4"]:
        meta = probe(filepath)

        meta_format = meta.get("format", {})
        duration = meta_format.get("duration")
        tags = meta_format.get("tags", {})

        date = tags.get("creation_time")

        if date is None:
            return None

        dt = datetime.datetime.fromisoformat(date)
        dt = dt + datetime.timedelta(hours=9)
        dt = dt - datetime.timedelta(seconds=int(math.ceil(float(duration))))
        dt = dt.strftime("%Y%m%d_%H%M%S")

        return {"datetime": dt, "milliseconds": 0, "ext": "mp4"}

    return None
