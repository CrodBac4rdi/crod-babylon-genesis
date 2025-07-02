#!/bin/bash
# Generate GitHub Container Registry secret for Kubernetes

echo "🔐 Generating GitHub Container Registry secret..."

# Check if GITHUB_TOKEN is set
if [ -z "${GITHUB_TOKEN}" ]; then
    echo "❌ GITHUB_TOKEN environment variable not set!"
    echo "Please run: export GITHUB_TOKEN=your_github_personal_access_token"
    exit 1
fi

# GitHub username (can be passed as argument or use current)
GITHUB_USER=${1:-$USER}

# Create docker config
DOCKER_CONFIG=$(echo -n "{\"auths\":{\"ghcr.io\":{\"username\":\"${GITHUB_USER}\",\"password\":\"${GITHUB_TOKEN}\",\"auth\":\"$(echo -n ${GITHUB_USER}:${GITHUB_TOKEN} | base64 -w 0)\"}}}" | base64 -w 0)

# Update the secret file
cat > k8s/image-pull-secret.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: ghcr-secret
  namespace: crod-polyglot
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: ${DOCKER_CONFIG}
EOF

echo "✅ GitHub Container Registry secret generated!"
echo "📋 To apply to your cluster: kubectl apply -f k8s/image-pull-secret.yaml"