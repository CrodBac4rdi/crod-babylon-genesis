package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "sync"
    "sync/atomic"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/gorilla/websocket"
    "github.com/nats-io/nats.go"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "github.com/redis/go-redis/v9"
    "go.uber.org/zap"
)

type MemoryQuarter struct {
    nc          *nats.Conn
    redis       *redis.Client
    logger      *zap.Logger
    stores      map[string]*MemoryStore
    mu          sync.RWMutex
    stats       *Statistics
    wsUpgrader  websocket.Upgrader
    wsClients   sync.Map
}

type MemoryStore struct {
    name        string
    data        sync.Map
    capacity    int64
    used        int64
    lastAccess  time.Time
    mu          sync.RWMutex
}

type Statistics struct {
    TotalOperations  uint64
    CacheHits        uint64
    CacheMisses      uint64
    ActiveStores     int32
    TotalMemoryUsed  int64
}

type MemoryEntry struct {
    Key       string      `json:"key"`
    Value     interface{} `json:"value"`
    TTL       int         `json:"ttl,omitempty"`
    Timestamp time.Time   `json:"timestamp"`
}

var (
    opsCounter = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "memory_quarter_operations_total",
            Help: "Total number of memory operations",
        },
        []string{"operation", "store"},
    )
    
    memoryGauge = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "memory_quarter_usage_bytes",
            Help: "Memory usage in bytes",
        },
        []string{"store"},
    )
)

func init() {
    prometheus.MustRegister(opsCounter)
    prometheus.MustRegister(memoryGauge)
}

func main() {
    logger, _ := zap.NewProduction()
    defer logger.Sync()

    mq := &MemoryQuarter{
        logger:     logger,
        stores:     make(map[string]*MemoryStore),
        stats:      &Statistics{},
        wsUpgrader: websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }},
    }

    // Connect to NATS
    natsHost := os.Getenv("NATS_HOST")
    if natsHost == "" {
        natsHost = "localhost"
    }
    
    nc, err := nats.Connect(fmt.Sprintf("nats://%s:4222", natsHost))
    if err != nil {
        logger.Fatal("Failed to connect to NATS", zap.Error(err))
    }
    mq.nc = nc
    defer nc.Close()

    // Connect to Redis
    redisHost := os.Getenv("REDIS_HOST")
    if redisHost == "" {
        redisHost = "localhost"
    }
    
    mq.redis = redis.NewClient(&redis.Options{
        Addr: fmt.Sprintf("%s:6379", redisHost),
    })
    
    ctx := context.Background()
    if err := mq.redis.Ping(ctx).Err(); err != nil {
        logger.Fatal("Failed to connect to Redis", zap.Error(err))
    }

    // Initialize default stores
    mq.createStore("patterns", 1000)
    mq.createStore("sessions", 500)
    mq.createStore("cache", 2000)

    // Start NATS subscriptions
    mq.startSubscriptions()

    // Announce to Phoenix Rathaus
    mq.announceDistrict()

    // Setup Gin router
    gin.SetMode(gin.ReleaseMode)
    r := gin.New()
    r.Use(gin.Recovery())

    // Routes
    r.GET("/", mq.handleRoot)
    r.GET("/health", mq.handleHealth)
    r.GET("/metrics", gin.WrapH(promhttp.Handler()))
    r.POST("/store/:name/set", mq.handleSet)
    r.GET("/store/:name/get/:key", mq.handleGet)
    r.DELETE("/store/:name/delete/:key", mq.handleDelete)
    r.GET("/stores", mq.handleListStores)
    r.POST("/stores/create", mq.handleCreateStore)
    r.GET("/stats", mq.handleStats)
    r.GET("/ws", mq.handleWebSocket)

    logger.Info("🏛️ Go Memory Quarter starting on port 7031")
    log.Fatal(r.Run(":7031"))
}

