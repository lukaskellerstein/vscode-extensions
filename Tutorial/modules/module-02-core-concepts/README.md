# Module 2: Core Concepts

**Duration**: Week 2 | **Difficulty**: Beginner

Master the fundamental building blocks of VS Code extensions.

## 📖 Learning Objectives

- Register and manage commands effectively
- Work with VS Code configuration system
- Add items to menus and context menus
- Display notifications and progress indicators
- Create status bar items
- Handle user input with input boxes and quick picks

## 📚 Lessons

### [2.1 Commands and Command Palette](./2.1-commands.md)
- Registering commands
- Command parameters and return values
- Built-in VS Code commands
- Command URIs and links
- Keyboard shortcuts (keybindings)
- Command context and enablement

### [2.2 Configuration and Settings](./2.2-configuration.md)
- Contributing configuration schemas
- Reading configuration values
- Updating configuration programmatically
- Workspace vs user vs folder settings
- Configuration scopes
- Reacting to configuration changes
- Configuration validation

### [2.3 Menus and Context Menus](./2.3-menus.md)
- Menu contribution points
- Editor context menus
- Explorer context menus
- Title bar menus
- View menus
- Menu groups and ordering
- Dynamic menus with "when" clauses
- Icons in menus

### [2.4 Status Bar and Information Messages](./2.4-ui-elements.md)
- Creating status bar items
- Status bar alignment and priority
- Showing notifications (info, warning, error)
- Progress indicators
- Input boxes and validation
- Quick picks and multi-select
- Multi-step input flows
- Modal vs non-modal dialogs

## 💻 Examples

Browse working examples in the `examples/` folder:

1. **command-registration** - Various command types
2. **configuration-demo** - Reading and updating settings
3. **menu-integration** - All menu types
4. **notification-samples** - Different notification patterns
5. **status-bar-examples** - Status bar use cases
6. **input-validation** - Input box with validation
7. **quick-pick-demo** - Single and multi-select quick picks
8. **multi-step-input** - Wizard-style input collection

## ✏️ Exercises

1. **Command Manager** - Create commands with undo/redo
2. **Settings UI** - Build a custom settings interface
3. **Context Menu Suite** - Add context menus for different file types
4. **Progress Dashboard** - Show progress for long operations
5. **Smart Input** - Create intelligent input validation

See detailed instructions in `exercises/README.md`.

## 🎯 Mini Project: Task Runner Extension

**Objective**: Build an extension that runs custom tasks with configuration.

**Features**:
- Commands to add, run, and manage tasks
- Configuration for task definitions
- Status bar showing active task
- Progress notifications for running tasks
- Context menus for file-specific tasks
- Quick pick for task selection

**Time**: 2-3 hours

## 📝 Key Takeaways

- Commands are the foundation of extension functionality
- Configuration makes extensions flexible and customizable
- Menus provide contextual access to commands
- Good UX requires appropriate notifications and progress indicators
- Status bar provides always-visible information
- Input validation prevents errors

## ⏭️ Next Steps

Proceed to [Module 3: User Interface Extensions](../module-03-ui-extensions/README.md).
