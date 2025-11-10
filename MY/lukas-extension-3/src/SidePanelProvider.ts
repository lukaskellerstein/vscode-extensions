import * as vscode from "vscode";
import * as path from "path";

export class SidePanelProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = "lukas-extension-3.sidePanel";
  private _view?: vscode.WebviewView;

  constructor(
    private readonly _extensionUri: vscode.Uri,
    private readonly _extensionPath: string
  ) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    console.log("[SidePanelProvider] Resolving webview view");
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    try {
      webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
      console.log("[SidePanelProvider] HTML set successfully");
    } catch (error) {
      console.error("[SidePanelProvider] Error setting HTML:", error);
      vscode.window.showErrorMessage(`Failed to load webview: ${error}`);
    }

    // Handle messages from the webview
    webviewView.webview.onDidReceiveMessage((data) => {
      console.log("[SidePanelProvider] Received message:", data);
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
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.file(path.join(this._extensionPath, "out", "webview", "index.js"))
    );

    console.log("[SidePanelProvider] Script URI:", scriptUri.toString());

    // Use a nonce to only allow specific scripts to be run
    const nonce = getNonce();

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';">
    <title>React Side Panel</title>
</head>
<body>
    <div id="root"></div>
    <script nonce="${nonce}" src="${scriptUri}"></script>
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

function getNonce() {
  let text = "";
  const possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (let i = 0; i < 32; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}
