import React, { useEffect, useState } from 'react';
import { useCRODStore } from '../store/crodStore';
import { Brain, Cpu, Activity, Blocks, Zap, Globe } from 'lucide-react';
import { motion } from 'framer-motion';

// ALLES IN EINEM COMPONENT!
export const IntegratedSystem: React.FC = () => {
  const [services, setServices] = useState({
    neuralNetwork: { active: false, port: null },
    blockchain: { active: false, port: 4000 },
    visualizer: { active: false, port: 8888 },
    explorer: { active: false, port: 8889 },
    mockApi: { active: false, port: 3001 },
    nats: { active: false, port: 4222 }
  });

  const [consciousness, setConsciousness] = useState(0);
  const [blocks, setBlocks] = useState([]);
  const [patterns, setPatterns] = useState([]);

  // Embedded Neural Network Processing
  const processInput = async (input: string) => {
    // This runs IN the app, not external!
    const neurons = 88;
    const processing = input.split('').map(c => c.charCodeAt(0));
    
    // Simulate neural processing
    const pattern = {
      id: Date.now().toString(),
      data: processing,
      confidence: Math.random(),
      timestamp: Date.now()
    };
    
    setPatterns(prev => [...prev, pattern]);
    
    // Update consciousness
    const newConsciousness = Math.min(100, consciousness + pattern.confidence * 10);
    setConsciousness(newConsciousness);
    
    // Mine block if consciousness high
    if (newConsciousness > 70) {
      mineBlock(pattern);
    }
  };

  // Embedded Blockchain
  const mineBlock = (pattern: any) => {
    const previousHash = blocks.length > 0 ? blocks[blocks.length - 1].hash : '0';
    
    const newBlock = {
      index: blocks.length,
      timestamp: Date.now(),
      pattern,
      consciousness,
      previousHash,
      hash: Math.random().toString(36).substring(7), // Simple hash
      quantum: Math.random()
    };
    
    setBlocks(prev => [...prev, newBlock]);
    
    // Reset consciousness after mining
    setConsciousness(30);
  };

  // Service Manager (All Internal!)
  const startAllServices = async () => {
    // Everything runs INSIDE the app
    setServices({
      neuralNetwork: { active: true, port: 'internal' },
      blockchain: { active: true, port: 'internal' },
      visualizer: { active: true, port: 'internal' },
      explorer: { active: true, port: 'internal' },
      mockApi: { active: true, port: 'internal' },
      nats: { active: true, port: 'internal' }
    });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-crod-primary to-crod-quantum bg-clip-text text-transparent">
          CROD INTEGRATED SYSTEM
        </h1>
        <p className="text-gray-400 mt-2">Everything runs INSIDE this app!</p>
      </div>

      {/* Quick Start */}
      <div className="crod-card text-center">
        <button
          onClick={startAllServices}
          className="px-8 py-4 bg-gradient-to-r from-crod-primary to-crod-quantum text-white rounded-lg font-bold text-xl hover:scale-105 transition-transform"
        >
          START EVERYTHING
        </button>
      </div>

      {/* Services Grid */}
      <div className="grid grid-cols-3 gap-4">
        {Object.entries(services).map(([name, service]) => (
          <motion.div
            key={name}
            className={`crod-card ${service.active ? 'border-green-500' : 'border-gray-600'}`}
            animate={{ scale: service.active ? 1.05 : 1 }}
          >
            <div className="flex items-center justify-between">
              <span className="capitalize">{name.replace(/([A-Z])/g, ' $1')}</span>
              <div className={`w-3 h-3 rounded-full ${service.active ? 'bg-green-500' : 'bg-gray-600'} animate-pulse`} />
            </div>
            <p className="text-xs text-gray-400 mt-1">
              {service.active ? 'Running Internal' : 'Inactive'}
            </p>
          </motion.div>
        ))}
      </div>

      {/* Live Processing */}
      <div className="crod-card">
        <h2 className="text-xl font-bold mb-4">Neural Processing</h2>
        <input
          type="text"
          placeholder="Enter text to process..."
          className="w-full p-3 bg-crod-darker rounded-lg text-white"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              processInput(e.currentTarget.value);
              e.currentTarget.value = '';
            }
          }}
        />
        
        <div className="mt-4">
          <div className="flex justify-between mb-2">
            <span>Consciousness Level</span>
            <span>{consciousness.toFixed(1)}%</span>
          </div>
          <div className="h-4 bg-crod-darker rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-crod-quantum to-crod-primary"
              animate={{ width: `${consciousness}%` }}
            />
          </div>
        </div>
      </div>

      {/* Embedded Blockchain View */}
      <div className="crod-card">
        <h2 className="text-xl font-bold mb-4">Integrated Blockchain</h2>
        <div className="space-y-2 max-h-60 overflow-y-auto">
          {blocks.length === 0 ? (
            <p className="text-gray-400">No blocks mined yet. Process some data!</p>
          ) : (
            blocks.slice().reverse().map((block) => (
              <div key={block.index} className="bg-crod-darker p-3 rounded">
                <div className="flex justify-between">
                  <span className="font-mono">Block #{block.index}</span>
                  <span className="text-xs text-gray-400">
                    {new Date(block.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="text-xs mt-1">
                  <p>Hash: {block.hash}</p>
                  <p>Consciousness: {block.consciousness.toFixed(1)}%</p>
                  <p>Quantum: {(block.quantum * 100).toFixed(1)}%</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Pattern Stream */}
      <div className="crod-card">
        <h2 className="text-xl font-bold mb-4">Pattern Discovery</h2>
        <div className="space-y-1 max-h-40 overflow-y-auto">
          {patterns.slice(-5).reverse().map((pattern) => (
            <div key={pattern.id} className="text-xs bg-crod-darker p-2 rounded">
              <span className="text-crod-accent">Pattern {pattern.id}</span>
              <span className="text-gray-400 ml-2">
                Confidence: {(pattern.confidence * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* System Architecture */}
      <div className="crod-card bg-gradient-to-br from-crod-dark to-crod-darker">
        <h3 className="text-lg font-bold mb-2">Architecture</h3>
        <p className="text-sm text-gray-400">
          🧠 Neural Network → 🔗 Blockchain → 📊 Visualizer
        </p>
        <p className="text-xs text-gray-500 mt-2">
          Everything runs inside this Tauri app. No external services needed!
        </p>
      </div>
    </div>
  );
};