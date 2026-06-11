"""Smoke tests."""

from unittest.mock import patch

from main import _parse_args, main


@patch("main.is_ffprobe_available", return_value=True)
def test_main_runs(_mock_ffprobe, capsys, tmp_path) -> None:
    exit_code = main(str(tmp_path))
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Start" in captured.out
    assert "Done: 0 renamed, 0 failed" in captured.out


@patch("main.is_ffprobe_available", return_value=True)
def test_main_dry_run(_mock_ffprobe, capsys, tmp_path) -> None:
    exit_code = main(str(tmp_path), dry_run=True)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Dry run" in captured.out
    assert "Done (dry run): 0 would rename, 0 failed" in captured.out


def test_parse_args_no_args() -> None:
    args = _parse_args([])
    assert args.path is None
    assert args.dry_run is False


def test_parse_args_dry_run_only() -> None:
    args = _parse_args(["--dry-run"])
    assert args.path is None
    assert args.dry_run is True


def test_parse_args_dry_run_with_path() -> None:
    args = _parse_args(["--dry-run", "/tmp/media"])
    assert args.dry_run is True
    assert args.path == "/tmp/media"


def test_parse_args_path_only() -> None:
    args = _parse_args(["/tmp/media"])
    assert args.dry_run is False
    assert args.path == "/tmp/media"


def test_parse_args_path_after_flag() -> None:
    args = _parse_args(["/tmp/media", "--dry-run"])
    assert args.dry_run is True
    assert args.path == "/tmp/media"


@patch("main.is_ffprobe_available", return_value=False)
def test_main_exits_when_ffprobe_missing(_mock_ffprobe, capsys, tmp_path) -> None:
    exit_code = main(str(tmp_path))
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Start" not in captured.out
    assert "ffprobe not found" in captured.err
