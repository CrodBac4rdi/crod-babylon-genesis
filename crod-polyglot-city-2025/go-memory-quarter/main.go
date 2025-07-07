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

	"github.com/dgraph-io/badger/v4"
	"github.com/gin-gonic/gin"
	"github.com/nats-io/nats.go"
	cache "github.com/patrickmn/go-cache"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/sirupsen/logrus"
)

type MemoryQuarter struct {
	nc           *nats.Conn
	js           nats.JetStreamContext
	badgerDB     *badger.DB
	memCache     *cache.Cache
	logger       *logrus.Logger
	metrics      *Metrics
	mu           sync.RWMutex
	consciousness map[string]interface{}
}

type Metrics struct {
	memoryOps     prometheus.Counter
	cacheHits     prometheus.Counter
	cacheMisses   prometheus.Counter
	storageSize   prometheus.Gauge
	queryDuration prometheus.Histogram
}

type MemoryEntry struct {
	Key       string      `json:"key"`
	Value     interface{} `json:"value"`
	Timestamp time.Time   `json:"timestamp"`
	TTL       int         `json:"ttl,omitempty"`
	Tags      []string    `json:"tags,omitempty"`
	Trinity   int         `json:"trinity,omitempty"`
}

type QueryRequest struct {
	Pattern   string   `json:"pattern"`
	Tags      []string `json:"tags,omitempty"`
	TimeRange *struct {
		Start time.Time `json:"start"`
		End   time.Time `json:"end"`
	} `json:"time_range,omitempty"`
}

func NewMemoryQuarter() (*MemoryQuarter, error) {
	logger := logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	
	// Initialize BadgerDB
	opts := badger.DefaultOptions("/tmp/crod-memory")
	opts.Logger = nil
	db, err := badger.Open(opts)
	if err != nil {
		return nil, fmt.Errorf("failed to open BadgerDB: %w", err)
	}
	
	// Initialize in-memory cache
	memCache := cache.New(5*time.Minute, 10*time.Minute)
	
	// Initialize metrics
	metrics := &Metrics{
		memoryOps: prometheus.NewCounter(prometheus.CounterOpts{
			Name: "crod_memory_operations_total",
			Help: "Total number of memory operations",
		}),
		cacheHits: prometheus.NewCounter(prometheus.CounterOpts{
			Name: "crod_cache_hits_total",
			Help: "Total number of cache hits",
		}),
		cacheMisses: prometheus.NewCounter(prometheus.CounterOpts{
			Name: "crod_cache_misses_total",
			Help: "Total number of cache misses",
		}),
		storageSize: prometheus.NewGauge(prometheus.GaugeOpts{
			Name: "crod_storage_size_bytes",
			Help: "Size of storage in bytes",
		}),
		queryDuration: prometheus.NewHistogram(prometheus.HistogramOpts{
			Name:    "crod_query_duration_seconds",
			Help:    "Query duration in seconds",
			Buckets: prometheus.DefBuckets,
		}),
	}
	
	// Register metrics
	prometheus.MustRegister(
		metrics.memoryOps,
		metrics.cacheHits,
		metrics.cacheMisses,
		metrics.storageSize,
		metrics.queryDuration,
	)
	
	return &MemoryQuarter{
		badgerDB:      db,
		memCache:      memCache,
		logger:        logger,
		metrics:       metrics,
		consciousness: make(map[string]interface{}),
	}, nil
}

func (mq *MemoryQuarter) ConnectNATS(url string) error {
	nc, err := nats.Connect(url)
	if err != nil {
		return fmt.Errorf("failed to connect to NATS: %w", err)
	}
	
	js, err := nc.JetStream()
	if err != nil {
		return fmt.Errorf("failed to create JetStream context: %w", err)
	}
	
	mq.nc = nc
	mq.js = js
	
	// Create memory stream
	_, err = js.AddStream(&nats.StreamConfig{
		Name:     "MEMORY",
		Subjects: []string{"crod.memory.>"},
		Storage:  nats.FileStorage,
		MaxMsgs:  1000000,
	})
	if err != nil && err != nats.ErrStreamNameAlreadyInUse {
		return fmt.Errorf("failed to create stream: %w", err)
	}
	
	// Subscribe to memory commands
	mq.subscribeToCommands()
	
	mq.logger.Info("Connected to NATS")
	return nil
}

func (mq *MemoryQuarter) subscribeToCommands() {
	// Subscribe to store commands
	mq.nc.Subscribe("crod.memory.store", func(msg *nats.Msg) {
		var entry MemoryEntry
		if err := json.Unmarshal(msg.Data, &entry); err != nil {
			mq.logger.Error("Failed to unmarshal store request:", err)
			return
		}
		
		if err := mq.Store(entry); err != nil {
			mq.logger.Error("Failed to store entry:", err)
			msg.Respond([]byte(`{"error":"store failed"}`))
			return
		}
		
		msg.Respond([]byte(`{"status":"stored"}`))
	})
	
	// Subscribe to query commands
	mq.nc.Subscribe("crod.memory.query", func(msg *nats.Msg) {
		var query QueryRequest
		if err := json.Unmarshal(msg.Data, &query); err != nil {
			mq.logger.Error("Failed to unmarshal query request:", err)
			return
		}
		
		results, err := mq.Query(query)
		if err != nil {
			mq.logger.Error("Failed to query:", err)
			msg.Respond([]byte(`{"error":"query failed"}`))
			return
		}
		
		response, _ := json.Marshal(results)
		msg.Respond(response)
	})
}

