package main

import (
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "log"
    "math/big"
    "net/http"
    "os"
    "sync"
    "time"

    "github.com/go-redis/redis/v8"
    "github.com/gorilla/mux"
    "github.com/sergi/go-diff/diffmatchpatch"
    "context"
)

// CROD Hash-Document Delta System
type DocumentDelta struct {
    DocumentHash    string          `json:"document_hash"`
    PreviousHash    string          `json:"previous_hash"`
    Delta          json.RawMessage `json:"delta"`
    DeltaType      string          `json:"delta_type"` // "add", "modify", "remove"
    Timestamp      int64           `json:"timestamp"`
    PrimeReference *big.Int        `json:"prime_reference"`
    Heat           float64         `json:"heat"`
    AtomWeight     float64         `json:"atom_weight"`
}

type DeltaChain struct {
    DocumentID string           `json:"document_id"`
    Deltas     []DocumentDelta `json:"deltas"`
    HeadHash   string          `json:"head_hash"`
    TotalHeat  float64         `json:"total_heat"`
}

type DeltaQuarter struct {
    chains      map[string]*DeltaChain
    chainsMutex sync.RWMutex
    redisClient *redis.Client
    dmp         *diffmatchpatch.DiffMatchPatch
}

// Hash to Prime conversion - CROD style
func hashToPrime(hash string) *big.Int {
    // Convert hash to number
    hashBytes, _ := hex.DecodeString(hash[:16]) // Use first 16 chars for manageable primes
    num := new(big.Int).SetBytes(hashBytes)
    
    // Find next prime
    for !num.ProbablyPrime(20) {
        num.Add(num, big.NewInt(1))
    }
    return num
}

// Calculate document heat based on changes
func calculateHeat(deltaSize int, frequency float64) float64 {
    // CROD heat formula: size of change + frequency
    baseHeat := float64(deltaSize) / 100.0
    return baseHeat * (1 + frequency)
}

// Process document update
func (dq *DeltaQuarter) ProcessDelta(documentID string, content []byte, previousContent []byte) (*DocumentDelta, error) {
    // Calculate hashes
    currentHash := sha256.Sum256(content)
    currentHashStr := hex.EncodeToString(currentHash[:])
    
    previousHash := sha256.Sum256(previousContent)
    previousHashStr := hex.EncodeToString(previousHash[:])
    
    // Calculate text diff
    diffs := dq.dmp.DiffMain(string(previousContent), string(content), false)
    patches := dq.dmp.PatchMake(string(previousContent), diffs)
    
    deltaJSON, _ := json.Marshal(map[string]interface{}{
        "patches": dq.dmp.PatchToText(patches),
        "additions": countAdditions(diffs),
        "deletions": countDeletions(diffs),
    })
    
    // Determine delta type
    deltaType := "modify"
    if len(previousContent) == 0 {
        deltaType = "add"
    } else if len(content) == 0 {
        deltaType = "remove"
    }
    
    // Calculate heat
    heat := calculateHeat(len(patches), 1.0)
    
    // Create delta object
    delta := &DocumentDelta{
        DocumentHash:   currentHashStr,
        PreviousHash:   previousHashStr,
        Delta:         deltaJSON,
        DeltaType:     deltaType,
        Timestamp:     time.Now().Unix(),
        PrimeReference: hashToPrime(currentHashStr),
        Heat:          heat,
        AtomWeight:    100.0, // CROD default atom weight
    }
    
    // Update chain
    dq.chainsMutex.Lock()
    chain, exists := dq.chains[documentID]
    if !exists {
        chain = &DeltaChain{
            DocumentID: documentID,
            Deltas:     []DocumentDelta{},
        }
        dq.chains[documentID] = chain
    }
    
    chain.Deltas = append(chain.Deltas, *delta)
    chain.HeadHash = delta.DocumentHash
    chain.TotalHeat += heat
    dq.chainsMutex.Unlock()
    
    // Broadcast to Redis
    dq.broadcastDelta(documentID, delta)
    
    return delta, nil
}

// Broadcast delta to other services via Redis
func (dq *DeltaQuarter) broadcastDelta(documentID string, delta *DocumentDelta) {
    ctx := context.Background()
    
    message := map[string]interface{}{
        "type":        "document_delta",
        "document_id": documentID,
        "delta":       delta,
        "timestamp":   time.Now().Unix(),
    }
    
    messageJSON, _ := json.Marshal(message)
    
    // Publish to CROD channels
    dq.redisClient.Publish(ctx, "crod:deltas", messageJSON)
    dq.redisClient.Publish(ctx, fmt.Sprintf("crod:document:%s", documentID), messageJSON)
}

