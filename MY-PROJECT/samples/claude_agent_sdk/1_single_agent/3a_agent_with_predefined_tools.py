#!/usr/bin/env python3
"""
Single Agent Example (c): Agent with Predefined Tools

Demonstrates using built-in Claude Code tools like Read, Write, Bash, etc.
"""

import anyio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)


async def example_read_write_tools():
    """Agent with Read and Write tools."""
    print("=== Example 1: Read and Write Tools ===\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write"],
        system_prompt="You are a file management assistant.",
    )

    async for message in query(
        prompt="Create a file called /tmp/test_claude.txt with the content 'Hello from Claude SDK!'",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"Using tool: {block.name}")
                    print(f"  Input: {block.input}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")

    print("\n")


async def example_bash_tool():
    """Agent with Bash tool."""
    print("=== Example 2: Bash Tool ===\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Bash"],
        system_prompt="You are a command-line assistant.",
    )

    async for message in query(
        prompt="List the files in the current directory using ls command",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"Using tool: {block.name}")
                    print(f"  Command: {block.input.get('command', 'N/A')}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")

    print("\n")


async def example_search_tools():
    """Agent with search and navigation tools."""
    print("=== Example 3: Search Tools (Glob, Grep) ===\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Glob", "Grep", "Read"],
        system_prompt="You are a code search assistant.",
    )

    async for message in query(
        prompt="Find all Python files in the current directory using glob pattern",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"Using tool: {block.name}")
                    print(f"  Input: {block.input}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")

    print("\n")


async def example_multiple_tools():
    """Agent with multiple predefined tools."""
    print("=== Example 4: Multiple Tools ===\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash", "Glob", "Edit"],
        system_prompt="You are a comprehensive development assistant.",
    )

    async for message in query(
        prompt="Count how many Python files are in the single_agent directory",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"Using tool: {block.name}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")
            print(f"Total turns: {message.num_turns}")

    print("\n")


async def main():
    """Run all predefined tools examples."""
    await example_read_write_tools()
    await example_bash_tool()
    await example_search_tools()
    await example_multiple_tools()


if __name__ == "__main__":
    anyio.run(main)
