
# backend/vectorstores/chroma_vectorstore.py
from typing import Any, List
from uuid import uuid4
from backend.interfaces import IVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
# from langchain_chroma import Chroma
import chromadb
from chromadb.config import Settings, DEFAULT_DATABASE, DEFAULT_TENANT
import os 
import logging

logger = logging.getLogger(__name__)





class ChromaVectorStore(IVectorStore):
    def __init__(self, openai_api_key: str, vector_store_path: str):
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=self.openai_api_key)
        self.vector_store_path = vector_store_path
        self.collection = None
        self.load()



    def load(self):
        try:
            logger.info("Loading vector store...")
            if not os.path.exists(self.vector_store_path):
                logger.info("Vector store path not found. Creating directory...")
                os.makedirs(self.vector_store_path)
            # vector_store = Chroma(embedding_function=self.embeddings, persist_directory=self.vector_store_path)
            chroma_client = chromadb.PersistentClient(path=self.vector_store_path,
                                                      settings=Settings(),
                                                      tenant=DEFAULT_TENANT,
                                                      database=DEFAULT_DATABASE
                                                      )
            collection = chroma_client.get_or_create_collection("chroma_collection")
            
            self.collection = collection
            logger.info("Vector store loaded!")
            
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            

    def add_documents(self, documents: List[Document]):
        try:
            logger.info("Adding documents to vector store...")
            documents = [doc.page_content for doc in documents]
           
            ids = [str(uuid4()) for _ in range(len(documents))]
            self.collection.add(documents=documents, ids=ids)
            logger.info(f"ids of documents added: {len(ids)}")
            logger.info("Documents added to vector store!")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            
    
    def query(self, query_text: str, top_k: int = 5) -> List[Any]:
        try:
            logger.info(f"Querying chroma vector store with query text: '{query_text}' and top_k: {top_k}")
            results = self.collection.query(query_texts=query_text,
                                               n_results=top_k
                                               )
            """ 
            results = {'ids': [['id1', 'id2', 'id3']],
                       'embeddings': None,
                       'documents': [['document1', 'document2', 'document3']],
                       'uris': None,
                       'data': None,
                        'metadata': [[None, None, None]],
                        'distances': [[0.0, 0.0, 0.0]]
                       }
            """
            similar_texts = results['documents'][0]
            logger.info(f"Query successful! Found {len(similar_texts)} similar texts. Total length: {sum(len(t) for t in similar_texts)}")

            return similar_texts
            
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            return []