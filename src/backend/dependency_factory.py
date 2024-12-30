# backend/dependency_factory.py

import dotenv
from backend.file_processors.processor_factory import FileProcessorFactory
from backend.interfaces import IVectorStore, ILLMService
from backend.storage import local_storage
from backend.storage.base_storage import BaseStorage
from backend.vectorstores.chroma_vectorstore import ChromaVectorStore
from backend.vectorstores.faiss_vectorstore import FAISSVectorStore
from backend.llms.openai_llm import OpenAILLMService
from backend.llms.huggingface_llm import HuggingFaceLLMService
import os
import logging

logger = logging.getLogger(__name__)
dotenv.load_dotenv()
class DependencyFactory:
    def __init__(self):
        self.raw_file_storage = self.create_raw_file_storage()
        self.vector_store = self.create_vector_store()
        self.llm_service = self.create_llm_service()
        self.file_processor_factory = self.create_file_processor_factory()


    def create_vector_store(self) -> IVectorStore:
        
        vector_store_type = os.getenv("VECTOR_STORE_TYPE")
        logger.info(f"Vector store type: {vector_store_type}")
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        vector_store_path = os.getenv("VECTOR_STORE_PATH")
        logger.info(f"Vector store path: {vector_store_path}")
        vector_store = None
          
        if vector_store_type == "CHROMA":
            vector_store = ChromaVectorStore(openai_api_key=openai_api_key, vector_store_path=vector_store_path)
        elif vector_store_type == "FAISS":
            vector_store = FAISSVectorStore(openai_api_key=openai_api_key, vector_store_path=vector_store_path)
        # elif os.getenv("VECTOR_STORE") == "PINECONE":
        #     vector_store = PineconeVectorStore()
        else:
            logger.error("Invalid vector store type!")
        return vector_store


    def create_llm_service(self) -> ILLMService:
        llm_service_type = os.getenv("LLM_SERVICE_TYPE")
        
        llm_service = None

        if llm_service_type == "OPENAI":
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_LLM_MODEL")
            llm_service = OpenAILLMService(openai_api_key=openai_api_key, model=model)
        elif llm_service_type == "HUGGINGFACE":
            model = os.getenv("HUGGINGFACE_LLM_MODEL")
            llm_service = HuggingFaceLLMService(model=model)

        else:
            logger.error("Invalid LLM service type!")
        return llm_service

    
    def create_raw_file_storage(self) -> BaseStorage:
        storage_type = os.getenv("RAW_FILE_STORAGE_TYPE")
        logger.info(f"Storage type: {storage_type}")
        if storage_type == "local":
            base_directory = os.getenv("LOCAL_STORAGE_DIRECTORY")
            storage = local_storage.LocalStorage(base_directory=base_directory)
        # elif self.storage_type == "s3":
        #     self.storage = s3_storage.S3Storage(bucket_name=os.getenv("S3_BUCKET_NAME"))
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
        return storage

  
    def create_file_processor_factory(self) -> FileProcessorFactory:
        file_processor_factory = FileProcessorFactory()
        return file_processor_factory
    
    