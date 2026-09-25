"""
Forecasting Agent

Responsible for:
- Loading time series datasets
- Forecast generation
- Trend analysis
- Forecast evaluation

Project:
Predictive Intelligence Engine
"""

import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class ForecastingAgent:

    def __init__(self):

        self.results = {}

        self.project_root = Path(__file__).resolve().parent.parent
        self.data_directory = self.project_root / "data" / "cleaned"

    def load_dataset(self, filename: str) -> pd.DataFrame:
        """
        Load a dataset from any location (cleaned, uploaded, or real-time).
        
        Parameters
        ----------
        filename : str
            Full file path or just filename. If just filename, checks:
            1. data/uploaded/
            2. data/realtime/
            3. data/cleaned/
        
        Returns
        -------
        pd.DataFrame
            Loaded dataset.
        
        Raises
        ------
        FileNotFoundError
            If the dataset file does not exist.
        """
        # Check if it's a full file path
        if "/" in filename or "\\" in filename:
            file_path = Path(filename)
            if file_path.exists():
                df = pd.read_csv(file_path)
                print(f"\nLoaded dataset from: {file_path}")
                print("Loaded Columns:", df.columns.tolist())
                return df
            else:
                raise FileNotFoundError(f"Dataset not found: {file_path}")
        
        # Check multiple directories for the file
        search_dirs = [
            self.project_root / "data" / "uploaded",
            self.project_root / "data" / "realtime",
            self.project_root / "data" / "cleaned"
        ]
        
        for directory in search_dirs:
            file_path = directory / filename
            if file_path.exists():
                df = pd.read_csv(file_path)
                print(f"\nLoaded dataset from: {file_path}")
                print("Loaded Columns:", df.columns.tolist())
                return df
        
        raise FileNotFoundError(
            f"Dataset not found: {filename}. Searched in: {[str(d) for d in search_dirs]}"
        )

    def preprocess_time_series(
        self,
        df: pd.DataFrame,
        date_columns: list
    ) -> pd.DataFrame:

        processed_df = df.copy()

        # Convert all column names to lowercase
        processed_df.columns = processed_df.columns.str.lower()

        # Convert incoming names to lowercase too
        date_columns = [col.lower() for col in date_columns]

        print("\nUsing Date Columns:", date_columns)

        if len(date_columns) == 2:

            processed_df["date"] = pd.to_datetime(
                {
                    "year": processed_df[date_columns[0]],
                    "month": processed_df[date_columns[1]],
                    "day": 1
                }
            )

        elif len(date_columns) == 1:

            processed_df["date"] = pd.to_datetime(
                processed_df[date_columns[0]]
            )

        else:
            raise ValueError("Unsupported date configuration.")

        processed_df = processed_df.sort_values("date")
        processed_df.set_index("date", inplace=True)

        return processed_df

    def prepare_training_data(
        self,
        df: pd.DataFrame,
        target_column: str
    ) -> pd.Series:

        target_column = target_column.lower()

        if target_column not in df.columns:
            raise ValueError(
                f"{target_column} not found.\nAvailable columns:\n{df.columns.tolist()}"
            )

        return df[target_column]

    def train_holt_winters(
        self,
        training_series: pd.Series,
        seasonal_periods: int = 12
    ):

        model = ExponentialSmoothing(
            training_series,
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_periods
        )

        return model.fit()

    def generate_forecast(
        self,
        fitted_model,
        forecast_periods: int = 12
    ):

        return fitted_model.forecast(forecast_periods)

    def calculate_accuracy(self, actual, predicted):
        actual = np.array(actual, dtype=float)
        predicted = np.array(predicted, dtype=float)
        # align lengths
        min_len = min(len(actual), len(predicted))
        actual, predicted = actual[-min_len:], predicted[-min_len:]
        mask = actual != 0
        actual, predicted = actual[mask], predicted[mask]
        if len(actual) == 0:
            return 15.0
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return round(float(np.clip(mape, 0, 100)), 2)

    def save_results(
        self,
        dataset_name,
        forecast,
        mape
    ):

        accuracy = max(0, round(100 - mape, 2))

        result = {

            "dataset_name": dataset_name,
            "forecast": forecast.tolist(),
            "mape": mape,
            "forecast_accuracy": accuracy

        }

        self.results[dataset_name] = result

        return result

    def forecast_dataset(
        self,
        filename,
        date_columns,
        target_column,
        forecast_periods=12
    ):

        df = self.load_dataset(filename)
        df = self.preprocess_time_series(df, date_columns)
        target_column = target_column.lower()

        if target_column not in df.columns:
            raise ValueError(f"{target_column} not found. Available: {df.columns.tolist()}")

        # Aggregate to monthly totals so Holt-Winters gets a proper time series
        series = df[target_column].resample('MS').sum()
        series = series[series > 0]  # drop zero months

        use_hw = len(series) >= 24  # need 2 full seasonal cycles
        if use_hw:
            try:
                model = self.train_holt_winters(series)
                forecast = model.forecast(forecast_periods)
                fitted = model.fittedvalues
                mape = self.calculate_accuracy(series, fitted)
            except Exception:
                use_hw = False

        if not use_hw:
            # Weighted moving average fallback
            vals = series.values.astype(float)
            window = min(3, len(vals))
            weights = np.arange(1, window + 1)
            avg = float(np.average(vals[-window:], weights=weights))
            trend = float(np.mean(np.diff(vals[-window:]))) * 0.3 if window > 1 else 0
            forecast = np.array([max(avg + trend * (i + 1), avg * 0.5) for i in range(forecast_periods)])
            # For sparse data use leave-one-out style accuracy on available points
            if len(vals) >= 2:
                errors = [abs(vals[i] - np.mean(vals[:i])) / max(vals[i], 1) for i in range(1, len(vals))]
                mape = round(float(np.mean(errors)) * 100, 2)
            else:
                mape = 20.0  # safe default for single-point series

        return self.save_results(filename, forecast, mape)
    