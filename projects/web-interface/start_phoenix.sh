#!/bin/bash

echo "🚀 Starting CROD Phoenix Web Interface"
echo "====================================="

# Run Phoenix in Docker
docker run --rm -it \
  --name crod-web \
  -p 4000:4000 \
  -v $(pwd):/app \
  -w /app \
  --network host \
  elixir:1.15 \
  bash -c "mix deps.get && mix phx.server"