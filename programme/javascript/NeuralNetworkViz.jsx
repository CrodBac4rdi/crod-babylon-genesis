import React from 'react'
import { motion } from 'framer-motion'
import { Network, Brain, Activity, BarChart3 } from 'lucide-react'

const NeuralNetworkViz = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Neural Network Architecture</h2>
          <Network className="w-6 h-6 text-green-400" />
        </div>
        
        <div className="bg-gray-800 rounded-lg p-8 text-center">
          <Brain className="w-16 h-16 text-green-400 mx-auto mb-4" />
          <div className="text-lg font-semibold mb-2">Multi-Layer Neural Network</div>
          <div className="text-gray-400">
            JavaScript: 128-64-32 layers<br/>
            Python: 256-512-256-128 deep network<br/>
            Elixir: Native implementation with backprop
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-6">
          <button className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors">
            Start Training
          </button>
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
            Test Prediction
          </button>
        </div>
      </motion.div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-900 rounded-xl p-6 border border-gray-800"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Training Progress</h3>
            <Activity className="w-5 h-5 text-blue-400" />
          </div>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Loss</span>
                <span>0.0234</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div className="bg-gradient-to-r from-green-600 to-green-400 h-2 rounded-full" style={{ width: '85%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Accuracy</span>
                <span>94.2%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-600 to-blue-400 h-2 rounded-full" style={{ width: '94.2%' }} />
              </div>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-900 rounded-xl p-6 border border-gray-800"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Model Stats</h3>
            <BarChart3 className="w-5 h-5 text-purple-400" />
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Total Parameters</span>
              <span className="font-semibold">1.2M</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Training Epochs</span>
              <span className="font-semibold">150</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Batch Size</span>
              <span className="font-semibold">32</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Learning Rate</span>
              <span className="font-semibold">0.001</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default NeuralNetworkViz