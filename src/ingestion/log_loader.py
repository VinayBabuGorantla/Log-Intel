import os
import zipfile
from typing import List
from src.utils.file_utils import is_supported_file
from src.exception.custom_exception import FileTypeNotSupported, LogProcessingError
from src.config.logger import setup_logger

logger = setup_logger(__name__)

def extract_text_from_file(file_path: str) -> str:
    """Reads and returns text from a single log file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        raise LogProcessingError(str(e))

def extract_from_zip(zip_path: str, temp_dir: str) -> List[str]:
    """Extracts valid files from ZIP and returns their paths."""
    try:
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for name in files:
                    file_path = os.path.join(root, name)
                    if is_supported_file(file_path):
                        extracted_files.append(file_path)
        return extracted_files
    except Exception as e:
        logger.error(f"Failed to extract ZIP: {e}")
        raise FileTypeNotSupported("Invalid ZIP archive")

def load_and_aggregate_text(file_paths: List[str]) -> str:
    """Reads and combines text from all valid files."""
    aggregated_text = ""
    for path in file_paths:
        logger.info(f"Loading: {path}")
        aggregated_text += extract_text_from_file(path) + "\n"
    return aggregated_text.strip()
