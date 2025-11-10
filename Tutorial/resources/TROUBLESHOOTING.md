# VS Code Extension Development Troubleshooting Guide

## Common Issues and Solutions

### Extension Development Issues

#### 1. Extension Not Activating

**Symptoms**:
- Extension code doesn't run
- Commands don't appear
- No log output

**Solutions**:

**Check Activation Events**:
```json
// package.json
{
  "activationEvents": [
    "onCommand:yourExtension.command",
    "onLanguage:javascript"
  ]
}
```

**Verify Extension Host is Running**:
- Open Debug Console (`Ctrl+Shift+Y`)
- Look for "Extension Host" output
- Check for activation errors

**Check Main Entry Point**:
```json
// package.json
{
  "main": "./out/extension.js"  // Must point to compiled JS
}
```

**Verify Compilation**:
```bash
npm run compile
# Check that out/ directory exists with .js files
```

---

#### 2. Command Not Found

**Symptoms**:
- Command doesn't appear in Command Palette
- "Command not found" error

**Solutions**:

**Check Command Registration**:
```typescript
// extension.ts
context.subscriptions.push(
    vscode.commands.registerCommand('extension.command', () => {
        // Implementation
    })
);
```

**Verify package.json**:
```json
{
  "contributes": {
    "commands": [
      {
        "command": "extension.command",  // Must match exactly
        "title": "My Command"
      }
    ]
  }
}
```

**Reload Window**:
- Press `Ctrl+Shift+P`
- Type "Developer: Reload Window"
- Or press `Ctrl+R` in Extension Development Host

---

#### 3. TypeScript Compilation Errors

**Symptoms**:
- Red squiggles in code
- Build fails
- "Cannot find module 'vscode'"

**Solutions**:

**Install Type Definitions**:
```bash
npm install --save-dev @types/vscode @types/node
```

**Check tsconfig.json**:
```json
{
  "compilerOptions": {
    "module": "Node16",
    "target": "ES2022",
    "outDir": "out",
    "lib": ["ES2022"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true
  }
}
```

**Verify Engine Version**:
```json
// package.json
{
  "engines": {
    "vscode": "^1.85.0"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0"  // Must match engine version
  }
}
```

---

#### 4. Changes Not Reflected

**Symptoms**:
- Code changes don't take effect
- Still seeing old behavior

**Solutions**:

**Rebuild**:
```bash
npm run compile
```

**Use Watch Mode**:
```bash
npm run watch  # Auto-compiles on save
```

**Restart Extension Host**:
- Press `Ctrl+Shift+F5` in main VS Code window
- Or `Ctrl+R` in Extension Development Host

**Check Source Maps**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true  // Enable debugging TypeScript
  }
}
```

---

#### 5. Debugging Not Working

**Symptoms**:
- Breakpoints don't hit
- Can't inspect variables
- Debugger doesn't attach

**Solutions**:

**Verify launch.json**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
      "outFiles": ["${workspaceFolder}/out/**/*.js"],
      "preLaunchTask": "${defaultBuildTask}"
    }
  ]
}
```

**Enable Source Maps**:
- Ensure `tsconfig.json` has `"sourceMap": true`
- Check that `.js.map` files exist in `out/`

**Check Breakpoint Location**:
- Breakpoints must be in TypeScript files (`src/*.ts`)
- Not in compiled JavaScript (`out/*.js`)

**View Debug Console**:
- `Ctrl+Shift+Y` to see console output
- Check for errors or warnings

---

#### 6. Extension Host Crash

**Symptoms**:
- Extension Development Host closes unexpectedly
- "Extension host terminated unexpectedly" error

**Solutions**:

**Check for Infinite Loops**:
```typescript
// Bad: Infinite loop
while (true) {
    // ...
}

// Good: Limited iterations
for (let i = 0; i < 1000; i++) {
    // ...
}
```

**Handle Promises Properly**:
```typescript
// Bad: Unhandled rejection
someAsyncFunction();

// Good: Handle errors
someAsyncFunction().catch(error => {
    console.error('Error:', error);
});
```

**Check Memory Usage**:
- Monitor extension host process
- Look for memory leaks
- Dispose of resources properly

**View Extension Host Log**:
- Help → Toggle Developer Tools
- Check Console tab for errors

---

#### 7. Webview Not Displaying

**Symptoms**:
- Blank webview panel
- Content not loading

**Solutions**:

**Check Content Security Policy**:
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none';
               style-src ${webview.cspSource} 'unsafe-inline';
               script-src ${webview.cspSource};">
```

**Use Webview URIs**:
```typescript
// Bad: Local file path
const imagePath = '/path/to/image.png';

