import logging
from abc import ABC, abstractmethod

# --- Centralized Registry and Base Interface ---

class BaseProcessor(ABC):
    """
    Abstract Base Class (Interface) for all data processors.
    All concrete processors must inherit from this class and implement
    the 'process' method.
    """
    @abstractmethod
    def process(self, data: dict) -> dict:
        """
        Processes the input JSON data and returns a transformed dictionary.
        """
        pass

class ProcessorRegistry:
    """
    Manages and isolates different concrete processor implementations.
    This centralized dictionary is the single source of truth for routing.
    """
    _processors = {}

    @classmethod
    def register_processor(cls, name: str, processor: BaseProcessor):
        """Registers a processor instance with a unique name (key)."""
        if not isinstance(processor, BaseProcessor):
            raise TypeError(f"The object registered under '{name}' must be an instance of BaseProcessor.")
        cls._processors[name] = processor
        logging.info(f"Processor '{name}' registered successfully.")

    @classmethod
    def get_processor(cls, name: str) -> BaseProcessor | None:
        """Retrieves a registered processor by name."""
        return cls._processors.get(name)

    @classmethod
    def list_processors(cls) -> list[str]:
        """Returns a list of all registered processor names."""
        return list(cls._processors.keys())

# --- Logging Helper (Used in health check/function_app.py) ---

def configure_logging(level=logging.INFO):
    """Sets up basic logging configuration."""
    # In Azure Functions, the logging library automatically hooks into Application Insights,
    # so standard logging.info/error/etc. is the recommended way.
    logging.basicConfig(level=level)
