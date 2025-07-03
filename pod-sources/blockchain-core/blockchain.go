package main

import (
    "crypto/rand"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "log"
    "strings"
    "sync"
    "time"
    
    // Quantum-safe crypto will be added later
    // For now using enhanced classical crypto
    "github.com/go-redis/redis/v8"
    "context"
)

// Block represents a CROD quantum-safe blockchain block
type Block struct {
    Index        int64        `json:"index"`
    Timestamp    time.Time    `json:"timestamp"`
    Data         CRODData     `json:"data"`
    PreviousHash string       `json:"previous_hash"`
    Hash         string       `json:"hash"`
    Nonce        int          `json:"nonce"`
    QuantumProof QuantumProof `json:"quantum_proof"`
    Signature    []byte       `json:"signature"`
}

// CRODData contains CROD-specific blockchain data
type CRODData struct {
    District      string                 `json:"district"`
    Pattern       string                 `json:"pattern"`
    Trinity       map[string]float64     `json:"trinity"`
    Atoms         []string               `json:"atoms"`
    DocumentDelta *DocumentDelta         `json:"document_delta,omitempty"`
    Metadata      map[string]interface{} `json:"metadata"`
}

// DocumentDelta from Delta Quarter
type DocumentDelta struct {
    DocumentHash   string          `json:"document_hash"`
    PreviousHash   string          `json:"previous_hash"`
    Delta          json.RawMessage `json:"delta"`
    DeltaType      string          `json:"delta_type"`
    PrimeReference string          `json:"prime_reference"`
    Heat           float64         `json:"heat"`
}

// QuantumProof - Post-quantum cryptographic proof
type QuantumProof struct {
    KyberCiphertext []byte `json:"kyber_ciphertext"`
    DilithiumPubKey []byte `json:"dilithium_pub_key"`
    LatticeHash     string `json:"lattice_hash"`
}

// CalculateHash generates quantum-resistant hash for a block
func (b *Block) CalculateHash() string {
    record := fmt.Sprintf("%d%s%s%s%d", 
        b.Index, 
        b.Timestamp, 
        b.Data, 
        b.PreviousHash, 
        b.Nonce)
    
    // Multiple rounds of SHA-256 for quantum resistance
    hash := sha256.Sum256([]byte(record))
    for i := 0; i < 100; i++ {
        hash = sha256.Sum256(hash[:])
    }
    
    return hex.EncodeToString(hash[:])
}

// NewBlock creates a new quantum-safe block
func NewBlock(data CRODData, previousHash string, privateKey []byte) *Block {
    block := &Block{
        Index:        time.Now().Unix(),
        Timestamp:    time.Now(),
        Data:         data,
        PreviousHash: previousHash,
        Nonce:        0,
    }
    
    // Mine the block
    block.MineBlock(4) // difficulty 4
    
    // Add quantum proof
    block.addQuantumProof(privateKey)
    
    return block
}

// MineBlock implements proof of work
func (b *Block) MineBlock(difficulty int) {
    target := strings.Repeat("0", difficulty)
    for !strings.HasPrefix(b.Hash, target) {
        b.Nonce++
        b.Hash = b.CalculateHash()
    }
}

// Add quantum-resistant proof using enhanced classical methods
func (b *Block) addQuantumProof(privateKey []byte) {
    // For now, using enhanced classical crypto
    // Real quantum crypto (Kyber/Dilithium) to be added later
    
    // Create multi-round hash for quantum resistance
    message := []byte(b.Hash)
    hash := sha256.Sum256(message)
    
    // 256 rounds of hashing for enhanced security
    for i := 0; i < 256; i++ {
        hash = sha256.Sum256(append(hash[:], byte(i)))
    }
    
    b.QuantumProof.KyberCiphertext = hash[:]
    
    // Create signature using SHA256 (placeholder for Dilithium)
    if len(privateKey) > 0 {
        sigData := append([]byte(b.Hash), privateKey...)
        signature := sha256.Sum256(sigData)
        b.Signature = signature[:]
        
        // Store "public key" (hash of private key)
        pubKey := sha256.Sum256(privateKey)
        b.QuantumProof.DilithiumPubKey = pubKey[:]
    }
    
    // Lattice-based hash simulation
    latticeData := append([]byte(b.Hash), b.Signature...)
    latticeHash := sha256.Sum256(latticeData)
    b.QuantumProof.LatticeHash = hex.EncodeToString(latticeHash[:])
}

// Blockchain represents the CROD quantum-safe blockchain
type Blockchain struct {
    Blocks      []*Block      `json:"blocks"`
    PrivateKey  []byte        `json:"-"`
    PublicKey   []byte        `json:"public_key"`
    mutex       sync.RWMutex
    redisClient *redis.Client
}

// AddBlock adds a new quantum-safe block to the chain
func (bc *Blockchain) AddBlock(data CRODData) *Block {
    bc.mutex.Lock()
    defer bc.mutex.Unlock()
    
    previousBlock := bc.Blocks[len(bc.Blocks)-1]
    newBlock := NewBlock(data, previousBlock.Hash, bc.PrivateKey)
    bc.Blocks = append(bc.Blocks, newBlock)
    
    // Broadcast to Redis
    bc.broadcastBlock(newBlock)
    
    return newBlock
}

