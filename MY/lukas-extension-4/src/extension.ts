import * as vscode from "vscode";
import { SidePanelProvider } from "./SidePanelProvider";
import { LukeEditorProvider } from "./LukeEditorProvider";

export function activate(context: vscode.ExtensionContext) {
  console.log(
    'Congratulations, your extension "lukas-extension-4" is now active!'
  );

  // Register the custom editor provider for .luke files
  const lukeEditorProvider = new LukeEditorProvider(context);
  context.subscriptions.push(
    vscode.window.registerCustomEditorProvider(
      LukeEditorProvider.viewType,
      lukeEditorProvider,
      {
        webviewOptions: {
          retainContextWhenHidden: true,
        },
      }
    )
  );

  // Register the side panel provider
  const sidePanelProvider = new SidePanelProvider(
    context.extensionUri,
    context.extensionPath
  );
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      SidePanelProvider.viewType,
      sidePanelProvider
    )
  );

  // Register hello world command
  const disposable = vscode.commands.registerCommand(
    "lukas-extension-4.helloWorld",
    () => {
      vscode.window.showInformationMessage(
        "Hello World from lukas-extension-4!"
      );
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {}
