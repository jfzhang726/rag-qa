# backend/dependency_factory.py

import dotenv
from backend.interfaces import IVectorStore, ILLMService
from backend.vectorstores.chroma_vectorstore import ChromaVectorStore
from backend.vectorstores.faiss_vectorstore import FAISSVectorStore
# from backend.vectorstores.pinecone_vectorstore import PineconeVectorStore
from backend.llms.openai_llm import OpenAILLMService
from backend.llms.huggingface_llm import HuggingFaceLLMService
import os
import logging

logger = logging.getLogger(__name__)
dotenv.load_dotenv()
class DependencyFactory:
    @staticmethod
    def get_vector_store() -> IVectorStore:
        
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

    @staticmethod
    def get_llm_service() -> ILLMService:
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
