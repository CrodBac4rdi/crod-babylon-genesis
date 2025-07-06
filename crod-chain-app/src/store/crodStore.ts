import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface Block {
  id: string;
  previousHash: string;
  timestamp: number;
  data: any;
  hash: string;
  nonce: number;
  consciousness: number;
}

interface CRODState {
  // Blockchain
  chain: Block[];
  miningDifficulty: number;
  
  // Neural Network
  neurons: number;
  synapses: number;
  learningRate: number;
  patterns: Record<string, any>;
  
  // System Status
  isRunning: boolean;
  parasiteActive: boolean;
  quantumEntanglement: number;
  
  // Stats
  blocksMinced: number;
  patternsLearned: number;
  userSatisfaction: number;
  
  // Actions
  startSystem: () => void;
  stopSystem: () => void;
  addBlock: (data: any) => void;
  updateQuantum: (value: number) => void;
  learnPattern: (pattern: any) => void;
  toggleParasite: () => void;
}

export const useCRODStore = create<CRODState>()(
  persist(
    (set, get) => ({
      // Initial state
      chain: [],
      miningDifficulty: 4,
      neurons: 88,
      synapses: 7744,
      learningRate: 0.001,
      patterns: {},
      isRunning: false,
      parasiteActive: false,
      quantumEntanglement: 0,
      blocksMinced: 0,
      patternsLearned: 0,
      userSatisfaction: 50,
      
      // Actions
      startSystem: () => set({ isRunning: true }),
      stopSystem: () => set({ isRunning: false }),
      
      addBlock: (data: any) => {
        const chain = get().chain;
        const previousBlock = chain[chain.length - 1];
        const newBlock: Block = {
          id: `block-${chain.length}`,
          previousHash: previousBlock?.hash || '0',
          timestamp: Date.now(),
          data,
          hash: '', // Will be calculated
          nonce: 0,
          consciousness: Math.random() * 100,
        };
        
        // Simple hash calculation (in real app, this would be more complex)
        newBlock.hash = btoa(JSON.stringify(newBlock));
        
        set(state => ({
          chain: [...state.chain, newBlock],
          blocksMinced: state.blocksMinced + 1,
        }));
      },
      
      updateQuantum: (value: number) => set({ quantumEntanglement: value }),
      
      learnPattern: (pattern: any) => {
        set(state => ({
          patterns: { ...state.patterns, [Date.now()]: pattern },
          patternsLearned: state.patternsLearned + 1,
        }));
      },
      
      toggleParasite: () => set(state => ({ parasiteActive: !state.parasiteActive })),
    }),
    {
      name: 'crod-storage',
    }
  )
);