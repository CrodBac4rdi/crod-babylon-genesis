// MEMORY UPDATER - Quick Updates für Session Memory
// Usage: node memory-updater.js "action" "description"

const ClaudeInstructor = require('./claude-instructions.js');

async function updateMemory() {
    const instructor = new ClaudeInstructor();
    
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log(`
🧠 MEMORY UPDATER USAGE:
========================

node memory-updater.js "last_action" "What just happened"
node memory-updater.js "implementation" "New feature implemented"
node memory-updater.js "next" "step1,step2,step3"

Examples:
node memory-updater.js "last_action" "Started docker-compose successfully"
node memory-updater.js "implementation" "Neural Genesis Block completed"
node memory-updater.js "next" "Test quantum entanglement,Fix pattern bugs"
`);
        return;
    }
    
    const [type, description] = args;
    const updates = {};
    
    switch (type) {
        case 'last_action':
        case 'action':
            updates.last_action = description;
            break;
            
        case 'implementation':
        case 'impl':
            updates.recent_implementation = description;
            break;
            
        case 'next':
        case 'steps':
            updates.next_steps = description.split(',').map(s => s.trim());
            break;
            
        default:
            console.log('❌ Unknown type. Use: last_action, implementation, or next');
            return;
    }
    
    await instructor.updateSessionMemory(updates);
    
    console.log('✅ Memory updated:', updates);
    console.log('\n📋 Quick reload command:');
    console.log('node ~/.claude/crod-startup/claude-instructions.js');
}

updateMemory().catch(console.error);