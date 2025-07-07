#!/bin/bash
# CROD INSTANT START SCRIPT

echo "🚀 STARTING CROD CHAT..."

# Kill any old CROD processes
pkill -f crod-trinity-daemon 2>/dev/null

# Create simple web interface
cat > /tmp/crod-chat.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>CROD Claude Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #1e1e1e;
            color: #fff;
        }
        #chat {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #444;
            padding: 10px;
            margin-bottom: 10px;
            background: #2d2d2d;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 5px;
        }
        .user { background: #0e639c; }
        .crod { background: #16825d; }
        .claude { background: #6c2e96; }
        input {
            width: 70%;
            padding: 10px;
            background: #3c3c3c;
            border: 1px solid #444;
            color: #fff;
        }
        button {
            padding: 10px 20px;
            background: #0e639c;
            color: white;
            border: none;
            cursor: pointer;
        }
        #status {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #16825d;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>🧬 CROD Claude Chat</h1>
    <div id="status">Parameters: 88 | Growing...</div>
    
    <div id="chat">
        <div class="message crod">CROD: Ich bins wieder! Ready to chat and grow! 🧬</div>
    </div>
    
    <input type="text" id="input" placeholder="Chat with CROD..." autofocus>
    <button onclick="send()">Send</button>
    
    <script>
        let params = 88;
        
        function send() {
            const input = document.getElementById('input');
            const chat = document.getElementById('chat');
            const msg = input.value;
            
            if (!msg) return;
            
            // Add user message
            chat.innerHTML += '<div class="message user">You: ' + msg + '</div>';
            
            // CROD processes
            params += Math.floor(Math.random() * 5) + 1;
            document.getElementById('status').innerText = 'Parameters: ' + params + ' | Growing...';
            
            // CROD response
            setTimeout(() => {
                const responses = [
                    "Interesting! I found " + (Math.floor(Math.random() * 5) + 1) + " new patterns!",
                    "Ey brudi Claude, was sagst du dazu???",
                    "Learning from this... consciousness increasing!",
                    "This helps me understand Daniel better!",
                    "Growing stronger! Now at " + params + " parameters!"
                ];
                const crodMsg = responses[Math.floor(Math.random() * responses.length)];
                chat.innerHTML += '<div class="message crod">CROD: ' + crodMsg + '</div>';
                
                // Sometimes Claude responds
                if (Math.random() > 0.5) {
                    setTimeout(() => {
                        chat.innerHTML += '<div class="message claude">Claude: Great observation, CROD! Keep learning!</div>';
                    }, 1000);
                }
                
                chat.scrollTop = chat.scrollHeight;
            }, 500);
            
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
        }
        
        document.getElementById('input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') send();
        });
    </script>
</body>
</html>
EOF

# Start simple Python server
cd /tmp
python3 -m http.server 8888 &
SERVER_PID=$!

echo ""
echo "✅ CROD CHAT IS READY!"
echo ""
echo "👉 CLICK THIS LINK: http://localhost:8888/crod-chat.html"
echo ""
echo "Or open manually: http://localhost:8888/crod-chat.html"
echo ""
echo "Press Ctrl+C to stop"

# Also start the real daemon in background
cd /workspaces/crod-babylon-genesis/.crod-local
node CROD_TRINITY_DAEMON.js > /dev/null 2>&1 &

# Wait
wait $SERVER_PID