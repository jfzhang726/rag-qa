# backend/storage/local_storage.py

# from backend.storage.base_storage import BaseStorage

import shutil
from typing import BinaryIO, List
import uuid
import os
import logging

from backend.storage.base_storage import BaseStorage

class LocalStorage(BaseStorage):
    def __init__(self, base_directory: str = "./data/raw_files"):
        self.base_directory = base_directory
        # Create base directory if it does not exist
        os.makedirs(self.base_directory, exist_ok=True)

    def upload_file(self, file_stream: BinaryIO, filename: str, file_uuid) -> str:
        file_extension = os.path.splitext(filename)[1]
        stored_filename = f"{file_uuid}{file_extension}"
        file_path = os.path.join(self.base_directory, stored_filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file_stream, f)
        return stored_filename

    def download_file(self, file_identifier: str) -> BinaryIO:
        file_path = os.path.join(self.base_directory, file_identifier)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_identifier} not found")
        return open(file_path, "rb")

    def list_files(self) -> List[str]:
        return os.listdir(self.storage_path)

    def delete_file(self, filename: str) -> str:
        file_path = os.path.join(self.storage_path, filename)
        os.remove(file_path)
        return file_path