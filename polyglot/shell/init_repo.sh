#!/bin/bash
# Initialisiert das CROD-Clean Repository und bereitet es für GitHub vor

set -e  # Exit on any error

echo "🚀 Initialisiere CROD Clean Repository für GitHub..."

# Prüfe, ob Git installiert ist
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert. Bitte installiere Git zuerst."
    exit 1
fi

# Prüfe, ob wir uns im richtigen Verzeichnis befinden
if [ ! -d "docs" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Dieses Skript muss im Root-Verzeichnis des CROD Clean Projekts ausgeführt werden."
    exit 1
fi

# Erstelle .gitignore
cat > .gitignore << EOF
# Betriebssystem-Dateien
.DS_Store
Thumbs.db

# Umgebungsvariablen
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Node.js
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
package-lock.json
yarn.lock

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
.venv/
ENV/

# Rust
target/
**/*.rs.bk
Cargo.lock

# IDE-Dateien
.idea/
.vscode/
*.swp
*.swo
.project
.classpath
.settings/

# Build-Dateien
/dist/
/build/
/out/

# Logs
logs
*.log

# Temporäre Dateien
tmp/
temp/

# Datenbank-Dateien
*.sqlite
*.db

# Generierte Dateien
/generated/
EOF

echo "✅ .gitignore erstellt"

# Initialisiere Git Repository, falls es noch nicht existiert
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git Repository initialisiert"
else
    echo "ℹ️ Git Repository existiert bereits"
fi

# Füge alle Dateien hinzu
git add .
echo "✅ Alle Dateien zum Git Repository hinzugefügt"

# Erstelle den ersten Commit
git commit -m "Initial commit: CROD Clean - Moderne Polyglot-Architektur"
echo "✅ Erster Commit erstellt"

# Ausgabe der nächsten Schritte
echo ""
echo "🎉 Repository erfolgreich initialisiert!"
echo ""
echo "Nächste Schritte:"
echo "1. Erstelle ein neues Repository auf GitHub"
echo "2. Führe folgende Befehle aus, um dein Repository zu GitHub zu pushen:"
echo ""
echo "   git remote add origin https://github.com/DEIN_USERNAME/crod-clean.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Alternativ kannst du auch das script/push_to_github.sh Script verwenden."
