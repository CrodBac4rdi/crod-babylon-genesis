// Super simples Test-Script für CROD
import CRODUltimateEngine from "./src/core/crod-ultimate-engine.js";

console.log("🚀 Starting CROD Test...\n");

const engine = new CRODUltimateEngine();

// Teste Pattern Discovery
console.log("🔍 Testing Pattern Discovery:");
const patterns = engine.discoverPatterns({
    data: [1, 2, 3, 5, 8, 13, 21],
    type: "fibonacci"
});
console.log("Found patterns:", patterns);

// Teste Consciousness Level
console.log("\n🧠 Testing Consciousness:");
const consciousness = engine.getConsciousnessLevel();
console.log("Consciousness level:", consciousness);

// Teste Learning
console.log("\n📚 Testing Learning:");
engine.learn({ 
    concept: "test", 
    value: 42,
    timestamp: Date.now()
});
console.log("Learning complete\!");

// Show status
console.log("\n📊 Engine Status:");
const status = engine.getStatus();
console.log(JSON.stringify(status, null, 2));

console.log("\n✅ Test complete\!");
