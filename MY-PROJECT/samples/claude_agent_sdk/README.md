# Claude Agent SDK - Comprehensive Examples

A comprehensive demonstration project showcasing all patterns and capabilities of the Claude Agent SDK for Python.

## Overview

This project provides complete, runnable examples demonstrating:
- **Single Agent Patterns** (7 examples)
- **Multi-Agent Systems** (3 examples)
- **Workflow Patterns** (4 examples)

## Project Structure

```
claude_agent_sdk/
├── single_agent/          # Single agent examples
│   ├── a_simplest_agent.py
│   ├── b_agent_with_options.py
│   ├── c_agent_with_predefined_tools.py
│   ├── d_agent_with_custom_tools.py
│   ├── e_agent_with_memory.py
│   ├── f_agent_with_hooks.py
│   └── g_agent_with_subagents.py
├── multi_agent/           # Multi-agent examples
│   ├── a_collaboration.py
│   ├── b_supervision.py
│   └── c_swarm.py
├── workflows/             # Workflow examples
│   ├── a_sequential_workflow.py
│   ├── b_parallel_workflow.py
│   ├── c_conditional_workflow.py
│   └── d_loop_workflow.py
├── pyproject.toml
├── GOAL.md
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

## Single Agent Examples

### a) Simplest Agent
The most basic usage - a simple query to Claude.

```bash
python single_agent/a_simplest_agent.py
```

**Demonstrates:**
- Basic `query()` function
- Message handling
- Simple request-response pattern

### b) Agent with Options
Configuring agents with `ClaudeAgentOptions`.

```bash
python single_agent/b_agent_with_options.py
```

**Demonstrates:**
- Custom system prompts
- Model selection
- Permission modes
- Max turns configuration
- Combined option usage

### c) Agent with Predefined Tools
Using built-in Claude Code tools.

```bash
python single_agent/c_agent_with_predefined_tools.py
```

**Demonstrates:**
- Read/Write tools for file operations
- Bash tool for command execution
- Glob/Grep tools for searching
- Multiple tools working together

### d) Agent with Custom Tools
Creating custom tools using MCP servers.

```bash
python single_agent/d_agent_with_custom_tools.py
```

**Demonstrates:**
- `@tool` decorator for defining custom tools
- `create_sdk_mcp_server()` for MCP server creation
- Calculator tools (add, multiply, power)
- String manipulation tools (reverse, uppercase, word_count)
- Multiple MCP servers

### e) Agent with Memory
Multi-turn conversations with context retention.

```bash
python single_agent/e_agent_with_memory.py
```

**Demonstrates:**
- `ClaudeSDKClient` for stateful conversations
- Conversation memory across queries
- Session continuation with `resume`
- Multi-turn interactions

### f) Agent with Hooks
Intercepting and modifying agent behavior.

```bash
python single_agent/f_agent_with_hooks.py
```

**Demonstrates:**
- PreToolUse hooks for validation
- PostToolUse hooks for logging
- UserPromptSubmit hooks for context injection
- Permission decisions (allow/deny)
- Multiple hooks working together

### g) Agent with Subagents
Specialized agents with custom roles.

```bash
python single_agent/g_agent_with_subagents.py
```

**Demonstrates:**
- `AgentDefinition` for custom agents
- Code reviewer agent
- Documentation writer agent
- Test writer agent
- Multiple specialized agents
- Hierarchical agent setups

## Multi-Agent Examples

### a) Collaboration
Agents working together on shared tasks.

```bash
python multi_agent/a_collaboration.py
```

**Demonstrates:**
- Research and writing collaboration
- Analysis and optimization collaboration
- Plan-implement-test collaboration
- Agents building on each other's work

### b) Supervision
Supervisor coordinating worker agents.

```bash
python multi_agent/b_supervision.py
```

**Demonstrates:**
- Supervisor with specialist workers
- Task delegation
- Result synthesis
- Hierarchical supervision (multiple levels)

### c) Swarm
Multiple agents working in parallel.

```bash
python multi_agent/c_swarm.py
```

**Demonstrates:**
- Parallel code analysis from different perspectives
- Distributed file processing
- Multi-perspective reviews
- Search and aggregate patterns

## Workflow Examples

### a) Sequential Workflow
Tasks executing in sequence.

```bash
python workflows/a_sequential_workflow.py
```

**Demonstrates:**
- Step-by-step execution
- Data pipeline (collect → process → analyze)
- Document generation (outline → write → edit)
- Each step depends on previous results

### b) Parallel Workflow
Independent tasks running simultaneously.

```bash
python workflows/b_parallel_workflow.py
```

**Demonstrates:**
- Parallel task execution with `anyio.create_task_group()`
- Parallel file analysis
- Multiple specialized agents running concurrently
- Map-reduce pattern

### c) Conditional Workflow
Branching based on conditions.

```bash
python workflows/c_conditional_workflow.py
```

**Demonstrates:**
- If-else branching
- Multi-branch routing
- Error handling paths
- Dynamic routing based on content
- Classifier-based routing

### d) Loop Workflow
Iterative and repetitive tasks.

```bash
python workflows/d_loop_workflow.py
```

**Demonstrates:**
- Fixed iteration loops
- Conditional loops (while)
- Iterative refinement
- Batch processing
- Retry logic

## Key Concepts

### 1. Query vs ClaudeSDKClient

**`query()`** - For simple, stateless requests:
```python
async for message in query(prompt="Hello"):
    # Process messages
