"""Entry point: wires up config, logging and the model, then sends a test prompt."""

from config import Config
from logger import Logger
from model import Model

if __name__ == "__main__":
    config = Config()
    logger = Logger("RAG-chatbot").get_logger()
    model = Model("llama3.1:8b", logger)
    model.post_prompt("Hello world!")
