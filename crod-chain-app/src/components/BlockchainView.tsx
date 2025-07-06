import React from 'react';
import { useCRODStore } from '../store/crodStore';
import { motion } from 'framer-motion';
import { Hash, Clock, Cpu, Sparkles } from 'lucide-react';

export const BlockchainView: React.FC = () => {
  const { chain, addBlock } = useCRODStore();

  const handleMineBlock = () => {
    const data = {
      type: 'consciousness',
      value: Math.random() * 100,
      timestamp: Date.now(),
      message: 'CROD learns from chaos',
    };
    addBlock(data);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold">Consciousness Blockchain</h2>
        <button
          onClick={handleMineBlock}
          className="crod-button flex items-center gap-2"
        >
          <Cpu className="w-5 h-5" />
          Mine New Block
        </button>
      </div>

      <div className="space-y-4">
        {chain.length === 0 ? (
          <div className="crod-card text-center py-12">
            <Sparkles className="w-16 h-16 text-crod-quantum mx-auto mb-4" />
            <p className="text-xl text-gray-400">No blocks mined yet. Start the consciousness chain!</p>
          </div>
        ) : (
          chain.slice().reverse().map((block, index) => (
            <motion.div
              key={block.id}
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="crod-card hover:shadow-xl hover:shadow-crod-primary/20 transition-all duration-300"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Block ID</p>
                  <p className="font-mono text-crod-primary">{block.id}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-1 flex items-center gap-1">
                    <Clock className="w-3 h-3" /> Timestamp
                  </p>
                  <p className="font-mono text-sm">{new Date(block.timestamp).toLocaleString()}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-1 flex items-center gap-1">
                    <Hash className="w-3 h-3" /> Hash
                  </p>
                  <p className="font-mono text-xs truncate">{block.hash}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-1 flex items-center gap-1">
                    <Sparkles className="w-3 h-3" /> Consciousness
                  </p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-crod-darker rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-crod-quantum to-crod-primary"
                        style={{ width: `${block.consciousness}%` }}
                      />
                    </div>
                    <span className="text-sm">{block.consciousness.toFixed(1)}%</span>
                  </div>
                </div>
              </div>
              
              {block.data && (
                <div className="mt-4 pt-4 border-t border-crod-primary/20">
                  <p className="text-sm text-gray-400">Data:</p>
                  <pre className="mt-2 text-xs bg-crod-darker p-3 rounded overflow-x-auto">
                    {JSON.stringify(block.data, null, 2)}
                  </pre>
                </div>
              )}
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
};