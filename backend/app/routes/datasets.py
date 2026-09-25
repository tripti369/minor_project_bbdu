"""
/api/datasets
=============
Lists every dataset currently available to the engine — the ones shipped
under data/cleaned/ plus anything a user has uploaded via /api/upload.
"""

from fastapi import APIRouter

from app.utils import DATA_DIR, UPLOAD_DIR

router = APIRouter()


def _describe(directory, source: str):
    items = []
    if not directory.exists():
        return items
    for path in sorted(directory.glob("*.csv")):
        try:
            size_kb = round(path.stat().st_size / 1024, 1)
        except OSError:
            size_kb = None
        items.append({"filename": path.name, "source": source, "size_kb": size_kb})
    return items


@router.get("/datasets")
def datasets():
    return {
        "datasets": _describe(DATA_DIR, "built-in") + _describe(UPLOAD_DIR, "uploaded"),
    }
