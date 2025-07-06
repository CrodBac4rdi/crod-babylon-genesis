import React, { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

interface CRODMessage {
  type: 'user' | 'claude' | 'crod' | 'system';
  content: string;
  timestamp: number;
  metadata?: any;
}

interface CRODStats {
  total_neurons: number;
  active_neurons: number;
  consciousness: number;
  quantum_level: number;
  interactions: number;
  improvements: number;
  parasite_active: boolean;
}

export const LiveCodingConsole: React.FC = () => {
  const [messages, setMessages] = useState<CRODMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [crodStats, setCRODStats] = useState<CRODStats | null>(null);
  const [parasiteMode, setParasiteMode] = useState(false);
  const [crashLog, setCrashLog] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-scroll to bottom
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Initialize CROD and load stats
    loadCRODStats();
    
    // Set up crash recovery
    const savedMessages = localStorage.getItem('crod_messages');
    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
      addSystemMessage('🔄 CROD: Session restored from crash log');
    }
    
    // Periodic stats update
    const interval = setInterval(loadCRODStats, 2000);
    return () => clearInterval(interval);
  }, []);

  const addSystemMessage = (content: string) => {
    const message: CRODMessage = {
      type: 'system',
      content,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, message]);
  };

  const loadCRODStats = async () => {
    try {
      const stats = await invoke('get_crod_stats');
      setCRODStats(stats as CRODStats);
    } catch (error) {
      console.error('Failed to load CROD stats:', error);
    }
  };

  const toggleParasiteMode = async () => {
    try {
      const newState = await invoke('toggle_parasite_mode');
      setParasiteMode(newState as boolean);
      addSystemMessage(
        `🦠 CROD Parasit-Modus: ${newState ? 'AKTIV' : 'INAKTIV'}`
      );
    } catch (error) {
      addSystemMessage(`❌ Error toggling parasite mode: ${error}`);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: CRODMessage = {
      type: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Save to crash log
      const updatedMessages = [...messages, userMessage];
      localStorage.setItem('crod_messages', JSON.stringify(updatedMessages));

      // Process with CROD
      const response = await invoke('process_with_crod', {
        userInput: input,
        parasiteMode: parasiteMode
      });

      const claudeMessage: CRODMessage = {
        type: 'claude',
        content: response as string,
        timestamp: Date.now()
      };

      setMessages(prev => [...prev, claudeMessage]);
      
      // Update crash log
      localStorage.setItem('crod_messages', JSON.stringify([...updatedMessages, claudeMessage]));
      
      // Load updated stats
      loadCRODStats();

    } catch (error) {
      const errorMessage: CRODMessage = {
        type: 'system',
        content: `❌ CRASH DETECTED: ${error}`,
        timestamp: Date.now()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setCrashLog(prev => [...prev, `${new Date().toISOString()}: ${error}`]);
      
      // Auto-recovery
      setTimeout(() => {
        addSystemMessage('🔄 CROD: Auto-recovery activated, restarting...');
        loadCRODStats();
      }, 2000);
    } finally {
      setIsLoading(false);
    }
  };

  const clearCrashLog = () => {
    localStorage.removeItem('crod_messages');
    setCrashLog([]);
    setMessages([]);
    addSystemMessage('🧹 CROD: Session cleared, fresh start!');
  };

  const formatMessageContent = (message: CRODMessage) => {
    // Handle code blocks and formatting
    if (message.content.includes('```')) {
      return message.content; // Keep as is for now, add syntax highlighting later
    }
    return message.content;
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-green-400 font-mono">
      {/* Header with CROD Stats */}
      <div className="p-4 border-b border-green-600 bg-black">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-green-400">
              🧠 CROD Live Coding Console
            </h1>
            <button
              onClick={toggleParasiteMode}
              className={`px-3 py-1 rounded ${
                parasiteMode 
                  ? 'bg-red-600 hover:bg-red-700' 
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              🦠 Parasit: {parasiteMode ? 'AKTIV' : 'INAKTIV'}
            </button>
          </div>
          
          <div className="flex space-x-4 text-sm">
            {crodStats && (
              <>
                <div>🧠 Neurons: {crodStats.active_neurons}/{crodStats.total_neurons}</div>
                <div>🌟 Consciousness: {crodStats.consciousness.toFixed(1)}%</div>
                <div>⚡ Quantum: {crodStats.quantum_level.toFixed(1)}%</div>
                <div>🔄 Interactions: {crodStats.interactions}</div>
                <div>✨ Improvements: {crodStats.improvements}</div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl p-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-900 text-blue-100'
                  : message.type === 'claude'
                  ? 'bg-green-900 text-green-100'
                  : message.type === 'crod'
                  ? 'bg-purple-900 text-purple-100'
                  : 'bg-gray-800 text-gray-300'
              }`}
            >
              <div className="flex items-center mb-2">
                <span className="text-sm font-bold">
                  {message.type === 'user' ? '👤 You' : 
                   message.type === 'claude' ? '🤖 Claude' :
                   message.type === 'crod' ? '🧠 CROD' : '⚙️ System'}
                </span>
                <span className="text-xs ml-2 opacity-70">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="whitespace-pre-wrap">
                {formatMessageContent(message)}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-gray-300 p-3 rounded-lg">
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-400 mr-2"></div>
                🧠 CROD is processing...
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-green-600 bg-black">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message to Claude/CROD..."
            className="flex-1 bg-gray-800 text-green-400 p-2 rounded border border-green-600 focus:outline-none focus:border-green-400"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-4 py-2 rounded"
          >
            Send
          </button>
          <button
            onClick={clearCrashLog}
            className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
            title="Clear crash log and restart"
          >
            🧹 Clear
          </button>
        </div>
      </div>

      {/* Crash Log Display */}
      {crashLog.length > 0 && (
        <div className="p-2 bg-red-900 text-red-100 text-xs max-h-20 overflow-y-auto">
          <div className="font-bold">Crash Log:</div>
          {crashLog.map((log, index) => (
            <div key={index}>{log}</div>
          ))}
        </div>
      )}
    </div>
  );
};
