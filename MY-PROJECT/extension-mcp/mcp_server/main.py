"""
Luke Editor MCP Server
Provides drawing tools for the Luke Editor VSCode extension.
"""
import json
import asyncio
import sys
from mcp.server.lowlevel import Server
import mcp.types as types
from mcp.server.stdio import stdio_server

from tools.draw_circle import draw_circle
from tools.draw_rectangle import draw_rectangle
from tools.get_elements import get_elements
from tools.get_element_by_id import get_element_by_id
from tools.drawing_api import drawing_api

server = Server("luke-editor-mcp")

# Default file path - can be overridden by command line argument
DEFAULT_FILE = "/tmp/luke_editor_canvas.luke"


async def run_server():
    """Run the MCP server."""

    # Note: Don't set file at startup, let the agent call set_file tool first
    print(f"Luke Editor MCP Server - Ready to accept connections", file=sys.stderr)

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List all available drawing tools."""
        return [
            types.Tool(
                name="get_active_file",
                description="Get the currently active .luke file in VSCode. Use this first before drawing to know which file to work with.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="set_file",
                description="Set the target .luke file to work with by opening it in VSCode",
                inputSchema={
                    "type": "object",
                    "required": ["file_path"],
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Absolute path to the .luke file",
                        }
                    },
                },
            ),
            types.Tool(
                name="draw_circle",
                description="Draw a circle on the canvas",
                inputSchema={
                    "type": "object",
                    "required": ["id", "x", "y", "radius"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique identifier for the circle",
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate of the circle center",
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate of the circle center",
                        },
                        "radius": {
                            "type": "number",
                            "description": "Radius of the circle",
                        },
                        "color": {
                            "type": "string",
                            "description": "Color of the circle (hex format, e.g., #FF0000)",
                            "default": "#000000",
                        },
                    },
                },
            ),
            types.Tool(
                name="draw_rectangle",
                description="Draw a rectangle on the canvas",
                inputSchema={
                    "type": "object",
                    "required": ["id", "x", "y", "width", "height"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique identifier for the rectangle",
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate of the rectangle's top-left corner",
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate of the rectangle's top-left corner",
                        },
                        "width": {
                            "type": "number",
                            "description": "Width of the rectangle",
                        },
                        "height": {
                            "type": "number",
                            "description": "Height of the rectangle",
                        },
                        "color": {
                            "type": "string",
                            "description": "Color of the rectangle (hex format, e.g., #FF0000)",
                            "default": "#000000",
                        },
                    },
                },
            ),
            types.Tool(
                name="get_elements",
                description="Get all drawn elements from the canvas",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="get_element_by_id",
                description="Get a specific element by its ID",
                inputSchema={
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "The unique identifier of the element",
                        }
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool calls."""
        result = None

        if name == "get_active_file":
            result = drawing_api.get_active_file()
        elif name == "set_file":
            file_path = arguments["file_path"]
            drawing_api.set_file(file_path)
            result = {"status": "success", "file_path": file_path}
        elif name == "draw_circle":
            result = draw_circle(
                arguments["id"],
                arguments["x"],
                arguments["y"],
                arguments["radius"],
                arguments.get("color", "#000000"),
            )
        elif name == "draw_rectangle":
            result = draw_rectangle(
                arguments["id"],
                arguments["x"],
                arguments["y"],
                arguments["width"],
                arguments["height"],
                arguments.get("color", "#000000"),
            )
        elif name == "get_elements":
            result = get_elements()
        elif name == "get_element_by_id":
            result = get_element_by_id(arguments["id"])

        result_json = json.dumps(result)
        return [types.TextContent(type="text", text=result_json)]

    # Run the server
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


if __name__ == "__main__":
    asyncio.run(run_server())
