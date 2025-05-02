import logging
import os
import sys
from datetime import datetime

def setup_logger(name=__name__):
    """Configures and returns a logger with both stdout and file output."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Console output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File output
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        log_filename = datetime.now().strftime("loggenie_%Y%m%d.log")
        file_handler = logging.FileHandler(os.path.join(logs_dir, log_filename))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
