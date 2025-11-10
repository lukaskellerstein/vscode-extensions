# Multi-Agent Patterns

This directory contains implementations of three multi-agent coordination patterns using the Claude Agent SDK for Python.

## Overview

Multi-agent systems allow multiple AI agents to work together to solve complex problems. Each pattern offers different coordination strategies suitable for different use cases.

## Patterns

### 1. Collaboration Pattern

**File:** `collaboration_pattern.py`

**Description:** Multiple agents work in a defined sequential order. Each agent processes the task and passes their results to the next agent in the sequence.

**Characteristics:**
- All agents are "equal" (no hierarchy)
- Order of agents is predefined
- Each agent can pass work to the next agent in sequence
- Linear workflow

**Use Cases:**
- Software development workflows (requirements → design → implementation)
- Content creation pipelines (research → writing → editing)
- Manufacturing assembly lines
- Sequential approval processes

**Example:**
```python
agents = [
    ("researcher", researcher_definition),
    ("writer", writer_definition),
    ("editor", editor_definition),
]

group = CollaborationGroup(agents)
result = await group.execute("Create a blog post about AI")
```

### 2. Supervisor Pattern

**File:** `supervisor_pattern.py`

**Description:** Multiple agents work under the leadership of a supervisor agent. The supervisor analyzes tasks, delegates to team members, and synthesizes final results.

**Characteristics:**
- Hierarchical structure (NOT equal agents)
- Supervisor agent controls the workflow
- Supervisor decides what information is passed to agents
- Supervisor decides what information is presented to the user
- Team members report only to the supervisor

**Use Cases:**
- Research teams (supervisor coordinates specialists)
- Development teams (tech lead managing developers)
- Customer service escalation (manager overseeing support staff)
- Project management scenarios

**Example:**
```python
supervisor = AgentDefinition(
    description="Manages research projects and coordinates team members",
    prompt="You are a research supervisor...",
    tools=["Read", "Grep"],
)

team = {
    "data-collector": collector_definition,
    "analyst": analyst_definition,
    "report-writer": writer_definition,
}

team = SupervisorTeam("supervisor", supervisor, team)
result = await team.execute("Analyze the market trends")
```

### 3. Swarm Pattern

**File:** `swarm_pattern.py`

**Description:** Each agent has defined "handoffs" specifying which agents they can pass work to. Agents autonomously decide which handoff to use based on the task requirements.

**Characteristics:**
- All agents are "equal" (no hierarchy)
- No specific predetermined order (unlike collaboration)
- Only the first agent is defined
- Each agent has a handoff list of possible next agents
- Dynamic, adaptive workflow based on agent decisions

**Use Cases:**
- Customer support systems (routing based on issue type)
- Dynamic task routing
- Adaptive problem-solving
- Complex workflows with multiple paths

**Example:**
```python
agents = {
    "triage": SwarmAgent(
        name="triage",
        definition=triage_definition,
        handoffs=["technical-support", "billing-support"],
    ),
    "technical-support": SwarmAgent(
        name="technical-support",
        definition=tech_definition,
        handoffs=["engineering", "triage"],
    ),
}

swarm = Swarm(agents, initial_agent="triage")
result = await swarm.execute("Customer has API errors")
```

## Pattern Comparison

| Feature | Collaboration | Supervisor | Swarm |
|---------|--------------|------------|-------|
| Structure | Sequential | Hierarchical | Dynamic Network |
| Agent Equality | Equal | Supervisor leads | Equal |
| Order | Predefined | Supervisor decides | Agent decides |
| Flexibility | Low | Medium | High |
| Complexity | Low | Medium | High |
| Best For | Linear workflows | Managed teams | Adaptive routing |

## Installation

Ensure you have the Claude Agent SDK installed:

```bash
pip install claude-agent-sdk
```

## Running the Examples

Each pattern file contains multiple demonstration scenarios:

```bash
# Collaboration pattern demos
python collaboration_pattern.py

# Supervisor pattern demos
python supervisor_pattern.py

# Swarm pattern demos
python swarm_pattern.py

# Run all demos
python demo_all_patterns.py
```

