# Communication Flow in lukas-extension-4

This document explains how communication flows between different components when you click the "Add Circle to Editor" button in the sidebar.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VSCode Extension Host                            │
│                      (Node.js process - main thread)                     │
│                                                                           │
│  ┌────────────────────┐         ┌──────────────────────┐               │
│  │  extension.ts      │         │ LukeEditorProvider   │               │
│  │  - Activation      │────────▶│ - Singleton Instance │               │
│  │  - Registration    │         │ - Active Panel Ref   │               │
│  └────────────────────┘         └──────────┬───────────┘               │
│                                             │                             │
│  ┌────────────────────┐                    │                             │
│  │ SidePanelProvider  │                    │                             │
│  │ - Message Handler  │────────────────────┘                             │
│  └─────────┬──────────┘                                                  │
│            │                                                              │
└────────────┼──────────────────────────────────────────────────────────────┘
             │
             │ postMessage / onDidReceiveMessage
             │ (IPC - Inter-Process Communication)
             │
┌────────────┼──────────────────────────────────────────────────────────────┐
│            ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │              VSCode Webview Containers                           │     │
│  │            (Isolated sandboxed iframes - renderer process)       │     │
│  │                                                                   │     │
│  │  ┌──────────────────────┐          ┌──────────────────────┐     │     │
│  │  │  Sidebar Webview     │          │  Editor Webview      │     │     │
│  │  │  (React App)         │          │  (Canvas App)        │     │     │
│  │  │                      │          │                      │     │     │
│  │  │  ┌────────────────┐ │          │  ┌────────────────┐ │     │     │
│  │  │  │   App.tsx      │ │          │  │  index.tsx     │ │     │     │
│  │  │  │   - Button     │ │          │  │  - Canvas      │ │     │     │
│  │  │  │   - onClick    │ │          │  │  - Circles     │ │     │     │
│  │  │  └────────────────┘ │          │  └────────────────┘ │     │     │
│  │  └──────────────────────┘          └──────────────────────┘     │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                           │
│           Browser Context (Chromium renderer)                            │
└───────────────────────────────────────────────────────────────────────────┘
```

## Complete Communication Flow: Adding a Circle

### Step-by-Step Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    1. USER CLICKS BUTTON                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ SIDEBAR WEBVIEW (src/webview/sidebar/App.tsx:48)                        │
│                                                                           │
│   <button onClick={handleAddCircle}>                                     │
│      Add Circle to Editor                                                │
│   </button>                                                              │
│                                                                           │
│   handleAddCircle() {                                                    │
│     vscode.postMessage({                                                 │
│       type: 'addCircleToEditor'    ◀─── Sends message to extension      │
│     });                                                                  │
│   }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ IPC Channel
                                  │ (postMessage API)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EXTENSION HOST - SidePanelProvider (src/SidePanelProvider.ts:36)        │
│                                                                           │
│   webviewView.webview.onDidReceiveMessage((data) => {                   │
│     switch (data.type) {                                                 │
│       case "addCircleToEditor":                                          │
│         const editorProvider = LukeEditorProvider.getInstance();         │
│         editorProvider.addCircleToActiveEditor();  ◀─── Calls method     │
│         break;                                                           │
│     }                                                                    │
│   });                                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Method Call (Same Process)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EXTENSION HOST - LukeEditorProvider (src/LukeEditorProvider.ts:74)      │
│                                                                           │
│   addCircleToActiveEditor() {                                            │
│     const circle = {                                                     │
│       x: Math.random() * 400 + 50,                                       │
│       y: Math.random() * 400 + 50,                                       │
│       radius: 30,                                                        │
│       color: this._getRandomColor()                                      │
│     };                                                                   │
│                                                                           │
│     this._activeWebviewPanel.webview.postMessage({                       │
│       type: "addCircleFromSidebar",   ◀─── Sends to editor webview      │
│       circle                                                             │
│     });                                                                  │
│   }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ IPC Channel
                                  │ (postMessage API)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EDITOR WEBVIEW (src/webview/editor/index.tsx:60)                        │
│                                                                           │
│   window.addEventListener("message", (event) => {                        │
│     const message = event.data;                                          │
│                                                                           │
│     switch (message.type) {                                              │
│       case "addCircleFromSidebar":                                       │
│         vscode.postMessage({         ◀─── Send back to extension        │
│           type: "addCircle",                                             │
│           circle: message.circle                                         │
│         });                                                              │
│         break;                                                           │
│     }                                                                    │
│   });                                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ IPC Channel
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EXTENSION HOST - LukeEditorProvider (src/LukeEditorProvider.ts:46)      │
│                                                                           │
│   webviewPanel.webview.onDidReceiveMessage((message) => {               │
│     switch (message.type) {                                              │
│       case "addCircle":                                                  │
│         this._addCircle(document, message.circle); ◀─── Add to doc      │
│         break;                                                           │
│     }                                                                    │
│   });                                                                    │
│                                                                           │
│   _addCircle(document, circle) {                                         │
│     const data = this._getDocumentData(document);                        │
│     data.circles.push(circle);                                           │
│     this._updateTextDocument(document, data);  ◀─── Save to file        │
│   }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Document Update Event
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EXTENSION HOST - LukeEditorProvider (src/LukeEditorProvider.ts:58)      │
│                                                                           │
│   vscode.workspace.onDidChangeTextDocument((e) => {                      │
│     if (e.document.uri === document.uri) {                               │
│       this._updateWebview(document, webview);  ◀─── Send updated data   │
│     }                                                                    │
│   });                                                                    │
│                                                                           │
│   _updateWebview(document, webview) {                                    │
│     webview.postMessage({                                                │
│       type: "update",                                                    │
│       data: this._getDocumentData(document)                              │
│     });                                                                  │
│   }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ IPC Channel
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ EDITOR WEBVIEW (src/webview/editor/index.tsx:60)                        │
│                                                                           │
│   window.addEventListener("message", (event) => {                        │
│     switch (event.data.type) {                                           │
│       case "update":                                                     │
│         this.circles = message.data.circles;  ◀─── Update state         │
│         this.render();                        ◀─── Redraw canvas         │
│         break;                                                           │
│     }                                                                    │
│   });                                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Concepts Explained

### 1. **Why `vscode.postMessage()`?**

**What it is:**
- `vscode.postMessage()` is a special API provided by VSCode to webviews
- It's obtained via `acquireVsCodeApi()` in the webview context

**Why we use it:**
- **Security Isolation**: Webviews run in sandboxed iframes with restricted access
- **IPC (Inter-Process Communication)**: Webviews run in a separate renderer process from the extension host (Node.js process)
- **Only Communication Bridge**: This is the ONLY way for webview code to communicate with the extension host
- **Secure Message Passing**: Messages are serialized and passed through a secure channel

**Example:**
```typescript
// In webview (sidebar/App.tsx:33)
const vscode = acquireVsCodeApi();
vscode.postMessage({ type: 'addCircleToEditor' });
```

### 2. **Why `webview.onDidReceiveMessage()`?**

**What it is:**
- A VSCode API method on the extension host side
- Listens for messages sent FROM the webview TO the extension

**Why we use it:**
- **Receive Messages from Webview**: It's the counterpart to `postMessage` from the webview side
- **Handle User Actions**: Allows the extension to respond to user interactions in the webview
- **Bridge to Extension APIs**: Webviews can't directly access VSCode APIs, so they send messages to the extension host which has full API access

**Example:**
```typescript
// In extension host (SidePanelProvider.ts:36)
webviewView.webview.onDidReceiveMessage((data) => {
  // This receives messages sent from the webview
  switch (data.type) {
    case "addCircleToEditor":
      // Now we can use VSCode APIs
      editorProvider.addCircleToActiveEditor();
      break;
  }
});
```

### 3. **Why `canvas.addEventListener('click')`?**

**What it is:**
- Standard browser DOM API for listening to DOM events
- Works exactly like in regular web development

**Why we use it:**
- **User Interaction**: Detects when users click on the canvas
- **Get Click Position**: The event provides `clientX` and `clientY` coordinates
- **Create Circle at Position**: We use these coordinates to place the circle where the user clicked

**Example:**
```typescript
// In editor webview (editor/index.tsx:41)
this.canvas.addEventListener("click", (e) => {
  const rect = this.canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;  // Get click position
  const y = e.clientY - rect.top;

  // Send circle data to extension
  vscode.postMessage({
    type: "addCircle",
    circle: { x, y, radius: 30, color: "#ff0000" }
  });
});
```

### 4. **Why `window.addEventListener('message')`?**

**What it is:**
- Standard browser API for listening to messages sent to the window
- Used to receive messages FROM the extension host TO the webview

**Why we use it:**
- **Receive Extension Messages**: Listens for messages sent via `webview.postMessage()` from the extension host
- **Update UI**: Allows the extension to push updates to the webview (like new circle data)
- **Two-Way Communication**: Completes the bidirectional communication channel

**Example:**
```typescript
// In editor webview (editor/index.tsx:61)
window.addEventListener("message", (event) => {
  const message = event.data;

  switch (message.type) {
    case "update":
      // Extension is telling us the document changed
      this.circles = message.data.circles;
      this.render();  // Redraw the canvas
      break;
  }
});
```

## Communication Patterns

### Pattern 1: Webview → Extension Host → Webview

This is what happens when you click "Add Circle":

1. **Sidebar Webview** sends `addCircleToEditor` message
2. **Extension Host** receives it, generates circle data
3. **Extension Host** sends circle to **Editor Webview**
4. **Editor Webview** sends `addCircle` back to **Extension Host**
5. **Extension Host** saves to document
6. **Extension Host** sends `update` to **Editor Webview**
7. **Editor Webview** renders the new circle

### Pattern 2: Direct Extension → Webview (Document Changes)

When the document changes:

1. **VSCode** fires `onDidChangeTextDocument` event
2. **Extension Host** reads the updated document
3. **Extension Host** sends `update` message to **Editor Webview**
4. **Editor Webview** re-renders with new data

## Security Model

### Sandboxing

```
┌──────────────────────────────────────────────────────┐
│  Extension Host (Node.js)                            │
│  - Full VSCode API access                            │
│  - File system access                                │
│  - Network access                                    │
│  - Can execute code                                  │
└──────────────────────────────────────────────────────┘
                      ▲
                      │ Secure IPC
                      │ (postMessage only)
                      ▼
