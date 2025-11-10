import * as vscode from 'vscode';
import { DrawingAPI } from './drawingAPI';

/**
 * Provider for Luke Editor custom editor.
 * Handles the webview-based canvas editor for .luke files.
 */
export class LukeEditorProvider implements vscode.CustomTextEditorProvider {
    private static readonly viewType = 'lukeEditor.editor';
    private static instance: LukeEditorProvider | null = null;
    private drawingAPI: DrawingAPI;
    private openDocuments: Map<string, vscode.TextDocument> = new Map();
    private currentActiveFile: string | null = null;

    constructor(private readonly context: vscode.ExtensionContext) {
        this.drawingAPI = new DrawingAPI();
        LukeEditorProvider.instance = this;
    }

    public getCurrentActiveFile(): string | null {
        return this.currentActiveFile;
    }

    public setCurrentActiveFile(filePath: string) {
        this.currentActiveFile = filePath;
    }

    public static register(context: vscode.ExtensionContext): vscode.Disposable {
        const provider = new LukeEditorProvider(context);
        const providerRegistration = vscode.window.registerCustomEditorProvider(
            LukeEditorProvider.viewType,
            provider,
            {
                webviewOptions: {
                    retainContextWhenHidden: true,
                },
            }
        );
        return providerRegistration;
    }

    public static getInstance(): LukeEditorProvider | null {
        return LukeEditorProvider.instance;
    }

    public async resolveCustomTextEditor(
        document: vscode.TextDocument,
        webviewPanel: vscode.WebviewPanel,
        _token: vscode.CancellationToken
    ): Promise<void> {
        // Track open documents
        this.openDocuments.set(document.uri.fsPath, document);

        // Set this as the current active file
        this.setCurrentActiveFile(document.uri.fsPath);

        // Setup initial webview
        webviewPanel.webview.options = {
            enableScripts: true,
        };
        webviewPanel.webview.html = this.getHtmlForWebview(webviewPanel.webview);

        // Load document content into DrawingAPI
        const documentData = this.parseDocument(document);
        if (documentData.elements && documentData.elements.length > 0) {
            this.drawingAPI.loadElements(documentData.elements);
        }

        // Send initial data to webview
        webviewPanel.webview.postMessage({
            type: 'init',
            data: documentData,
        });

        // Handle messages from the webview
        webviewPanel.webview.onDidReceiveMessage(
            (message) => this.handleWebviewMessage(message, document, webviewPanel),
            undefined,
            this.context.subscriptions
        );

        // Update webview when document changes
        const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument((e) => {
            if (e.document.uri.toString() === document.uri.toString()) {
                const data = this.parseDocument(document);
                // Reload DrawingAPI state
                if (data.elements && data.elements.length > 0) {
                    this.drawingAPI.loadElements(data.elements);
                } else {
                    this.drawingAPI.clearCanvas();
                }
                webviewPanel.webview.postMessage({
                    type: 'update',
                    data: data,
                });
            }
        });

        webviewPanel.onDidDispose(() => {
            changeDocumentSubscription.dispose();
            this.openDocuments.delete(document.uri.fsPath);
        });
    }

    private handleWebviewMessage(
        message: any,
        document: vscode.TextDocument,
        webviewPanel: vscode.WebviewPanel
    ) {
        switch (message.type) {
            case 'draw_circle':
                this.drawingAPI.drawCircle(message.data);
                this.updateDocument(document, this.drawingAPI.getElements());
                break;
            case 'draw_rectangle':
                this.drawingAPI.drawRectangle(message.data);
                this.updateDocument(document, this.drawingAPI.getElements());
                break;
            case 'delete_element':
                this.drawingAPI.deleteElement(message.data.id);
                this.updateDocument(document, this.drawingAPI.getElements());
                break;
            case 'clear_canvas':
                this.drawingAPI.clearCanvas();
                this.updateDocument(document, this.drawingAPI.getElements());
                break;
            case 'get_elements':
                webviewPanel.webview.postMessage({
                    type: 'elements',
                    data: this.drawingAPI.getElements(),
                });
                break;
        }
    }

    private parseDocument(document: vscode.TextDocument): any {
        const text = document.getText();
        if (!text.trim()) {
            return { elements: [] };
        }
        try {
            return JSON.parse(text);
        } catch {
            return { elements: [] };
        }
    }

    private updateDocument(document: vscode.TextDocument, elements: any[]) {
        const edit = new vscode.WorkspaceEdit();
        const data = JSON.stringify({ elements }, null, 2);
        edit.replace(
            document.uri,
            new vscode.Range(0, 0, document.lineCount, 0),
            data
        );
        vscode.workspace.applyEdit(edit);
    }

    // MCP Server Integration Methods
    public async executeDrawCommand(filePath: string, command: string, data: any): Promise<any> {
        // Get or open the document
        const document = await this.getOrOpenDocument(filePath);

        // Parse current document
        const docData = this.parseDocument(document);
        this.drawingAPI.loadElements(docData.elements || []);

        // Execute the drawing command
        let result;
        if (command === 'draw_circle') {
            result = this.drawingAPI.drawCircle(data);
        } else if (command === 'draw_rectangle') {
            result = this.drawingAPI.drawRectangle(data);
        }

        // Update the document
        this.updateDocument(document, this.drawingAPI.getElements());

        return result;
    }

