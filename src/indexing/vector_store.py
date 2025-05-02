from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from src.config.logger import setup_logger
from src.config.settings import VECTOR_DB_DIR
import os

logger = setup_logger(__name__)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def create_vector_store(text: str):
    try:
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        os.makedirs(VECTOR_DB_DIR, exist_ok=True)
        vector_store = Chroma.from_texts(
            texts=chunks, embedding=embeddings, persist_directory=VECTOR_DB_DIR
        )
        vector_store.persist()
        logger.info("Vector store created successfully.")
        return vector_store
    except Exception as e:
        logger.error(f"Vector store creation failed: {e}")
        raise

def load_vector_store():
    try:
        if not os.path.exists(VECTOR_DB_DIR):
            logger.warning("Vector DB not found.")
            return None
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    except Exception as e:
        logger.error(f"Vector store loading failed: {e}")
        return None
