# backend/storage/base_storage.py

from abc import ABC, abstractmethod
from typing import BinaryIO, List
import os 
import logging

class BaseStorage(ABC):
    @abstractmethod
    def upload_file(self, file_stream: BinaryIO, filename: str, file_uuid:str) -> str:
        pass

    @abstractmethod
    def download_file(self, filename: str) -> BinaryIO:
        pass

    @abstractmethod
    def list_files(self) -> List[str]:
        pass
    @abstractmethod
    def delete_file(self, filename: str) -> str:
        pass

    