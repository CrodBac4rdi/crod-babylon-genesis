# Enterprise Security Guide: Secrets Management for CROD Project

## Overview
This guide covers enterprise-level security practices for handling secrets, API keys, and passwords in development environments, specifically tailored for the CROD Polyglot City architecture.

## 1. GitHub Secrets for CI/CD

### Core Principles
- **Rotate regularly**: Every 30-90 days
- **Use OIDC**: Prefer OpenID Connect over long-lived tokens
- **Environment-based access**: Implement approval workflows
- **Descriptive naming**: Use clear, consistent naming conventions

### Implementation
```yaml
# .github/workflows/deploy.yml
name: Deploy CROD Services
on:
  push:
    branches: [main]

jobs:
  deploy:
    environment: production  # Requires approval
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure Kubernetes
        run: |
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=./kubeconfig
          
      - name: Deploy to K8s
        env:
          REDIS_PASSWORD: ${{ secrets.REDIS_PASSWORD }}
          DB_CONNECTION: ${{ secrets.DB_CONNECTION }}
        run: |
          kubectl create secret generic crod-secrets \
            --from-literal=redis-password=$REDIS_PASSWORD \
            --from-literal=db-connection=$DB_CONNECTION \
            -n crod-polyglot --dry-run=client -o yaml | kubectl apply -f -
```

### GitHub Secrets Hierarchy
1. **Repository Secrets**: Specific to single repo
2. **Environment Secrets**: Require approval, environment-specific
3. **Organization Secrets**: Shared across repos (use sparingly!)

### Best Practices
- Use GitHub Variables for non-sensitive config
- Implement least privilege access
- Prefer GitHub Apps over Personal Access Tokens
- Never use organizational secrets without scoping

## 2. Environment Variables Best Practices

### DO's
```bash
# Good: Explicit naming with service prefix
export CROD_META_CHAIN_API_KEY="..."
export CROD_PATTERN_DISTRICT_TOKEN="..."
export CROD_REDIS_PASSWORD="..."

# Good: Use defaults for development
export CROD_ENV="${CROD_ENV:-development}"
export CROD_LOG_LEVEL="${CROD_LOG_LEVEL:-info}"
```

### DON'Ts
```bash
# Bad: Generic names
export PASSWORD="..."
export KEY="..."
export TOKEN="..."

# Bad: Hardcoded values in scripts
API_KEY="sk-1234567890"  # NEVER DO THIS!
```

### Loading Order (Priority)
1. Command-line arguments
2. Environment variables
3. `.env.local` (git-ignored)
4. `.env.development` / `.env.production`
5. `.env` (defaults only, no secrets!)

## 3. .env Files and .gitignore

### File Structure
```
/crod-polyglot-city/
├── .env                    # Defaults only, committed
├── .env.example           # Template with dummy values
├── .env.local             # Local overrides, git-ignored
├── .env.development       # Dev defaults, committed
├── .env.production        # Prod structure, no values
└── .gitignore            # MUST include .env.local
```

### .env.example
```bash
# CROD Polyglot City Configuration
# Copy to .env.local and fill in your values

# Meta-Chain Service
META_CHAIN_PORT=8000
META_CHAIN_API_KEY=your-api-key-here

# Pattern District
PATTERN_DISTRICT_PORT=7007
PATTERN_DISTRICT_TOKEN=your-token-here

# Redis Cluster
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Kubernetes
KUBECONFIG=/path/to/your/kubeconfig
```

### .gitignore (CRITICAL!)
```gitignore
# Environment files with secrets
.env.local
.env.*.local
*.env

# Kubernetes secrets
kubeconfig
*.kubeconfig
*-kubeconfig.yaml

# Keys and certificates
*.key
*.pem
*.p12
*.pfx
private/
secrets/

# IDE and OS
.vscode/settings.json
.idea/
.DS_Store

# Logs that might contain secrets
*.log
logs/
```

## 4. Docker Secrets Management

### Development Mode
```dockerfile
# Dockerfile
FROM elixir:1.15-alpine

# Use build args for non-sensitive config
ARG APP_ENV=development
ENV APP_ENV=${APP_ENV}

# NEVER put secrets in Dockerfile!
# BAD: ENV API_KEY=sk-1234567890
```

### Docker Compose with Secrets
```yaml
# docker-compose.yml
version: '3.8'

services:
  meta-chain:
    image: crod/meta-chain-elixir:latest
    environment:
      - APP_ENV=development
    secrets:
      - redis_password
      - api_key
    
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass_file /run/secrets/redis_password
    secrets:
      - redis_password

secrets:
  redis_password:
    file: ./secrets/redis_password.txt  # Git-ignored
  api_key:
    file: ./secrets/api_key.txt         # Git-ignored
```

### Production with Docker Swarm
```bash
# Create secrets in Swarm
echo "super-secret-password" | docker secret create redis_password -
echo "api-key-value" | docker secret create crod_api_key -

# Deploy with secrets
docker stack deploy -c docker-compose.prod.yml crod-stack
```