// Get delta history for a document
func (dq *DeltaQuarter) GetDeltaHistory(documentID string) (*DeltaChain, error) {
    dq.chainsMutex.RLock()
    defer dq.chainsMutex.RUnlock()
    
    chain, exists := dq.chains[documentID]
    if !exists {
        return nil, fmt.Errorf("document not found: %s", documentID)
    }
    
    return chain, nil
}

// Helper functions
func countAdditions(diffs []diffmatchpatch.Diff) int {
    count := 0
    for _, diff := range diffs {
        if diff.Type == diffmatchpatch.DiffInsert {
            count += len(diff.Text)
        }
    }
    return count
}

func countDeletions(diffs []diffmatchpatch.Diff) int {
    count := 0
    for _, diff := range diffs {
        if diff.Type == diffmatchpatch.DiffDelete {
            count += len(diff.Text)
        }
    }
    return count
}

// HTTP Handlers
func (dq *DeltaQuarter) handleProcessDelta(w http.ResponseWriter, r *http.Request) {
    var req struct {
        DocumentID      string `json:"document_id"`
        Content         string `json:"content"`
        PreviousContent string `json:"previous_content"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    delta, err := dq.ProcessDelta(
        req.DocumentID,
        []byte(req.Content),
        []byte(req.PreviousContent),
    )
    
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(delta)
}

func (dq *DeltaQuarter) handleGetHistory(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    documentID := vars["documentId"]
    
    chain, err := dq.GetDeltaHistory(documentID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
        return
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(chain)
}

func (dq *DeltaQuarter) handleHealth(w http.ResponseWriter, r *http.Request) {
    dq.chainsMutex.RLock()
    totalChains := len(dq.chains)
    totalDeltas := 0
    totalHeat := 0.0
    
    for _, chain := range dq.chains {
        totalDeltas += len(chain.Deltas)
        totalHeat += chain.TotalHeat
    }
    dq.chainsMutex.RUnlock()
    
    health := map[string]interface{}{
        "service":      "delta-quarter",
        "status":       "healthy",
        "chains":       totalChains,
        "total_deltas": totalDeltas,
        "total_heat":   totalHeat,
        "timestamp":    time.Now().Unix(),
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(health)
}

func main() {
    // Initialize Delta Quarter
    dq := &DeltaQuarter{
        chains: make(map[string]*DeltaChain),
        dmp:    diffmatchpatch.New(),
    }
    
    // Connect to Redis
    redisAddr := "redis:6379"
    if addr := getEnv("REDIS_ADDR", ""); addr != "" {
        redisAddr = addr
    }
    
    dq.redisClient = redis.NewClient(&redis.Options{
        Addr: redisAddr,
    })
    
    ctx := context.Background()
    if err := dq.redisClient.Ping(ctx).Err(); err != nil {
        log.Printf("Warning: Could not connect to Redis: %v", err)
    } else {
        log.Printf("Connected to Redis at %s", redisAddr)
    }
    
    // Setup routes
    router := mux.NewRouter()
    router.HandleFunc("/delta/process", dq.handleProcessDelta).Methods("POST")
    router.HandleFunc("/delta/history/{documentId}", dq.handleGetHistory).Methods("GET")
    router.HandleFunc("/health", dq.handleHealth).Methods("GET")
    
    // CROD Delta Quarter info
    router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        info := map[string]interface{}{
            "service":     "CROD Delta Quarter",
            "version":     "1.0.0",
            "description": "Hash-Document Delta Tracking System",
            "features": []string{
                "Document hash to prime conversion",
                "Delta calculation and storage",
                "Heat tracking for active documents",
                "Redis pub/sub integration",
                "Pattern emergence through primes",
            },
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(info)
    }).Methods("GET")
    
    port := getEnv("PORT", "8087")
    log.Printf("🔺 CROD Delta Quarter starting on port %s", port)
    log.Printf("📊 Hash-Document Delta System Active")
    log.Fatal(http.ListenAndServe(":"+port, router))
}

func getEnv(key, defaultValue string) string {
    if value, exists := os.LookupEnv(key); exists {
        return value
    }
    return defaultValue
}