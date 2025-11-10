# VS Code Extension API Cheatsheet

## Quick Reference Guide

### Essential Imports

```typescript
import * as vscode from 'vscode';
```

---

## Commands

### Register Command

```typescript
vscode.commands.registerCommand('extension.commandId', () => {
    // Command implementation
});

// With arguments
vscode.commands.registerCommand('extension.commandId', (arg1, arg2) => {
    // Use arguments
});
```

### Execute Command

```typescript
await vscode.commands.executeCommand('extension.commandId');
await vscode.commands.executeCommand('workbench.action.files.save');
```

### Get Commands

```typescript
const commands = await vscode.commands.getCommands();
```

---

## Window

### Messages

```typescript
// Information
vscode.window.showInformationMessage('Info message');

// Warning
vscode.window.showWarningMessage('Warning message');

// Error
vscode.window.showErrorMessage('Error message');

// With actions
const selection = await vscode.window.showInformationMessage(
    'Message',
    'Action 1',
    'Action 2'
);
if (selection === 'Action 1') {
    // Handle action
}
```

### Input Box

```typescript
const value = await vscode.window.showInputBox({
    prompt: 'Enter value',
    placeHolder: 'Placeholder text',
    value: 'Default value',
    validateInput: (text) => {
        return text.length < 3 ? 'Must be at least 3 characters' : null;
    }
});
```

### Quick Pick

```typescript
const items = ['Option 1', 'Option 2', 'Option 3'];
const selected = await vscode.window.showQuickPick(items, {
    placeHolder: 'Select an option',
    canPickMany: false
});

// With custom items
interface MyQuickPickItem extends vscode.QuickPickItem {
    value: string;
}

const items: MyQuickPickItem[] = [
    { label: 'Option 1', description: 'Description', value: 'val1' },
    { label: 'Option 2', description: 'Description', value: 'val2' }
];

const selected = await vscode.window.showQuickPick(items);
```

### Progress

```typescript
vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: 'Processing...',
    cancellable: true
}, async (progress, token) => {
    token.onCancellationRequested(() => {
        console.log('User canceled');
    });

    progress.report({ increment: 0 });
    await doWork();
    progress.report({ increment: 50, message: 'Half done' });
    await doMoreWork();
    progress.report({ increment: 50 });
});
```

### Status Bar

```typescript
const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100  // Priority
);

statusBarItem.text = '$(check) Status';
statusBarItem.tooltip = 'Tooltip text';
statusBarItem.command = 'extension.command';
statusBarItem.show();

// Update
statusBarItem.text = 'New text';

// Dispose
statusBarItem.dispose();
```

### Output Channel

```typescript
const outputChannel = vscode.window.createOutputChannel('My Extension');
outputChannel.appendLine('Log message');
outputChannel.show();
```

### Active Editor

```typescript
const editor = vscode.window.activeTextEditor;
if (editor) {
    const document = editor.document;
    const selection = editor.selection;
}
```

---

## Text Editor

### Get Text

```typescript
const editor = vscode.window.activeTextEditor;
const document = editor.document;

// All text
const allText = document.getText();

// Range
const range = new vscode.Range(0, 0, 5, 10);
const rangeText = document.getText(range);

// Selection
const selectedText = document.getText(editor.selection);

// Line
const line = document.lineAt(0);
const lineText = line.text;
```

### Edit Text

```typescript
editor.edit(editBuilder => {
    // Insert
    editBuilder.insert(new vscode.Position(0, 0), 'Text to insert');

    // Replace
    editBuilder.replace(
        new vscode.Range(0, 0, 1, 0),
        'Replacement text'
    );

    // Delete
    editBuilder.delete(new vscode.Range(0, 0, 1, 0));
});
```

### Selections

```typescript
// Get selection
const selection = editor.selection;
const start = selection.start;  // Position
const end = selection.end;      // Position

// Set selection
editor.selection = new vscode.Selection(
    new vscode.Position(0, 0),
    new vscode.Position(0, 10)
);

// Multiple selections
editor.selections = [
    new vscode.Selection(0, 0, 0, 5),
    new vscode.Selection(1, 0, 1, 5)
];
```

### Insert Snippet

```typescript
const snippet = new vscode.SnippetString('Hello ${1:World}!');
editor.insertSnippet(snippet);
```

---

## Workspace

### Configuration

```typescript
// Get configuration
const config = vscode.workspace.getConfiguration('myExtension');

// Get value
const value = config.get<string>('settingName', 'defaultValue');

// Update configuration
await config.update('settingName', 'newValue', vscode.ConfigurationTarget.Global);
```

### Workspace Folders

```typescript
const folders = vscode.workspace.workspaceFolders;
if (folders) {
    folders.forEach(folder => {
        console.log(folder.uri.fsPath);
    });
}
```

### Find Files

