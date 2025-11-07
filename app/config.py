import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH")
    TOKENIZER_PATH = os.getenv("TOKENIZER_PATH")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH")
    
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
    QDRANT_VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", 768))
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)