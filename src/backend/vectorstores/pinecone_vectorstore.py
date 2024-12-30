# backend/vectorstores/pinecone_vectorstore.py

from backend.interfaces import IVectorStore
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os
import logging
from typing import Any, List

from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)

