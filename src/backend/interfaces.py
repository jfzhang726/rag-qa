# backend/interfaces.py

from abc import ABC, abstractmethod
from typing import List, Any 

class IVectorStore(ABC):

    @abstractmethod
    def load(self) -> None:
        """ Load the vector store form persistent storage """
        pass

    @abstractmethod
    def add_documents(self, documents: List[str]) -> None:
        """ Add documents to the vector store """
        pass

    @abstractmethod
    def query(self, query_text: str, top_k: int = 5) -> List[Any]:
        """ Query the vector store """
        pass


class ILLMService(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """ Generate text using the language model """
        pass

