import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import * as Tabs from '@radix-ui/react-tabs';
import { Dashboard } from './components/Dashboard';
import { BlockchainView } from './components/BlockchainView';
import { ParasiteControl } from './components/ParasiteControl';
import { IntegratedSystem } from './components/IntegratedSystem';
import { LiveCodingConsole } from './components/LiveCodingConsole';
import { useCRODStore } from './store/crodStore';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Blocks, Brain, Settings, RefreshCw, Terminal } from 'lucide-react';
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("live-coding");
  const [updateAvailable, setUpdateAvailable] = useState(false);
  const { isRunning, quantumEntanglement, updateQuantum } = useCRODStore();

  // Check for updates on mount
  useEffect(() => {
    // Simulate quantum fluctuations
    const interval = setInterval(() => {
      if (isRunning) {
        updateQuantum(Math.min(100, Math.max(0, quantumEntanglement + (Math.random() - 0.5) * 10)));
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [isRunning, quantumEntanglement, updateQuantum]);

  const tabs = [
    { id: 'live-coding', label: '🧠 Live Coding', icon: Terminal },
    { id: 'integrated', label: '🏠 Integrated', icon: Home },
    { id: 'dashboard', label: '📊 Dashboard', icon: Home },
    { id: 'blockchain', label: '⛓️ Blockchain', icon: Blocks },
    { id: 'parasite', label: '🦠 Parasite', icon: Brain },
    { id: 'settings', label: '⚙️ Settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-crod-darker">
      {/* Background Animation */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-crod-primary/20 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-crod-quantum/20 rounded-full blur-[100px] animate-pulse" />
      </div>

      <div className="relative z-10">
        <Tabs.Root value={activeTab} onValueChange={setActiveTab} className="h-screen flex flex-col">
          {/* Tab List */}
          <Tabs.List className="flex border-b border-crod-primary/20 bg-crod-dark/50 backdrop-blur-sm">
            {tabs.map((tab) => (
              <Tabs.Trigger
                key={tab.id}
                value={tab.id}
                className={`flex-1 flex items-center justify-center gap-2 py-4 px-6 transition-all duration-300 border-b-2 ${
                  activeTab === tab.id
                    ? 'border-crod-primary text-crod-primary bg-crod-primary/10'
                    : 'border-transparent text-gray-400 hover:text-white hover:bg-crod-dark/30'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </Tabs.Trigger>
            ))}
          </Tabs.List>

          {/* Tab Content */}
          <div className="flex-1 overflow-auto">
            <Tabs.Content value="live-coding" className="h-full">
              <LiveCodingConsole />
            </Tabs.Content>
            
            <Tabs.Content value="integrated" className="h-full">
              <IntegratedSystem />
            </Tabs.Content>
            
            <Tabs.Content value="dashboard" className="h-full">
              <Dashboard />
            </Tabs.Content>
            
            <Tabs.Content value="blockchain" className="h-full">
              <BlockchainView />
            </Tabs.Content>
            
            <Tabs.Content value="parasite" className="h-full">
              <ParasiteControl />
            </Tabs.Content>
            
            <Tabs.Content value="settings" className="h-full">
              <div className="p-6">
                <h2 className="text-2xl font-bold mb-6 text-crod-primary">Settings</h2>
                <div className="crod-card">
                  <h3 className="text-lg font-semibold mb-4">System Configuration</h3>
                  <p className="text-gray-400">Settings coming soon...</p>
                  
                  <div className="mt-6">
                    <button className="crod-button flex items-center gap-2">
                      <RefreshCw className="w-4 h-4" />
                      Check for Updates
                    </button>
                  </div>
                </div>
              </div>
            </Tabs.Content>
          </div>
        </Tabs.Root>
      </div>
    </div>
  );
}

export default App;
