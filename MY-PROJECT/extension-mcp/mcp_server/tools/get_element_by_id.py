"""Get element by ID tool."""
from .drawing_api import drawing_api


def get_element_by_id(id: str) -> dict | None:
    """
    Get a specific element by its ID.

    Args:
        id: The unique identifier of the element

    Returns:
        Dictionary containing the element data, or None if not found
    """
    return drawing_api.get_element_by_id(id)
