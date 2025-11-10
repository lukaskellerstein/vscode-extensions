"""Draw rectangle tool."""
from .drawing_api import drawing_api


def draw_rectangle(id: str, x: float, y: float, width: float, height: float, color: str = "#000000") -> dict:
    """
    Draw a rectangle on the canvas.

    Args:
        id: Unique identifier for the rectangle
        x: X coordinate of the rectangle's top-left corner
        y: Y coordinate of the rectangle's top-left corner
        width: Width of the rectangle
        height: Height of the rectangle
        color: Color of the rectangle (hex format, default: #000000)

    Returns:
        Dictionary containing the rectangle data
    """
    return drawing_api.draw_rectangle(id, x, y, width, height, color)
