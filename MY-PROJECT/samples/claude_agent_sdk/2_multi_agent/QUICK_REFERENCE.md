# Multi-Agent Patterns Quick Reference

## Pattern Selection Guide

```
┌─────────────────────────────────────────────────┐
│ Is the workflow sequential?                    │
│ ├─ YES → Use COLLABORATION PATTERN              │
│ └─ NO → Continue...                             │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ Do you need central coordination?              │
│ ├─ YES → Use SUPERVISOR PATTERN                 │
│ └─ NO → Continue...                             │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ Do agents need to choose routing dynamically?  │
│ ├─ YES → Use SWARM PATTERN                      │
│ └─ NO → Reconsider your requirements            │
└─────────────────────────────────────────────────┘
```

## Pattern Comparison Table

| Feature          | Collaboration | Supervisor | Swarm     |
|------------------|--------------|------------|-----------|
| **Structure**    | Sequential   | Hierarchical | Network |
| **Equality**     | Equal agents | Supervisor leads | Equal agents |
| **Order**        | Fixed        | Dynamic    | Dynamic   |
| **Complexity**   | Low ⭐       | Medium ⭐⭐ | High ⭐⭐⭐ |
| **Flexibility**  | Low          | Medium     | High      |
| **Control**      | Predefined   | Supervisor decides | Agent decides |

## Code Templates

### Collaboration Pattern

```python
from claude_agent_sdk import AgentDefinition
from collaboration_pattern import CollaborationGroup

agents = [
    ("agent1", AgentDefinition(
        description="What agent1 does",
        prompt="Instructions for agent1",
        tools=["Read", "Grep"],
        model="sonnet",
    )),
    ("agent2", AgentDefinition(
        description="What agent2 does",
        prompt="Instructions for agent2",
        tools=["Write"],
        model="sonnet",
    )),
]

group = CollaborationGroup(agents)
result = await group.execute("Your task here")
```

### Supervisor Pattern

```python
from claude_agent_sdk import AgentDefinition
from supervisor_pattern import SupervisorTeam

supervisor = AgentDefinition(
    description="Coordinates team",
    prompt="You are a supervisor. Delegate and synthesize.",
    tools=["Read", "Grep"],
    model="sonnet",
)

team = {
    "specialist1": AgentDefinition(
        description="Specialist 1 role",
        prompt="Specialist 1 instructions",
        tools=["Read"],
        model="sonnet",
    ),
    "specialist2": AgentDefinition(
        description="Specialist 2 role",
        prompt="Specialist 2 instructions",
        tools=["Write"],
        model="sonnet",
    ),
}

team = SupervisorTeam("supervisor", supervisor, team)
result = await team.execute("Your task here")
```

### Swarm Pattern

```python
from claude_agent_sdk import AgentDefinition
from swarm_pattern import Swarm, SwarmAgent

agents = {
    "agent1": SwarmAgent(
        name="agent1",
        definition=AgentDefinition(
            description="Agent 1 role",
            prompt="Agent 1 instructions",
            tools=["Read"],
            model="sonnet",
        ),
        handoffs=["agent2", "agent3"],
    ),
    "agent2": SwarmAgent(
        name="agent2",
        definition=AgentDefinition(
            description="Agent 2 role",
            prompt="Agent 2 instructions",
            tools=["Write"],
            model="sonnet",
        ),
        handoffs=["agent3"],
    ),
    "agent3": SwarmAgent(
        name="agent3",
        definition=AgentDefinition(
            description="Agent 3 role (terminal)",
            prompt="Agent 3 instructions",
            tools=["Read"],
            model="sonnet",
        ),
        handoffs=[],  # Terminal agent
    ),
}

swarm = Swarm(agents, initial_agent="agent1")
result = await swarm.execute("Your task here", max_handoffs=10)
```

## Control Flow Markers

### Supervisor Pattern

```python
# In supervisor's prompt, teach it to use:
"""
To delegate:
DELEGATE TO: agent-name
TASK: description of task

To finish:
FINAL ANSWER:
your answer to the user
"""
```

### Swarm Pattern

```python
# In agent's prompt, teach it to use:
"""
To hand off:
HANDOFF TO: agent-name
TASK: description of task
CONTEXT: relevant context

To finish:
FINAL ANSWER:
your answer to the user
"""
```

## Common Configurations

### Research Team (Supervisor)

```python
supervisor = AgentDefinition(
    description="Research coordinator",
    prompt="Coordinate research and synthesis findings",
    tools=["Read", "Grep"],
)

team = {
    "researcher": AgentDefinition(
        description="Finds and collects information",
        prompt="Research and collect data",
        tools=["Read", "Grep", "Glob"],
    ),
    "analyst": AgentDefinition(
        description="Analyzes data",
        prompt="Analyze and identify patterns",
        tools=["Read"],
    ),
    "writer": AgentDefinition(
        description="Writes reports",
        prompt="Create clear reports",
        tools=["Read", "Write"],
    ),
}
```

### Customer Support (Swarm)

