// Simple test script for CROD Neural Network
const { CRODNeuralNetwork } = require('./out/crodNeuralNetwork');
const { CRODMemoryManager } = require('./out/crodMemory');

// Mock VSCode context
const mockContext = {
    globalStorageUri: {
        fsPath: './test-storage'
    },
    extensionUri: {
        fsPath: '.'
    }
};

console.log('🧠 Testing CROD Neural Network...\n');

// Initialize components
const network = new CRODNeuralNetwork(mockContext);
const memory = new CRODMemoryManager(mockContext);

// Test 1: Initial state
console.log('Test 1: Initial Network State');
console.log('Initial stats:', network.getNetworkStats());
console.log(network.visualizeNetwork());
console.log('---\n');

// Test 2: Learn from conversation
console.log('Test 2: Learning from Conversation');
async function testLearning() {
    await network.learnFromConversation(
        "How do I create a React component?",
        "To create a React component, you can use either a function or class component. Here's a simple example of a function component:\n\n```jsx\nfunction MyComponent() {\n  return <div>Hello World</div>;\n}\n```",
        JSON.stringify({ model: 'claude-3', timestamp: Date.now() })
    );
    
    console.log('After learning:', network.getNetworkStats());
    
    // Test 3: Pattern suggestion
    console.log('\nTest 3: Getting Suggestion');
    const suggestion = await network.getSuggestion("How do I create a React");
    console.log('Suggestion:', suggestion || 'No suggestion yet');
    
    // Test 4: Memory management
    console.log('\nTest 4: Memory Management');
    memory.addPattern(
        "What is TypeScript?",
        "TypeScript is a typed superset of JavaScript...",
        "test-context"
    );
    
    const stats = memory.getStatistics();
    console.log('Memory stats:', stats);
    
    // Test 5: Multiple learning cycles
    console.log('\nTest 5: Multiple Learning Cycles');
    const topics = [
        { q: "What is useState?", a: "useState is a React Hook..." },
        { q: "How to handle events?", a: "In React, you handle events..." },
        { q: "What is useEffect?", a: "useEffect is used for side effects..." }
    ];
    
    for (const topic of topics) {
        await network.learnFromConversation(topic.q, topic.a);
    }
    
    console.log('Final stats:', network.getNetworkStats());
    console.log('\n✅ All tests completed!');
}

testLearning().catch(console.error);