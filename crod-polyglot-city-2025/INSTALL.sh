#!/bin/bash
# CROD Polyglot City 2025 - Installation Script

echo "🏛️ Installing CROD Polyglot City 2025..."

# Install NATS
echo "📦 Installing NATS..."
wget https://github.com/nats-io/nats-server/releases/download/v2.10.7/nats-server-v2.10.7-linux-amd64.tar.gz
tar -xzf nats-server-v2.10.7-linux-amd64.tar.gz
sudo cp nats-server-v2.10.7-linux-amd64/nats-server /usr/local/bin/
rm -rf nats-server-v2.10.7-linux-amd64*

# Create directory structure
mkdir -p crod-{rathaus-phoenix,parasit-python,pattern-rust,memory-go,gateway-js}

echo "✅ Base installation complete!"
echo "🚀 Ready to build districts!"