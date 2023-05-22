import sys
import logging
import coloredlogs
from datetime import datetime
from tqdm import tqdm


def setup_logger(name):
    logger = logging.getLogger(name)
    
    # Configure the handlers only for the root logger.
    if name == "":
        coloredlogs.install(level="INFO", logger=logger)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_handler = logging.FileHandler(f"logs/logger_{timestamp}.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        logger.addHandler(file_handler)
    
    return logger


class TqdmToLogger(logging.StreamHandler):
    """Send log messages to tqdm.write to avoid progress bar interruption."""

    def emit(self, record):
        msg = self.format(record)
        tqdm.write(msg)


def setup_tqdm_logger(name):
    logger = logging.getLogger(name)

    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers = []

    logger.setLevel(logging.INFO)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_handler = logging.FileHandler(f"logs/logger_{timestamp}.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
    
    logger.addHandler(file_handler)

    return logger