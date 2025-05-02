import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Directory to persist vector DB
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "vector_db")

# HuggingFace API token (optional for private models)
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)

# Allowed log file extensions
ALLOWED_EXTENSIONS = {".log", ".txt", ".json", ".xml"}
