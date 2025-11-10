import * as vscode from "vscode";
import { SidePanelProvider } from "./SidePanelProvider";

export function activate(context: vscode.ExtensionContext) {
  console.log(
    'Congratulations, your extension "lukas-extension-3" is now active!'
  );

  // Register the side panel provider
  const provider = new SidePanelProvider(
    context.extensionUri,
    context.extensionPath
  );
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      SidePanelProvider.viewType,
      provider
    )
  );

  // Register hello world command
  const disposable = vscode.commands.registerCommand(
    "lukas-extension-3.helloWorld",
    () => {
      vscode.window.showInformationMessage(
        "Hello World from lukas-extension-3!"
      );
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {}
