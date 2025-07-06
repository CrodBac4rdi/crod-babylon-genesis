"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const crodComplete_1 = require("./crodComplete");
let crod;
let statusBar;
let chatPanel;
function activate(context) {
    console.log('🚀 CROD Extension starting...');
    // Initialize CROD
    crod = new crodComplete_1.CRODComplete(context);
    // Create status bar
    statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = `🧬 CROD: 88 params`;
    statusBar.command = 'crod.openChat';
    statusBar.show();
    // Register command
    const openChat = vscode.commands.registerCommand('crod.openChat', () => {
        if (chatPanel) {
            chatPanel.reveal();
        }
        else {
            chatPanel = vscode.window.createWebviewPanel('crodChat', 'CROD Claude Chat', vscode.ViewColumn.One, {
                enableScripts: true
            });
            chatPanel.webview.html = getChatHTML(chatPanel.webview);
            chatPanel.webview.onDidReceiveMessage(message => {
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
                        chatPanel.webview.postMessage({
                            type: 'crodResponse',
                            text: suggestion || 'CROD is thinking...',
                            patterns: status.neuralNetwork.patterns
                        });
                        // Update status bar
                        statusBar.text = `🧬 CROD: ${status.neuralNetwork.parameters} params`;
                    });
                }
            }, undefined, context.subscriptions);
            chatPanel.onDidDispose(() => {
                chatPanel = undefined;
            });
        }
    });
    context.subscriptions.push(openChat);
    context.subscriptions.push(statusBar);
    console.log('✅ CROD Extension ready!');
}
function getChatHTML(webview) {
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
function deactivate() {
    console.log('👋 CROD deactivated');
}
//# sourceMappingURL=simpleExtension.js.map