"""
Main Entry Point

Predictive Intelligence Engine

This file is responsible for:
1. Creating the Analysis Agent
2. Running Dataset Analysis
3. Running Forecasting
4. Displaying Results
"""

from agents.analysis_agent import AnalysisAgent
from agents.forecasting_agent import ForecastingAgent
from agents.scenario_agent import ScenarioAgent
from agents.rag_agent import RAGAgent
from agents.decision_agent import DecisionAgent

def main():
    """Main execution function."""

    print("=" * 60)
    print("Predictive Intelligence Engine Started")
    print("=" * 60)

    # ==========================================================
    # ANALYSIS AGENT
    # ==========================================================

    print("\n[STEP 1] Creating Analysis Agent...")
    analysis_agent = AnalysisAgent()
    print("✓ Analysis Agent Created")

    print("\n[STEP 2] Starting Dataset Analysis...")
    analysis_result = analysis_agent.analyze_dataset(
        "customer_churn_cleaned.csv"
    )
    print("✓ Dataset Analysis Completed")

    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)

    print(f"\nDataset Name: {analysis_result['dataset_name']}")

    print("\nBasic Statistics:")
    print(analysis_result["basic_statistics"])

    print("\nDescriptive Statistics:")
    print(analysis_result["descriptive_statistics"])

    print("\nCorrelation Matrix:")
    print(analysis_result["correlation"])

    print("\nOutlier Report:")
    print(analysis_result["outlier_report"])

    # ==========================================================
    # FORECASTING AGENT
    # ==========================================================

    print("\n" + "=" * 60)
    print("FORECASTING RESULTS")
    print("=" * 60)

    forecast_agent = ForecastingAgent()

    forecast_result = forecast_agent.forecast_dataset(
        filename="retail_warehouse_sales_cleaned.csv",
        date_columns=["year", "month"],
        target_column="retail_sales",
        forecast_periods=12
    )

    print("\nDataset:")
    print(forecast_result["dataset_name"])

    print("\nMAPE:")
    print(forecast_result["mape"])

    print("\nForecast Accuracy:")
    print(f"{forecast_result['forecast_accuracy']}%")

    print("\nNext 12 Forecast Values:")
    print(forecast_result["forecast"])
    print("\n" + "=" * 60)
    print("SCENARIO ANALYSIS")
    print("=" * 60)

    scenario_agent = ScenarioAgent()

    scenario = scenario_agent.simulate(
    forecast_result["forecast"]
)

    print("\nBest Case")
    print(scenario["best_case"])

    print("\nBase Case")
    print(scenario["base_case"])

    print("\nWorst Case")
    print(scenario["worst_case"])    # ==========================================================
    # RAG AGENT
    # ==========================================================

    print("\n" + "=" * 60)
    print("KNOWLEDGE RETRIEVAL")
    print("=" * 60)

    rag_agent = RAGAgent()

    rag_agent.build_index()

    rag_result = rag_agent.answer(
        "business forecasting risk"
    )

    print("\nRetrieved Documents:")

    for doc in rag_result["results"]:

        print("-" * 40)
        print("Document :", doc["doc_id"])
        print("Score    :", round(doc["score"], 2))
        print("Excerpt  :", doc["excerpt"])


    # ==========================================================
    # DECISION AGENT
    # ==========================================================

    print("\n" + "=" * 60)
    print("EXECUTIVE DECISION")
    print("=" * 60)

    decision_agent = DecisionAgent()

    decision = decision_agent.generate_decision(
        analysis_result,
        forecast_result,
        rag_result
    )

    for key, value in decision.items():

        print(f"{key}: {value}")

    print("\n" + "=" * 60)
    print("Program Finished Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()