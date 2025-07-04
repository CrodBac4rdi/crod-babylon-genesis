# CROD Current Architecture - July 4, 2025

## 🏗️ Current System Architecture

```mermaid
graph TB
    subgraph "Local Python Processes"
        P1[claude_code_api.py<br/>11h runtime]
        P2[crod_self_reflection.py<br/>2.5h runtime]
        P3[crod_identity_booster.py<br/>2.5h runtime]
        P4[unified_crod_main.py<br/>2h runtime]
        P5[crod_mirror_websocket.py<br/>1h runtime]
    end

    subgraph "Kubernetes Pods - crod-polyglot"
        K1[meta-chain<br/>Elixir:8000]
        K2[pattern-district<br/>Rust:7007]
        K3[memory-quarter<br/>Go:7031]
        K4[intelligence-hub<br/>Python:7113]
        K5[crod-core<br/>JS:8100/8101]
        K6[gateway<br/>:8888]
        K7[redis<br/>:6379]
        K8[postgres-spatial<br/>:5432]
    end

    subgraph "Databases"
        D1[crod_3d_database.db<br/>121k rows]
        D2[unified_crod.db<br/>769 rows]
        D3[crod.db<br/>19 rows total]
        D4[Empty DBs<br/>3 files]
    end

    subgraph "Ollama"
        O1[crod-ultimate<br/>4.7GB model]
    end

    %% Connections
    K7 -.-> K1
    K7 -.-> K2
    K7 -.-> K3
    K7 -.-> K5
    K7 -.-> K6
    
    P4 --> D2
    P5 --> D1
    
    P1 --> O1
    
    classDef running fill:#90EE90
    classDef broken fill:#FFB6C1
    classDef data fill:#87CEEB
    
    class K1,K2,K3,K4,K5,K6,K7,K8 running
    class D1,D2,D3 data
```

## 🔄 Data Flow Issues

```mermaid
graph LR
    subgraph "Current Problems"
        A[Districts Connected to Redis] -->|❌ No Pub/Sub| B[Districts Don't Talk]
        C[5 Python Processes] -->|❌ Duplicate Work| D[Resource Waste]
        E[9 Databases] -->|❌ Fragmented Data| F[No Single Truth]
    end
```

## 🎯 Target Architecture

```mermaid
graph TD
    subgraph "CROD Ultimate Orchestrator"
        CROD[CROD Ultimate Model<br/>Ollama Integration]
    end

    subgraph "Elixir Blockchain Core"
        BC[Blockchain Supervisor]
        GB[Genesis Block]
        B1[Block 1]
        B2[Block 2]
        DB[Delta Blocks]
        
        GB --> B1
        B1 --> B2
        B2 -.-> DB
    end

    subgraph "Quarter Supervisors"
        QS[Quarter Supervisor<br/>OTP]
        Q1[Pattern Quarter<br/>GenServer]
        Q2[Memory Quarter<br/>GenServer]
        Q3[Intelligence Quarter<br/>GenServer]
        Q4[Gateway Quarter<br/>GenServer]
        
        QS --> Q1
        QS --> Q2
        QS --> Q3
        QS --> Q4
    end

    subgraph "Communication Layer"
        NATS[NATS Message Bus<br/>5x faster than Redis]
        REDIS[Redis Fallback<br/>For compatibility]
    end

    subgraph "Storage"
        UDB[Unified Database<br/>Mnesia/ETS]
        S3D[3D Spatial Grid<br/>Infinite Context]
    end

    subgraph "External"
        CLAUDE[Claude API]
        DOCKER[Docker/K8s]
    end

    %% Connections
    CROD --> BC
    BC --> QS
    QS <--> NATS
    NATS <--> REDIS
    Q1 --> UDB
    Q2 --> S3D
    CROD --> CLAUDE
    CROD --> DOCKER
    
    classDef brain fill:#FFD700
    classDef blockchain fill:#98FB98
    classDef quarter fill:#87CEEB
    classDef comm fill:#DDA0DD
    
    class CROD brain
    class BC,GB,B1,B2,DB blockchain
    class QS,Q1,Q2,Q3,Q4 quarter
    class NATS,REDIS comm
```

## 📝 Delta Block Implementation

```mermaid
graph LR
    subgraph "Development Mode"
        A[Original Block] --> D1[Delta 1<br/>Change A]
        A --> D2[Delta 2<br/>Change B]
        D1 --> M[Merged Block<br/>A + B]
        D2 --> M
    end
    
    subgraph "Production Mode"
        M --> P[Production Block<br/>Clean Chain]
    end
```

### Delta Block Options:

1. **Option A: Single Delta Chain**
   ```elixir
   defmodule CROD.DeltaChain do
     # One delta block at start during dev
     def read_chain(chain) do
       case chain.mode do
         :dev -> apply_deltas(chain.genesis, chain.delta_head)
         :prod -> read_normal(chain)
       end
     end
   end
   ```

2. **Option B: Per-Block Deltas**
   ```elixir
   defmodule CROD.Block do
     defstruct [:hash, :data, :deltas]
     
     # Each block can have multiple deltas
     def get_current_state(block) do
       Enum.reduce(block.deltas, block.data, &apply_delta/2)
     end
   end
   ```

## 🚀 Implementation Order

```mermaid
graph TD
    A[1. Stop All Processes<br/>Preserve Data] --> B[2. Build Elixir Blockchain<br/>With OTP]
    B --> C[3. Integrate CROD Ultimate<br/>As Orchestrator]
    C --> D[4. Implement NATS<br/>Message Bus]
    D --> E[5. Migrate Districts<br/>To GenServers]
    E --> F[6. Unified Database<br/>Mnesia]
    F --> G[7. Deploy & Test<br/>Block by Block]
```