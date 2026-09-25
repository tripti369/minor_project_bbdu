"""
/api/analysis
=============
Returns descriptive statistics, correlation matrix and outlier report for
a chosen dataset (defaults to the customer churn dataset).
"""

from fastapi import APIRouter, Query

from app.agents.analysis_agent import AnalysisAgent

router = APIRouter()
analysis_agent = AnalysisAgent()


@router.get("/analysis")
def analysis(dataset: str = Query("customer_churn_cleaned.csv", description="CSV filename to analyze")):
    result = analysis_agent.analyze_dataset(dataset)
    return result
