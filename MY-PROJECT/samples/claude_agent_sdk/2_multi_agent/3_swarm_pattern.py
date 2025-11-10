#!/usr/bin/env python3
"""Swarm Pattern Implementation.

In this pattern, each agent has defined "handoffs" that specify which agents
they can pass work to. Each agent autonomously decides to which agent from their
handoff list they will pass the work next.

Key Characteristics:
- All agents are "equal" (no hierarchy)
- No specific order of agents (unlike collaboration)
- Only the first agent is defined
- Each agent has a handoff list of possible next agents
- Each agent decides autonomously which handoff to use

Usage:
    python swarm_pattern.py
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


class SwarmAgent:
    """Represents an agent in the swarm with its handoffs."""

    def __init__(
        self, name: str, definition: AgentDefinition, handoffs: list[str] | None = None
    ):
        """Initialize a swarm agent.

        Args:
            name: Agent name
            definition: Agent definition
            handoffs: List of agent names this agent can hand off to
        """
        self.name = name
        self.definition = definition
        self.handoffs = handoffs or []


class Swarm:
    """Manages a swarm of agents with dynamic handoffs."""

    def __init__(
        self,
        agents: dict[str, SwarmAgent],
        initial_agent: str,
        options: ClaudeAgentOptions | None = None,
    ):
        """Initialize the swarm.

        Args:
            agents: Dictionary of {agent_name: SwarmAgent}
            initial_agent: Name of the agent that receives the first task
            options: Base options for the Claude client
        """
        self.agents = agents
        self.initial_agent = initial_agent
        self.options = options or ClaudeAgentOptions()

        # Build agent definitions for options
        self.options.agents = {name: agent.definition for name, agent in agents.items()}

    async def execute(self, initial_task: str, max_handoffs: int = 10) -> str:
        """Execute the swarm pattern with the initial task.

        Args:
            initial_task: The initial task to process
            max_handoffs: Maximum number of handoffs allowed

        Returns:
            Final result from the swarm
        """
        result = ""
        current_agent = self.initial_agent
        context = initial_task
        handoff_count = 0

        async with ClaudeSDKClient(options=self.options) as client:
            while handoff_count < max_handoffs:
                agent = self.agents[current_agent]

                print(f"\n{'='*60}")
                print(f"Current Agent: {current_agent}")
                print(f"Handoff Count: {handoff_count}/{max_handoffs}")
                print(f"{'='*60}")

                # Build handoff information
                if agent.handoffs:
                    handoff_info = "\n".join(
                        [
                            f"- {name}: {self.agents[name].definition.description}"
                            for name in agent.handoffs
                        ]
                    )
                else:
                    handoff_info = "None - This is a terminal agent"

                # Construct the prompt for this agent
                prompt = f"""You are {current_agent}, working in a swarm of collaborative agents.

Your role: {agent.definition.description}

Current task/context:
{context}

Available handoffs (agents you can pass work to):
{handoff_info}

Instructions:
1. Analyze the task and decide if you can handle it or if it needs another specialist
2. If you can complete the task, provide the FINAL ANSWER
3. If you need to hand off, specify which agent should handle it and what task to give them

To hand off to another agent, use this format:
HANDOFF TO: [agent-name]
TASK: [specific task for that agent]
CONTEXT: [any relevant context to pass along]

