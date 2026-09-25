"""
Decision Agent

Combines outputs from:
- Analysis Agent
- Forecasting Agent
- RAG Agent

Produces an executive business recommendation.
"""

from typing import Dict


class DecisionAgent:
    """
    Decision Agent for Predictive Intelligence Engine.
    """

    def __init__(self):

        self.results = {}

    def generate_decision(
        self,
        analysis_result: Dict,
        forecast_result: Dict,
        rag_result: Dict
    ) -> Dict:

        accuracy = forecast_result.get(
            "forecast_accuracy",
            0
        )

        if accuracy >= 90:
            risk = "Low"

        elif accuracy >= 70:
            risk = "Medium"

        else:
            risk = "High"

        recommendation = []

        if risk == "Low":

            recommendation.append(
                "Current business trend is stable."
            )

            recommendation.append(
                "Proceed with planned investments."
            )

        elif risk == "Medium":

            recommendation.append(
                "Monitor business KPIs closely."
            )

            recommendation.append(
                "Review financial planning monthly."
            )

        else:

            recommendation.append(
                "Forecast confidence is low."
            )

            recommendation.append(
                "Perform manual business review."
            )

            recommendation.append(
                "Use additional historical data."
            )

        executive_summary = {

            "dataset": analysis_result["dataset_name"],

            "forecast_accuracy": accuracy,

            "risk_level": risk,

            "knowledge_documents": len(
                rag_result.get("results", [])
            ),

            "recommendation": recommendation

        }

        self.results[
            analysis_result["dataset_name"]
        ] = executive_summary

        return executive_summary
