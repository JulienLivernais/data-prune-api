import math
import pandas as pd
from importers.base import DataImporter


class EXCELImporter(DataImporter):
    def extract(self, file_path: str) -> list[dict]:
        df = pd.read_excel(file_path, index_col=False)
        records = df.to_dict(orient="records")

        for record in records:
            for key, value in record.items():
                if isinstance(value, float) and math.isnan(value):
                    record[key] = None

        return records
