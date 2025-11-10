# Module 1 Exercises

## Exercise 1: Custom Greeting Command

**Difficulty**: Easy
**Time**: 15 minutes

### Objective
Create an extension that provides a personalized greeting based on the time of day.

### Requirements
1. Create a command "Good Morning/Afternoon/Evening"
2. The command should detect the current time
3. Display appropriate greeting:
   - "Good Morning!" (5 AM - 11:59 AM)
   - "Good Afternoon!" (12 PM - 5:59 PM)
   - "Good Evening!" (6 PM - 4:59 AM)
4. Add the user's name if configured in settings

### Steps
1. Generate a new extension using `yo code`
2. Implement the time-based logic
3. Add configuration for user name
4. Test with different times (mock the time if needed)

### Bonus
- Add an icon to the command
- Show greeting in status bar instead of notification

---

## Exercise 2: Multiple Commands with Different Activation

**Difficulty**: Medium
**Time**: 30 minutes

### Objective
Create an extension with multiple commands that activate under different conditions.

### Requirements
1. Command 1: "Count Lines" - Only activates when a text file is open
2. Command 2: "Count Words" - Activates for markdown files
3. Command 3: "Show Stats" - Always available
4. Each command should show different statistics

### Activation Events
```json
{
  "activationEvents": [
    "onCommand:stats.countLines",
    "onLanguage:markdown",
    "onCommand:stats.showStats"
  ]
}
```

### Bonus
- Add a status bar item showing stats in real-time
- Create a custom view to display statistics history

---

## Exercise 3: Manifest Customization

**Difficulty**: Easy
**Time**: 20 minutes

### Objective
Enhance your extension's manifest with professional metadata and contributions.

### Requirements
1. Add a custom icon (128x128 PNG)
2. Configure gallery banner color
3. Add appropriate keywords and category
4. Create keyboard shortcuts for commands
5. Add commands to context menus

### Files to Modify
- `package.json` - Update metadata
- Add `images/icon.png`
- Add repository and bug tracking URLs

### Validation
- Package your extension: `vsce package`
- Install the `.vsix` file
- Verify icon appears in Extensions view
- Test keyboard shortcuts

---

## Exercise 4: Language-Specific Activation

**Difficulty**: Medium
**Time**: 40 minutes

### Objective
Create an extension that provides Python-specific utilities.

### Requirements
1. Activate only when Python files are open
2. Command: "Insert Python Docstring" - Adds template docstring
3. Command: "Run Current File" - Executes Python file
4. Command: "Add Type Hints" - Prompts for type hints
5. Status bar showing Python version (mock it)

### Activation Event
```json
{
  "activationEvents": [
    "onLanguage:python"
  ]
}
```

### Implementation Hints
- Use `vscode.window.activeTextEditor`
- Use `vscode.workspace.getConfiguration('python')`
- Insert text at cursor position
- Use terminal for running files

### Bonus
- Detect Python virtual environment
- Show different status bar items based on file type
- Add snippet suggestions

---

## Exercise 5: Extension with Configuration

**Difficulty**: Medium
**Time**: 45 minutes

### Objective
Create a configurable extension that respects user preferences.

### Requirements
1. Add multiple configuration options:
   - Boolean: Enable/disable feature
   - Number: Max items to show
   - String: Default output format
   - Array: List of excluded patterns
2. Read configuration in your code
3. React to configuration changes
4. Validate configuration values

### Configuration Schema
```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myExt.enabled": {
          "type": "boolean",
          "default": true
        },
        "myExt.maxItems": {
          "type": "number",
          "default": 10,
          "minimum": 1,
          "maximum": 100
        },
        "myExt.format": {
          "type": "string",
          "enum": ["json", "xml", "yaml"],
          "default": "json"
        },
        "myExt.excludePatterns": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "default": ["node_modules", ".git"]
        }
      }
    }
  }
}
```

### Bonus
- Add configuration validation
- Show warning when invalid configuration is detected
- Provide quick fix for common configuration errors

---

## Exercise 6: Comprehensive Extension

**Difficulty**: Hard
**Time**: 90 minutes

### Objective
Build a complete "File Info" extension combining everything you've learned.

### Requirements

#### Commands
1. "Show File Info" - Display comprehensive file information
2. "Compare Files" - Compare two selected files
3. "Export File Stats" - Export statistics to JSON

#### UI Elements
1. Status bar showing current file stats
2. Context menu items for files
3. Commands in editor title bar

#### Features
- File information to display:
  - Name, size, extension
  - Line count, word count, character count
  - Creation date, modification date
  - Language ID
  - Git status (if in repository)
- Update stats when file changes
- Configuration for what info to show
- Keyboard shortcuts

#### Configuration
```json
{
  "fileInfo.showInStatusBar": true,
  "fileInfo.statsToShow": ["lines", "words", "size"],
  "fileInfo.updateFrequency": 500
}
```

### Testing Checklist
- [ ] Commands appear in Command Palette
- [ ] Status bar updates when switching files
- [ ] Configuration changes take effect immediately
- [ ] Context menu items show in correct locations
- [ ] Keyboard shortcuts work
- [ ] Extension only activates when needed
- [ ] No errors in Debug Console

### Bonus Features
- Export to multiple formats (JSON, CSV, Markdown)
- Historical statistics tracking
- Compare two files side-by-side
- Customize status bar format
- Add icons to all commands

---

## Solutions

Solutions for all exercises are available in the `solutions/` directory.

**Important**: Try to complete the exercises on your own first! Only refer to solutions if you're stuck.

## Grading Rubric

For each exercise, evaluate:

- **Functionality** (40%): Does it work as specified?
- **Code Quality** (30%): Is the code clean and well-organized?
- **User Experience** (20%): Is it intuitive and user-friendly?
- **Best Practices** (10%): Follows VS Code extension guidelines?

## Getting Help

If you're stuck:

1. Review the lesson materials
2. Check the [VS Code API Documentation](https://code.visualstudio.com/api)
3. Look at example code in the `examples/` directory
4. Search for similar extensions on GitHub
5. Ask in VS Code Discord or Stack Overflow

## Next Steps

Once you've completed these exercises, you're ready for [Module 2: Core Concepts](../../module-02-core-concepts/README.md)!
