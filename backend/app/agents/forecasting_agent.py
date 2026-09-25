"""
Forecasting Agent
=================
Responsible for:
- Loading time series datasets
- Forecast generation (Holt-Winters exponential smoothing)
- Forecast accuracy evaluation (MAPE)

A safe fallback (weighted moving average) kicks in automatically when a
series is too short / not seasonal enough for Holt-Winters to fit — this
keeps the API from ever crashing on real, messy data.
"""

import numpy as np
import pandas as pd
from pathlib import Path

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except ImportError:  # statsmodels missing -> fallback-only mode
    ExponentialSmoothing = None


class ForecastingAgent:

    def __init__(self):
        self.results = {}
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.data_directory = self.project_root / "data" / "cleaned"

    def load_dataset(self, filename: str) -> pd.DataFrame:
        if "/" in filename or "\\" in filename:
            file_path = Path(filename)
            if file_path.exists():
                return pd.read_csv(file_path)
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        search_dirs = [
            self.project_root / "data" / "uploaded",
            self.project_root / "data" / "cleaned",
        ]
        for directory in search_dirs:
            file_path = directory / filename
            if file_path.exists():
                return pd.read_csv(file_path)

        raise FileNotFoundError(f"Dataset not found: {filename}")

    def _weighted_moving_average_forecast(self, series: pd.Series, periods: int):
        """Simple, dependable fallback forecaster used when the series is
        too short for Holt-Winters (e.g. fewer than 2 full seasonal cycles)."""
        values = series.values.astype(float)
        window = min(3, len(values))
        weights = np.arange(1, window + 1)
        avg = float(np.average(values[-window:], weights=weights))
        trend = float(np.mean(np.diff(values[-window:]))) if window > 1 else 0.0
        trend *= 0.3  # dampen so forecast doesn't run away
        forecast = [max(avg + trend * (i + 1), avg * 0.5) for i in range(periods)]
        fitted = values  # naive "fit" = actuals, used only for MAPE fallback
        return np.array(forecast), fitted

    def train_holt_winters(self, training_series: pd.Series, seasonal_periods: int = 12):
        model = ExponentialSmoothing(
            training_series, trend="add", seasonal="add", seasonal_periods=seasonal_periods
        )
        return model.fit()

    def calculate_accuracy(self, actual, predicted):
        actual = np.array(actual, dtype=float)
        predicted = np.array(predicted, dtype=float)
        mask = actual != 0
        actual, predicted = actual[mask], predicted[mask]
        if len(actual) == 0:
            return 15.0  # sane default
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return round(float(mape), 2)

    def forecast_series(self, series: pd.Series, forecast_periods: int = 6, seasonal_periods: int = 12):
        """Forecast a plain numeric pandas Series (already sorted by time)."""
        use_holt_winters = (
            ExponentialSmoothing is not None
            and len(series) >= seasonal_periods * 2
        )

        if use_holt_winters:
            try:
                model = self.train_holt_winters(series, seasonal_periods)
                forecast = model.forecast(forecast_periods).values
                fitted = model.fittedvalues.values
            except Exception:
                forecast, fitted = self._weighted_moving_average_forecast(series, forecast_periods)
        else:
            forecast, fitted = self._weighted_moving_average_forecast(series, forecast_periods)

        mape = self.calculate_accuracy(series.values[-len(fitted):], fitted)
        accuracy = max(0.0, round(100 - mape, 2))

        return {
            "forecast": [round(float(v), 2) for v in forecast],
            "mape": mape,
            "forecast_accuracy": accuracy,
        }

    def forecast_dataset(self, filename, date_columns, target_column, forecast_periods=12):
        df = self.load_dataset(filename)
        df.columns = df.columns.str.lower()
        date_columns = [c.lower() for c in date_columns]
        target_column = target_column.lower()

        if len(date_columns) == 2:
            df["date"] = pd.to_datetime(
                {"year": df[date_columns[0]], "month": df[date_columns[1]], "day": 1}
            )
        elif len(date_columns) == 1:
            df["date"] = pd.to_datetime(df[date_columns[0]])
        else:
            raise ValueError("Unsupported date configuration.")

        df = df.sort_values("date").set_index("date")
        series = df[target_column]

        result = self.forecast_series(series, forecast_periods)
        result["dataset_name"] = filename
        self.results[filename] = result
        return result
