"""
This file makes the directory a Python package and ensures all concrete
processors (like downstream_app_1.py) are imported when the package is
imported, which triggers their self-registration logic.
"""
from .base_processor import BaseProcessor, ProcessorRegistry

# Explicitly import all concrete processor modules to trigger their
# self-registration logic defined at the bottom of each file.
# As you add new downstream apps (e.g., 'downstream_app_2.py'),
# simply add them to this list.
from . import downstream_app_1

# Optionally expose the registry and base class for convenience
__all__ = ["BaseProcessor", "ProcessorRegistry"]