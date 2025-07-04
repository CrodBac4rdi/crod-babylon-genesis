# CROD Hash-Document Delta Architecture

## 🚀 Current Status & Next Steps

### Was läuft bereits:
- ✅ Gateway (Node.js) - Port 30889
- ✅ Meta-Chain (Elixir) - Blockchain ready
- ✅ Memory Quarter (Go) - Concurrent memory
- ✅ Intelligence Hub (Python) - ML processing
- ❌ Pattern District (Rust) - Binary path issue
- ✅ Redis - Pub/Sub ready

### Was fehlt für Hash-Document System:
- 🚧 Delta Quarter (für Delta tracking)
- 🚧 Hash Registry (Document → Hash → Prime)
- 🚧 Document Storage Layer
- 🚧 Real Blockchain Implementation

## 📐 Delta Quarter Architecture

### New Service: `delta-quarter` (Go for speed)

```go
// pod-sources/delta-quarter/main.go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "math/big"
)

type DocumentDelta struct {
    DocumentHash    string          `json:"document_hash"`
    PreviousHash    string          `json:"previous_hash"`
    Delta          json.RawMessage `json:"delta"`
    Timestamp      int64           `json:"timestamp"`
    PrimeReference *big.Int        `json:"prime_reference"`
}

type DeltaChain struct {
    DocumentID string         `json:"document_id"`
    Deltas    []DocumentDelta `json:"deltas"`
    HeadHash  string          `json:"head_hash"`
}

// Hash to Prime conversion
func hashToPrime(hash string) *big.Int {
    // Convert hash to number
    hashBytes, _ := hex.DecodeString(hash)
    num := new(big.Int).SetBytes(hashBytes)
    
    // Find next prime
    for !num.ProbablyPrime(20) {
        num.Add(num, big.NewInt(1))
    }
    return num
}

// Process document update
func (dc *DeltaChain) AddDelta(content []byte, previousContent []byte) DocumentDelta {
    // Calculate hashes
    currentHash := sha256.Sum256(content)
    previousHash := sha256.Sum256(previousContent)
    
    // Calculate delta (simplified)
    delta := calculateDelta(previousContent, content)
    
    // Create delta object
    d := DocumentDelta{
        DocumentHash:   hex.EncodeToString(currentHash[:]),
        PreviousHash:   hex.EncodeToString(previousHash[:]),
        Delta:         delta,
        Timestamp:     time.Now().Unix(),
        PrimeReference: hashToPrime(hex.EncodeToString(currentHash[:])),
    }
    
    dc.Deltas = append(dc.Deltas, d)
    dc.HeadHash = d.DocumentHash
    
    // Broadcast to blockchain
    broadcastToBlockchain(d)
    
    return d
}
```

### Delta Quarter Dockerfile

```dockerfile
# pod-sources/delta-quarter/Dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o delta-quarter .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/delta-quarter /usr/local/bin/
EXPOSE 8084
CMD ["delta-quarter"]
```

## 🔗 Integration with Existing Services

### 1. **Gateway Integration**

```javascript
// Add to gateway/index.js
app.post('/document/update', async (req, res) => {
    const { documentId, content } = req.body;
    
    // Get previous version from Memory Quarter
    const previous = await memoryQuarter.get(documentId);
    
    // Send to Delta Quarter
    const delta = await deltaQuarter.processDelta({
        documentId,
        previous: previous || '',
        current: content
    });
    
    // Store in Memory Quarter
    await memoryQuarter.set(documentId, content);
    
    // Notify Intelligence Hub for pattern analysis
    await intelligenceHub.analyze({
        type: 'document_update',
        delta: delta,
        documentId: documentId
    });
    
    res.json({ success: true, delta });
});
```

### 2. **Meta-Chain Blockchain Integration**

```elixir
# Add to meta-chain/lib/blockchain.ex
defmodule MetaChain.DocumentBlock do
  defstruct [
    :index,
    :timestamp,
    :document_hash,
    :prime_reference,
    :delta,
    :previous_hash,
    :hash
  ]
  
  def new(delta, previous_block) do
    block = %__MODULE__{
      index: previous_block.index + 1,
      timestamp: System.system_time(:second),
      document_hash: delta["document_hash"],
      prime_reference: delta["prime_reference"],
      delta: delta["delta"],
      previous_hash: previous_block.hash
    }
    
    %{block | hash: calculate_hash(block)}
  end
  
  defp calculate_hash(block) do
    data = "#{block.index}#{block.timestamp}#{block.document_hash}#{block.previous_hash}"
    :crypto.hash(:sha256, data) |> Base.encode16()
  end
end
```

