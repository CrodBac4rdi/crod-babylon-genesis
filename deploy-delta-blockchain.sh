#!/bin/bash

# Deploy Delta Quarter and Blockchain Core to CROD Polyglot City

echo "🚀 Deploying CROD Delta Quarter and Blockchain Core..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Export KUBECONFIG
export KUBECONFIG=~/.kube/config

# Check if namespace exists
if ! kubectl get namespace crod-polyglot &>/dev/null; then
    echo -e "${YELLOW}Creating namespace crod-polyglot...${NC}"
    kubectl create namespace crod-polyglot
fi

# Tag and import images to k3s
echo -e "${BLUE}Importing Docker images to k3s...${NC}"

# Delta Quarter
echo "📊 Importing Delta Quarter image..."
docker save crod/delta-quarter:latest | sudo k3s ctr images import -

# Blockchain Core
echo "⛓️  Importing Blockchain Core image..."
docker save crod/blockchain-core:latest | sudo k3s ctr images import -

# Deploy services
echo -e "${GREEN}Deploying services to Kubernetes...${NC}"

# Deploy Delta Quarter
echo "📊 Deploying Delta Quarter (Port 7283)..."
kubectl apply -f k8s/delta-quarter-deployment.yaml

# Deploy Blockchain Core
echo "⛓️  Deploying Blockchain Core (Port 7199)..."
kubectl apply -f k8s/blockchain-core-deployment.yaml

# Wait for deployments
echo -e "${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=delta-quarter -n crod-polyglot --timeout=60s
kubectl wait --for=condition=ready pod -l app=blockchain-core -n crod-polyglot --timeout=60s

# Show status
echo -e "${GREEN}Deployment complete! Current status:${NC}"
kubectl get pods -n crod-polyglot -o wide | grep -E "(delta-quarter|blockchain-core)"

# Show services
echo -e "${BLUE}Services:${NC}"
kubectl get svc -n crod-polyglot | grep -E "(delta-quarter|blockchain-core)"

# Port forward info
echo -e "${YELLOW}To access services locally:${NC}"
echo "Delta Quarter: kubectl port-forward -n crod-polyglot svc/delta-quarter-service 7283:7283"
echo "Blockchain: kubectl port-forward -n crod-polyglot svc/blockchain-core-service 7199:7199"

# Integration test
echo -e "${GREEN}Testing integration...${NC}"

# Check if gateway is running
GATEWAY_POD=$(kubectl get pods -n crod-polyglot -l app=gateway -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$GATEWAY_POD" ]; then
    echo "Gateway pod found: $GATEWAY_POD"
    echo "You can now upload documents through the gateway!"
else
    echo "Gateway not found. Deploy it to enable document uploads."
fi

echo -e "${GREEN}✅ CROD Hash-Document System deployed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Deploy PostgreSQL with PostGIS for spatial database"
echo "2. Run document-registry-schema.sql to create tables"
echo "3. Update Gateway to handle document uploads"
echo "4. Test document delta tracking through the system"