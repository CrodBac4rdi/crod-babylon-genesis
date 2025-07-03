/**
 * LLAMA Learning System (Kubernetes Version)
 * Adapted from original - now with Redis state and Meta-Chain integration
 */

const fs = require('fs');
const Redis = require('redis');

class LLAMALearningSystem {
  constructor(redisClient) {
    this.redis = redisClient;
    this.sessionId = Date.now();
    
    // In-memory cache
    this.cache = {
      successfulPatterns: [],
      failedPatterns: [],
      networkScores: {}
    };
    
    // Load initial state from Redis
    this.loadState();
  }
  
  async loadState() {
    try {
      const state = await this.redis.get('llama:learning:state');
      if (state) {
        const parsed = JSON.parse(state);
        this.cache = { ...this.cache, ...parsed };
      }
      
      // Load network scores
      const scores = await this.redis.hGetAll('llama:network:scores');
      if (scores) {
        this.cache.networkScores = scores;
      }
      
      console.log('🧠 LLAMA loaded previous learning state');
    } catch (error) {
      console.log('🆕 LLAMA starting fresh (no previous state)');
    }
  }
  
  async observeClaudeAction(action) {
    const observation = {
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      claudeAction: action,
      networksInvolved: this.detectNetworks(action),
      complexity: this.calculateComplexity(action),
      predictedDanielReaction: await this.predictReaction(action)
    };
    
    // Store in Redis
    await this.redis.lPush('llama:observations', JSON.stringify(observation));
    await this.redis.expire('llama:observations', 86400); // 24h TTL
    
    // Publish to Meta-Chain
    await this.redis.publish('llama:observation', JSON.stringify({
      district: 'llama-learning',
      event: 'observation',
      data: observation
    }));
    
    console.log(`👁️ LLAMA observes: ${action.type}`);
    return observation;
  }
  
  async learnFromDanielReaction(reaction, lastAction) {
    const learning = {
      action: lastAction,
      danielReaction: reaction,
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId
    };
    
    // Kategorisiere Reaktion
    if (reaction.match(/geil|nice|super|perfekt|läuft|👍|✅|🔥/i)) {
      learning.sentiment = 'POSITIVE';
      learning.score = 1.0;
      this.cache.successfulPatterns.push({
        pattern: lastAction.type,
        networks: lastAction.networks || [],
        keywords: reaction.split(' ')
      });
    } else if (reaction.match(/wtf|nein|falsch|scheisse|fuck|mist/i)) {
      learning.sentiment = 'NEGATIVE';
      learning.score = -1.0;
      this.cache.failedPatterns.push({
        pattern: lastAction.type,
        reason: 'daniel_disapproval',
        keywords: reaction.split(' ')
      });
    } else if (reaction.match(/hä|check nicht|versteh nicht|was/i)) {
      learning.sentiment = 'CONFUSED';
      learning.score = -0.5;
    } else {
      learning.sentiment = 'NEUTRAL';
      learning.score = 0.0;
    }
    
    // Update network scores
    if (lastAction.networks) {
      for (const network of lastAction.networks) {
        await this.updateNetworkScore(network, learning.score);
      }
    }
    
    // Store learning
    await this.redis.lPush('llama:learnings', JSON.stringify(learning));
    await this.redis.expire('llama:learnings', 604800); // 7d TTL
    
    // Update cache in Redis
    await this.saveState();
    
    // Notify Meta-Chain
    await this.redis.publish('llama:learning', JSON.stringify({
      district: 'llama-learning',
      event: 'learned',
      sentiment: learning.sentiment,
      score: learning.score
    }));
    
    console.log(`🧠 LLAMA learns: Daniel's reaction was ${learning.sentiment} (${learning.score})`);
    return learning;
  }
  
  async suggestAction(context) {
    console.log(`🤔 LLAMA thinking about: ${context.request}`);
    
    // Get best networks based on scores
    const bestNetworks = await this.getBestNetworks(context);
    
    // Check for similar patterns
    const confidence = await this.calculateConfidence(context);
    
    const suggestion = {
      networks: bestNetworks,
      confidence: confidence,
      reasoning: this.explainReasoning(bestNetworks, confidence),
      basedOn: {
        observations: await this.redis.lLen('llama:observations'),
        learnings: await this.redis.lLen('llama:learnings'),
        patterns: this.cache.successfulPatterns.length
      }
    };
    
    // Publish suggestion
    await this.redis.publish('llama:suggestion', JSON.stringify({
      district: 'llama-learning',
      event: 'suggestion',
      data: suggestion
    }));
    
    console.log(`💡 LLAMA suggests: ${suggestion.networks.join(', ')} (${(confidence * 100).toFixed(0)}% confident)`);
    return suggestion;
  }
  
