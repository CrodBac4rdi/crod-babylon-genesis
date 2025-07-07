import { create } from 'zustand'
import axios from 'axios'
import io from 'socket.io-client'

const API_BASE = 'http://localhost:3001/api'

export const useCrodStore = create((set, get) => ({
  // State
  consciousness: {
    level: 'DORMANT',
    score: 0,
    history: []
  },
  
  patterns: {
    total: 0,
    trinity: 0,
    learned: 0,
    recent: []
  },
  
  systemHealth: {
    api: false,
    nats: false,
    blockchain: false,
    services: {}
  },
  
  services: {
    'Pattern Genesis': 'offline',
    'Short-Term Memory': 'offline',
    'Working Memory': 'offline',
    'Quantum Superposition': 'offline',
    'Neural Genesis': 'offline',
    'Master Orchestrator': 'offline'
  },
  
  gameTheory: {
    activeGames: [],
    equilibria: [],
    simulations: []
  },
  
  neuralNetwork: {
    architecture: [],
    training: false,
    loss: 0,
    accuracy: 0
  },
  
  // Actions
  fetchSystemStatus: async () => {
    try {
      const response = await axios.get(`${API_BASE}/status`)
      const data = response.data
      
      set({
        consciousness: {
          level: data.consciousness?.level || 'DORMANT',
          score: data.consciousness?.score || 0,
          history: data.consciousness?.history || []
        },
        patterns: {
          total: data.patterns?.total_patterns || 0,
          trinity: data.patterns?.trinity_patterns || 0,
          learned: data.patterns?.learned_patterns || 0,
          recent: data.patterns?.recent_detections || []
        },
        systemHealth: {
          api: true,
          nats: !data.health?.emergency_mode,
          blockchain: Object.values(data.health?.services || {}).some(s => s.healthy),
          services: data.health?.services || {}
        }
      })
      
      // Update service status
      const serviceStatus = {}
      Object.entries(data.health?.services || {}).forEach(([key, value]) => {
        const name = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
        serviceStatus[name] = value.healthy ? 'online' : 'offline'
      })
      set({ services: serviceStatus })
      
    } catch (error) {
      console.error('Failed to fetch status:', error)
      set({ 
        systemHealth: { 
          api: false, 
          nats: false, 
          blockchain: false,
          services: {}
        } 
      })
    }
  },
  
  detectPattern: async (input) => {
    try {
      const response = await axios.post(`${API_BASE}/neural/process`, { input })
      return response.data
    } catch (error) {
      console.error('Pattern detection failed:', error)
      return null
    }
  },
  
  activateFullCROD: async () => {
    try {
      const response = await axios.get(`${API_BASE}/activate`)
      await get().fetchSystemStatus()
      return response.data
    } catch (error) {
      console.error('Activation failed:', error)
      return null
    }
  },
  
  connectWebSocket: () => {
    // Use native WebSocket instead of socket.io
    const ws = new WebSocket('ws://localhost:3001')
    
    ws.onopen = () => {
      console.log('WebSocket connected to CROD Live System')
    }
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        switch(data.type) {
          case 'status':
            // Update services from live system
            const serviceMap = {}
            Object.entries(data.services).forEach(([key, info]) => {
              serviceMap[info.description] = info.status
            })
            set({ services: serviceMap })
            break
            
          case 'neural_result':
            // Update neural network data
            set(state => ({
              patterns: {
                ...state.patterns,
                recent: [...data.data.patterns, ...state.patterns.recent].slice(0, 10),
                total: state.patterns.total + data.data.patterns.length
              },
              consciousness: {
                ...state.consciousness,
                score: Math.round(data.data.confidence * 100)
              }
            }))
            break
            
          case 'welcome':
            console.log('Connected:', data.message)
            break
        }
      } catch (e) {
        console.error('WebSocket message error:', e)
      }
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    return () => ws.close()
  },
  
  // Game Theory Actions
  createGame: async (gameType, players) => {
    try {
      const response = await axios.post(`${API_BASE}/game/create`, { gameType, players })
      return response.data
    } catch (error) {
      console.error('Game creation failed:', error)
      return null
    }
  },
  
  findEquilibrium: async (gameId) => {
    try {
      const response = await axios.post(`${API_BASE}/game/equilibrium`, { gameId })
      return response.data
    } catch (error) {
      console.error('Equilibrium calculation failed:', error)
      return null
    }
  },
  
  // Neural Network Actions
  startTraining: async (config) => {
    set(state => ({ 
      neuralNetwork: { 
        ...state.neuralNetwork, 
        training: true 
      } 
    }))
    
    try {
      const response = await axios.post(`${API_BASE}/neural/train`, config)
      return response.data
    } catch (error) {
      console.error('Training failed:', error)
      return null
    } finally {
      set(state => ({ 
        neuralNetwork: { 
          ...state.neuralNetwork, 
          training: false 
        } 
      }))
    }
  }
}))