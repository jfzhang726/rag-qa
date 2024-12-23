# backend/vectorstores/faiss_vectorstore.py

from backend.interfaces import IVectorStore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import logging
from typing import Any, List


logger = logging.getLogger(__name__)

class FAISSVectorStore(IVectorStore):
    def __init__(self, openai_api_key: str, vector_store_path: str):
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=self.openai_api_key)
        self.vector_store_path = vector_store_path
        self.vector_store = None
        self.load()

    def load(self):
        try:
            logger.info("Loading vector store...")
            if not os.path.exists(self.vector_store_path):
                logger.info("Vector store path not found. Creating directory...")
                os.makedirs(self.vector_store_path)
            vector_store = FAISS(embedding_function=self.embeddings, persist_directory=self.vector_store_path)
            self.vector_store = vector_store
            logger.info("Vector store loaded!")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")

    def add_documents(self, documents: List[str]):
        try:
            logger.info("Adding documents to vector store...")
            self.vector_store.add_documents(documents=documents)
            logger.info("Documents added to vector store!")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")

    def query(self, query_text: str, top_k: int = 5) -> List[Any]:
        try:
            logger.info(f"Querying faiss vector store with query text: '{query_text}' and top_k: {top_k}")
            results = self.vector_store.similarity_search(query=query_text, k=top_k)
            logger.info("Query successful!")
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            return []
