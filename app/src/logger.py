"""Console logger factory for the RAG chatbot."""

import logging


class Logger:
    """Wraps the standard library ``logging`` module with a console handler.

    Creates a named logger that prints timestamped, leveled messages to
    the console at DEBUG level and above.
    """

    def __init__(self, name: str):
        """Create and configure a logger with the given name.

        Args:
            name: Name used to identify this logger (e.g. the component
                or application name), shown in every log line.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add formatter to console handler
        ch.setFormatter(formatter)

        # Add console handler to logger
        self.logger.addHandler(ch)

    def get_logger(self):
        """Return the underlying configured ``logging.Logger`` instance."""
        return self.logger
