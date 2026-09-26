"""
models.py
=========
SQLAlchemy ORM models — these define the tables inside data/app.db.

Three tables:
  1. PredictionRun  -> every time GET /api/predict is called, we log a row
  2. ScenarioRun     -> every time GET /api/scenario is called, we log a row
  3. UploadedDataset -> every time a CSV is uploaded via POST /api/upload

This lets the frontend "Reports / History" page show real history instead
of hardcoded numbers.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, Text

from app.database import Base


class PredictionRun(Base):
    __tablename__ = "prediction_runs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    forecast_accuracy = Column(Float)
    growth_rate = Column(Float)
    churn_rate = Column(Float)
    attrition_rate = Column(Float)
    risk_level = Column(String(20))


class ScenarioRun(Base):
    __tablename__ = "scenario_runs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    growth = Column(Float)
    elastic = Column(Float)
    cost = Column(Float)
    expected_revenue = Column(Float)
    var_95 = Column(Float)


class UploadedDataset(Base):
    __tablename__ = "uploaded_datasets"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    filename = Column(String(255))
    stored_path = Column(String(500))
    rows = Column(Integer)
    columns = Column(Integer)
    detected_type = Column(String(120))
    confidence = Column(Float)
    null_count = Column(Integer)
    headers = Column(Text)  # comma-separated column names
