#!/bin/bash
# Blue-Green Deployment Script for CROD Delta Tracker

BLUE_PORT=8000
GREEN_PORT=8001
ACTIVE_PORT_FILE=".active_port"

# Get current active port
if [ -f "$ACTIVE_PORT_FILE" ]; then
    CURRENT_PORT=$(cat $ACTIVE_PORT_FILE)
else
    CURRENT_PORT=$BLUE_PORT
    echo $BLUE_PORT > $ACTIVE_PORT_FILE
fi

# Determine new port
if [ "$CURRENT_PORT" == "$BLUE_PORT" ]; then
    NEW_PORT=$GREEN_PORT
    OLD_PORT=$BLUE_PORT
else
    NEW_PORT=$BLUE_PORT
    OLD_PORT=$GREEN_PORT
fi

echo "🔄 Blue-Green Deployment"
echo "Current: localhost:$CURRENT_PORT"
echo "New: localhost:$NEW_PORT"

# Build new version
echo "🔨 Building new version..."
cargo build --release || exit 1

# Start new instance
echo "🚀 Starting new instance on port $NEW_PORT..."
./target/release/crod-delta-tracker --port $NEW_PORT &
NEW_PID=$!

# Wait for health check
echo "⏳ Waiting for new instance to be healthy..."
for i in {1..30}; do
    if curl -s http://localhost:$NEW_PORT/health | grep -q "healthy"; then
        echo "✅ New instance is healthy!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ New instance failed health check!"
        kill $NEW_PID
        exit 1
    fi
    sleep 1
done

# Update HAProxy or nginx config here (if using)
# For now, just update the active port file
echo $NEW_PORT > $ACTIVE_PORT_FILE

echo "✅ Deployment complete! New instance running on port $NEW_PORT"
echo ""
echo "To stop old instance on port $OLD_PORT:"
echo "  lsof -ti:$OLD_PORT | xargs kill"