## 5. Kubernetes Secrets

### Basic Secrets (Encrypted at Rest)
```bash
# Create secret imperatively (for dev/testing)
kubectl create secret generic crod-secrets \
  --from-literal=redis-password='${REDIS_PASSWORD}' \
  --from-literal=api-key='${API_KEY}' \
  -n crod-polyglot

# Create from file
kubectl create secret generic crod-config \
  --from-file=config.json=./config.json \
  -n crod-polyglot
```

### Declarative with Sealed Secrets
```bash
# Install Sealed Secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Encrypt secret
echo -n "mypassword" | kubectl create secret generic crod-secrets \
  --dry-run=client \
  --from-file=redis-password=/dev/stdin \
  -o yaml | kubeseal -o yaml > sealed-secrets.yaml

# Apply sealed secret (safe to commit!)
kubectl apply -f sealed-secrets.yaml
```

### External Secrets Operator (Recommended for Production)
```yaml
# Install ESO
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets-system --create-namespace

# secretstore.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: crod-polyglot
spec:
  provider:
    vault:
      server: "https://vault.crod.internal:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "crod-services"

---
# externalsecret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: crod-secrets
  namespace: crod-polyglot
spec:
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: crod-secrets
  data:
    - secretKey: redis-password
      remoteRef:
        key: crod/data/redis
        property: password
    - secretKey: meta-chain-api-key
      remoteRef:
        key: crod/data/meta-chain
        property: api_key
```

### Using Secrets in Pods
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meta-chain
  namespace: crod-polyglot
spec:
  template:
    spec:
      containers:
      - name: meta-chain
        image: crod/meta-chain-elixir:latest
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: crod-secrets
              key: redis-password
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        secret:
          secretName: crod-config
```

## 6. HashiCorp Vault Integration

### Basic Setup
```bash
# Install Vault in K8s
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault \
  --set "server.ha.enabled=true" \
  --set "injector.enabled=true" \
  -n vault --create-namespace

# Initialize Vault
kubectl exec -it vault-0 -n vault -- vault operator init
kubectl exec -it vault-0 -n vault -- vault operator unseal
```

### Vault Agent Injector Annotations
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pattern-district
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "crod-services"
        vault.hashicorp.com/agent-inject-secret-redis: "secret/data/crod/redis"
        vault.hashicorp.com/agent-inject-template-redis: |
          {{- with secret "secret/data/crod/redis" -}}
          export REDIS_PASSWORD="{{ .Data.data.password }}"
          {{- end }}
    spec:
      containers:
      - name: pattern-district
        image: crod/pattern-district-rust:latest
        command: ["/bin/sh"]
        args: ["-c", "source /vault/secrets/redis && ./pattern-district"]
```

### Dynamic Secrets for Databases
```bash
# Configure database secrets engine
vault secrets enable database

vault write database/config/postgresql \
  plugin_name=postgresql-database-plugin \
  allowed_roles="crod-*" \
  connection_url="postgresql://{{username}}:{{password}}@postgres.crod.internal:5432/crod"

# Create role with TTL
vault write database/roles/crod-app \
  db_name=postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';" \
  default_ttl="1h" \
  max_ttl="24h"
```

## Security Checklist for CROD Project

### Before Every Commit
- [ ] Run `git diff --cached` to check for secrets
- [ ] Verify `.gitignore` includes all sensitive files
- [ ] Check no hardcoded values in code
- [ ] Ensure environment variables use CROD_ prefix

### Repository Setup
- [ ] Enable GitHub secret scanning
- [ ] Configure branch protection rules
- [ ] Set up environment-based deployments
- [ ] Create `.env.example` with dummy values

### Kubernetes Deployment
- [ ] Enable etcd encryption at rest
- [ ] Install Sealed Secrets or ESO
- [ ] Configure RBAC for secret access
- [ ] Set up NetworkPolicies
- [ ] Implement secret rotation

### Production Readiness
- [ ] All secrets in external vault (not K8s secrets)
- [ ] Automated secret rotation configured
- [ ] Audit logging enabled
- [ ] Least privilege access implemented
- [ ] Disaster recovery plan for secrets

## Quick Reference Commands

```bash
# Check for secrets in git history
git secrets --scan-history

# Verify no secrets in current changes
git diff --cached | grep -E "(password|key|token|secret)" 

# List all K8s secrets
kubectl get secrets -A | grep crod

# Rotate a secret in Vault
vault write -f secret/rotate/crod/redis

# Emergency: Delete exposed secret from git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret-file' \
  --prune-empty --tag-name-filter cat -- --all
```

## Remember: Security is a Journey

1. **Start Simple**: Basic K8s secrets + .gitignore
2. **Improve**: Add Sealed Secrets for Git storage
3. **Mature**: External Secrets Operator + Vault
4. **Excellence**: Full automation with dynamic secrets

The CROD project's distributed nature makes proper secrets management critical. Each district (service) should have its own credentials, never share secrets between services, and always assume breach - rotate regularly!