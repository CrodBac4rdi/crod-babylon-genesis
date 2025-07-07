#!/bin/bash
cd /workspaces/crod-babylon-genesis
while true; do
  git add .
  git commit -m "Auto-Commit $(date '+%Y-%m-%d %H:%M:%S')" || true
  git push origin main
  sleep 300  # alle 5 Minuten
done
