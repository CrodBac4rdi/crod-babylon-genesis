#!/bin/bash

echo "🚀 Running CROD Blockchain in Docker"
echo "===================================="

# Run the simple test in Docker
docker run --rm -it \
  -v $(pwd):/app \
  -w /app \
  elixir:1.15-alpine \
  elixir simple_blockchain_test.exs