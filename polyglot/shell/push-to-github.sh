#!/bin/bash

echo "🚀 CROD Clean GitHub Push Script"
echo "================================"

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# GitHub Username abfragen
read -p "GitHub Username: " GITHUB_USER
read -p "Repository Name (default: crod-clean): " REPO_NAME
REPO_NAME=${REPO_NAME:-crod-clean}

# Repository URL setzen
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo -e "\n${YELLOW}Setting up repository: ${REPO_URL}${NC}"

# Git konfigurieren (falls noch nicht geschehen)
git config user.name "$GITHUB_USER" 2>/dev/null
git config user.email "${GITHUB_USER}@users.noreply.github.com" 2>/dev/null

# Remote setzen
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo -e "\n${GREEN}Repository configured!${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "   - Repository name: ${REPO_NAME}"
echo "   - Make it public or private"
echo "   - DO NOT initialize with README, .gitignore or license"
echo ""
echo "2. Then run:"
echo -e "   ${GREEN}git push -u origin main${NC}"
echo ""
echo "Or if you want to push to an existing repo (will overwrite!):"
echo -e "   ${GREEN}git push -u origin main --force${NC}"

# Optional: Direkt pushen
echo -e "\n${YELLOW}Do you want to push now? (y/n)${NC}"
read -p "> " PUSH_NOW

if [ "$PUSH_NOW" = "y" ] || [ "$PUSH_NOW" = "Y" ]; then
    echo -e "\n${YELLOW}Pushing to GitHub...${NC}"
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Successfully pushed to GitHub!${NC}"
        echo -e "Repository URL: ${REPO_URL}"
    else
        echo -e "\n${RED}❌ Push failed. Make sure:${NC}"
        echo "1. The repository exists on GitHub"
        echo "2. You have the correct permissions"
        echo "3. You're authenticated (try: gh auth login)"
    fi
fi