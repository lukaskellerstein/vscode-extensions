# Claude Code Predefined Tools

This document lists all the built-in tools available in Claude Code.

## Core File Operations

- **Read** - Read files from the filesystem

  - Supports reading multiple files in parallel
  - Can read images, PDFs, and Jupyter notebooks
  - Supports line offset and limit for large files

- **Write** - Create or overwrite files

  - Overwrites existing files
  - Handles text content with proper encoding

- **Edit** - Make line-based edits to existing files

  - Performs exact string replacements
  - Supports replace_all for renaming across files
  - Returns git-style diff of changes

- **Glob** - Pattern matching to find files

  - Supports glob patterns like `**/*.js` or `src/**/*.ts`
  - Returns matching file paths sorted by modification time
  - Fast file pattern matching for any codebase size

- **Grep** - Search file contents with regex patterns
  - Built on ripgrep for performance
  - Supports context lines (-A, -B, -C)
  - Multiple output modes: content, files_with_matches, count
  - Filter by file type or glob patterns

## System & Command Execution

- **Bash** - Execute shell commands

  - Persistent shell session with optional timeout
  - Can be scoped (e.g., `Bash(git:*)` for only git commands)
  - Supports background execution with `run_in_background`
  - Common scoped commands:
    - `Bash(git:*)` - Git operations
    - `Bash(npm:*)` - NPM commands
    - `Bash(docker:*)` - Docker operations
    - `Bash(python:*)` - Python execution

- **BashOutput** - Retrieve output from background shells

  - Monitor long-running processes
  - Supports regex filtering of output

- **KillShell** - Terminate background bash shells

## Web Capabilities

- **WebSearch** - Search the web for current information

  - Provides up-to-date information beyond training cutoff
  - Supports domain filtering (allowed/blocked)
  - Only available in the US

- **WebFetch** - Fetch and analyze content from URLs
  - Converts HTML to markdown
  - Processes content with AI model
  - Includes 15-minute cache for performance
  - Handles redirects

## Task Management & Orchestration

- **Task** - Launch specialized sub-agents for complex tasks

  - Multiple agent types available:
    - `general-purpose` - Multi-step tasks and research
    - `Explore` - Fast codebase exploration
    - `Plan` - Planning and analysis
    - `statusline-setup` - Configure status line
    - `output-style-setup` - Create output styles
  - Can launch multiple agents in parallel
  - Agents run autonomously and return results

- **TodoWrite** - Manage task lists during execution

  - Track progress with states: pending, in_progress, completed
  - Break down complex tasks into steps
  - Provides visibility to user

- **Skill** - Execute custom user-defined skills

  - Skills are specialized workflows
  - Defined in project configuration

- **SlashCommand** - Execute user-defined slash commands
  - Custom commands defined in `.claude/commands/`
  - Examples: `/commit`, `/generate-changelog`, `/lss`

## Jupyter/Code Execution

- **NotebookEdit** - Edit Jupyter notebook cells

  - Replace, insert, or delete cells
  - Supports code and markdown cell types
  - 0-indexed cell numbering

- **mcp**ide**executeCode** - Execute Python code in Jupyter kernel

  - All code executes in current Jupyter kernel
  - State persists across calls
  - Returns execution results

- **mcp**ide**getDiagnostics** - Get language diagnostics from VS Code
  - Retrieve errors and warnings
  - Can filter by file URI

## Interactive Features

- **AskUserQuestion** - Ask clarifying questions during execution

  - Support for 1-4 questions at once
  - Multiple choice options (2-4 per question)
  - Multi-select support
  - Automatic "Other" option for custom input

- **ExitPlanMode** - Exit planning mode and proceed to implementation
  - Used when transitioning from planning to coding
  - Prompts user approval of plan

## MCP (Model Context Protocol) Integrations

Claude Code can be extended with MCP servers for additional capabilities:

### Built-in MCP Tools

- **mcp**filesystem**\*** - Enhanced filesystem operations

  - `read_text_file`, `read_media_file`, `read_multiple_files`
  - `write_file`, `edit_file`
  - `create_directory`, `list_directory`, `directory_tree`
  - `move_file`, `search_files`, `get_file_info`

- **mcp**tavily**\*** - Advanced web search and extraction
  - `tavily-search` - Comprehensive AI-powered web search
  - `tavily-extract` - Extract content from URLs
  - `tavily-crawl` - Structured web crawling
  - `tavily-map` - Website structure mapping

### Popular Community MCP Servers (50+ available)

**Development & Version Control**

- GitHub MCP - Repository and issue management
- GitLab MCP - GitLab API access
- Sentry MCP - Error tracking integration

**Productivity & Communication**

- Slack MCP - Team messaging
- Notion MCP - Document and task management
- Google Drive MCP - File access and search

**Web & Automation**

- Brave Search MCP - Web search API
- Puppeteer MCP - Browser automation
- Google Maps MCP - Location services

**Design & Content**

- Figma MCP - Design file access
- Canva MCP - Design creation

**Development Tools**

- Prisma MCP - Database schema management
- Socket MCP - Security analysis

## Tool Scoping & Permissions

Tools can be restricted using the `allowed_tools` and `disallowed_tools` options:

```python
# Specific tools only
allowed_tools=["Read", "Write", "Bash(git:*)"]

# Exclude dangerous operations
disallowed_tools=["Bash(rm:*)", "Bash(dd:*)"]
```

## Permission Modes

Control tool approval with `permission_mode`:

- `default` - CLI prompts for dangerous tools
- `acceptEdits` - Auto-accept file edits
- `bypassPermissions` - Allow all tools (use with caution)

## References

- Built-in tools are defined in the Claude Code system prompt
- MCP servers extend functionality beyond built-in tools
- Tool availability can be configured per agent or session
- Some tools require specific environment setup (e.g., Jupyter for code execution)