┌──────────────────────────────────────────────────────┐
│  Webview (Sandboxed iframe)                          │
│  - NO VSCode API access (except postMessage)         │
│  - NO file system access                             │
│  - NO network access (CSP restricted)                │
│  - Can only run approved scripts (nonce-based)       │
│  - Isolated from other webviews                      │
└──────────────────────────────────────────────────────┘
```

### Content Security Policy (CSP)

Each webview has a strict CSP:
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none';
               style-src ${webview.cspSource} 'unsafe-inline';
               script-src 'nonce-${nonce}';">
```

- **`default-src 'none'`**: Block everything by default
- **`script-src 'nonce-${nonce}'`**: Only allow scripts with matching nonce
- **`style-src ... 'unsafe-inline'`**: Allow inline styles (for React)

## Data Flow for Circle Persistence

```
User Click
    │
    ▼
Canvas Event Handler (click)
    │
    ▼
vscode.postMessage({ type: 'addCircle', circle })
    │
    ▼
Extension: onDidReceiveMessage
    │
    ▼
Read Current Document (JSON)
    │
    ▼
Add Circle to Array
    │
    ▼
Write to VSCode Document (WorkspaceEdit)
    │
    ▼
VSCode: onDidChangeTextDocument Event
    │
    ▼
Read Updated Document
    │
    ▼
webview.postMessage({ type: 'update', data })
    │
    ▼
Webview: window.addEventListener('message')
    │
    ▼
Update Canvas State
    │
    ▼
Render Canvas (draw circles)
```

