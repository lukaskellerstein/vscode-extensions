# VSCode Extension Communication Tutorials

This folder contains step-by-step tutorials demonstrating different types of communication patterns in VSCode extensions. Each tutorial builds on the previous one, progressively teaching more complex scenarios.

## Tutorial Overview

### Tutorial 1: Basic Sidebar ↔ Extension Communication
**Folder:** `01-sidebar-to-extension`

**Goal:** Learn the fundamental communication pattern between a sidebar webview and the extension host.

**What You'll Learn:**
- How to create a sidebar webview with React
- How to send messages from webview to extension using `vscode.postMessage()`
- How to receive messages in extension using `webview.onDidReceiveMessage()`
- How to send responses back from extension to webview
- Basic message routing and type safety

**Example Scenario:**
- Sidebar has a button "Send Greeting"
- Click sends message to extension
- Extension processes it and sends back a personalized greeting
- Sidebar displays the response

**Key Concepts:**
- `acquireVsCodeApi()`
- `postMessage()` (webview → extension)
- `onDidReceiveMessage()` (extension receives)
- `webview.postMessage()` (extension → webview)
- `window.addEventListener('message')` (webview receives)

---

### Tutorial 2: Custom Editor ↔ Extension Communication
**Folder:** `02-editor-to-extension`

**Goal:** Learn how custom editors communicate with the extension host and persist data.

**What You'll Learn:**
- How to create a custom text editor for specific file types
- How to read and write to VSCode documents
- How to sync editor state with file content
- Document change events and update patterns
- Data persistence in custom editors

**Example Scenario:**
- Custom editor for `.counter` files
- Canvas with increment/decrement buttons
- Clicking updates counter and saves to file
- File changes trigger UI updates
- Multiple instances stay in sync

**Key Concepts:**
- `CustomTextEditorProvider`
- `resolveCustomTextEditor()`
- `TextDocument` API
- `WorkspaceEdit` for document updates
- `onDidChangeTextDocument` events
- State synchronization

---

### Tutorial 3: Multiple Editors Broadcasting
**Folder:** `03-multiple-editors`

**Goal:** Learn how to manage multiple editor instances and broadcast updates between them.

**What You'll Learn:**
- How to track multiple open editor instances
- How to broadcast messages to all active editors
- How to handle editor lifecycle (open/close)
- How to maintain shared state across editors
- Collision detection and conflict resolution

**Example Scenario:**
- Custom editor for `.shared` files
- Multiple editors can be open for same file
- Drawing app where all editors see the same canvas
- Changes in one editor appear in all others in real-time
- Extension host acts as central coordinator

**Key Concepts:**
- Instance tracking with Maps/Arrays
- Broadcast patterns
- `webviewPanel.onDidDispose()`
- Shared state management
- Race condition handling

---

### Tutorial 4: Sidebar + Editor Coordination
**Folder:** `04-sidebar-editor-coordination`

**Goal:** Learn how to coordinate between sidebar and editor, passing data between them.

**What You'll Learn:**
- How sidebar can control editor behavior
- How editor can update sidebar state
- Singleton pattern for cross-component access
- Bidirectional data flow
- Active editor detection

**Example Scenario:**
- Sidebar with color palette and tool selection
- Custom drawing editor for `.draw` files
- Sidebar button adds shapes to active editor
- Editor selection updates sidebar properties panel
- Tool changes in sidebar affect editor behavior

**Key Concepts:**
- Singleton pattern
- `getInstance()` for cross-provider access
- Active editor tracking
- Message routing between components
- Coordinated state management

---

### Tutorial 5: Extension to Extension Communication (Commands)
**Folder:** `05-extension-to-extension`

**Goal:** Learn how different extensions can communicate with each other.

**What You'll Learn:**
- How to expose commands for other extensions
- How to call commands from other extensions
- Extension API exports
- Event-based communication
- Extension dependencies

**Example Scenario:**
- Extension A: "Data Provider" - exposes data commands
- Extension B: "Data Consumer" - uses Extension A's commands
- Commands to get/set shared data
- Events when data changes
- Both extensions update their UIs

**Key Concepts:**
- `vscode.commands.registerCommand()`
- `vscode.commands.executeCommand()`
- Extension exports API
- `ExtensionContext.extensionPath`
- Cross-extension events

---

### Tutorial 6: TreeView ↔ Extension Communication
**Folder:** `06-treeview-communication`

**Goal:** Learn how TreeView providers communicate with extensions and handle user interactions.

**What You'll Learn:**
- How to create custom TreeView providers
- How to handle TreeView item clicks
- How to refresh TreeView data
- How to implement commands on tree items
- Dynamic tree updates based on events

**Example Scenario:**
- Sidebar TreeView showing project tasks
- Click item to open/edit task
- Add/delete/complete tasks via commands
- Tree updates when tasks change
- Integration with webview panel for task details

