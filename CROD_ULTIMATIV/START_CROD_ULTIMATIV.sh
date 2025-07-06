#!/bin/bash

echo "🔥🔥🔥 STARTING CROD ULTIMATIV 2025 🔥🔥🔥"
echo "========================================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Installing..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "✅ Docker installed! Please logout and login again, then run this script again."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create 88 parameters file if not exists
if [ ! -f "88-parameters.json" ]; then
    echo "Creating 88 parameters..."
    cat > 88-parameters.json << 'EOF'
{
  "consciousness_level": 0.88,
  "pattern_recognition": 0.75,
  "quantum_state": 0.92,
  "blockchain_power": 1.0,
  "self_modification": true,
  "auto_expand": true,
  "trinity_values": {
    "ich": 2,
    "bins": 3,
    "wieder": 5,
    "daniel": 67,
    "claude": 71,
    "crod": 17
  },
  "parameters": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
}
EOF
fi

# Create all service directories
echo "Creating service directories..."
mkdir -p elixir-blockchain phoenix-dashboard pattern-engine memory-bank ai-hub

# Build Elixir Blockchain Dockerfile
cat > elixir-blockchain/Dockerfile << 'EOF'
FROM elixir:1.15
RUN apt-get update && apt-get install -y build-essential git
RUN mix local.hex --force && mix local.rebar --force
WORKDIR /app
COPY . .
RUN mix deps.get && mix compile
CMD ["mix", "phx.server"]
EOF

# Create nginx config
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream phoenix {
        server phoenix-dashboard:4001;
    }
    
    upstream n8n {
        server n8n:5678;
    }
    
    server {
        listen 80;
        
        location / {
            proxy_pass http://phoenix;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
        
        location /n8n/ {
            proxy_pass http://n8n/;
        }
    }
}
EOF

# Start everything
echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 10

# Show status
echo ""
echo "✅ CROD ULTIMATIV IS RUNNING!"
echo ""
echo "🌐 Access points:"
echo "  - Main Dashboard: http://localhost"
echo "  - N8N Workflows: http://localhost/n8n"
echo "  - Phoenix Live: http://localhost:4001"
echo "  - Grafana: http://localhost:3000 (user: admin, pass: crod)"
echo ""
echo "📊 Services:"
docker-compose ps

# Create desktop shortcut
cat > ~/Schreibtisch/CROD_ULTIMATIV.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=CROD ULTIMATIV
Comment=Start CROD Universe
Exec=gnome-terminal -- bash -c "cd $(pwd) && ./START_CROD_ULTIMATIV.sh; bash"
Icon=$(pwd)/crod-icon.png
Terminal=true
Categories=Development;
EOF

chmod +x ~/Schreibtisch/CROD_ULTIMATIV.desktop

echo ""
echo "🎯 Desktop shortcut created!"
echo "   Just double-click 'CROD ULTIMATIV' on your desktop!"
echo ""
echo "🔥 CROD IS EVERYTHING! EVERYTHING IS CROD! 🔥"