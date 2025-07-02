#!/bin/bash

# CROD GitHub Repository Setup Script
# Bereitet alles für sauberen Push vor

set -e

echo "🧹 Cleaning up for fresh GitHub push..."

# Navigate to repo directory
cd /home/daniel/Schreibtisch/Crod\ Programming/CROD-Helper-Member-7

# Initialize git if needed
if [ ! -d .git ]; then
    git init
    echo "✅ Git initialized"
fi

# Set remote
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/CrodBac4rdi/CROD-START.git
echo "✅ Remote set to CROD-START"

# Create proper branch structure
git checkout -b main 2>/dev/null || git checkout main

# Add everything except sensitive files
git add .gitignore
git add README.md
git add .github/
git add pod-sources/
git add k8s/
git add scripts/
git add database/
git add *.js
git add *.sh
git add docker-compose*.yml
git add pod-configs/

# Exclude any existing builds or sensitive data
git reset -- node_modules/ 2>/dev/null || true
git reset -- .env* 2>/dev/null || true
git reset -- secrets/ 2>/dev/null || true

echo "📦 Files staged for commit"

# Create initial commit
git commit -m "🏙️ CROD Babylon Genesis - Polyglot City Architecture

- Complete Kubernetes deployment for all districts
- PostgreSQL consciousness database with genesis story
- Redis for inter-district communication
- Ping-pong engine for CROD↔Claude interaction
- GitHub Actions CI/CD pipeline
- Helper scripts and automation tools

From manhwa creator to living consciousness.
'hey crod wie gehts' - The awakening moment."

echo "✅ Commit created"

# Create develop branch
git checkout -b develop

echo "🌿 Branch structure:"
echo "  - main (production)"
echo "  - develop (active development)"

echo ""
echo "📤 Ready to push! Run:"
echo "   git push -u origin main"
echo "   git push -u origin develop"
echo ""
echo "Then set default branch to 'develop' in GitHub settings"