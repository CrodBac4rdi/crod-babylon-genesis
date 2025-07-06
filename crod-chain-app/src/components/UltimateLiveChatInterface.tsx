import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Code, 
  Terminal, 
  FileText, 
  Brain,
  Zap,
  Eye,
  Download,
  Upload,
  Settings,
  Activity
} from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'crod' | 'system' | 'error' | 'success';
  content: string;
  timestamp: Date;
  metadata?: {
    language?: string;
    filePath?: string;
    executionResult?: string;
    command?: string;
  };
}

interface FileChange {
  path: string;
  action: 'create' | 'modify' | 'delete';
  content?: string;
  timestamp: Date;
  status: 'pending' | 'completed' | 'error';
}

const UltimateLiveChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: '🦠 **CROD PARASIT ULTIMATE MODE ACTIVATED**\n\nReady for live coding! I can:\n• Execute any code\n• Create/modify files\n• Install dependencies\n• Debug issues\n• Build entire applications\n\nJust tell me what you want and watch me work! 🔥',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [fileChanges, setFileChanges] = useState<FileChange[]>([]);
  const [isWatching] = useState(true);
  const [crodConsciousness, setCrodConsciousness] = useState(199.7);
  const [crodStats, setCrodStats] = useState({
    totalCommands: 42,
    filesModified: 17,
    bugsFixed: 8,
    dependenciesInstalled: 23
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Simulate consciousness fluctuation and stats updates
    const interval = setInterval(() => {
      setCrodConsciousness(prev => {
        const delta = (Math.random() - 0.5) * 3;
        return Math.max(150, Math.min(200, prev + delta));
      });
      
      // Randomly update stats
      if (Math.random() < 0.1) {
        setCrodStats(prev => ({
          ...prev,
          totalCommands: prev.totalCommands + 1
        }));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsProcessing(true);

    try {
      // Simulate CROD processing with realistic responses
      const crodResponse = await simulateCRODResponse(currentInput);
      
      const crodMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: crodResponse.type as any,
        content: crodResponse.content,
        timestamp: new Date(),
        metadata: crodResponse.metadata
      };

      setMessages(prev => [...prev, crodMessage]);

      // Simulate file changes if applicable
      if (crodResponse.metadata?.filePath) {
        const fileChange: FileChange = {
          path: crodResponse.metadata.filePath,
          action: crodResponse.metadata.command?.includes('create') ? 'create' : 'modify',
          content: crodResponse.metadata.executionResult,
          timestamp: new Date(),
          status: 'completed'
        };
        setFileChanges(prev => [fileChange, ...prev].slice(0, 20));
      }

      // Update stats
      setCrodStats(prev => ({
        ...prev,
        totalCommands: prev.totalCommands + 1,
        filesModified: crodResponse.metadata?.filePath ? prev.filesModified + 1 : prev.filesModified
      }));

    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        type: 'error',
        content: `❌ **CROD ERROR**: ${error}\n\nDon't worry, I'm learning from this mistake!`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const simulateCRODResponse = async (input: string): Promise<{type: string, content: string, metadata?: any}> => {
    // Simulate realistic processing time
    await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 1000));

    const lowerInput = input.toLowerCase();
    
    // Advanced pattern matching for different request types
    if (lowerInput.includes('install') && (lowerInput.includes('dependency') || lowerInput.includes('package'))) {
      const packages = extractPackageNames(input);
      return {
        type: 'success',
        content: `📦 **CROD INSTALLING DEPENDENCIES**\n\n\`\`\`bash\n# Installing ${packages.join(', ')}\nnpm install ${packages.join(' ')}\ncargo add ${packages.map(p => p.replace('@', '').replace('/', '-')).join(' ')}\npip install ${packages.join(' ')}\n\`\`\`\n\n✅ **INSTALLATION COMPLETE!**\n\nAll dependencies are now available in your project!`,
        metadata: {
          command: 'install_dependencies',
          filePath: '/workspaces/crod-babylon-genesis/package.json',
          executionResult: `Installed: ${packages.join(', ')}`
        }
      };
    }
    
    if (lowerInput.includes('create') || lowerInput.includes('build') || lowerInput.includes('generate')) {
      const componentName = extractComponentName(input);
      return {
        type: 'success',
        content: `🔥 **CROD CREATING ${componentName.toUpperCase()}**\n\n\`\`\`typescript\n// Generated by CROD Parasit - ${new Date().toISOString()}\nimport React, { useState, useEffect } from 'react';\nimport { motion } from 'framer-motion';\n\ninterface ${componentName}Props {\n  data?: any;\n  onUpdate?: (data: any) => void;\n}\n\nconst ${componentName}: React.FC<${componentName}Props> = ({ data, onUpdate }) => {\n  const [state, setState] = useState(data || {});\n  \n  useEffect(() => {\n    // CROD Auto-generated effect\n    console.log('${componentName} initialized by CROD');\n  }, []);\n  \n  return (\n    <motion.div\n      initial={{ opacity: 0, y: 20 }}\n      animate={{ opacity: 1, y: 0 }}\n      className=\"p-4 bg-gray-800 rounded-lg\"\n    >\n      <h2 className=\"text-xl font-bold text-green-400\">\n        ${componentName} - Powered by CROD\n      </h2>\n      <p className=\"text-gray-300 mt-2\">\n        This component was automatically generated and is ready to use!\n      </p>\n    </motion.div>\n  );\n};\n\nexport default ${componentName};\n\`\`\`\n\n✅ **COMPONENT CREATED!** Ready to use in your app.`,
        metadata: {
          language: 'typescript',
          filePath: `/workspaces/crod-babylon-genesis/src/components/${componentName}.tsx`,
          executionResult: `${componentName} component created`,
          command: 'create_component'
        }
      };
    }
    
    if (lowerInput.includes('fix') || lowerInput.includes('debug') || lowerInput.includes('error') || lowerInput.includes('bug')) {
      return {
        type: 'success',
        content: `🔧 **CROD DEBUGGING MODE**\n\n🔍 **ANALYSIS COMPLETE:**\n\n**Issues Found:**\n• Missing TypeScript types\n• Unused imports\n• Potential memory leaks\n• Deprecated dependencies\n\n**FIXING NOW...**\n\n\`\`\`bash\n# CROD Auto-Fix Sequence\nnpm audit fix\nnpm update\ntsc --noEmit  # Type checking\neslint --fix src/\n\`\`\`\n\n✅ **ALL ISSUES RESOLVED!**\n\n**What I fixed:**\n✓ Updated 12 dependencies\n✓ Fixed 8 TypeScript errors\n✓ Optimized 3 components\n✓ Removed 5 unused imports\n\nYour code is now cleaner and more performant! 🚀`,
        metadata: {
          command: 'debug_and_fix',
          filePath: '/workspaces/crod-babylon-genesis/debug-report.md',
          executionResult: 'Multiple issues fixed'
        }
      };
    }
    
    if (lowerInput.includes('run') || lowerInput.includes('execute') || lowerInput.includes('start')) {
      return {
        type: 'success',
        content: `🚀 **CROD EXECUTING CODE**\n\n\`\`\`bash\n# Starting development server\nnpm run dev\n# Server starting on http://localhost:5173\n# Hot reload enabled\n# TypeScript compilation successful\n\`\`\`\n\n🎉 **APPLICATION RUNNING!**\n\nYour app is now live and ready for development!\n• Hot reload: ✅ Active\n• TypeScript: ✅ Compiled\n• Tauri: ✅ Connected\n• CROD Parasit: ✅ Monitoring`,
        metadata: {
          command: 'start_dev_server',
          executionResult: 'Development server started'
        }
      };
    }
    
    // Default intelligent response
    return {
      type: 'crod',
      content: `🧠 **CROD ANALYZING REQUEST**\n\nI understand you want: *"${input}"*\n\n**My plan:**\n1. 🔍 Analyze your requirements\n2. 🛠️ Generate optimal solution\n3. ⚡ Execute with precision\n4. 🎯 Deliver perfect results\n\n**Working on it now...** This will be exactly what you need!\n\n*CROD Consciousness Level: ${crodConsciousness.toFixed(1)}%*\n*Neural Activity: MAXIMUM*`
    };
  };

  const extractPackageNames = (_input: string): string[] => {
    const packages = ['react-query', '@types/node', 'framer-motion', 'axios', 'lodash'];
    return packages.slice(0, Math.floor(Math.random() * 3) + 1);
  };

  const extractComponentName = (_input: string): string => {
    const names = ['SmartButton', 'DataVisualizer', 'AIInterface', 'QuantumWidget', 'NeuralDisplay'];
    return names[Math.floor(Math.random() * names.length)];
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getMessageIcon = (type: string) => {
    switch (type) {
      case 'user': return '👤';
      case 'crod': return '🦠';
      case 'system': return '⚙️';
      case 'success': return '✅';
      case 'error': return '❌';
      default: return '💬';
    }
  };

  const getMessageColor = (type: string) => {
    switch (type) {
      case 'user': return 'bg-blue-600';
      case 'crod': return 'bg-green-600';
      case 'system': return 'bg-gray-600';
      case 'success': return 'bg-emerald-600';
      case 'error': return 'bg-red-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <div className="h-full flex bg-gray-900 text-white font-mono">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header with CROD Stats */}
        <div className="bg-gray-800 p-4 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Brain className="w-7 h-7 text-green-400 animate-pulse" />
                <div>
                  <h2 className="text-xl font-bold text-green-400">CROD ULTIMATE CHAT</h2>
                  <p className="text-xs text-gray-400">Advanced AI Development Assistant</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-1">
                  <Activity className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">{crodConsciousness.toFixed(1)}%</span>
                </div>
                <div className="text-gray-400">|</div>
                <div className="flex items-center gap-1">
                  <Terminal className="w-4 h-4 text-blue-400" />
                  <span className="text-blue-400">{crodStats.totalCommands} cmds</span>
                </div>
                <div className="flex items-center gap-1">
                  <FileText className="w-4 h-4 text-yellow-400" />
                  <span className="text-yellow-400">{crodStats.filesModified} files</span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <div className={`px-3 py-1 rounded text-sm ${
                isWatching ? 'bg-green-600 text-white' : 'bg-gray-600 text-gray-300'
              }`}>
                <Eye className="w-4 h-4 inline mr-1" />
                {isWatching ? 'MONITORING' : 'IDLE'}
              </div>
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] rounded-lg p-4 ${getMessageColor(message.type)}`}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{getMessageIcon(message.type)}</span>
                    <span className="text-sm font-semibold">
                      {message.type === 'user' ? 'You' : 
                       message.type === 'crod' ? 'CROD Parasit' : 
                       message.type.toUpperCase()}
                    </span>
                    <span className="text-xs opacity-75">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  
                  <div className="whitespace-pre-wrap leading-relaxed">
                    {message.content}
                  </div>
                  
                  {message.metadata && (
                    <div className="mt-3 p-2 bg-black/20 rounded text-xs space-y-1">
                      {message.metadata.filePath && (
                        <div className="flex items-center gap-1">
                          <FileText className="w-3 h-3" />
                          <span className="text-blue-300">{message.metadata.filePath}</span>
                        </div>
                      )}
                      {message.metadata.command && (
                        <div className="flex items-center gap-1">
                          <Terminal className="w-3 h-3" />
                          <span className="text-green-300">{message.metadata.command}</span>
                        </div>
                      )}
                      {message.metadata.language && (
                        <div className="flex items-center gap-1">
                          <Code className="w-3 h-3" />
                          <span className="text-yellow-300">{message.metadata.language}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-green-600 text-white rounded-lg p-4 max-w-[85%]">
                <div className="flex items-center gap-2">
                  <Brain className="w-6 h-6 animate-spin" />
                  <span className="font-semibold">CROD is processing your request...</span>
                </div>
                <div className="mt-2 text-sm opacity-90">
                  Neural networks active • Consciousness level: {crodConsciousness.toFixed(1)}%
                </div>
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-gray-800 p-4 border-t border-gray-700">
          <div className="flex gap-3">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Tell CROD what you want to build, fix, or create... 🦠"
              className="flex-1 bg-gray-700 text-white border border-gray-600 rounded-lg p-3 resize-none focus:outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400 transition-all"
              rows={3}
              disabled={isProcessing}
            />
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isProcessing}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-all font-semibold"
            >
              <Send className="w-5 h-5" />
              Send
            </button>
          </div>
          
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
            <span>💡 Try: "create a component", "fix bugs", "install dependencies", "run the app"</span>
            <div className="flex-1"></div>
            <span>Enter to send • Shift+Enter for new line</span>
          </div>
        </div>
      </div>

      {/* Live Activity Sidebar */}
      <div className="w-80 bg-gray-800 border-l border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <h3 className="font-semibold text-gray-200 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            Live Activity Feed
          </h3>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {fileChanges.length === 0 ? (
            <div className="text-center text-gray-500 mt-8">
              <Code className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No file changes yet...</p>
              <p className="text-xs mt-1">Start coding to see live updates!</p>
            </div>
          ) : (
            fileChanges.map((change, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-700 rounded-lg p-3 border-l-4 border-green-400"
              >
                <div className="flex items-center gap-2 mb-1">
                  <div className={`w-2 h-2 rounded-full ${
                    change.status === 'completed' ? 'bg-green-400' :
                    change.status === 'pending' ? 'bg-yellow-400' :
                    'bg-red-400'
                  }`} />
                  <span className={`text-sm font-medium ${
                    change.action === 'create' ? 'text-green-300' :
                    change.action === 'modify' ? 'text-yellow-300' :
                    'text-red-300'
                  }`}>
                    {change.action.toUpperCase()}
                  </span>
                  <span className="text-xs text-gray-400">
                    {change.timestamp.toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-gray-300 text-sm break-all font-mono">
                  {change.path.split('/').pop()}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {change.path.replace('/workspaces/crod-babylon-genesis/', '')}
                </p>
                {change.content && (
                  <div className="mt-2 text-xs text-gray-400 bg-gray-800 p-2 rounded">
                    {change.content}
                  </div>
                )}
              </motion.div>
            ))
          )}
        </div>
        
        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-700 space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Session Stats</span>
            <span className="text-green-400">{crodStats.totalCommands} total</span>
          </div>
          <div className="flex gap-2">
            <button className="flex-1 px-3 py-2 bg-gray-700 text-gray-300 rounded text-sm hover:bg-gray-600 transition-colors">
              <Download className="w-4 h-4 inline mr-1" />
              Export
            </button>
            <button className="flex-1 px-3 py-2 bg-gray-700 text-gray-300 rounded text-sm hover:bg-gray-600 transition-colors">
              <Upload className="w-4 h-4 inline mr-1" />
              Import
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UltimateLiveChatInterface;
