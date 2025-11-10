# Project 1: Snippet Manager Extension

**Difficulty**: Intermediate
**Time**: 6-8 hours
**Prerequisites**: Modules 1-3

## Project Overview

Build a comprehensive snippet management extension that allows users to create, organize, search, and use custom code snippets with a rich UI.

## Learning Goals

- Build complex webview interfaces
- Implement tree view with drag and drop
- Handle data persistence
- Create command palette integration
- Implement search and filtering
- Work with VS Code snippet format

## Features

### Core Features

1. **Snippet Creation**
   - Create snippets from selected text
   - Quick snippet creator command
   - Support for multiple languages
   - Placeholder support

2. **Snippet Organization**
   - Categories and tags
   - Tree view for browsing
   - Drag and drop to organize
   - Import/export functionality

3. **Snippet Search**
   - Full-text search
   - Filter by language
   - Filter by category
   - Recent snippets

4. **Snippet Insertion**
   - Quick pick for snippet selection
   - Context-aware suggestions
   - Keyboard shortcuts
   - Preview before insertion

### UI Components

1. **Webview Panel**
   - Snippet editor
   - Rich text editing
   - Syntax highlighting
   - Live preview

2. **Tree View**
   - Category hierarchy
   - Snippet list
   - Inline actions
   - Context menus

3. **Status Bar**
   - Snippet count
   - Quick access menu

## Project Structure

```
snippet-manager/
├── src/
│   ├── extension.ts          # Entry point
│   ├── snippetManager.ts     # Core logic
│   ├── snippetProvider.ts    # Tree view provider
│   ├── webview/
│   │   ├── snippetEditor.ts  # Webview controller
│   │   └── ui/
│   │       ├── index.html    # Editor UI
│   │       ├── style.css     # Styles
│   │       └── script.js     # Client-side logic
│   ├── storage/
│   │   └── snippetStorage.ts # Persistence
│   └── commands/
│       ├── createSnippet.ts  # Command handlers
│       ├── insertSnippet.ts
│       └── searchSnippets.ts
├── resources/
│   ├── icons/
│   └── snippets/             # Sample snippets
└── package.json
```

## Implementation Steps

### Phase 1: Basic Infrastructure (2 hours)

1. **Project Setup**
   ```bash
   yo code
   # Choose: New Extension (TypeScript)
   ```

2. **Data Model**
   ```typescript
   interface Snippet {
     id: string;
     name: string;
     prefix: string;
     body: string[];
     description: string;
     language: string;
     category: string;
     tags: string[];
     createdAt: Date;
     updatedAt: Date;
   }

   interface Category {
     id: string;
     name: string;
     icon: string;
     snippets: Snippet[];
   }
   ```

3. **Storage Service**
   - Implement snippet persistence
   - Use workspace state or file system
   - Add import/export functionality

### Phase 2: Tree View (2 hours)

1. **TreeDataProvider**
   ```typescript
   class SnippetTreeProvider implements vscode.TreeDataProvider<SnippetItem> {
     // Implement tree structure
     getChildren(element?: SnippetItem): SnippetItem[]
     getTreeItem(element: SnippetItem): vscode.TreeItem
   }
   ```

2. **Tree Actions**
   - Add snippet
   - Edit snippet
   - Delete snippet
   - Create category
   - Drag and drop

3. **Context Menus**
   - Right-click actions
   - Inline buttons

### Phase 3: Webview Editor (2 hours)

1. **Webview Setup**
   - Create webview panel
   - Load HTML/CSS/JS
   - Implement CSP

2. **Editor UI**
   - Form for snippet properties
   - Code editor for snippet body
   - Preview pane
   - Save/cancel buttons

3. **Communication**
   - Extension → Webview messages
   - Webview → Extension messages
   - State persistence

### Phase 4: Commands & Search (1.5 hours)

1. **Commands**
   - Create from selection
   - Insert snippet
   - Search snippets
   - Manage categories

2. **Quick Pick**
   - List snippets
   - Fuzzy search
   - Preview
   - Multi-step input

3. **Search**
   - Full-text search
   - Language filter
   - Category filter
   - Sort options

