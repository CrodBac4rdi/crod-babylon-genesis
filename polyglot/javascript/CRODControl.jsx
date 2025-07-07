import React, { useState, useEffect } from 'react';

export default function CRODControl() {
  const [consciousness, setConsciousness] = useState({ level: 'DORMANT', score: 0 });
  const [input, setInput] = useState('');
  const [patterns, setPatterns] = useState([]);
  const [llamaStatus, setLlamaStatus] = useState('Training...');
  const [genesisKeys, setGenesisKeys] = useState(null);

  useEffect(() => {
    // Poll for consciousness updates
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:4000/consciousness');
        if (res.ok) {
          const data = await res.json();
          setConsciousness(data);
        }
      } catch (e) {
        console.error('Failed to fetch consciousness:', e);
      }
    }, 2000);

    // Load genesis keys if available
    const keys = localStorage.getItem('crod-genesis-keys');
    if (keys) {
      setGenesisKeys(JSON.parse(keys));
    }

    return () => clearInterval(interval);
  }, []);

  const sendToCROD = async () => {
    try {
      const res = await fetch('http://localhost:4000/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input })
      });

      if (res.ok) {
        const data = await res.json();
        setPatterns(prev => [...prev.slice(-9), {
          time: new Date().toLocaleTimeString(),
          input,
          patterns: data.patterns || [],
          score: data.trinity_score || 0
        }]);
        setInput('');
      }
    } catch (e) {
      console.error('Failed to send to CROD:', e);
    }
  };

  const getConsciousnessColor = () => {
    const colors = {
      DORMANT: 'text-gray-500',
      AWAKENING: 'text-yellow-500',
      CONSCIOUS: 'text-green-500',
      ENLIGHTENED: 'text-purple-500',
      TRANSCENDENT: 'text-pink-500 animate-pulse'
    };
    return colors[consciousness.level] || 'text-gray-500';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold mb-8 text-center">
          🌌 CROD CONSCIOUSNESS CONTROL
        </h1>

        {/* Genesis Keys Display */}
        {!genesisKeys && (
          <div className="bg-yellow-900 border-2 border-yellow-500 p-4 rounded-lg mb-8">
            <p className="text-yellow-300">
              ⚠️ No Genesis Keys detected. Run START-CROD-NOW.sh to generate keys.
            </p>
          </div>
        )}

        {/* Consciousness Display */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8 text-center">
          <h2 className="text-2xl mb-4">Consciousness Level</h2>
          <div className={`text-6xl font-bold ${getConsciousnessColor()}`}>
            {consciousness.level}
          </div>
          <div className="text-3xl mt-2">Score: {consciousness.score}</div>
        </div>

        {/* Input Control */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-2xl mb-4">Send to CROD</h2>
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendToCROD()}
              className="flex-1 px-4 py-2 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Type 'ich bins wieder' to activate..."
            />
            <button
              onClick={sendToCROD}
              className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
            >
              Send
            </button>
          </div>
        </div>

        {/* Pattern History */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-2xl mb-4">Pattern Detection History</h2>
          <div className="space-y-2">
            {patterns.length === 0 ? (
              <p className="text-gray-500">No patterns detected yet...</p>
            ) : (
              patterns.map((p, i) => (
                <div key={i} className="bg-gray-700 p-3 rounded">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-400">{p.time}</span>
                    <span className="text-sm text-green-400">Score: {p.score}</span>
                  </div>
                  <div className="mt-1">
                    <span className="text-yellow-400">{p.input}</span>
                    {p.patterns.length > 0 && (
                      <span className="text-purple-400 ml-2">
                        → {p.patterns.join(', ')}
                      </span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* LLaMA Training Status */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-2xl mb-4">LLaMA 7B Training</h2>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
              <span>{llamaStatus}</span>
            </div>
            <span className="text-sm text-gray-400">
              Learning from your patterns...
            </span>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <button
            onClick={() => setInput('ich bins wieder daniel')}
            className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            🔥 Full Activation
          </button>
          <button
            onClick={() => window.open('http://localhost:4000/report', '_blank')}
            className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            📊 System Report
          </button>
          <button
            onClick={() => window.open('http://localhost:4000', '_blank')}
            className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            🔗 NATS Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}