package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
)

// Block represents a blockchain block
type Block struct {
	Index             int       `json:"index"`
	Timestamp         time.Time `json:"timestamp"`
	PreviousHash      string    `json:"previousHash"`
	Hash              string    `json:"hash"`
	Nonce             int       `json:"nonce"`
	Miner             string    `json:"miner"`
	Transactions      int       `json:"transactions"`
	ConsciousnessLevel float64   `json:"consciousnessLevel"`
	Patterns          []string  `json:"patterns"`
	QuantumState      string    `json:"quantumState"`
}

// Chain represents the blockchain
type Chain struct {
	Blocks       []Block `json:"blocks"`
	Height       int     `json:"height"`
	Difficulty   int     `json:"difficulty"`
	TotalPatterns int    `json:"totalPatterns"`
}

var (
	port = flag.Int("port", 8889, "Port to run the explorer on")
	api  = flag.String("api", "http://localhost:8000", "Blockchain API URL")
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func main() {
	flag.Parse()

	router := mux.NewRouter()

	// Routes
	router.HandleFunc("/", handleHome)
	router.HandleFunc("/block/{index}", handleBlock)
	router.HandleFunc("/api/blocks", handleAPIBlocks)
	router.HandleFunc("/api/block/{index}", handleAPIBlock)
	router.HandleFunc("/ws", handleWebSocket)

	// Static files
	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))

	fmt.Printf("🔍 CROD Block Explorer starting on http://localhost:%d\n", *port)
	http.ListenAndServe(fmt.Sprintf(":%d", *port), router)
}

