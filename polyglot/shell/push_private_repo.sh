#!/bin/bash

echo "Konfiguriere Git für den Push zu deinem privaten Repository"
echo "-----------------------------------------------------------"

# Wir verwenden HTTPS mit einem Personal Access Token
echo "Bitte gib deinen GitHub Personal Access Token ein:"
read -s token

echo "Setze Remote-URL mit Token..."
git remote set-url origin https://CrodBac4rdi:${token}@github.com/CrodBac4rdi/crod-clean.git

echo "Push zum Main-Branch..."
git push -u origin main

echo "Remote-URL zurücksetzen (aus Sicherheitsgründen)..."
git remote set-url origin https://github.com/CrodBac4rdi/crod-clean.git

echo "Fertig!"
