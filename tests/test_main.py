"""Smoke tests."""

from unittest.mock import patch

from main import main


@patch("main.is_ffprobe_available", return_value=True)
def test_main_runs(_mock_ffprobe, capsys, tmp_path) -> None:
    exit_code = main(str(tmp_path))
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Start" in captured.out
    assert "Done: 0 renamed, 0 failed" in captured.out


@patch("main.is_ffprobe_available", return_value=False)
def test_main_exits_when_ffprobe_missing(_mock_ffprobe, capsys, tmp_path) -> None:
    exit_code = main(str(tmp_path))
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Start" not in captured.out
    assert "ffprobe not found" in captured.err