## Why This Architecture?

### 1. **Security**:
- Webviews are sandboxed and can't access sensitive APIs
- Only the extension host can read/write files

### 2. **Isolation**:
- Multiple webviews don't interfere with each other
- Each webview is a separate context

### 3. **Performance**:
- Webviews run in separate processes (Chromium renderer)
- Extension logic runs in Node.js process
- Heavy canvas rendering doesn't block extension

### 4. **Persistence**:
- Extension host manages document changes
- Webviews just render the current state
- Single source of truth (the .luke file)

## Singleton Pattern for Editor Provider

```typescript
// LukeEditorProvider.ts:18-27
private static _instance: LukeEditorProvider | undefined;

constructor(private readonly context: vscode.ExtensionContext) {
  LukeEditorProvider._instance = this;  // Store singleton
}

public static getInstance(): LukeEditorProvider | undefined {
  return LukeEditorProvider._instance;  // Retrieve singleton
}
```

**Why Singleton?**
- **Cross-Component Access**: Allows SidePanelProvider to access the active editor
- **Shared State**: Only one instance tracks which editor is active
- **Coordination**: Sidebar can communicate with currently open editor

## Summary

The communication uses a **message-passing architecture** where:

1. **Webviews** are isolated sandboxes that can only communicate via `postMessage`
2. **Extension Host** is the central coordinator with full VSCode API access
3. **Messages** flow through secure IPC channels
4. **Document** is the single source of truth for data persistence
5. **Events** trigger updates to keep all views in sync

This architecture ensures security, isolation, and proper separation of concerns between UI (webviews) and logic (extension host).
