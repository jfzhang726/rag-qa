# backend/llms/huggingface_llm.py

from backend.interfaces import ILLMService
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class HuggingFaceLLMService(ILLMService):
    def __init__(self, model: str="gpt2"):
        self.model = model
        self.llm = None
        self.initialize_llm()

    def initialize_llm(self):
        try:
            logger.info(f"Initializing LLM {self.model}...")
            llm = pipeline('text-generation', model=self.model)
            logger.info("LLM initialized!")
            self.llm = llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")

    def generate_response(self, prompt: str) -> str:
        try:
            logger.info(f"Generating response for prompt: '{prompt[:50]}...'")
            response = self.llm(prompt=prompt)[0]['generated_text']
            logger.info("Response generated!")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""