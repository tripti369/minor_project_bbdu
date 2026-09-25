"""
/api/history
============
Reads real run history back out of the SQLite database. Powers the
frontend "Reports" page so numbers shown there are genuine past runs,
not hardcoded placeholders.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter()


@router.get("/history")
def history(db: Session = Depends(get_db), limit: int = 20):
    predictions = (
        db.query(models.PredictionRun)
        .order_by(models.PredictionRun.created_at.desc())
        .limit(limit)
        .all()
    )
    scenarios = (
        db.query(models.ScenarioRun)
        .order_by(models.ScenarioRun.created_at.desc())
        .limit(limit)
        .all()
    )
    uploads = (
        db.query(models.UploadedDataset)
        .order_by(models.UploadedDataset.created_at.desc())
        .limit(limit)
        .all()
    )

    def serialize(rows):
        return [
            {c.name: getattr(row, c.name) for c in row.__table__.columns}
            for row in rows
        ]

    return {
        "predictions": serialize(predictions),
        "scenarios": serialize(scenarios),
        "uploads": serialize(uploads),
    }
