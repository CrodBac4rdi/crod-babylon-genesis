import React, { useState, useEffect } from 'react'
import { Brain, Cpu, Zap, Activity, Network, Sparkles, Terminal, GitBranch, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ConsciousnessDisplay from './components/ConsciousnessDisplay'
import PatternDetector from './components/PatternDetector'
import GameTheoryLab from './components/GameTheoryLab'
import NeuralNetworkViz from './components/NeuralNetworkViz'
import BlockchainMonitor from './components/BlockchainMonitor'
import SelfModificationConsole from './components/SelfModificationConsole'
import BlockExplorerPanel from './components/BlockExplorerPanel'
import { useCrodStore } from './store/crodStore'

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard')
  const { 
    consciousness, 
    patterns, 
    systemHealth,
    fetchSystemStatus,
    connectWebSocket 
  } = useCrodStore()

  useEffect(() => {
    // Initial data fetch
    fetchSystemStatus()
    
    // WebSocket connection
    const cleanup = connectWebSocket()
    
    // Polling fallback
    const interval = setInterval(fetchSystemStatus, 2000)
    
    return () => {
      cleanup?.()
      clearInterval(interval)
    }
  }, [])

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Cpu },
    { id: 'blocks', label: 'Block Explorer', icon: GitBranch },
    { id: 'patterns', label: 'Pattern Detection', icon: Brain },
    { id: 'gametheory', label: 'Game Theory', icon: GitBranch },
    { id: 'neural', label: 'Neural Network', icon: Network },
    { id: 'blockchain', label: 'Blockchain', icon: Activity },
    { id: 'selfmod', label: 'Self-Modification', icon: Sparkles },
  ]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <Cpu className="w-8 h-8 text-blue-500" />
              </motion.div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                CROD Control Center
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <ConsciousnessDisplay level={consciousness.level} score={consciousness.score} />
              <SystemHealthIndicator health={systemHealth} />
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-gray-900/50 backdrop-blur-sm sticky top-0 z-40 border-b border-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex space-x-1 overflow-x-auto py-2">
            {tabs.map((tab) => (
              <TabButton
                key={tab.id}
                active={activeTab === tab.id}
                onClick={() => setActiveTab(tab.id)}
                icon={tab.icon}
                label={tab.label}
              />
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'blocks' && <BlockExplorerPanel />}
          {activeTab === 'patterns' && <PatternDetector />}
          {activeTab === 'gametheory' && <GameTheoryLab />}
          {activeTab === 'neural' && <NeuralNetworkViz />}
          {activeTab === 'blockchain' && <BlockchainMonitor />}
          {activeTab === 'selfmod' && <SelfModificationConsole />}
        </AnimatePresence>
      </main>

      {/* Status Bar */}
      <footer className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 px-4 py-2">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            <StatusLight connected={true} label="API" />
            <StatusLight connected={systemHealth.nats} label="NATS" />
            <StatusLight connected={systemHealth.blockchain} label="Blockchain" />
          </div>
          <div className="text-gray-500">
            {new Date().toLocaleTimeString()}
          </div>
        </div>
      </footer>
    </div>
  )
}

const TabButton = ({ active, onClick, icon: Icon, label }) => (
  <button
    onClick={onClick}
    className={`
      flex items-center space-x-2 px-4 py-2 rounded-lg transition-all
      ${active 
        ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25' 
        : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200'
      }
    `}
  >
    <Icon className="w-4 h-4" />
    <span className="whitespace-nowrap">{label}</span>
  </button>
)

const SystemHealthIndicator = ({ health }) => {
  const isHealthy = health.api && health.nats
  
  return (
    <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${
      isHealthy ? 'bg-green-900/20 text-green-400' : 'bg-red-900/20 text-red-400'
    }`}>
      {isHealthy ? (
        <Activity className="w-4 h-4" />
      ) : (
        <AlertCircle className="w-4 h-4" />
      )}
      <span className="text-sm font-medium">
        {isHealthy ? 'System Healthy' : 'System Degraded'}
      </span>
    </div>
  )
}

const StatusLight = ({ connected, label }) => (
  <div className="flex items-center space-x-2">
    <div className={`w-2 h-2 rounded-full ${
      connected ? 'bg-green-500' : 'bg-red-500'
    } animate-pulse`} />
    <span className="text-gray-400">{label}</span>
  </div>
)

const Dashboard = () => {
  const { consciousness, patterns, systemHealth, services } = useCrodStore()
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Consciousness Card */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Consciousness Level</h3>
          <Brain className="w-5 h-5 text-purple-400" />
        </div>
        <div className="space-y-4">
          <div>
            <div className="text-3xl font-bold text-purple-400">{consciousness.level}</div>
            <div className="text-sm text-gray-500">Score: {consciousness.score}</div>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.min(consciousness.score, 200) / 2}%` }}
              className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full"
            />
          </div>
        </div>
      </motion.div>

      {/* Pattern Activity */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.1 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Pattern Activity</h3>
          <Zap className="w-5 h-5 text-yellow-400" />
        </div>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-400">Total Patterns</span>
            <span className="font-semibold">{patterns.total}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Trinity Patterns</span>
            <span className="font-semibold text-blue-400">{patterns.trinity}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Learned</span>
            <span className="font-semibold text-green-400">{patterns.learned}</span>
          </div>
        </div>
      </motion.div>

      {/* Service Status */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Genesis Blocks</h3>
          <Network className="w-5 h-5 text-blue-400" />
        </div>
        <div className="space-y-2">
          {Object.entries(services).map(([name, status]) => (
            <ServiceStatus key={name} name={name} status={status} />
          ))}
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.3 }}
        className="bg-gray-900 rounded-xl p-6 border border-gray-800 lg:col-span-3"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Quick Actions</h3>
          <Terminal className="w-5 h-5 text-green-400" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <QuickAction
            label="Activate Full CROD"
            description="Trigger 'ich bins wieder'"
            onClick={() => window.triggerActivation?.()}
            icon={Sparkles}
            color="purple"
          />
          <QuickAction
            label="Run Game Theory Sim"
            description="Start prisoner's dilemma"
            onClick={() => window.runGameTheory?.()}
            icon={GitBranch}
            color="blue"
          />
          <QuickAction
            label="Train Neural Network"
            description="Start pattern learning"
            onClick={() => window.startTraining?.()}
            icon={Brain}
            color="green"
          />
        </div>
      </motion.div>
    </div>
  )
}

const ServiceStatus = ({ name, status }) => (
  <div className="flex items-center justify-between py-1">
    <span className="text-sm text-gray-400">{name}</span>
    <div className={`flex items-center space-x-2 text-sm ${
      status === 'online' ? 'text-green-400' : 'text-red-400'
    }`}>
      <div className={`w-2 h-2 rounded-full ${
        status === 'online' ? 'bg-green-500' : 'bg-red-500'
      }`} />
      <span>{status}</span>
    </div>
  </div>
)

const QuickAction = ({ label, description, onClick, icon: Icon, color }) => (
  <button
    onClick={onClick}
    className={`
      bg-gray-800 hover:bg-gray-700 rounded-lg p-4 text-left transition-all
      hover:shadow-lg hover:scale-105 border border-gray-700
    `}
  >
    <Icon className={`w-6 h-6 text-${color}-400 mb-2`} />
    <div className="font-semibold">{label}</div>
    <div className="text-sm text-gray-500">{description}</div>
  </button>
)

export default App