**Key Concepts:**
- `TreeDataProvider`
- `TreeItem` and `TreeItemCollapsibleState`
- `onDidChangeTreeData` event
- TreeView commands
- Refreshing tree data

---

### Tutorial 7: Webview Panel ↔ Extension (Modal Dialog Pattern)
**Folder:** `07-webview-panel`

**Goal:** Learn how to create modal-like webview panels for complex forms and workflows.

**What You'll Learn:**
- Difference between webview views and webview panels
- How to create and show webview panels
- Modal patterns and focus management
- Form submission from webview to extension
- Panel lifecycle management

**Example Scenario:**
- Command opens a settings panel (modal-like)
- Complex form with validation in React
- Submit sends data to extension
- Extension updates workspace settings
- Panel closes after successful submit

**Key Concepts:**
- `vscode.window.createWebviewPanel()`
- Panel options and view columns
- `panel.reveal()` and focus management
- `panel.dispose()` for cleanup
- Return values from panels

---

### Tutorial 8: Real-time Collaboration Pattern
**Folder:** `08-realtime-collaboration`

**Goal:** Learn how to implement real-time collaboration features using extension communication.

**What You'll Learn:**
- How to detect external file changes
- How to merge concurrent edits
- How to implement operational transforms
- Debouncing and throttling updates
- Conflict resolution strategies

**Example Scenario:**
- Collaborative text editor for `.collab` files
- Multiple users (simulated as multiple editors)
- Changes appear in real-time
- Visual indicators of other users' cursors
- Conflict resolution when both edit same location

**Key Concepts:**
- File watchers
- Operational Transformation (OT) basics
- Debouncing with timeouts
- Change detection and diffing
- Event coalescing

---

## Tutorial Structure

Each tutorial folder contains:

```
XX-tutorial-name/
├── README.md                 # Detailed explanation
├── COMMUNICATION.md          # Communication flow diagram
├── package.json             # Extension manifest
├── src/
│   ├── extension.ts         # Extension entry point
│   ├── providers/           # Provider classes
│   └── webview/             # React/TS webview code
└── examples/                # Example files to test with
```

## Learning Path

**Recommended Order:**
1. Start with Tutorial 1 (basics)
2. Move to Tutorial 2 (persistence)
3. Tutorial 3 (multiple instances)
4. Tutorial 4 (coordination)
5. Then choose based on interest:
   - Tutorial 5 for extension-to-extension
   - Tutorial 6 for TreeViews
   - Tutorial 7 for panels
   - Tutorial 8 for advanced patterns

## Key Communication Patterns Summary

| Pattern | Direction | Use Case |
|---------|-----------|----------|
| `vscode.postMessage()` | Webview → Extension | User actions in UI |
| `webview.postMessage()` | Extension → Webview | Update UI state |
| `window.addEventListener('message')` | Webview receives | Listen for extension messages |
| `onDidReceiveMessage()` | Extension receives | Handle webview messages |
| `vscode.commands.executeCommand()` | Extension ↔ Extension | Cross-extension calls |
| `onDidChangeTextDocument` | VSCode → Extension | Document changes |
| `WorkspaceEdit` | Extension → VSCode | Modify documents |

## Prerequisites

- Node.js and npm installed
- VSCode installed
- Basic TypeScript/React knowledge
- Understanding of async/await
- Familiarity with event-driven programming

## Running the Tutorials

Each tutorial can be run independently:

```bash
cd XX-tutorial-name
npm install
npm run compile
# Press F5 in VSCode to launch Extension Development Host
```

## Common Pitfalls to Avoid

1. **Forgetting to enable scripts** in webview options
2. **Not handling async** operations properly
3. **Memory leaks** from not disposing subscriptions
4. **Race conditions** in async message handling
5. **CSP violations** from incorrect nonce usage
6. **Stale closures** in event handlers
7. **Not validating** message types and data

## Advanced Topics (Post-Tutorial)

After completing these tutorials, explore:
- WebSocket integration for real collaboration
- IndexedDB for client-side persistence
- Web Workers in webviews
- Virtual scrolling for large datasets
- Monaco Editor integration
- Language Server Protocol (LSP)
- Debug Adapter Protocol (DAP)

## Resources

- [VSCode Extension API](https://code.visualstudio.com/api)
- [Webview API Guide](https://code.visualstudio.com/api/extension-guides/webview)
- [Custom Editor Guide](https://code.visualstudio.com/api/extension-guides/custom-editors)
- [Extension Samples](https://github.com/microsoft/vscode-extension-samples)

## Contributing

Each tutorial should:
- Be self-contained and runnable
- Include detailed comments
- Have a COMMUNICATION.md diagram
- Provide example files
- List key concepts learned
- Include common mistakes section

---

**Happy Learning!** 🚀

Start with Tutorial 1 and work your way through. Each tutorial builds foundational knowledge for the next.
