import math
import pandas as pd
from importers.base import DataImporter


def find_header_row(file_path: str) -> int:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if "cmdCode" in line or ("COMMODITY" in line and "COUNTRY" in line):
                return i
    return 0


class CSVImporter(DataImporter):
    def extract(self, file_path: str) -> list[dict]:
        header_row = find_header_row(file_path)
        df = pd.read_csv(file_path, skiprows=header_row, index_col=False)
        records = df.to_dict(orient="records")

        for record in records:
            for key, value in record.items():
                if isinstance(value, float) and math.isnan(value):
                    record[key] = None

        return records

