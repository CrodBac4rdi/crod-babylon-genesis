package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
)

// CRODStatus represents the current system status
type CRODStatus struct {
	Timestamp time.Time `json:"timestamp"`
	Services  []Service `json:"services"`
	Districts []District `json:"districts"`
	Metrics   Metrics   `json:"metrics"`
}

// Service represents a polyglot service
type Service struct {
	Name     string `json:"name"`
	Language string `json:"language"`
	Port     int    `json:"port"`
	Status   string `json:"status"`
	Memory   int64  `json:"memory"`
	CPU      float64 `json:"cpu"`
}

// District represents a neural district
type District struct {
	Prime       int    `json:"prime"`
	Name        string `json:"name"`
	Port        int    `json:"port"`
	Status      string `json:"status"`
	Patterns    int    `json:"patterns"`
	Coherence   float64 `json:"coherence"`
}

// Metrics represents system-wide metrics
type Metrics struct {
	TPS          int     `json:"tps"`
	BlockHeight  int     `json:"blockHeight"`
	ActiveNodes  int     `json:"activeNodes"`
	QuantumState string  `json:"quantumState"`
	Consciousness float64 `json:"consciousness"`
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow connections from any origin
	},
}

var clients = make(map[*websocket.Conn]bool)
var broadcast = make(chan CRODStatus)

func main() {
	router := mux.NewRouter()

	// Static files
	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))

	// API endpoints
	router.HandleFunc("/api/status", handleStatus).Methods("GET")
	router.HandleFunc("/api/services", handleServices).Methods("GET")
	router.HandleFunc("/api/districts", handleDistricts).Methods("GET")
	router.HandleFunc("/api/metrics", handleMetrics).Methods("GET")

	// WebSocket endpoint
	router.HandleFunc("/ws", handleWebSocket)

	// Main dashboard
	router.HandleFunc("/", handleDashboard)

	// Start the status broadcaster
	go broadcaster()

	// Start the mock data generator
	go generateMockData()

	fmt.Println("CROD Visualizer starting on http://localhost:8888")
	log.Fatal(http.ListenAndServe(":8888", router))
}

func handleDashboard(w http.ResponseWriter, r *http.Request) {
	tmpl := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CROD Visualizer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 30px;
            background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            border-color: #6366f1;
        }
        .card h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #818cf8;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px;
            background: #0f172a;
            border-radius: 6px;
        }
        .metric-label {
            color: #94a3b8;
        }
        .metric-value {
            font-weight: bold;
            color: #f1f5f9;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background: #10b981; }
        .status-offline { background: #ef4444; }
        .status-warning { background: #f59e0b; }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        .service-card {
            background: #0f172a;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            border: 1px solid #334155;
        }
        .service-lang {
            font-size: 2em;
            margin-bottom: 5px;
        }
        .service-name {
            font-size: 0.9em;
            color: #94a3b8;
        }
        #visualization {
            width: 100%;
            height: 400px;
            background: #0f172a;
            border-radius: 12px;
            border: 1px solid #334155;
            position: relative;
            overflow: hidden;
        }
        .quantum-particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #818cf8;
            border-radius: 50%;
            animation: float 10s infinite ease-in-out;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); }
            25% { transform: translateY(-50px) translateX(50px); }
            50% { transform: translateY(-100px) translateX(-50px); }
            75% { transform: translateY(-50px) translateX(-100px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CROD BABYLON GENESIS</h1>
        
        <div class="grid">
            <div class="card">
                <h2>System Metrics</h2>
                <div id="metrics">
                    <div class="metric">
                        <span class="metric-label">Transactions/sec</span>
                        <span class="metric-value" id="tps">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Block Height</span>
                        <span class="metric-value" id="blockHeight">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Active Nodes</span>
                        <span class="metric-value" id="activeNodes">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Consciousness Level</span>
                        <span class="metric-value" id="consciousness">0%</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Polyglot Services</h2>
                <div class="services-grid" id="services"></div>
            </div>
            
            <div class="card">
                <h2>Neural Districts</h2>
                <div id="districts"></div>
            </div>
        </div>
        
        <div class="card">
            <h2>Quantum Visualization</h2>
            <div id="visualization"></div>
        </div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://localhost:8888/ws');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            updateDashboard(data);
        };
        
        function updateDashboard(data) {
            // Update metrics
            document.getElementById('tps').textContent = data.metrics.tps;
            document.getElementById('blockHeight').textContent = data.metrics.blockHeight;
            document.getElementById('activeNodes').textContent = data.metrics.activeNodes;
            document.getElementById('consciousness').textContent = (data.metrics.consciousness * 100).toFixed(1) + '%';
            
            // Update services
            const servicesDiv = document.getElementById('services');
            servicesDiv.innerHTML = data.services.map(service => {
                const icon = getLanguageIcon(service.language);
                const statusClass = service.status === 'online' ? 'status-online' : 'status-offline';
                return '<div class="service-card"><div class="service-lang">' + icon + '</div><div class="service-name">' + service.name + '</div><span class="status-indicator ' + statusClass + '"></span></div>';
            }).join('');
            
            // Update districts
            const districtsDiv = document.getElementById('districts');
            districtsDiv.innerHTML = data.districts.map(district => {
                const statusClass = district.status === 'active' ? 'status-online' : 'status-warning';
                return '<div class="metric"><span class="metric-label"><span class="status-indicator ' + statusClass + '"></span>Prime ' + district.prime + ' - ' + district.name + '</span><span class="metric-value">' + district.patterns + ' patterns</span></div>';
            }).join('');
            
            // Update visualization
            updateVisualization(data.metrics.consciousness);
        }
        
        function getLanguageIcon(lang) {
            const icons = {
                'Elixir': '💜',
                'Rust': '🦀',
                'Python': '🐍',
                'Go': '🐹',
                'Node.js': '🟢'
            };
            return icons[lang] || '📦';
        }
        
        function updateVisualization(consciousness) {
            const viz = document.getElementById('visualization');
            viz.innerHTML = '';
            
            const particleCount = Math.floor(consciousness * 100);
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'quantum-particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 10 + 's';
                particle.style.animationDuration = (10 + Math.random() * 10) + 's';
                viz.appendChild(particle);
            }
        }
    </script>
