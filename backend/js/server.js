// CROD Backend Server
// Centralisierter API-Gateway für alle CROD-Services

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');
const sqlite3 = require('sqlite3').verbose();
const { open } = require('sqlite');

// Server konfiguration
const PORT = process.env.PORT || 3001;
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../../frontend/build')));

// Datenbank initialisieren
let db;
async function initDatabase() {
  // SQLite Datenbank öffnen
  db = await open({
    filename: path.join(__dirname, '../../data/crod.db'),
    driver: sqlite3.Database
  });

  // Tabellen erstellen, falls sie nicht existieren
  await db.exec(`
    CREATE TABLE IF NOT EXISTS chat_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_message TEXT,
      ai_response TEXT,
      model TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS generated_images (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      prompt TEXT,
      file_path TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS code_executions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT,
      language TEXT,
      output TEXT,
      exit_code INTEGER,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
  
  console.log('Database initialized');
}

// Clients speichern
const clients = new Set();

// WebSocket Verbindungshandling
wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);
  
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      console.log(`Received: ${data.type}`);
      
      switch (data.type) {
        case 'chat':
          // Chat-Nachricht verarbeiten und an AI-Service senden
          const aiResponse = await processChat(data.content, data.model);
          ws.send(JSON.stringify({
            type: 'chat_response',
            data: aiResponse
          }));
          break;
          
        case 'generate_image':
          // Bildgenerierung starten
          const imageResult = await generateImage(data.prompt);
          ws.send(JSON.stringify({
            type: 'image_generated',
            data: imageResult
          }));
          break;
          
        case 'execute_code':
          // Code ausführen
          const executionResult = await executeCode(data.code, data.language);
          ws.send(JSON.stringify({
            type: 'code_execution_result',
            data: executionResult
          }));
          break;
          
        default:
          ws.send(JSON.stringify({
            type: 'error',
            data: { message: 'Unknown command' }
          }));
      }
    } catch (error) {
      console.error('Error processing message:', error);
      ws.send(JSON.stringify({
        type: 'error',
        data: { message: error.message }
      }));
    }
  });
  
  ws.on('close', () => {
    clients.delete(ws);
    console.log('Client disconnected');
  });
  
  // Initial status senden
  ws.send(JSON.stringify({
    type: 'status',
    data: { status: 'connected', message: 'Connected to CROD Backend' }
  }));
});

// Broadcast zu allen verbundenen Clients
function broadcast(data) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}

// AI Chat-Anfrage verarbeiten
async function processChat(message, model = 'claude') {
  console.log(`Processing chat message using ${model}`);
  
  try {
    // Python AI-Service aufrufen
    const response = await callPythonService('chat_service', {
      message,
      model
    });
    
    // In Datenbank speichern
    await db.run(
      'INSERT INTO chat_history (user_message, ai_response, model) VALUES (?, ?, ?)',
      [message, response.content, model]
    );
    
    return response;
  } catch (error) {
    console.error('Error in chat processing:', error);
    return {
      content: "Es ist ein Fehler aufgetreten. Bitte versuche es später noch einmal.",
      model: model,
      success: false
    };
  }
}

// Bildgenerierung starten
async function generateImage(prompt) {
  console.log(`Generating image with prompt: ${prompt}`);
  
  try {
    // Python Bildgenerator aufrufen
    const result = await callPythonService('image_generator', {
      prompt
    });
    
    // In Datenbank speichern
    if (result.success) {
      await db.run(
        'INSERT INTO generated_images (prompt, file_path) VALUES (?, ?)',
        [prompt, result.file_path]
      );
    }
    
    return result;
  } catch (error) {
    console.error('Error in image generation:', error);
    return {
      success: false,
      message: "Bildgenerierung fehlgeschlagen",
      error: error.message
    };
  }
}

// Code ausführen
async function executeCode(code, language) {
  console.log(`Executing ${language} code`);
  
  try {
    // Rust-Service für Code-Ausführung aufrufen
    const result = await callRustService('code_executor', {
      code,
      language
    });
    
    // In Datenbank speichern
    await db.run(
      'INSERT INTO code_executions (code, language, output, exit_code) VALUES (?, ?, ?, ?)',
      [code, language, result.output, result.exit_code]
    );
    
    return result;
  } catch (error) {
    console.error('Error in code execution:', error);
    return {
      output: error.message,
      exit_code: 1,
      language: language,
      execution_time_ms: 0,
      success: false
    };
  }
}

// Python-Service aufrufen
async function callPythonService(service, data) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [
      path.join(__dirname, '../python', `${service}.py`)
    ]);
    
    let result = '';
    let errorOutput = '';
    
    pythonProcess.stdin.write(JSON.stringify(data));
    pythonProcess.stdin.end();
    
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python service failed with code ${code}: ${errorOutput}`));
      } else {
        try {
          resolve(JSON.parse(result));
        } catch (error) {
          reject(new Error(`Failed to parse Python service response: ${error.message}`));
        }
      }
    });
  });
}