```python
agents = {
    "triage": SwarmAgent(
        name="triage",
        definition=AgentDefinition(
            description="Initial contact, routes issues",
            prompt="Categorize and route requests",
            tools=["Read"],
        ),
        handoffs=["technical", "billing", "general"],
    ),
    "technical": SwarmAgent(
        name="technical",
        definition=AgentDefinition(
            description="Technical support",
            prompt="Solve technical issues",
            tools=["Read", "Grep"],
        ),
        handoffs=["specialist"],
    ),
    "specialist": SwarmAgent(
        name="specialist",
        definition=AgentDefinition(
            description="Complex issue resolution",
            prompt="Solve complex problems",
            tools=["Read", "Grep", "Glob"],
        ),
        handoffs=[],  # Terminal
    ),
}
```

### Software Pipeline (Collaboration)

```python
agents = [
    ("requirements", AgentDefinition(
        description="Analyzes requirements",
        prompt="Create technical specifications",
        tools=["Read"],
    )),
    ("design", AgentDefinition(
        description="Designs architecture",
        prompt="Design system architecture",
        tools=["Read"],
    )),
    ("implementation", AgentDefinition(
        description="Implements solution",
        prompt="Write clean code",
        tools=["Read", "Write", "Edit"],
    )),
    ("testing", AgentDefinition(
        description="Tests implementation",
        prompt="Test thoroughly",
        tools=["Read", "Bash"],
    )),
]
```

## Best Practices Checklist

### Agent Design
- [ ] Each agent has a single, clear responsibility
- [ ] Agent descriptions are specific and actionable
- [ ] Prompts include clear instructions
- [ ] Appropriate tools are assigned
- [ ] Model selection is justified

### Pattern Selection
- [ ] Pattern matches workflow structure
- [ ] Complexity level is appropriate
- [ ] Control flow is well-defined
- [ ] Terminal conditions are clear

### Error Handling
- [ ] Maximum iterations/handoffs are set
- [ ] Invalid handoffs/delegations are caught
- [ ] Parse failures are handled gracefully
- [ ] Cost tracking is enabled

### Testing
- [ ] Structure tests pass
- [ ] Parsing logic is tested
- [ ] Demo scenarios work
- [ ] Edge cases are handled

## Troubleshooting

### Agent Not Responding
```python
# Check:
1. Agent definition is complete
2. Tools are allowed in options
3. Model is specified
4. Prompt is clear
```

### Invalid Handoff/Delegation
```python
# Check:
1. Target agent name is correct
2. Target is in handoff/team list
3. Control markers are formatted correctly
4. Parsing logic is working
```

### Infinite Loop
```python
# Solutions:
1. Set max_handoffs/max_iterations
2. Add terminal agents (empty handoffs)
3. Review agent decision logic
4. Check for circular handoffs
```

### High Costs
```python
# Optimizations:
1. Use simpler models where possible
2. Reduce number of agents
3. Optimize prompts (shorter)
4. Set lower max_turns
5. Add early termination conditions
```

## Command Cheat Sheet

```bash
# Run tests
uv run python test_patterns.py

# Run specific pattern demo
uv run python collaboration_pattern.py
uv run python supervisor_pattern.py
uv run python swarm_pattern.py

# Run all demos
uv run python demo_all_patterns.py

# Run specific demo scenario
uv run python demo_all_patterns.py --pattern collaboration

# View pattern comparison
uv run python demo_all_patterns.py --pattern comparison
```

## File Structure

```
MY/multi_agents/
├── __init__.py                    # Package exports
├── collaboration_pattern.py       # Collaboration implementation
├── supervisor_pattern.py          # Supervisor implementation
├── swarm_pattern.py              # Swarm implementation
├── demo_all_patterns.py          # Unified demos
├── test_patterns.py              # Structure tests
├── GOAL.md                       # Original requirements
├── README.md                     # Full documentation
├── IMPLEMENTATION_SUMMARY.md     # Implementation details
└── QUICK_REFERENCE.md           # This file
```

## Import Guide

```python
# Import patterns
from collaboration_pattern import CollaborationGroup
from supervisor_pattern import SupervisorTeam
from swarm_pattern import Swarm, SwarmAgent

# Import SDK types
from claude_agent_sdk import (
    AgentDefinition,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Import errors | Run with `uv run python` |
| Agent not working | Check tools allowed |
| Wrong handoff | Verify handoff list |
| Loop detected | Set max iterations |
| High latency | Use haiku model |
| Parse failure | Check marker format |

## Model Selection Guide

```python
model="haiku"   # Fast, low cost, simple tasks
model="sonnet"  # Balanced, most use cases (default)
model="opus"    # Complex reasoning, high accuracy
```

## Tool Selection Guide

```python
# File Operations
tools=["Read", "Write", "Edit"]

# Code Analysis
tools=["Read", "Grep", "Glob"]

# Execution
tools=["Bash"]

# Common Combinations
tools=["Read", "Grep"]        # Research
tools=["Read", "Write"]       # Documentation
tools=["Read", "Edit", "Bash"] # Development
```

---

For detailed information, see:
- **README.md** - Full documentation
- **IMPLEMENTATION_SUMMARY.md** - Architecture details
- **Pattern files** - Implementation code
