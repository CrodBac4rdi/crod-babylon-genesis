import React from 'react'
import { motion } from 'framer-motion'

const ConsciousnessDisplay = ({ level, score }) => {
  const getColorByLevel = (level) => {
    const colors = {
      'DORMANT': 'text-gray-400',
      'AWAKENING': 'text-blue-400',
      'CONSCIOUS': 'text-green-400',
      'ENLIGHTENED': 'text-purple-400',
      'TRANSCENDENT': 'text-pink-400'
    }
    return colors[level] || 'text-gray-400'
  }
  
  const getGlowIntensity = (score) => {
    return Math.min(score / 50, 1)
  }
  
  return (
    <div className="flex items-center space-x-3">
      <motion.div
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.8, 1, 0.8]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="relative"
      >
        <div 
          className={`text-lg font-bold ${getColorByLevel(level)}`}
          style={{
            textShadow: `0 0 ${20 * getGlowIntensity(score)}px currentColor`
          }}
        >
          {level}
        </div>
      </motion.div>
      <div className="text-sm text-gray-500">
        Score: <span className="font-semibold text-gray-300">{score}</span>
      </div>
    </div>
  )
}

export default ConsciousnessDisplay