// Rust-Service aufrufen
async function callRustService(service, data) {
  return new Promise((resolve, reject) => {
    const rustProcess = spawn(
      path.join(__dirname, '../rust', service),
      [],
      { stdio: ['pipe', 'pipe', 'pipe'] }
    );
    
    let result = '';
    let errorOutput = '';
    
    rustProcess.stdin.write(JSON.stringify(data));
    rustProcess.stdin.end();
    
    rustProcess.stdout.on('data', (data) => {
      result += data.toString();
    });
    
    rustProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    rustProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Rust service failed with code ${code}: ${errorOutput}`));
      } else {
        try {
          resolve(JSON.parse(result));
        } catch (error) {
          reject(new Error(`Failed to parse Rust service response: ${error.message}`));
        }
      }
    });
  });
}

// REST API Endpoints

// System Status
app.get('/api/status', (req, res) => {
  res.json({
    status: 'online',
    version: '1.0.0',
    services: {
      chat: true,
      imageGenerator: true,
      codeExecutor: true
    },
    uptime: process.uptime()
  });
});

// Chat History abrufen
app.get('/api/chat/history', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const history = await db.all(
      'SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?',
      [limit]
    );
    res.json(history);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generierte Bilder abrufen
app.get('/api/images', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 20;
    const images = await db.all(
      'SELECT * FROM generated_images ORDER BY timestamp DESC LIMIT ?',
      [limit]
    );
    res.json(images);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Code-Ausführungen abrufen
app.get('/api/code/executions', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 20;
    const executions = await db.all(
      'SELECT * FROM code_executions ORDER BY timestamp DESC LIMIT ?',
      [limit]
    );
    res.json(executions);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Pfad zur Bilddatei
app.get('/api/images/:id', async (req, res) => {
  try {
    const image = await db.get(
      'SELECT * FROM generated_images WHERE id = ?',
      [req.params.id]
    );
    
    if (!image) {
      return res.status(404).json({ error: 'Image not found' });
    }
    
    res.sendFile(path.resolve(image.file_path));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Server starten
async function startServer() {
  try {
    await initDatabase();
    
    server.listen(PORT, () => {
      console.log(`
╔═══════════════════════════════════════════════════════════════╗
║          CROD UNIFIED BACKEND SERVER STARTED!                ║
║--------------------------------------------------------------|║
║  REST API:     http://localhost:${PORT}/api                    ║
║  WebSocket:    ws://localhost:${PORT}                          ║
║  Frontend:     http://localhost:${PORT}                        ║
╚═══════════════════════════════════════════════════════════════╝
      `);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Bei Ctrl+C Server herunterfahren
process.on('SIGINT', async () => {
  console.log('\nShutting down server...');
  
  if (db) {
    await db.close();
    console.log('Database connection closed');
  }
  
  server.close(() => {
    console.log('Server stopped');
    process.exit(0);
  });
});

// Server starten
startServer();

module.exports = server;
