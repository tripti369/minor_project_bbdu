"""
schemas.py
==========
Pydantic models describing the shape of API responses. FastAPI uses these
to validate/serialize data and to auto-generate the /docs page.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PredictionRunOut(BaseModel):
    id: int
    created_at: datetime
    forecast_accuracy: float
    growth_rate: float
    churn_rate: float
    attrition_rate: float
    risk_level: str

    class Config:
        from_attributes = True


class ScenarioRunOut(BaseModel):
    id: int
    created_at: datetime
    growth: float
    elastic: float
    cost: float
    expected_revenue: float
    var_95: float

    class Config:
        from_attributes = True


class UploadedDatasetOut(BaseModel):
    id: int
    created_at: datetime
    filename: str
    rows: int
    columns: int
    detected_type: str
    confidence: float
    null_count: int

    class Config:
        from_attributes = True


class HistoryOut(BaseModel):
    predictions: List[PredictionRunOut]
    scenarios: List[ScenarioRunOut]
    uploads: List[UploadedDatasetOut]
