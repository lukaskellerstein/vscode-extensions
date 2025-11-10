#!/usr/bin/env python3
"""Supervisor Pattern Implementation.

In this pattern, multiple agents work under the leadership of a supervisor agent.
Like humans in teams with their own manager, each agent reports only to the supervisor.
The supervisor decides whether to answer the user directly or delegate tasks to team members.

Key Characteristics:
- All agents are NOT "equal" - Hierarchical structure
- Supervisor agent controls the workflow
- Supervisor decides what information is passed to agents
- Supervisor decides what information is presented to the user

Usage:
    python supervisor_pattern.py
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


class SupervisorTeam:
    """Manages a team of agents under a supervisor."""

    def __init__(
        self,
        supervisor_name: str,
        supervisor_definition: AgentDefinition,
        team_agents: dict[str, AgentDefinition],
        options: ClaudeAgentOptions | None = None,
    ):
        """Initialize supervisor team.

        Args:
            supervisor_name: Name of the supervisor agent
            supervisor_definition: Definition of the supervisor agent
            team_agents: Dictionary of {agent_name: agent_definition} for team members
            options: Base options for the Claude client
        """
        self.supervisor_name = supervisor_name
        self.supervisor_definition = supervisor_definition
        self.team_agents = team_agents
        self.options = options or ClaudeAgentOptions()

        # Combine all agent definitions
        all_agents = {supervisor_name: supervisor_definition}
        all_agents.update(team_agents)
        self.options.agents = all_agents

    async def execute(self, initial_task: str) -> str:
        """Execute the supervisor pattern with the initial task.

        Args:
            initial_task: The initial task to process

        Returns:
            Final result from the supervisor
        """
        result = ""

        async with ClaudeSDKClient(options=self.options) as client:
            print(f"\n{'='*60}")
            print(f"Supervisor: {self.supervisor_name}")
            print(f"{'='*60}")

            # Build team member descriptions
            team_info = "\n".join([
                f"- {name}: {defn.description}"
                for name, defn in self.team_agents.items()
            ])

            # Initial supervisor prompt
            supervisor_prompt = f"""You are a supervisor managing a team of specialized agents.

Your responsibility:
{self.supervisor_definition.description}

Your team members:
{team_info}

Task to accomplish:
{initial_task}

As the supervisor, you should:
1. Analyze the task and decide if you can handle it directly or need to delegate
2. If delegating, clearly specify which team member should handle which part
3. Collect results from team members
4. Synthesize the final answer for the user

When you need to delegate work, use this format:
DELEGATE TO: [agent-name]
TASK: [specific task for that agent]

When you have the final answer, use this format:
FINAL ANSWER:
[your answer to the user]
"""

            await client.query(supervisor_prompt)

            # Process supervisor's decision-making
            max_iterations = 10
            iteration = 0

            while iteration < max_iterations:
                supervisor_response = []

                async for msg in client.receive_response():
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                print(f"Supervisor: {block.text}")
                                supervisor_response.append(block.text)
                    elif isinstance(msg, ResultMessage):
                        if msg.total_cost_usd and msg.total_cost_usd > 0:
                            print(f"\nCost: ${msg.total_cost_usd:.4f}")

                response_text = "\n".join(supervisor_response)

                # Check if supervisor wants to delegate
                if "DELEGATE TO:" in response_text:
                    # Parse delegation request
                    delegation = self._parse_delegation(response_text)

                    if delegation:
                        agent_name, agent_task = delegation
                        print(f"\n{'='*60}")
                        print(f"Team Member: {agent_name}")
                        print(f"{'='*60}")

                        # Execute task with team member
                        agent_result = await self._execute_agent_task(
                            client, agent_name, agent_task
                        )

                        # Return result to supervisor
                        feedback_prompt = f"""The team member '{agent_name}' has completed their task.

Result from {agent_name}:
{agent_result}

Please review this result and decide on next steps:
- Delegate to another team member if needed
- Or provide the FINAL ANSWER to the user
"""
                        await client.query(feedback_prompt)
                        iteration += 1
                    else:
                        # Could not parse delegation, treat as final answer
                        result = response_text
                        break
                elif "FINAL ANSWER:" in response_text:
                    # Supervisor has provided final answer
                    result = response_text.split("FINAL ANSWER:")[1].strip()
                    break
                else:
                    # No delegation marker, treat as final answer
                    result = response_text
                    break

        return result

    def _parse_delegation(self, text: str) -> tuple[str, str] | None:
        """Parse delegation request from supervisor's response.

        Args:
            text: Supervisor's response text

        Returns:
            Tuple of (agent_name, task) or None if parsing fails
        """
        try:
            lines = text.split("\n")
            agent_name = None
            task = None

            for i, line in enumerate(lines):
                if "DELEGATE TO:" in line:
                    agent_name = line.split("DELEGATE TO:")[1].strip()
                elif "TASK:" in line and agent_name:
                    # Collect all lines after TASK: until next section or end
                    task_lines = [line.split("TASK:")[1].strip()]
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith("DELEGATE"):
                            task_lines.append(lines[j].strip())
                        else:
                            break
                    task = " ".join(task_lines)
                    break

            if agent_name and task and agent_name in self.team_agents:
                return (agent_name, task)

            return None
        except Exception:
            return None

    async def _execute_agent_task(
        self, client: ClaudeSDKClient, agent_name: str, task: str
    ) -> str:
        """Execute a task with a specific team member.

        Args:
            client: The Claude SDK client
            agent_name: Name of the team member
            task: Task to execute

        Returns:
            Result from the team member
        """
        agent_definition = self.team_agents[agent_name]

        prompt = f"""You are {agent_name}, a specialized team member.