func (mq *MemoryQuarter) createStore(name string, capacity int64) *MemoryStore {
    mq.mu.Lock()
    defer mq.mu.Unlock()

    store := &MemoryStore{
        name:       name,
        capacity:   capacity,
        lastAccess: time.Now(),
    }
    
    mq.stores[name] = store
    atomic.AddInt32(&mq.stats.ActiveStores, 1)
    
    mq.logger.Info("Created memory store", zap.String("name", name), zap.Int64("capacity", capacity))
    return store
}

func (mq *MemoryQuarter) startSubscriptions() {
    // Subscribe to memory operations
    mq.nc.Subscribe("memory.set", func(msg *nats.Msg) {
        var entry MemoryEntry
        if err := json.Unmarshal(msg.Data, &entry); err != nil {
            mq.logger.Error("Failed to unmarshal memory entry", zap.Error(err))
            return
        }

        store := mq.getOrCreateStore("default")
        store.Set(entry.Key, entry.Value, time.Duration(entry.TTL)*time.Second)
        
        atomic.AddUint64(&mq.stats.TotalOperations, 1)
        opsCounter.WithLabelValues("set", "default").Inc()

        if msg.Reply != "" {
            response := map[string]string{"status": "success", "key": entry.Key}
            data, _ := json.Marshal(response)
            mq.nc.Publish(msg.Reply, data)
        }
    })

    mq.nc.Subscribe("memory.get", func(msg *nats.Msg) {
        var request map[string]string
        if err := json.Unmarshal(msg.Data, &request); err != nil {
            return
        }

        store := mq.getOrCreateStore("default")
        value, found := store.Get(request["key"])
        
        atomic.AddUint64(&mq.stats.TotalOperations, 1)
        if found {
            atomic.AddUint64(&mq.stats.CacheHits, 1)
        } else {
            atomic.AddUint64(&mq.stats.CacheMisses, 1)
        }

        if msg.Reply != "" {
            response := map[string]interface{}{
                "found": found,
                "value": value,
            }
            data, _ := json.Marshal(response)
            mq.nc.Publish(msg.Reply, data)
        }
    })

    mq.logger.Info("Started NATS subscriptions")
}

func (mq *MemoryQuarter) announceDistrict() {
    announcement := map[string]interface{}{
        "district":     "go_memory",
        "status":       "online",
        "port":         7031,
        "capabilities": []string{"memory_management", "caching", "session_storage"},
    }
    
    data, _ := json.Marshal(announcement)
    mq.nc.Publish("district.announce", data)
    
    mq.logger.Info("Announced Go Memory Quarter to Phoenix Rathaus")
}

func (mq *MemoryQuarter) getOrCreateStore(name string) *MemoryStore {
    mq.mu.RLock()
    store, exists := mq.stores[name]
    mq.mu.RUnlock()

    if !exists {
        store = mq.createStore(name, 1000)
    }
    
    return store
}

// MemoryStore methods
func (ms *MemoryStore) Set(key string, value interface{}, ttl time.Duration) {
    ms.mu.Lock()
    defer ms.mu.Unlock()

    ms.data.Store(key, value)
    ms.lastAccess = time.Now()
    atomic.AddInt64(&ms.used, 1)
    
    memoryGauge.WithLabelValues(ms.name).Set(float64(ms.used))

    if ttl > 0 {
        time.AfterFunc(ttl, func() {
            ms.Delete(key)
        })
    }
}

func (ms *MemoryStore) Get(key string) (interface{}, bool) {
    ms.mu.RLock()
    defer ms.mu.RUnlock()

    ms.lastAccess = time.Now()
    return ms.data.Load(key)
}

func (ms *MemoryStore) Delete(key string) {
    ms.mu.Lock()
    defer ms.mu.Unlock()

    if _, existed := ms.data.LoadAndDelete(key); existed {
        atomic.AddInt64(&ms.used, -1)
        memoryGauge.WithLabelValues(ms.name).Set(float64(ms.used))
    }
}