### Phase 5: Polish & Testing (0.5 hours)

1. **Configuration**
   - Default language
   - Auto-save
   - Search settings

2. **Icons & UI**
   - Custom icons
   - Consistent styling
   - Loading states

3. **Testing**
   - Unit tests
   - Integration tests
   - Edge cases

## Code Samples

### Extension Activation

```typescript
export function activate(context: vscode.ExtensionContext) {
    const snippetManager = new SnippetManager(context);
    const treeProvider = new SnippetTreeProvider(snippetManager);

    // Register tree view
    vscode.window.registerTreeDataProvider('snippetManager.snippetsView', treeProvider);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('snippetManager.createSnippet', () =>
            snippetManager.createSnippet()
        ),
        vscode.commands.registerCommand('snippetManager.insertSnippet', () =>
            snippetManager.insertSnippet()
        ),
        vscode.commands.registerCommand('snippetManager.searchSnippets', () =>
            snippetManager.searchSnippets()
        )
    );
}
```

### Snippet Insertion

```typescript
async insertSnippet(snippet: Snippet) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const snippetString = new vscode.SnippetString(snippet.body.join('\n'));
    await editor.insertSnippet(snippetString);
}
```

### Webview Communication

```typescript
// Extension side
webviewPanel.webview.postMessage({
    command: 'loadSnippet',
    snippet: snippetData
});

// Webview side (script.js)
window.addEventListener('message', event => {
    const message = event.data;
    switch (message.command) {
        case 'loadSnippet':
            loadSnippet(message.snippet);
            break;
    }
});
```

## Configuration

**package.json**:
```json
{
  "contributes": {
    "views": {
      "explorer": [
        {
          "id": "snippetManager.snippetsView",
          "name": "Snippets"
        }
      ]
    },
    "commands": [
      {
        "command": "snippetManager.createSnippet",
        "title": "Create Snippet from Selection",
        "icon": "$(add)"
      },
      {
        "command": "snippetManager.insertSnippet",
        "title": "Insert Snippet",
        "icon": "$(insert)"
      },
      {
        "command": "snippetManager.searchSnippets",
        "title": "Search Snippets",
        "icon": "$(search)"
      }
    ],
    "keybindings": [
      {
        "command": "snippetManager.createSnippet",
        "key": "ctrl+alt+s",
        "mac": "cmd+alt+s",
        "when": "editorHasSelection"
      },
      {
        "command": "snippetManager.insertSnippet",
        "key": "ctrl+alt+i",
        "mac": "cmd+alt+i"
      }
    ],
    "configuration": {
      "properties": {
        "snippetManager.defaultLanguage": {
          "type": "string",
          "default": "plaintext"
        },
        "snippetManager.autoSave": {
          "type": "boolean",
          "default": true
        }
      }
    }
  }
}
```

## Testing

### Test Cases

1. **Snippet Creation**
   - Create from selection
   - Create empty snippet
   - Validate required fields

2. **Snippet Management**
   - Edit snippet
   - Delete snippet
   - Move to category

3. **Snippet Insertion**
   - Insert at cursor
   - Replace selection
   - Multiple cursors

4. **Search**
   - Find by name
   - Find by content
   - Filter by language

## Bonus Features

1. **Sync**
   - Sync snippets across devices
   - Export to GitHub Gist
   - Import from VS Code snippets

2. **Collaboration**
   - Share snippets with team
   - Snippet marketplace
   - Rating system

3. **Advanced**
   - Variable substitution
   - Snippet transformations
   - Dynamic snippets based on context

## Resources

- [VS Code Snippets Guide](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
- [Tree View API](https://code.visualstudio.com/api/extension-guides/tree-view)
- [Webview API](https://code.visualstudio.com/api/extension-guides/webview)

## Evaluation Criteria

- **Functionality** (40%): All core features work correctly
- **Code Quality** (25%): Clean, maintainable code
- **UX** (20%): Intuitive and responsive UI
- **Error Handling** (15%): Graceful error handling

## Submission

1. Create GitHub repository
2. Add comprehensive README
3. Include demo GIF/video
4. Add unit tests
5. Package as VSIX

Good luck building your Snippet Manager! 🚀
