"""Tests for ffprobe availability and probing."""

from unittest.mock import patch

import pytest

from ffprobe import is_ffprobe_available, probe


@patch("ffprobe.shutil.which")
def test_is_ffprobe_available(mock_which) -> None:
    mock_which.return_value = "/usr/bin/ffprobe"
    assert is_ffprobe_available() is True
    mock_which.assert_called_once_with("ffprobe")


@patch("ffprobe.shutil.which", return_value=None)
def test_is_ffprobe_not_available(mock_which) -> None:
    assert is_ffprobe_available() is False
    mock_which.assert_called_once_with("ffprobe")


@patch("ffprobe.shutil.which", return_value=None)
def test_probe_raises_when_ffprobe_missing(_mock_which) -> None:
    with pytest.raises(RuntimeError, match="ffprobe not found"):
        probe("/videos/clip.mp4")


@patch("ffprobe.ffmpeg.probe")
@patch("ffprobe.shutil.which", return_value="/usr/bin/ffprobe")
def test_probe_delegates_to_ffmpeg(mock_which, mock_ffmpeg_probe) -> None:
    mock_ffmpeg_probe.return_value = {"format": {}}

    result = probe("/videos/clip.mp4")

    assert result == {"format": {}}
    mock_which.assert_called_once_with("ffprobe")
    mock_ffmpeg_probe.assert_called_once_with("/videos/clip.mp4")
