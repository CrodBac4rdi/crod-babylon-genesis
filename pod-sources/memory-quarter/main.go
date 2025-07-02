package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "sync"
    "time"

    "github.com/go-redis/redis/v8"
    "github.com/gorilla/mux"
)

type Atom struct {
    Word  string    `json:"word"`
    Heat  float64   `json:"heat"`
    Prime int       `json:"prime,omitempty"`
    Time  time.Time `json:"time"`
}

type Memory struct {
    ID        string    `json:"id"`
    Atoms     []Atom    `json:"atoms"`
    CreatedAt time.Time `json:"created_at"`
    Type      string    `json:"type"` // short_term, working, long_term
}

type MemoryQuarter struct {
    shortTerm sync.Map // Recent memories
    working   sync.Map // Active processing
    longTerm  sync.Map // Important patterns
    redis     *redis.Client
    mu        sync.RWMutex
}

func NewMemoryQuarter() *MemoryQuarter {
    redisAddr := os.Getenv("REDIS_ADDR")
    if redisAddr == "" {
        redisAddr = "redis:6379"
    }

    rdb := redis.NewClient(&redis.Options{
        Addr: redisAddr,
    })

    return &MemoryQuarter{
        redis: rdb,
    }
}

func (mq *MemoryQuarter) StoreMemory(mem Memory) error {
    // Determine memory type based on heat
    totalHeat := 0.0
    for _, atom := range mem.Atoms {
        totalHeat += atom.Heat
    }
    avgHeat := totalHeat / float64(len(mem.Atoms))

    // Store in appropriate memory bank
    if avgHeat > 70 {
        mem.Type = "long_term"
        mq.longTerm.Store(mem.ID, mem)
    } else if avgHeat > 50 {
        mem.Type = "working"
        mq.working.Store(mem.ID, mem)
    } else {
        mem.Type = "short_term"
        mq.shortTerm.Store(mem.ID, mem)
    }

    // Publish to Redis
    ctx := context.Background()
    msg, _ := json.Marshal(map[string]interface{}{
        "from":     "memory-quarter",
        "type":     "memory_stored",
        "memory_id": mem.ID,
        "memory_type": mem.Type,
        "avg_heat": avgHeat,
    })
    
    mq.redis.Publish(ctx, "crod:memory", string(msg))

    // Cleanup old short-term memories
    go mq.cleanupShortTerm()

    return nil
}

func (mq *MemoryQuarter) cleanupShortTerm() {
    cutoff := time.Now().Add(-5 * time.Minute)
    
    mq.shortTerm.Range(func(key, value interface{}) bool {
        if mem, ok := value.(Memory); ok {
            if mem.CreatedAt.Before(cutoff) {
                mq.shortTerm.Delete(key)
            }
        }
        return true
    })
}

func (mq *MemoryQuarter) GetMemoryStats() map[string]interface{} {
    shortCount := 0
    workingCount := 0
    longCount := 0

    mq.shortTerm.Range(func(_, _ interface{}) bool {
        shortCount++
        return true
    })

    mq.working.Range(func(_, _ interface{}) bool {
        workingCount++
        return true
    })

    mq.longTerm.Range(func(_, _ interface{}) bool {
        longCount++
        return true
    })

    return map[string]interface{}{
        "short_term_memories": shortCount,
        "working_memories":    workingCount,
        "long_term_memories":  longCount,
        "total_memories":      shortCount + workingCount + longCount,
    }
}

// HTTP Handlers
func (mq *MemoryQuarter) healthHandler(w http.ResponseWriter, r *http.Request) {
    stats := mq.GetMemoryStats()
    stats["status"] = "healthy"
    stats["district"] = "memory-quarter"
    stats["language"] = "go"
    stats["port"] = 7031

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(stats)
}

func (mq *MemoryQuarter) storeHandler(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Atoms []Atom `json:"atoms"`
    }

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    memory := Memory{
        ID:        fmt.Sprintf("mem_%d", time.Now().UnixNano()),
        Atoms:     req.Atoms,
        CreatedAt: time.Now(),
    }

    if err := mq.StoreMemory(memory); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "memory_id": memory.ID,
        "type":      memory.Type,
        "stored":    true,
    })
}

func (mq *MemoryQuarter) recallHandler(w http.ResponseWriter, r *http.Request) {
    memType := r.URL.Query().Get("type")
    if memType == "" {
        memType = "all"
    }

    memories := []Memory{}

    collectMemories := func(store *sync.Map) {
        store.Range(func(key, value interface{}) bool {
            if mem, ok := value.(Memory); ok {
                memories = append(memories, mem)
            }
            return true
        })
    }

    switch memType {
    case "short_term":
        collectMemories(&mq.shortTerm)
    case "working":
        collectMemories(&mq.working)
    case "long_term":
        collectMemories(&mq.longTerm)
    default:
        collectMemories(&mq.shortTerm)
        collectMemories(&mq.working)
        collectMemories(&mq.longTerm)
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "memories": memories,
        "count":    len(memories),
        "type":     memType,
    })
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "7031"
    }

    mq := NewMemoryQuarter()

    // Test Redis connection
    ctx := context.Background()
    if err := mq.redis.Ping(ctx).Err(); err != nil {
        log.Printf("Warning: Redis connection failed: %v", err)
    } else {
        log.Println("✅ Connected to Redis")
    }

    router := mux.NewRouter()
    router.HandleFunc("/health", mq.healthHandler).Methods("GET")
    router.HandleFunc("/store", mq.storeHandler).Methods("POST")
    router.HandleFunc("/recall", mq.recallHandler).Methods("GET")

    log.Printf("🧠 Memory Quarter (Go) starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, router))
}