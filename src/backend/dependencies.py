# backend/dependencies.py

from backend.file_processors.processor_factory import FileProcessorFactory
from backend.interfaces import IVectorStore, ILLMService
from backend.dependency_factory import DependencyFactory
from backend.storage.base_storage import BaseStorage

factory = DependencyFactory()

def get_vector_store() -> IVectorStore:
    return factory.vector_store

def get_llm_service() -> ILLMService:
    return factory.llm_service

def get_raw_file_storage() -> BaseStorage:
    return factory.raw_file_storage

def get_file_processor_factory() -> FileProcessorFactory:
    return factory.file_processor_factory

