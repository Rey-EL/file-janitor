# file-janitor

I wrote this to clean out folders full of duplicate files without hunting them down by hand.

![CI](https://github.com/Rey-EL/file-janitor/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- Finds duplicates by SHA-256 content hash, not by filename
- Finds folders that are completely empty, including nested ones
- Keeps the newest copy of each duplicate set (by modification time); only older copies are proposed for deletion
- Never touches files in a path containing "backup"
- Asks for one confirmation before deleting duplicates, and another before deleting empty folders
- Writes a timestamped log of everything it did

## Install

```bash
git clone https://github.com/Rey-EL/file-janitor.git
cd file-janitor
pip install -r requirements.txt
```

## Usage

```bash
python3 file_janitor.py
```

Pick a folder in the dialog, review the findings, answer `y`/`n` for each cleanup step. A `FileJanitor_log_*.txt` report is written next to the script when it finishes.

## How it works

The tool walks the folder, hashes every non-empty file with SHA-256, and groups identical hashes. The most recently modified file in each group is the keeper. Empty folders are found with a bottom-up walk so nested empties are caught. Tests live in `tests/` and run on Python 3.10–3.12 in CI.

## Project structure

```
file-janitor/
├── file_janitor.py            # the tool
├── requirements.txt
├── tests/                     # pytest suite (pure functions only)
└── .github/workflows/ci.yml  # CI workflow
```

## License

MIT — see [LICENSE.md](LICENSE.md).
