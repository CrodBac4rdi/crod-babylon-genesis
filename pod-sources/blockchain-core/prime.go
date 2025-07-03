package main

import (
    "crypto/sha256"
    "encoding/hex"
    "math/big"
)

// PrimeCalculator handles hash to prime conversions
type PrimeCalculator struct {
    cache map[string]*big.Int
}

// NewPrimeCalculator creates a new prime calculator with cache
func NewPrimeCalculator() *PrimeCalculator {
    return &PrimeCalculator{
        cache: make(map[string]*big.Int),
    }
}

// HashToPrime converts a hash string to the next prime number
func (pc *PrimeCalculator) HashToPrime(hash string) *big.Int {
    // Check cache first
    if prime, exists := pc.cache[hash]; exists {
        return prime
    }
    
    // Convert hash to big integer
    hashBytes, _ := hex.DecodeString(hash)
    num := new(big.Int).SetBytes(hashBytes)
    
    // Find next prime
    prime := new(big.Int).Set(num)
    for !prime.ProbablyPrime(20) {
        prime.Add(prime, big.NewInt(1))
    }
    
    // Cache result
    pc.cache[hash] = prime
    
    return prime
}

// DocumentHashToPrime converts document content to hash then to prime
func (pc *PrimeCalculator) DocumentHashToPrime(content []byte) (*big.Int, string) {
    hash := sha256.Sum256(content)
    hashStr := hex.EncodeToString(hash[:])
    prime := pc.HashToPrime(hashStr)
    return prime, hashStr
}

// CalculatePatternPrime multiplies two document primes to create pattern prime
func (pc *PrimeCalculator) CalculatePatternPrime(prime1, prime2 *big.Int) *big.Int {
    result := new(big.Int)
    result.Mul(prime1, prime2)
    return result
}

// VerifyPatternPrime checks if a pattern prime is valid (product of two primes)
func (pc *PrimeCalculator) VerifyPatternPrime(patternPrime, prime1, prime2 *big.Int) bool {
    expected := new(big.Int)
    expected.Mul(prime1, prime2)
    return expected.Cmp(patternPrime) == 0
}