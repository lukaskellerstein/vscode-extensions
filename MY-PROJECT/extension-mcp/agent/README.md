# Luke Editor AI Agent

AI agent that uses Claude Agent SDK to interact with the Luke Editor through an MCP server.

## Setup

```bash
cd agent
uv venv
source .venv/bin/activate
uv sync
```

## Usage

### Interactive Mode

```bash
python main.py
```

Then interact with the agent by typing commands like:
- "Draw a red circle at position 100,100 with radius 50"
- "Draw a blue rectangle at position 200,200 with width 100 and height 60"
- "Write 'Hello World' at position 150,50 with font size 20"
- "Show me all elements on the canvas"

### Demo Mode

```bash
python main.py --demo
```

This will run a predefined demo showcasing the agent's capabilities.

## Architecture

The agent uses:
- **Claude Agent SDK** for AI interactions
- **MCP Server** (stdio) for drawing tools
- The MCP server provides tools: draw_circle, draw_rectangle, write_text, get_elements, get_element_by_id

## Requirements

- Python 3.12+
- Claude Agent SDK
- Anthropic API key (set as ANTHROPIC_API_KEY environment variable)
