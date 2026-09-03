"""Client for talking to a locally-hosted Ollama model over its HTTP API."""

import requests

from logger import Logger


class Model:
    """Thin wrapper around Ollama's ``/api/chat`` endpoint for one model."""

    def __init__(self, model_name: str, logger: Logger):
        """
        Args:
            model_name: The Ollama model tag to query (e.g. "llama3.1:8b"),
                must already be pulled locally (``ollama pull <model_name>``).
            logger: Logger used to record outgoing prompts and raw responses.
        """
        self.model_name = model_name
        self.logger = logger

    def post_prompt(self, prompt: str) -> str:
        """Send a single user prompt to the model via Ollama's chat API.

        Uses Ollama's default (streaming) behavior, so the returned text
        will contain multiple newline-delimited JSON chunks rather than a
        single JSON object — pass ``"stream": false`` in the request body
        to get one consolidated response instead.

        Args:
            prompt: The user's message to send to the model.

        Returns:
            The raw, unparsed response body text from Ollama.
        """
        self.logger.info(f"Posting prompt to model {self.model_name}: {prompt}")
        url = "http://localhost:11434/api/chat"
        response = requests.post(url, json={"model": self.model_name, "messages": [{"role": "user", "content": prompt}]})
        self.logger.info(f"Received response: {response.text}")
        return response.text