## Architecture

All patterns are built on top of the Claude Agent SDK's core components:

- **ClaudeSDKClient**: Bidirectional communication with Claude
- **AgentDefinition**: Defines agent capabilities and behavior
- **ClaudeAgentOptions**: Configures tools, models, and settings

### Key Design Principles

1. **Modularity**: Each pattern is self-contained and reusable
2. **Extensibility**: Easy to add new agents or modify existing ones
3. **Type Safety**: Leverages Python type hints for better IDE support
4. **Clean Code**: Follows SOLID principles and maintains simplicity
5. **Async First**: Uses anyio for async/await patterns

## Implementation Details

### Agent Communication

Agents communicate through the ClaudeSDKClient by:
1. Sending prompts with context
2. Receiving structured responses
3. Parsing responses for control flow (handoffs, delegations, final answers)

### Control Flow Markers

Each pattern uses specific markers for control flow:

**Collaboration:**
- Sequential processing (no markers needed)
- Each agent processes and passes to next

**Supervisor:**
- `DELEGATE TO: [agent-name]` - Delegate to team member
- `TASK: [description]` - Specify the task
- `FINAL ANSWER:` - Provide final result

**Swarm:**
- `HANDOFF TO: [agent-name]` - Hand off to another agent
- `TASK: [description]` - Specify the task
- `CONTEXT: [context]` - Provide context
- `FINAL ANSWER:` - Provide final result

### Error Handling

All patterns include:
- Maximum iteration limits to prevent infinite loops
- Validation of agent names in handoffs/delegations
- Graceful handling of parsing failures
- Cost tracking for API usage

## Customization

### Adding New Agents

Create an `AgentDefinition` with:
- `description`: What the agent does
- `prompt`: Instructions for the agent
- `tools`: List of tools the agent can use
- `model`: Model to use (sonnet, opus, haiku)

```python
custom_agent = AgentDefinition(
    description="Specializes in data analysis",
    prompt="You are a data analyst...",
    tools=["Read", "Grep", "Bash"],
    model="sonnet",
)
```

### Modifying Workflows

Each pattern class can be extended or modified:

```python
class CustomCollaboration(CollaborationGroup):
    async def execute(self, task):
        # Add custom logic
        result = await super().execute(task)
        # Post-process result
        return result
```

## Best Practices

1. **Choose the Right Pattern**
   - Use Collaboration for linear, sequential workflows
   - Use Supervisor for complex projects needing coordination
   - Use Swarm for dynamic, adaptive scenarios

2. **Define Clear Roles**
   - Give each agent a specific, well-defined responsibility
   - Avoid overlapping agent capabilities

3. **Manage Context**
   - Pass relevant context between agents
   - Don't overload agents with unnecessary information

4. **Set Limits**
   - Use max_iterations or max_handoffs to prevent infinite loops
   - Monitor costs and usage

5. **Test Incrementally**
   - Start with simple scenarios
   - Gradually increase complexity
   - Monitor agent decisions and adjust prompts

## Troubleshooting

### Agents Not Handing Off

- Check handoff list includes target agent
- Verify control flow markers are correct
- Ensure prompts clearly explain handoff format

### Infinite Loops

- Set appropriate max_handoffs/max_iterations
- Add terminal agents (with empty handoff lists)
- Review agent decision-making logic

### Poor Quality Results

- Refine agent prompts with more specific instructions
- Adjust which tools are available to each agent
- Consider using different models for different agents

## Future Enhancements

Potential improvements to these patterns:

1. **Persistence**: Save and resume multi-agent sessions
2. **Monitoring**: Add logging and visualization of agent interactions
3. **Parallel Execution**: Allow multiple agents to work simultaneously
4. **Learning**: Agents learn from previous interactions
5. **Human-in-the-Loop**: Interactive approval at key decision points

## References

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [LangGraph Multi-Agent Patterns](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)

## Contributing

To improve these patterns:
1. Follow SOLID principles
2. Maintain clean, readable code
3. Add comprehensive docstrings
4. Include usage examples
5. Test thoroughly

## License

MIT License - Same as the Claude Agent SDK