To provide the final answer, use this format:
FINAL ANSWER:
[your complete answer]
"""

                await client.query(prompt)

                # Collect the agent's response
                agent_response = []
                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                print(f"{current_agent}: {block.text}")
                                agent_response.append(block.text)
                    elif isinstance(msg, ResultMessage):
                        if msg.total_cost_usd and msg.total_cost_usd > 0:
                            print(
                                f"\nCost for {current_agent}: ${msg.total_cost_usd:.4f}"
                            )

                response_text = "\n".join(agent_response)

                # Check if agent wants to hand off
                if "HANDOFF TO:" in response_text:
                    handoff = self._parse_handoff(response_text, agent.handoffs)

                    if handoff:
                        next_agent, task, handoff_context = handoff

                        # Validate handoff is allowed
                        if next_agent not in agent.handoffs:
                            print(
                                f"\n⚠️  Warning: {current_agent} tried to hand off to {next_agent}, "
                                f"but it's not in their handoff list!"
                            )
                            result = response_text
                            break

                        # Update for next iteration
                        current_agent = next_agent
                        context = f"Previous agent: {agent.name}\nTask: {task}\nContext: {handoff_context}"
                        handoff_count += 1
                    else:
                        # Could not parse handoff, treat as final answer
                        result = response_text
                        break
                elif "FINAL ANSWER:" in response_text:
                    # Agent has provided final answer
                    result = response_text.split("FINAL ANSWER:")[1].strip()
                    break
                else:
                    # No handoff marker, treat as final answer
                    result = response_text
                    break

        if handoff_count >= max_handoffs:
            result += f"\n\n⚠️  Reached maximum handoff limit ({max_handoffs})"

        return result

    def _parse_handoff(
        self, text: str, valid_handoffs: list[str]
    ) -> tuple[str, str, str] | None:
        """Parse handoff request from agent's response.

        Args:
            text: Agent's response text
            valid_handoffs: List of valid agent names for handoff

        Returns:
            Tuple of (agent_name, task, context) or None if parsing fails
        """
        try:
            lines = text.split("\n")
            agent_name = None
            task = None
            context_text = ""

            for i, line in enumerate(lines):
                if "HANDOFF TO:" in line:
                    agent_name = line.split("HANDOFF TO:")[1].strip()
                elif "TASK:" in line and agent_name:
                    # Collect task lines
                    task_lines = [line.split("TASK:")[1].strip()]
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("CONTEXT:"):
                        if lines[j].strip():
                            task_lines.append(lines[j].strip())
                        j += 1
                    task = " ".join(task_lines)
                elif "CONTEXT:" in line:
                    # Collect context lines
                    context_lines = [line.split("CONTEXT:")[1].strip()]
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip():
                            context_lines.append(lines[j].strip())
                    context_text = " ".join(context_lines)
                    break

            if agent_name and task and agent_name in valid_handoffs:
                return (agent_name, task, context_text)

            return None
        except Exception:
            return None


async def demo_customer_support():
    """Demonstrate swarm pattern with customer support workflow."""
    print("\n" + "=" * 80)
    print("SWARM PATTERN DEMO: Customer Support System")
    print("=" * 80)

    # Define agents with their handoffs
    agents = {
        "triage": SwarmAgent(
            name="triage",
            definition=AgentDefinition(
                description="Initial contact point that assesses customer issues and routes to specialists",
                prompt="You are a triage agent. Assess customer issues and route to the appropriate specialist.",
                tools=["Read"],
                model="sonnet",
            ),
            handoffs=["technical-support", "billing-support", "account-manager"],
        ),
        "technical-support": SwarmAgent(
            name="technical-support",
            definition=AgentDefinition(
                description="Handles technical issues and troubleshooting",
                prompt="You are a technical support specialist. Solve technical problems and provide solutions.",
                tools=["Read", "Grep"],
                model="sonnet",
            ),
            handoffs=["engineering", "triage"],
        ),
        "billing-support": SwarmAgent(
            name="billing-support",
            definition=AgentDefinition(
                description="Handles billing, payments, and subscription issues",
                prompt="You are a billing specialist. Handle payment and subscription issues.",
                tools=["Read"],
                model="sonnet",
            ),
            handoffs=["account-manager", "triage"],
        ),
        "account-manager": SwarmAgent(
            name="account-manager",
            definition=AgentDefinition(
                description="Manages customer accounts and relationships",
                prompt="You are an account manager. Handle account-related requests and customer relationships.",
                tools=["Read"],
                model="sonnet",
            ),
            handoffs=["billing-support", "technical-support"],
        ),
        "engineering": SwarmAgent(
            name="engineering",
            definition=AgentDefinition(
                description="Handles complex technical issues requiring engineering expertise",
                prompt="You are an engineering specialist. Solve complex technical problems.",
                tools=["Read", "Grep", "Glob"],
                model="sonnet",
            ),
            handoffs=[],  # Terminal agent - no handoffs
        ),
    }

    swarm = Swarm(agents, initial_agent="triage")

    task = """A customer reports that their API requests are failing with 500 errors
    only when they try to process large files (>10MB). Small files work fine.
    They're on the enterprise plan and this is affecting their production system."""

    result = await swarm.execute(task)

    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    print(result)


async def demo_software_project():
    """Demonstrate swarm pattern with software project workflow."""
    print("\n" + "=" * 80)
    print("SWARM PATTERN DEMO: Software Project Team")
    print("=" * 80)

    # Define agents with their handoffs
    agents = {
        "project-manager": SwarmAgent(
            name="project-manager",
            definition=AgentDefinition(
                description="Coordinates project activities and delegates tasks to team members",
                prompt="You are a project manager. Coordinate tasks and delegate to appropriate team members.",
                tools=["Read", "Grep"],
                model="sonnet",
            ),
            handoffs=["developer", "designer", "qa-engineer"],
        ),
        "developer": SwarmAgent(
            name="developer",
            definition=AgentDefinition(
                description="Writes code and implements features",
                prompt="You are a software developer. Implement features and write code.",
                tools=["Read", "Write", "Edit", "Grep"],
                model="sonnet",
            ),
            handoffs=["qa-engineer", "architect", "project-manager"],
        ),
        "designer": SwarmAgent(
            name="designer",
            definition=AgentDefinition(
                description="Creates UI/UX designs and specifications",
                prompt="You are a UI/UX designer. Create designs and specifications.",
                tools=["Read", "Write"],
                model="sonnet",
            ),
            handoffs=["developer", "project-manager"],
        ),
        "qa-engineer": SwarmAgent(
            name="qa-engineer",
            definition=AgentDefinition(
                description="Tests code and ensures quality",
                prompt="You are a QA engineer. Test code and ensure quality.",
                tools=["Read", "Bash"],
                model="sonnet",
            ),
            handoffs=["developer", "project-manager"],
        ),
        "architect": SwarmAgent(
            name="architect",
            definition=AgentDefinition(
                description="Reviews architecture and provides technical guidance",
                prompt="You are a software architect. Review designs and provide technical guidance.",
                tools=["Read", "Grep", "Glob"],
                model="sonnet",
            ),
            handoffs=["developer", "project-manager"],
        ),
    }

    swarm = Swarm(agents, initial_agent="project-manager")

    task = """We need to implement a new feature: real-time notifications for users.
    This should work across web and mobile platforms. Please coordinate the implementation."""

    result = await swarm.execute(task)

    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    print(result)


async def main():
    """Run swarm pattern demonstrations."""
    # Uncomment the demo you want to run:

    await demo_customer_support()
    # await demo_software_project()


if __name__ == "__main__":
    anyio.run(main)
