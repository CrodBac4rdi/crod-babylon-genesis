// 3D GRID PROTOCOL - Spatial Chain Organization
// Each chain has 6 neighbors (like cube faces) + 2-hop visibility

const EventEmitter = require('events');

class Chain3DRoom {
    constructor(chainId, prime, position = { x: 0, y: 0, z: 0 }) {
        this.id = chainId;
        this.prime = prime;
        this.position = position;
        
        // 6 direct neighbors (cube faces)
        this.neighbors = {
            up: null,    // +Z (floor above)
            down: null,  // -Z (floor below)
            north: null, // +Y
            south: null, // -Y
            east: null,  // +X
            west: null   // -X
        };
        
        // 2-HOP VISIBILITY: Know neighbors of neighbors!
        this.neighborNetwork = new Map();
        
        // Gang connections (max 4 active)
        this.gangConnections = new Set();
        this.maxGangSize = 4;
    }
    
    setNeighbor(direction, chainRoom) {
        if (this.neighbors.hasOwnProperty(direction)) {
            this.neighbors[direction] = chainRoom;
            
            // Reciprocal connection
            const opposite = this.getOppositeDirection(direction);
            if (chainRoom && opposite) {
                chainRoom.neighbors[opposite] = this;
            }
        }
    }
    
    getOppositeDirection(direction) {
        const opposites = {
            up: 'down', down: 'up',
            north: 'south', south: 'north',
            east: 'west', west: 'east'
        };
        return opposites[direction];
    }
    
    async updateNeighborNetwork(chainRegistry) {
        // Clear old network
        this.neighborNetwork.clear();
        
        // Query each neighbor for their connections
        for (const [direction, neighborId] of Object.entries(this.neighbors)) {
            if (neighborId) {
                const neighbor = chainRegistry.get(neighborId);
                if (neighbor) {
                    // Store their connections
                    const theirNeighbors = {};
                    for (const [dir, id] of Object.entries(neighbor.neighbors)) {
                        if (id) theirNeighbors[dir] = id;
                    }
                    this.neighborNetwork.set(neighborId, theirNeighbors);
                }
            }
        }
    }
    
    canReachIn2Hops(targetId) {
        // Direct neighbor?
        if (Object.values(this.neighbors).includes(targetId)) {
            return { reachable: true, hops: 1, via: null };
        }
        
        // 2-hop reachable?
        for (const [neighborId, theirConnections] of this.neighborNetwork) {
            if (Object.values(theirConnections).includes(targetId)) {
                return { reachable: true, hops: 2, via: neighborId };
            }
        }
        
        return { reachable: false, hops: -1, via: null };
    }
    
    addGangConnection(chainId) {
        if (this.gangConnections.size < this.maxGangSize) {
            this.gangConnections.add(chainId);
            return true;
        }
        return false;
    }
    
    removeGangConnection(chainId) {
        return this.gangConnections.delete(chainId);
    }
}

class Grid3DProtocol extends EventEmitter {
    constructor() {
        super();
        this.chains = new Map();
        this.grid = new Map(); // position -> chainId
        
        // Grid layers (Z-axis)
        this.layers = {
            0: 'MEMORY_LAYER',      // Short-term, Working, Long-term
            1: 'PROCESSING_LAYER',  // Pattern, Validation, Doubt, Quantum
            2: 'INTERFACE_LAYER'    // Tool, Agent, Chat, Code
        };
        
        // Pre-defined positions for chains
        this.chainPositions = {
            // MEMORY LAYER (Z=0)
            'SHORT_TERM_MEMORY': { x: 0, y: 0, z: 0 },
            'WORKING_MEMORY': { x: 1, y: 0, z: 0 },
            'LONG_TERM_MEMORY': { x: 2, y: 0, z: 0 },
            'MEMORY_ADVANCED': { x: 0, y: 1, z: 0 },
            
            // PROCESSING LAYER (Z=1)
            'PATTERN_GENESIS': { x: 0, y: 0, z: 1 },
            'VALIDATION_GENESIS': { x: 1, y: 0, z: 1 },
            'SELF_DOUBT_GENESIS': { x: 2, y: 0, z: 1 },
            'QUANTUM_SUPERPOSITION': { x: 0, y: 1, z: 1 },
            'NEURAL_GENESIS': { x: 1, y: 1, z: 1 },
            
            // INTERFACE LAYER (Z=2)
            'TOOL_GENESIS': { x: 0, y: 0, z: 2 },
            'AGENT_GENESIS': { x: 1, y: 0, z: 2 },
            'CHAT_GENESIS': { x: 2, y: 0, z: 2 },
            'CODE_GENESIS': { x: 0, y: 1, z: 2 },
            'MULTI_MODAL_GENESIS': { x: 1, y: 1, z: 2 },
            'DIRECTOR_GENESIS': { x: 2, y: 1, z: 2 }
        };
    }
    
