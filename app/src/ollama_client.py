"""Client for talking to a locally-hosted Ollama model over its HTTP API."""

import requests

from .logger import Logger


class OllamaClient:
    """Thin wrapper around Ollama's ``/api/chat`` endpoint for one model."""

    def __init__(self, logger: Logger):
        self.logger = logger

    def embed(self, model_name: str, text: str) -> str:
        """Send a single text string to the model via Ollama's embedding API.

        Args:
            model_name: The Ollama model tag to query (e.g. "llama3.1:8b"),
                must already be pulled locally (``ollama pull <model_name>``).
            text: The text string to embed.

        Returns:
            The raw, unparsed response body text from Ollama, or ``None``
            if the request failed (e.g. Ollama isn't running, or the model
            isn't loaded).
        """
        self.logger.info(f"Posting text to embedding model {model_name}: {text}")
        url = "http://localhost:11434/api/embed"
        try:
            response = requests.post(url, json={"model": model_name, "input": text})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request to Ollama failed: {e}")
            return None
        self.logger.info(f"Received embedding response: {response.text}")
        return response.text

    def generate(self, model_name: str, prompt: str, stream: bool = True) -> str:
        """Send a single user prompt to the model via Ollama's chat API.

        Uses Ollama's default (streaming) behavior, so the returned text
        will contain multiple newline-delimited JSON chunks rather than a
        single JSON object — pass ``"stream": false`` in the request body
        to get one consolidated response instead.

        Args:
            model_name: The Ollama model tag to query (e.g. "llama3.1:8b"),
                must already be pulled locally (``ollama pull <model_name>``).
            prompt: The user's message to send to the model.

        Returns:
            The raw, unparsed response body text from Ollama, or ``None``
            if the request failed (e.g. Ollama isn't running, or the model
            isn't loaded).
        """
        self.logger.info(f"Posting prompt to model {model_name}: {prompt}")
        url = "http://localhost:11434/api/chat"
        try:
            response = requests.post(url, json={"model": model_name, "stream": stream, "messages": [{"role": "user", "content": prompt}]})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request to Ollama failed: {e}")
            return None
        self.logger.info(f"Received response: {response.text}")
        return response.text
