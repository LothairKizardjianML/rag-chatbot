"""Application configuration, exposed as a process-wide singleton."""

import os

from pathlib import Path


class Singleton:
    """Base class that restricts a subclass to a single shared instance.

    Any class inheriting from ``Singleton`` will always return the same
    instance, no matter how many times it is constructed.
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
        return cls._instances[cls]


class Config(Singleton):
    """Holds application-wide configuration values.

    Values are read from environment variables, falling back to sane
    defaults when unset.
    """

    def __init__(self):
        self.api_key = os.getenv("API_KEY", "default_api_key")
        self.ingestion_folder = os.path.join(os.path.dirname(os.getcwd()), "app", "data", "ingestion")