"""Video metadata probing via ffprobe.

Queries media file metadata through ``ffmpeg-python``.
"""

import shutil

import ffmpeg

_FFPROBE_CMD = "ffprobe"


def is_ffprobe_available() -> bool:
    """Return whether the ffprobe executable is on PATH."""
    return shutil.which(_FFPROBE_CMD) is not None


def probe(file: str) -> dict:
    """Probe a media file and return ffprobe metadata.

    :param file: Path to the file to probe.
    :return: Metadata dictionary returned by ffprobe.
    :raises RuntimeError: If ffprobe is not installed or not on PATH.
    """
    if not is_ffprobe_available():
        raise RuntimeError(
            "ffprobe not found. Install ffmpeg and ensure ffprobe is on PATH."
        )
    return ffmpeg.probe(file)