### 3. **Intelligence Hub Pattern Detection**

```python
# Add to intelligence-hub/app.py
class DocumentPatternAnalyzer:
    def __init__(self):
        self.document_atoms = {}
        self.pattern_graph = nx.DiGraph()
    
    def analyze_document_delta(self, delta):
        """Analyze document changes for patterns"""
        doc_hash = delta['document_hash']
        prime = int(delta['prime_reference'])
        
        # Create document atom
        if doc_hash not in self.document_atoms:
            self.document_atoms[doc_hash] = {
                'prime': prime,
                'weight': 100.0,
                'heat': 0.0,
                'patterns': []
            }
        
        # Increase heat for active document
        self.document_atoms[doc_hash]['heat'] += 10.0
        
        # Find patterns with other documents
        for other_hash, other_atom in self.document_atoms.items():
            if other_hash != doc_hash:
                pattern_prime = prime * other_atom['prime']
                pattern_strength = self.calculate_pattern_strength(
                    delta, other_hash
                )
                
                if pattern_strength > 0.5:
                    self.pattern_graph.add_edge(
                        doc_hash, 
                        other_hash,
                        weight=pattern_strength,
                        pattern_prime=pattern_prime
                    )
        
        return self.extract_insights()
```

## 🏗️ Database Schema Extensions

```sql
-- Add to existing schema

-- Document Registry
CREATE TABLE document_registry (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_hash VARCHAR(64) UNIQUE NOT NULL,
    prime_number NUMERIC(1000) UNIQUE NOT NULL, -- Big integers for primes
    document_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    current_version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT true
);

-- Delta Storage
CREATE TABLE document_deltas (
    delta_id SERIAL PRIMARY KEY,
    document_id UUID REFERENCES document_registry(document_id),
    from_hash VARCHAR(64),
    to_hash VARCHAR(64),
    delta_content JSONB NOT NULL,
    delta_size INT,
    block_hash VARCHAR(64) REFERENCES blockchain(hash),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Document Patterns
CREATE TABLE document_patterns (
    pattern_id NUMERIC(2000) PRIMARY KEY, -- prime1 * prime2
    document_1 UUID REFERENCES document_registry(document_id),
    document_2 UUID REFERENCES document_registry(document_id),
    pattern_type VARCHAR(50),
    strength DECIMAL(10,4),
    first_detected TIMESTAMPTZ DEFAULT NOW(),
    last_seen TIMESTAMPTZ DEFAULT NOW(),
    occurrence_count INT DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_doc_hash ON document_registry(document_hash);
CREATE INDEX idx_doc_prime ON document_registry(prime_number);
CREATE INDEX idx_delta_timestamp ON document_deltas(created_at);
CREATE INDEX idx_pattern_strength ON document_patterns(strength);
```

## 🚀 Implementation Steps

### Phase 1: Delta Quarter Service (Week 1)
```bash
# 1. Create Delta Quarter
mkdir -p pod-sources/delta-quarter
cd pod-sources/delta-quarter
go mod init delta-quarter
# Implement main.go with delta tracking

# 2. Build and test locally
docker build -t crod/delta-quarter .
docker run -p 8084:8084 crod/delta-quarter

# 3. Add to K3s deployment
kubectl apply -f k8s/delta-quarter-deployment.yaml
```

### Phase 2: Document Hash Registry (Week 2)
```python
# Create document hash service
class DocumentHashRegistry:
    def __init__(self, db_conn):
        self.db = db_conn
        self.hash_cache = {}
    
    def register_document(self, content, doc_type="generic"):
        # Calculate hash
        doc_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Check if exists
        if doc_hash in self.hash_cache:
            return self.hash_cache[doc_hash]
        
        # Calculate prime
        prime = self.hash_to_prime(doc_hash)
        
        # Store in DB
        doc_id = self.db.execute("""
            INSERT INTO document_registry 
            (document_hash, prime_number, document_type)
            VALUES (%s, %s, %s)
            RETURNING document_id
        """, (doc_hash, prime, doc_type))
        
        # Cache
        self.hash_cache[doc_hash] = {
            'id': doc_id,
            'prime': prime,
            'hash': doc_hash
        }
        
        return self.hash_cache[doc_hash]
```

