package main

import (
    "encoding/json"
    "log"
    "net/http"
    
    "github.com/gorilla/mux"
)

// StartAPI starts the blockchain API server
func StartAPI(blockchain *Blockchain, port string) {
    router := mux.NewRouter()
    
    // Health check
    router.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
    }).Methods("GET")
    
    // Get blockchain
    router.HandleFunc("/blockchain", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(blockchain)
    }).Methods("GET")
    
    // Add block
    router.HandleFunc("/block", func(w http.ResponseWriter, r *http.Request) {
        var crodData CRODData
        json.NewDecoder(r.Body).Decode(&crodData)
        
        blockchain.AddBlock(crodData)
        json.NewEncoder(w).Encode(map[string]string{"status": "block added"})
    }).Methods("POST")
    
    log.Printf("Blockchain API starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, router))
}