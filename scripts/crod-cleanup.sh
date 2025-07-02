#!/bin/bash

# CROD CLEANUP - Räumt auf!

echo "🧹 CROD Cleanup starting..."

# 1. Clean up duplicate deployments
echo "📦 Removing duplicate deployments..."
cs kubectl delete deployment meta-chain pattern-district memory-quarter intelligence-hub gateway -n crod-polyglot 2>/dev/null

# 2. Clean failed pods
echo "🗑️ Removing failed pods..."
cs kubectl delete pods --field-selector=status.phase=Failed -n crod-polyglot

# 3. Clean old images
echo "🐳 Cleaning old Docker images..."
docker image prune -f

# 4. Organize files
echo "📁 Organizing project structure..."
cd "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7"

# Create organized structure
mkdir -p {scripts/{builders,runners,helpers},deployments,backups,logs}

# Move scripts to categories
mv scripts/*-build*.sh scripts/builders/ 2>/dev/null
mv scripts/*-run*.sh scripts/runners/ 2>/dev/null
mv scripts/*-helper*.sh scripts/helpers/ 2>/dev/null

echo "✅ Cleanup complete!"