#!/usr/bin/env python3
"""
Luke Editor AI Agent

AI agent that uses the Luke Editor MCP server to draw shapes and text.
The agent communicates with the MCP server via stdio.
"""

import anyio
import sys
from pathlib import Path
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)
from claude_agent_sdk.types import McpStdioServerConfig


async def run_agent():
    """Run the Luke Editor AI agent with MCP server integration."""

    # Get the path to the MCP server
    mcp_server_path = Path(__file__).parent.parent / "mcp_server"

    # Configure the Luke Editor MCP server
    # Use the MCP server's venv Python to ensure dependencies are available
    luke_server: McpStdioServerConfig = {
        "command": str(mcp_server_path / ".venv" / "bin" / "python"),
        "args": [str(mcp_server_path / "main.py")],
        "env": {},
    }

    # Setup agent options with MCP server
    options = ClaudeAgentOptions(
        mcp_servers={"luke_editor": luke_server},
        # Allow all tools from luke_editor MCP server
        allowed_tools=[
            "mcp__luke_editor",
        ],
        system_prompt=(
            "You are an AI assistant with access to Luke Editor drawing tools. "
            "You can use these tools to draw shapes and manage elements in .luke files:\n"
            "- get_active_file: Get the currently active .luke file (ALWAYS call this FIRST)\n"
            "- set_file: Set/open a different .luke file in VSCode\n"
            "- draw_circle: Draw a circle with id, x, y, radius, and color\n"
            "- draw_rectangle: Draw a rectangle with id, x, y, width, height, and color\n"
            "- get_elements: Get all drawn elements\n"
            "- get_element_by_id: Get a specific element by ID\n\n"
            "IMPORTANT: When users ask you to draw shapes:\n"
            "1. FIRST call get_active_file to find out which .luke file is currently open in VSCode\n"
            "2. Then use that file to draw shapes\n"
            "3. NEVER create new files or use /tmp paths\n"
            "4. If no file is active, ask the user to open a .luke file first"
        ),
    )

    print("=" * 70)
    print("Luke Editor AI Agent")
    print("=" * 70)
    print()
    print("Available commands:")
    print("  - Draw shapes (circles, rectangles)")
    print("  - Get all elements")
    print("  - Get element by ID")
    print()
    print("Example: 'Draw a blue circle at position 500,500 with radius 50'")
    print("Example: 'Draw a blue circle at random position with radius 50'")
    print()
    print("Type 'exit' or 'quit' to stop")
    print("=" * 70)
    print()

    async with ClaudeSDKClient(options=options) as client:
        # Debug: Print available tools
        print("\nDebug: Checking available tools...")
        print(f"MCP servers configured: {list(options.mcp_servers.keys())}")
        print(f"Allowed tools: {options.allowed_tools}")
        print()

        while True:
            # Get user input
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            # Send query to agent
            await client.query(user_input)

            # Process response
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}")
                        elif isinstance(block, ToolUseBlock):
                            print(f"  [Using tool: {block.name}]")
                            if block.input:
                                print(f"  [Input: {block.input}]")
                elif isinstance(message, ResultMessage):
                    if message.total_cost_usd and message.total_cost_usd > 0:
                        print(f"  [Cost: ${message.total_cost_usd:.4f}]")

            print()


async def run_demo():
    """Run a demo showcasing the agent's capabilities."""

    # Get the path to the MCP server
    mcp_server_path = Path(__file__).parent.parent / "mcp_server"

    # Configure the Luke Editor MCP server
    # Use the MCP server's venv Python to ensure dependencies are available
    luke_server: McpStdioServerConfig = {
        "command": str(mcp_server_path / ".venv" / "bin" / "python"),
        "args": [str(mcp_server_path / "main.py")],
        "env": {},
    }

    options = ClaudeAgentOptions(
        mcp_servers={"luke_editor": luke_server},
        # Allow all tools from luke_editor MCP server
        allowed_tools=[
            "mcp__luke_editor",
        ],
        system_prompt=(
            "You are an AI assistant with access to Luke Editor drawing tools. "
            "You can use these tools to draw shapes and manage elements in .luke files:\n"
            "- get_active_file: Get the currently active .luke file (ALWAYS call this FIRST)\n"
            "- set_file: Set/open a different .luke file in VSCode\n"
            "- draw_circle: Draw a circle with id, x, y, radius, and color\n"
            "- draw_rectangle: Draw a rectangle with id, x, y, width, height, and color\n"
            "- get_elements: Get all drawn elements\n"
            "- get_element_by_id: Get a specific element by ID\n\n"
            "IMPORTANT: When users ask you to draw shapes:\n"
            "1. FIRST call get_active_file to find out which .luke file is currently open in VSCode\n"
            "2. Then use that file to draw shapes\n"
            "3. NEVER create new files or use /tmp paths\n"
            "4. If no file is active, ask the user to open a .luke file first"
        ),
    )

    print("=" * 70)
    print("Luke Editor AI Agent - Demo Mode")
    print("=" * 70)
    print()

    async with ClaudeSDKClient(options=options) as client:
        # Demo 1: Set file and draw shapes
        print("Demo 1: Setting file and drawing shapes")
        print("-" * 70)
        await client.query(
            "Set the file to /tmp/luke_demo.luke. "
            "Then draw a blue circle with id 'circle1' at position (100, 100) with radius 50. "
            "Then draw a red rectangle with id 'rect1' at position (200, 200) with width 100 and height 60."
        )

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")
                    elif isinstance(block, ToolUseBlock):
                        print(f"  [Tool: {block.name}]")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"  [Cost: ${message.total_cost_usd:.4f}]")

        print()

        # Demo 2: Get all elements
        print("Demo 2: Getting all elements")
        print("-" * 70)
        await client.query("Show me all the elements on the canvas.")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")
                    elif isinstance(block, ToolUseBlock):
                        print(f"  [Tool: {block.name}]")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"  [Cost: ${message.total_cost_usd:.4f}]")

        print()

    print("=" * 70)
    print("Demo completed!")
    print("=" * 70)


async def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        await run_demo()
    else:
        await run_agent()


if __name__ == "__main__":
    anyio.run(main)
