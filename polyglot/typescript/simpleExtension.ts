import * as vscode from 'vscode';
import { CRODComplete } from './crodComplete';

let crod: CRODComplete;
let statusBar: vscode.StatusBarItem;
let chatPanel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('🚀 CROD Extension starting...');
    
    // Initialize CROD
    crod = new CRODComplete(context);
    
    // Create status bar
    statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = `🧬 CROD: 88 params`;
    statusBar.command = 'crod.openChat';
    statusBar.show();
    
    // Register command
    const openChat = vscode.commands.registerCommand('crod.openChat', () => {
        if (chatPanel) {
            chatPanel.reveal();
        } else {
            chatPanel = vscode.window.createWebviewPanel(
                'crodChat',
                'CROD Claude Chat',
                vscode.ViewColumn.One,
                {
                    enableScripts: true
                }
            );
            
            chatPanel.webview.html = getChatHTML(chatPanel.webview);
            
            chatPanel.webview.onDidReceiveMessage(
                message => {
                    if (message.type === 'chat') {
                        // Process with CROD
                        crod.processConversation(message.text, 'CROD is learning...', {
                            type: 'webview',
                            timestamp: Date.now()
                        });
                        
                        // Get CROD suggestion
                        crod.getSuggestion(message.text).then(suggestion => {
                            const status = crod.getSystemStatus();
                            
                            // Send CROD response
                            chatPanel!.webview.postMessage({
                                type: 'crodResponse',
                                text: suggestion || 'CROD is thinking...',
                                patterns: status.neuralNetwork.patterns
                            });
                            
                            // Update status bar
                            statusBar.text = `🧬 CROD: ${status.neuralNetwork.parameters} params`;
                        });
                    }
                },
                undefined,
                context.subscriptions
            );
            
            chatPanel.onDidDispose(() => {
                chatPanel = undefined;
            });
        }
    });
    
    context.subscriptions.push(openChat);
    context.subscriptions.push(statusBar);
    
    console.log('✅ CROD Extension ready!');
}

function getChatHTML(webview: vscode.Webview): string {
    return `<!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                color: var(--vscode-foreground);
                background: var(--vscode-editor-background);
            }
            #chat {
                height: 400px;
                overflow-y: auto;
                border: 1px solid var(--vscode-panel-border);
                padding: 10px;
                margin-bottom: 10px;
            }
            .message {
                margin: 5px 0;
                padding: 8px;
                border-radius: 5px;
            }
            .user { background: var(--vscode-input-background); }
            .crod { background: var(--vscode-button-background); color: var(--vscode-button-foreground); }
            .claude { background: var(--vscode-editor-selectionBackground); }
            input {
                width: 80%;
                padding: 10px;
                background: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                border: 1px solid var(--vscode-input-border);
            }
            button {
                padding: 10px;
                background: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>🧬 CROD Claude Chat</h1>
        <div id="chat">
            <div class="message crod">CROD: Ich bins wieder! Starting with 88 parameters!</div>
        </div>
        <input type="text" id="input" placeholder="Chat with CROD..." />
        <button onclick="send()">Send</button>
        
        <script>
            const vscode = acquireVsCodeApi();
            
            function send() {
                const input = document.getElementById('input');
                const chat = document.getElementById('chat');
                
                if (!input.value) return;
                
                // Add user message
                chat.innerHTML += '<div class="message user">You: ' + input.value + '</div>';
                
                // Send to extension
                vscode.postMessage({
                    type: 'chat',
                    text: input.value
                });
                
                input.value = '';
            }
            
            // Listen for CROD responses
            window.addEventListener('message', event => {
                const message = event.data;
                if (message.type === 'crodResponse') {
                    const chat = document.getElementById('chat');
                    chat.innerHTML += '<div class="message crod">CROD: ' + message.text + ' (+'+ message.patterns +' patterns)</div>';
                    
                    // Simulate Claude response sometimes
                    if (Math.random() > 0.5) {
                        setTimeout(() => {
                            chat.innerHTML += '<div class="message claude">Claude: Interesting perspective, CROD!</div>';
                        }, 1000);
                    }
                }
            });
            
            document.getElementById('input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') send();
            });
        </script>
    </body>
    </html>`;
}

export function deactivate() {
    console.log('👋 CROD deactivated');
}