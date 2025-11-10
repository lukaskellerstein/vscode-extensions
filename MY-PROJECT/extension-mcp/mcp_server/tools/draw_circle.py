"""Draw circle tool."""
from .drawing_api import drawing_api


def draw_circle(id: str, x: float, y: float, radius: float, color: str = "#000000") -> dict:
    """
    Draw a circle on the canvas.

    Args:
        id: Unique identifier for the circle
        x: X coordinate of the circle center
        y: Y coordinate of the circle center
        radius: Radius of the circle
        color: Color of the circle (hex format, default: #000000)

    Returns:
        Dictionary containing the circle data
    """
    return drawing_api.draw_circle(id, x, y, radius, color)
