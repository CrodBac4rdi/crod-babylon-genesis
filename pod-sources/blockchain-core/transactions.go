package main

import (
    "encoding/json"
    "time"
)

// TransactionType defines the type of transaction
type TransactionType string

const (
    TxTypeTransfer       TransactionType = "transfer"
    TxTypeDocumentDelta  TransactionType = "document_delta"
    TxTypePatternFound   TransactionType = "pattern_found"
    TxTypeSmartContract  TransactionType = "smart_contract"
    TxTypeNFTMint       TransactionType = "nft_mint"
    TxTypeDAOProposal   TransactionType = "dao_proposal"
    TxTypeStaking       TransactionType = "staking"
    TxTypeDeFiSwap      TransactionType = "defi_swap"
)

// Transaction represents a CROD transaction
type Transaction struct {
    ID        string                 `json:"id"`
    Type      TransactionType        `json:"type"`
    From      string                 `json:"from"`
    To        string                 `json:"to,omitempty"`
    Amount    float64                `json:"amount,omitempty"`
    Data      map[string]interface{} `json:"data"`
    Timestamp time.Time              `json:"timestamp"`
    Hash      string                 `json:"hash"`
}

// SmartContractCall represents a call to Meta-Chain smart contract
type SmartContractCall struct {
    ContractAddress string                 `json:"contract_address"`
    Function        string                 `json:"function"`
    Args            []interface{}          `json:"args"`
    GasUsed         int64                  `json:"gas_used"`
    Result          interface{}            `json:"result,omitempty"`
}

// PatternTransaction represents a pattern discovery
type PatternTransaction struct {
    PatternID    string   `json:"pattern_id"`
    PatternPrime string   `json:"pattern_prime"`
    Atoms        []string `json:"atoms"`
    Weight       float64  `json:"weight"`
    Discoverer   string   `json:"discoverer"`
    Reward       float64  `json:"reward"`
}

// NFTTransaction represents NFT minting
type NFTTransaction struct {
    TokenID      int    `json:"token_id"`
    PatternID    string `json:"pattern_id"`
    Owner        string `json:"owner"`
    Rarity       string `json:"rarity"`
    MetadataURI  string `json:"metadata_uri"`
}

// DeFiTransaction represents DeFi operations
type DeFiTransaction struct {
    Pool         string  `json:"pool"`
    TokenIn      string  `json:"token_in"`
    TokenOut     string  `json:"token_out"`
    AmountIn     float64 `json:"amount_in"`
    AmountOut    float64 `json:"amount_out"`
    PriceImpact  float64 `json:"price_impact"`
}

// CreatePatternTransaction creates a pattern discovery transaction
func CreatePatternTransaction(patternID string, patternPrime string, atoms []string, discoverer string) Transaction {
    patternTx := PatternTransaction{
        PatternID:    patternID,
        PatternPrime: patternPrime,
        Atoms:        atoms,
        Weight:       100.0,
        Discoverer:   discoverer,
        Reward:       10.0, // 10 CROD reward
    }
    
    data, _ := json.Marshal(patternTx)
    var dataMap map[string]interface{}
    json.Unmarshal(data, &dataMap)
    
    return Transaction{
        ID:        generateTransactionID(),
        Type:      TxTypePatternFound,
        From:      "pattern-district",
        To:        discoverer,
        Amount:    patternTx.Reward,
        Data:      dataMap,
        Timestamp: time.Now(),
    }
}

// CreateSmartContractTransaction creates a smart contract call transaction
func CreateSmartContractTransaction(from string, contractCall SmartContractCall) Transaction {
    data, _ := json.Marshal(contractCall)
    var dataMap map[string]interface{}
    json.Unmarshal(data, &dataMap)
    
    return Transaction{
        ID:        generateTransactionID(),
        Type:      TxTypeSmartContract,
        From:      from,
        To:        contractCall.ContractAddress,
        Data:      dataMap,
        Timestamp: time.Now(),
    }
}

// CreateNFTMintTransaction creates an NFT minting transaction
func CreateNFTMintTransaction(nft NFTTransaction) Transaction {
    data, _ := json.Marshal(nft)
    var dataMap map[string]interface{}
    json.Unmarshal(data, &dataMap)
    
    return Transaction{
        ID:        generateTransactionID(),
        Type:      TxTypeNFTMint,
        From:      "nft-contract",
        To:        nft.Owner,
        Data:      dataMap,
        Timestamp: time.Now(),
    }
}

// CreateDeFiSwapTransaction creates a DeFi swap transaction
func CreateDeFiSwapTransaction(trader string, swap DeFiTransaction) Transaction {
    data, _ := json.Marshal(swap)
    var dataMap map[string]interface{}
    json.Unmarshal(data, &dataMap)
    
    return Transaction{
        ID:        generateTransactionID(),
        Type:      TxTypeDeFiSwap,
        From:      trader,
        To:        swap.Pool,
        Amount:    swap.AmountIn,
        Data:      dataMap,
        Timestamp: time.Now(),
    }
}

// generateTransactionID creates a unique transaction ID
func generateTransactionID() string {
    return time.Now().Format("20060102150405") + "-" + generateRandomHex(8)
}

// generateRandomHex generates random hex string (simplified)
func generateRandomHex(length int) string {
    // In production, use crypto/rand
    return "abcdef12"
}