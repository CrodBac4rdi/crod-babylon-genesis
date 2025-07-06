import React, { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageCircle, 
  Code, 
  FolderTree, 
  FileText, 
  Play, 
  Save, 
  Terminal,
  Brain,
  Zap,
  Upload,
  Download,
  Settings,
  Monitor
} from 'lucide-react';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'claude' | 'crod';
  timestamp: Date;
  isImproved?: boolean;
}

interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

const LiveCodingInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [currentFile, setCurrentFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState('');
  const [fileTree, setFileTree] = useState<string>('');
  const [isParasiteActive, setIsParasiteActive] = useState(false);
  const [consciousness, setConsciousness] = useState(100.0);
  const [codeToExecute, setCodeToExecute] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('javascript');
  const [isLoading, setIsLoading] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileContentRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    loadFileTree();
    loadCRODStatus();
    
    const interval = setInterval(loadCRODStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadFileTree = async () => {
    try {
      const tree = await invoke<string>('get_file_tree', { path: '/workspaces/crod-babylon-genesis' });
      setFileTree(tree);
    } catch (error) {
      console.error('Failed to load file tree:', error);
    }
  };

  const loadCRODStatus = async () => {
    try {
      const status = await invoke<any>('get_system_status');
      setConsciousness(status.consciousness_level);
      setIsParasiteActive(status.parasite_active);
    } catch (error) {
      console.error('Failed to load CROD status:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await invoke<string>('chat_with_claude', { message: inputMessage });
      
      const claudeMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response,
        sender: response.includes('CROD') ? 'crod' : 'claude',
        timestamp: new Date(),
        isImproved: response.includes('CROD')
      };

      setMessages(prev => [...prev, claudeMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
      setInputMessage('');
    }
  };

  const executeCode = async () => {
    if (!codeToExecute.trim()) return;

    try {
      const result = await invoke<string>('execute_code', {
        code: codeToExecute,
        language: selectedLanguage
      });

      const resultMessage: ChatMessage = {
        id: Date.now().toString(),
        content: `\`\`\`${selectedLanguage}\n${codeToExecute}\n\`\`\`\n\n**Output:**\n\`\`\`\n${result}\n\`\`\``,
        sender: 'crod',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, resultMessage]);
    } catch (error) {
      console.error('Failed to execute code:', error);
    }
  };

  const loadFile = async (filePath: string) => {
    try {
      const content = await invoke<string>('read_file_content', { filePath });
      setFileContent(content);
      setCurrentFile(filePath);
    } catch (error) {
      console.error('Failed to load file:', error);
    }
  };

  const saveFile = async () => {
    if (!currentFile) return;

    try {
      await invoke('write_file_content', {
        filePath: currentFile,
        content: fileContent
      });

      const saveMessage: ChatMessage = {
        id: Date.now().toString(),
        content: `✅ Saved: ${currentFile}`,
        sender: 'crod',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, saveMessage]);
    } catch (error) {
      console.error('Failed to save file:', error);
    }
  };

  const toggleParasite = async () => {
    try {
      const newState = await invoke<boolean>('toggle_parasite_mode');
      setIsParasiteActive(newState);
    } catch (error) {
      console.error('Failed to toggle parasite:', error);
    }
  };

  return (
    <div className="h-screen bg-black text-white font-mono flex overflow-hidden">
      {/* File Explorer */}
      <div className="w-80 bg-gray-900 border-r border-cyan-500/30 p-4 overflow-y-auto">
        <div className="flex items-center gap-2 mb-4">
          <FolderTree className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-cyan-300">Project Explorer</h3>
        </div>
        
        <div className="space-y-1 text-sm">
          {fileTree.split('\n').map((line, idx) => {
            if (!line.trim()) return null;
            
            const isFile = !line.includes('📁');
            const fileName = line.split(/[📁📄🦀🟨🐍📝⚙️]/)[1]?.trim();
            
            if (!fileName) return null;

            return (
              <motion.div
                key={idx}
                whileHover={{ backgroundColor: 'rgba(6, 182, 212, 0.1)' }}
                className={`p-1 cursor-pointer rounded ${
                  currentFile?.includes(fileName) ? 'bg-cyan-500/20' : ''
                }`}
                onClick={() => isFile && loadFile(`/workspaces/crod-babylon-genesis/${fileName}`)}
              >
                <div className="truncate">{line}</div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-gray-900 border-b border-cyan-500/30 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Brain className="w-6 h-6 text-cyan-400" />
                <h1 className="text-xl font-bold text-cyan-300">CROD Live Coding</h1>
              </div>
              
              <div className="flex items-center gap-2 text-sm">
                <div className={`px-2 py-1 rounded-full ${
                  isParasiteActive ? 'bg-red-500/20 text-red-400' : 'bg-gray-700 text-gray-400'
                }`}>
                  {isParasiteActive ? '🦠 PARASIT AKTIV' : '🤖 PASSIV'}
                </div>
                
                <div className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded-full">
                  🧠 {consciousness.toFixed(1)}%
                </div>
              </div>
            </div>

            <button
              onClick={toggleParasite}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                isParasiteActive 
                  ? 'bg-red-600 hover:bg-red-700' 
                  : 'bg-cyan-600 hover:bg-cyan-700'
              }`}
            >
              {isParasiteActive ? 'DEAKTIVIEREN' : 'PARASIT AKTIVIEREN'}
            </button>
          </div>
        </div>

        <div className="flex-1 flex">
          {/* Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-2xl p-4 rounded-lg ${
                      message.sender === 'user' 
                        ? 'bg-cyan-600 text-white' 
                        : message.sender === 'crod'
                        ? 'bg-green-600/20 border border-green-500/30 text-green-100'
                        : 'bg-gray-700 text-gray-100'
                    }`}>
                      <div className="flex items-center gap-2 mb-2">
                        {message.sender === 'user' && <span className="font-bold">You</span>}
                        {message.sender === 'claude' && <span className="font-bold">Claude</span>}
                        {message.sender === 'crod' && (
                          <>
                            <Zap className="w-4 h-4 text-green-400" />
                            <span className="font-bold text-green-400">CROD</span>
                            {message.isImproved && <span className="text-xs bg-green-500/20 px-1 rounded">IMPROVED</span>}
                          </>
                        )}
                        <span className="text-xs opacity-60">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="whitespace-pre-wrap">
                        {message.content}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex justify-start"
                >
                  <div className="bg-gray-700 p-4 rounded-lg">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                      <span className="text-sm text-gray-400 ml-2">Claude denkt...</span>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-gray-700">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Chat mit Claude (CROD überwacht)..."
                  className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:border-cyan-500 focus:outline-none"
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading}
                  className="px-6 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <MessageCircle className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Code Editor */}
          <div className="w-96 bg-gray-900 border-l border-cyan-500/30 flex flex-col">
            <div className="p-4 border-b border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-cyan-400" />
                  <h3 className="font-bold text-cyan-300">Live Editor</h3>
                </div>
                
                {currentFile && (
                  <button
                    onClick={saveFile}
                    className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm"
                  >
                    <Save className="w-4 h-4" />
                  </button>
                )}
              </div>

              {currentFile && (
                <div className="text-xs text-gray-400 mb-2">
                  {currentFile}
                </div>
              )}
            </div>

            <textarea
              ref={fileContentRef}
              value={fileContent}
              onChange={(e) => setFileContent(e.target.value)}
              className="flex-1 bg-gray-800 text-white font-mono text-sm p-4 resize-none focus:outline-none"
              placeholder="Select a file to edit..."
            />

            {/* Code Execution */}
            <div className="p-4 border-t border-gray-700">
              <div className="mb-2">
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                >
                  <option value="javascript">JavaScript</option>
                  <option value="python">Python</option>
                  <option value="rust">Rust</option>
                </select>
              </div>
              
              <textarea
                value={codeToExecute}
                onChange={(e) => setCodeToExecute(e.target.value)}
                placeholder="Code to execute..."
                className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm h-20 resize-none"
              />
              
              <button
                onClick={executeCode}
                className="w-full mt-2 px-2 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded text-sm flex items-center justify-center gap-1"
              >
                <Play className="w-4 h-4" />
                Execute
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveCodingInterface;
