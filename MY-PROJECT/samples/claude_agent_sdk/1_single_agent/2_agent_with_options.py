#!/usr/bin/env python3
"""
Single Agent Example (b): Agent with Options

Demonstrates using ClaudeAgentOptions to configure the agent with:
- Custom system prompts
- Model selection
- Max turns
- Permission modes
- Working directory
"""

import anyio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)


async def example_system_prompt():
    """Agent with custom system prompt."""
    print("=== Example 1: Custom System Prompt ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant that always responds in a pirate accent.",
        max_turns=1,
    )

    async for message in query(
        prompt="Tell me about Python programming.", options=options
    ):

        print("-----")
        print(message)
        print("-----\n")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")

    print("\n")


async def example_model_selection():
    """Agent with specific model selection."""
    print("=== Example 2: Model Selection ===\n")

    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt="You are a code review assistant.",
        max_turns=1,
    )

    async for message in query(
        prompt="Explain the difference between async and sync in one sentence.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")
            print(f"Model: {message.usage.get('model') if message.usage else 'N/A'}")

    print("\n")


async def example_permission_mode():
    """Agent with permission mode configuration."""
    print("=== Example 3: Permission Mode ===\n")

    options = ClaudeAgentOptions(
        permission_mode="acceptEdits",  # Auto-accept file edits
        system_prompt="You are a helpful file management assistant.",
    )

    async for message in query(
        prompt="What permission mode allows auto-accepting file edits?",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")

    print("\n")


async def example_combined_options():
    """Agent with multiple options combined."""
    print("=== Example 4: Combined Options ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a concise technical documentation writer.",
        model="claude-sonnet-4-5-20250929",
        max_turns=2,
        permission_mode="default",
    )

    async for message in query(
        prompt="Explain what ClaudeAgentOptions is in 2 sentences.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\nCost: ${message.total_cost_usd:.4f}")
            print(f"Turns: {message.num_turns}")

    print("\n")


async def main():
    """Run all option examples."""
    await example_system_prompt()
    await example_model_selection()
    await example_permission_mode()
    await example_combined_options()


if __name__ == "__main__":
    anyio.run(main)
