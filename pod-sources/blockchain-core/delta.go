package main

import (
    "encoding/json"
    "math/big"
    "time"
)

// DeltaProcessor handles document delta operations
type DeltaProcessor struct {
    primeCalc *PrimeCalculator
    blockchain *Blockchain
}

// NewDeltaProcessor creates a new delta processor
func NewDeltaProcessor(blockchain *Blockchain) *DeltaProcessor {
    return &DeltaProcessor{
        primeCalc:  NewPrimeCalculator(),
        blockchain: blockchain,
    }
}

// ProcessDocumentUpdate processes a document update and creates delta
func (dp *DeltaProcessor) ProcessDocumentUpdate(docID string, previousContent, currentContent []byte) (*DocumentDelta, error) {
    // Calculate hashes and primes
    previousPrime, previousHash := dp.primeCalc.DocumentHashToPrime(previousContent)
    currentPrime, currentHash := dp.primeCalc.DocumentHashToPrime(currentContent)
    
    // Calculate delta (simplified - in production use proper diff algorithm)
    delta := dp.calculateDelta(previousContent, currentContent)
    
    // Calculate heat based on change size
    heat := float64(len(delta)) / float64(len(previousContent)) * 100.0
    
    docDelta := &DocumentDelta{
        DocumentHash:   currentHash,
        PreviousHash:   previousHash,
        Delta:          delta,
        DeltaType:      "update",
        PrimeReference: currentPrime.String(),
        Heat:           heat,
    }
    
    // Add to blockchain
    data := CRODData{
        District: "delta-quarter",
        Pattern:  "document-update",
        DocumentDelta: docDelta,
        Trinity: map[string]float64{
            "heat":     heat,
            "delta_size": float64(len(delta)),
        },
        Atoms: []string{docID, "delta", currentHash[:8]},
        Metadata: map[string]interface{}{
            "document_id": docID,
            "timestamp":   time.Now().Unix(),
            "previous_prime": previousPrime.String(),
            "current_prime":  currentPrime.String(),
        },
    }
    
    dp.blockchain.AddBlock(data)
    
    return docDelta, nil
}

// calculateDelta computes the difference between two documents
func (dp *DeltaProcessor) calculateDelta(previous, current []byte) json.RawMessage {
    // Simplified delta - in production use myers diff or similar
    delta := map[string]interface{}{
        "type": "simple_delta",
        "previous_length": len(previous),
        "current_length": len(current),
        "size_change": len(current) - len(previous),
    }
    
    deltaJSON, _ := json.Marshal(delta)
    return deltaJSON
}

// FindPatternBetweenDocuments finds patterns between two documents using their primes
func (dp *DeltaProcessor) FindPatternBetweenDocuments(hash1, hash2 string) *big.Int {
    prime1 := dp.primeCalc.HashToPrime(hash1)
    prime2 := dp.primeCalc.HashToPrime(hash2)
    
    patternPrime := dp.primeCalc.CalculatePatternPrime(prime1, prime2)
    
    // Record pattern in blockchain
    data := CRODData{
        District: "pattern-district",
        Pattern:  "document-pattern",
        Trinity: map[string]float64{
            "prime1": float64(prime1.BitLen()),
            "prime2": float64(prime2.BitLen()),
            "pattern": float64(patternPrime.BitLen()),
        },
        Atoms: []string{hash1[:8], hash2[:8], "pattern"},
        Metadata: map[string]interface{}{
            "pattern_prime": patternPrime.String(),
            "document_1": hash1,
            "document_2": hash2,
            "timestamp": time.Now().Unix(),
        },
    }
    
    dp.blockchain.AddBlock(data)
    
    return patternPrime
}