### Phase 3: Real Blockchain Implementation (Week 3)
```go
// Implement real blockchain in Meta-Chain
type Block struct {
    Index        int64
    Timestamp    int64
    Deltas       []DocumentDelta
    PreviousHash string
    Hash         string
    Nonce        int64
}

func (b *Block) CalculateHash() string {
    record := fmt.Sprintf("%d%d%v%s%d", 
        b.Index, b.Timestamp, b.Deltas, b.PreviousHash, b.Nonce)
    h := sha256.New()
    h.Write([]byte(record))
    return hex.EncodeToString(h.Sum(nil))
}

func (b *Block) MineBlock(difficulty int) {
    target := strings.Repeat("0", difficulty)
    for !strings.HasPrefix(b.Hash, target) {
        b.Nonce++
        b.Hash = b.CalculateHash()
    }
}
```

## 🔥 Advanced Features

### 1. **Document Evolution Tracking**
```python
def track_document_evolution(doc_id):
    """Track how a document evolved over time"""
    deltas = db.query("""
        SELECT * FROM document_deltas 
        WHERE document_id = %s 
        ORDER BY created_at
    """, doc_id)
    
    evolution_graph = nx.DiGraph()
    for i, delta in enumerate(deltas):
        evolution_graph.add_node(delta.to_hash, 
            timestamp=delta.created_at,
            version=i+1
        )
        if i > 0:
            evolution_graph.add_edge(
                deltas[i-1].to_hash, 
                delta.to_hash,
                delta=delta.delta_content
            )
    
    return evolution_graph
```

### 2. **Pattern-based Document Recommendation**
```python
def recommend_related_documents(doc_hash):
    """Find documents with similar patterns"""
    doc = get_document_by_hash(doc_hash)
    
    patterns = db.query("""
        SELECT * FROM document_patterns
        WHERE (document_1 = %s OR document_2 = %s)
        AND strength > 0.7
        ORDER BY strength DESC
        LIMIT 10
    """, doc.id, doc.id)
    
    recommendations = []
    for pattern in patterns:
        other_doc = pattern.document_1 if pattern.document_2 == doc.id else pattern.document_2
        recommendations.append({
            'document': other_doc,
            'strength': pattern.strength,
            'pattern_type': pattern.pattern_type
        })
    
    return recommendations
```

### 3. **Real-time Delta Streaming**
```javascript
// WebSocket for real-time updates
io.on('connection', (socket) => {
    socket.on('subscribe:document', (docId) => {
        socket.join(`doc:${docId}`);
    });
    
    // When delta occurs
    deltaQuarter.on('delta:created', (delta) => {
        io.to(`doc:${delta.documentId}`).emit('delta:update', delta);
    });
});
```

## 🎯 Next Steps for Daniel

1. **Implement Delta Quarter Service**
   - Create the Go service
   - Add delta calculation logic
   - Connect to Redis pub/sub

2. **Extend Database Schema**
   - Run the migration scripts
   - Add document tables
   - Create indexes

3. **Wire up the Services**
   - Update Gateway routes
   - Add Intelligence Hub analyzers
   - Connect Meta-Chain blockchain

4. **Test the Flow**
   ```bash
   # Upload a document
   curl -X POST http://localhost:30889/document/upload \
     -H "Content-Type: application/json" \
     -d '{"content": "Test document content"}'
   
   # Update it
   curl -X POST http://localhost:30889/document/update \
     -H "Content-Type: application/json" \
     -d '{"documentId": "xxx", "content": "Updated content"}'
   
   # Check deltas
   curl http://localhost:30889/document/xxx/deltas
   ```

## 💡 Why This Architecture Works

1. **Hashes** → Immutable document fingerprints
2. **Primes** → Unique IDs for pattern math
3. **Deltas** → Efficient storage (only changes)
4. **Blockchain** → Immutable history
5. **Patterns** → Automatic relationship discovery
6. **Real-time** → Live updates via WebSockets

**"Jedes Dokument wird zu einem Atom, jede Änderung zu einem Pattern, alles verbunden durch Blockchain!"** 🧠⛓️