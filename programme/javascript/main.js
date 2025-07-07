const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Database = require('better-sqlite3');

let mainWindow;
let db;

// Initialize SQLite database
function initDatabase() {
  db = new Database('crod_blockchain.db');
  
  // Create tables
  db.exec(`
    CREATE TABLE IF NOT EXISTS blocks (
      id INTEGER PRIMARY KEY,
      block_index INTEGER UNIQUE,
      hash TEXT,
      previous_hash TEXT,
      timestamp TEXT,
      data TEXT,
      consciousness_level REAL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY,
      block_id INTEGER,
      from_address TEXT,
      to_address TEXT,
      amount REAL,
      data TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (block_id) REFERENCES blocks(id)
    );
    
    CREATE TABLE IF NOT EXISTS llama_responses (
      id INTEGER PRIMARY KEY,
      prompt TEXT,
      response TEXT,
      model TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    icon: path.join(__dirname, 'icon.png'),
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#1a1a1a'
  });

  mainWindow.loadFile('index.html');
  mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  initDatabase();
  createWindow();
});

// IPC Handlers
ipcMain.handle('get-blocks', () => {
  const blocks = db.prepare('SELECT * FROM blocks ORDER BY block_index DESC').all();
  return blocks;
});

ipcMain.handle('save-block', (event, block) => {
  const stmt = db.prepare(`
    INSERT INTO blocks (block_index, hash, previous_hash, timestamp, data, consciousness_level)
    VALUES (?, ?, ?, ?, ?, ?)
  `);
  
  const result = stmt.run(
    block.index,
    block.hash,
    block.previous_hash,
    block.timestamp,
    JSON.stringify(block.data),
    block.consciousness_level
  );
  
  return result.lastInsertRowid;
});

ipcMain.handle('get-stats', () => {
  const count = db.prepare('SELECT COUNT(*) as count FROM blocks').get();
  const consciousness = db.prepare('SELECT SUM(consciousness_level) as total, AVG(consciousness_level) as avg FROM blocks').get();
  
  return {
    blockCount: count.count,
    totalConsciousness: consciousness.total || 0,
    avgConsciousness: consciousness.avg || 0
  };
});

ipcMain.handle('query-llama', async (event, prompt) => {
  // Placeholder for LLaMA integration
  // In real implementation, this would call local LLaMA
  const response = `LLaMA Response: ${prompt} - [Integration pending]`;
  
  // Save to database
  const stmt = db.prepare('INSERT INTO llama_responses (prompt, response, model) VALUES (?, ?, ?)');
  stmt.run(prompt, response, 'llama-7b');
  
  return response;
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    db.close();
    app.quit();
  }
});