// HTTP Handlers
func (mq *MemoryQuarter) handleRoot(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "service":      "Go Memory Quarter",
        "version":      "1.0.0",
        "status":       "operational",
        "capabilities": []string{"memory_management", "caching", "session_storage"},
    })
}

func (mq *MemoryQuarter) handleHealth(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "status":    "healthy",
        "timestamp": time.Now(),
    })
}

func (mq *MemoryQuarter) handleSet(c *gin.Context) {
    storeName := c.Param("name")
    var entry MemoryEntry
    
    if err := c.ShouldBindJSON(&entry); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    store := mq.getOrCreateStore(storeName)
    store.Set(entry.Key, entry.Value, time.Duration(entry.TTL)*time.Second)
    
    c.JSON(http.StatusOK, gin.H{
        "status": "success",
        "key":    entry.Key,
        "store":  storeName,
    })
}

func (mq *MemoryQuarter) handleGet(c *gin.Context) {
    storeName := c.Param("name")
    key := c.Param("key")

    store := mq.getOrCreateStore(storeName)
    value, found := store.Get(key)
    
    c.JSON(http.StatusOK, gin.H{
        "found": found,
        "value": value,
        "store": storeName,
    })
}

func (mq *MemoryQuarter) handleDelete(c *gin.Context) {
    storeName := c.Param("name")
    key := c.Param("key")

    store := mq.getOrCreateStore(storeName)
    store.Delete(key)
    
    c.JSON(http.StatusOK, gin.H{
        "status": "deleted",
        "key":    key,
        "store":  storeName,
    })
}

func (mq *MemoryQuarter) handleListStores(c *gin.Context) {
    mq.mu.RLock()
    defer mq.mu.RUnlock()

    stores := make(map[string]interface{})
    for name, store := range mq.stores {
        stores[name] = map[string]interface{}{
            "capacity":    store.capacity,
            "used":        atomic.LoadInt64(&store.used),
            "lastAccess":  store.lastAccess,
        }
    }
    
    c.JSON(http.StatusOK, stores)
}

func (mq *MemoryQuarter) handleCreateStore(c *gin.Context) {
    var request struct {
        Name     string `json:"name" binding:"required"`
        Capacity int64  `json:"capacity"`
    }
    
    if err := c.ShouldBindJSON(&request); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    if request.Capacity == 0 {
        request.Capacity = 1000
    }

    mq.createStore(request.Name, request.Capacity)
    
    c.JSON(http.StatusOK, gin.H{
        "status":   "created",
        "name":     request.Name,
        "capacity": request.Capacity,
    })
}

func (mq *MemoryQuarter) handleStats(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
        "totalOperations": atomic.LoadUint64(&mq.stats.TotalOperations),
        "cacheHits":       atomic.LoadUint64(&mq.stats.CacheHits),
        "cacheMisses":     atomic.LoadUint64(&mq.stats.CacheMisses),
        "activeStores":    atomic.LoadInt32(&mq.stats.ActiveStores),
        "totalMemoryUsed": atomic.LoadInt64(&mq.stats.TotalMemoryUsed),
    })
}

func (mq *MemoryQuarter) handleWebSocket(c *gin.Context) {
    conn, err := mq.wsUpgrader.Upgrade(c.Writer, c.Request, nil)
    if err != nil {
        mq.logger.Error("WebSocket upgrade failed", zap.Error(err))
        return
    }
    defer conn.Close()

    clientID := fmt.Sprintf("client_%d", time.Now().UnixNano())
    mq.wsClients.Store(clientID, conn)
    defer mq.wsClients.Delete(clientID)

    // Send initial stats
    stats := map[string]interface{}{
        "type":  "stats",
        "stats": mq.stats,
    }
    conn.WriteJSON(stats)

    // Keep connection alive and handle messages
    for {
        var msg map[string]interface{}
        if err := conn.ReadJSON(&msg); err != nil {
            break
        }

        if msg["type"] == "ping" {
            conn.WriteJSON(map[string]string{"type": "pong"})
        }
    }
}