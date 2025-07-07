import React, { useState, useEffect } from 'react';
import './App.css';

// Creative Modules
import GameCreator from './components/GameCreator';
import ThreeDStudio from './components/ThreeDStudio';
import StoryGenerator from './components/StoryGenerator';
import MediaProcessor from './components/MediaProcessor';
import InnovationDashboard from './components/InnovationDashboard';
import ReviewSystem from './components/ReviewSystem';

interface Creation {
  id: string;
  type: 'game' | '3d' | 'story' | 'media' | 'other';
  title: string;
  data: any;
  innovationScore?: number;
  reviews: Review[];
  blockHash?: string;
}

interface Review {
  id: string;
  rating: number;
  comment: string;
  tags: string[];
  timestamp: number;
}

function App() {
  const [activeModule, setActiveModule] = useState<string>('dashboard');
  const [creations, setCreations] = useState<Creation[]>([]);
  const [networkEfficiency, setNetworkEfficiency] = useState<number>(1.0);
  const [minedBlocks, setMinedBlocks] = useState<number>(0);
  const [currentCreation, setCurrentCreation] = useState<Creation | null>(null);

  useEffect(() => {
    // Connect to CROD Brain
    connectToBrain();
    
    // Subscribe to innovation events
    subscribeToInnovations();
  }, []);

  const connectToBrain = async () => {
    try {
      const response = await fetch('http://localhost:4000/status');
      const data = await response.json();
      console.log('Connected to CROD Brain:', data);
    } catch (error) {
      console.error('Failed to connect to CROD Brain:', error);
    }
  };

  const subscribeToInnovations = () => {
    const eventSource = new EventSource('http://localhost:4000/innovations/stream');
    
    eventSource.onmessage = (event) => {
      const innovation = JSON.parse(event.data);
      console.log('New innovation:', innovation);
      
      if (innovation.type === 'new_block') {
        setMinedBlocks(prev => prev + 1);
        setNetworkEfficiency(innovation.efficiency);
      }
    };
  };

  const submitCreation = async (creation: Omit<Creation, 'id' | 'reviews'>) => {
    try {
      const response = await fetch('http://localhost:4000/creations/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(creation)
      });
      
      const result = await response.json();
      
      if (result.status === 'mined') {
        // Innovation was unique enough to mine a new block!
        alert(`🎉 Innovation mined! Score: ${result.innovationScore}, Reward: ${result.reward}`);
        setCreations(prev => [...prev, { ...creation, id: result.id, reviews: [], blockHash: result.blockHash }]);
      } else {
        // Not innovative enough
        alert(`Creation rejected: ${result.reason}`);
      }
    } catch (error) {
      console.error('Failed to submit creation:', error);
    }
  };

  const addReview = async (creationId: string, review: Omit<Review, 'id' | 'timestamp'>) => {
    try {
      const response = await fetch(`http://localhost:4000/creations/${creationId}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(review)
      });
      
      const result = await response.json();
      console.log('Review added:', result);
      
      // Update local state
      setCreations(prev => prev.map(c => 
        c.id === creationId 
          ? { ...c, reviews: [...c.reviews, { ...review, id: result.id, timestamp: Date.now() }] }
          : c
      ));
    } catch (error) {
      console.error('Failed to add review:', error);
    }
  };

  const renderModule = () => {
    switch (activeModule) {
      case 'dashboard':
        return <InnovationDashboard 
          creations={creations}
          networkEfficiency={networkEfficiency}
          minedBlocks={minedBlocks}
        />;
      
      case 'game':
        return <GameCreator onSubmit={submitCreation} />;
      
      case '3d':
        return <ThreeDStudio onSubmit={submitCreation} />;
      
      case 'story':
        return <StoryGenerator onSubmit={submitCreation} />;
      
      case 'media':
        return <MediaProcessor onSubmit={submitCreation} />;
      
      case 'review':
        return <ReviewSystem 
          creations={creations}
          onReview={addReview}
        />;
      
      default:
        return <div>Select a module</div>;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔥 CROD ULTIMATIV CREATIVE SUITE 🔥</h1>
        <div className="stats">
          <span>Network Efficiency: {(networkEfficiency * 100).toFixed(2)}%</span>
          <span>Mined Blocks: {minedBlocks}</span>
          <span>Creations: {creations.length}</span>
        </div>
      </header>
      
      <nav className="app-nav">
        <button 
          className={activeModule === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveModule('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={activeModule === 'game' ? 'active' : ''}
          onClick={() => setActiveModule('game')}
        >
          🎮 Game Creator
        </button>
        <button 
          className={activeModule === '3d' ? 'active' : ''}
          onClick={() => setActiveModule('3d')}
        >
          🎨 3D Studio
        </button>
        <button 
          className={activeModule === 'story' ? 'active' : ''}
          onClick={() => setActiveModule('story')}
        >
          📖 Story Generator
        </button>
        <button 
          className={activeModule === 'media' ? 'active' : ''}
          onClick={() => setActiveModule('media')}
        >
          🎬 Media Processor
        </button>
        <button 
          className={activeModule === 'review' ? 'active' : ''}
          onClick={() => setActiveModule('review')}
        >
          ⭐ Review System
        </button>
      </nav>
      
      <main className="app-main">
        {renderModule()}
      </main>
      
      <footer className="app-footer">
        <p>Everything is Blockchain. Every creation is a potential innovation.</p>
      </footer>
    </div>
  );
}

export default App;