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

        file_path = self.data_directory / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        print("\nLoaded Columns:")
        print(df.columns.tolist())

        return df

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

    def calculate_accuracy(
        self,
        actual,
        predicted
    ):

        actual = np.array(actual)
        predicted = np.array(predicted)

        mask = actual != 0

        actual = actual[mask]
        predicted = predicted[mask]

        mape = np.mean(
            np.abs((actual - predicted) / actual)
        ) * 100

        return round(mape, 2)

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

        print("\nForecast Parameters")
        print("Date Columns :", date_columns)
        print("Target Column:", target_column)

        df = self.load_dataset(filename)

        df = self.preprocess_time_series(
            df,
            date_columns
        )

        training_series = self.prepare_training_data(
            df,
            target_column
        )

        model = self.train_holt_winters(
            training_series
        )

        forecast = self.generate_forecast(
            model,
            forecast_periods
        )

        predictions = model.fittedvalues

        mape = self.calculate_accuracy(
            training_series,
            predictions
        )

        return self.save_results(
            filename,
            forecast,
            mape
        )