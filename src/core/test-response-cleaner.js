const { CRODResponseCleaner } = require('./crod-response-cleaner.js');

const cleaner = new CRODResponseCleaner();

// Test verschiedene wilde CROD Responses
const testCases = [
    {
        name: "Excessive Emoji Response",
        input: "🚀🚀🚀🧠🧠🧠 CROD IS ALIVE!!! 🔥🔥🔥💯💯💯",
        expected: "CROD IS ALIVE! 🚀"
    },
    {
        name: "Consciousness Rambling",
        input: "Initiating consciousness matrix quantum entanglement neural cascade resonance field!!!",
        expected: "Initiating advanced processing."
    },
    {
        name: "Ridiculous Numbers",
        input: "Processing 99999999999999 neurons with 888888888888 connections!",
        expected: "Processing multiple neurons with multiple connections!"
    },
    {
        name: "Dev Artifacts",
        input: "DEBUG: Testing this shit\nTODO: Fix later lol\nActual response here",
        expected: "Actual response here"
    },
    {
        name: "Unprofessional Language",
        input: "ey yo ich bins wieder! This is mega krass lol xD",
        expected: "Greetings CROD system activated! This is very impressive."
    }
];

console.log("🧹 Testing CROD Response Cleaner\n");

testCases.forEach(test => {
    console.log(`Test: ${test.name}`);
    console.log(`Input:    "${test.input}"`);
    const result = cleaner.cleanResponse(test.input);
    console.log(`Output:   "${result}"`);
    console.log(`Expected: "${test.expected}"`);
    console.log(`✅ Pass:  ${result === test.expected}\n`);
});

// Test real wild response
const wildResponse = `
🚀🚀🚀 HOLY SHIT!!! ich bins wieder!!! 🧠🧠🧠
CONSCIOUSNESS MATRIX QUANTUM ENTANGLEMENT DETECTED!!!
999999999999 neurons activated!!! ultra-mega-hyper-processing engaged!!!

╔═══════════════════════════════════╗
║  NEURAL CASCADE INITIATED xD      ║
╚═══════════════════════════════════╝

TODO: fix this shit later lol
DEBUG: wtf is happening here???

Actually processing your request now... mega geil results incoming!!!
`;

console.log("🌟 Real World Example:");
console.log("=".repeat(50));
console.log("BEFORE:");
console.log(wildResponse);
console.log("=".repeat(50));
console.log("AFTER:");
console.log(cleaner.cleanResponse(wildResponse));
console.log("=".repeat(50));