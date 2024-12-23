import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")
