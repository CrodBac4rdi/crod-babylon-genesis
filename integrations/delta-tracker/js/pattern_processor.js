#!/usr/bin/env node
/**
 * CROD Pattern Processor - JavaScript Teil für Pattern Matching
 */

const fs = require('fs');

class PatternProcessor {
    constructor() {
        // Core patterns from CROD
        this.corePatterns = {
            'ich_bins_wieder': {
                atoms: [2, 3, 5],
                strength: 15.0,
                type: 'activation'
            },
            'daniel_claude': {
                atoms: [67, 71],
                strength: 12.0,
                type: 'collaboration'
            },
            'crod_system': {
                atoms: [17, 23],
                strength: 10.0,
                type: 'meta'
            }
        };
        
        this.primeMap = {
            2: 'ich',
            3: 'bins', 
            5: 'wieder',
            17: 'crod',
            67: 'daniel',
            71: 'claude'
        };
    }
    
    findPatternMatches(tokens) {
        const matches = [];
        
        // Convert tokens to lowercase for matching
        const normalizedTokens = tokens.map(t => t.toLowerCase());
        const tokenSet = new Set(normalizedTokens);
        
        // Check each known pattern
        for (const [patternName, pattern] of Object.entries(this.corePatterns)) {
            const atomTokens = pattern.atoms.map(prime => this.primeMap[prime] || '');
            const matchCount = atomTokens.filter(token => tokenSet.has(token)).length;
            
            if (matchCount > 0) {
                const matchStrength = (matchCount / atomTokens.length) * pattern.strength;
                matches.push({
                    pattern: patternName,
                    matched_atoms: atomTokens.filter(token => tokenSet.has(token)),
                    match_ratio: matchCount / atomTokens.length,
                    strength: matchStrength,
                    type: pattern.type
                });
            }
        }
        
        return matches;
    }
    
    generatePatternGraph(patterns) {
        // Create adjacency graph of patterns
        const graph = {};
        
        patterns.forEach(p1 => {
            graph[p1.pattern] = [];
            patterns.forEach(p2 => {
                if (p1.pattern !== p2.pattern) {
                    // Find common atoms
                    const common = p1.matched_atoms.filter(a => 
                        p2.matched_atoms.includes(a)
                    );
                    
                    if (common.length > 0) {
                        graph[p1.pattern].push({
                            target: p2.pattern,
                            weight: common.length,
                            common_atoms: common
                        });
                    }
                }
            });
        });
        
        return graph;
    }
    
    calculateEmergence(patterns, graph) {
        // Calculate emergence score based on pattern interactions
        let emergence = 0;
        
        for (const [pattern, connections] of Object.entries(graph)) {
            const patternData = patterns.find(p => p.pattern === pattern);
            if (!patternData) continue;
            
            // Base emergence from pattern strength
            emergence += patternData.strength;
            
            // Additional emergence from connections
            connections.forEach(conn => {
                emergence += conn.weight * 0.5;
            });
        }
        
        // Apply CROD-style activation
        const phi = 1.618033988749;
        return emergence * phi;
    }
    
    processRequest(data) {
        const tokens = data.tokens || [];
        
        // Find pattern matches
        const patterns = this.findPatternMatches(tokens);
        
        // Generate pattern graph
        const graph = this.generatePatternGraph(patterns);
        
        // Calculate emergence
        const emergence = this.calculateEmergence(patterns, graph);
        
        // Find strongest pattern
        const dominantPattern = patterns.reduce((max, p) => 
            p.strength > (max?.strength || 0) ? p : max
        , null);
        
        return {
            patterns: patterns,
            pattern_graph: graph,
            emergence_score: emergence,
            dominant_pattern: dominantPattern,
            metrics: {
                total_patterns: patterns.length,
                avg_strength: patterns.reduce((sum, p) => sum + p.strength, 0) / (patterns.length || 1),
                graph_connections: Object.values(graph).reduce((sum, conns) => sum + conns.length, 0)
            }
        };
    }
}

// Main execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log(JSON.stringify({error: 'No input provided'}));
        process.exit(1);
    }
    
    try {
        const input = JSON.parse(args[0]);
        const processor = new PatternProcessor();
        const result = processor.processRequest(input);
        console.log(JSON.stringify(result));
    } catch (error) {
        console.log(JSON.stringify({error: error.message}));
        process.exit(1);
    }
}

module.exports = PatternProcessor;