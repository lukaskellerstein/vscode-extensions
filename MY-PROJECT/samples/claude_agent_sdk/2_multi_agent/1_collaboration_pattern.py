#!/usr/bin/env python3
"""Collaboration Pattern Implementation.

In this pattern, multiple agents work in a defined sequential order.
Each agent can either return an answer to the user or pass the solution
to the next agent in the group. The order of agents is predefined.

Key Characteristics:
- All agents are "equal" (no hierarchy)
- Order of agents is defined
- Each agent can pass work to the next agent in sequence

Usage:
    python collaboration_pattern.py
"""

import anyio

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


class CollaborationGroup:
    """Manages a group of agents working in collaboration pattern."""

    def __init__(self, agents: list[tuple[str, AgentDefinition]], options: ClaudeAgentOptions | None = None):
        """Initialize collaboration group.

        Args:
            agents: List of (agent_name, agent_definition) tuples in order
            options: Base options for the Claude client
        """
        self.agent_names = [name for name, _ in agents]
        self.agent_definitions = {name: defn for name, defn in agents}
        self.options = options or ClaudeAgentOptions()
        self.options.agents = self.agent_definitions

    async def execute(self, initial_task: str) -> str:
        """Execute the collaboration pattern with the initial task.

        Args:
            initial_task: The initial task to process

        Returns:
            Final result from the collaboration
        """
        result = ""
        context = initial_task

        async with ClaudeSDKClient(options=self.options) as client:
            for agent_name in self.agent_names:
                print(f"\n{'='*60}")
                print(f"Agent: {agent_name}")
                print(f"{'='*60}")

                # Construct the prompt for this agent
                prompt = f"""You are working as part of a collaboration group.

Your role: {self.agent_definitions[agent_name].description}

Current task/context:
{context}

Please process this task and provide your contribution. If you believe the task needs
further processing by another specialist, clearly indicate what should be passed forward.
Otherwise, provide the final answer."""

                await client.query(prompt)

                # Collect the agent's response
                agent_response = []
                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                print(f"{agent_name}: {block.text}")
                                agent_response.append(block.text)
                    elif isinstance(msg, ResultMessage):
                        if msg.total_cost_usd and msg.total_cost_usd > 0:
                            print(f"\nCost for {agent_name}: ${msg.total_cost_usd:.4f}")

                # Update context for next agent
                context = "\n".join(agent_response)
                result = context

        return result


async def demo_software_development():
    """Demonstrate collaboration pattern with software development workflow."""
    print("\n" + "="*80)
    print("COLLABORATION PATTERN DEMO: Software Development Workflow")
    print("="*80)

    # Define agents in order of collaboration
    agents = [
        ("requirements-analyst", AgentDefinition(
            description="Analyzes requirements and creates technical specifications",
            prompt="You are a requirements analyst. Analyze user requirements and create "
                   "clear technical specifications. Focus on what needs to be built.",
            tools=["Read", "Grep"],
            model="sonnet",
        )),
        ("architect", AgentDefinition(
            description="Designs system architecture and components",
            prompt="You are a software architect. Based on requirements, design the system "
                   "architecture, define components, and specify technologies to use.",
            tools=["Read", "Glob"],
            model="sonnet",
        )),
        ("developer", AgentDefinition(
            description="Implements the solution based on architecture",
            prompt="You are a software developer. Implement the solution based on the "
                   "architecture and requirements. Write clean, maintainable code.",
            tools=["Read", "Write", "Edit"],
            model="sonnet",
        )),
    ]

    group = CollaborationGroup(agents)

    task = """Create a simple REST API for a todo list application.
    The API should support:
    - Creating new todos
    - Listing all todos
    - Marking todos as complete
    - Deleting todos
    """

    result = await group.execute(task)

    print("\n" + "="*80)
    print("FINAL RESULT:")
    print("="*80)
    print(result)


async def demo_content_creation():
    """Demonstrate collaboration pattern with content creation workflow."""
    print("\n" + "="*80)
    print("COLLABORATION PATTERN DEMO: Content Creation Workflow")
    print("="*80)

    # Define agents in order of collaboration
    agents = [
        ("researcher", AgentDefinition(
            description="Researches topics and gathers information",
            prompt="You are a researcher. Gather relevant information and create a "
                   "comprehensive research summary on the given topic.",
            tools=["Read", "Grep", "Glob"],
            model="sonnet",
        )),
        ("writer", AgentDefinition(
            description="Creates engaging content based on research",
            prompt="You are a content writer. Transform research into engaging, well-structured "
                   "content. Focus on clarity and reader engagement.",
            tools=["Read", "Write"],
            model="sonnet",
        )),
        ("editor", AgentDefinition(
            description="Reviews and polishes content",
            prompt="You are an editor. Review content for grammar, style, consistency, and "
                   "overall quality. Make final improvements.",
            tools=["Read", "Edit"],
            model="sonnet",
        )),
    ]

    group = CollaborationGroup(agents)

    task = """Create a blog post explaining the concept of multi-agent systems
    in AI, focusing on collaboration patterns."""

    result = await group.execute(task)

    print("\n" + "="*80)
    print("FINAL RESULT:")
    print("="*80)
    print(result)


async def main():
    """Run collaboration pattern demonstrations."""
    # Uncomment the demo you want to run:

    await demo_software_development()
    # await demo_content_creation()


if __name__ == "__main__":
    anyio.run(main)