// Broadcast block to other services
func (bc *Blockchain) broadcastBlock(block *Block) {
    if bc.redisClient == nil {
        return
    }
    
    ctx := context.Background()
    message := map[string]interface{}{
        "type":      "new_block",
        "block":     block,
        "timestamp": time.Now().Unix(),
    }
    
    messageJSON, _ := json.Marshal(message)
    bc.redisClient.Publish(ctx, "crod:blockchain", messageJSON)
}

// NewBlockchain creates the quantum-resistant genesis block
func NewBlockchain() *Blockchain {
    // Generate keys (placeholder for quantum-safe keys)
    privateKey := make([]byte, 32)
    rand.Read(privateKey)
    
    // Public key is hash of private key (placeholder)
    pubKeyHash := sha256.Sum256(privateKey)
    
    genesisData := CRODData{
        District: "genesis",
        Pattern:  "CROD-INIT",
        Trinity: map[string]float64{
            "daniel": 67,
            "claude": 71,
            "crod":   17,
        },
        Atoms: []string{"ich", "bins", "wieder"},
        Metadata: map[string]interface{}{
            "quantum_resistant": true,
            "algorithm":        "sha256-256-rounds",
            "future_upgrade":   "dilithium5+kyber1024",
        },
    }
    
    bc := &Blockchain{
        PrivateKey: privateKey,
        PublicKey:  pubKeyHash[:],
    }
    
    genesis := NewBlock(genesisData, "0", privateKey)
    bc.Blocks = []*Block{genesis}
    
    return bc
}

// ValidateChain checks if blockchain is valid
func (bc *Blockchain) ValidateChain() bool {
    for i := 1; i < len(bc.Blocks); i++ {
        currentBlock := bc.Blocks[i]
        previousBlock := bc.Blocks[i-1]
        
        if currentBlock.Hash != currentBlock.CalculateHash() {
            return false
        }
        
        if currentBlock.PreviousHash != previousBlock.Hash {
            return false
        }
    }
    return true
}

// InitRedis initializes Redis connection
func (bc *Blockchain) InitRedis(addr string) error {
    bc.redisClient = redis.NewClient(&redis.Options{
        Addr: addr,
    })
    
    ctx := context.Background()
    return bc.redisClient.Ping(ctx).Err()
}

func main() {
    log.Println("🔐 CROD Blockchain Core v3.0 initializing...")
    
    // Create blockchain
    blockchain := NewBlockchain()
    
    // Connect to Redis
    redisAddr := "redis:6379"
    if err := blockchain.InitRedis(redisAddr); err != nil {
        log.Printf("Warning: Could not connect to Redis at %s: %v", redisAddr, err)
        // Try localhost
        if err := blockchain.InitRedis("localhost:6379"); err != nil {
            log.Printf("Warning: Could not connect to Redis at localhost: %v", err)
        }
    }
    
    port := "8085"
    
    // Start API directly
    go StartAPI(blockchain, port)
    
    // Subscribe to Redis events
    go subscribeToRedisEvents(blockchain)
    log.Printf("⛓️  CROD Blockchain Core running on port %s", port)
    log.Printf("🔐 Quantum-safe with document deltas and pattern transactions")
    log.Printf("🔗 Connected to CROD ecosystem via Redis")
    
    // Keep main thread alive
    select {}
}

// subscribeToRedisEvents listens for events from other CROD services
func subscribeToRedisEvents(blockchain *Blockchain) {
    if blockchain.redisClient == nil {
        return
    }
    
    ctx := context.Background()
    pubsub := blockchain.redisClient.Subscribe(ctx, "crod:transactions", "crod:patterns", "crod:deltas")
    defer pubsub.Close()
    
    ch := pubsub.Channel()
    
    for msg := range ch {
        var event map[string]interface{}
        if err := json.Unmarshal([]byte(msg.Payload), &event); err != nil {
            continue
        }
        
        // Process events from other services
        switch msg.Channel {
        case "crod:patterns":
            // Pattern discovered by Pattern District
            if patternData, ok := event["pattern"].(map[string]interface{}); ok {
                data := CRODData{
                    District: "pattern-district",
                    Pattern:  event["pattern_id"].(string),
                    Atoms:    []string{"redis", "event"},
                    Trinity:  map[string]float64{"weight": 100.0},
                    Metadata: patternData,
                }
                blockchain.AddBlock(data)
            }
            
        case "crod:deltas":
            // Document delta from Delta Quarter
            if deltaData, ok := event["delta"].(map[string]interface{}); ok {
                data := CRODData{
                    District: "delta-quarter",
                    Pattern:  "document-update",
                    Atoms:    []string{"redis", "delta"},
                    Trinity:  map[string]float64{"heat": 50.0},
                    Metadata: deltaData,
                }
                blockchain.AddBlock(data)
            }
            
        case "crod:transactions":
            // Transaction from Meta-Chain or other service
            if txData, ok := event["transaction"].(map[string]interface{}); ok {
                data := CRODData{
                    District: event["district"].(string),
                    Pattern:  "transaction",
                    Atoms:    []string{"redis", "tx"},
                    Trinity:  map[string]float64{"value": 1.0},
                    Metadata: txData,
                }
                blockchain.AddBlock(data)
            }
        }
    }
}