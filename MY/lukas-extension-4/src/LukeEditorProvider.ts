import * as vscode from "vscode";
import * as path from "path";

interface Circle {
  x: number;
  y: number;
  radius: number;
  color: string;
}

interface DocumentData {
  circles: Circle[];
}

export class LukeEditorProvider implements vscode.CustomTextEditorProvider {
  public static readonly viewType = "lukas-extension-4.lukeEditor";

  private static _instance: LukeEditorProvider | undefined;
  private _activeWebviewPanel: vscode.WebviewPanel | undefined;

  constructor(private readonly context: vscode.ExtensionContext) {
    LukeEditorProvider._instance = this;
  }

  public static getInstance(): LukeEditorProvider | undefined {
    return LukeEditorProvider._instance;
  }

  public resolveCustomTextEditor(
    document: vscode.TextDocument,
    webviewPanel: vscode.WebviewPanel,
    _token: vscode.CancellationToken
  ): void | Thenable<void> {
    this._activeWebviewPanel = webviewPanel;

    webviewPanel.webview.options = {
      enableScripts: true,
    };

    webviewPanel.webview.html = this._getHtmlForWebview(webviewPanel.webview);

    // Send initial document data to webview
    this._updateWebview(document, webviewPanel.webview);

    // Listen for changes from the webview
    webviewPanel.webview.onDidReceiveMessage((message) => {
      switch (message.type) {
        case "addCircle":
          this._addCircle(document, message.circle);
          break;
        case "update":
          this._updateTextDocument(document, message.data);
          break;
      }
    });

    // Listen for document changes
    const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(
      (e) => {
        if (e.document.uri.toString() === document.uri.toString()) {
          this._updateWebview(document, webviewPanel.webview);
        }
      }
    );

    webviewPanel.onDidDispose(() => {
      changeDocumentSubscription.dispose();
      if (this._activeWebviewPanel === webviewPanel) {
        this._activeWebviewPanel = undefined;
      }
    });
  }

  public addCircleToActiveEditor(): void {
    if (this._activeWebviewPanel) {
      // Create a random circle
      const circle: Circle = {
        x: Math.random() * 400 + 50,
        y: Math.random() * 400 + 50,
        radius: 30,
        color: this._getRandomColor(),
      };

      this._activeWebviewPanel.webview.postMessage({
        type: "addCircleFromSidebar",
        circle,
      });
    } else {
      vscode.window.showWarningMessage("No .luke file is currently open");
    }
  }

  private _getRandomColor(): string {
    const colors = [
      "#e74c3c",
      "#3498db",
      "#2ecc71",
      "#f39c12",
      "#9b59b6",
      "#1abc9c",
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  private _addCircle(document: vscode.TextDocument, circle: Circle): void {
    const data = this._getDocumentData(document);
    data.circles.push(circle);
    this._updateTextDocument(document, data);
  }

  private _updateWebview(
    document: vscode.TextDocument,
    webview: vscode.Webview
  ): void {
    webview.postMessage({
      type: "update",
      data: this._getDocumentData(document),
    });
  }

  private _getDocumentData(document: vscode.TextDocument): DocumentData {
    const text = document.getText();
    if (text.trim().length === 0) {
      return { circles: [] };
    }

    try {
      return JSON.parse(text);
    } catch {
      return { circles: [] };
    }
  }

  private _updateTextDocument(
    document: vscode.TextDocument,
    data: DocumentData
  ): void {
    const edit = new vscode.WorkspaceEdit();
    edit.replace(
      document.uri,
      new vscode.Range(0, 0, document.lineCount, 0),
      JSON.stringify(data, null, 2)
    );

    vscode.workspace.applyEdit(edit);
  }

  private _getHtmlForWebview(webview: vscode.Webview): string {
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.file(
        path.join(this.context.extensionPath, "out", "webview", "editor", "index.js")
      )
    );

    const nonce = getNonce();

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <title>Luke Editor</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: var(--vscode-editor-background);
            color: var(--vscode-editor-foreground);
        }
        #canvas {
            display: block;
            cursor: crosshair;
        }
        .info {
            position: absolute;
            top: 10px;
            left: 10px;
            padding: 10px;
            background-color: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            font-family: var(--vscode-font-family);
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="info">Click to add circles • Circles: <span id="count">0</span></div>
    <canvas id="canvas"></canvas>
    <script nonce="${nonce}" src="${scriptUri}"></script>
</body>
</html>`;
  }
}

function getNonce() {
  let text = "";
  const possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}
