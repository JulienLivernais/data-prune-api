from importers.csv_importer import CSVImporter
from importers.excel_importer import EXCELImporter
from importers.json_importer import JSONImporter


IMPORTERS = {
    "csv": CSVImporter,
    "excel": EXCELImporter,
    "json": JSONImporter,
}


def get_importer(source_type: str):
    importer_class = IMPORTERS[source_type]
    return importer_class()

