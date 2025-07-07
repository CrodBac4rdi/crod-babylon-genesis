import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { GitBranch, Play, RotateCcw, TrendingUp, Users } from 'lucide-react'
import { useCrodStore } from '../store/crodStore'

const GameTheoryLab = () => {
  const [selectedGame, setSelectedGame] = useState('prisoners_dilemma')
  const [strategy1, setStrategy1] = useState('cooperate')
  const [strategy2, setStrategy2] = useState('cooperate')
  const [gameResult, setGameResult] = useState(null)
  const [simulating, setSimulating] = useState(false)
  const { createGame, findEquilibrium } = useCrodStore()
  
  const games = {
    prisoners_dilemma: {
      name: "Prisoner's Dilemma",
      description: "Classic game theory problem",
      strategies: ['cooperate', 'defect'],
      payoffMatrix: {
        'cooperate,cooperate': [3, 3],
        'cooperate,defect': [0, 5],
        'defect,cooperate': [5, 0],
        'defect,defect': [1, 1]
      }
    },
    coordination: {
      name: "Coordination Game",
      description: "Players win by choosing the same",
      strategies: ['left', 'center', 'right'],
      payoffMatrix: {
        'same': [10, 10],
        'different': [-1, -1]
      }
    },
    quantum: {
      name: "Quantum Game",
      description: "Superposition and entanglement",
      strategies: ['collapse', 'superpose', 'entangle'],
      payoffMatrix: {
        'entangle,entangle': [10, 10],
        'superpose,superpose': [3, 3],
        'collapse,collapse': [2, 2]
      }
    }
  }
  
  const playGame = () => {
    const game = games[selectedGame]
    const key = `${strategy1},${strategy2}`
    const payoff = game.payoffMatrix[key] || game.payoffMatrix['different'] || [0, 0]
    
    setGameResult({
      player1: { strategy: strategy1, payoff: payoff[0] },
      player2: { strategy: strategy2, payoff: payoff[1] },
      outcome: analyzeOutcome(strategy1, strategy2, selectedGame)
    })
  }
  
  const analyzeOutcome = (s1, s2, gameType) => {
    if (gameType === 'prisoners_dilemma') {
      if (s1 === 'cooperate' && s2 === 'cooperate') return 'Mutual cooperation - Good outcome!'
      if (s1 === 'defect' && s2 === 'defect') return 'Mutual defection - Nash equilibrium'
      if (s1 === 'cooperate' && s2 === 'defect') return 'Player 2 exploited Player 1'
      if (s1 === 'defect' && s2 === 'cooperate') return 'Player 1 exploited Player 2'
    }
    if (gameType === 'coordination') {
      if (s1 === s2) return 'Perfect coordination achieved!'
      return 'Failed to coordinate'
    }
    if (gameType === 'quantum') {
      if (s1 === 'entangle' && s2 === 'entangle') return 'Quantum advantage unlocked!'
      return 'Classical outcome'
    }
    return 'Game completed'
  }
  
  const runSimulation = async () => {
    setSimulating(true)
    // Simulate multiple rounds
    setTimeout(() => {
      setSimulating(false)
      // Show simulation results
    }, 2000)
  }
  
  return (
    <div className="space-y-6">
      {/* Game Selection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Game Theory Laboratory</h2>
          <GitBranch className="w-6 h-6 text-blue-400" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {Object.entries(games).map(([key, game]) => (
            <button
              key={key}
              onClick={() => setSelectedGame(key)}
              className={`p-4 rounded-lg border transition-all ${
                selectedGame === key
                  ? 'bg-blue-900/20 border-blue-600 shadow-lg shadow-blue-600/20'
                  : 'bg-gray-800 border-gray-700 hover:bg-gray-700'
              }`}
            >
              <div className="font-semibold mb-1">{game.name}</div>
              <div className="text-sm text-gray-400">{game.description}</div>
            </button>
          ))}
        </div>
        
        {/* Strategy Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Player 1 Strategy</label>
            <select
              value={strategy1}
              onChange={(e) => setStrategy1(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
            >
              {games[selectedGame].strategies.map(strategy => (
                <option key={strategy} value={strategy}>
                  {strategy.charAt(0).toUpperCase() + strategy.slice(1)}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Player 2 Strategy</label>
            <select
              value={strategy2}
              onChange={(e) => setStrategy2(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
            >
              {games[selectedGame].strategies.map(strategy => (
                <option key={strategy} value={strategy}>
                  {strategy.charAt(0).toUpperCase() + strategy.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="flex space-x-4 mt-6">
          <button
            onClick={playGame}
            className="flex items-center space-x-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            <Play className="w-4 h-4" />
            <span>Play Game</span>
          </button>
          
          <button
            onClick={runSimulation}
            disabled={simulating}
            className="flex items-center space-x-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors disabled:opacity-50"
          >
            <RotateCcw className={`w-4 h-4 ${simulating ? 'animate-spin' : ''}`} />
            <span>{simulating ? 'Simulating...' : 'Run 100 Rounds'}</span>
          </button>
        </div>
      </motion.div>
      
      {/* Game Result */}
      {gameResult && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-gray-900 rounded-xl p-6 border border-gray-800"
        >
          <h3 className="text-lg font-semibold mb-4">Game Result</h3>
          
          <div className="grid grid-cols-2 gap-6 mb-4">
            <PlayerResult
              player="Player 1"
              strategy={gameResult.player1.strategy}
              payoff={gameResult.player1.payoff}
              color="blue"
            />
            <PlayerResult
              player="Player 2"
              strategy={gameResult.player2.strategy}
              payoff={gameResult.player2.payoff}
              color="purple"
            />
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Outcome</div>
            <div className="font-semibold">{gameResult.outcome}</div>
          </div>
        </motion.div>
      )}
      
      {/* Payoff Matrix */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Payoff Matrix</h3>
          <TrendingUp className="w-5 h-5 text-green-400" />
        </div>
        
        <PayoffMatrix game={games[selectedGame]} />
      </motion.div>
      
      {/* Nash Equilibrium */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Nash Equilibrium Analysis</h3>
          <Users className="w-5 h-5 text-yellow-400" />
        </div>
        
        <div className="space-y-3">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Pure Strategy Nash Equilibria</div>
            {selectedGame === 'prisoners_dilemma' && (
              <div className="font-mono text-sm">
                (Defect, Defect) - Both players defect
              </div>
            )}
            {selectedGame === 'coordination' && (
              <div className="font-mono text-sm">
                (Left, Left), (Center, Center), (Right, Right)
              </div>
            )}
            {selectedGame === 'quantum' && (
              <div className="font-mono text-sm">
                (Entangle, Entangle) - Quantum Nash equilibrium
              </div>
            )}
          </div>
          
          <button className="w-full py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-sm">
            Calculate Mixed Strategy Equilibrium
          </button>
        </div>
      </motion.div>
    </div>
  )
}

const PlayerResult = ({ player, strategy, payoff, color }) => (
  <div className={`bg-gray-800 rounded-lg p-4 border border-${color}-600/50`}>
    <div className="text-sm text-gray-400 mb-1">{player}</div>
    <div className="font-semibold mb-2 capitalize">{strategy}</div>
    <div className={`text-2xl font-bold text-${color}-400`}>+{payoff}</div>
  </div>
)

const PayoffMatrix = ({ game }) => {
  if (game.name === "Prisoner's Dilemma") {
    return (
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="p-2"></th>
              <th className="p-2 text-blue-400">Cooperate</th>
              <th className="p-2 text-blue-400">Defect</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="p-2 font-semibold text-purple-400">Cooperate</td>
              <td className="p-2 bg-gray-800 text-center">3, 3</td>
              <td className="p-2 bg-gray-800 text-center">0, 5</td>
            </tr>
            <tr>
              <td className="p-2 font-semibold text-purple-400">Defect</td>
              <td className="p-2 bg-gray-800 text-center">5, 0</td>
              <td className="p-2 bg-gray-800 text-center">1, 1</td>
            </tr>
          </tbody>
        </table>
      </div>
    )
  }
  
  return (
    <div className="text-center text-gray-500">
      Payoff matrix visualization for {game.name}
    </div>
  )
}

export default GameTheoryLab