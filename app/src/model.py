import os
import numpy
import langchain.text_splitter as text_splitter

from src.logger import Logger

class Model:
    def __init__(self, model_name: str, logger: Logger):
        self.model_name = model_name
        self.logger = logger
        self.model = self.load_model()

    def load_model(self):
        self.logger.info(f"Loading model: {self.model_name}")
        return None  # Replace with actual model loading code

    def predict(self, input_data):
        self.logger.info(f"Making prediction with model: {self.model_name}")
        return None  # Replace with actual prediction code