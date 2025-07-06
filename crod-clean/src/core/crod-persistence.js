const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Create database directory
const dbDir = path.join(__dirname, '../data');
const fs = require('fs');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

// Initialize SQLite database
const db = new sqlite3.Database(path.join(dbDir, 'crod.db'));

// Create tables
db.serialize(() => {
    // Neural Processing Results
    db.run(`CREATE TABLE IF NOT EXISTS neural_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT,
        patterns TEXT,
        confidence REAL,
        neurons_activated INTEGER,
        processing_time REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // ML Learning History
    db.run(`CREATE TABLE IF NOT EXISTS ml_learning (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        learned_patterns INTEGER,
        accuracy_improvement TEXT,
        new_connections INTEGER,
        evolution_score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Visualization History
    db.run(`CREATE TABLE IF NOT EXISTS visualizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        complexity INTEGER,
        colors TEXT,
        dimensions TEXT,
        animated BOOLEAN,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Pattern Discovery
    db.run(`CREATE TABLE IF NOT EXISTS patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern_name TEXT UNIQUE,
        occurrences INTEGER DEFAULT 1,
        confidence_avg REAL,
        last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
        metadata TEXT
    )`);

    // System Events
    db.run(`CREATE TABLE IF NOT EXISTS system_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        service TEXT,
        data TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
});

// Database functions
const persistence = {
    // Save neural processing result
    saveNeuralResult: (result) => {
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO neural_results (input, patterns, confidence, neurons_activated, processing_time) 
                 VALUES (?, ?, ?, ?, ?)`,
                [
                    result.input,
                    JSON.stringify(result.patterns),
                    result.confidence,
                    result.neurons_activated,
                    result.processing_time
                ],
                function(err) {
                    if (err) reject(err);
                    else resolve({ id: this.lastID, ...result });
                }
            );
        });
    },

    // Save ML learning result
    saveLearningResult: (result, data) => {
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO ml_learning (data, learned_patterns, accuracy_improvement, new_connections, evolution_score) 
                 VALUES (?, ?, ?, ?, ?)`,
                [
                    JSON.stringify(data),
                    result.learned_patterns,
                    result.accuracy_improvement,
                    result.new_connections,
                    result.evolution_score
                ],
                function(err) {
                    if (err) reject(err);
                    else resolve({ id: this.lastID, ...result });
                }
            );
        });
    },

    // Save visualization
    saveVisualization: (viz) => {
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO visualizations (type, complexity, colors, dimensions, animated) 
                 VALUES (?, ?, ?, ?, ?)`,
                [
                    viz.type,
                    viz.complexity,
                    JSON.stringify(viz.colors),
                    JSON.stringify(viz.dimensions),
                    viz.animated ? 1 : 0
                ],
                function(err) {
                    if (err) reject(err);
                    else resolve({ id: this.lastID, ...viz });
                }
            );
        });
    },

    // Update pattern discovery
    updatePattern: (patternName, confidence) => {
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO patterns (pattern_name, confidence_avg) 
                 VALUES (?, ?)
                 ON CONFLICT(pattern_name) DO UPDATE SET
                 occurrences = occurrences + 1,
                 confidence_avg = (confidence_avg * occurrences + ?) / (occurrences + 1),
                 last_seen = CURRENT_TIMESTAMP`,
                [patternName, confidence, confidence],
                function(err) {
                    if (err) reject(err);
                    else resolve({ pattern: patternName, updated: true });
                }
            );
        });
    },

    // Log system event
    logEvent: (eventType, service, data) => {
        return new Promise((resolve, reject) => {
            db.run(
                `INSERT INTO system_events (event_type, service, data) VALUES (?, ?, ?)`,
                [eventType, service, JSON.stringify(data)],
                function(err) {
                    if (err) reject(err);
                    else resolve({ id: this.lastID });
                }
            );
        });
    },

    // Get recent neural results
    getRecentNeuralResults: (limit = 10) => {
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT * FROM neural_results ORDER BY timestamp DESC LIMIT ?`,
                [limit],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        ...row,
                        patterns: JSON.parse(row.patterns)
                    })));
                }
            );
        });
    },

    // Get pattern statistics
    getPatternStats: () => {
        return new Promise((resolve, reject) => {
            db.all(
                `SELECT * FROM patterns ORDER BY occurrences DESC`,
                [],
                (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows);
                }
            );
        });
    },

    // Get system metrics
    getSystemMetrics: () => {
        return new Promise((resolve, reject) => {
            const queries = {
                totalNeuralProcessing: 'SELECT COUNT(*) as count FROM neural_results',
                totalLearning: 'SELECT COUNT(*) as count FROM ml_learning',
                totalVisualizations: 'SELECT COUNT(*) as count FROM visualizations',
                totalPatterns: 'SELECT COUNT(*) as count FROM patterns',
                avgConfidence: 'SELECT AVG(confidence) as avg FROM neural_results',
                avgNeurons: 'SELECT AVG(neurons_activated) as avg FROM neural_results'
            };

            const metrics = {};
            const promises = Object.entries(queries).map(([key, query]) => {
                return new Promise((res) => {
                    db.get(query, (err, row) => {
                        if (!err && row) {
                            metrics[key] = row.count || row.avg || 0;
                        }
                        res();
                    });
                });
            });

            Promise.all(promises).then(() => resolve(metrics));
        });
    }
};

module.exports = { db, persistence };