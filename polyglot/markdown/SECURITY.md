# 🔒 CROD Security Guidelines

## GitHub Secrets Setup

### Required Secrets

These MUST be set in GitHub Secrets, NEVER in code:

1. **Go to:** `Settings → Secrets and variables → Codespaces`
2. **Add these secrets:**

| Secret Name | Description | Required |
|------------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API Key | ✅ Yes |
| `DANIEL_OVERRIDE_KEY` | Master override key | ✅ Yes |
| `OPENAI_API_KEY` | OpenAI API Key | ⚪ Optional |
| `CROD_MASTER_KEY` | Master encryption key | ⚪ Optional |
| `CROD_ENCRYPTION_KEY` | Data encryption key | ⚪ Optional |
| `DOCKERHUB_TOKEN` | Docker Hub access | ⚪ Optional |

### How to add secrets:

```
1. Go to: github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/codespaces
2. Click "New repository secret"
3. Name: ANTHROPIC_API_KEY
4. Value: [Your actual API key]
5. Click "Add secret"
```

## Security Rules

### ✅ DO:
- Use GitHub Secrets for ALL sensitive data
- Use `.env.example` with placeholders
- Run security checks before commit
- Use private ports only
- Encrypt sensitive data at rest

### ❌ DON'T:
- NEVER commit real API keys
- NEVER use default passwords
- NEVER expose ports publicly
- NEVER log sensitive data
- NEVER store secrets in Docker images

## Pre-commit Check

Before committing, run:

```bash
# Check for exposed secrets
grep -r "api_key\|password\|secret" . --exclude-dir=.git --exclude="*.example"

# Check for .env files
find . -name ".env" -o -name ".env.local"
```

## Environment Variables

### Development (local .env):
```bash
# Safe for .env
CROD_ENV=development
DEBUG=true
DATABASE_URL=postgresql://crod:crod123@localhost:5432/crod_blockchain
```

### Production (GitHub Secrets):
```bash
# Must be in Secrets
ANTHROPIC_API_KEY=sk-ant-...
DANIEL_OVERRIDE_KEY=super-secret-key-...
DATABASE_PASSWORD=production-password-...
```

## Network Security

All services are configured with:
- No public ports
- localhost only access
- NetworkPolicy blocking external traffic
- iptables rules for extra protection

## Monitoring

GitHub Actions automatically check for:
- Exposed API keys
- Hardcoded passwords
- Committed .env files
- Known secret patterns

See `.github/workflows/security-check.yml`