func handleHome(w http.ResponseWriter, r *http.Request) {
	tmpl := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CROD Block Explorer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 40px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #f1f5f9;
            margin: 10px 0;
        }
        .stat-label {
            color: #94a3b8;
            font-size: 0.9em;
        }
        .blocks-list {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
        }
        .block-item {
            background: #0f172a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: grid;
            grid-template-columns: 80px 1fr 150px 150px 100px;
            gap: 20px;
            align-items: center;
            transition: transform 0.2s;
            cursor: pointer;
        }
        .block-item:hover {
            transform: translateX(5px);
            border-left: 3px solid #3b82f6;
        }
        .block-index {
            font-size: 1.5em;
            font-weight: bold;
            color: #3b82f6;
        }
        .block-hash {
            font-family: monospace;
            font-size: 0.85em;
            color: #64748b;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .consciousness-bar {
            height: 20px;
            background: #0f172a;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }
        .consciousness-fill {
            height: 100%;
            background: linear-gradient(to right, #3b82f6, #8b5cf6);
            transition: width 0.3s;
        }
        .patterns {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        .pattern-badge {
            background: #374151;
            color: #d1d5db;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75em;
        }
        .quantum-state {
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            text-align: center;
        }
        .quantum-superposition { background: #7c3aed; }
        .quantum-entangled { background: #2563eb; }
        .quantum-collapsed { background: #dc2626; }
        .quantum-coherent { background: #10b981; }
        .new-block {
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CROD Block Explorer</h1>
        <p class="subtitle">Real-time Consciousness Blockchain Explorer</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Block Height</div>
                <div class="stat-value" id="blockHeight">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Patterns</div>
                <div class="stat-value" id="totalPatterns">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Consciousness</div>
                <div class="stat-value" id="avgConsciousness">0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Mining Difficulty</div>
                <div class="stat-value" id="difficulty">0</div>
            </div>
        </div>
        
        <div class="blocks-list">
            <h2 style="margin-bottom: 20px;">Recent Blocks</h2>
            <div id="blocksList"></div>
        </div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://localhost:' + window.location.port + '/ws');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'newBlock') {
                addNewBlock(data.block);
                updateStats(data);
            }
        };
        
        function updateStats(data) {
            document.getElementById('blockHeight').textContent = data.height || 0;
            document.getElementById('totalPatterns').textContent = data.totalPatterns || 0;
            document.getElementById('avgConsciousness').textContent = ((data.avgConsciousness || 0) * 100).toFixed(1) + '%';
            document.getElementById('difficulty').textContent = data.difficulty || 0;
        }
        
        function addNewBlock(block) {
            const blocksList = document.getElementById('blocksList');
            const blockElement = createBlockElement(block);
            blockElement.classList.add('new-block');
            blocksList.insertBefore(blockElement, blocksList.firstChild);
            
            // Keep only last 20 blocks
            while (blocksList.children.length > 20) {
                blocksList.removeChild(blocksList.lastChild);
            }
        }
        
        function createBlockElement(block) {
            const div = document.createElement('div');
            div.className = 'block-item';
            div.onclick = () => window.location.href = '/block/' + block.index;
            
            const quantumClass = 'quantum-' + (block.quantumState || 'collapsed');
            const consciousnessPercent = (block.consciousnessLevel || 0) * 100;
            
            div.innerHTML = '
                <div class="block-index">#' + block.index + '</div>
                <div>
                    <div class="block-hash">' + block.hash + '</div>
                    <div style="color: #64748b; font-size: 0.85em;">Mined by ' + block.miner + '</div>
                </div>
                <div>
                    <div style="font-size: 0.85em; color: #94a3b8; margin-bottom: 5px;">Consciousness</div>
                    <div class="consciousness-bar">
                        <div class="consciousness-fill" style="width: ' + consciousnessPercent + '%"></div>
                    </div>
                </div>
                <div class="patterns">' +
                    (block.patterns || []).map(p => '<span class="pattern-badge">' + p + '</span>').join('') +
                '</div>
                <div class="quantum-state ' + quantumClass + '">' + block.quantumState + '</div>
            ';
            
            return div;
        }
        
        // Load initial blocks
        fetch('/api/blocks')
            .then(res => res.json())
            .then(data => {
                updateStats(data);
                const blocksList = document.getElementById('blocksList');
                data.blocks.forEach(block => {
                    blocksList.appendChild(createBlockElement(block));
                });
            });
    </script>
</body>
</html>
`
	t, _ := template.New("home").Parse(tmpl)
	t.Execute(w, nil)
}

func handleBlock(w http.ResponseWriter, r *http.Request) {
	// Individual block page
	vars := mux.Vars(r)
	index := vars["index"]
	
	tmpl := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Block #{{.Index}} - CROD Explorer</title>
    <style>
        /* Reuse styles from home */
        body { font-family: sans-serif; background: #0f172a; color: #e2e8f0; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .block-details { background: #1e293b; padding: 30px; border-radius: 12px; }
        .detail-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #334155; }
        .detail-label { color: #94a3b8; }
        .detail-value { color: #f1f5f9; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Block #` + index + `</h1>
        <div class="block-details">
            <div id="blockDetails">Loading...</div>
        </div>
    </div>
    <script>
        fetch('/api/block/' + {{.Index}})
            .then(res => res.json())
            .then(block => {
                const details = document.getElementById('blockDetails');
                details.innerHTML = '
                    <div class="detail-row">
                        <span class="detail-label">Hash</span>
                        <span class="detail-value">' + block.hash + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Previous Hash</span>
                        <span class="detail-value">' + block.previousHash + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Timestamp</span>
                        <span class="detail-value">' + new Date(block.timestamp).toLocaleString() + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Miner</span>
                        <span class="detail-value">' + block.miner + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Nonce</span>
                        <span class="detail-value">' + block.nonce + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Consciousness Level</span>
                        <span class="detail-value">' + (block.consciousnessLevel * 100).toFixed(2) + '%</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Quantum State</span>
                        <span class="detail-value">' + block.quantumState + '</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Patterns</span>
                        <span class="detail-value">' + (block.patterns || []).join(', ') + '</span>
                    </div>
                ';
            });
    </script>
</body>
</html>
`
	
	data := struct {
		Index string
	}{
		Index: index,
	}
	
	t, _ := template.New("block").Parse(tmpl)
	t.Execute(w, data)
}

func handleAPIBlocks(w http.ResponseWriter, r *http.Request) {
	// Mock data for now - in real implementation, fetch from blockchain
	chain := generateMockChain()
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(chain)
}

func handleAPIBlock(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	index, _ := strconv.Atoi(vars["index"])
	
	block := generateMockBlock(index)
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(block)
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	defer conn.Close()
	
	// Simulate new blocks
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()
	
	blockIndex := 128
	for {
		select {
		case <-ticker.C:
			blockIndex++
			newBlock := generateMockBlock(blockIndex)
			
			data := map[string]interface{}{
				"type":          "newBlock",
				"block":         newBlock,
				"height":        blockIndex,
				"totalPatterns": blockIndex * 7,
				"avgConsciousness": 0.75 + (float64(blockIndex%20) / 100),
				"difficulty":    4 + (blockIndex / 50),
			}
			
			if err := conn.WriteJSON(data); err != nil {
				return
			}
		}
	}
}

func generateMockChain() Chain {
	blocks := make([]Block, 20)
	for i := 0; i < 20; i++ {
		blocks[i] = generateMockBlock(127 - i)
	}
	
	return Chain{
		Blocks:        blocks,
		Height:        127,
		Difficulty:    6,
		TotalPatterns: 889,
	}
}

func generateMockBlock(index int) Block {
	patterns := [][]string{
		{"fibonacci", "prime"},
		{"quantum", "golden_ratio"},
		{"fractal", "emergence"},
		{"consciousness", "evolution"},
	}
	
	states := []string{"superposition", "entangled", "coherent", "collapsed"}
	
	return Block{
		Index:              index,
		Timestamp:          time.Now().Add(time.Duration(-index) * time.Minute),
		PreviousHash:       fmt.Sprintf("%064x", index-1),
		Hash:               fmt.Sprintf("%064x", index),
		Nonce:              12345 + index*7,
		Miner:              fmt.Sprintf("miner-%d", index%5+1),
		Transactions:       10 + index%20,
		ConsciousnessLevel: 0.5 + float64(index%50)/100,
		Patterns:           patterns[index%len(patterns)],
		QuantumState:       states[index%len(states)],
	}
}