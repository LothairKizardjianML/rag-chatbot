"""Entry point: wires up config, logging and the model, then sends a test prompt."""

from src.config import Config
from src.logger import Logger
from src.ollama_client import OllamaClient
from src.embeddings_db import EmbeddingsDB

if __name__ == "__main__":
    config = Config()
    logger = Logger("RAG-chatbot").get_logger()
    client = OllamaClient(logger)
    embeddings_db = EmbeddingsDB(logger)
    # # Send a test prompt to the model and print the response 
    # client.generate("llama3.1:8b", "Hello world!", stream=False)
    # # Send a test prompt to the model and embed it
    # client.embed("snowflake-arctic-embed:33m", "Hello world!")
    pdfs = embeddings_db.retrieve_pdfs()
    