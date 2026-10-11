"""Measure delivered files, including SQLite, assets and verification evidence."""
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
excluded = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache'}
size = 0
for directory, children, files in os.walk(root):
    children[:] = [name for name in children if name not in excluded]
    size += sum((Path(directory) / name).stat().st_size for name in files)
print(f'{size} bytes; limit: 500000000 bytes; excluded: {sorted(excluded)}')
raise SystemExit(0 if size < 500_000_000 else 1)
