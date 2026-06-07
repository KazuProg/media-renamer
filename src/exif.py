"""Image EXIF extraction.

Reads EXIF tags embedded in image files using Pillow.
"""

from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_of_image(file: str) -> dict[str, object]:
    """Get EXIF data from an image.

    Returns an empty dict when EXIF is missing or cannot be read.

    :param file: Path to the target image file.
    :return: EXIF dict keyed by human-readable tag names.
    """
    im = Image.open(file)

    try:
        exif = im._getexif()  # type: ignore[attr-defined]
    except AttributeError:
        return {}

    if exif is None:
        return {}

    exif_table: dict[str, object] = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[str(tag)] = value

    return exif_table