Your role: {agent_definition.description}

Your supervisor has assigned you this task:
{task}

Please complete this task and report your findings back to the supervisor.
"""

        await client.query(prompt)

        result_parts = []
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"{agent_name}: {block.text}")
                        result_parts.append(block.text)
            elif isinstance(msg, ResultMessage):
                if msg.total_cost_usd and msg.total_cost_usd > 0:
                    print(f"\nCost for {agent_name}: ${msg.total_cost_usd:.4f}")

        return "\n".join(result_parts)


async def demo_research_team():
    """Demonstrate supervisor pattern with a research team."""
    print("\n" + "="*80)
    print("SUPERVISOR PATTERN DEMO: Research Team")
    print("="*80)

    supervisor = AgentDefinition(
        description="Manages research projects and coordinates team members to deliver comprehensive results",
        prompt="You are a research supervisor. Analyze requests, delegate to specialists, "
               "and synthesize findings into coherent answers.",
        tools=["Read", "Grep", "Glob"],
        model="sonnet",
    )

    team = {
        "data-collector": AgentDefinition(
            description="Collects and organizes raw data and information",
            prompt="You are a data collector. Find and organize relevant information efficiently.",
            tools=["Read", "Grep", "Glob"],
            model="sonnet",
        ),
        "analyst": AgentDefinition(
            description="Analyzes data and identifies patterns and insights",
            prompt="You are a data analyst. Analyze information, identify patterns, and draw insights.",
            tools=["Read"],
            model="sonnet",
        ),
        "report-writer": AgentDefinition(
            description="Creates clear, professional reports from analysis",
            prompt="You are a report writer. Transform analysis into clear, professional reports.",
            tools=["Read", "Write"],
            model="sonnet",
        ),
    }

    supervisor_team = SupervisorTeam("research-supervisor", supervisor, team)

    task = """Analyze the structure of the claude_agent_sdk Python package.
    I need to understand:
    1. What are the main modules?
    2. What are the key classes and their purposes?
    3. A summary of the architecture
    """

    result = await supervisor_team.execute(task)

    print("\n" + "="*80)
    print("FINAL RESULT:")
    print("="*80)
    print(result)


async def demo_development_team():
    """Demonstrate supervisor pattern with a development team."""
    print("\n" + "="*80)
    print("SUPERVISOR PATTERN DEMO: Development Team")
    print("="*80)

    supervisor = AgentDefinition(
        description="Technical lead managing development projects and coordinating specialists",
        prompt="You are a technical lead. Break down requirements, delegate to team members, "
               "and ensure quality delivery.",
        tools=["Read", "Grep", "Glob"],
        model="sonnet",
    )

    team = {
        "backend-dev": AgentDefinition(
            description="Develops backend services and APIs",
            prompt="You are a backend developer specializing in APIs and services.",
            tools=["Read", "Write", "Edit"],
            model="sonnet",
        ),
        "frontend-dev": AgentDefinition(
            description="Develops user interfaces and client applications",
            prompt="You are a frontend developer specializing in user interfaces.",
            tools=["Read", "Write", "Edit"],
            model="sonnet",
        ),
        "qa-engineer": AgentDefinition(
            description="Tests code and ensures quality",
            prompt="You are a QA engineer. Test code thoroughly and identify issues.",
            tools=["Read", "Bash"],
            model="sonnet",
        ),
    }

    supervisor_team = SupervisorTeam("tech-lead", supervisor, team)

    task = """We need to add input validation to our API endpoints.
    Please ensure proper validation is implemented and tested."""

    result = await supervisor_team.execute(task)

    print("\n" + "="*80)
    print("FINAL RESULT:")
    print("="*80)
    print(result)


async def main():
    """Run supervisor pattern demonstrations."""
    # Uncomment the demo you want to run:

    await demo_research_team()
    # await demo_development_team()


if __name__ == "__main__":
    anyio.run(main)
