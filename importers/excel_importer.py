import pandas as pd
from importers.base import DataImporter


class EXCELImporter(DataImporter):
    def extract(self, file_path: str) -> list[dict]:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")

