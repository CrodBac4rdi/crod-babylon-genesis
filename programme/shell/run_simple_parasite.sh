#!/bin/bash

echo "🦠 Starting Simple CROD Parasite..."

docker run --rm -it \
  --name simple-parasite \
  --network host \
  -v $(pwd):/app \
  -w /app \
  python:3.11-alpine \
  sh -c "pip install flask numpy requests && python simple_parasite.py"