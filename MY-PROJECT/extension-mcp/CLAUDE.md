# Goal

Implement VSCode extension (folder `extension`) and AI agent (folder `agent`). AI agent will use MCP server (via stdio) with tools (ex. draw circle, draw rectangle, get all drawn elements ... etc.), and the MCP server will communicate with

## Agent

Agent will be implemented via `claude_agent_sdk`. All examples are located in folder `samples/claude_agent_sdk`. Notice especially the example with MCP: `samples/claude_agent_sdk/3c_agent_with_mcp_tools.py`

## MCP

MCP server will be implemented via `stdio`. All examples are located in folder `samples/mcp`. Notice expecially the example with simplest tools implementation for server: `samples/mcp/1_tools/my_server`

## Editor

Editor will open when user selects `.luke` file. The editor will provide it's functionality via "interface/API". The MCP server will further provide these functionalities to the AI agent.

Functionalities:

- Draw circle
- Draw rectangle
- Write text
- Get elements
- Get element by ID
- ..etc.

## Communication

When agent chooses to use some MCP tool, it will call the MCP tool. The MCP tool will handover the request to the editor, and the editor will proceed with the task. The MCP tool itself should not manipulate with the files directly, but only via editor.
