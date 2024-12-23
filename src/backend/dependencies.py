# backend/dependencies.py

from backend.interfaces import IVectorStore, ILLMService
from backend.dependency_factory import DependencyFactory

def get_vector_store() -> IVectorStore:
    return DependencyFactory.get_vector_store()

def get_llm_service() -> ILLMService:
    return DependencyFactory.get_llm_service()