import pandas as pd
from importers.base import DataImporter


class CSVImporter(DataImporter):
    def extract(self, file_path: str) -> list[dict]:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")



