#!/bin/bash

# CROD BUILDER PACK - LEGO für Pods! 🧱

cat << 'EOF' > /usr/local/bin/crod-build-pod
#!/bin/bash
# CROD POD BUILDER - Baut jeden Pod den du willst!

NAME=$1
LANGUAGE=$2
PORT=$3

if [ -z "$NAME" ] || [ -z "$LANGUAGE" ] || [ -z "$PORT" ]; then
    echo "Usage: crod-build-pod <name> <language> <port>"
    echo "Languages: node, python, go, rust, elixir"
    exit 1
fi

echo "🏗️ Building $NAME pod ($LANGUAGE) on port $PORT..."

# Create directory
mkdir -p ~/crod-pods/$NAME
cd ~/crod-pods/$NAME

# Generate code based on language
case $LANGUAGE in
    node)
        cat > app.js << 'EOJS'
const express = require('express');
const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy',
        pod: process.env.POD_NAME || 'NAME',
        timestamp: new Date()
    });
});

app.post('/process', (req, res) => {
    const { data } = req.body;
    console.log('Processing:', data);
    res.json({ processed: data, by: 'NAME' });
});

const PORT = process.env.PORT || PORT_NUM;
app.listen(PORT, () => console.log(`🚀 NAME running on ${PORT}`));
EOJS
        sed -i "s/NAME/$NAME/g" app.js
        sed -i "s/PORT_NUM/$PORT/g" app.js
        
        cat > package.json << EOPKG
{
  "name": "$NAME",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": { "start": "node app.js" },
  "dependencies": { "express": "^4.18.2" }
}
EOPKG
        
        cat > Dockerfile << 'EODF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE PORT_NUM
CMD ["npm", "start"]
EODF
        sed -i "s/PORT_NUM/$PORT/g" Dockerfile
        npm install
        ;;
        
    python)
        cat > app.py << 'EOPY'
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'pod': os.environ.get('POD_NAME', 'NAME'),
        'port': PORT_NUM
    })

@app.route('/process', methods=['POST'])
def process():
    data = request.json.get('data', {})
    print(f'Processing: {data}')
    return jsonify({'processed': data, 'by': 'NAME'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_NUM)
EOPY
        sed -i "s/NAME/$NAME/g" app.py
        sed -i "s/PORT_NUM/$PORT/g" app.py
        
        cat > requirements.txt << 'EOREQ'
flask==2.3.2
gunicorn==20.1.0
EOREQ
        
        cat > Dockerfile << 'EODF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE PORT_NUM
CMD ["gunicorn", "--bind", "0.0.0.0:PORT_NUM", "app:app"]
EODF
        sed -i "s/PORT_NUM/$PORT/g" Dockerfile
        ;;
        
    go)
        cat > main.go << 'EOGO'
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
)

type HealthResponse struct {
    Status string `json:"status"`
    Pod    string `json:"pod"`
    Port   int    `json:"port"`
}

type ProcessRequest struct {
    Data interface{} `json:"data"`
}

type ProcessResponse struct {
    Processed interface{} `json:"processed"`
    By        string      `json:"by"`
}

