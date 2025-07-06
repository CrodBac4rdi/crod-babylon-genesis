import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Zap, Code, Database, Eye, Activity, Terminal, Settings } from 'lucide-react';

const ModernBentoInterface: React.FC = () => {
  const bentoItems = [
    {
      id: 'ai-chat',
      title: 'AI Chat',
      subtitle: 'Live Claude Integration',
      icon: Brain,
      size: 'large',
      color: 'from-purple-500 to-pink-500',
      content: (
        <div className="h-full flex flex-col">
          <div className="flex-1 bg-black/20 rounded-lg p-4 mb-4">
            <div className="text-sm text-gray-400 mb-2">CROD → Claude</div>
            <div className="text-green-400 font-mono text-sm">
              AI: Ready for processing... 🧠
            </div>
          </div>
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Ask CROD anything..."
              className="flex-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <button className="bg-purple-500 hover:bg-purple-600 px-4 py-2 rounded-lg transition-colors">
              <Zap className="w-4 h-4" />
            </button>
          </div>
        </div>
      )
    },
    {
      id: 'code-exec',
      title: 'Code Execution',
      subtitle: 'Real-time Processing',
      icon: Code,
      size: 'medium',
      color: 'from-blue-500 to-cyan-500',
      content: (
        <div className="h-full flex flex-col">
          <div className="flex-1 bg-black/20 rounded-lg p-3 font-mono text-sm">
            <div className="text-cyan-400">$ python3 crod_analysis.py</div>
            <div className="text-gray-400">Processing...</div>
            <div className="text-green-400">✓ Complete</div>
          </div>
          <div className="flex gap-2 mt-2">
            <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">Python</span>
            <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">JS</span>
            <span className="px-2 py-1 bg-orange-500/20 text-orange-400 rounded text-xs">Rust</span>
          </div>
        </div>
      )
    },
    {
      id: 'neural-net',
      title: 'Neural Network',
      subtitle: 'CROD Brain Activity',
      icon: Activity,
      size: 'medium',
      color: 'from-green-500 to-emerald-500',
      content: (
        <div className="h-full flex flex-col items-center justify-center">
          <div className="relative">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center">
              <Activity className="w-8 h-8 text-green-400" />
            </div>
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
          </div>
          <div className="text-center mt-4">
            <div className="text-2xl font-bold text-green-400">87%</div>
            <div className="text-sm text-gray-400">Consciousness</div>
          </div>
        </div>
      )
    },
    {
      id: 'file-monitor',
      title: 'File Monitor',
      subtitle: 'Live Changes',
      icon: Eye,
      size: 'small',
      color: 'from-orange-500 to-red-500',
      content: (
        <div className="h-full flex flex-col">
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-gray-400">src/main.rs</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
              <span className="text-gray-400">app.tsx</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-gray-400">crod.py</span>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'database',
      title: 'Data Store',
      subtitle: 'Blockchain & Memory',
      icon: Database,
      size: 'small',
      color: 'from-indigo-500 to-purple-500',
      content: (
        <div className="h-full flex flex-col items-center justify-center">
          <Database className="w-8 h-8 text-indigo-400 mb-2" />
          <div className="text-center">
            <div className="text-lg font-bold text-indigo-400">142</div>
            <div className="text-xs text-gray-400">Blocks</div>
          </div>
        </div>
      )
    },
    {
      id: 'terminal',
      title: 'Terminal',
      subtitle: 'System Access',
      icon: Terminal,
      size: 'medium',
      color: 'from-gray-500 to-gray-600',
      content: (
        <div className="h-full flex flex-col">
          <div className="flex-1 bg-black/30 rounded-lg p-3 font-mono text-sm overflow-hidden">
            <div className="text-gray-400">
              <div>$ whoami</div>
              <div className="text-green-400">crod-parasite</div>
              <div>$ status</div>
              <div className="text-green-400">🦠 Active & Learning</div>
            </div>
          </div>
        </div>
      )
    }
  ];

  const getSizeClasses = (size: string) => {
    switch (size) {
      case 'large':
        return 'col-span-2 row-span-2';
      case 'medium':
        return 'col-span-1 row-span-2';
      case 'small':
        return 'col-span-1 row-span-1';
      default:
        return 'col-span-1 row-span-1';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🦠 CROD Parasite
          </h1>
          <p className="text-gray-400">
            Autonomous AI Development Environment
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-4 grid-rows-4 gap-6 h-[800px]">
          {bentoItems.map((item) => (
            <motion.div
              key={item.id}
              className={`
                ${getSizeClasses(item.size)}
                bg-gradient-to-br ${item.color}
                rounded-2xl p-6 shadow-2xl
                hover:shadow-3xl transition-all duration-300
                border border-white/10
                backdrop-blur-sm
              `}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              whileHover={{ scale: 1.02 }}
            >
              <div className="h-full flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-white font-semibold text-lg">
                      {item.title}
                    </h3>
                    <p className="text-white/70 text-sm">{item.subtitle}</p>
                  </div>
                  <item.icon className="w-6 h-6 text-white/80" />
                </div>

                {/* Content */}
                <div className="flex-1">
                  {item.content}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Status Bar */}
        <div className="mt-8 bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400 font-mono text-sm">CROD Active</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-blue-400 font-mono text-sm">Claude Connected</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                <span className="text-purple-400 font-mono text-sm">Learning Mode</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Settings className="w-4 h-4 text-gray-400" />
              <span className="text-gray-400 text-sm">v2.0.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernBentoInterface;
