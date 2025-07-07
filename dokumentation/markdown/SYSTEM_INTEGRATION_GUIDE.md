# CROD System Integration Guide 🔧

## Overview

This guide provides comprehensive instructions for integrating the CROD Neural Network with the Polyglot City architecture within the Phoenix framework.

## Neural Network Integration Points

### 1. Phoenix Application Integration

The CROD Neural Network is embedded within the Phoenix application at multiple levels:

#### A. Direct JavaScript Execution

```elixir
defmodule Crod.Neural.Executor do
  @moduledoc """
  Executes the CROD Neural Network JavaScript implementation
  """
  
  @neural_network_path "priv/neural/crod-neural-network.js"
  
  def process(input) do
    with {:ok, node} <- NodeJS.start_link(),
         {:ok, result} <- NodeJS.call(node, @neural_network_path, "process", [input]) do
      parse_result(result)
    end
  end
  
  defp parse_result(js_result) do
    %{
      atoms: js_result["atoms"],
      patterns: js_result["patterns"],
      network_complexity: js_result["network_complexity"],
      attention_weights: js_result["attention_weights"],
      loss: js_result["loss"]
    }
  end
end
```

#### B. GenServer Wrapper

```elixir
defmodule Crod.Neural.Server do
  use GenServer
  require Logger
  
  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def process_input(text) do
    GenServer.call(__MODULE__, {:process, text}, 10_000)
  end
  
  def get_state do
    GenServer.call(__MODULE__, :get_state)
  end
  
  # Server Callbacks
  def init(_opts) do
    {:ok, node} = NodeJS.start_link()
    {:ok, _} = NodeJS.call(node, "priv/neural/crod-neural-network.js", "initialize", [])
    
    state = %{
      node: node,
      processing_count: 0,
      last_complexity: 0
    }
    
    {:ok, state}
  end
  
  def handle_call({:process, text}, _from, state) do
    result = NodeJS.call(state.node, "priv/neural/crod-neural-network.js", "process", [text])
    
    new_state = %{state | 
      processing_count: state.processing_count + 1,
      last_complexity: result["network_complexity"]
    }
    
    {:reply, {:ok, result}, new_state}
  end
end
```

### 2. District Communication

Each district can interact with the neural network through NATS messaging:

#### Pattern District (Rust)

```rust
use nats::jetstream::{self, Message};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct NeuralRequest {
    text: String,
    correlation_id: String,
}

#[derive(Serialize, Deserialize)]
struct NeuralResponse {
    atoms: Vec<String>,
    patterns: Vec<Pattern>,
    complexity: f64,
}

async fn request_neural_processing(
    client: &nats::Client,
    text: String,
) -> Result<NeuralResponse, Error> {
    let request = NeuralRequest {
        text,
        correlation_id: Uuid::new_v4().to_string(),
    };
    
    let response = client
        .request("neural.process", serde_json::to_vec(&request)?)
        .await?;
        
    Ok(serde_json::from_slice(&response.data)?)
}
```

#### Intelligence Hub (Python)

```python
import asyncio
import nats
from nats.errors import TimeoutError
import json

class NeuralClient:
    def __init__(self):
        self.nc = None
        self.js = None
        
    async def connect(self):
        self.nc = await nats.connect("nats://localhost:4222")
        self.js = self.nc.jetstream()
        
    async def process_with_neural(self, text: str) -> dict:
        request = {
            "text": text,
            "correlation_id": str(uuid.uuid4())
        }
        
        try:
            response = await self.nc.request(
                "neural.process", 
                json.dumps(request).encode(),
                timeout=5.0
            )
            return json.loads(response.data.decode())
        except TimeoutError:
            return {"error": "Neural network timeout"}
```

### 3. Event Sourcing Integration

Neural network events are captured in the event store:

```elixir
defmodule Crod.Neural.Events do
  defmodule InputProcessed do
    @derive Jason.Encoder
    defstruct [:input, :atoms, :patterns, :complexity, :timestamp]
  end
  
  defmodule PatternEmerged do
    @derive Jason.Encoder
    defstruct [:pattern_id, :atoms, :weight, :occurrences, :timestamp]
  end
  
  defmodule NetworkEvolved do
    @derive Jason.Encoder
    defstruct [:reason, :changes, :new_parameters, :timestamp]
  end
end

defmodule Crod.Neural.Aggregate do
  use Commanded.Aggregate
  
  def execute(%__MODULE__{}, %ProcessInput{text: text}) do
    result = Crod.Neural.Executor.process(text)
    
    %InputProcessed{
      input: text,
      atoms: result.atoms,
      patterns: result.patterns,
      complexity: result.network_complexity,
      timestamp: DateTime.utc_now()
    }
  end
end
```

## Deployment Configuration

### 1. Docker Integration

