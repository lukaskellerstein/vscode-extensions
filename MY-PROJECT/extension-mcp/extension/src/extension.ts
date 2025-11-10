import * as vscode from 'vscode';
import { LukeEditorProvider } from './lukeEditorProvider';
import { WsServer } from './wsServer';

let mcpServer: WsServer | null = null;

export async function activate(context: vscode.ExtensionContext) {
    console.log('Luke Editor extension is now active');

    // Register the custom editor provider
    context.subscriptions.push(
        LukeEditorProvider.register(context)
    );

    // Start MCP WebSocket server
    mcpServer = new WsServer(context);
    const provider = LukeEditorProvider.getInstance();
    if (provider) {
        mcpServer.setEditorProvider(provider);
    }

    try {
        const port = await mcpServer.start();
        console.log(`MCP WebSocket Server started on port ${port}`);
        vscode.window.showInformationMessage(`Luke Editor MCP server running on port ${port}`);
    } catch (error) {
        console.error('Failed to start MCP WebSocket server:', error);
        vscode.window.showErrorMessage('Failed to start Luke Editor MCP server');
    }
}

export function deactivate() {
    if (mcpServer) {
        mcpServer.stop();
        mcpServer = null;
    }
}
