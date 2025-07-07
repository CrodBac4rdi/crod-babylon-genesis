package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "sync"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/nats-io/nats.go"
)

type MemoryStore struct {
    mu    sync.RWMutex
    data  map[string]interface{}
    stats map[string]int
}

type ServiceInfo struct {
    Service  string `json:"service"`
    Port     int    `json:"port"`
    Status   string `json:"status"`
    Memories int    `json:"memories"`
}

var (
    store *MemoryStore
    nc    *nats.Conn
)

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "7031"
    }

    natsURL := os.Getenv("NATS_URL")
    if natsURL == "" {
        natsURL = "nats://localhost:4222"
    }

    // Initialize memory store
    store = &MemoryStore{
        data:  make(map[string]interface{}),
        stats: make(map[string]int),
    }

    // Connect to NATS
    var err error
    nc, err = nats.Connect(natsURL)
    if err != nil {
        log.Printf("Failed to connect to NATS: %v", err)
    } else {
        log.Printf("Connected to NATS at %s", natsURL)
        
        // Announce presence
        announcement := map[string]interface{}{
            "district": "go-memory",
            "port":     7031,
        }
        data, _ := json.Marshal(announcement)
        nc.Publish("crod.district.online", data)

        // Subscribe to memory operations
        nc.Subscribe("crod.memory.>", handleMemoryMessage)
    }

    // Setup Gin router
    gin.SetMode(gin.ReleaseMode)
    r := gin.Default()

    r.GET("/", getIndex)
    r.GET("/memory/:key", getMemory)
    r.POST("/memory/:key", setMemory)
    r.DELETE("/memory/:key", deleteMemory)
    r.GET("/stats", getStats)

    log.Printf("Go Memory Quarter listening on port %s", port)
    r.Run(":" + port)
}

func handleMemoryMessage(msg *nats.Msg) {
    log.Printf("Received message on %s", msg.Subject)
}

func getIndex(c *gin.Context) {
    store.mu.RLock()
    memCount := len(store.data)
    store.mu.RUnlock()

    c.JSON(http.StatusOK, ServiceInfo{
        Service:  "CROD Go Memory Quarter",
        Port:     7031,
        Status:   "storing",
        Memories: memCount,
    })
}

func getMemory(c *gin.Context) {
    key := c.Param("key")
    
    store.mu.RLock()
    value, exists := store.data[key]
    store.stats["reads"]++
    store.mu.RUnlock()

    if !exists {
        c.JSON(http.StatusNotFound, gin.H{"error": "key not found"})
        return
    }

    c.JSON(http.StatusOK, gin.H{
        "key":   key,
        "value": value,
        "timestamp": time.Now().Unix(),
    })
}

func setMemory(c *gin.Context) {
    key := c.Param("key")
    
    var body map[string]interface{}
    if err := c.ShouldBindJSON(&body); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    store.mu.Lock()
    store.data[key] = body["value"]
    store.stats["writes"]++
    store.mu.Unlock()

    // Publish to NATS
    if nc != nil {
        msg := map[string]interface{}{
            "action": "set",
            "key":    key,
            "value":  body["value"],
        }
        data, _ := json.Marshal(msg)
        nc.Publish("crod.memory.set", data)
    }

    c.JSON(http.StatusOK, gin.H{
        "status": "stored",
        "key":    key,
    })
}

func deleteMemory(c *gin.Context) {
    key := c.Param("key")
    
    store.mu.Lock()
    delete(store.data, key)
    store.stats["deletes"]++
    store.mu.Unlock()

    c.JSON(http.StatusOK, gin.H{
        "status": "deleted",
        "key":    key,
    })
}

func getStats(c *gin.Context) {
    store.mu.RLock()
    stats := make(map[string]int)
    for k, v := range store.stats {
        stats[k] = v
    }
    stats["total_keys"] = len(store.data)
    store.mu.RUnlock()

    c.JSON(http.StatusOK, stats)
}