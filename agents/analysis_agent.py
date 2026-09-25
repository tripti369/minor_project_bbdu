"""
Analysis Agent

Responsible for:
- Loading cleaned datasets
- Statistical analysis
- Trend detection
- Insight generation

Project:
Predictive Intelligence Engine
"""
import pandas as pd
import numpy as np
import json
from pathlib import Path

class AnalysisAgent:

    def __init__(self):
        """
        Initialize the Analysis Agent.
        """

        # Store analysis results
        self.results = {}

        # Project directories
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
                return df
        
        raise FileNotFoundError(
            f"Dataset not found: {filename}. Searched in: {[str(d) for d in search_dirs]}"
        )
    def calculate_basic_statistics(self, df: pd.DataFrame) -> dict:
        """
        Calculate basic statistics of a dataset.
        """

        statistics = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "data_types": df.dtypes.astype(str).to_dict(),
        }

        return statistics
    def calculate_descriptive_statistics(self, df: pd.DataFrame) -> dict:
        """
        Calculate descriptive statistics for all numerical columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        Returns
        -------
        dict
            Descriptive statistics as a dictionary.
        """

        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            return {}

        descriptive_stats = numeric_df.describe().to_dict()

        return descriptive_stats
    def calculate_correlation(self, df: pd.DataFrame) -> dict:
        """
        Calculate the correlation matrix for numerical columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        Returns
        -------
        dict
            Correlation matrix as a dictionary.
        """

        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            return {}

        correlation_matrix = numeric_df.corr()

        return correlation_matrix.to_dict()
    def detect_outliers(self, df: pd.DataFrame) -> dict:
        """
        Detect outliers in all numeric columns using the IQR method.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        Returns
        -------
        dict
            Outlier statistics for each numeric column.
        """

        outlier_report = {}

        # Select only numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:

            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = df[
                (df[column] < lower_bound) |
                (df[column] > upper_bound)
            ]

            outlier_report[column] = {
                "outlier_count": int(len(outliers)),
                "outlier_percentage": round(
                    (len(outliers) / len(df)) * 100 if len(df) > 0 else 0.0,
                    2
                )
            }

        return outlier_report
    def analyze_dataset(self, filename: str) -> dict:
        """
        Perform complete analysis of a dataset.

        Parameters
        ----------
        filename : str
            Name of the cleaned CSV file.

        Returns
        -------
        dict
            Complete analysis results.
        """

        # Load dataset
        df = self.load_dataset(filename)

        # Perform analysis
        outlier_report = self.detect_outliers(df)

        analysis = {
            "dataset_name": filename,
            "basic_statistics": self.calculate_basic_statistics(df),
            "descriptive_statistics": self.calculate_descriptive_statistics(df),
            "correlation": self.calculate_correlation(df),
            "outlier_report": outlier_report,
            "outliers": outlier_report,
        }

        # Store results
        self.results[filename] = analysis

        return analysis
