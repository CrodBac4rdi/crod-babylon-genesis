#!/bin/bash
# Push CROD Clean Repository to GitHub

# This script pushes the crod-clean repository to GitHub
# Make sure you have created a GitHub repository first and have the necessary permissions

echo "Setting up GitHub repository for CROD Clean..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "Git repository initialized."
fi

# Add all files to the repository
git add .

# Commit changes
git commit -m "Initial commit of CROD Clean - Modern Polyglot Architecture"

# Set up remote repository
echo "Please enter your GitHub username:"
read username

echo "Please enter your GitHub repository name (e.g., crod-clean):"
read repo_name

# Add GitHub remote
git remote add origin "https://github.com/$username/$repo_name.git"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "Repository successfully pushed to GitHub!"
echo "You can now access your repository at: https://github.com/$username/$repo_name"
