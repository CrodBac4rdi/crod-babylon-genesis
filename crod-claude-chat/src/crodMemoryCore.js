#!/usr/bin/env node
/**
 * CROD Memory v1.0 - Simple but Working
 * Step-by-step evolution - nicht alles auf einmal!
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

class CRODMemoryV1 {
  constructor() {
    this.dbPath = path.join(__dirname, 'crod-brain-v1.db');
    this.db = null;
    console.log("🧠 CROD Memory v1.0 - Starting simple!");
  }
  
  // Step 1: Simple initialization
  init() {
    return new Promise((resolve, reject) => {
      this.db = new sqlite3.Database(this.dbPath, (err) => {
        if (err) {
          console.error('❌ Failed to open database:', err);
          reject(err);
        } else {
          console.log('✅ Database opened:', this.dbPath);
          this.createBasicTables().then(resolve).catch(reject);
        }
      });
    });
  }
  
  // Step 2: Only the ESSENTIAL tables first
  createBasicTables() {
    console.log('📊 Creating basic tables...');
    
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        // 1. User interactions - the CORE
        this.db.run(`
          CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_input TEXT,
            claude_output TEXT,
            crod_improved TEXT,
            user_happy INTEGER DEFAULT 0
          )
        `);
        
        // 2. What CROD learned
        this.db.run(`
          CREATE TABLE IF NOT EXISTS learnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            pattern TEXT,
            action TEXT,
            success INTEGER DEFAULT 0
          )
        `);
        
        // 3. Simple neurons (88 parameters)
        this.db.run(`
          CREATE TABLE IF NOT EXISTS neurons (
            token TEXT PRIMARY KEY,
            weight REAL DEFAULT 50.0,
            heat INTEGER DEFAULT 0
          )
        `, (err) => {
          if (err) reject(err);
          else {
            console.log('✅ Basic tables created!');
            resolve();
          }
        });
      });
    });
  }
  
  // Step 3: Save interaction (SIMPLE version)
  saveInteraction(data) {
    return new Promise((resolve, reject) => {
      const stmt = this.db.prepare(`
        INSERT INTO interactions (user_input, claude_output, crod_improved, user_happy)
        VALUES (?, ?, ?, ?)
      `);
      
      stmt.run(
        data.userInput,
        data.claudeOutput,
        data.crodImproved || data.claudeOutput,
        data.userHappy ? 1 : 0,
        function(err) {
          if (err) {
            console.error('❌ Save failed:', err);
            reject(err);
          } else {
            console.log('✅ Interaction saved! ID:', this.lastID);
            resolve(this.lastID);
          }
        }
      );
      
      stmt.finalize();
    });
  }
  
  // Step 4: Learn from pattern
  learn(pattern, action, success = false) {
    return new Promise((resolve, reject) => {
      this.db.run(
        "INSERT INTO learnings (pattern, action, success) VALUES (?, ?, ?)",
        [pattern, action, success ? 1 : 0],
        (err) => {
          if (err) reject(err);
          else {
            console.log(`📝 Learned: ${pattern} → ${action} (${success ? '✅' : '❌'})`);
            resolve();
          }
        }
      );
    });
  }
  
  // Step 5: Update neuron
  updateNeuron(token, heatIncrease = 1) {
    return new Promise((resolve, reject) => {
      this.db.run(`
        INSERT INTO neurons (token, heat) VALUES (?, ?)
        ON CONFLICT(token) DO UPDATE SET 
          heat = heat + ?,
          weight = MIN(100, weight + 0.1)
      `, [token, heatIncrease, heatIncrease], (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }
  
  // Step 6: Get stats (SIMPLE)
  getStats() {
    return new Promise((resolve, reject) => {
      const stats = {};
      
      this.db.get(
        "SELECT COUNT(*) as total, SUM(user_happy) as happy FROM interactions",
        (err, row) => {
          if (err) {
            reject(err);
          } else {
            stats.totalInteractions = row.total;
            stats.happyInteractions = row.happy;
            stats.happyRate = row.total > 0 ? (row.happy / row.total * 100).toFixed(1) : 0;
            
            this.db.get(
              "SELECT COUNT(*) as count FROM neurons",
              (err2, row2) => {
                if (err2) reject(err2);
                else {
                  stats.totalNeurons = row2.count;
                  resolve(stats);
                }
              }
            );
          }
        }
      );
    });
  }
  
  // Close database
  close() {
    return new Promise((resolve, reject) => {
      this.db.close((err) => {
        if (err) reject(err);
        else {
          console.log('👋 Database closed');
          resolve();
        }
      });
    });
  }
}

// DEMO - Show step-by-step evolution
async function demo() {
  console.log("🚀 CROD Memory v1.0 Demo");
  console.log("=" * 50);
  console.log("Building step-by-step, not everything at once!\n");
  
  const memory = new CRODMemoryV1();
  
  try {
    // Initialize
    await memory.init();
    
    // Simulate some interactions
    console.log("\n📝 Simulating interactions...\n");
    
    // Interaction 1: User frustrated
    await memory.saveInteraction({
      userInput: "mach mir ne blockchain wtf",
      claudeOutput: "I'll create a comprehensive quantum blockchain with 10,000 TPS...",
      crodImproved: "Ich mache dir eine simple blockchain",
      userHappy: true
    });
    
    // Learn from it
    await memory.learn("user_says_wtf", "keep_it_simple", true);
    await memory.updateNeuron("wtf", 5);
    await memory.updateNeuron("simple", 3);
    
    // Interaction 2: User happy
    await memory.saveInteraction({
      userInput: "nice, das ist gut",
      claudeOutput: "Thank you!",
      crodImproved: "Danke! Ich lerne weiter.",
      userHappy: true
    });
    
    await memory.learn("user_says_nice", "continue_this_style", true);
    await memory.updateNeuron("nice", 3);
    await memory.updateNeuron("gut", 3);
    
    // Show stats
    console.log("\n📊 Current Stats:");
    const stats = await memory.getStats();
    console.log(`Total Interactions: ${stats.totalInteractions}`);
    console.log(`Happy Rate: ${stats.happyRate}%`);
    console.log(`Active Neurons: ${stats.totalNeurons}`);
    
    await memory.close();
    
  } catch (error) {
    console.error("Error:", error);
  }
  
  console.log("\n✅ v1.0 Complete! Ready for v2.0 with more features!");
}

// Run if called directly
if (require.main === module) {
  demo();
}

module.exports = CRODMemoryV1;