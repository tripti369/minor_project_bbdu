"""
/api/predict
============
The main dashboard endpoint. Runs the Analysis, Forecasting, RAG and
Decision agents together on the real CSV datasets and returns everything
the frontend dashboard needs in one call. Every call is also logged to
the database so the Reports/History page has real history to show.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd

from app.database import get_db
from app import models
from app.agents.analysis_agent import AnalysisAgent
from app.agents.forecasting_agent import ForecastingAgent
from app.agents.rag_agent import RAGAgent
from app.agents.decision_agent import DecisionAgent
from app.utils import DATA_DIR, load_csv

router = APIRouter()

analysis_agent = AnalysisAgent()
forecasting_agent = ForecastingAgent()
rag_agent = RAGAgent()
decision_agent = DecisionAgent()


def _detect_dataset_type(df: pd.DataFrame) -> str:
    cols = set(df.columns.str.lower())
    if "churn" in cols or "subscription_type" in cols:
        return "churn"
    if "leaveornot" in cols or "joiningyear" in cols:
        return "hr"
    if "retail_sales" in cols or "warehouse_sales" in cols:
        return "retail"
    if "year" in cols and "month" in cols:
        return "timeseries"
    return "generic"


def _build_timeseries(df: pd.DataFrame, filename: str):
    """Return (series, labels) for any dataset that has year+month or a date col."""
    cols = df.columns.str.lower()
    df.columns = cols
    if "year" in cols and "month" in cols:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        value_col = next(
            (c for c in numeric_cols if c not in ("year", "month")), numeric_cols[0] if numeric_cols else None
        )
        if value_col is None:
            raise ValueError("No numeric column found for time series")
        monthly = df.groupby(["year", "month"])[value_col].sum().reset_index().sort_values(["year", "month"])
        monthly["date"] = pd.to_datetime(
            monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
        )
        series = monthly.set_index("date")[value_col]
        labels = monthly["date"].dt.strftime("%Y-%m").tolist()
        return series, labels, value_col
    raise ValueError(f"Cannot build time series from {filename}")


@router.get("/predict")
def predict(
    dataset: str = Query(None, description="CSV filename to analyse (auto-detects type)"),
    db: Session = Depends(get_db),
):
    # ---- Determine which dataset to use ---------------------------------
    if dataset:
        df_main = load_csv(dataset)
        ds_type = _detect_dataset_type(df_main)
    else:
        dataset = None  # will fall through to defaults per type
        ds_type = "all"  # default: load all three

    # ---- Revenue / time-series ------------------------------------------
    if ds_type in ("retail", "timeseries", "generic") and dataset:
        try:
            series, labels, value_col = _build_timeseries(df_main, dataset)
        except Exception:
            # fallback: treat first numeric col as flat series
            num = df_main.select_dtypes(include=[np.number]).iloc[:, 0]
            series = num.reset_index(drop=True)
            series.index = pd.RangeIndex(len(series))
            labels = [str(i) for i in range(len(series))]
            value_col = num.name
    else:
        retail = load_csv("retail_warehouse_sales_cleaned.csv")
        retail.columns = retail.columns.str.lower()
        retail["total_sales"] = retail["retail_sales"].fillna(0) + retail["warehouse_sales"].fillna(0)
        monthly = (
            retail.groupby(["year", "month"])["total_sales"]
            .sum().reset_index().sort_values(["year", "month"])
        )
        monthly["date"] = pd.to_datetime(
            monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)
        )
        series = monthly.set_index("date")["total_sales"]
        labels = monthly["date"].dt.strftime("%Y-%m").tolist()

    forecast_result = forecasting_agent.forecast_series(series, forecast_periods=6, seasonal_periods=12)
    growth_rate = round(
        ((series.iloc[-1] - series.iloc[0]) / max(abs(float(series.iloc[0])), 1)) * 100, 1
    )

    # ---- Churn ----------------------------------------------------------
    if ds_type == "churn" and dataset:
        churn_df = df_main
    else:
        churn_df = load_csv("customer_churn_cleaned.csv")
    churn_df.columns = churn_df.columns.str.lower()

    if "churn" in churn_df.columns:
        churn_rate = round(float(churn_df["churn"].mean()) * 100, 1)
    else:
        churn_rate = 0.0

    avg_spend = round(float(churn_df["total_spend"].mean()), 1) if "total_spend" in churn_df.columns else 0.0
    avg_tenure = round(float(churn_df["tenure"].mean()), 1) if "tenure" in churn_df.columns else 0.0
    churn_by_sub = (
        churn_df.groupby("subscription_type")["churn"].mean().mul(100).round(1).to_dict()
        if "subscription_type" in churn_df.columns and "churn" in churn_df.columns
        else {}
    )

    # ---- Attrition ------------------------------------------------------
    if ds_type == "hr" and dataset:
        emp_df = df_main
    else:
        emp_df = load_csv("employee_hr_cleaned.csv")
    emp_df.columns = emp_df.columns.str.lower()

    attrition_rate = round(float(emp_df["leaveornot"].mean()) * 100, 1) if "leaveornot" in emp_df.columns else 0.0
    attrition_by_city = (
        emp_df.groupby("city")["leaveornot"].mean().mul(100).round(1).to_dict()
        if "city" in emp_df.columns and "leaveornot" in emp_df.columns
        else {}
    )

    # ---- Analysis + RAG + Decision --------------------------------------
    analysis_result = analysis_agent.analyze_dataset(dataset or "customer_churn_cleaned.csv")
    rag_agent.build_index(rebuild=False)
    rag_result = rag_agent.answer("business forecasting risk churn attrition")
    decision = decision_agent.generate_decision(
        forecast_accuracy=forecast_result["forecast_accuracy"],
        churn_rate=churn_rate,
        attrition_rate=attrition_rate,
        rag_result=rag_result,
    )

    # ---- Persist --------------------------------------------------------
    run = models.PredictionRun(
        forecast_accuracy=forecast_result["forecast_accuracy"],
        growth_rate=growth_rate,
        churn_rate=churn_rate,
        attrition_rate=attrition_rate,
        risk_level=decision["risk_level"],
    )
    db.add(run)
    db.commit()

    return {
        "dataset": dataset or "(all defaults)",
        "forecast_accuracy": forecast_result["forecast_accuracy"],
        "growth_rate": growth_rate,
        "churn_rate": churn_rate,
        "attrition_rate": attrition_rate,
        "avg_spend": avg_spend,
        "avg_tenure": avg_tenure,
        "revenue": {"labels": labels[-12:], "values": [round(float(v), 2) for v in series.tolist()[-12:]]},
        "forecast": {
            "labels": [f"M+{i+1}" for i in range(len(forecast_result["forecast"]))],
            "values": forecast_result["forecast"],
        },
        "churn_by_subscription": churn_by_sub,
        "attrition_by_city": attrition_by_city,
        "analysis": analysis_result,
        "rag": rag_result,
        "decision": decision,
    }