```typescript
const files = await vscode.workspace.findFiles(
    '**/*.js',           // include pattern
    '**/node_modules/**' // exclude pattern
);
```

### Open Text Document

```typescript
const document = await vscode.workspace.openTextDocument(uri);

// Create untitled
const document = await vscode.workspace.openTextDocument({
    content: 'Initial content',
    language: 'javascript'
});
```

### Edit Document

```typescript
const edit = new vscode.WorkspaceEdit();

// Insert
edit.insert(uri, position, 'text');

// Replace
edit.replace(uri, range, 'text');

// Delete
edit.delete(uri, range);

// Apply
await vscode.workspace.applyEdit(edit);
```

---

## Events

### Document Events

```typescript
vscode.workspace.onDidOpenTextDocument(document => {
    console.log('Opened:', document.fileName);
});

vscode.workspace.onDidCloseTextDocument(document => {
    console.log('Closed:', document.fileName);
});

vscode.workspace.onDidChangeTextDocument(event => {
    console.log('Changed:', event.document.fileName);
    event.contentChanges.forEach(change => {
        console.log('Change:', change.text);
    });
});

vscode.workspace.onDidSaveTextDocument(document => {
    console.log('Saved:', document.fileName);
});
```

### Editor Events

```typescript
vscode.window.onDidChangeActiveTextEditor(editor => {
    if (editor) {
        console.log('Active editor:', editor.document.fileName);
    }
});

vscode.window.onDidChangeTextEditorSelection(event => {
    console.log('Selection changed:', event.selections);
});
```

### Configuration Events

```typescript
vscode.workspace.onDidChangeConfiguration(event => {
    if (event.affectsConfiguration('myExtension.settingName')) {
        // Reload configuration
    }
});
```

---

## Decorations

### Create Decoration Type

```typescript
const decorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(255, 0, 0, 0.3)',
    border: '1px solid red',
    borderRadius: '3px',
    color: 'white',
    fontWeight: 'bold',
    textDecoration: 'underline',
    cursor: 'pointer',

    // Gutter
    gutterIconPath: vscode.Uri.file('/path/to/icon.svg'),
    gutterIconSize: 'contain',

    // Overview ruler
    overviewRulerColor: 'red',
    overviewRulerLane: vscode.OverviewRulerLane.Full,

    // Before/After
    before: {
        contentText: '→ ',
        color: 'grey'
    },
    after: {
        contentText: ' ←',
        color: 'grey'
    }
});
```

### Apply Decorations

```typescript
const ranges = [
    new vscode.Range(0, 0, 0, 10),
    new vscode.Range(1, 0, 1, 10)
];

editor.setDecorations(decorationType, ranges);

// With hover message
const decorations = ranges.map(range => ({
    range,
    hoverMessage: 'Hover text'
}));

editor.setDecorations(decorationType, decorations);
```

---

## Language Features

### Hover Provider

```typescript
vscode.languages.registerHoverProvider('javascript', {
    provideHover(document, position, token) {
        const range = document.getWordRangeAtPosition(position);
        const word = document.getText(range);

        const markdown = new vscode.MarkdownString();
        markdown.appendCodeblock(word, 'javascript');
        markdown.appendText('Description of ' + word);

        return new vscode.Hover(markdown);
    }
});
```

### Completion Provider

```typescript
vscode.languages.registerCompletionItemProvider('javascript', {
    provideCompletionItems(document, position, token, context) {
        const items: vscode.CompletionItem[] = [];

        // Simple completion
        const item1 = new vscode.CompletionItem('myFunction');
        item1.kind = vscode.CompletionItemKind.Function;
        item1.detail = 'My custom function';
        item1.documentation = 'Documentation';
        items.push(item1);

        // Snippet completion
        const item2 = new vscode.CompletionItem('mySnippet');
        item2.insertText = new vscode.SnippetString('function ${1:name}() {\n\t$0\n}');
        item2.kind = vscode.CompletionItemKind.Snippet;
        items.push(item2);

        return items;
    }
}, '.');  // Trigger characters
```

### Code Actions

```typescript
vscode.languages.registerCodeActionsProvider('javascript', {
    provideCodeActions(document, range, context, token) {
        const actions: vscode.CodeAction[] = [];

        // Quick fix
        const fix = new vscode.CodeAction(
            'Fix this issue',
            vscode.CodeActionKind.QuickFix
        );
        fix.edit = new vscode.WorkspaceEdit();
        fix.edit.replace(document.uri, range, 'fixed text');
        actions.push(fix);

        // Refactor
        const refactor = new vscode.CodeAction(
            'Extract method',
            vscode.CodeActionKind.Refactor
        );
        refactor.command = {
            command: 'extension.extractMethod',
            title: 'Extract Method',
            arguments: [document, range]
        };
        actions.push(refactor);

        return actions;
    }
});
```

