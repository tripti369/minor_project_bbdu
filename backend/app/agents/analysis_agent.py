"""
Analysis Agent
==============
Responsible for:
- Loading cleaned datasets
- Basic + descriptive statistics
- Correlation matrix
- Outlier detection (IQR method)
"""

import numpy as np
import pandas as pd
from pathlib import Path


class AnalysisAgent:

    def __init__(self):
        self.results = {}
        self.project_root = Path(__file__).resolve().parent.parent.parent  # -> backend/
        self.data_directory = self.project_root / "data" / "cleaned"

    def load_dataset(self, filename: str) -> pd.DataFrame:
        """Load a dataset, checking uploaded/ then cleaned/."""
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

        raise FileNotFoundError(
            f"Dataset not found: {filename}. Searched: {[str(d) for d in search_dirs]}"
        )

    def calculate_basic_statistics(self, df: pd.DataFrame) -> dict:
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_values": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
            "duplicate_rows": int(df.duplicated().sum()),
            "data_types": df.dtypes.astype(str).to_dict(),
        }

    def calculate_descriptive_statistics(self, df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {}
        return numeric_df.describe().round(2).to_dict()

    def calculate_correlation(self, df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {}
        return numeric_df.corr().round(3).to_dict()

    def detect_outliers(self, df: pd.DataFrame) -> dict:
        outlier_report = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for column in numeric_columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            outlier_report[column] = {
                "outlier_count": int(len(outliers)),
                "outlier_percentage": round(
                    (len(outliers) / len(df)) * 100 if len(df) > 0 else 0.0, 2
                ),
            }
        return outlier_report

    def analyze_dataset(self, filename: str) -> dict:
        df = self.load_dataset(filename)
        outlier_report = self.detect_outliers(df)
        analysis = {
            "dataset_name": filename,
            "basic_statistics": self.calculate_basic_statistics(df),
            "descriptive_statistics": self.calculate_descriptive_statistics(df),
            "correlation": self.calculate_correlation(df),
            "outlier_report": outlier_report,
        }
        self.results[filename] = analysis
        return analysis
