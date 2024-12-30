# backend/file_processors/pdf_processor.py

import io
from backend.file_processors.base_processor import BaseFileProcessor
from typing import BinaryIO, List

from markitdown import MarkItDown

import logging

logger = logging.getLogger(__name__)

class PDFProcessor(BaseFileProcessor):
    def __init__(self):
        self.md = MarkItDown()
        self.file_extension = ".pdf"
    
    def can_process(self, file_extension: str) -> bool:
        return file_extension == ".pdf"

    def process(self, file_path: str) -> List[str]:
        logger.info(f"Processing PDF file by MarkItDown. {file_path} ")
        
        
        md_text = self.md.convert_local(file_path, file_extension=self.file_extension)
        text = md_text.text_content
        logger.info(f"PDF file processed by MarkItDown: {text[:100]}")
        return text