### Code Lens

```typescript
vscode.languages.registerCodeLensProvider('javascript', {
    provideCodeLenses(document, token) {
        const codeLenses: vscode.CodeLens[] = [];

        const topOfDocument = new vscode.Range(0, 0, 0, 0);
        const lens = new vscode.CodeLens(topOfDocument, {
            title: 'Click me',
            command: 'extension.command',
            arguments: [document]
        });

        codeLenses.push(lens);
        return codeLenses;
    }
});
```

---

## Tree View

### Tree Data Provider

```typescript
class MyTreeDataProvider implements vscode.TreeDataProvider<MyTreeItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<MyTreeItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }

    getTreeItem(element: MyTreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: MyTreeItem): MyTreeItem[] {
        if (!element) {
            // Root items
            return [
                new MyTreeItem('Item 1', vscode.TreeItemCollapsibleState.None),
                new MyTreeItem('Item 2', vscode.TreeItemCollapsibleState.Collapsed)
            ];
        }
        // Children of element
        return [];
    }
}

class MyTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.tooltip = `Tooltip for ${this.label}`;
        this.description = 'Description';
    }

    iconPath = new vscode.ThemeIcon('symbol-class');
    contextValue = 'myTreeItem';
}

// Register
const treeDataProvider = new MyTreeDataProvider();
vscode.window.registerTreeDataProvider('myView', treeDataProvider);
```

---

## Webview

### Create Webview Panel

```typescript
const panel = vscode.window.createWebviewPanel(
    'myWebview',                        // View type
    'My Webview',                       // Title
    vscode.ViewColumn.One,             // Column
    {
        enableScripts: true,
        localResourceRoots: [
            vscode.Uri.file(path.join(context.extensionPath, 'media'))
        ]
    }
);

panel.webview.html = getWebviewContent();

// Handle messages from webview
panel.webview.onDidReceiveMessage(
    message => {
        switch (message.command) {
            case 'alert':
                vscode.window.showInformationMessage(message.text);
                return;
        }
    },
    undefined,
    context.subscriptions
);
```

### Webview HTML

```typescript
function getWebviewContent() {
    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'none'; script-src 'nonce-${getNonce()}'; style-src 'unsafe-inline';">
</head>
<body>
    <button onclick="sendMessage()">Click me</button>
    <script nonce="${getNonce()}">
        const vscode = acquireVsCodeApi();

        function sendMessage() {
            vscode.postMessage({
                command: 'alert',
                text: 'Hello from webview!'
            });
        }
    </script>
</body>
</html>`;
}

function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
```

---

## File System

### Read File

```typescript
const uri = vscode.Uri.file('/path/to/file.txt');
const bytes = await vscode.workspace.fs.readFile(uri);
const text = Buffer.from(bytes).toString('utf8');
```

### Write File

```typescript
const uri = vscode.Uri.file('/path/to/file.txt');
const bytes = Buffer.from('Hello World', 'utf8');
await vscode.workspace.fs.writeFile(uri, bytes);
```

### File Operations

```typescript
// Create directory
await vscode.workspace.fs.createDirectory(uri);

// Delete
await vscode.workspace.fs.delete(uri);

// Rename
await vscode.workspace.fs.rename(oldUri, newUri);

// Copy
await vscode.workspace.fs.copy(sourceUri, targetUri);

// Stat
const stat = await vscode.workspace.fs.stat(uri);
console.log('Size:', stat.size);
console.log('Modified:', stat.mtime);
```

---

## Common Patterns

### Dispose Pattern

```typescript
const disposable = vscode.commands.registerCommand('cmd', () => {});
context.subscriptions.push(disposable);

// Or manually
disposable.dispose();
```

### Async Command

```typescript
vscode.commands.registerCommand('cmd', async () => {
    try {
        const result = await someAsyncOperation();
        vscode.window.showInformationMessage(`Result: ${result}`);
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
});
```

### Get Extension Path

```typescript
const extensionPath = context.extensionPath;
const resourcePath = path.join(extensionPath, 'resources', 'file.txt');
```

---

## Useful Utilities

```typescript
// Delay
await new Promise(resolve => setTimeout(resolve, 1000));

// Position
const pos = new vscode.Position(line, character);

// Range
const range = new vscode.Range(startPos, endPos);
const range2 = new vscode.Range(startLine, startChar, endLine, endChar);

// URI
const fileUri = vscode.Uri.file('/path/to/file');
const httpUri = vscode.Uri.parse('https://example.com');

// Theme Icon
const icon = new vscode.ThemeIcon('check');
```

---

## References

- [VS Code API Reference](https://code.visualstudio.com/api/references/vscode-api)
- [Extension Guides](https://code.visualstudio.com/api/extension-guides/overview)
- [Extension Samples](https://github.com/microsoft/vscode-extension-samples)
