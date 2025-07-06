import React from 'react';
import { Brain, Cpu, Activity, Zap, Database, GitBranch } from 'lucide-react';
import { useCRODStore } from '../store/crodStore';
import { motion } from 'framer-motion';

export const Dashboard: React.FC = () => {
  const {
    isRunning,
    neurons,
    synapses,
    quantumEntanglement,
    blocksMinced,
    patternsLearned,
    userSatisfaction,
    parasiteActive,
    startSystem,
    stopSystem,
    toggleParasite,
  } = useCRODStore();

  const stats = [
    { label: 'Neurons', value: neurons, icon: Brain, color: 'text-crod-primary' },
    { label: 'Synapses', value: synapses, icon: GitBranch, color: 'text-crod-secondary' },
    { label: 'Blocks', value: blocksMinced, icon: Database, color: 'text-crod-accent' },
    { label: 'Patterns', value: patternsLearned, icon: Cpu, color: 'text-crod-quantum' },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-crod-primary to-crod-secondary bg-clip-text text-transparent">
          CROD Chain Control Center
        </h1>
        
        <div className="flex gap-4">
          <button
            onClick={toggleParasite}
            className={`px-6 py-3 rounded-lg font-bold transition-all duration-300 ${
              parasiteActive 
                ? 'bg-crod-quantum text-white shadow-lg shadow-crod-quantum/50' 
                : 'bg-gray-700 text-gray-400'
            }`}
          >
            {parasiteActive ? 'PARASITE ACTIVE' : 'PARASITE INACTIVE'}
          </button>
          
          <button
            onClick={isRunning ? stopSystem : startSystem}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-300 ${
              isRunning 
                ? 'bg-red-600 hover:bg-red-700 text-white' 
                : 'bg-crod-primary hover:bg-crod-primary/80 text-white animate-pulse'
            }`}
          >
            {isRunning ? 'STOP SYSTEM' : 'START CROD'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="crod-card quantum-border"
          >
            <div className="flex items-center justify-between mb-4">
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
              <span className="text-2xl font-bold">{stat.value.toLocaleString()}</span>
            </div>
            <p className="text-gray-400">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="crod-card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Quantum Entanglement</h2>
            <Zap className="w-6 h-6 text-crod-quantum" />
          </div>
          
          <div className="relative h-4 bg-crod-darker rounded-full overflow-hidden">
            <motion.div
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-crod-quantum to-crod-primary"
              animate={{ width: `${quantumEntanglement}%` }}
              transition={{ type: 'spring', stiffness: 100 }}
            />
          </div>
          <p className="mt-2 text-sm text-gray-400">{quantumEntanglement.toFixed(1)}% Entangled</p>
        </div>

        <div className="crod-card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">User Satisfaction</h2>
            <Activity className="w-6 h-6 text-crod-accent" />
          </div>
          
          <div className="relative h-4 bg-crod-darker rounded-full overflow-hidden">
            <motion.div
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-crod-accent to-crod-secondary"
              animate={{ width: `${userSatisfaction}%` }}
              transition={{ type: 'spring', stiffness: 100 }}
            />
          </div>
          <p className="mt-2 text-sm text-gray-400">{userSatisfaction}% Satisfied</p>
        </div>
      </div>

      <div className="crod-card">
        <h2 className="text-xl font-bold mb-4">System Status</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
            <span className="text-gray-400">Core System</span>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${parasiteActive ? 'bg-crod-quantum' : 'bg-gray-600'} animate-pulse`} />
            <span className="text-gray-400">Parasite Mode</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-crod-secondary animate-pulse" />
            <span className="text-gray-400">Blockchain Active</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-crod-primary animate-pulse" />
            <span className="text-gray-400">Neural Network</span>
          </div>
        </div>
      </div>
    </div>
  );
};