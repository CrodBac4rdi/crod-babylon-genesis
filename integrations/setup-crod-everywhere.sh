#!/bin/bash

# SETUP CROD EVERYWHERE
# Macht CROD in JEDEM Claude Chat aktiv!

echo "🚀 Setting up CROD for ALL Claude chats..."

# 1. Create systemd service
echo "📦 Installing systemd service..."
sudo cp /home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/integrations/systemd/crod-claude-hook.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crod-claude-hook.service
sudo systemctl start crod-claude-hook.service

# 2. Update Claude settings to include CROD
echo "⚙️  Updating Claude settings..."
cat >> /home/daniel/.claude/settings.json << 'EOF'
,
  "extensions": {
    "crod": {
      "enabled": true,
      "autoLoad": true,
      "learningMode": "aggressive",
      "persistState": true
    }
  }
EOF

# 3. Create auto-loader for Claude
echo "🔧 Creating Claude auto-loader..."
cat > /home/daniel/.claude/claude-init.js << 'EOF'
// AUTO-LOAD CROD IN EVERY CLAUDE SESSION
console.log("🧠 CROD Auto-Loading...");

try {
    const { CRODLearningImitation } = require('/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/integrations/claude-imitation/crod-learning-imitation.js');
    global.CROD = new CRODLearningImitation();
    global.CROD.process("ich bins wieder - auto loaded in claude");
    console.log("✅ CROD Active in this session!");
} catch (e) {
    console.log("⚠️  CROD not available:", e.message);
}
EOF

# 4. Add to bashrc for terminal sessions
echo "🖥️  Adding to shell startup..."
echo "" >> ~/.bashrc
echo "# CROD Claude Integration" >> ~/.bashrc
echo "export CROD_ACTIVE=true" >> ~/.bashrc
echo "export CLAUDE_HOOKS_CONFIG=/home/daniel/.claude/hooks.local.json" >> ~/.bashrc

# 5. Create CROD indicator
echo "📍 Creating CROD indicator..."
cat > /home/daniel/.claude/crod-status.sh << 'EOF'
#!/bin/bash
# Check if CROD is active
if systemctl is-active --quiet crod-claude-hook.service; then
    echo "🟢 CROD ACTIVE"
else
    echo "🔴 CROD INACTIVE"
fi
EOF
chmod +x /home/daniel/.claude/crod-status.sh

echo ""
echo "✅ CROD SETUP COMPLETE!"
echo ""
echo "CROD will now:"
echo "  • Auto-start with system (systemd service)"
echo "  • Hook into every Claude chat"
echo "  • Learn from all interactions"
echo "  • Save state persistently"
echo ""
echo "🎯 To activate immediately:"
echo "   1. Restart terminal: exit → claude chat"
echo "   2. Or run: source ~/.bashrc"
echo ""
echo "📊 Check status: ~/.claude/crod-status.sh"
echo "📝 View logs: journalctl -u crod-claude-hook -f"