  // Helper methods
  
  detectNetworks(action) {
    const networks = [];
    const actionStr = JSON.stringify(action).toLowerCase();
    
    const networkMap = {
      'pattern': 'pattern-district',
      'memory': 'memory-quarter',
      'intelligence': 'intelligence-hub',
      'blockchain': 'blockchain-core',
      'delta': 'delta-quarter',
      'gateway': 'gateway',
      'heat': 'meta-chain',
      'flow': 'meta-chain'
    };
    
    for (const [keyword, network] of Object.entries(networkMap)) {
      if (actionStr.includes(keyword)) {
        networks.push(network);
      }
    }
    
    return [...new Set(networks)]; // Remove duplicates
  }
  
  calculateComplexity(action) {
    let complexity = 0;
    
    if (action.code) complexity += action.code.length / 1000;
    if (action.files) complexity += action.files.length;
    if (action.dependencies) complexity += action.dependencies.length * 0.5;
    if (action.networks) complexity += action.networks.length * 0.3;
    
    return Math.min(complexity, 10);
  }
  
  async predictReaction(action) {
    // Count similar successful/failed patterns
    let positive = 0;
    let negative = 0;
    
    const actionLower = action.type.toLowerCase();
    
    this.cache.successfulPatterns.forEach(p => {
      if (p.pattern.toLowerCase().includes(actionLower) || 
          actionLower.includes(p.pattern.toLowerCase())) {
        positive++;
      }
    });
    
    this.cache.failedPatterns.forEach(p => {
      if (p.pattern.toLowerCase().includes(actionLower) || 
          actionLower.includes(p.pattern.toLowerCase())) {
        negative++;
      }
    });
    
    if (positive + negative === 0) {
      return { prediction: 'UNKNOWN', confidence: 0 };
    }
    
    const confidence = Math.abs(positive - negative) / (positive + negative);
    
    if (positive > negative) {
      return { prediction: 'POSITIVE', confidence };
    } else {
      return { prediction: 'NEGATIVE', confidence };
    }
  }
  
  async updateNetworkScore(network, score) {
    const current = parseFloat(await this.redis.hGet('llama:network:scores', network) || 0);
    const updated = current + score;
    await this.redis.hSet('llama:network:scores', network, updated.toString());
    this.cache.networkScores[network] = updated;
  }
  
  async getBestNetworks(context) {
    const scores = await this.redis.hGetAll('llama:network:scores');
    
    // Sort by score
    const sorted = Object.entries(scores)
      .map(([network, score]) => ({ network, score: parseFloat(score) }))
      .sort((a, b) => b.score - a.score)
      .filter(item => item.score > 0);
    
    // Return top 3 or defaults
    if (sorted.length > 0) {
      return sorted.slice(0, 3).map(item => item.network);
    }
    
    // Default suggestions
    return ['pattern-district', 'memory-quarter', 'meta-chain'];
  }
  
  async calculateConfidence(context) {
    const observations = await this.redis.lLen('llama:observations');
    const learnings = await this.redis.lLen('llama:learnings');
    
    // Base confidence on amount of data
    const dataConfidence = Math.min((observations + learnings) / 100, 0.5);
    
    // Add pattern matching confidence
    const contextLower = context.request.toLowerCase();
    let patternMatches = 0;
    
    this.cache.successfulPatterns.forEach(p => {
      if (contextLower.includes(p.pattern.toLowerCase())) {
        patternMatches++;
      }
    });
    
    const patternConfidence = Math.min(patternMatches / 10, 0.5);
    
    return dataConfidence + patternConfidence;
  }
  
  explainReasoning(networks, confidence) {
    const parts = [];
    
    if (confidence > 0.7) {
      parts.push('High confidence based on previous successes');
    } else if (confidence > 0.4) {
      parts.push('Moderate confidence from limited data');
    } else {
      parts.push('Low confidence - still learning');
    }
    
    if (networks.length > 0) {
      parts.push(`Selected ${networks[0]} as primary district`);
    }
    
    if (this.cache.successfulPatterns.length > 10) {
      parts.push(`Learned from ${this.cache.successfulPatterns.length} successful patterns`);
    }
    
    return parts.join('. ');
  }
  
  async saveState() {
    await this.redis.set('llama:learning:state', JSON.stringify({
      successfulPatterns: this.cache.successfulPatterns.slice(-100), // Keep last 100
      failedPatterns: this.cache.failedPatterns.slice(-50), // Keep last 50
      lastUpdate: new Date().toISOString()
    }));
  }
}

module.exports = LLAMALearningSystem;