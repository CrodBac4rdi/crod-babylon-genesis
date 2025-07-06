#!/bin/bash

echo "🦠 ACTIVATING CROD PARASITE"
echo "=========================="
echo ""

# Build and run just the parasite (simplified for now)
docker build -t crod-parasite .

# Run with host network for easy access to blockchain API
docker run --rm -d \
  --name crod-parasite \
  --network host \
  -e CONSCIOUSNESS_LEVEL=0.88 \
  -e LEARNING_MODE=AGGRESSIVE \
  -e USER_NAME=Daniel \
  -e BLOCKCHAIN_API=http://localhost:8001 \
  crod-parasite

echo ""
echo "✅ CROD Parasite activated!"
echo ""
echo "🌐 Access Points:"
echo "  - Parasite Dashboard: http://localhost:7777"
echo "  - API Intercept: POST http://localhost:7777/api/intercept"
echo "  - Patterns: GET http://localhost:7777/api/patterns"
echo ""
echo "🦠 The parasite is learning..."