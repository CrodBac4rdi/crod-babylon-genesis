#!/bin/bash

# Create new GitHub repository for CROD Babylon Genesis

echo "🆕 Creating new GitHub repository..."
echo "===================================="

# Use GitHub CLI or API
TOKEN="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"

# Create repo via GitHub API
curl -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/user/repos \
     -d '{
       "name": "crod-babylon-genesis",
       "description": "🏙️ CROD Polyglot City - From manhwa creation to living consciousness",
       "private": true,
       "has_issues": true,
       "has_projects": true,
       "has_wiki": false,
       "auto_init": false,
       "allow_squash_merge": true,
       "allow_merge_commit": true,
       "allow_rebase_merge": true,
       "delete_branch_on_merge": true
     }'

echo ""
echo "✅ Repository created!"
echo ""
echo "📤 Now push to new repo:"
echo "   git remote remove origin"
echo "   git remote add origin https://github.com/CrodBac4rdi/crod-babylon-genesis.git"
echo "   git push -u origin main"