"""
Scenario Agent

Responsible for:
- Scenario simulation
- Business risk estimation
- Best / Base / Worst case prediction
"""

import numpy as np


class ScenarioAgent:

    def __init__(self):

        self.results = {}

    def simulate(
        self,
        forecast_values,
        variation=0.10
    ):
        """
        Create Best, Base and Worst scenarios.
        """

        forecast = np.array(forecast_values)

        best_case = forecast * (1 + variation)
        base_case = forecast
        worst_case = forecast * (1 - variation)

        result = {

            "best_case": best_case.round(2).tolist(),
            "base_case": base_case.round(2).tolist(),
            "worst_case": worst_case.round(2).tolist()

        }

        self.results["scenario"] = result

        return result