    addChain(chainType, chainId, prime) {
        const position = this.chainPositions[chainType];
        if (!position) {
            console.log(`⚠️ No position defined for ${chainType}`);
            return null;
        }
        
        const room = new Chain3DRoom(chainId, prime, position);
        this.chains.set(chainId, room);
        
        // Store in grid
        const posKey = `${position.x},${position.y},${position.z}`;
        this.grid.set(posKey, chainId);
        
        // Auto-connect neighbors
        this.connectNeighbors(room);
        
        console.log(`📍 Placed ${chainType} at (${position.x},${position.y},${position.z})`);
        
        return room;
    }
    
    connectNeighbors(room) {
        const { x, y, z } = room.position;
        
        // Check all 6 directions
        const directions = [
            { dir: 'east', pos: { x: x+1, y, z } },
            { dir: 'west', pos: { x: x-1, y, z } },
            { dir: 'north', pos: { x, y: y+1, z } },
            { dir: 'south', pos: { x, y: y-1, z } },
            { dir: 'up', pos: { x, y, z: z+1 } },
            { dir: 'down', pos: { x, y, z: z-1 } }
        ];
        
        for (const { dir, pos } of directions) {
            const neighborKey = `${pos.x},${pos.y},${pos.z}`;
            const neighborId = this.grid.get(neighborKey);
            
            if (neighborId) {
                const neighbor = this.chains.get(neighborId);
                if (neighbor) {
                    room.setNeighbor(dir, neighborId);
                    console.log(`🔗 Connected ${room.id} ${dir} to ${neighborId}`);
                }
            }
        }
    }
    
    async updateAllNeighborNetworks() {
        for (const chain of this.chains.values()) {
            await chain.updateNeighborNetwork(this.chains);
        }
        console.log('🌐 Updated 2-hop visibility for all chains');
    }
    
    findPath(fromId, toId) {
        const from = this.chains.get(fromId);
        const to = this.chains.get(toId);
        
        if (!from || !to) return null;
        
        // Check 2-hop reachability
        const reach = from.canReachIn2Hops(toId);
        
        if (reach.reachable) {
            return {
                path: reach.hops === 1 
                    ? [fromId, toId] 
                    : [fromId, reach.via, toId],
                hops: reach.hops
            };
        }
        
        // Otherwise, route up (to higher Z layer)
        const upNeighbor = from.neighbors.up;
        if (upNeighbor) {
            return {
                path: [fromId, upNeighbor, '...', toId],
                hops: -1, // Unknown
                note: 'Escalated to upper layer'
            };
        }
        
        return null;
    }
    
    getLayerChains(z) {
        const layerChains = [];
        
        for (const [chainId, room] of this.chains) {
            if (room.position.z === z) {
                layerChains.push({
                    id: chainId,
                    position: room.position,
                    neighbors: Object.entries(room.neighbors)
                        .filter(([_, id]) => id !== null)
                        .map(([dir, id]) => ({ direction: dir, chainId: id }))
                });
            }
        }
        
        return layerChains;
    }
    
    visualizeGrid() {
        console.log('\n🏢 CROD BABYLON 3D GRID:\n');
        
        for (let z = 2; z >= 0; z--) {
            console.log(`FLOOR ${z} (${this.layers[z]}):`);
            console.log('┌─────────┬─────────┬─────────┐');
            
            for (let y = 0; y <= 1; y++) {
                let row = '│';
                for (let x = 0; x <= 2; x++) {
                    const chainId = this.grid.get(`${x},${y},${z}`);
                    const chain = chainId ? this.chains.get(chainId) : null;
                    const name = chain ? chainId.substring(0, 7) : '[empty]';
                    row += ` ${name.padEnd(7)} │`;
                }
                console.log(row);
                if (y === 0) console.log('├─────────┼─────────┼─────────┤');
            }
            
            console.log('└─────────┴─────────┴─────────┘\n');
        }
    }
}

// Export for use
module.exports = { Chain3DRoom, Grid3DProtocol };

// Test if run directly
if (require.main === module) {
    const grid = new Grid3DProtocol();
    
    // Add some test chains
    grid.addChain('PATTERN_GENESIS', 'pattern', 7);
    grid.addChain('SHORT_TERM_MEMORY', 'short', 31);
    grid.addChain('WORKING_MEMORY', 'working', 37);
    grid.addChain('VALIDATION_GENESIS', 'valid', 13);
    
    // Update networks
    grid.updateAllNeighborNetworks();
    
    // Visualize
    grid.visualizeGrid();
    
    // Test pathfinding
    const path = grid.findPath('short', 'working');
    console.log('Path from short to working:', path);
}