```dockerfile
# Dockerfile for CROD Phoenix with Neural Network
FROM elixir:1.15-alpine AS build

# Install Node.js for neural network
RUN apk add --no-cache nodejs npm python3 make g++

WORKDIR /app

# Copy and compile Elixir deps
COPY mix.exs mix.lock ./
RUN mix deps.get && mix deps.compile

# Copy neural network
COPY priv/neural/crod-neural-network.js ./priv/neural/

# Copy application code
COPY lib lib
COPY config config

# Compile application
RUN mix compile

# Runtime stage
FROM elixir:1.15-alpine

RUN apk add --no-cache nodejs

WORKDIR /app

COPY --from=build /app/_build ./_build
COPY --from=build /app/lib ./lib
COPY --from=build /app/priv ./priv
COPY --from=build /app/mix.exs ./mix.exs

EXPOSE 4000

CMD ["mix", "phx.server"]
```

### 2. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crod-phoenix
  namespace: crod-polyglot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crod-phoenix
  template:
    metadata:
      labels:
        app: crod-phoenix
        district: rathaus
    spec:
      containers:
      - name: phoenix
        image: crod/phoenix:latest
        ports:
        - containerPort: 4000
        env:
        - name: NEURAL_NETWORK_ENABLED
          value: "true"
        - name: NATS_URL
          value: "nats://nats.crod-polyglot.svc.cluster.local:4222"
        volumeMounts:
        - name: neural-state
          mountPath: /app/neural-state
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: neural-state
        persistentVolumeClaim:
          claimName: neural-state-pvc
```

### 3. Environment Configuration

```elixir
# config/runtime.exs
import Config

if config_env() == :prod do
  config :crod_phoenix, :neural,
    enabled: System.get_env("NEURAL_NETWORK_ENABLED", "true") == "true",
    max_complexity: String.to_integer(System.get_env("NEURAL_MAX_COMPLEXITY", "200")),
    learning_rate: String.to_float(System.get_env("NEURAL_LEARNING_RATE", "0.001")),
    state_persistence: System.get_env("NEURAL_STATE_PATH", "/app/neural-state")
end
```

## Performance Optimization

### 1. Neural Network Caching

```elixir
defmodule Crod.Neural.Cache do
  use Nebulex.Cache,
    otp_app: :crod_phoenix,
    adapter: Nebulex.Adapters.Local
    
  def process_with_cache(text) do
    get_or_store(text, fn ->
      Crod.Neural.Executor.process(text)
    end, ttl: :timer.minutes(5))
  end
end
```

### 2. Batch Processing

```elixir
defmodule Crod.Neural.BatchProcessor do
  use GenStage
  
  def start_link(opts) do
    GenStage.start_link(__MODULE__, opts, name: __MODULE__)
  end
  
  def init(_opts) do
    {:producer_consumer, %{}, subscribe_to: [{Crod.Neural.Queue, max_demand: 100}]}
  end
  
  def handle_events(texts, _from, state) do
    results = Enum.map(texts, &Crod.Neural.Executor.process/1)
    {:noreply, results, state}
  end
end
```

## Monitoring & Metrics

### 1. Telemetry Integration

```elixir
defmodule Crod.Neural.Telemetry do
  def setup do
    events = [
      [:crod, :neural, :process, :start],
      [:crod, :neural, :process, :stop],
      [:crod, :neural, :pattern, :emerged],
      [:crod, :neural, :evolution, :triggered]
    ]
    
    :telemetry.attach_many(
      "crod-neural-metrics",
      events,
      &handle_event/4,
      nil
    )
  end
  
  defp handle_event([:crod, :neural, :process, :stop], measurements, metadata, _) do
    Prometheus.Histogram.observe(
      [name: :neural_processing_duration_seconds],
      measurements.duration / 1_000_000_000
    )
    
    Prometheus.Gauge.set(
      [name: :neural_network_complexity],
      metadata.result.network_complexity
    )
  end
end
```

### 2. Grafana Dashboard

```json
{
  "dashboard": {
    "title": "CROD Neural Network",
    "panels": [
      {
        "title": "Network Complexity",
        "targets": [{
          "expr": "neural_network_complexity"
        }]
      },
      {
        "title": "Processing Rate",
        "targets": [{
          "expr": "rate(neural_processing_total[5m])"
        }]
      },
      {
        "title": "Pattern Emergence",
        "targets": [{
          "expr": "increase(neural_patterns_emerged_total[1h])"
        }]
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

1. **Neural Network Not Loading**
   - Check Node.js installation
   - Verify file path in config
   - Check file permissions

2. **High Memory Usage**
   - Implement state pruning
   - Reduce pattern retention
   - Enable garbage collection

3. **Slow Processing**
   - Enable caching
   - Use batch processing
   - Scale horizontally

### Debug Mode

```elixir
# Enable detailed logging
config :logger, :console,
  level: :debug,
  format: "$time $metadata[$level] $message\n",
  metadata: [:neural_atoms, :neural_patterns, :neural_complexity]
```

---

*This integration guide ensures seamless operation of the CROD Neural Network within the Polyglot City architecture.*