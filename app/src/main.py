import os

from src.config import Config
from src.logger import Logger
from src.model import Model

if __name__ == "__main__":
    config = Config()
    logger = Logger("RAG-chatbot").get_logger()
    model = Model("example_model", logger)
    model.predict("Hello world!")