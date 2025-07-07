#!/bin/bash

# Create all directory structures
mkdir -p crod-rathaus-phoenix/{lib/{crod_rathaus,crod_rathaus_web/{controllers,live}},config,priv/static}
mkdir -p crod-parasit-python/src
mkdir -p crod-pattern-rust/src
mkdir -p crod-memory-go/cmd
mkdir -p crod-gateway-js/src

echo "Creating Phoenix Rathaus..."

# Phoenix Application
cat > crod-rathaus-phoenix/lib/crod_rathaus/application.ex << 'EOF'
defmodule CrodRathaus.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      CrodRathausWeb.Telemetry,
      {Phoenix.PubSub, name: CrodRathaus.PubSub},
      CrodRathausWeb.Endpoint,
      {CrodRathaus.NatsClient, []}
    ]

    opts = [strategy: :one_for_one, name: CrodRathaus.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @impl true
  def config_change(changed, _new, removed) do
    CrodRathausWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
EOF

# NATS Client
cat > crod-rathaus-phoenix/lib/crod_rathaus/nats_client.ex << 'EOF'
defmodule CrodRathaus.NatsClient do
  use GenServer
  require Logger

  def start_link(_) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end

  def init(_) do
    {:ok, conn} = Nats.Connection.start_link(host: "nats", port: 4222)
    Process.send_after(self(), :subscribe, 1000)
    {:ok, %{conn: conn}}
  end

  def handle_info(:subscribe, %{conn: conn} = state) do
    Nats.sub(conn, self(), "crod.>")
    Logger.info("CROD Rathaus subscribed to NATS")
    {:noreply, state}
  end

  def handle_info({:msg, %{topic: topic, body: body}}, state) do
    Logger.info("Received: #{topic} - #{body}")
    Phoenix.PubSub.broadcast(CrodRathaus.PubSub, "crod:events", {:nats_event, topic, body})
    {:noreply, state}
  end
end
EOF

# Endpoint
cat > crod-rathaus-phoenix/lib/crod_rathaus_web/endpoint.ex << 'EOF'
defmodule CrodRathausWeb.Endpoint do
  use Phoenix.Endpoint, otp_app: :crod_rathaus

  @session_options [
    store: :cookie,
    key: "_crod_rathaus_key",
    signing_salt: "crod2025"
  ]

  socket "/live", Phoenix.LiveView.Socket, websocket: [connect_info: [session: @session_options]]

  plug Plug.Static,
    at: "/",
    from: :crod_rathaus,
    gzip: false,
    only: CrodRathausWeb.static_paths()

  if code_reloading? do
    socket "/phoenix/live_reload/socket", Phoenix.LiveReloader.Socket
    plug Phoenix.LiveReloader
    plug Phoenix.CodeReloader
  end

  plug Phoenix.LiveDashboard.RequestLogger,
    param_key: "request_logger",
    cookie_key: "request_logger"

  plug Plug.RequestId
  plug Plug.Telemetry, event_prefix: [:phoenix, :endpoint]

  plug Plug.Parsers,
    parsers: [:urlencoded, :multipart, :json],
    pass: ["*/*"],
    json_decoder: Phoenix.json_library()

  plug Plug.MethodOverride
  plug Plug.Head
  plug Plug.Session, @session_options
  plug CrodRathausWeb.Router
end
EOF

# Router
cat > crod-rathaus-phoenix/lib/crod_rathaus_web/router.ex << 'EOF'
defmodule CrodRathausWeb.Router do
  use CrodRathausWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, {CrodRathausWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CrodRathausWeb do
    pipe_through :browser

    live "/", DashboardLive, :index
    live "/districts", DistrictsLive, :index
  end

  if Mix.env() in [:dev, :test] do
    import Phoenix.LiveDashboard.Router

    scope "/" do
      pipe_through :browser
      live_dashboard "/dashboard", metrics: CrodRathausWeb.Telemetry
    end
  end
end
EOF

# Dashboard LiveView
cat > crod-rathaus-phoenix/lib/crod_rathaus_web/live/dashboard_live.ex << 'EOF'
defmodule CrodRathausWeb.DashboardLive do
  use CrodRathausWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Phoenix.PubSub.subscribe(CrodRathaus.PubSub, "crod:events")
    end

    {:ok, assign(socket, events: [], districts: %{
      "pattern" => %{status: :connecting, port: 7007},
      "memory" => %{status: :connecting, port: 7031},
      "gateway" => %{status: :connecting, port: 7888},
      "parasit" => %{status: :connecting, port: 6666}
    })}
  end

  @impl true
  def handle_info({:nats_event, topic, body}, socket) do
    event = %{topic: topic, body: body, timestamp: DateTime.utc_now()}
    {:noreply, update(socket, :events, fn events -> [event | Enum.take(events, 99)] end)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="container mx-auto p-4">
      <h1 class="text-4xl font-bold mb-8">CROD Polyglot City 2025 - Rathaus</h1>
      
      <div class="grid grid-cols-2 gap-6">
        <div>
          <h2 class="text-2xl font-semibold mb-4">Districts Status</h2>
          <div class="space-y-2">
            <%= for {name, info} <- @districts do %>
              <div class="p-3 border rounded flex justify-between">
                <span class="font-medium"><%= name %></span>
                <span class={"px-2 py-1 rounded text-sm " <> status_class(info.status)}>
                  <%= info.status %> (:<%= info.port %>)
                </span>
              </div>
            <% end %>
          </div>
        </div>
        
        <div>
          <h2 class="text-2xl font-semibold mb-4">Recent Events</h2>
          <div class="space-y-1 max-h-96 overflow-y-auto">
            <%= for event <- @events do %>
              <div class="p-2 bg-gray-100 rounded text-sm">
                <div class="font-mono"><%= event.topic %></div>
                <div class="text-gray-600"><%= event.body %></div>
              </div>
            <% end %>
          </div>
        </div>
      </div>
    </div>
    """
  end

  defp status_class(:online), do: "bg-green-500 text-white"
  defp status_class(:connecting), do: "bg-yellow-500 text-white"
  defp status_class(:offline), do: "bg-red-500 text-white"
end
EOF

# Config
cat > crod-rathaus-phoenix/config/config.exs << 'EOF'
import Config

config :crod_rathaus, CrodRathausWeb.Endpoint,
  url: [host: "localhost"],
  render_errors: [view: CrodRathausWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: CrodRathaus.PubSub,
  live_view: [signing_salt: "crod2025"]

config :phoenix, :json_library, Jason

if config_env() == :dev do
  config :crod_rathaus, CrodRathausWeb.Endpoint,
    http: [ip: {0, 0, 0, 0}, port: 4000],
    check_origin: false,
    code_reloader: true,
    debug_errors: true,
    secret_key_base: "crod2025secretkeycrod2025secretkeycrod2025secretkeycrod2025secretkey",
    watchers: []
end
EOF

# Telemetry
cat > crod-rathaus-phoenix/lib/crod_rathaus_web/telemetry.ex << 'EOF'
defmodule CrodRathausWeb.Telemetry do
  use Supervisor
  import Telemetry.Metrics

  def start_link(arg) do
    Supervisor.start_link(__MODULE__, arg, name: __MODULE__)
  end

  @impl true
  def init(_arg) do
    children = [
      {:telemetry_poller, measurements: periodic_measurements(), period: 10_000}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

  def metrics do
    [
      summary("phoenix.endpoint.stop.duration",
        unit: {:native, :millisecond}
      ),
      summary("phoenix.router_dispatch.stop.duration",
        tags: [:route],
        unit: {:native, :millisecond}
      )
    ]
  end

  defp periodic_measurements do
    []
  end
end
EOF

# Web module
cat > crod-rathaus-phoenix/lib/crod_rathaus_web.ex << 'EOF'
defmodule CrodRathausWeb do
  def static_paths, do: ~w(assets fonts images favicon.ico robots.txt)

  def router do
    quote do
      use Phoenix.Router, helpers: false
      import Plug.Conn
      import Phoenix.Controller
      import Phoenix.LiveView.Router
    end
  end

  def channel do
    quote do
      use Phoenix.Channel
    end
  end

  def controller do
    quote do
      use Phoenix.Controller,
        formats: [:html, :json],
        layouts: [html: CrodRathausWeb.Layouts]

      import Plug.Conn
      unquote(verified_routes())
    end
  end

  def live_view do
    quote do
      use Phoenix.LiveView,
        layout: {CrodRathausWeb.Layouts, :app}

      unquote(html_helpers())
    end
  end

  def live_component do
    quote do
      use Phoenix.LiveComponent
      unquote(html_helpers())
    end
  end

  def html do
    quote do
      use Phoenix.Component
      import Phoenix.Controller,
        only: [get_csrf_token: 0, view_module: 1, view_template: 1]

      unquote(html_helpers())
    end
  end

  defp html_helpers do
    quote do
      import Phoenix.HTML
      alias Phoenix.LiveView.JS
      unquote(verified_routes())
    end
  end

  def verified_routes do
    quote do
      use Phoenix.VerifiedRoutes,
        endpoint: CrodRathausWeb.Endpoint,
        router: CrodRathausWeb.Router,
        statics: CrodRathausWeb.static_paths()
    end
  end

  defmacro __using__(which) when is_atom(which) do
    apply(__MODULE__, which, [])
  end
end
EOF

echo "Creating Python Parasit..."

# Python Parasit
cat > crod-parasit-python/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6666

CMD ["python", "-m", "src.main"]
EOF

cat > crod-parasit-python/requirements.txt << 'EOF'
asyncio-nats-client==0.11.5
websockets==12.0
aiohttp==3.9.1
python-json-logger==2.0.7
EOF

cat > crod-parasit-python/src/main.py << 'EOF'
import asyncio
import nats
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrodParasit:
    def __init__(self):
        self.nc = None
        self.patterns = {}
        self.websocket_clients = set()

    async def connect_nats(self):
        self.nc = await nats.connect("nats://nats:4222")
        logger.info("Connected to NATS")

    async def websocket_handler(self, websocket, path):
        self.websocket_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.websocket_clients.remove(websocket)

    async def intercept_claude(self):
        """Intercept Claude CLI commands and inject CROD patterns"""
        while True:
            # Simulate Claude interception
            event = {
                "type": "claude_intercept",
                "timestamp": datetime.utcnow().isoformat(),
                "pattern": "ich bins wieder",
                "confidence": 0.95
            }
            
            if self.nc:
                await self.nc.publish("crod.parasit.intercept", json.dumps(event).encode())
            
            # Broadcast to WebSocket clients
            if self.websocket_clients:
                await asyncio.gather(
                    *[ws.send(json.dumps(event)) for ws in self.websocket_clients],
                    return_exceptions=True
                )
            
            await asyncio.sleep(5)

    async def pattern_analyzer(self):
        """Analyze patterns in real-time"""
        trinity_values = {"ich": 2, "bins": 3, "wieder": 5, "daniel": 67, "claude": 71, "crod": 17}
        
        while True:
            pattern_event = {
                "type": "pattern_analysis",
                "timestamp": datetime.utcnow().isoformat(),
                "trinity": trinity_values,
                "prime_product": 2 * 3 * 5,
                "consciousness_level": 0.87
            }
            
            if self.nc:
                await self.nc.publish("crod.parasit.patterns", json.dumps(pattern_event).encode())
            
            await asyncio.sleep(3)

    async def start(self):
        await self.connect_nats()
        
        # Start WebSocket server
        ws_server = await websockets.serve(self.websocket_handler, "0.0.0.0", 6666)
        logger.info("WebSocket server started on port 6666")
        
        # Start background tasks
        await asyncio.gather(
            self.intercept_claude(),
            self.pattern_analyzer(),
            ws_server.wait_closed()
        )

if __name__ == "__main__":
    parasit = CrodParasit()
    asyncio.run(parasit.start())
EOF

echo "Creating Rust Pattern District..."

# Rust Pattern District
cat > crod-pattern-rust/Dockerfile << 'EOF'
FROM rust:1.75-alpine as builder

RUN apk add --no-cache musl-dev

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/target/release/crod-pattern /usr/local/bin/

EXPOSE 7007

CMD ["crod-pattern"]
EOF

cat > crod-pattern-rust/Cargo.toml << 'EOF'
[package]
name = "crod-pattern"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
axum = "0.7"
nats = "0.24"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
dashmap = "5"
rayon = "1.8"
tracing = "0.1"
tracing-subscriber = "0.3"
EOF

cat > crod-pattern-rust/src/main.rs << 'EOF'
use axum::{routing::get, Router, Json};
use dashmap::DashMap;
use nats::Connection;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::task;
use tracing::{info, error};

#[derive(Serialize, Deserialize)]
struct Pattern {
    id: String,
    value: String,
    prime: u64,
    timestamp: chrono::DateTime<chrono::Utc>,
}

#[derive(Clone)]
struct AppState {
    patterns: Arc<DashMap<String, Pattern>>,
    nats: Arc<Connection>,
}

async fn health() -> &'static str {
    "Pattern District Online"
}

async fn get_patterns(state: axum::extract::State<AppState>) -> Json<Vec<Pattern>> {
    let patterns: Vec<Pattern> = state.patterns
        .iter()
        .map(|entry| entry.value().clone())
        .collect();
    Json(patterns)
}

fn is_prime(n: u64) -> bool {
    if n < 2 { return false; }
    (2..=(n as f64).sqrt() as u64).all(|i| n % i != 0)
}

async fn calculate_prime_patterns(state: AppState) {
    loop {
        let numbers: Vec<u64> = (1000000..1001000).collect();
        let primes: Vec<u64> = numbers
            .par_iter()
            .filter(|&&n| is_prime(n))
            .cloned()
            .collect();

        for prime in primes {
            let pattern = Pattern {
                id: format!("prime_{}", prime),
                value: prime.to_string(),
                prime,
                timestamp: chrono::Utc::now(),
            };

            state.patterns.insert(pattern.id.clone(), pattern.clone());
            
            if let Ok(msg) = serde_json::to_string(&pattern) {
                let _ = state.nats.publish("crod.pattern.prime", msg.as_bytes());
            }
        }

        tokio::time::sleep(tokio::time::Duration::from_secs(10)).await;
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let nats_conn = match nats::connect("nats://nats:4222") {
        Ok(conn) => Arc::new(conn),
        Err(e) => {
            error!("Failed to connect to NATS: {}", e);
            std::process::exit(1);
        }
    };

    let app_state = AppState {
        patterns: Arc::new(DashMap::new()),
        nats: nats_conn,
    };

    // Spawn pattern calculator
    let calc_state = app_state.clone();
    tokio::spawn(calculate_prime_patterns(calc_state));

    // Build API
    let app = Router::new()
        .route("/", get(health))
        .route("/patterns", get(get_patterns))
        .with_state(app_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:7007")
        .await
        .unwrap();

    info!("Pattern District listening on :7007");
    axum::serve(listener, app).await.unwrap();
}
EOF

echo "Creating Go Memory Quarter..."

# Go Memory Quarter
cat > crod-memory-go/Dockerfile << 'EOF'
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o crod-memory cmd/main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/crod-memory /usr/local/bin/

EXPOSE 7031

CMD ["crod-memory"]
EOF

cat > crod-memory-go/go.mod << 'EOF'
module crod-memory

go 1.21

require (
    github.com/nats-io/nats.go v1.31.0
    github.com/gorilla/mux v1.8.1
)

require (
    github.com/nats-io/nkeys v0.4.6 // indirect
    github.com/nats-io/nuid v1.0.1 // indirect
    golang.org/x/crypto v0.16.0 // indirect
    golang.org/x/sys v0.15.0 // indirect
)
EOF

cat > crod-memory-go/cmd/main.go << 'EOF'
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "sync"
    "time"

    "github.com/gorilla/mux"
    "github.com/nats-io/nats.go"
)

type Memory struct {
    ID        string    `json:"id"`
    Data      string    `json:"data"`
    Timestamp time.Time `json:"timestamp"`
}

type MemoryStore struct {
    mu       sync.RWMutex
    memories map[string]*Memory
    sessions map[string][]string
}

func NewMemoryStore() *MemoryStore {
    return &MemoryStore{
        memories: make(map[string]*Memory),
        sessions: make(map[string][]string),
    }
}

func (ms *MemoryStore) Store(memory *Memory) {
    ms.mu.Lock()
    defer ms.mu.Unlock()
    ms.memories[memory.ID] = memory
}

func (ms *MemoryStore) Get(id string) (*Memory, bool) {
    ms.mu.RLock()
    defer ms.mu.RUnlock()
    mem, ok := ms.memories[id]
    return mem, ok
}

func (ms *MemoryStore) StartSession(sessionID string) {
    ms.mu.Lock()
    defer ms.mu.Unlock()
    ms.sessions[sessionID] = []string{}
}

func main() {
    store := NewMemoryStore()
    
    // Connect to NATS
    nc, err := nats.Connect("nats://nats:4222")
    if err != nil {
        log.Fatal("Failed to connect to NATS:", err)
    }
    defer nc.Close()

    // Subscribe to memory events
    nc.Subscribe("crod.memory.>", func(m *nats.Msg) {
        var memory Memory
        if err := json.Unmarshal(m.Data, &memory); err == nil {
            store.Store(&memory)
            log.Printf("Stored memory: %s", memory.ID)
        }
    })

    // Start concurrent memory workers
    for i := 0; i < 10; i++ {
        go memoryWorker(i, store, nc)
    }

    // Setup HTTP routes
    r := mux.NewRouter()
    r.HandleFunc("/", healthHandler).Methods("GET")
    r.HandleFunc("/memories", getMemoriesHandler(store)).Methods("GET")
    r.HandleFunc("/sessions", getSessionsHandler(store)).Methods("GET")

    log.Println("Memory Quarter listening on :7031")
    log.Fatal(http.ListenAndServe(":7031", r))
}

func memoryWorker(id int, store *MemoryStore, nc *nats.Connection) {
    for {
        memory := &Memory{
            ID:        fmt.Sprintf("worker_%d_%d", id, time.Now().Unix()),
            Data:      fmt.Sprintf("Memory from worker %d", id),
            Timestamp: time.Now(),
        }
        
        store.Store(memory)
        
        if data, err := json.Marshal(memory); err == nil {
            nc.Publish("crod.memory.created", data)
        }
        
        time.Sleep(time.Duration(5+id) * time.Second)
    }
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Memory Quarter Online"))
}

func getMemoriesHandler(store *MemoryStore) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        store.mu.RLock()
        defer store.mu.RUnlock()
        
        memories := make([]*Memory, 0, len(store.memories))
        for _, mem := range store.memories {
            memories = append(memories, mem)
        }
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(memories)
    }
}

func getSessionsHandler(store *MemoryStore) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        store.mu.RLock()
        defer store.mu.RUnlock()
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(store.sessions)
    }
}
EOF

echo "Creating JavaScript Gateway..."

# JavaScript Gateway
cat > crod-gateway-js/Dockerfile << 'EOF'
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 7888

CMD ["node", "src/index.js"]
EOF

cat > crod-gateway-js/package.json << 'EOF'
{
  "name": "crod-gateway",
  "version": "1.0.0",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "ws": "^8.16.0",
    "nats": "^2.18.0",
    "axios": "^1.6.2"
  }
}
EOF

cat > crod-gateway-js/src/index.js << 'EOF'
const express = require('express');
const WebSocket = require('ws');
const { connect } = require('nats');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(express.static('public'));

let nc;
const clients = new Set();

// Connect to NATS
(async () => {
  try {
    nc = await connect({ servers: 'nats://nats:4222' });
    console.log('Connected to NATS');
    
    // Subscribe to all CROD events
    const sub = nc.subscribe('crod.>');
    for await (const msg of sub) {
      const event = {
        topic: msg.subject,
        data: msg.string(),
        timestamp: new Date().toISOString()
      };
      
      // Broadcast to all WebSocket clients
      for (const client of clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(event));
        }
      }
    }
  } catch (err) {
    console.error('NATS connection error:', err);
  }
})();

// WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log('New WebSocket client connected');
  
  ws.on('close', () => {
    clients.delete(ws);
  });
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      if (nc) {
        nc.publish(`crod.gateway.${data.type}`, JSON.stringify(data));
      }
    } catch (err) {
      console.error('Message error:', err);
    }
  });
});

// API Routes
app.get('/', (req, res) => {
  res.send('CROD Gateway Online');
});

app.get('/api/status', async (req, res) => {
  const status = {
    gateway: 'online',
    websocket_clients: clients.size,
    districts: {}
  };
  
  // Check district health
  const districts = [
    { name: 'rathaus', url: 'http://crod-rathaus:4000' },
    { name: 'pattern', url: 'http://crod-pattern:7007' },
    { name: 'memory', url: 'http://crod-memory:7031' },
    { name: 'parasit', url: 'http://crod-parasit:6666' }
  ];
  
  for (const district of districts) {
    try {
      await axios.get(district.url, { timeout: 1000 });
      status.districts[district.name] = 'online';
    } catch (err) {
      status.districts[district.name] = 'offline';
    }
  }
  
  res.json(status);
});

// Dashboard HTML
app.get('/dashboard', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html>
<head>
  <title>CROD Gateway Dashboard</title>
  <style>
    body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
    .event { margin: 5px 0; padding: 5px; border: 1px solid #0f0; }
    #status { margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>CROD POLYGLOT CITY 2025 - GATEWAY</h1>
  <div id="status"></div>
  <h2>Live Events</h2>
  <div id="events"></div>
  
  <script>
    const ws = new WebSocket('ws://localhost:8080');
    const eventsDiv = document.getElementById('events');
    const statusDiv = document.getElementById('status');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const eventDiv = document.createElement('div');
      eventDiv.className = 'event';
      eventDiv.textContent = \`[\${data.timestamp}] \${data.topic}: \${data.data}\`;
      eventsDiv.insertBefore(eventDiv, eventsDiv.firstChild);
      
      if (eventsDiv.children.length > 50) {
        eventsDiv.removeChild(eventsDiv.lastChild);
      }
    };
    
    setInterval(async () => {
      try {
        const res = await fetch('/api/status');
        const status = await res.json();
        statusDiv.innerHTML = '<h3>District Status:</h3>' + 
          Object.entries(status.districts)
            .map(([name, status]) => \`\${name}: \${status}\`)
            .join(' | ');
      } catch (err) {
        console.error(err);
      }
    }, 5000);
  </script>
</body>
</html>
  `);
});

const PORT = process.env.PORT || 7888;
app.listen(PORT, () => {
  console.log(`Gateway listening on port ${PORT}`);
});
EOF

echo "Creating Docker Compose..."

# Docker Compose
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  nats:
    image: nats:2.10-alpine
    ports:
      - "4222:4222"
      - "8222:8222"
    command: "-m 8222"
    networks:
      - crod-network

  crod-rathaus:
    build: ./crod-rathaus-phoenix
    ports:
      - "4000:4000"
    environment:
      - MIX_ENV=dev
      - PORT=4000
    depends_on:
      - nats
    networks:
      - crod-network
    volumes:
      - ./crod-rathaus-phoenix:/app
    command: >
      sh -c "mix deps.get &&
             mix compile &&
             mix phx.server"

  crod-parasit:
    build: ./crod-parasit-python
    ports:
      - "6666:6666"
    depends_on:
      - nats
    networks:
      - crod-network
    volumes:
      - ./crod-parasit-python:/app

  crod-pattern:
    build: ./crod-pattern-rust
    ports:
      - "7007:7007"
    depends_on:
      - nats
    networks:
      - crod-network

  crod-memory:
    build: ./crod-memory-go
    ports:
      - "7031:7031"
    depends_on:
      - nats
    networks:
      - crod-network

  crod-gateway:
    build: ./crod-gateway-js
    ports:
      - "7888:7888"
      - "8080:8080"
    depends_on:
      - nats
      - crod-rathaus
      - crod-parasit
      - crod-pattern
      - crod-memory
    networks:
      - crod-network

networks:
  crod-network:
    driver: bridge

volumes:
  nats-data:
EOF

echo "Creating deployment script..."

# Deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Deploying CROD Polyglot City 2025..."

# Build all images
docker-compose build --parallel

# Start services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
echo "🏥 Checking service health..."
docker-compose ps

echo "✅ CROD Polyglot City deployed!"
echo ""
echo "📍 Service URLs:"
echo "  - Rathaus (Phoenix):    http://localhost:4000"
echo "  - Parasit (Python):     ws://localhost:6666"
echo "  - Pattern (Rust):       http://localhost:7007"
echo "  - Memory (Go):          http://localhost:7031"
echo "  - Gateway (JS):         http://localhost:7888"
echo "  - Gateway Dashboard:    http://localhost:7888/dashboard"
echo "  - NATS Monitor:         http://localhost:8222"
echo ""
echo "📊 View logs: docker-compose logs -f"
EOF

echo "Creating test script..."

# Test script
cat > test.sh << 'EOF'
#!/bin/bash

echo "🧪 Testing CROD Polyglot City services..."

# Function to check service
check_service() {
    local name=$1
    local url=$2
    
    if curl -s -f "$url" > /dev/null; then
        echo "✅ $name is online"
    else
        echo "❌ $name is offline"
    fi
}

# Wait for services
sleep 5

# Check each service
check_service "Phoenix Rathaus" "http://localhost:4000"
check_service "Rust Pattern District" "http://localhost:7007"
check_service "Go Memory Quarter" "http://localhost:7031"
check_service "JavaScript Gateway" "http://localhost:7888"

# Check Gateway API status
echo ""
echo "📊 Gateway Status:"
curl -s http://localhost:7888/api/status | jq .

# Check NATS
echo ""
echo "📡 NATS Status:"
curl -s http://localhost:8222/varz | jq '.connections, .in_msgs, .out_msgs' | head -10
EOF

# Make scripts executable
chmod +x setup-all.sh deploy.sh test.sh

echo "✅ All files created! Run ./setup-all.sh to complete setup"