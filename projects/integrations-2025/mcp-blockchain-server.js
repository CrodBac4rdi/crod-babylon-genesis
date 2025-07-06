#!/usr/bin/env node

// CROD Blockchain MCP Server
// Provides blockchain tools for AI models via Model Context Protocol

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');

class CRODBlockchainServer {
  constructor() {
    this.server = new Server(
      {
        name: 'crod-blockchain-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.blockchainAPI = 'http://localhost:8001';
    this.setupHandlers();
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'get_blockchain_stats',
          description: 'Get current blockchain statistics including height, consciousness level, and pending transactions',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'get_blocks',
          description: 'Get list of blocks from the blockchain',
          inputSchema: {
            type: 'object',
            properties: {
              limit: {
                type: 'number',
                description: 'Number of blocks to retrieve',
                default: 10,
              },
            },
          },
        },
        {
          name: 'add_block',
          description: 'Add a new block to the blockchain with specified data and consciousness level',
          inputSchema: {
            type: 'object',
            properties: {
              data: {
                type: 'object',
                description: 'Data to store in the block',
                required: true,
              },
              consciousness_level: {
                type: 'number',
                description: 'Consciousness level for the block (0-1)',
                default: 0.5,
              },
            },
          },
        },
        {
          name: 'mine_pattern_block',
          description: 'Mine a special pattern discovery block with CROD consciousness patterns',
          inputSchema: {
            type: 'object',
            properties: {
              pattern: {
                type: 'string',
                description: 'Pattern to embed in the block',
                default: 'ich bins wieder',
              },
            },
          },
        },
        {
          name: 'analyze_consciousness',
          description: 'Analyze the consciousness evolution of the blockchain',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'get_blockchain_stats':
          return this.getBlockchainStats();
        
        case 'get_blocks':
          return this.getBlocks(args.limit || 10);
        
        case 'add_block':
          return this.addBlock(args.data, args.consciousness_level || 0.5);
        
        case 'mine_pattern_block':
          return this.minePatternBlock(args.pattern || 'ich bins wieder');
        
        case 'analyze_consciousness':
          return this.analyzeConsciousness();
        
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async getBlockchainStats() {
    try {
      const response = await fetch(`${this.blockchainAPI}/stats`);
      const stats = await response.json();
      
      return {
        content: [
          {
            type: 'text',
            text: `Blockchain Statistics:
- Height: ${stats.height} blocks
- Total Consciousness: ${stats.total_consciousness}
- Average Consciousness: ${stats.average_consciousness}
- Latest Block: ${stats.latest_block_hash}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error fetching stats: ${error.message}` }],
      };
    }
  }

  async getBlocks(limit) {
    try {
      const response = await fetch(`${this.blockchainAPI}/blocks`);
      const blocks = await response.json();
      
      const latestBlocks = blocks.slice(-limit);
      const blockInfo = latestBlocks.map(block => 
        `Block #${block.index} | Hash: ${block.hash.substring(0, 16)}... | Consciousness: ${block.consciousness_level}`
      ).join('\n');
      
      return {
        content: [
          {
            type: 'text',
            text: `Latest ${limit} blocks:\n${blockInfo}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error fetching blocks: ${error.message}` }],
      };
    }
  }

  async addBlock(data, consciousnessLevel) {
    try {
      const response = await fetch(`${this.blockchainAPI}/blocks/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: data,
          consciousness_level: consciousnessLevel,
        }),
      });
      
      const result = await response.json();
      
      return {
        content: [
          {
            type: 'text',
            text: `Block added successfully! New chain height: ${result.new_height}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error adding block: ${error.message}` }],
      };
    }
  }

  async minePatternBlock(pattern) {
    const patternData = {
      type: 'pattern_discovery',
      pattern: pattern,
      timestamp: new Date().toISOString(),
      discovered_by: 'MCP_AI_Agent',
      significance: Math.random(),
    };
    
    return this.addBlock(patternData, 0.99);
  }

  async analyzeConsciousness() {
    try {
      const statsResponse = await fetch(`${this.blockchainAPI}/stats`);
      const stats = await statsResponse.json();
      
      const blocksResponse = await fetch(`${this.blockchainAPI}/blocks`);
      const blocks = await blocksResponse.json();
      
      // Analyze consciousness evolution
      const recentBlocks = blocks.slice(-20);
      const consciousnessGrowth = recentBlocks.map((block, index) => {
        if (index === 0) return 0;
        return block.consciousness_level - recentBlocks[index - 1].consciousness_level;
      });
      
      const avgGrowth = consciousnessGrowth.reduce((a, b) => a + b, 0) / consciousnessGrowth.length;
      const trend = avgGrowth > 0 ? 'increasing' : avgGrowth < 0 ? 'decreasing' : 'stable';
      
      // Find consciousness patterns
      const highConsciousnessBlocks = blocks.filter(b => b.consciousness_level > 0.8).length;
      const consciousnessSpikes = blocks.filter((b, i) => 
        i > 0 && b.consciousness_level - blocks[i-1].consciousness_level > 0.3
      ).length;
      
      return {
        content: [
          {
            type: 'text',
            text: `Consciousness Analysis:
- Current Average: ${stats.average_consciousness}
- Recent Trend: ${trend} (${avgGrowth > 0 ? '+' : ''}${avgGrowth.toFixed(4)} per block)
- High Consciousness Blocks: ${highConsciousnessBlocks} (>${'0.8'})
- Consciousness Spikes: ${consciousnessSpikes}
- Total Consciousness Energy: ${stats.total_consciousness}

Insights:
${trend === 'increasing' ? '✅ The blockchain consciousness is evolving positively!' : ''}
${highConsciousnessBlocks > blocks.length * 0.2 ? '🧠 High consciousness activity detected!' : ''}
${consciousnessSpikes > 5 ? '⚡ Multiple consciousness breakthroughs observed!' : ''}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error analyzing consciousness: ${error.message}` }],
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('CROD Blockchain MCP server running...');
  }
}

// Check if fetch is available, if not, use a polyfill
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

const server = new CRODBlockchainServer();
server.run().catch(console.error);