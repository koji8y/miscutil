"""reflection related utilities."""
from typing import Any

import importlib


def get_module(fully_qualified_name: str) -> Any:
    """get module."""
    return importlib.import_module(fully_qualified_name)
