# backend/data_loader.py

from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

def process_documents(texts)-> List[Document]:
    logger.info(f"Received {len(texts)} texts...")
    try:
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        documents = text_splitter.create_documents(texts)
        logger.info(f"Processed {len(documents)} documents")
        return documents
    except Exception as e:
        logger.error(f"Error processing documents: {e}")
        return []