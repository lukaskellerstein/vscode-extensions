"""Get all elements tool."""
from .drawing_api import drawing_api


def get_elements() -> list:
    """
    Get all drawn elements from the canvas.

    Returns:
        List of all elements with their properties
    """
    return drawing_api.get_elements()
