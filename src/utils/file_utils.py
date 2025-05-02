import os
from src.config.settings import ALLOWED_EXTENSIONS

def is_supported_file(file_path: str) -> bool:
    """Check if file has supported extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in ALLOWED_EXTENSIONS
