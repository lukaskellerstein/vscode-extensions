"""
Drawing API for Luke Editor.
This module communicates with the VSCode extension via WebSocket.
The VSCode extension handles all file operations.
"""

import sys
import json
from typing import Dict, List
from dataclasses import dataclass, asdict
from pathlib import Path
import websocket


@dataclass
class Circle:
    id: str
    x: float
    y: float
    radius: float
    color: str = "#000000"


@dataclass
class Rectangle:
    id: str
    x: float
    y: float
    width: float
    height: float
    color: str = "#000000"


class DrawingAPI:
    """
    Interface to communicate with the VSCode extension via WebSocket.
    The extension provides a WebSocket endpoint that handles all drawing operations.
    """

    def __init__(self):
        self.file_path: str | None = None
        self.vscode_port: int | None = None
        self.ws: websocket.WebSocket | None = None
        # Don't connect at startup, connect on first command
        self._discover_vscode_port()

    def _discover_vscode_port(self):
        """Discover the VSCode extension WebSocket port from the port file."""
        possible_paths = [
            Path.home() / ".vscode" / "extensions" / "globalStorage" / "mcp_port.txt",
            Path.home()
            / ".config"
            / "Code"
            / "User"
            / "globalStorage"
            / "mcp_port.txt",
            Path("/tmp") / "luke_editor_mcp_port.txt",
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    with open(path, "r") as f:
                        self.vscode_port = int(f.read().strip())
                        print(
                            f"Discovered VSCode extension port: {self.vscode_port}",
                            file=sys.stderr,
                        )
                        return
                except (ValueError, IOError) as e:
                    print(f"Error reading port from {path}: {e}", file=sys.stderr)
                    continue

        print("Warning: Could not discover VSCode extension port.", file=sys.stderr)

    def _connect(self):
        """Connect to the VSCode extension WebSocket server."""
        if not self.vscode_port:
            self._discover_vscode_port()

        if not self.vscode_port:
            print(
                "Warning: VSCode extension WebSocket server not found. Will retry on first command.",
                file=sys.stderr,
            )
            return

        try:
            ws_url = f"ws://localhost:{self.vscode_port}"
            self.ws = websocket.create_connection(ws_url, timeout=5)
            print(
                f"Connected to VSCode extension WebSocket at {ws_url}", file=sys.stderr
            )
        except Exception as e:
            print(f"Failed to connect to VSCode extension: {e}", file=sys.stderr)
            self.ws = None

    def _ensure_connected(self):
        """Ensure WebSocket connection is established."""
        if self.ws and self.ws.connected:
            return

        # Try to reconnect
        self._discover_vscode_port()
        if not self.vscode_port:
            raise Exception(
                "VSCode extension WebSocket server not found. Make sure the extension is running."
            )

        self._connect()
        if not self.ws or not self.ws.connected:
            raise Exception("Failed to connect to VSCode extension WebSocket server.")

    def _send_command(self, command: Dict) -> Dict:
        """Send a command to the VSCode extension WebSocket endpoint."""
        self._ensure_connected()

        try:
            # Send command
            self.ws.send(json.dumps(command))

            # Receive response
            response_str = self.ws.recv()
            response = json.loads(response_str)

            if response.get("success"):
                return response.get("result", {})
            else:
                raise Exception(response.get("error", "Unknown error"))

        except Exception as e:
            # Connection might be broken, try to reconnect on next call
            if self.ws:
                self.ws.close()
            self.ws = None
            raise Exception(f"Failed to communicate with VSCode extension: {e}")

    def get_active_file(self) -> Dict:
        """Get the currently active .luke file in VSCode."""
        command = {"type": "get_active_file"}
        result = self._send_command(command)
        # Update our cached file path
        if result.get("file_path"):
            self.file_path = result["file_path"]
        return result

    def set_file(self, file_path: str):
        """Set the target .luke file."""
        self.file_path = file_path
        command = {"type": "set_file", "file_path": file_path}
        return self._send_command(command)

    def draw_circle(
        self, id: str, x: float, y: float, radius: float, color: str = "#000000"
    ) -> Dict:
        """Draw a circle on the canvas."""
        if not self.file_path:
            raise Exception("No file path set. Call set_file first.")

        circle = Circle(id=id, x=x, y=y, radius=radius, color=color)
        command = {
            "type": "draw_circle",
            "file_path": self.file_path,
            "data": asdict(circle),
        }
        return self._send_command(command)

    def draw_rectangle(
        self,
        id: str,
        x: float,
        y: float,
        width: float,
        height: float,
        color: str = "#000000",
    ) -> Dict:
        """Draw a rectangle on the canvas."""
        if not self.file_path:
            raise Exception("No file path set. Call set_file first.")

        rectangle = Rectangle(id=id, x=x, y=y, width=width, height=height, color=color)
        command = {
            "type": "draw_rectangle",
            "file_path": self.file_path,
            "data": asdict(rectangle),
        }
        return self._send_command(command)

    def get_elements(self) -> List[Dict]:
        """Get all drawn elements."""
        if not self.file_path:
            raise Exception("No file path set. Call set_file first.")

        command = {"type": "get_elements", "file_path": self.file_path}
        result = self._send_command(command)
        return result if isinstance(result, list) else []

    def get_element_by_id(self, id: str) -> Dict | None:
        """Get a specific element by its ID."""
        if not self.file_path:
            raise Exception("No file path set. Call set_file first.")

        command = {
            "type": "get_element_by_id",
            "file_path": self.file_path,
            "data": {"id": id},
        }
        return self._send_command(command)


# Global instance
drawing_api = DrawingAPI()
