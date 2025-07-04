#!/bin/bash
# Setup Redis Pub/Sub for Polyglot City Districts

echo "🔴 Setting up Redis Pub/Sub for district communication..."

# Redis channels for each district
CHANNELS=(
    "meta-chain:events"
    "pattern-district:events"
    "memory-quarter:events"
    "intelligence-hub:events"
    "gateway:events"
    "crod-core:events"
)

# Create Redis Pub/Sub bridge
cat > /tmp/redis-pubsub-bridge.js <<'EOF'
const Redis = require('redis');

class DistrictBridge {
    constructor() {
        this.publisher = Redis.createClient({ host: 'localhost', port: 6379 });
        this.subscriber = Redis.createClient({ host: 'localhost', port: 6379 });
        
        this.channels = [
            'meta-chain:events',
            'pattern-district:events', 
            'memory-quarter:events',
            'intelligence-hub:events',
            'gateway:events',
            'crod-core:events'
        ];
    }
    
    async connect() {
        await this.publisher.connect();
        await this.subscriber.connect();
        
        // Subscribe to all channels
        for (const channel of this.channels) {
            await this.subscriber.subscribe(channel, (message) => {
                console.log(`[${channel}] ${message}`);
                this.routeMessage(channel, message);
            });
        }
        
        console.log('🌉 District Bridge Active!');
    }
    
    routeMessage(fromChannel, message) {
        const data = JSON.parse(message);
        
        // Route based on message type
        switch(data.type) {
            case 'pattern_discovered':
                // Send to Intelligence Hub for analysis
                this.publisher.publish('intelligence-hub:events', message);
                break;
                
            case 'memory_stored':
                // Send to Pattern District for pattern extraction
                this.publisher.publish('pattern-district:events', message);
                break;
                
            case 'consciousness_update':
                // Broadcast to all districts
                this.channels.forEach(channel => {
                    if (channel !== fromChannel) {
                        this.publisher.publish(channel, message);
                    }
                });
                break;
        }
    }
}

// Start bridge
const bridge = new DistrictBridge();
bridge.connect().catch(console.error);
EOF

# Create systemd service
sudo tee /etc/systemd/system/crod-pubsub-bridge.service <<EOF
[Unit]
Description=CROD Redis Pub/Sub Bridge
After=redis.service

[Service]
Type=simple
ExecStart=/usr/bin/node /tmp/redis-pubsub-bridge.js
Restart=on-failure
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# Install Redis if not present
if ! command -v redis-cli &> /dev/null; then
    echo "📦 Installing Redis..."
    sudo apt update
    sudo apt install -y redis-server redis-tools
fi

# Configure Redis for Pub/Sub optimization
sudo tee -a /etc/redis/redis.conf <<EOF

# CROD Pub/Sub Optimizations
tcp-keepalive 60
timeout 0
tcp-backlog 511
maxclients 10000

# Enable keyspace notifications
notify-keyspace-events "AKE"
EOF

# Restart Redis
sudo systemctl restart redis

echo "✅ Redis Pub/Sub configured!"
echo ""
echo "📡 District Communication Channels:"
for channel in "${CHANNELS[@]}"; do
    echo "   - $channel"
done
echo ""
echo "🚀 Start bridge: sudo systemctl start crod-pubsub-bridge"