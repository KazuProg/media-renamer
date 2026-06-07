"""Tests for media metadata extraction."""

from unittest.mock import patch

from media_info import get_media_info


def test_get_media_info_skips_already_renamed() -> None:
    assert get_media_info("/photos/20240607_153045.000_IMG_1234.jpg") is None


def test_get_media_info_unsupported_extension() -> None:
    assert get_media_info("/photos/document.pdf") is None


@patch("media_info.get_exif_of_image")
def test_get_media_info_jpg_from_exif(mock_get_exif) -> None:
    mock_get_exif.return_value = {"DateTimeOriginal": "2024:06:07 15:30:45"}

    result = get_media_info("/photos/IMG_1234.JPG")

    assert result == {
        "datetime": "20240607_153045",
        "milliseconds": 0,
        "ext": "jpg",
    }


@patch("media_info.get_exif_of_image")
def test_get_media_info_jpg_without_datetime(mock_get_exif) -> None:
    mock_get_exif.return_value = {}

    assert get_media_info("/photos/IMG_1234.jpg") is None


@patch("media_info.probe")
def test_get_media_info_mov(mock_probe) -> None:
    mock_probe.return_value = {
        "format": {
            "tags": {"com.apple.quicktime.creationdate": "2024-06-07T15:30:45+09:00"}
        }
    }

    result = get_media_info("/videos/clip.MOV")

    assert result == {
        "datetime": "20240607_153045",
        "milliseconds": 0,
        "ext": "mov",
    }


@patch("media_info.probe")
def test_get_media_info_mov_without_creation_date(mock_probe) -> None:
    mock_probe.return_value = {"format": {"tags": {}}}

    assert get_media_info("/videos/clip.mov") is None


@patch("media_info.probe")
def test_get_media_info_mp4_start_time_from_duration(mock_probe) -> None:
    mock_probe.return_value = {
        "format": {
            "duration": "10.2",
            "tags": {"creation_time": "2024-06-07T06:30:45"},
        }
    }

    result = get_media_info("/videos/clip.mp4")

    assert result == {
        "datetime": "20240607_153034",
        "milliseconds": 0,
        "ext": "mp4",
    }


@patch("media_info.probe")
def test_get_media_info_mp4_without_creation_time(mock_probe) -> None:
    mock_probe.return_value = {"format": {"duration": "10.0", "tags": {}}}

    assert get_media_info("/videos/clip.mp4") is None
