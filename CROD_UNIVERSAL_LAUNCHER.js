#!/usr/bin/env node
/**
 * CROD UNIVERSAL LAUNCHER
 * One launcher to rule them all!
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const EventEmitter = require('events');

class CRODUniversalLauncher extends EventEmitter {
  constructor() {
    super();
    this.services = new Map();
    this.config = {
      // Core Services
      blockchainServer: {
        name: 'Blockchain API',
        command: 'node',
        args: ['blockchain-server.js'],
        cwd: path.join(__dirname, 'src'),
        port: 3001,
        color: '\x1b[36m' // Cyan
      },
      
      neuralNetwork: {
        name: 'Neural Network',
        command: 'node',
        args: ['src/index.js', '--server'],
        cwd: __dirname,
        port: 6000,
        color: '\x1b[35m' // Magenta
      },
      
      // Frontend
      tauriApp: {
        name: 'CROD Chain App',
        command: 'npm',
        args: ['run', 'dev:web'],
        cwd: path.join(__dirname, 'crod-chain-app'),
        port: 5173,
        color: '\x1b[32m' // Green
      },
      
      // Python Services
      pythonVisualizer: {
        name: 'Python Visualizer',
        command: 'python3',
        args: ['crod_web_studio.py'],
        cwd: path.join(__dirname, 'bilder'),
        port: 5000,
        color: '\x1b[33m' // Yellow
      },
      
      // Elixir Blockchain (optional)
      elixirBlockchain: {
        name: 'Elixir Blockchain',
        command: 'mix',
        args: ['phx.server'],
        cwd: path.join(__dirname, 'src/blockchain/elixir'),
        port: 4000,
        enabled: false, // Disable by default
        color: '\x1b[95m' // Light Magenta
      }
    };
    
    this.runningServices = new Set();
  }

  async start() {
    console.clear();
    this.printBanner();
    
    // Check dependencies
    await this.checkDependencies();
    
    // Start all enabled services
    for (const [key, config] of Object.entries(this.config)) {
      if (config.enabled !== false) {
        await this.startService(key, config);
        await this.sleep(2000); // Give service time to start
      }
    }
    
    // Print status
    this.printStatus();
    
    // Handle shutdown
    process.on('SIGINT', () => this.shutdown());
    process.on('SIGTERM', () => this.shutdown());
  }
  
  printBanner() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗██████╗  ██████╗ ██████╗                           ║
║  ██╔════╝██╔══██╗██╔═══██╗██╔══██╗                          ║
║  ██║     ██████╔╝██║   ██║██║  ██║                          ║
║  ██║     ██╔══██╗██║   ██║██║  ██║                          ║
║  ╚██████╗██║  ██║╚██████╔╝██████╔╝                          ║
║   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝                           ║
║                                                               ║
║            UNIVERSAL SYSTEM LAUNCHER v1.0                     ║
║                                                               ║
║  Starting all components in unified mode...                   ║
╚═══════════════════════════════════════════════════════════════╝
    `);
  }
  
  async checkDependencies() {
    console.log('\n📋 Checking dependencies...\n');
    
    const checks = [
      { cmd: 'node --version', name: 'Node.js' },
      { cmd: 'npm --version', name: 'npm' },
      { cmd: 'python3 --version', name: 'Python 3' },
    ];
    
    for (const check of checks) {
      try {
        const result = await this.execCommand(check.cmd);
        console.log(`✅ ${check.name}: ${result.trim()}`);
      } catch {
        console.log(`❌ ${check.name}: NOT FOUND`);
      }
    }
    
    console.log('');
  }
  
  async startService(key, config) {
    console.log(`${config.color}🚀 Starting ${config.name}...\\x1b[0m`);
    
    const proc = spawn(config.command, config.args, {
      cwd: config.cwd,
      env: { ...process.env, PORT: config.port },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    
    // Handle output
    proc.stdout.on('data', (data) => {
      const lines = data.toString().split('\\n').filter(line => line.trim());
      lines.forEach(line => {
        console.log(`${config.color}[${config.name}]\\x1b[0m ${line}`);
      });
    });
    
    proc.stderr.on('data', (data) => {
      const lines = data.toString().split('\\n').filter(line => line.trim());
      lines.forEach(line => {
        if (!line.includes('warning')) {
          console.error(`${config.color}[${config.name}] ERROR:\\x1b[0m ${line}`);
        }
      });
    });
    
    proc.on('exit', (code) => {
      console.log(`${config.color}[${config.name}] Exited with code ${code}\\x1b[0m`);
      this.runningServices.delete(key);
    });
    
    this.services.set(key, proc);
    this.runningServices.add(key);
  }
  
  printStatus() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                    SYSTEM STATUS                              ║
╚═══════════════════════════════════════════════════════════════╝

🌐 Access Points:
`);
    
    for (const [key, config] of Object.entries(this.config)) {
      if (this.runningServices.has(key)) {
        console.log(`   ${config.color}■\\x1b[0m ${config.name}: http://localhost:${config.port}`);
      }
    }
    
    console.log(`
📊 Services Running: ${this.runningServices.size}/${Object.keys(this.config).length}

🛑 Press Ctrl+C to stop all services
    `);
  }
  
  async shutdown() {
    console.log('\\n\\n🛑 Shutting down all services...');
    
    for (const [key, proc] of this.services) {
      console.log(`   Stopping ${this.config[key].name}...`);
      proc.kill('SIGTERM');
    }
    
    // Give services time to shut down gracefully
    await this.sleep(2000);
    
    // Force kill if needed
    for (const [key, proc] of this.services) {
      if (!proc.killed) {
        proc.kill('SIGKILL');
      }
    }
    
    console.log('\\n✅ All services stopped. Goodbye!\\n');
    process.exit(0);
  }
  
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  execCommand(cmd) {
    return new Promise((resolve, reject) => {
      require('child_process').exec(cmd, (error, stdout) => {
        if (error) reject(error);
        else resolve(stdout);
      });
    });
  }
}

// Launch if called directly
if (require.main === module) {
  const launcher = new CRODUniversalLauncher();
  launcher.start().catch(console.error);
}

module.exports = CRODUniversalLauncher;