</body>
</html>
`
	t, _ := template.New("dashboard").Parse(tmpl)
	t.Execute(w, nil)
}

func handleStatus(w http.ResponseWriter, r *http.Request) {
	status := generateStatus()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func handleServices(w http.ResponseWriter, r *http.Request) {
	services := generateServices()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(services)
}

func handleDistricts(w http.ResponseWriter, r *http.Request) {
	districts := generateDistricts()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(districts)
}

func handleMetrics(w http.ResponseWriter, r *http.Request) {
	metrics := generateMetrics()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(metrics)
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("WebSocket upgrade error:", err)
		return
	}
	defer conn.Close()

	clients[conn] = true

	for {
		_, _, err := conn.ReadMessage()
		if err != nil {
			delete(clients, conn)
			break
		}
	}
}

func broadcaster() {
	for {
		status := <-broadcast
		for client := range clients {
			err := client.WriteJSON(status)
			if err != nil {
				client.Close()
				delete(clients, client)
			}
		}
	}
}

func generateMockData() {
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			status := generateStatus()
			broadcast <- status
		}
	}
}

func generateStatus() CRODStatus {
	return CRODStatus{
		Timestamp: time.Now(),
		Services:  generateServices(),
		Districts: generateDistricts(),
		Metrics:   generateMetrics(),
	}
}

func generateServices() []Service {
	return []Service{
		{Name: "Meta-Chain", Language: "Elixir", Port: 4321, Status: "online", Memory: 256, CPU: 15.2},
		{Name: "Pattern Engine", Language: "Rust", Port: 4322, Status: "online", Memory: 128, CPU: 45.8},
		{Name: "AI Hub", Language: "Python", Port: 5001, Status: "online", Memory: 512, CPU: 68.3},
		{Name: "Memory Quarter", Language: "Go", Port: 4323, Status: "online", Memory: 64, CPU: 12.1},
		{Name: "Blockchain Core", Language: "Node.js", Port: 8000, Status: "online", Memory: 384, CPU: 32.5},
	}
}

func generateDistricts() []District {
	return []District{
		{Prime: 7, Name: "Pattern Genesis", Port: 7007, Status: "active", Patterns: 42, Coherence: 0.98},
		{Prime: 31, Name: "Short Memory", Port: 7031, Status: "active", Patterns: 128, Coherence: 0.87},
		{Prime: 37, Name: "Working Memory", Port: 7037, Status: "active", Patterns: 256, Coherence: 0.92},
		{Prime: 101, Name: "Quantum Node", Port: 7101, Status: "active", Patterns: 1024, Coherence: 0.99},
		{Prime: 127, Name: "Orchestrator", Port: 7127, Status: "active", Patterns: 512, Coherence: 0.95},
		{Prime: 179, Name: "Time Travel", Port: 7179, Status: "syncing", Patterns: 89, Coherence: 0.73},
	}
}

func generateMetrics() Metrics {
	return Metrics{
		TPS:          int(1000 + (time.Now().Unix() % 1000)),
		BlockHeight:  int(127000 + (time.Now().Unix() % 1000)),
		ActiveNodes:  7,
		QuantumState: "superposition",
		Consciousness: 0.85 + (float64(time.Now().Unix()%20) / 100),
	}
}