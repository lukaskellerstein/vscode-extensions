# Module 6: Workspace Management

**Duration**: Week 6 | **Difficulty**: Advanced

Manage workspaces, implement virtual file systems, create tasks, and integrate with source control.

## 📖 Learning Objectives

- Handle multi-root workspaces
- Implement file system providers
- Create task providers
- Integrate with source control
- Implement timeline providers
- Work with workspace trust

## 📚 Lessons

### [6.1 Workspace and Folders](./6.1-workspace-folders.md)
- Workspace vs folder
- Multi-root workspaces
- Workspace folder operations
- Workspace events
- Workspace trust API
- .code-workspace files
- Workspace state

### [6.2 File System Provider](./6.2-filesystem-provider.md)
- FileSystemProvider interface
- Implementing virtual file systems
- File operations (CRUD)
- File watching
- Directory reading
- Copy, move, delete operations
- Error handling

### [6.3 Tasks and Task Providers](./6.3-tasks.md)
- Task contribution
- Custom task providers
- Task definitions
- Problem matchers
- Task execution
- Task detection
- Build system integration

### [6.4 Source Control Management](./6.4-source-control.md)
- SCM provider implementation
- Resource states and groups
- Quick diff provider
- Timeline provider
- Commit and push operations
- Repository management
- Integration with Git

## 💻 Examples

1. **multi-root-workspace** - Workspace operations
2. **memory-filesystem** - In-memory file system
3. **task-provider** - Custom tasks
4. **problem-matcher** - Error parsing
5. **scm-provider** - Simple SCM integration
6. **timeline-provider** - File history

## ✏️ Exercises

1. **Workspace Manager** - Manage multi-root workspaces
2. **Virtual FS** - Implement virtual file system
3. **Build System** - Custom task provider
4. **Version Control** - Basic SCM provider
5. **History Tracker** - Timeline provider

## 🎯 Mini Project: Project Manager

**Features**:
- Workspace templates
- Task automation
- File system operations
- Source control integration
- Project history

**Time**: 6-8 hours

## ⏭️ Next Steps

[Module 7: Debugging](../module-07-debugging/README.md)
