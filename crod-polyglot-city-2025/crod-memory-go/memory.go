package main

import (
	"sync"
	"time"
)

type MemoryBank struct {
	memories map[string]CrodMemory
	mu       sync.RWMutex
	typeIndex map[string][]string // type -> []memory_ids
}

func NewMemoryBank() *MemoryBank {
	return &MemoryBank{
		memories:  make(map[string]CrodMemory),
		typeIndex: make(map[string][]string),
	}
}

func (mb *MemoryBank) Store(memory CrodMemory) {
	mb.mu.Lock()
	defer mb.mu.Unlock()

	// Set default TTL if not specified
	if memory.TTL == 0 {
		memory.TTL = 24 * time.Hour
	}

	// Store memory
	mb.memories[memory.ID] = memory

	// Update type index
	if memory.Type != "" {
		mb.typeIndex[memory.Type] = append(mb.typeIndex[memory.Type], memory.ID)
	}
}

func (mb *MemoryBank) Get(id string) (CrodMemory, bool) {
	mb.mu.RLock()
	defer mb.mu.RUnlock()

	memory, exists := mb.memories[id]
	if !exists {
		return CrodMemory{}, false
	}

	// Check if expired
	if time.Since(memory.Timestamp) > memory.TTL {
		return CrodMemory{}, false
	}

	return memory, true
}

func (mb *MemoryBank) Search(memType string, limit int) []CrodMemory {
	mb.mu.RLock()
	defer mb.mu.RUnlock()

	var results []CrodMemory

	if memType == "" {
		// Return all memories
		for _, memory := range mb.memories {
			if time.Since(memory.Timestamp) <= memory.TTL {
				results = append(results, memory)
				if limit > 0 && len(results) >= limit {
					break
				}
			}
		}
	} else {
		// Search by type
		if ids, ok := mb.typeIndex[memType]; ok {
			for _, id := range ids {
				if memory, exists := mb.memories[id]; exists {
					if time.Since(memory.Timestamp) <= memory.TTL {
						results = append(results, memory)
						if limit > 0 && len(results) >= limit {
							break
						}
					}
				}
			}
		}
	}

	return results
}

func (mb *MemoryBank) Cleanup() int {
	mb.mu.Lock()
	defer mb.mu.Unlock()

	expired := 0
	now := time.Now()

	// Find expired memories
	var toDelete []string
	for id, memory := range mb.memories {
		if now.Sub(memory.Timestamp) > memory.TTL {
			toDelete = append(toDelete, id)
			expired++
		}
	}

	// Delete expired memories
	for _, id := range toDelete {
		memory := mb.memories[id]
		delete(mb.memories, id)

		// Remove from type index
		if memory.Type != "" {
			mb.removeFromTypeIndex(memory.Type, id)
		}
	}

	return expired
}

func (mb *MemoryBank) removeFromTypeIndex(memType, id string) {
	if ids, ok := mb.typeIndex[memType]; ok {
		newIds := make([]string, 0, len(ids)-1)
		for _, existingId := range ids {
			if existingId != id {
				newIds = append(newIds, existingId)
			}
		}
		if len(newIds) > 0 {
			mb.typeIndex[memType] = newIds
		} else {
			delete(mb.typeIndex, memType)
		}
	}
}

func (mb *MemoryBank) Count() int {
	mb.mu.RLock()
	defer mb.mu.RUnlock()
	return len(mb.memories)
}

func (mb *MemoryBank) GetTypeStats() map[string]int {
	mb.mu.RLock()
	defer mb.mu.RUnlock()

	stats := make(map[string]int)
	for memType, ids := range mb.typeIndex {
		// Count non-expired memories
		count := 0
		for _, id := range ids {
			if memory, exists := mb.memories[id]; exists {
				if time.Since(memory.Timestamp) <= memory.TTL {
					count++
				}
			}
		}
		if count > 0 {
			stats[memType] = count
		}
	}
	return stats
}