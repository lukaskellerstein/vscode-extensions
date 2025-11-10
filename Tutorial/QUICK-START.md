# VS Code Extensions - Quick Start Guide

Get started in 15 minutes! ⚡

## Step 1: Install Tools (5 minutes)

```bash
# Verify Node.js (v18+)
node --version

# Install generator
npm install -g yo generator-code vsce

# Verify
yo --version
```

## Step 2: Create Extension (2 minutes)

```bash
# Generate extension
yo code

# Answers:
# - Type: New Extension (TypeScript)
# - Name: my-extension
# - Identifier: my-extension
# - Description: My first extension
# - Git: Yes
# - Package manager: npm

# Open in VS Code
cd my-extension
code .
```

## Step 3: Run & Test (1 minute)

1. Press `F5` to launch Extension Development Host
2. In new window: `Ctrl+Shift+P` → "Hello World"
3. See notification: "Hello World from my-extension!"

**✅ Success!** You've created and run your first extension.

## Step 4: Make Changes (5 minutes)

Edit `src/extension.ts`:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Command 1: Greeting
    let hello = vscode.commands.registerCommand('my-extension.hello', () => {
        vscode.window.showInformationMessage('Hello! 👋');
    });

    // Command 2: Show time
    let time = vscode.commands.registerCommand('my-extension.time', () => {
        const now = new Date().toLocaleTimeString();
        vscode.window.showInformationMessage(`Time: ${now} ⏰`);
    });

    // Command 3: User input
    let greet = vscode.commands.registerCommand('my-extension.greet', async () => {
        const name = await vscode.window.showInputBox({
            prompt: 'What is your name?'
        });
        if (name) {
            vscode.window.showInformationMessage(`Hello, ${name}! 🎉`);
        }
    });

    context.subscriptions.push(hello, time, greet);
}

export function deactivate() {}
```

Update `package.json`:

```json
{
  "contributes": {
    "commands": [
      {
        "command": "my-extension.hello",
        "title": "Say Hello"
      },
      {
        "command": "my-extension.time",
        "title": "Show Time"
      },
      {
        "command": "my-extension.greet",
        "title": "Greet Me"
      }
    ]
  }
}
```

## Step 5: Test Changes (2 minutes)

1. Save files
2. In Extension Development Host: `Ctrl+R` (reload)
3. Try all three commands!

## Next Steps

### Learn More (Choose Your Path)

**Complete Tutorial**:
- 📖 Read [GETTING-STARTED.md](./GETTING-STARTED.md)
- 📚 Start [Module 1](./modules/module-01-foundations/README.md)

**Need Help?**:
- 🔧 [Troubleshooting Guide](./resources/TROUBLESHOOTING.md)
- 📋 [API Cheatsheet](./resources/cheatsheets/API-CHEATSHEET.md)

**Build Something**:
- 🎯 Try [Project 1: Snippet Manager](./projects/project-01-snippet-manager/README.md)

### Common Tasks

**Add Status Bar Item**:
```typescript
const statusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right
);
statusBar.text = '$(heart) My Extension';
statusBar.show();
context.subscriptions.push(statusBar);
```

**Add Configuration**:
```json
// package.json
{
  "contributes": {
    "configuration": {
      "properties": {
        "myExtension.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable extension"
        }
      }
    }
  }
}
```

**Read Configuration**:
```typescript
const config = vscode.workspace.getConfiguration('myExtension');
const enabled = config.get<boolean>('enabled', true);
```

**Add Keyboard Shortcut**:
```json
// package.json
{
  "contributes": {
    "keybindings": [
      {
        "command": "my-extension.hello",
        "key": "ctrl+alt+h",
        "mac": "cmd+alt+h"
      }
    ]
  }
}
```

**Edit Active File**:
```typescript
const editor = vscode.window.activeTextEditor;
if (editor) {
    editor.edit(editBuilder => {
        editBuilder.insert(
            new vscode.Position(0, 0),
            '// Hello from extension\n'
        );
    });
}
```

## Debugging Tips

- `F5` - Start debugging
- `Ctrl+Shift+F5` - Restart
- `Ctrl+Shift+Y` - Debug Console
- Set breakpoints in TypeScript files
- Use `console.log()` for quick debugging

## Common Issues

**Extension not activating?**
- Check `activationEvents` in package.json
- Run `npm run compile`
- Check Debug Console for errors

**Command not found?**
- Reload Extension Host (`Ctrl+R`)
- Verify command ID matches in code and package.json
- Check `contributes.commands` section

**Changes not showing?**
- Run `npm run compile`
- Or use `npm run watch` for auto-compile
- Reload Extension Host

## Package & Publish

```bash
# Package
vsce package

# Creates: my-extension-0.0.1.vsix

# Install locally
code --install-extension my-extension-0.0.1.vsix

# Publish (after creating publisher account)
vsce publish
```

## Resources

- 📖 [Complete Tutorial](./README.md)
- 🎓 [Module 1: Foundations](./modules/module-01-foundations/README.md)
- 🔧 [Troubleshooting](./resources/TROUBLESHOOTING.md)
- 📋 [API Cheatsheet](./resources/cheatsheets/API-CHEATSHEET.md)
- 🌐 [VS Code API Docs](https://code.visualstudio.com/api)
- 💬 [VS Code Discord](https://aka.ms/vscode-discord)

## That's It!

You're now ready to build VS Code extensions. Happy coding! 🚀

For comprehensive learning, continue with the [full tutorial](./GETTING-STARTED.md).
