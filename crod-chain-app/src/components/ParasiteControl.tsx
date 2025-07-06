import React, { useState } from 'react';
import { useCRODStore } from '../store/crodStore';
import { motion } from 'framer-motion';
import { Brain, Zap, Target, Shield, AlertCircle } from 'lucide-react';

export const ParasiteControl: React.FC = () => {
  const { parasiteActive, toggleParasite, learnPattern } = useCRODStore();
  const [interceptedData, setInterceptedData] = useState<any[]>([]);
  const [learningMode, setLearningMode] = useState('passive');

  const simulateIntercept = () => {
    const fakeData = {
      timestamp: Date.now(),
      type: 'user_interaction',
      frustration: Math.random() * 100,
      satisfaction: Math.random() * 100,
      query: 'How to build a quantum computer?',
      response_quality: Math.random() * 100,
      learned_pattern: {
        user_prefers: 'detailed_explanations',
        avoid: 'vague_answers',
        tone: 'technical',
      }
    };
    
    setInterceptedData(prev => [fakeData, ...prev].slice(0, 10));
    learnPattern(fakeData.learned_pattern);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="crod-card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">CROD Parasite Control</h2>
            <p className="text-gray-400">
              Intercept and learn from User-Claude interactions
            </p>
          </div>
          
          <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
            parasiteActive ? 'bg-crod-quantum/20 text-crod-quantum' : 'bg-gray-700 text-gray-400'
          }`}>
            <Shield className="w-5 h-5" />
            <span className="font-bold">{parasiteActive ? 'ACTIVE' : 'INACTIVE'}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <button
            onClick={toggleParasite}
            className={`p-4 rounded-lg border-2 transition-all duration-300 ${
              parasiteActive 
                ? 'border-red-500 bg-red-500/10 hover:bg-red-500/20' 
                : 'border-crod-quantum bg-crod-quantum/10 hover:bg-crod-quantum/20'
            }`}
          >
            <Brain className="w-8 h-8 mb-2 mx-auto" />
            <p className="font-bold">{parasiteActive ? 'Deactivate' : 'Activate'} Parasite</p>
          </button>

          <button
            onClick={simulateIntercept}
            disabled={!parasiteActive}
            className={`p-4 rounded-lg border-2 transition-all duration-300 ${
              parasiteActive
                ? 'border-crod-primary bg-crod-primary/10 hover:bg-crod-primary/20'
                : 'border-gray-600 bg-gray-800 opacity-50 cursor-not-allowed'
            }`}
          >
            <Zap className="w-8 h-8 mb-2 mx-auto" />
            <p className="font-bold">Simulate Intercept</p>
          </button>

          <button
            onClick={() => setLearningMode(learningMode === 'passive' ? 'aggressive' : 'passive')}
            disabled={!parasiteActive}
            className={`p-4 rounded-lg border-2 transition-all duration-300 ${
              learningMode === 'aggressive'
                ? 'border-orange-500 bg-orange-500/10'
                : 'border-crod-secondary bg-crod-secondary/10'
            }`}
          >
            <Target className="w-8 h-8 mb-2 mx-auto" />
            <p className="font-bold">{learningMode.toUpperCase()} Mode</p>
          </button>
        </div>

        {!parasiteActive && (
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-500" />
            <p className="text-yellow-500">
              Parasite is inactive. Activate to start learning from interactions.
            </p>
          </div>
        )}
      </div>

      <div className="crod-card">
        <h3 className="text-xl font-bold mb-4">Intercepted Data Stream</h3>
        
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {interceptedData.length === 0 ? (
            <p className="text-gray-400 text-center py-8">
              No data intercepted yet. Activate parasite and simulate interactions.
            </p>
          ) : (
            interceptedData.map((data, index) => (
              <motion.div
                key={data.timestamp}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-crod-darker p-4 rounded-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">
                    {new Date(data.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="text-xs px-2 py-1 bg-crod-quantum/20 text-crod-quantum rounded">
                    {data.type}
                  </span>
                </div>
                
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-gray-400">Frustration</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex-1 h-2 bg-crod-darker rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-red-500"
                          style={{ width: `${data.frustration}%` }}
                        />
                      </div>
                      <span>{data.frustration.toFixed(0)}%</span>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-gray-400">Satisfaction</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex-1 h-2 bg-crod-darker rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-green-500"
                          style={{ width: `${data.satisfaction}%` }}
                        />
                      </div>
                      <span>{data.satisfaction.toFixed(0)}%</span>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-gray-400">Quality</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex-1 h-2 bg-crod-darker rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-crod-secondary"
                          style={{ width: `${data.response_quality}%` }}
                        />
                      </div>
                      <span>{data.response_quality.toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
                
                {data.learned_pattern && (
                  <div className="mt-3 text-xs bg-crod-dark p-2 rounded">
                    <p className="text-gray-400 mb-1">Learned Pattern:</p>
                    <pre className="text-crod-accent">
                      {JSON.stringify(data.learned_pattern, null, 2)}
                    </pre>
                  </div>
                )}
              </motion.div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};