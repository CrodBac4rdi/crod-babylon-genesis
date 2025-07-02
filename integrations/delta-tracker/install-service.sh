#!/bin/bash
# Install systemd service for CROD Delta Tracker

SERVICE_NAME="crod-delta-tracker@$USER"
SERVICE_FILE="crod-delta-tracker.service"

echo "📦 Installing CROD Delta Tracker as systemd service..."

# Copy service file
sudo cp $SERVICE_FILE /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable $SERVICE_NAME

# Start service
sudo systemctl start $SERVICE_NAME

echo "✅ Service installed!"
echo ""
echo "Commands:"
echo "  sudo systemctl status $SERVICE_NAME"
echo "  sudo systemctl stop $SERVICE_NAME"
echo "  sudo systemctl restart $SERVICE_NAME"
echo "  sudo journalctl -u $SERVICE_NAME -f"