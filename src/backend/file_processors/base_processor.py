# backend/file_processors/base_processor.py

from abc import ABC, abstractmethod
from typing import BinaryIO, List


class BaseFileProcessor(ABC):
    @abstractmethod
    def can_process(self, file_extension: str) -> bool:
        pass

    @abstractmethod
    def process(self, file_path: str) -> List[str]:
        pass