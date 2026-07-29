from abc import ABC, abstractmethod


class DataImporter(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> list[dict]:
        pass

