# backend/llms/openai_llm.py

from backend.interfaces import ILLMService
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAILLMService(ILLMService):
    def __init__(self, openai_api_key: str, model: str="gpt-4o-mini"):
        self.openai_api_key = openai_api_key
        self.model = model
        self.llm = None
        self.initialize_llm()

    def initialize_llm(self):
        try:
            logger.info(f"Initializing LLM {self.model}...")
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=self.openai_api_key)
            logger.info("LLM initialized!")
            self.llm = llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")

    def generate_response(self, prompt: str) -> str:
        try:
            logger.info(f"Generating response for prompt: '{prompt[:50]}...'")
            response = self.llm.invoke(input=prompt)
            logger.info("Response generated!")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""