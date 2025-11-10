// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as fs from "fs/promises";
import * as vscode from "vscode";

async function readFiles(selectedUris: vscode.Uri[]): Promise<string> {
  const separator = "\n" + "=".repeat(70) + "\n";
  const contents: string[] = [];

  for (const fileUri of selectedUris) {
    try {
      const data = await fs.readFile(fileUri.fsPath, "utf-8");
      contents.push(data);
    } catch (err) {
      vscode.window.showErrorMessage(`Failed to read ${fileUri.fsPath}`);
    }
  }

  return separator + contents.join(separator) + separator;
}

export function activate(context: vscode.ExtensionContext) {
  const formatCmd = vscode.commands.registerCommand(
    "extension.formatForLLM",
    async (uri: vscode.Uri, selectedUris: vscode.Uri[]) => {
      const files = selectedUris || [uri];
      const result = await readFiles(files);

      const doc = await vscode.workspace.openTextDocument({
        content: result,
        language: "plaintext",
      });
      await vscode.window.showTextDocument(doc);
    }
  );

  const copyCmd = vscode.commands.registerCommand(
    "extension.copyForLLM",
    async (uri: vscode.Uri, selectedUris: vscode.Uri[]) => {
      const files = selectedUris || [uri];
      const result = await readFiles(files);

      await vscode.env.clipboard.writeText(result);
      vscode.window.showInformationMessage(
        "LLM-formatted text copied to clipboard!"
      );
    }
  );

  context.subscriptions.push(formatCmd, copyCmd);
}

// This method is called when your extension is deactivated
export function deactivate() {}
