package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "sync"
    "time"

    "github.com/gorilla/mux"
    "github.com/nats-io/nats.go"
)

type Memory struct {
    ID        string    `json:"id"`
    Data      string    `json:"data"`
    Timestamp time.Time `json:"timestamp"`
}

type MemoryStore struct {
    mu       sync.RWMutex
    memories map[string]*Memory
    sessions map[string][]string
}

func NewMemoryStore() *MemoryStore {
    return &MemoryStore{
        memories: make(map[string]*Memory),
        sessions: make(map[string][]string),
    }
}

func (ms *MemoryStore) Store(memory *Memory) {
    ms.mu.Lock()
    defer ms.mu.Unlock()
    ms.memories[memory.ID] = memory
}

func (ms *MemoryStore) Get(id string) (*Memory, bool) {
    ms.mu.RLock()
    defer ms.mu.RUnlock()
    mem, ok := ms.memories[id]
    return mem, ok
}

func (ms *MemoryStore) StartSession(sessionID string) {
    ms.mu.Lock()
    defer ms.mu.Unlock()
    ms.sessions[sessionID] = []string{}
}

func main() {
    store := NewMemoryStore()
    
    // Connect to NATS
    nc, err := nats.Connect("nats://nats:4222")
    if err != nil {
        log.Fatal("Failed to connect to NATS:", err)
    }
    defer nc.Close()

    // Subscribe to memory events
    nc.Subscribe("crod.memory.>", func(m *nats.Msg) {
        var memory Memory
        if err := json.Unmarshal(m.Data, &memory); err == nil {
            store.Store(&memory)
            log.Printf("Stored memory: %s", memory.ID)
        }
    })

    // Start concurrent memory workers
    for i := 0; i < 10; i++ {
        go memoryWorker(i, store, nc)
    }

    // Setup HTTP routes
    r := mux.NewRouter()
    r.HandleFunc("/", healthHandler).Methods("GET")
    r.HandleFunc("/memories", getMemoriesHandler(store)).Methods("GET")
    r.HandleFunc("/sessions", getSessionsHandler(store)).Methods("GET")

    log.Println("Memory Quarter listening on :7031")
    log.Fatal(http.ListenAndServe(":7031", r))
}

func memoryWorker(id int, store *MemoryStore, nc *nats.Connection) {
    for {
        memory := &Memory{
            ID:        fmt.Sprintf("worker_%d_%d", id, time.Now().Unix()),
            Data:      fmt.Sprintf("Memory from worker %d", id),
            Timestamp: time.Now(),
        }
        
        store.Store(memory)
        
        if data, err := json.Marshal(memory); err == nil {
            nc.Publish("crod.memory.created", data)
        }
        
        time.Sleep(time.Duration(5+id) * time.Second)
    }
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Memory Quarter Online"))
}

func getMemoriesHandler(store *MemoryStore) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        store.mu.RLock()
        defer store.mu.RUnlock()
        
        memories := make([]*Memory, 0, len(store.memories))
        for _, mem := range store.memories {
            memories = append(memories, mem)
        }
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(memories)
    }
}

func getSessionsHandler(store *MemoryStore) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        store.mu.RLock()
        defer store.mu.RUnlock()
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(store.sessions)
    }
}
