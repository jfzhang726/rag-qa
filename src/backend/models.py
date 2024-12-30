#backend/models.py

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from backend.database import Base
import enum
from datetime import datetime


class FileStatus(enum.Enum):
    pending = "Pending"
    indexed = "Indexed"
    failed = "Failed"



class Files(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    uuid = Column(String, unique=True, nullable=False)
    s3_key = Column(String, nullable=True)        # Applicable if using S3
    local_path = Column(String, nullable=True)    # Applicable if using local storage
    uploader_id = Column(String, nullable=True)   # Replace with actual type (e.g., Integer) based on your user model
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(FileStatus), default=FileStatus.pending)
    file_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)