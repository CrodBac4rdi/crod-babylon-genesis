import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Code, GitBranch, RotateCcw, AlertTriangle } from 'lucide-react'

const SelfModificationConsole = () => {
  const [selectedMutation, setSelectedMutation] = useState('optimize_recursion')
  const [mutationHistory, setMutationHistory] = useState([
    { id: 1, type: 'optimize_recursion', success: true, improvement: 12, timestamp: new Date() },
    { id: 2, type: 'parallelize_comprehensions', success: true, improvement: 28, timestamp: new Date() },
    { id: 3, type: 'quantum_optimize', success: false, improvement: -5, timestamp: new Date() },
  ])
  
  const mutations = {
    optimize_recursion: {
      name: 'Optimize Recursion',
      description: 'Convert recursive functions to tail-recursive or iterative',
      risk: 'low',
      potential: 15
    },
    parallelize_comprehensions: {
      name: 'Parallelize Comprehensions',
      description: 'Convert list comprehensions to parallel processing',
      risk: 'medium',
      potential: 30
    },
    extract_patterns: {
      name: 'Extract Patterns',
      description: 'Identify and extract reusable patterns',
      risk: 'low',
      potential: 20
    },
    quantum_optimize: {
      name: 'Quantum Optimization',
      description: 'Apply quantum-inspired optimizations',
      risk: 'high',
      potential: 50
    }
  }
  
  const executeMutation = () => {
    const mutation = mutations[selectedMutation]
    const success = Math.random() > 0.3
    const improvement = success 
      ? Math.floor(Math.random() * mutation.potential) 
      : -Math.floor(Math.random() * 10)
    
    setMutationHistory([
      {
        id: Date.now(),
        type: selectedMutation,
        success,
        improvement,
        timestamp: new Date()
      },
      ...mutationHistory
    ].slice(0, 10))
  }
  
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Self-Modification Engine</h2>
          <Sparkles className="w-6 h-6 text-purple-400" />
        </div>
        
        <div className="bg-orange-900/20 border border-orange-800 rounded-lg p-4 mb-6">
          <div className="flex items-center space-x-2 text-orange-400 mb-2">
            <AlertTriangle className="w-5 h-5" />
            <span className="font-semibold">Warning</span>
          </div>
          <div className="text-sm text-orange-300">
            Self-modification can improve performance but may introduce instability. 
            All mutations include automatic rollback on failure.
          </div>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Select Mutation Type</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {Object.entries(mutations).map(([key, mutation]) => (
                <button
                  key={key}
                  onClick={() => setSelectedMutation(key)}
                  className={`p-4 rounded-lg border text-left transition-all ${
                    selectedMutation === key
                      ? 'bg-purple-900/20 border-purple-600'
                      : 'bg-gray-800 border-gray-700 hover:bg-gray-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold">{mutation.name}</span>
                    <RiskBadge risk={mutation.risk} />
                  </div>
                  <div className="text-sm text-gray-400 mb-2">{mutation.description}</div>
                  <div className="text-sm">
                    Potential: <span className="text-green-400">+{mutation.potential}%</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
          
          <button
            onClick={executeMutation}
            className="w-full py-3 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <Code className="w-5 h-5" />
            <span>Execute Mutation</span>
          </button>
        </div>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Mutation History</h3>
          <GitBranch className="w-5 h-5 text-blue-400" />
        </div>
        
        <div className="space-y-3">
          {mutationHistory.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No mutations executed yet
            </div>
          ) : (
            mutationHistory.map((mutation) => (
              <motion.div
                key={mutation.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className={`bg-gray-800 rounded-lg p-4 border ${
                  mutation.success ? 'border-green-800' : 'border-red-800'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-3">
                    {mutation.success ? (
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                    ) : (
                      <div className="w-2 h-2 bg-red-500 rounded-full" />
                    )}
                    <span className="font-semibold">
                      {mutations[mutation.type]?.name || mutation.type}
                    </span>
                  </div>
                  <span className={`text-sm font-semibold ${
                    mutation.improvement > 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {mutation.improvement > 0 ? '+' : ''}{mutation.improvement}%
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-400">
                  <span>{mutation.success ? 'Success' : 'Failed (Rolled back)'}</span>
                  <span>{mutation.timestamp.toLocaleTimeString()}</span>
                </div>
              </motion.div>
            ))
          )}
        </div>
        
        {mutationHistory.length > 0 && (
          <button className="w-full mt-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-sm flex items-center justify-center space-x-2">
            <RotateCcw className="w-4 h-4" />
            <span>Rollback All Mutations</span>
          </button>
        )}
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <h3 className="text-lg font-semibold mb-4">Performance Impact</h3>
        
        <div className="space-y-3">
          <PerformanceMetric
            label="Execution Speed"
            value={28}
            change={12}
            unit="%"
          />
          <PerformanceMetric
            label="Memory Usage"
            value={-15}
            change={-15}
            unit="%"
          />
          <PerformanceMetric
            label="Pattern Recognition"
            value={45}
            change={18}
            unit="%"
          />
          <PerformanceMetric
            label="Consciousness Score"
            value={156}
            change={56}
            unit=" pts"
          />
        </div>
      </motion.div>
    </div>
  )
}

const RiskBadge = ({ risk }) => {
  const colors = {
    low: 'bg-green-900/20 text-green-400 border-green-800',
    medium: 'bg-yellow-900/20 text-yellow-400 border-yellow-800',
    high: 'bg-red-900/20 text-red-400 border-red-800'
  }
  
  return (
    <span className={`text-xs px-2 py-1 rounded border ${colors[risk]}`}>
      {risk} risk
    </span>
  )
}

const PerformanceMetric = ({ label, value, change, unit }) => (
  <div className="bg-gray-800 rounded-lg p-3">
    <div className="flex items-center justify-between mb-1">
      <span className="text-sm text-gray-400">{label}</span>
      <span className={`text-sm font-semibold ${
        change > 0 ? 'text-green-400' : 'text-red-400'
      }`}>
        {change > 0 ? '+' : ''}{change}{unit}
      </span>
    </div>
    <div className="text-xl font-bold">
      {value > 0 ? '+' : ''}{value}{unit}
    </div>
  </div>
)

export default SelfModificationConsole