// Good: Webview URI
const imagePath = webviewPanel.webview.asWebviewUri(
    vscode.Uri.file(path.join(context.extensionPath, 'media', 'image.png'))
);
```

**Enable Local Resource Roots**:
```typescript
const panel = vscode.window.createWebviewPanel(
    'myWebview',
    'My Webview',
    vscode.ViewColumn.One,
    {
        enableScripts: true,
        localResourceRoots: [
            vscode.Uri.file(path.join(context.extensionPath, 'media'))
        ]
    }
);
```

**Check Developer Tools**:
- Right-click webview → Inspect Element
- Check Console for errors

---

#### 8. Configuration Not Working

**Symptoms**:
- Settings don't apply
- Can't read configuration values

**Solutions**:

**Read Configuration Correctly**:
```typescript
// Get configuration
const config = vscode.workspace.getConfiguration('myExtension');
const value = config.get<string>('settingName', 'defaultValue');
```

**Check Configuration Schema**:
```json
{
  "contributes": {
    "configuration": {
      "properties": {
        "myExtension.settingName": {  // Full name with prefix
          "type": "string",
          "default": "defaultValue"
        }
      }
    }
  }
}
```

**Listen to Configuration Changes**:
```typescript
vscode.workspace.onDidChangeConfiguration(e => {
    if (e.affectsConfiguration('myExtension.settingName')) {
        // Reload configuration
    }
});
```

---

#### 9. Tests Failing

**Symptoms**:
- Tests fail or don't run
- "Cannot find module" errors in tests

**Solutions**:

**Check Test Configuration**:
```json
// package.json
{
  "scripts": {
    "test": "vscode-test"
  }
}
```

**Install Test Dependencies**:
```bash
npm install --save-dev @vscode/test-cli @vscode/test-electron mocha @types/mocha
```

**Verify Test File Structure**:
```
src/
└── test/
    ├── extension.test.ts
    └── index.ts  # Test runner
```

**Run Tests**:
```bash
npm test
```

---

#### 10. Publishing Errors

**Symptoms**:
- `vsce publish` fails
- Package validation errors

**Solutions**:

**Check Required Fields**:
```json
{
  "name": "my-extension",
  "publisher": "your-publisher-name",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.85.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/username/repo"
  }
}
```

**Add .vscodeignore**:
```
.vscode/**
src/**
node_modules/**
*.ts
tsconfig.json
.gitignore
.eslintrc.json
```

**Create Publisher**:
```bash
vsce create-publisher your-publisher-name
```

**Login**:
```bash
vsce login your-publisher-name
```

---

### Performance Issues

#### 11. Slow Extension Activation

**Solutions**:

**Use Lazy Activation**:
```json
{
  "activationEvents": [
    "onCommand:extension.command"  // Only when command is used
    // Not "*"  // Avoid activating on startup
  ]
}
```

**Defer Heavy Operations**:
```typescript
export function activate(context: vscode.ExtensionContext) {
    // Quick activation
    registerCommands(context);

    // Defer heavy initialization
    setTimeout(() => {
        loadHeavyResources();
    }, 1000);
}
```

**Profile Activation**:
```typescript
console.time('Extension Activation');
// ... activation code
console.timeEnd('Extension Activation');
```

---

#### 12. High Memory Usage

**Solutions**:

**Dispose Resources**:
```typescript
const disposable = vscode.commands.registerCommand('cmd', () => {});
context.subscriptions.push(disposable);  // Ensures cleanup
```

**Avoid Global State**:
```typescript
// Bad: Global cache grows indefinitely
const globalCache = new Map();

// Good: Use WeakMap or limit size
const cache = new Map();
if (cache.size > 1000) {
    cache.clear();
}
```

**Profile Memory**:
- Help → Toggle Developer Tools
- Memory tab → Take heap snapshot

---

### Debugging Tips

#### Enable Verbose Logging

```typescript
const outputChannel = vscode.window.createOutputChannel('My Extension');
outputChannel.appendLine('Debug message');
outputChannel.show();
```

#### Use Debug Points

```typescript
debugger;  // Pauses execution when DevTools is open
```

#### Check Extension Host Logs

```bash
# Linux/Mac
~/.vscode/extensions/logs

# Windows
%USERPROFILE%\.vscode\extensions\logs
```

---

## Getting Help

### Official Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [Extension Samples](https://github.com/microsoft/vscode-extension-samples)
- [VS Code Discord](https://aka.ms/vscode-discord)

### Community Resources

- [Stack Overflow](https://stackoverflow.com/questions/tagged/vscode-extensions)
- [GitHub Discussions](https://github.com/microsoft/vscode-discussions)
- [Reddit r/vscode](https://www.reddit.com/r/vscode)

### Debugging Checklist

- [ ] Check Debug Console for errors
- [ ] Verify compilation succeeded (`npm run compile`)
- [ ] Reload Extension Development Host (`Ctrl+R`)
- [ ] Check `package.json` manifest
- [ ] Verify activation events
- [ ] Check command registration
- [ ] Review extension logs
- [ ] Test in clean VS Code profile
- [ ] Check VS Code version compatibility

---

## Useful Commands

```bash
# Build
npm run compile
npm run watch

# Test
npm test

# Package
vsce package

# Publish
vsce publish

# Clean rebuild
rm -rf out node_modules
npm install
npm run compile
```

---

## Still Stuck?

1. **Create minimal reproduction**
2. **Check existing issues** on GitHub
3. **Ask in VS Code Discord** #api channel
4. **Post on Stack Overflow** with `vscode-extensions` tag
5. **Open GitHub issue** if it's a bug

Include:
- VS Code version
- Extension manifest (`package.json`)
- Minimal code example
- Steps to reproduce
- Error messages
- Debug console output
