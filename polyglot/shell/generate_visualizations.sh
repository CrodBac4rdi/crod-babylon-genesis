#!/bin/bash
# Generate CROD visualizations

# Create assets directory if it doesn't exist
mkdir -p ../assets/generated

# Install required packages if not already installed
pip install matplotlib numpy

# Run the visualizer
python crod_visualizer.py

echo "Visualizations generated successfully!"
