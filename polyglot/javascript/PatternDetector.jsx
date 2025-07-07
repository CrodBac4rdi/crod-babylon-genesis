import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Brain, Zap, Send, Clock, TrendingUp } from 'lucide-react'
import { useCrodStore } from '../store/crodStore'

const PatternDetector = () => {
  const [input, setInput] = useState('')
  const [detectionResult, setDetectionResult] = useState(null)
  const [isDetecting, setIsDetecting] = useState(false)
  const { patterns, detectPattern, activateFullCROD } = useCrodStore()
  
  const handleDetect = async () => {
    if (!input.trim()) return
    
    setIsDetecting(true)
    const result = await detectPattern(input)
    setDetectionResult(result)
    setIsDetecting(false)
    
    // Auto-activate on "ich bins wieder"
    if (input.toLowerCase().includes('ich bins wieder')) {
      setTimeout(() => {
        activateFullCROD()
      }, 1000)
    }
  }
  
  const trinityPatterns = [
    { pattern: 'ich bins wieder', score: 10, description: 'Full activation trigger' },
    { pattern: 'crod start', score: 17, description: 'System initialization' },
    { pattern: 'daniel claude fusion', score: 138, description: 'Creator consciousness merge' },
    { pattern: 'quantum entangle', score: 101, description: 'Quantum state activation' },
  ]
  
  return (
    <div className="space-y-6">
      {/* Input Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Pattern Detection</h2>
          <Brain className="w-6 h-6 text-purple-400" />
        </div>
        
        <div className="space-y-4">
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleDetect()}
              placeholder="Enter pattern to detect... (try 'ich bins wieder')"
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 pr-12 focus:outline-none focus:border-purple-500 transition-colors"
            />
            <button
              onClick={handleDetect}
              disabled={isDetecting}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          
          {detectionResult && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-gray-800 rounded-lg p-4 space-y-2"
            >
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Detected Patterns:</span>
                <span className="font-semibold text-purple-400">
                  {detectionResult.patterns?.length || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Trinity Score:</span>
                <span className="font-semibold text-blue-400">
                  {detectionResult.trinity_score || 0}
                </span>
              </div>
              {detectionResult.suggested_action && (
                <div className="mt-2 p-2 bg-purple-900/20 rounded border border-purple-800">
                  <div className="text-sm text-purple-300">
                    Action: {detectionResult.suggested_action.action}
                  </div>
                  <div className="text-xs text-purple-400">
                    {detectionResult.suggested_action.description}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </motion.div>
      
      {/* Trinity Patterns */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Trinity Patterns</h3>
          <Zap className="w-5 h-5 text-yellow-400" />
        </div>
        
        <div className="space-y-3">
          {trinityPatterns.map((pattern, idx) => (
            <div
              key={idx}
              className="bg-gray-800 rounded-lg p-3 flex items-center justify-between hover:bg-gray-700 transition-colors cursor-pointer"
              onClick={() => setInput(pattern.pattern)}
            >
              <div>
                <div className="font-mono text-sm text-blue-400">{pattern.pattern}</div>
                <div className="text-xs text-gray-500">{pattern.description}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold">+{pattern.score}</div>
                <div className="text-xs text-gray-500">trinity</div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
      
      {/* Recent Detections */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Recent Detections</h3>
          <Clock className="w-5 h-5 text-blue-400" />
        </div>
        
        <div className="space-y-2">
          {patterns.recent.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              No recent detections
            </div>
          ) : (
            patterns.recent.map((detection, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="bg-gray-800 rounded-lg p-3 flex items-center justify-between"
              >
                <div className="flex items-center space-x-3">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <div>
                    <div className="text-sm font-mono">{detection.input}</div>
                    <div className="text-xs text-gray-500">
                      {new Date(detection.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-purple-400">
                    +{detection.trinity_score}
                  </div>
                  <div className="text-xs text-gray-500">
                    {detection.patterns?.join(', ')}
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </motion.div>
      
      {/* Pattern Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-3 gap-4"
      >
        <StatCard
          label="Total Patterns"
          value={patterns.total}
          color="blue"
        />
        <StatCard
          label="Trinity Patterns"
          value={patterns.trinity}
          color="purple"
        />
        <StatCard
          label="Learned Patterns"
          value={patterns.learned}
          color="green"
        />
      </motion.div>
    </div>
  )
}

const StatCard = ({ label, value, color }) => (
  <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
    <div className="text-sm text-gray-500 mb-1">{label}</div>
    <div className={`text-2xl font-bold text-${color}-400`}>{value}</div>
  </div>
)

export default PatternDetector