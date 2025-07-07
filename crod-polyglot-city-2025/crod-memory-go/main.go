package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/gorilla/mux"
	"github.com/nats-io/nats.go"
	"github.com/nats-io/stan.go"
	"github.com/patrickmn/go-cache"
)

type MemoryService struct {
	cache       *cache.Cache
	sessions    sync.Map
	nc          *nats.Conn
	sc          stan.Conn
	mu          sync.RWMutex
	metrics     *Metrics
}

type Metrics struct {
	mu          sync.RWMutex
	hits        uint64
	misses      uint64
	sets        uint64
	deletes     uint64
	activeSessions int32
}

type Session struct {
	ID        string                 `json:"id"`
	Data      map[string]interface{} `json:"data"`
	CreatedAt time.Time              `json:"created_at"`
	UpdatedAt time.Time              `json:"updated_at"`
	TTL       time.Duration          `json:"ttl"`
}

type CacheEntry struct {
	Key       string      `json:"key"`
	Value     interface{} `json:"value"`
	TTL       int         `json:"ttl,omitempty"`
}

type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

func NewMemoryService() (*MemoryService, error) {
	// Initialize distributed cache with 5min default, 10min cleanup
	c := cache.New(5*time.Minute, 10*time.Minute)

	// Connect to NATS
	natsURL := os.Getenv("NATS_URL")
	if natsURL == "" {
		natsURL = "nats://localhost:4222"
	}

	nc, err := nats.Connect(natsURL,
		nats.ReconnectWait(2*time.Second),
		nats.MaxReconnects(60),
		nats.DisconnectErrHandler(func(nc *nats.Conn, err error) {
			log.Printf("NATS disconnected: %v", err)
		}),
		nats.ReconnectHandler(func(nc *nats.Conn) {
			log.Printf("NATS reconnected to %s", nc.ConnectedUrl())
		}),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to NATS: %w", err)
	}

	// Connect to NATS Streaming
	clusterID := os.Getenv("NATS_CLUSTER_ID")
	if clusterID == "" {
		clusterID = "crod-cluster"
	}

	clientID := fmt.Sprintf("memory-service-%d", time.Now().UnixNano())
	sc, err := stan.Connect(clusterID, clientID, stan.NatsConn(nc))
	if err != nil {
		nc.Close()
		return nil, fmt.Errorf("failed to connect to NATS Streaming: %w", err)
	}

	ms := &MemoryService{
		cache:   c,
		nc:      nc,
		sc:      sc,
		metrics: &Metrics{},
	}

	// Subscribe to cache sync channel
	ms.setupSubscriptions()

	return ms, nil
}

func (ms *MemoryService) setupSubscriptions() {
	// Subscribe to cache operations for distributed sync
	ms.sc.Subscribe("cache.sync", func(msg *stan.Msg) {
		var entry CacheEntry
		if err := json.Unmarshal(msg.Data, &entry); err != nil {
			log.Printf("Failed to unmarshal cache sync message: %v", err)
			return
		}

		// Apply cache operation locally
		if entry.TTL > 0 {
			ms.cache.Set(entry.Key, entry.Value, time.Duration(entry.TTL)*time.Second)
		} else {
			ms.cache.Set(entry.Key, entry.Value, cache.DefaultExpiration)
		}
	}, stan.DurableName("memory-cache-sync"))

	// Subscribe to session operations
	ms.sc.Subscribe("session.update", func(msg *stan.Msg) {
		var session Session
		if err := json.Unmarshal(msg.Data, &session); err != nil {
			log.Printf("Failed to unmarshal session message: %v", err)
			return
		}

		ms.sessions.Store(session.ID, &session)
		ms.updateMetrics("session", true)
	}, stan.DurableName("memory-session-sync"))
}

func (ms *MemoryService) handleSet(w http.ResponseWriter, r *http.Request) {
	var entry CacheEntry
	if err := json.NewDecoder(r.Body).Decode(&entry); err != nil {
		ms.respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	// Set in local cache
	if entry.TTL > 0 {
		ms.cache.Set(entry.Key, entry.Value, time.Duration(entry.TTL)*time.Second)
	} else {
		ms.cache.Set(entry.Key, entry.Value, cache.DefaultExpiration)
	}

	ms.updateMetrics("set", true)

	// Publish to distributed cache
	go ms.publishCacheSync(entry)

	ms.respondSuccess(w, map[string]interface{}{
		"key": entry.Key,
		"ttl": entry.TTL,
	})
}

func (ms *MemoryService) handleGet(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]

	value, found := ms.cache.Get(key)
	if !found {
		ms.updateMetrics("miss", true)
		ms.respondError(w, http.StatusNotFound, "Key not found")
		return
	}

	ms.updateMetrics("hit", true)
	ms.respondSuccess(w, map[string]interface{}{
		"key":   key,
		"value": value,
	})
}

func (ms *MemoryService) handleDelete(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	key := vars["key"]

	ms.cache.Delete(key)
	ms.updateMetrics("delete", true)

	// Publish deletion to distributed cache
	go ms.publishCacheSync(CacheEntry{Key: key, Value: nil})

	ms.respondSuccess(w, map[string]interface{}{
		"key": key,
		"deleted": true,
	})
}