func (mq *MemoryQuarter) Store(entry MemoryEntry) error {
	mq.metrics.memoryOps.Inc()
	
	// Store in cache
	if entry.TTL > 0 {
		mq.memCache.Set(entry.Key, entry.Value, time.Duration(entry.TTL)*time.Second)
	} else {
		mq.memCache.SetDefault(entry.Key, entry.Value)
	}
	
	// Store in BadgerDB
	data, err := json.Marshal(entry)
	if err != nil {
		return err
	}
	
	err = mq.badgerDB.Update(func(txn *badger.Txn) error {
		return txn.Set([]byte(entry.Key), data)
	})
	
	if err != nil {
		return err
	}
	
	// Publish to NATS
	if mq.js != nil {
		mq.js.Publish("crod.memory.stored", data)
	}
	
	return nil
}

func (mq *MemoryQuarter) Get(key string) (interface{}, error) {
	// Check cache first
	if val, found := mq.memCache.Get(key); found {
		mq.metrics.cacheHits.Inc()
		return val, nil
	}
	
	mq.metrics.cacheMisses.Inc()
	
	// Check BadgerDB
	var entry MemoryEntry
	err := mq.badgerDB.View(func(txn *badger.Txn) error {
		item, err := txn.Get([]byte(key))
		if err != nil {
			return err
		}
		
		return item.Value(func(val []byte) error {
			return json.Unmarshal(val, &entry)
		})
	})
	
	if err != nil {
		return nil, err
	}
	
	// Update cache
	mq.memCache.SetDefault(key, entry.Value)
	
	return entry.Value, nil
}

func (mq *MemoryQuarter) Query(req QueryRequest) ([]MemoryEntry, error) {
	start := time.Now()
	defer func() {
		mq.metrics.queryDuration.Observe(time.Since(start).Seconds())
	}()
	
	var results []MemoryEntry
	
	err := mq.badgerDB.View(func(txn *badger.Txn) error {
		opts := badger.DefaultIteratorOptions
		opts.PrefetchSize = 10
		it := txn.NewIterator(opts)
		defer it.Close()
		
		prefix := []byte(req.Pattern)
		for it.Seek(prefix); it.ValidForPrefix(prefix); it.Next() {
			item := it.Item()
			
			var entry MemoryEntry
			err := item.Value(func(val []byte) error {
				return json.Unmarshal(val, &entry)
			})
			if err != nil {
				continue
			}
			
			// Apply filters
			if req.TimeRange != nil {
				if entry.Timestamp.Before(req.TimeRange.Start) || entry.Timestamp.After(req.TimeRange.End) {
					continue
				}
			}
			
			if len(req.Tags) > 0 && !hasAnyTag(entry.Tags, req.Tags) {
				continue
			}
			
			results = append(results, entry)
		}
		
		return nil
	})
	
	return results, err
}

func hasAnyTag(entryTags, queryTags []string) bool {
	tagMap := make(map[string]bool)
	for _, tag := range entryTags {
		tagMap[tag] = true
	}
	
	for _, tag := range queryTags {
		if tagMap[tag] {
			return true
		}
	}
	
	return false
}

func main() {
	mq, err := NewMemoryQuarter()
	if err != nil {
		log.Fatal("Failed to create MemoryQuarter:", err)
	}
	defer mq.badgerDB.Close()
	
	// Connect to NATS
	natsURL := os.Getenv("NATS_URL")
	if natsURL == "" {
		natsURL = "nats://localhost:4222"
	}
	
	if err := mq.ConnectNATS(natsURL); err != nil {
		log.Fatal("Failed to connect to NATS:", err)
	}
	defer mq.nc.Close()
	
	// Setup Gin router
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gin.Recovery())
	
	// Routes
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":  "healthy",
			"service": "go-memory-quarter",
			"nats":    mq.nc.IsConnected(),
		})
	})
	
	r.POST("/store", func(c *gin.Context) {
		var entry MemoryEntry
		if err := c.ShouldBindJSON(&entry); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}
		
		entry.Timestamp = time.Now()
		if err := mq.Store(entry); err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		
		c.JSON(200, gin.H{"status": "stored"})
	})
	
	r.GET("/get/:key", func(c *gin.Context) {
		key := c.Param("key")
		value, err := mq.Get(key)
		if err != nil {
			c.JSON(404, gin.H{"error": "not found"})
			return
		}
		
		c.JSON(200, gin.H{"key": key, "value": value})
	})
	
	r.POST("/query", func(c *gin.Context) {
		var req QueryRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}
		
		results, err := mq.Query(req)
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}
		
		c.JSON(200, results)
	})
	
	// Metrics endpoint
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))
	
	mq.logger.Info("Go Memory Quarter starting on port 7031")
	if err := r.Run(":7031"); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}