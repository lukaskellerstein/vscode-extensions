import * as vscode from 'vscode';
import { WebSocketServer, WebSocket } from 'ws';
import { LukeEditorProvider } from './lukeEditorProvider';

export class WsServer {
    private server: WebSocketServer | null = null;
    private port: number = 0;
    private editorProvider: LukeEditorProvider | null = null;
    private clients: Set<WebSocket> = new Set();

    constructor(private readonly context: vscode.ExtensionContext) {}

    setEditorProvider(provider: LukeEditorProvider) {
        this.editorProvider = provider;
    }

    async start(): Promise<number> {
        return new Promise((resolve, reject) => {
            // Create WebSocket server on random available port
            this.server = new WebSocketServer({ port: 0 });

            this.server.on('listening', () => {
                const address = this.server!.address();
                if (address && typeof address !== 'string') {
                    this.port = address.port;
                    console.log(`MCP WebSocket Server listening on port ${this.port}`);

                    // Write port to /tmp so MCP server can discover it
                    const fs = require('fs');
                    const portFilePath = '/tmp/luke_editor_mcp_port.txt';
                    fs.writeFileSync(portFilePath, this.port.toString());

                    resolve(this.port);
                } else {
                    reject(new Error('Failed to get server address'));
                }
            });

            this.server.on('connection', (ws: WebSocket) => {
                console.log('MCP server connected');
                this.clients.add(ws);

                ws.on('message', async (data: Buffer) => {
                    try {
                        const message = JSON.parse(data.toString());
                        const result = await this.handleCommand(message);

                        ws.send(JSON.stringify({
                            success: true,
                            result: result
                        }));
                    } catch (error) {
                        console.error('Error handling MCP command:', error);
                        ws.send(JSON.stringify({
                            success: false,
                            error: error instanceof Error ? error.message : 'Internal server error'
                        }));
                    }
                });

                ws.on('close', () => {
                    console.log('MCP server disconnected');
                    this.clients.delete(ws);
                });

                ws.on('error', (error: Error) => {
                    console.error('WebSocket error:', error);
                    this.clients.delete(ws);
                });
            });

            this.server.on('error', reject);
        });
    }

    stop() {
        // Close all client connections
        this.clients.forEach(ws => {
            ws.close();
        });
        this.clients.clear();

        // Close server
        if (this.server) {
            this.server.close();
            this.server = null;
        }
    }

    // Broadcast updates to all connected MCP servers (for future use)
    broadcast(message: any) {
        const data = JSON.stringify(message);
        this.clients.forEach(ws => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(data);
            }
        });
    }

    private async handleCommand(command: any): Promise<any> {
        if (!this.editorProvider) {
            throw new Error('Editor provider not initialized');
        }

        const { type, file_path, data } = command;

        switch (type) {
            case 'get_active_file':
                // Return the currently active .luke file
                const activeFile = this.editorProvider.getCurrentActiveFile();
                if (!activeFile) {
                    throw new Error('No .luke file is currently open. Please open a .luke file first.');
                }
                return { file_path: activeFile };

            case 'set_file':
                // Open the file in the editor
                const uri = vscode.Uri.file(file_path);
                await vscode.window.showTextDocument(uri);
                this.editorProvider.setCurrentActiveFile(file_path);
                return { status: 'success', file_path };

            case 'draw_circle':
                return await this.editorProvider.executeDrawCommand(file_path, 'draw_circle', data);

            case 'draw_rectangle':
                return await this.editorProvider.executeDrawCommand(file_path, 'draw_rectangle', data);

            case 'get_elements':
                return await this.editorProvider.executeGetElements(file_path);

            case 'get_element_by_id':
                return await this.editorProvider.executeGetElementById(file_path, data.id);

            default:
                throw new Error(`Unknown command type: ${type}`);
        }
    }
}
