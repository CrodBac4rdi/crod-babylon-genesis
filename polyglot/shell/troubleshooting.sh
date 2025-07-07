#!/bin/bash
# 🔧 CROD Codespace Troubleshooting Script

echo "🔧 CROD Codespace Troubleshooting"
echo "================================="

# Check system
echo ""
echo "📊 System Info:"
echo "- OS: $(cat /etc/os-release | grep PRETTY_NAME)"
echo "- Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "- CPU: $(nproc) cores"
echo "- Disk: $(df -h / | tail -1 | awk '{print $4}' ) free"

# Check installations
echo ""
echo "🔍 Checking installations..."

check_command() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1: $(which $1)"
        if [ "$2" ]; then
            echo "   Version: $($2)"
        fi
    else
        echo "❌ $1: NOT FOUND"
    fi
}

# Languages
echo ""
echo "💻 Programming Languages:"
check_command python "python --version"
check_command node "node --version"
check_command rustc "rustc --version"
check_command go "go version"
check_command elixir "elixir --version"
check_command dotnet "dotnet --version"
check_command java "java --version 2>&1 | head -1"
check_command ruby "ruby --version"

# Tools
echo ""
echo "🛠️ Development Tools:"
check_command docker "docker --version"
check_command kubectl "kubectl version --client --short"
check_command helm "helm version --short"
check_command git "git --version"
check_command claude "claude --version 2>&1 | head -1"
check_command ollama "ollama --version"

# Services
echo ""
echo "🔄 Services Status:"
systemctl is-active --quiet docker && echo "✅ Docker: running" || echo "❌ Docker: not running"
systemctl is-active --quiet k3s && echo "✅ K3s: running" || echo "❌ K3s: not running"
pgrep redis-server > /dev/null && echo "✅ Redis: running" || echo "❌ Redis: not running"
pgrep postgres > /dev/null && echo "✅ PostgreSQL: running" || echo "❌ PostgreSQL: not running"

# Network
echo ""
echo "🌐 Network Check:"
curl -s -o /dev/null -w "✅ Internet: OK (Google: %{http_code})\n" https://google.com || echo "❌ Internet: FAILED"
nc -zv localhost 6379 2>&1 | grep -q succeeded && echo "✅ Redis port 6379: open" || echo "❌ Redis port 6379: closed"
nc -zv localhost 5432 2>&1 | grep -q succeeded && echo "✅ PostgreSQL port 5432: open" || echo "❌ PostgreSQL port 5432: closed"

# CROD specific
echo ""
echo "🧠 CROD Status:"
if [ -f ~/.claude/claude_config.json ]; then
    echo "✅ Claude config: found"
else
    echo "❌ Claude config: missing"
fi

if [ -d /workspace/training/knowledge ]; then
    pattern_count=$(find /workspace/training/knowledge -name "crod-patterns-*.json" | wc -l)
    echo "✅ CROD patterns: $pattern_count files found"
else
    echo "❌ CROD patterns: directory missing"
fi

# Common fixes
echo ""
echo "🔨 Common Fixes:"
echo "- Docker not running: sudo systemctl start docker"
echo "- K3s not running: sudo systemctl start k3s"
echo "- Claude not found: Check .devcontainer/setup.sh ran"
echo "- Missing tools: Run .devcontainer/setup.sh manually"

echo ""
echo "🔥 ich bins wieder - Ready to debug!"