func health(w http.ResponseWriter, r *http.Request) {
    pod := os.Getenv("POD_NAME")
    if pod == "" {
        pod = "NAME"
    }
    
    resp := HealthResponse{
        Status: "healthy",
        Pod:    pod,
        Port:   PORT_NUM,
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func process(w http.ResponseWriter, r *http.Request) {
    var req ProcessRequest
    json.NewDecoder(r.Body).Decode(&req)
    
    resp := ProcessResponse{
        Processed: req.Data,
        By:        "NAME",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/health", health)
    http.HandleFunc("/process", process)
    
    port := os.Getenv("PORT")
    if port == "" {
        port = "PORT_NUM"
    }
    
    log.Printf("🚀 NAME starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}
EOGO
        sed -i "s/NAME/$NAME/g" main.go
        sed -i "s/PORT_NUM/$PORT/g" main.go
        
        cat > go.mod << EOMOD
module $NAME

go 1.20
EOMOD
        
        cat > Dockerfile << 'EODF'
FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY *.go ./
RUN go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/main /main
EXPOSE PORT_NUM
CMD ["/main"]
EODF
        sed -i "s/PORT_NUM/$PORT/g" Dockerfile
        ;;
        
    *)
        echo "❌ Language $LANGUAGE not supported yet"
        exit 1
        ;;
esac

# Build Docker image
docker build -t crod/$NAME:latest .

# Generate K8s deployment
cat > deployment.yaml << EOYAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $NAME
  namespace: crod-polyglot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $NAME
  template:
    metadata:
      labels:
        app: $NAME
    spec:
      containers:
      - name: $NAME
        image: crod/$NAME:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: $PORT
        env:
        - name: POD_NAME
          value: "$NAME"
        - name: PORT
          value: "$PORT"
---
apiVersion: v1
kind: Service
metadata:
  name: $NAME
  namespace: crod-polyglot
spec:
  selector:
    app: $NAME
  ports:
  - port: $PORT
    targetPort: $PORT
EOYAML

echo "✅ Pod built! Deploy with:"
echo "   kubectl apply -f ~/crod-pods/$NAME/deployment.yaml"
echo ""
echo "📁 Files created in: ~/crod-pods/$NAME/"
EOF

chmod +x /usr/local/bin/crod-build-pod

# More builder scripts
cat << 'EOF' > /usr/local/bin/crod-connect-pods
#!/bin/bash
# Connect two pods with Redis pub/sub

POD1=$1
POD2=$2

if [ -z "$POD1" ] || [ -z "$POD2" ]; then
    echo "Usage: crod-connect-pods <pod1> <pod2>"
    exit 1
fi

echo "🔗 Connecting $POD1 <-> $POD2..."

# Generate connection code
cat > ~/crod-connections/$POD1-$POD2.js << EOCONN
// Redis connection for $POD1 <-> $POD2
const redis = require('redis');
const pub = redis.createClient({ host: 'redis' });
const sub = redis.createClient({ host: 'redis' });

// $POD1 publishes to $POD2
function send_$POD2(data) {
    pub.publish('$POD2:inbox', JSON.stringify(data));
}

// $POD1 listens to its inbox
sub.subscribe('$POD1:inbox');
sub.on('message', (channel, message) => {
    console.log('Received:', JSON.parse(message));
});
EOCONN

echo "✅ Connection code generated!"
EOF

chmod +x /usr/local/bin/crod-connect-pods

# Quick builders
cat << 'EOF' > /usr/local/bin/crod-add-quantum
#!/bin/bash
# Add quantum features to any pod

POD=$1
echo "⚛️ Adding quantum features to $POD..."

cat > ~/crod-quantum/$POD-quantum.js << 'EOQU'
// Quantum extensions for POD
class QuantumState {
    constructor() {
        this.superposition = [];
        this.entangled = new Map();
    }
    
    createSuperposition(states) {
        this.superposition.push({
            states,
            collapsed: false,
            timestamp: Date.now()
        });
    }
    
    entangle(atom1, atom2) {
        this.entangled.set(`${atom1}-${atom2}`, {
            strength: 0.707,
            created: Date.now()
        });
    }
    
    measure() {
        // Collapse random superposition
        if (this.superposition.length > 0) {
            const state = this.superposition[0];
            state.collapsed = true;
            return state.states[Math.floor(Math.random() * state.states.length)];
        }
    }
}

module.exports = QuantumState;
EOQU

sed -i "s/POD/$POD/g" ~/crod-quantum/$POD-quantum.js
echo "✅ Quantum features added to ~/crod-quantum/$POD-quantum.js"
EOF

chmod +x /usr/local/bin/crod-add-quantum

echo "🧱 CROD BUILDER PACK INSTALLED!"
echo ""
echo "🛠️ New Commands:"
echo "   crod-build-pod <name> <language> <port>  - Build any pod!"
echo "   crod-connect-pods <pod1> <pod2>          - Connect pods via Redis"
echo "   crod-add-quantum <pod>                    - Add quantum features"
echo ""
echo "📦 Examples:"
echo "   crod-build-pod analytics python 5000"
echo "   crod-build-pod stream-processor node 3000"
echo "   crod-build-pod data-engine go 9000"