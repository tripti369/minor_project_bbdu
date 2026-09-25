"""
Scenario Agent
==============
Responsible for:
- Best / Base / Worst case projection off a forecast
- Monte Carlo simulation of revenue outcomes under different
  growth / pricing-elasticity / cost-inflation assumptions
"""

import numpy as np


class ScenarioAgent:

    def __init__(self):
        self.results = {}

    def simulate(self, forecast_values, variation: float = 0.10) -> dict:
        """Create Best, Base and Worst scenarios off a forecast series."""
        forecast = np.array(forecast_values, dtype=float)
        result = {
            "best_case": (forecast * (1 + variation)).round(2).tolist(),
            "base_case": forecast.round(2).tolist(),
            "worst_case": (forecast * (1 - variation)).round(2).tolist(),
        }
        self.results["scenario"] = result
        return result

    def monte_carlo(self, base_revenue: float, growth: float, elastic: float, cost: float,
                     runs: int = 3000, bins: int = 20) -> dict:
        """Monte-Carlo simulate a revenue distribution given business
        assumptions, computed on top of a real base revenue figure pulled
        from the dataset (not a hardcoded number)."""
        mean = base_revenue * (1 + growth / 100) * (1 + elastic * 0.02) * (1 - cost / 200)
        std = 0.9 + abs(growth) * 0.03 + elastic * 0.15
        samples = np.random.normal(mean, max(std, 0.01), runs)

        counts, edges = np.histogram(samples, bins=bins)
        sorted_samples = np.sort(samples)
        var_95 = float(mean - sorted_samples[int(len(sorted_samples) * 0.05)])

        return {
            "expected_revenue": round(float(mean), 2),
            "var_95": round(max(var_95, 0.1), 2),
            "sensitivity": round(1 + elastic * 0.4 - growth * 0.01, 2),
            "histogram": {
                "labels": [round(float(e), 2) for e in edges[:-1]],
                "counts": counts.tolist(),
            },
        }
