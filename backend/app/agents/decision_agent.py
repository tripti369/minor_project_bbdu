"""
Decision Agent
==============
Combines outputs from the Analysis, Forecasting and RAG agents into a
single executive recommendation with a risk level and action items.
"""

from typing import Dict


class DecisionAgent:

    def __init__(self):
        self.results = {}

    def generate_decision(self, forecast_accuracy: float, churn_rate: float,
                           attrition_rate: float, rag_result: Dict) -> Dict:

        if forecast_accuracy >= 90:
            risk = "Low"
        elif forecast_accuracy >= 70:
            risk = "Medium"
        else:
            risk = "High"

        # Escalate risk if churn/attrition signals are also unhealthy
        if churn_rate > 30 or attrition_rate > 25:
            risk = "High" if risk != "Low" else "Medium"

        recommendation = []
        if risk == "Low":
            recommendation.append("Current business trend is stable — proceed with planned investments.")
            recommendation.append("Continue monitoring churn and attrition monthly.")
        elif risk == "Medium":
            recommendation.append("Monitor business KPIs closely and review financial planning monthly.")
            recommendation.append("Investigate the subscription tiers / cities with the highest churn or attrition.")
        else:
            recommendation.append("Forecast confidence is low — perform a manual business review.")
            recommendation.append("Gather more historical data before committing new capital.")
            recommendation.append("Prioritise a retention initiative given elevated churn/attrition.")

        decision = {
            "forecast_accuracy": forecast_accuracy,
            "churn_rate": churn_rate,
            "attrition_rate": attrition_rate,
            "risk_level": risk,
            "knowledge_documents": len(rag_result.get("results", [])),
            "recommendation": recommendation,
        }
        self.results["latest"] = decision
        return decision
