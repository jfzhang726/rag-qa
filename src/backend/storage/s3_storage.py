# backend/storage/s3_storage.py

from typing import BinaryIO, List
from backend.storage.base_storage import BaseStorage

class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        # Create bucket if it does not exist
        self._create_bucket()
        
    def _create_bucket(self):
        # Create bucket if it does not exist
        pass

    def upload_file(self, file_stream: BinaryIO, filename: str, file_uuid:str) -> str:
        # Upload file to S3
        pass

    def download_file(self, file_identifier: str) -> BinaryIO:
        # Download file from S3
        pass

    def list_files(self) -> List[str]:
        # List files in S3 bucket
        pass

    def delete_file(self, filename: str) -> str:
        # Delete file from S3
        pass