#!/usr/bin/env python3
"""
Single Agent Example (e): Agent with Memory

Demonstrates continuing conversations - the agent remembers previous exchanges
and can reference them in subsequent queries.
"""

import anyio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)


async def example_conversation_memory():
    """Multi-turn conversation with memory using ClaudeSDKClient."""
    print("=== Example 1: Conversation with Memory ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant with memory of our conversation.",
    )

    async with ClaudeSDKClient(options=options) as client:
        # First query
        print("User: My favorite color is blue.\n")
        await client.query("My favorite color is blue.")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

        # Second query - referencing the first
        print("User: What color did I just tell you about?\n")
        await client.query("What color did I just tell you about?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

        # Third query - building on conversation
        print("User: Can you suggest a complementary color?\n")
        await client.query("Can you suggest a complementary color to my favorite?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

    print("\n")


async def example_technical_conversation():
    """Multi-turn technical conversation with context building."""
    print("=== Example 2: Technical Conversation with Context ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a Python programming tutor.",
    )

    async with ClaudeSDKClient(options=options) as client:
        # First: Define a concept
        print("User: Explain what a list comprehension is in Python.\n")
        await client.query(
            "Explain what a list comprehension is in Python in one sentence."
        )

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

        # Second: Ask for an example
        print("User: Give me an example of what you just explained.\n")
        await client.query("Give me a simple code example of what you just explained.")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

        # Third: Ask for comparison
        print("User: How is that different from a regular for loop?\n")
        await client.query("How is that different from a regular for loop?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}\n")

    print("\n")


async def example_session_continuation():
    """Demonstrate session continuation across different client instances."""
    print("=== Example 3: Session Continuation ===\n")

    session_id = None

    # First conversation session
    print("--- First Session ---")
    options1 = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant.",
    )

    async with ClaudeSDKClient(options=options1) as client:
        print("User: Remember this number: 42\n")
        await client.query("Remember this number: 42")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
            elif isinstance(message, ResultMessage):
                # Save session ID for continuation
                session_id = message.session_id
                if message.total_cost_usd and message.total_cost_usd > 0:
                    print(f"\nCost: ${message.total_cost_usd:.4f}")
                print(f"Session ID: {session_id}\n")

    # Second conversation session - resuming from first
    if session_id:
        print("--- Resumed Session ---")
        options2 = ClaudeAgentOptions(
            resume=session_id,  # Resume from previous session
            system_prompt="You are a helpful assistant.",
        )

        async with ClaudeSDKClient(options=options2) as client:
            print("User: What number did I ask you to remember?\n")
            await client.query("What number did I ask you to remember?")

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
                elif isinstance(message, ResultMessage):
                    if message.total_cost_usd and message.total_cost_usd > 0:
                        print(f"\nCost: ${message.total_cost_usd:.4f}\n")

    print("\n")


async def main():
    """Run all memory examples."""
    await example_conversation_memory()
    await example_technical_conversation()
    await example_session_continuation()


if __name__ == "__main__":
    anyio.run(main)
