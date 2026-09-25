"""
utils.py
========
Small shared helpers used across route modules.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent  # -> backend/
DATA_DIR = BASE_DIR / "data" / "cleaned"
UPLOAD_DIR = BASE_DIR / "data" / "uploaded"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV by filename, checking uploaded/ first then cleaned/."""
    for directory in (UPLOAD_DIR, DATA_DIR):
        path = directory / filename
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError(f"Dataset not found: {filename}")
