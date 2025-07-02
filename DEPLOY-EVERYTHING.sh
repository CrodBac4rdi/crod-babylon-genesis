#!/bin/bash
# 🔥 CROD COMPLETE DEPLOYMENT - ONE SHOT, NO BULLSHIT

set -e

echo "🧹 CLEANING UP OLD SHIT..."

# 1. Kill old deployments
export KUBECONFIG=~/.kube/config
kubectl delete namespace crod-system --ignore-not-found=true
kubectl delete namespace crod-polyglot --ignore-not-found=true

# 2. Clean old docker images
docker rmi $(docker images 'crod/*genesis*' -q) 2>/dev/null || true
docker rmi $(docker images 'crod/*' -q) 2>/dev/null || true

echo "🏗️ BUILDING FRESH..."

# 3. Build all images ONCE
./build-all-images.sh

echo "📦 CREATING HELM CHART..."

# 4. Create proper Helm chart
mkdir -p helm-chart/crod-city/{templates,charts}

cat > helm-chart/crod-city/Chart.yaml << 'EOF'
apiVersion: v2
name: crod-city
description: CROD Polyglot City - Complete Deployment
type: application
version: 1.0.0
appVersion: "1.0.0"
EOF

cat > helm-chart/crod-city/values.yaml << 'EOF'
namespace: crod-city
replicaCount: 1

images:
  metaChain: crod/meta-chain:latest
  patternDistrict: crod/pattern-district:latest  
  memoryQuarter: crod/memory-quarter:latest
  intelligenceHub: crod/intelligence-hub:latest
  gateway: crod/gateway:latest

ports:
  metaChain: 8000
  patternDistrict: 7007
  memoryQuarter: 7031
  intelligenceHub: 7113
  gateway: 8888

redis:
  enabled: true
  replicas: 1
EOF

# 5. Create namespace template
cat > helm-chart/crod-city/templates/namespace.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: {{ .Values.namespace }}
EOF

# 6. Create Redis deployment
cat > helm-chart/crod-city/templates/redis.yaml << 'EOF'
{{- if .Values.redis.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: {{ .Values.namespace }}
spec:
  replicas: {{ .Values.redis.replicas }}
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: {{ .Values.namespace }}
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
{{- end }}
EOF

# 7. Create deployments for all districts
for district in meta-chain pattern-district memory-quarter gateway; do
  cat > helm-chart/crod-city/templates/${district}-deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${district}
  namespace: {{ .Values.namespace }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: ${district}
  template:
    metadata:
      labels:
        app: ${district}
    spec:
      containers:
      - name: ${district}
        image: {{ .Values.images.${district//-/} }}
        imagePullPolicy: Always
        ports:
        - containerPort: {{ .Values.ports.${district//-/} }}
        env:
        - name: REDIS_HOST
          value: redis
        - name: REDIS_PORT
          value: "6379"
---
apiVersion: v1
kind: Service
metadata:
  name: ${district}
  namespace: {{ .Values.namespace }}
spec:
  selector:
    app: ${district}
  ports:
  - port: {{ .Values.ports.${district//-/} }}
    targetPort: {{ .Values.ports.${district//-/} }}
EOF
done

# 8. Create gateway ingress
cat > helm-chart/crod-city/templates/gateway-service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: gateway-external
  namespace: {{ .Values.namespace }}
spec:
  type: NodePort
  selector:
    app: gateway
  ports:
  - port: 8888
    targetPort: {{ .Values.ports.gateway }}
    nodePort: 30888
EOF

echo "🚀 DEPLOYING WITH HELM..."

# 9. Deploy everything
helm upgrade --install crod-city ./helm-chart/crod-city \
  --create-namespace \
  --namespace crod-city \
  --wait \
  --timeout 5m

echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "🔍 Checking status..."
kubectl get all -n crod-city

echo ""
echo "🌐 Access points:"
echo "Gateway: http://localhost:30888"
echo ""
echo "📊 Quick commands:"
echo "kubectl logs -n crod-city -l app=meta-chain --tail=50"
echo "kubectl port-forward -n crod-city svc/gateway 8888:8888"
echo ""
echo "🗑️ To remove everything:"
echo "helm uninstall crod-city -n crod-city"
echo "kubectl delete namespace crod-city"