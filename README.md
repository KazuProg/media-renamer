# media-renamer

メディアファイルのメタデータから撮影日時を読み取り、ファイル名を一括リネームする CLI ツール。

## 概要

指定ディレクトリ（引数省略時はカレントディレクトリ）以下を再帰的に走査し、メタデータから日時を取得できるファイルだけをリネームします。すでにリネーム済みと判定されたファイルはスキップします。

## 対応形式

| 拡張子 | 参照メタデータ |
| --- | --- |
| `jpg` / `jpeg` | EXIF `DateTimeOriginal` |
| `mov` | ffprobe `com.apple.quicktime.creationdate` |
| `mp4` | ffprobe `creation_time`（動画長を考慮して開始時刻を算出） |

## リネーム形式

```
YYYYMMDD_HHMMSS.FFF_{original}
```

例: `IMG_1234.JPG` → `20240607_153045.000_IMG_1234.jpg`

拡張子は小文字に統一します（`JPEG` → `jpg` など）。

同名ファイルが存在する場合はミリ秒部分（`.000`, `.001`, ...）をインクリメントして衝突を回避します。

## 前提条件

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/)
- `ffmpeg`（`ffprobe` コマンドが PATH から実行できること）

## セットアップ

```bash
uv sync
uv tool install pre-commit
pre-commit install
```

## 実行

```bash
# カレントディレクトリを対象
uv run python src/main.py

# ディレクトリを指定
uv run python src/main.py /path/to/media
```

処理完了時に `Done: N renamed, M failed` が表示されます。失敗が 1 件以上ある場合、終了コードは `1` になります。

## 構成

- `src/main.py` — エントリポイント
- `src/rename.py` — 走査・リネーム処理
- `src/media_info.py` — 形式別メタデータ抽出
- `src/exif.py` — JPEG EXIF 読み取り
- `src/ffprobe.py` — ffprobe ラッパー
- `src/utils.py` — ファイル名ユーティリティ

配布パッケージではなく、`uv run python src/main.py` で直接実行する想定です（`[tool.uv] package = false`）。

## 開発

```bash
uv run pytest
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run pyright
```

- `ruff` — format / lint
- `pyright` — 型チェック（standard モード）
- `pytest` — テスト（`src/` を pythonpath に追加済み）
- `pre-commit` — コミット時に上記を自動実行
- GitHub Actions — `main` への push / PR で lint + test を実行
