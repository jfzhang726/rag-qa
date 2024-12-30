# backend/file_processors/text_processor.py

from typing import BinaryIO, List
from .base_processor import BaseFileProcessor

class TextProcessor(BaseFileProcessor):
    def __init__(self):
        self.file_extension = ".txt"
    def can_process(self, file_extension: str) -> bool:
        return file_extension == ".txt"

    def process(self, file_path: str) -> List[str]:
        with open(file_path, "r") as file:
            text = file.read()
        return text