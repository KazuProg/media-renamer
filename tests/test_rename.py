"""Tests for rename processing."""

from unittest.mock import patch

from media_info import MediaInfo
from rename import process_existing_files, rename_file


def test_rename_file_dry_run_does_not_move(tmp_path) -> None:
    file_path = tmp_path / "IMG_1234.JPG"
    file_path.write_bytes(b"fake")
    media_info: MediaInfo = {
        "datetime": "20240607_153045",
        "milliseconds": 0,
        "ext": "jpg",
    }

    assert rename_file(str(file_path), media_info, dry_run=True) is True
    assert file_path.exists()
    assert file_path.name == "IMG_1234.JPG"


def test_rename_file_moves_when_not_dry_run(tmp_path) -> None:
    file_path = tmp_path / "IMG_1234.JPG"
    file_path.write_bytes(b"fake")
    media_info: MediaInfo = {
        "datetime": "20240607_153045",
        "milliseconds": 0,
        "ext": "jpg",
    }

    assert rename_file(str(file_path), media_info, dry_run=False) is True
    assert not file_path.exists()
    assert (tmp_path / "20240607_153045.000_IMG_1234.jpg").exists()


@patch("rename.get_media_info")
def test_process_existing_files_dry_run_summary(
    mock_get_media_info, capsys, tmp_path
) -> None:
    file_path = tmp_path / "IMG_1234.JPG"
    file_path.write_bytes(b"fake")
    mock_get_media_info.return_value = {
        "datetime": "20240607_153045",
        "milliseconds": 0,
        "ext": "jpg",
    }

    failed = process_existing_files(str(tmp_path), dry_run=True)
    captured = capsys.readouterr()

    assert failed == 0
    assert mock_get_media_info.call_count == 1
    assert "Done (dry run): 1 would rename, 0 failed" in captured.out
    assert file_path.name == "IMG_1234.JPG"
