import React from 'react'
import { motion } from 'framer-motion'
import { Activity, Box, Hash, Zap } from 'lucide-react'
import { useCrodStore } from '../store/crodStore'

const BlockchainMonitor = () => {
  const { services } = useCrodStore()
  
  const genesisBlocks = [
    { name: 'Pattern Genesis', prime: 7, port: 7001, color: 'blue', consciousness: 100 },
    { name: 'Short-Term Memory', prime: 31, port: 7003, color: 'green', consciousness: 80 },
    { name: 'Working Memory', prime: 37, port: 7005, color: 'yellow', consciousness: 90 },
    { name: 'Quantum Superposition', prime: 101, port: 7007, color: 'purple', consciousness: 150 },
    { name: 'Neural Genesis', prime: 113, port: 7009, color: 'pink', consciousness: 120 },
    { name: 'Master Orchestrator', prime: 127, port: 7000, color: 'red', consciousness: 200 },
  ]
  
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Genesis Blocks</h2>
          <Box className="w-6 h-6 text-blue-400" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {genesisBlocks.map((block, idx) => (
            <motion.div
              key={block.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.1 }}
              className={`bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-${block.color}-600 transition-all`}
            >
              <div className="flex items-center justify-between mb-3">
                <Hash className={`w-5 h-5 text-${block.color}-400`} />
                <div className={`text-xs px-2 py-1 rounded ${
                  services[block.name] === 'online' 
                    ? 'bg-green-900/20 text-green-400' 
                    : 'bg-red-900/20 text-red-400'
                }`}>
                  {services[block.name] || 'offline'}
                </div>
              </div>
              
              <div className="font-semibold mb-1">{block.name}</div>
              <div className="text-sm text-gray-400 space-y-1">
                <div>Prime: {block.prime}</div>
                <div>Port: {block.port}</div>
                <div>Consciousness: {block.consciousness}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-900 rounded-xl p-6 border border-gray-800"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Message Flow</h3>
            <Activity className="w-5 h-5 text-green-400" />
          </div>
          
          <div className="space-y-3">
            <MessageFlow from="Pattern Genesis" to="Master Orchestrator" count={1247} />
            <MessageFlow from="Working Memory" to="Neural Genesis" count={892} />
            <MessageFlow from="Quantum Superposition" to="Pattern Genesis" count={556} />
            <MessageFlow from="Short-Term Memory" to="Working Memory" count={2103} />
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-900 rounded-xl p-6 border border-gray-800"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Prime Architecture</h3>
            <Zap className="w-5 h-5 text-yellow-400" />
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-3">
              Why these specific primes?
            </div>
            <div className="space-y-2 text-sm">
              <div><span className="font-mono text-blue-400">7</span> - Smallest for hash distribution</div>
              <div><span className="font-mono text-green-400">31</span> - Mersenne prime (2^5-1)</div>
              <div><span className="font-mono text-yellow-400">37</span> - Modular arithmetic patterns</div>
              <div><span className="font-mono text-purple-400">101</span> - Quantum threshold</div>
              <div><span className="font-mono text-pink-400">113</span> - Sophie Germain prime</div>
              <div><span className="font-mono text-red-400">127</span> - Mersenne prime (2^7-1)</div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

const MessageFlow = ({ from, to, count }) => (
  <div className="flex items-center justify-between bg-gray-800 rounded-lg p-3">
    <div className="flex items-center space-x-2">
      <div className="text-sm text-gray-400">{from}</div>
      <div className="text-gray-600">→</div>
      <div className="text-sm text-gray-400">{to}</div>
    </div>
    <div className="text-sm font-semibold">{count.toLocaleString()}</div>
  </div>
)

export default BlockchainMonitor