"""Tests for filename utilities."""

from utils import is_already_renamed, resolve_unique_path, split_stem_and_ext


def test_split_stem_and_ext_simple() -> None:
    assert split_stem_and_ext("photo.jpg") == ("photo", "jpg")


def test_split_stem_and_ext_multiple_dots() -> None:
    assert split_stem_and_ext("archive.tar.gz") == ("archive.tar", "gz")


def test_split_stem_and_ext_lowercases_extension() -> None:
    assert split_stem_and_ext("IMG_1234.JPG") == ("IMG_1234", "jpg")


def test_is_already_renamed_true() -> None:
    assert is_already_renamed("20240607_153045.000_IMG_1234") is True


def test_is_already_renamed_false() -> None:
    assert is_already_renamed("IMG_1234") is False


def test_is_already_renamed_missing_milliseconds() -> None:
    assert is_already_renamed("20240607_153045_IMG_1234") is False


def test_resolve_unique_path_no_collision(tmp_path) -> None:
    name, path = resolve_unique_path(
        str(tmp_path),
        "20240607_153045",
        0,
        "photo.jpg",
    )
    assert name == "20240607_153045.000_photo.jpg"
    assert path == str(tmp_path / name)


def test_resolve_unique_path_increments_on_collision(tmp_path) -> None:
    existing = tmp_path / "20240607_153045.000_photo.jpg"
    existing.write_bytes(b"")

    name, path = resolve_unique_path(
        str(tmp_path),
        "20240607_153045",
        0,
        "photo.jpg",
    )
    assert name == "20240607_153045.001_photo.jpg"
    assert path == str(tmp_path / name)
