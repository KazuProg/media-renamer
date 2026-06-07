"""Smoke tests."""

from main import main


def test_main_runs(capsys) -> None:
    main()
    assert "python-template" in capsys.readouterr().out
