import { useState, useEffect } from "react";
import * as Tabs from '@radix-ui/react-tabs';
import { Dashboard } from './components/Dashboard';
import { BlockchainView } from './components/BlockchainView';
import { ParasiteControl } from './components/ParasiteControl';
import { useCRODStore } from './store/crodStore';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Blocks, Brain, Settings, AlertCircle } from 'lucide-react';
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const { isRunning, quantumEntanglement, updateQuantum } = useCRODStore();

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
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'blockchain', label: 'Blockchain', icon: Blocks },
    { id: 'parasite', label: 'Parasite', icon: Brain },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-crod-darker">
      {/* Background Animation */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-crod-primary/20 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-crod-quantum/20 rounded-full blur-[100px] animate-pulse" />
      </div>

      {/* Web Version Notice */}
      <div className="fixed top-0 left-0 right-0 bg-yellow-500/10 text-yellow-500 p-2 text-center text-sm z-50 backdrop-blur-sm">
        <AlertCircle className="inline w-4 h-4 mr-2" />
        Web Version - Running without Tauri backend. Data is stored locally.
      </div>

      <div className="relative z-10 pt-8">
        <Tabs.Root value={activeTab} onValueChange={setActiveTab} className="h-screen flex flex-col">
          {/* Tab List */}
          <Tabs.List className="flex border-b border-crod-primary/20 bg-crod-dark/50 backdrop-blur-sm">
            {tabs.map((tab) => (
              <Tabs.Trigger
                key={tab.id}
                value={tab.id}
                className={`flex-1 flex items-center justify-center gap-2 py-4 px-6 transition-all duration-300 border-b-2 ${
                  activeTab === tab.id
                    ? 'border-crod-primary text-crod-primary'
                    : 'border-transparent text-gray-400 hover:text-white'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span className="font-semibold">{tab.label}</span>
              </Tabs.Trigger>
            ))}
          </Tabs.List>

          {/* Tab Content */}
          <div className="flex-1 overflow-auto">
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
                <h2 className="text-2xl font-bold mb-6">Settings</h2>
                <div className="crod-card">
                  <h3 className="text-lg font-semibold mb-4">Web Version</h3>
                  <p className="text-gray-400">
                    This is the web version of CROD Chain. 
                    Download the desktop app for full functionality including:
                  </p>
                  <ul className="mt-4 space-y-2 text-gray-400">
                    <li>• Real blockchain mining</li>
                    <li>• Persistent storage</li>
                    <li>• Automatic updates</li>
                    <li>• Native performance</li>
                  </ul>
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