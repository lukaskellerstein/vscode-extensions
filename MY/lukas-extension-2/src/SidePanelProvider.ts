import * as vscode from "vscode";

export class SidePanelProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = "lukas-extension-2.sidePanel";
  private _view?: vscode.WebviewView;

  constructor(private readonly _extensionUri: vscode.Uri) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    // Handle messages from the webview
    webviewView.webview.onDidReceiveMessage((data) => {
      switch (data.type) {
        case "colorSelected":
          vscode.window.showInformationMessage(`Color selected: ${data.value}`);
          break;
        case "buttonClicked":
          vscode.window.showInformationMessage("Button was clicked!");
          break;
      }
    });
  }

  private _getHtmlForWebview(webview: vscode.Webview) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Side Panel</title>
    <style>
        body {
            padding: 10px;
            color: var(--vscode-foreground);
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
        }

        .container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .section {
            padding: 10px;
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            background-color: var(--vscode-editor-background);
        }

        h2 {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: var(--vscode-foreground);
        }

        button {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 8px 16px;
            cursor: pointer;
            border-radius: 2px;
            font-size: 13px;
            width: 100%;
        }

        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 6px;
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 2px;
            box-sizing: border-box;
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
        }

        input[type="text"]:focus, textarea:focus {
            outline: 1px solid var(--vscode-focusBorder);
        }

        textarea {
            min-height: 100px;
            resize: vertical;
        }

        .info {
            margin-top: 5px;
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
        }

        .color-picker {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .color-box {
            width: 30px;
            height: 30px;
            border-radius: 4px;
            cursor: pointer;
            border: 2px solid transparent;
        }

        .color-box:hover {
            border-color: var(--vscode-focusBorder);
        }

        .label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="section">
            <h2>Welcome</h2>
            <p>This is a custom side panel for lukas-extension-2.</p>
            <div class="info">You can add any custom UI components here.</div>
        </div>

        <div class="section">
            <h2>Quick Actions</h2>
            <button id="actionButton">Click Me</button>
        </div>

        <div class="section">
            <h2>Input Example</h2>
            <label class="label">Enter some text:</label>
            <input type="text" id="textInput" placeholder="Type something...">
        </div>

        <div class="section">
            <h2>Text Area Example</h2>
            <label class="label">Enter multiple lines:</label>
            <textarea id="textArea" placeholder="Enter multiple lines here..."></textarea>
        </div>

        <div class="section">
            <h2>Color Picker</h2>
            <label class="label">Select a color:</label>
            <div class="color-picker">
                <div class="color-box" style="background-color: #e74c3c;" data-color="#e74c3c"></div>
                <div class="color-box" style="background-color: #3498db;" data-color="#3498db"></div>
                <div class="color-box" style="background-color: #2ecc71;" data-color="#2ecc71"></div>
                <div class="color-box" style="background-color: #f39c12;" data-color="#f39c12"></div>
                <div class="color-box" style="background-color: #9b59b6;" data-color="#9b59b6"></div>
                <div class="color-box" style="background-color: #1abc9c;" data-color="#1abc9c"></div>
            </div>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();

        // Handle button click
        document.getElementById('actionButton').addEventListener('click', () => {
            vscode.postMessage({
                type: 'buttonClicked'
            });
        });

        // Handle color selection
        document.querySelectorAll('.color-box').forEach(box => {
            box.addEventListener('click', (e) => {
                const color = e.target.getAttribute('data-color');
                vscode.postMessage({
                    type: 'colorSelected',
                    value: color
                });
            });
        });

        // You can also handle input changes if needed
        document.getElementById('textInput').addEventListener('input', (e) => {
            // Handle input changes
            console.log('Input value:', e.target.value);
        });
    </script>
</body>
</html>`;
  }

  // Method to send messages to the webview
  public sendMessage(message: any) {
    if (this._view) {
      this._view.webview.postMessage(message);
    }
  }
}
