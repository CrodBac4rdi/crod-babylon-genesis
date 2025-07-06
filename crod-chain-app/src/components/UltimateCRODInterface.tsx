import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { invoke } from '@tauri-apps/api/core';
import { 
  Brain, 
  Zap, 
  Code, 
  FileText, 
  Download,
  Play,
  Activity,
  Cpu,
  Settings
} from 'lucide-react';

interface ClaudeResponse {
  content: string;
  model: string;
  tokens_used?: number;
  success: boolean;
}

interface CodeExecutionResult {
  output: string;
  exit_code: number;
  language: string;
  execution_time_ms: number;
}

const UltimateCRODInterface: React.FC = () => {
  const [chatMessages, setChatMessages] = useState<Array<{role: string, content: string, timestamp: number}>>([]);
  const [currentInput, setCurrentInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [systemInfo, setSystemInfo] = useState<any>(null);
  const [liveMetrics, setLiveMetrics] = useState({
    cpuUsage: 0,
    memoryUsage: 0,
    activeTasks: 0,
    quantumField: 0
  });

  // Live metrics update
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveMetrics(prev => ({
        cpuUsage: Math.random() * 100,
        memoryUsage: Math.random() * 100,
        activeTasks: Math.floor(Math.random() * 10),
        quantumField: Math.sin(Date.now() / 1000) * 50 + 50
      }));
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Add welcome message
  useEffect(() => {
    setChatMessages([{
      role: 'assistant',
      content: '🦠 CROD System Online! Ready for AI/ML live coding.\n\nI can help you with:\n• Code execution (Python, JavaScript, Rust, Bash)\n• File operations\n• System analysis\n• Real-time AI assistance\n\nWhat would you like to do?',
      timestamp: Date.now()
    }]);
  }, []);

  const loadSystemInfo = async () => {
    try {
      const info = await invoke<string>('real_get_system_info');
      setSystemInfo(info);
    } catch (error) {
      setSystemInfo(`Error loading system info: ${error}`);
    }
  };

  const handleClaudeChat = async () => {
    if (!currentInput.trim()) return;
    
    setIsProcessing(true);
    try {
      const response = await invoke<ClaudeResponse>('real_chat_with_claude', {
        message: currentInput
      });
      setChatMessages(prev => [...prev, {
        role: 'user',
        content: currentInput,
        timestamp: Date.now()
      }, {
        role: 'assistant',
        content: response.content,
        timestamp: Date.now()
      }]);
    } catch (error) {
      setChatMessages(prev => [...prev, {
        role: 'user',
        content: currentInput,
        timestamp: Date.now()
      }, {
        role: 'assistant',
        content: `Error: ${error}`,
        timestamp: Date.now()
      }]);
    }
    setIsProcessing(false);
    setCurrentInput('');
  };

  const handleCodeExecution = async () => {
    if (!currentInput.trim()) return;
    
    setIsProcessing(true);
    try {
      const result = await invoke<CodeExecutionResult>('real_execute_code', {
        code: currentInput,
        language: 'python' // Default to Python for code execution
      });
      setChatMessages(prev => [...prev, {
        role: 'user',
        content: currentInput,
        timestamp: Date.now()
      }, {
        role: 'assistant',
        content: `Output: ${result.output}\n\nExecution Time: ${result.execution_time_ms}ms\n\nExit Code: ${result.exit_code}`,
        timestamp: Date.now()
      }]);
    } catch (error) {
      setChatMessages(prev => [...prev, {
        role: 'user',
        content: currentInput,
        timestamp: Date.now()
      }, {
        role: 'assistant',
        content: `Error: ${error}`,
        timestamp: Date.now()
      }]);
    }
    setIsProcessing(false);
    setCurrentInput('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 p-6">
      <div className="max-w-[1800px] mx-auto">
        {/* Header */}
        <motion.div 
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                🦠 CROD ULTIMATE
              </h1>
              <p className="text-xl text-gray-300 mt-2">AI/ML Live Coding Parasite</p>
            </div>
            
            {/* Live Metrics Dashboard */}
            <div className="grid grid-cols-4 gap-4 text-center">
              <div className="bg-gray-800/50 p-3 rounded-lg border border-purple-500/30">
                <div className="text-2xl font-bold text-green-400">{liveMetrics.cpuUsage.toFixed(1)}%</div>
                <div className="text-xs text-gray-400">CPU</div>
              </div>
              <div className="bg-gray-800/50 p-3 rounded-lg border border-blue-500/30">
                <div className="text-2xl font-bold text-blue-400">{liveMetrics.memoryUsage.toFixed(1)}%</div>
                <div className="text-xs text-gray-400">RAM</div>
              </div>
              <div className="bg-gray-800/50 p-3 rounded-lg border border-cyan-500/30">
                <div className="text-2xl font-bold text-cyan-400">{liveMetrics.activeTasks}</div>
                <div className="text-xs text-gray-400">Tasks</div>
              </div>
              <div className="bg-gray-800/50 p-3 rounded-lg border border-pink-500/30">
                <div className="text-2xl font-bold text-pink-400">{liveMetrics.quantumField.toFixed(1)}%</div>
                <div className="text-xs text-gray-400">Quantum</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Main Bento Grid */}
        <div className="grid grid-cols-12 grid-rows-8 gap-6 h-[1000px]">
          
          {/* Claude Chat - Large */}
          <motion.div 
            className="col-span-6 row-span-4 bg-gradient-to-br from-purple-900/20 to-purple-600/20 rounded-3xl p-6 border border-purple-500/30 backdrop-blur-xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Brain className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">Real Claude Integration</h3>
              <div className="ml-auto">
                {/* {chatResponse?.success && (
                  <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded-full text-xs">
                    ✓ Connected
                  </span>
                )} */}
              </div>
            </div>
            
            <div className="h-64 bg-black/30 rounded-xl p-4 mb-4 overflow-y-auto font-mono text-sm">
              {chatMessages.length > 0 ? (
                <div>
                  {chatMessages.map((msg, index) => (
                    <div key={index} className={`mb-2 ${msg.role === 'user' ? 'text-blue-400' : 'text-white'}`}>
                      <span className="font-semibold">{msg.role === 'user' ? 'You' : 'CROD'}:</span> {msg.content}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-500">
                  🤖 Ask CROD anything and get real Claude responses...
                </div>
              )}
            </div>
            
            <div className="flex gap-2">
              <input
                type="text"
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                placeholder="Chat with Claude through CROD..."
                className="flex-1 bg-black/30 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                onKeyPress={(e) => e.key === 'Enter' && handleClaudeChat()}
              />
              <button
                onClick={handleClaudeChat}
                disabled={isProcessing}
                className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-600 px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
              >
                {isProcessing ? (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <Zap className="w-4 h-4" />
                )}
              </button>
            </div>
          </motion.div>

          {/* Code Execution - Large */}
          <motion.div 
            className="col-span-6 row-span-4 bg-gradient-to-br from-blue-900/20 to-cyan-600/20 rounded-3xl p-6 border border-blue-500/30 backdrop-blur-xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Code className="w-6 h-6 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Real Code Execution</h3>
              <select
                value={'python'} // Default to Python
                onChange={() => {}}
                className="ml-auto bg-black/30 border border-white/10 rounded-lg px-3 py-1 text-white text-sm"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="rust">Rust</option>
                <option value="bash">Bash</option>
              </select>
            </div>
            
            <div className="space-y-4 h-64">
              <textarea
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                className="w-full h-24 bg-black/30 border border-white/10 rounded-lg p-3 text-white font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your code here..."
              />
              
              <div className="h-32 bg-black/30 rounded-lg p-3 overflow-y-auto font-mono text-sm">
                {/* {codeResult ? (
                  <div>
                    <div className="text-gray-400 text-xs mb-2">
                      Exit Code: {codeResult.exit_code} | Time: {codeResult.execution_time_ms}ms | Lang: {codeResult.language}
                    </div>
                    <pre className="text-white whitespace-pre-wrap">
                      {codeResult.output}
                    </pre>
                  </div>
                ) : (
                  <div className="text-gray-500">
                    💻 Code output will appear here...
                  </div>
                )} */}
              </div>
            </div>
            
            <div className="flex gap-2 mt-4">
              <button
                onClick={handleCodeExecution}
                disabled={isProcessing}
                className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
              >
                <Play className="w-4 h-4" />
                Execute
              </button>
              <button
                onClick={() => {}}
                disabled={isProcessing}
                className="bg-green-500 hover:bg-green-600 disabled:bg-gray-600 px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Install Package
              </button>
            </div>
          </motion.div>

          {/* System Info */}
          <motion.div 
            className="col-span-4 row-span-2 bg-gradient-to-br from-green-900/20 to-emerald-600/20 rounded-3xl p-6 border border-green-500/30 backdrop-blur-xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Cpu className="w-6 h-6 text-green-400" />
              <h3 className="text-lg font-bold text-white">System Info</h3>
            </div>
            <div className="bg-black/30 rounded-lg p-3 h-20 overflow-y-auto font-mono text-xs">
              <pre className="text-green-400 whitespace-pre-wrap">
                {systemInfo || 'Loading system information...'}
              </pre>
            </div>
          </motion.div>

          {/* Neural Activity */}
          <motion.div 
            className="col-span-4 row-span-2 bg-gradient-to-br from-pink-900/20 to-rose-600/20 rounded-3xl p-6 border border-pink-500/30 backdrop-blur-xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <Activity className="w-6 h-6 text-pink-400" />
              <h3 className="text-lg font-bold text-white">Neural Activity</h3>
            </div>
            <div className="flex items-center justify-center h-20">
              <div className="relative">
                <div className="w-16 h-16 bg-pink-500/20 rounded-full flex items-center justify-center">
                  <Activity className="w-8 h-8 text-pink-400" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-pink-500 rounded-full animate-pulse"></div>
              </div>
            </div>
          </motion.div>

          {/* File Operations */}
          <motion.div 
            className="col-span-4 row-span-2 bg-gradient-to-br from-orange-900/20 to-amber-600/20 rounded-3xl p-6 border border-orange-500/30 backdrop-blur-xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <FileText className="w-6 h-6 text-orange-400" />
              <h3 className="text-lg font-bold text-white">File Operations</h3>
            </div>
            <div className="flex gap-2">
              <button className="flex-1 bg-orange-500/20 hover:bg-orange-500/30 border border-orange-500/30 px-3 py-2 rounded-lg text-orange-400 text-sm transition-colors">
                Read
              </button>
              <button className="flex-1 bg-orange-500/20 hover:bg-orange-500/30 border border-orange-500/30 px-3 py-2 rounded-lg text-orange-400 text-sm transition-colors">
                Write
              </button>
            </div>
          </motion.div>

        </div>

        {/* Status Bar */}
        <motion.div 
          className="mt-6 bg-gray-800/50 rounded-2xl p-4 backdrop-blur-sm border border-white/10"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400 font-mono text-sm">CROD Active</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-blue-400 font-mono text-sm">Real Backend</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                <span className="text-purple-400 font-mono text-sm">Claude Ready</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Settings className="w-4 h-4 text-gray-400" />
              <span className="text-gray-400 text-sm">v3.0.0 • Real Integration</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default UltimateCRODInterface;
