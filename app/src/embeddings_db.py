import os
import numpy as np

from .config import Config
from .logger import Logger

from glob import glob

class EmbeddingsDB:
    """A simple in-memory database for storing embeddings and their associated metadata."""

    def __init__(self, logger: Logger):
        self.config = Config()
        self.logger = logger

    def retrieve_pdfs(self):
        """Retrieve all PDFs from the ingestion folder."""
        pdfs = []
        for file in glob(os.path.join(self.config.ingestion_folder, "*.pdf")):
            self.logger.info(f"Retrieving {file}.")
            pdfs.append(file)
        self.logger.info(f"Retrieved {len(pdfs)} PDFs from the ingestion folder.")
        return pdfs