"""
/api/upload
===========
Accepts a CSV upload from the frontend Data Ingestion page, classifies
its likely dataset type from its column names, stores the file under
data/uploaded/ (so the other agents can immediately use it), and logs the
upload in the database.
"""

import io

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.utils import UPLOAD_DIR

router = APIRouter()


def classify(columns) -> tuple[str, int]:
    cols = [c.lower() for c in columns]
    joined = ",".join(cols)
    if any(k in joined for k in ["churn", "subscription", "tenure"]):
        return "CRM / Churn Dataset", 97
    if any(k in joined for k in ["leaveornot", "joiningyear", "education"]):
        return "HR / Employee Dataset", 96
    if any(k in joined for k in ["retail_sales", "warehouse", "supplier"]):
        return "Retail & Warehouse Sales", 98
    if any(k in joined for k in ["revenue", "profit", "margin", "ebitda", "balance sheet"]):
        return "Financial Ledger", 95
    return "General Dataset", 85


@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        return {"error": f"Could not parse CSV: {e}"}

    dtype, confidence = classify(df.columns)
    null_count = int(df.isnull().sum().sum())
    preview = df.head(5).fillna("").astype(str).to_dict(orient="records")

    # Persist the raw file so other endpoints (analysis/forecast) can use it
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    stored_path = UPLOAD_DIR / safe_name
    stored_path.write_bytes(content)

    record = models.UploadedDataset(
        filename=file.filename,
        stored_path=str(stored_path),
        rows=len(df),
        columns=len(df.columns),
        detected_type=dtype,
        confidence=confidence,
        null_count=null_count,
        headers=",".join(df.columns),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "headers": list(df.columns),
        "detected_type": dtype,
        "confidence": confidence,
        "null_count": null_count,
        "preview": preview,
    }