```

**`ClaudeSDKClient`** - For stateful, multi-turn conversations:
```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("First question")
    async for message in client.receive_response():
        # Process response

    await client.query("Follow-up question")
    async for message in client.receive_response():
        # Process response with context
```

### 2. ClaudeAgentOptions

Configure agent behavior:
```python
options = ClaudeAgentOptions(
    system_prompt="You are a helpful assistant",
    model="claude-sonnet-4-5-20250929",
    max_turns=5,
    permission_mode="acceptEdits",
    allowed_tools=["Read", "Write", "Bash"],
    mcp_servers={"calc": calculator_server},
    agents={"specialist": agent_definition},
    hooks={"PreToolUse": [hook_matcher]},
)
```

### 3. Custom Tools (MCP)

Define custom tools:
```python
@tool("add", "Add two numbers", {"a": float, "b": float})
async def add_numbers(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"Result: {result}"}]
    }

server = create_sdk_mcp_server(
    name="calculator",
    version="1.0.0",
    tools=[add_numbers],
)
```

### 4. Hooks

Intercept agent behavior:
```python
async def my_hook(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext,
) -> HookJSONOutput:
    # Hook logic
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [HookMatcher(matcher="Bash", hooks=[my_hook])],
    },
)
```

### 5. Subagents

Define specialized agents:
```python
options = ClaudeAgentOptions(
    agents={
        "code-reviewer": AgentDefinition(
            description="Reviews code",
            prompt="You are a code reviewer...",
            tools=["Read", "Grep"],
            model="sonnet",
        ),
    },
)
```

## Message Types

The SDK provides several message types:

- **`UserMessage`**: User input
- **`AssistantMessage`**: Claude's response (contains `TextBlock`, `ToolUseBlock`, etc.)
- **`SystemMessage`**: System notifications
- **`ResultMessage`**: Final result with cost and usage info

## Best Practices

### 1. Error Handling
```python
try:
    async for message in query(prompt="..."):
        if isinstance(message, ResultMessage):
            if message.is_error:
                print(f"Error: {message.result}")
except Exception as e:
    print(f"Exception: {e}")
```

### 2. Resource Management
```python
async with ClaudeSDKClient(options=options) as client:
    # Client automatically connects and disconnects
    await client.query("...")
```

### 3. Cost Tracking
```python
async for message in query(prompt="..."):
    if isinstance(message, ResultMessage):
        if message.total_cost_usd:
            print(f"Cost: ${message.total_cost_usd:.4f}")
        print(f"Turns: {message.num_turns}")
        print(f"Duration: {message.duration_ms}ms")
```

### 4. Parallel Execution
```python
async with anyio.create_task_group() as tg:
    tg.start_soon(task1)
    tg.start_soon(task2)
    tg.start_soon(task3)
```

## Common Patterns

### Pattern 1: Research → Analyze → Report
```python
async with ClaudeSDKClient(options) as client:
    # Research
    await client.query("Use researcher agent to gather data")
    # ... collect results

    # Analyze
    await client.query("Use analyzer agent to process the data")
    # ... collect analysis

    # Report
    await client.query("Create final report from analysis")
```

### Pattern 2: Validate → Process → Store
```python
# Validate
result = await validate_input(data)
if result.is_valid:
    # Process
    processed = await process_data(data)
    # Store
    await store_result(processed)
else:
    await handle_error(result.error)
```

### Pattern 3: Parallel Processing → Aggregate
```python
results = {}
async with anyio.create_task_group() as tg:
    for item in items:
        tg.start_soon(process_item, item, results)

# Aggregate results
final = await aggregate(results)
```

## Troubleshooting

### Issue: "Not connected" error
**Solution**: Use `async with ClaudeSDKClient()` or call `await client.connect()`

### Issue: Tools not working
**Solution**: Add tools to `allowed_tools` list in options

### Issue: High costs
**Solution**: Set `max_turns` in options to limit conversation length

### Issue: Permission denied
**Solution**: Set `permission_mode="bypassPermissions"` (use with caution)

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Claude Agent SDK GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [MCP Documentation](https://modelcontextprotocol.io/)

## License

This project is for demonstration purposes.

## Contributing

Feel free to submit issues or pull requests with additional examples or improvements.
