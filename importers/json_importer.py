from importers.base import DataImporter
import json


class JSONImporter(DataImporter):
    def extract(self, file_path: str) -> list[dict]:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data



