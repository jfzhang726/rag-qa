# backend/vectorstores/pinecone_vectorstore.py

from backend.interfaces import IVectorStore
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os
import logging
from typing import Any, List

from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)

# class PineconeVectorStore(IVectorStore):
#     def __init__(self, openai_api_key: str, pinecone_api_key: str, environment: str, index_name: str="pinecone-index"):
#         self.openai_api_key = openai_api_key
#         self.pinecone_api_key = pinecone_api_key
#         self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=self.pinecone_api_key)
#         self.environment = environment
#         self.index_name = index_name
#         self.vector_store = None
#         self.initilize_pinecone()

#     def initilize_pinecone(self):
#         try:
#             logger.info("Initializing Pinecone...")
#             pc = Pinecone(api_key=self.pinecone_api_key)
#             pc.