    public async executeGetElements(filePath: string): Promise<any[]> {
        const document = await this.getOrOpenDocument(filePath);
        const docData = this.parseDocument(document);
        return docData.elements || [];
    }

    public async executeGetElementById(filePath: string, id: string): Promise<any | null> {
        const document = await this.getOrOpenDocument(filePath);
        const docData = this.parseDocument(document);
        const elements = docData.elements || [];
        return elements.find((elem: any) => elem.id === id) || null;
    }

    private async getOrOpenDocument(filePath: string): Promise<vscode.TextDocument> {
        // Check if document is already open
        let document = this.openDocuments.get(filePath);
        if (document) {
            return document;
        }

        // Try to find in workspace
        const uri = vscode.Uri.file(filePath);
        document = vscode.workspace.textDocuments.find(doc => doc.uri.fsPath === filePath);
        if (document) {
            this.openDocuments.set(filePath, document);
            return document;
        }

        // Open the document
        document = await vscode.workspace.openTextDocument(uri);
        this.openDocuments.set(filePath, document);
        return document;
    }

    private getHtmlForWebview(webview: vscode.Webview): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luke Editor</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #1e1e1e;
        }
        #canvas-container {
            width: 100vw;
            height: 100vh;
            position: relative;
        }
        #canvas {
            border: 1px solid #333;
            background-color: white;
            cursor: crosshair;
        }
        #toolbar {
            position: fixed;
            top: 10px;
            left: 10px;
            background-color: #252526;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #3e3e42;
            color: #cccccc;
            z-index: 1000;
        }
        button {
            margin: 5px;
            padding: 8px 12px;
            background-color: #0e639c;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1177bb;
        }
        button.active {
            background-color: #1177bb;
            border: 2px solid #ffffff;
        }
        .color-picker {
            margin: 5px;
        }
        #status {
            margin-top: 10px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div id="toolbar">
        <div>
            <label>Tool:</label>
            <button id="circle-btn" class="active">Circle</button>
            <button id="rectangle-btn">Rectangle</button>
        </div>
        <div>
            <label>Color:</label>
            <input type="color" id="color-picker" class="color-picker" value="#000000">
        </div>
        <div>
            <button id="clear-btn">Clear Canvas</button>
        </div>
        <div id="status">Tool: Circle | Color: #000000</div>
    </div>
    <div id="canvas-container">
        <canvas id="canvas" width="1200" height="800"></canvas>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let elements = [];
        let currentTool = 'circle';
        let currentColor = '#000000';

        // Update status display
        function updateStatus() {
            const status = document.getElementById('status');
            status.textContent = \`Tool: \${currentTool.charAt(0).toUpperCase() + currentTool.slice(1)} | Color: \${currentColor}\`;
        }

        // Update active button
        function setActiveTool(tool) {
            document.querySelectorAll('#toolbar button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(tool + '-btn').classList.add('active');
            currentTool = tool;
            updateStatus();
        }

        // Tool selection
        document.getElementById('circle-btn').addEventListener('click', () => {
            setActiveTool('circle');
        });
        document.getElementById('rectangle-btn').addEventListener('click', () => {
            setActiveTool('rectangle');
        });

        // Color picker
        document.getElementById('color-picker').addEventListener('change', (e) => {
            currentColor = e.target.value;
            updateStatus();
        });

        // Clear button
        document.getElementById('clear-btn').addEventListener('click', () => {
            vscode.postMessage({ type: 'clear_canvas' });
        });

        // Canvas click handler
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const id = 'elem_' + Date.now();

            if (currentTool === 'circle') {
                vscode.postMessage({
                    type: 'draw_circle',
                    data: { id, x, y, radius: 30, color: currentColor }
                });
            } else if (currentTool === 'rectangle') {
                vscode.postMessage({
                    type: 'draw_rectangle',
                    data: { id, x, y, width: 100, height: 60, color: currentColor }
                });
            }
        });

        // Render elements on canvas
        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            elements.forEach(element => {
                ctx.fillStyle = element.color || '#000000';
                ctx.strokeStyle = element.color || '#000000';

                if (element.radius !== undefined) {
                    // Circle
                    ctx.beginPath();
                    ctx.arc(element.x, element.y, element.radius, 0, 2 * Math.PI);
                    ctx.fill();
                } else if (element.width !== undefined && element.height !== undefined) {
                    // Rectangle
                    ctx.fillRect(element.x, element.y, element.width, element.height);
                }
            });
        }

        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.type) {
                case 'init':
                case 'update':
                    elements = message.data.elements || [];
                    render();
                    break;
                case 'elements':
                    console.log('Elements:', message.data);
                    break;
            }
        });

        // Initial render
        render();
    </script>
</body>
</html>`;
    }
}