func (ms *MemoryService) handleCreateSession(w http.ResponseWriter, r *http.Request) {
	session := &Session{
		ID:        fmt.Sprintf("sess_%d", time.Now().UnixNano()),
		Data:      make(map[string]interface{}),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		TTL:       30 * time.Minute,
	}

	// Parse request body if provided
	var reqData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&reqData); err == nil {
		session.Data = reqData
	}

	ms.sessions.Store(session.ID, session)
	ms.updateMetrics("session", true)

	// Publish session creation
	go ms.publishSessionUpdate(session)

	// Launch goroutine to manage session lifecycle
	go ms.manageSession(session)

	ms.respondSuccess(w, session)
}

func (ms *MemoryService) handleGetSession(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	sessionID := vars["id"]

	value, found := ms.sessions.Load(sessionID)
	if !found {
		ms.respondError(w, http.StatusNotFound, "Session not found")
		return
	}

	session := value.(*Session)
	ms.respondSuccess(w, session)
}

func (ms *MemoryService) handleUpdateSession(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	sessionID := vars["id"]

	value, found := ms.sessions.Load(sessionID)
	if !found {
		ms.respondError(w, http.StatusNotFound, "Session not found")
		return
	}

	session := value.(*Session)
	
	var updateData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&updateData); err != nil {
		ms.respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	// Update session data
	for k, v := range updateData {
		session.Data[k] = v
	}
	session.UpdatedAt = time.Now()

	ms.sessions.Store(sessionID, session)

	// Publish session update
	go ms.publishSessionUpdate(session)

	ms.respondSuccess(w, session)
}

func (ms *MemoryService) handleMetrics(w http.ResponseWriter, r *http.Request) {
	ms.metrics.mu.RLock()
	defer ms.metrics.mu.RUnlock()

	stats := map[string]interface{}{
		"cache_hits":      ms.metrics.hits,
		"cache_misses":    ms.metrics.misses,
		"cache_sets":      ms.metrics.sets,
		"cache_deletes":   ms.metrics.deletes,
		"active_sessions": ms.metrics.activeSessions,
		"cache_items":     ms.cache.ItemCount(),
		"uptime":          time.Since(startTime).String(),
	}

	ms.respondSuccess(w, stats)
}

func (ms *MemoryService) manageSession(session *Session) {
	ticker := time.NewTicker(session.TTL)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// Session expired, remove it
			ms.sessions.Delete(session.ID)
			ms.updateMetrics("session", false)
			log.Printf("Session %s expired and removed", session.ID)
			return
		}
	}
}

func (ms *MemoryService) publishCacheSync(entry CacheEntry) {
	data, err := json.Marshal(entry)
	if err != nil {
		log.Printf("Failed to marshal cache entry: %v", err)
		return
	}

	if err := ms.sc.Publish("cache.sync", data); err != nil {
		log.Printf("Failed to publish cache sync: %v", err)
	}
}

func (ms *MemoryService) publishSessionUpdate(session *Session) {
	data, err := json.Marshal(session)
	if err != nil {
		log.Printf("Failed to marshal session: %v", err)
		return
	}

	if err := ms.sc.Publish("session.update", data); err != nil {
		log.Printf("Failed to publish session update: %v", err)
	}
}

func (ms *MemoryService) updateMetrics(metric string, increment bool) {
	ms.metrics.mu.Lock()
	defer ms.metrics.mu.Unlock()

	switch metric {
	case "hit":
		ms.metrics.hits++
	case "miss":
		ms.metrics.misses++
	case "set":
		ms.metrics.sets++
	case "delete":
		ms.metrics.deletes++
	case "session":
		if increment {
			ms.metrics.activeSessions++
		} else {
			ms.metrics.activeSessions--
		}
	}
}

func (ms *MemoryService) respondSuccess(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(Response{
		Success: true,
		Data:    data,
	})
}

func (ms *MemoryService) respondError(w http.ResponseWriter, code int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(Response{
		Success: false,
		Error:   message,
	})
}

func (ms *MemoryService) Close() {
	if ms.sc != nil {
		ms.sc.Close()
	}
	if ms.nc != nil {
		ms.nc.Close()
	}
}

var startTime = time.Now()

func main() {
	log.Println("Starting CROD Memory Service (Go)...")

	ms, err := NewMemoryService()
	if err != nil {
		log.Fatalf("Failed to create memory service: %v", err)
	}
	defer ms.Close()

	router := mux.NewRouter()

	// Cache endpoints
	router.HandleFunc("/cache/set", ms.handleSet).Methods("POST")
	router.HandleFunc("/cache/get/{key}", ms.handleGet).Methods("GET")
	router.HandleFunc("/cache/delete/{key}", ms.handleDelete).Methods("DELETE")

	// Session endpoints
	router.HandleFunc("/session/create", ms.handleCreateSession).Methods("POST")
	router.HandleFunc("/session/{id}", ms.handleGetSession).Methods("GET")
	router.HandleFunc("/session/{id}/update", ms.handleUpdateSession).Methods("PUT")

	// Metrics endpoint
	router.HandleFunc("/metrics", ms.handleMetrics).Methods("GET")

	// Health check
	router.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		ms.respondSuccess(w, map[string]string{
			"status": "healthy",
			"service": "memory-quarter",
			"language": "go",
		})
	}).Methods("GET")

	srv := &http.Server{
		Addr:         ":7031",
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Start server in goroutine
	go func() {
		log.Printf("Memory Quarter (Go) listening on port 7031")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed: %v", err)
		}
	}()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down Memory Quarter...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Printf("Server shutdown error: %v", err)
	}

	log.Println("Memory Quarter stopped")
}