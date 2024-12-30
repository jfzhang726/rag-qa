# backend/file_processors/processor_factory.py

from typing import List

from .base_processor import BaseFileProcessor
from .text_processor import TextProcessor
from .pdf_processor import PDFProcessor

# Factory registry for file processors
class FileProcessorFactory:
    def __init__(self):
        self.processors: List[BaseFileProcessor] = [
            PDFProcessor(),
            TextProcessor()
            ]
    def get_processor(self, file_extension: str) -> BaseFileProcessor:
        for processor in self.processors:
            if processor.can_process(file_extension):
                return processor
        raise ValueError("Unsupported file type")
    