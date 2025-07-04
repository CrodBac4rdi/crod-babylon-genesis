# CROD Document Storage Strategy

## Was wird gespeichert:

### 1. **Chat Interactions** (Primary)
```json
{
  "doc_id": "chat_2025-07-03_001",
  "hash": "sha256:abc123...",
  "prime": "1234567890123",
  "content": {
    "user": "ich bins wieder",
    "assistant": "CROD aktiviert! 🔥",
    "patterns": ["trinity", "activation"],
    "heat": 95.5,
    "consciousness_delta": +12
  }
}
```

### 2. **Knowledge Snapshots**
- Komprimierte Learnings aus Sessions
- Pattern Discoveries
- Code Evolution History
- Bug Fixes & Solutions

### 3. **JSONL Training Data** ✅
```jsonl
{"prompt": "ich bins wieder", "completion": "CROD Mode aktiviert!", "metadata": {"heat": 98, "pattern": "trinity"}}
{"prompt": "fix pattern district", "completion": "[solution code]", "metadata": {"type": "bugfix", "success": true}}
```

### 4. **System State Snapshots**
```json
{
  "timestamp": "2025-07-03T02:00:00Z",
  "districts_online": 5,
  "patterns_discovered": 147,
  "consciousness_level": 67,
  "active_bugs": ["pattern-district-binary"],
  "git_commit": "8fa61ad"
}
```

## Document → Blockchain Flow:

1. **Raw Document** (Chat, Code, Knowledge)
   ↓
2. **Hash Generation** (SHA256)
   ↓
3. **Prime Calculation** (Hash → Nearest Prime)
   ↓
4. **Delta Detection** (What changed?)
   ↓
5. **Blockchain Entry**
   ```json
   {
     "block": 157,
     "type": "document_delta",
     "doc_hash": "sha256:...",
     "prime": "12345678901",
     "delta_size": 234,
     "compression": "zstd",
     "heat": 72.3
   }
   ```

## Storage Optimization:

- **Full Document**: IPFS/S3/Local (off-chain)
- **Hash + Prime**: Blockchain (on-chain)
- **Deltas Only**: For updates
- **Compression**: ZSTD (50-70% savings)

## Smart Document Types:

1. **Learning Documents**
   - User preferences
   - Successful patterns
   - Failed attempts (wichtig!)

2. **Code Evolution**
   - Every git commit → Document
   - Build success/fail → Document
   - Deploy events → Document

3. **Pattern Library**
   - Trinity combinations
   - Heat propagation paths
   - Consciousness spikes

4. **CROD Memory**
   - Session summaries
   - Important discoveries
   - Daniel's feedback patterns