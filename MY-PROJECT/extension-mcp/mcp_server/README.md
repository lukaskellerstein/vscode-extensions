# Luke Editor MCP Server

MCP server providing drawing tools for the Luke Editor VSCode extension.

## Setup

```bash
cd mcp_server
uv venv
source .venv/bin/activate
uv sync
```

## Run

```bash
python main.py
```

## Available Tools

- `draw_circle`: Draw a circle on the canvas
- `draw_rectangle`: Draw a rectangle on the canvas
- `write_text`: Write text on the canvas
- `get_elements`: Get all drawn elements
- `get_element_by_id`: Get a specific element by its ID

## Architecture

The MCP server communicates via stdio with the AI agent and provides drawing functionality that will interface with the VSCode extension's custom editor.
