#!/usr/bin/env python3
"""
Test MCP server tools directly without Claude Agent SDK
"""
import asyncio
import json
from pathlib import Path
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def test_mcp_tools():
    # Get the path to the MCP server
    mcp_server_path = Path(__file__).parent.parent / "mcp_server"

    server_params = StdioServerParameters(
        command="python",
        args=[str(mcp_server_path / "main.py")]
    )

    print("Connecting to MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            result = await session.initialize()
            print(f"Initialized: {result.server_info.name}")
            print()

            # List tools
            tools_result = await session.list_tools()
            print(f"Available tools ({len(tools_result.tools)}):")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # Test set_file
            print("Testing set_file tool...")
            result = await session.call_tool("set_file", {
                "file_path": "/tmp/test_canvas.luke"
            })
            print(f"Result: {result.content}")
            print()

            # Test draw_circle
            print("Testing draw_circle tool...")
            result = await session.call_tool("draw_circle", {
                "id": "test_circle_1",
                "x": 100,
                "y": 100,
                "radius": 50,
                "color": "#FF0000"
            })
            print(f"Result: {result.content}")
            print()

            # Test get_elements
            print("Testing get_elements tool...")
            result = await session.call_tool("get_elements", {})
            print(f"Result: {result.content}")
            print()

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
