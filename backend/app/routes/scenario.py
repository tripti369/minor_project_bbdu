"""
/api/scenario
=============
Monte Carlo revenue scenario simulator. Base revenue is computed from the
real retail sales dataset; growth/elasticity/cost are user-supplied
assumptions from the frontend sliders.
"""

import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.agents.scenario_agent import ScenarioAgent
from app.utils import load_csv

router = APIRouter()
scenario_agent = ScenarioAgent()


@router.get("/scenario")
def scenario(
    growth: float = Query(6.0, description="Market growth rate, percent"),
    elastic: float = Query(1.2, description="Pricing elasticity multiplier"),
    cost: float = Query(3.5, description="Operating cost inflation, percent"),
    runs: int = Query(3000, ge=200, le=20000, description="Number of Monte Carlo samples"),
    db: Session = Depends(get_db),
):
    if math.isnan(growth) or math.isnan(elastic) or math.isnan(cost):
        growth, elastic, cost = 6.0, 1.2, 3.5

    retail = load_csv("retail_warehouse_sales_cleaned.csv")
    retail.columns = retail.columns.str.lower()
    base_revenue = round(float(retail["retail_sales"].sum()) / 1000, 2)  # in $K -> scaled to "$M" for display

    result = scenario_agent.monte_carlo(base_revenue, growth, elastic, cost, runs=runs)

    db.add(models.ScenarioRun(
        growth=growth, elastic=elastic, cost=cost,
        expected_revenue=result["expected_revenue"], var_95=result["var_95"],
    ))
    db.commit()

    return result
