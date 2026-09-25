    def load_dataset(self, filename: str) -> pd.DataFrame:
        """
        Load a cleaned dataset from the data directory.

        Parameters
        ----------
        filename : str
            Name of the cleaned CSV file.

        Returns
        -------
        pd.DataFrame
            Loaded dataset.

        Raises
        ------
        FileNotFoundError
            If the dataset file does not exist.
        """

        file_path = self.data_directory / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        return df