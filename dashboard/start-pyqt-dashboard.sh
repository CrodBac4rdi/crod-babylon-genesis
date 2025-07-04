#!/bin/bash

echo "🚀 Starting CROD PyQt Dashboard..."

cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7/dashboard

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
pip install -r requirements.txt

# Run dashboard
python crod_dashboard.py