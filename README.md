# Python Template

`uv` ベースの Python アプリケーション/スクリプト雛形。

## 構成

- `src/main.py` — エントリポイント（必要に応じてスクリプトを追加）
- `ruff` — format / lint
- `pyright` — 型チェック（standard モード）
- `pytest` — テスト（`src/` を pythonpath に追加済み）
- `pre-commit` — コミット時に上記を自動実行
- GitHub Actions — `main` への push / PR で lint + test を実行
- `.vscode/` — ruff を保存時フォーマッタに設定

配布パッケージではなく、`uv run python src/main.py` で直接実行する想定です（`[tool.uv] package = false`）。

## セットアップ

```bash
uv sync
uv tool install pre-commit
pre-commit install
```

## 実行

```bash
uv run python src/main.py
```

## 開発

```bash
uv run pytest
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run pyright
```
