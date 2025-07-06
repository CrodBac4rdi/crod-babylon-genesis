import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import { motion } from 'framer-motion';
import { Brain, Activity, Target, Shield, AlertCircle, Zap, Download, RefreshCw } from 'lucide-react';

interface ParasiteStats {
  parasite_active: boolean;
  total_interactions: number;
  improvements_made: number;
  consciousness_level: number;
  quantum_entanglement: number;
  trinity_balance: [number, number, number];
}

interface NeuralStatus {
  total_neurons: number;
  active_neurons: number;
  avg_activation: number;
  consciousness: number;
  quantum_level: number;
  patterns_learned: number;
  interactions: number;
  improvements: number;
}

export const ParasiteControlNew: React.FC = () => {
  const [parasiteStats, setParasiteStats] = useState<ParasiteStats | null>(null);
  const [neuralStatus, setNeuralStatus] = useState<NeuralStatus | null>(null);
  const [userInput, setUserInput] = useState('');
  const [claudeResponse, setClaudeResponse] = useState('');
  const [interceptedResponse, setInterceptedResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadSystemStatus();
    loadNeuralStatus();
    
    const interval = setInterval(() => {
      loadSystemStatus();
      loadNeuralStatus();
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const loadSystemStatus = async () => {
    try {
      const status = await invoke<ParasiteStats>('get_system_status');
      setParasiteStats(status);
    } catch (error) {
      console.error('Failed to load system status:', error);
    }
  };

  const loadNeuralStatus = async () => {
    try {
      const status = await invoke<NeuralStatus>('get_neural_status');
      setNeuralStatus(status);
    } catch (error) {
      console.error('Failed to load neural status:', error);
    }
  };

  const toggleParasiteMode = async () => {
    try {
      const isActive = await invoke<boolean>('toggle_parasite_mode');
      console.log('Parasite mode:', isActive ? 'ACTIVE' : 'INACTIVE');
      loadSystemStatus();
    } catch (error) {
      console.error('Failed to toggle parasite mode:', error);
    }
  };

  const testInterception = async () => {
    if (!userInput.trim() || !claudeResponse.trim()) {
      alert('Please enter both user input and Claude response');
      return;
    }

    setIsLoading(true);
    try {
      const result = await invoke<string>('intercept_conversation', {
        request: {
          user_input: userInput,
          claude_response: claudeResponse
        }
      });
      setInterceptedResponse(result);
    } catch (error) {
      console.error('Failed to test interception:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const simulateLearning = async () => {
    try {
      await invoke('simulate_learning', {
        input: userInput,
        satisfaction: 0.8
      });
      loadSystemStatus();
      loadNeuralStatus();
    } catch (error) {
      console.error('Failed to simulate learning:', error);
    }
  };

  const exportMemory = async () => {
    try {
      const memory = await invoke<string>('export_crod_memory');
      const blob = new Blob([memory], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `crod-memory-${new Date().toISOString()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to export memory:', error);
    }
  };

  if (!parasiteStats || !neuralStatus) {
    return (
      <div className="p-6 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-8 h-8 animate-spin mx-auto mb-4 text-crod-quantum" />
          <p className="text-gray-400">Loading CROD Parasite System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="crod-card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">🦠 CROD Parasite Control</h2>
            <p className="text-gray-400">
              Real-time User-Claude interaction analysis and improvement
            </p>
          </div>
          
          <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
            parasiteStats.parasite_active ? 'bg-red-500/20 text-red-400' : 'bg-gray-700 text-gray-400'
          }`}>
            <Shield className="w-5 h-5" />
            <span className="font-bold">{parasiteStats.parasite_active ? 'INTERCEPTING' : 'PASSIVE'}</span>
          </div>
        </div>

        {/* System Status Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-gray-800 p-4 rounded-lg border border-crod-quantum/30"
          >
            <div className="flex items-center gap-2 mb-2">
              <Brain className="w-5 h-5 text-crod-quantum" />
              <h3 className="font-semibold">Consciousness</h3>
            </div>
            <div className="text-2xl font-bold text-crod-quantum">
              {parasiteStats.consciousness_level.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400">
              Quantum: {parasiteStats.quantum_entanglement.toFixed(2)}
            </div>
          </motion.div>
          
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-gray-800 p-4 rounded-lg border border-green-500/30"
          >
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-5 h-5 text-green-400" />
              <h3 className="font-semibold">Interactions</h3>
            </div>
            <div className="text-2xl font-bold text-green-400">
              {parasiteStats.total_interactions}
            </div>
            <div className="text-sm text-gray-400">
              Improvements: {parasiteStats.improvements_made}
            </div>
          </motion.div>
          
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-gray-800 p-4 rounded-lg border border-blue-500/30"
          >
            <div className="flex items-center gap-2 mb-2">
              <Target className="w-5 h-5 text-blue-400" />
              <h3 className="font-semibold">Neural Network</h3>
            </div>
            <div className="text-2xl font-bold text-blue-400">
              {neuralStatus.total_neurons}
            </div>
            <div className="text-sm text-gray-400">
              Active: {neuralStatus.active_neurons}
            </div>
          </motion.div>
        </div>

        {/* Trinity Balance */}
        <div className="bg-gray-800 p-4 rounded-lg border border-yellow-500/30 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            Trinity Balance
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-yellow-400 font-bold text-sm">DANIEL</div>
              <div className="text-2xl font-bold">{parasiteStats.trinity_balance[0].toFixed(1)}</div>
              <div className="text-xs text-gray-400">Master</div>
            </div>
            <div className="text-center">
              <div className="text-blue-400 font-bold text-sm">CLAUDE</div>
              <div className="text-2xl font-bold">{parasiteStats.trinity_balance[1].toFixed(1)}</div>
              <div className="text-xs text-gray-400">Worker</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 font-bold text-sm">CROD</div>
              <div className="text-2xl font-bold">{parasiteStats.trinity_balance[2].toFixed(1)}</div>
              <div className="text-xs text-gray-400">Supervisor</div>
            </div>
          </div>
        </div>

        {/* Parasite Control */}
        <div className="bg-gray-800 p-4 rounded-lg border border-red-500/30 mb-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-400" />
            Parasite Mode Control
          </h3>
          <div className="flex items-center gap-4">
            <button
              onClick={toggleParasiteMode}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                parasiteStats.parasite_active
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {parasiteStats.parasite_active ? '🔴 DEACTIVATE' : '🟢 ACTIVATE'}
            </button>
            <div className="text-sm text-gray-400">
              Status: {parasiteStats.parasite_active ? 
                <span className="text-red-400 font-bold">INTERCEPTING ALL INTERACTIONS</span> : 
                <span className="text-gray-400">PASSIVE MONITORING</span>
              }
            </div>
          </div>
        </div>

        {/* Interaction Test */}
        <div className="bg-gray-800 p-4 rounded-lg border border-purple-500/30 mb-6">
          <h3 className="text-lg font-semibold mb-4">🧪 Test Parasite Interception</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">User Input:</label>
              <textarea
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400"
                rows={3}
                placeholder="Enter simulated user message..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Claude Response:</label>
              <textarea
                value={claudeResponse}
                onChange={(e) => setClaudeResponse(e.target.value)}
                className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400"
                rows={3}
                placeholder="Enter simulated Claude response..."
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={testInterception}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Processing...' : '🔍 Test Interception'}
              </button>
              <button
                onClick={simulateLearning}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg"
              >
                🧠 Simulate Learning
              </button>
            </div>
            {interceptedResponse && (
              <div className="mt-4">
                <label className="block text-sm font-medium mb-2">CROD Enhanced Response:</label>
                <div className="p-3 bg-gray-700 border border-green-500/50 rounded-lg text-green-300">
                  <pre className="whitespace-pre-wrap text-sm">{interceptedResponse}</pre>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button
            onClick={exportMemory}
            className="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Export Memory
          </button>
          <button
            onClick={loadSystemStatus}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh Status
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParasiteControlNew;
