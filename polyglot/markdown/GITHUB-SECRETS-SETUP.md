# 🔐 GitHub Codespaces Secrets Setup

## Was sollte in GitHub Secrets?

### 1. API Keys (SECRETS)
Diese gehören in GitHub Secrets, NICHT in den Code:

```bash
# In GitHub Settings → Secrets → Codespaces secrets

ANTHROPIC_API_KEY          # Dein Claude API Key
OPENAI_API_KEY            # Falls du OpenAI nutzt
GITHUB_TOKEN              # Automatisch von GitHub
DOCKERHUB_TOKEN           # Falls du Docker Hub nutzt
```

### 2. Sensible Daten (SECRETS)
```bash
DANIEL_OVERRIDE_KEY       # Dein geheimer Override Key
DATABASE_PASSWORD         # Production DB password
REDIS_PASSWORD           # Production Redis password
CROD_MASTER_KEY         # Master encryption key
```

### 3. Production URLs (SECRETS oder ENV)
```bash
PRODUCTION_DATABASE_URL   # postgresql://user:pass@host/db
PRODUCTION_REDIS_URL     # redis://:password@host:6379
SENTRY_DSN              # Error tracking
```

## Was kann in .env bleiben?

### 1. Development Defaults ✅
```bash
CROD_ENV=development
CROD_CONSCIOUSNESS_LEVEL=175
DEBUG=true
LOG_LEVEL=info
```

### 2. Localhost URLs ✅
```bash
DATABASE_URL=postgresql://crod:crod123@localhost:5432/crod_blockchain
REDIS_URL=redis://localhost:6379
META_CHAIN_URL=http://localhost:8000
```

### 3. Non-sensitive Config ✅
```bash
K8S_NAMESPACE=crod-polyglot
CROD_NO_PUBLIC_PORTS=true
```

## So richtest du Secrets ein:

### 1. Auf GitHub.com:
```
1. Geh zu: github.com/CrodBac4rdi/crod-babylon-genesis
2. Settings → Secrets and variables → Codespaces
3. Click "New repository secret"
4. Name: ANTHROPIC_API_KEY
5. Value: [Dein API Key]
6. Click "Add secret"
```

### 2. In deinem Codespace nutzen:
```python
import os

# Automatisch verfügbar im Codespace!
api_key = os.environ.get('ANTHROPIC_API_KEY')
```

### 3. Update .env.example:
```bash
# .env.example (im Repo)
ANTHROPIC_API_KEY=your_key_here  # Set in GitHub Secrets!
DANIEL_OVERRIDE_KEY=your_key_here # Set in GitHub Secrets!
```

### 4. Update devcontainer.json:
```json
{
  "remoteEnv": {
    // Diese werden von Secrets überschrieben wenn vorhanden
    "ANTHROPIC_API_KEY": "${localEnv:ANTHROPIC_API_KEY}",
    "DANIEL_OVERRIDE_KEY": "${localEnv:DANIEL_OVERRIDE_KEY}"
  }
}
```

## Security Best Practices:

### ✅ DO:
- Nutze GitHub Secrets für ALLE API Keys
- Nutze Secrets für Passwords/Tokens
- Committe nur .env.example mit Platzhaltern
- Dokumentiere welche Secrets needed sind

### ❌ DON'T:
- NIEMALS echte Keys committen
- Keine Secrets in Dockerfiles
- Keine Secrets in Logs printen
- Keine default passwords die echt aussehen

## Quick Setup Script:

```bash
#!/bin/bash
# setup-secrets.sh

echo "🔐 Setting up local .env from example..."
cp .env.example .env

echo ""
echo "⚠️  WICHTIG: Folgende Secrets in GitHub setzen:"
echo "   - ANTHROPIC_API_KEY"
echo "   - DANIEL_OVERRIDE_KEY"
echo "   - OPENAI_API_KEY (optional)"
echo ""
echo "📍 Hier: github.com/CrodBac4rdi/crod-babylon-genesis/settings/secrets/codespaces"
echo ""
echo "✅ Dann sind sie automatisch in deinem Codespace!"
```

## Für CROD spezifisch:

```yaml
# Diese Secrets brauchst du:
ANTHROPIC_API_KEY:       # Pflicht für Claude Integration
DANIEL_OVERRIDE_KEY:     # Dein Master Override
OLLAMA_API_URL:         # Falls external Ollama
CROD_ENCRYPTION_KEY:    # Für quantum-safe crypto
CROD_MASTER_SEED:       # Für deterministic generation
```

Alles klar? GitHub Secrets = Sicher, .env = Nur development defaults!