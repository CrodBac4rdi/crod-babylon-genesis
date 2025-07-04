#!/bin/bash
# 🌙 CROD OVERNIGHT TRAINING - Daniel schläft, CROD lernt!

echo "🌙 CROD OVERNIGHT TRAINING SETUP"
echo "================================"
echo "Daniel geht pennen, CROD wird schlauer!"
echo ""

# Kill any existing training processes
echo "🔧 Cleaning up old processes..."
pkill -f claude_teaches_crod.py || true
pkill -f live_crod_observer.py || true
pkill -f live_training_monitor.py || true

sleep 2

# Start everything in THIS terminal with output
echo "🚀 Starting CROD Training System..."
echo ""

# Function to show live progress
show_progress() {
    while true; do
        clear
        echo "🌙 CROD OVERNIGHT TRAINING - $(date '+%H:%M:%S')"
        echo "============================================"
        
        # Check if training is running
        if pgrep -f claude_teaches_crod.py > /dev/null; then
            echo "✅ Training Active!"
            
            # Show last 20 lines of log
            echo ""
            echo "📚 Recent Training Activity:"
            echo "----------------------------"
            tail -20 crod_training_session.log 2>/dev/null | grep -E "(Teaching CROD|Score:|✅|❌|🔥|Progress:|WOW)" || echo "Waiting for logs..."
            
            # Show database stats
            echo ""
            echo "📊 Database Stats:"
            python3 -c "
import sqlite3
conn = sqlite3.connect('crod_3d_database.db')
conversations = conn.execute('SELECT COUNT(*) FROM live_conversations').fetchone()[0]
atoms_activated = conn.execute('SELECT COUNT(*) FROM live_atom_activations').fetchone()[0]
learning_events = conn.execute('SELECT COUNT(*) FROM live_learning_events').fetchone()[0]
avg_heat = conn.execute('SELECT AVG(heat) FROM clean_universe_atoms WHERE heat > 0').fetchone()[0] or 0
print(f'   Conversations: {conversations}')
print(f'   Atoms Activated: {atoms_activated}')
print(f'   Learning Events: {learning_events}')
print(f'   Avg Atom Heat: {avg_heat:.2f}')
conn.close()
" 2>/dev/null || echo "   Database loading..."
            
        else
            echo "❌ Training stopped - restarting..."
            python3 claude_teaches_crod.py > crod_training_session.log 2>&1 &
        fi
        
        echo ""
        echo "💤 Daniel schläft... CROD lernt... 🧠"
        echo ""
        echo "Press Ctrl+C to stop training"
        
        sleep 10
    done
}

# Start the training in background
echo "🧠 Starting intelligent CROD training..."
python3 claude_teaches_crod.py > crod_training_session.log 2>&1 &
TRAINING_PID=$!

echo "✅ Training started (PID: $TRAINING_PID)"

# Start neural weight updater monitor
echo "🔄 Starting neural weight monitor..."
python3 -c "
import time
import sqlite3
from datetime import datetime

print('🧠 Neural Weight Monitor Active')
while True:
    try:
        conn = sqlite3.connect('crod_3d_database.db')
        
        # Check recent weight updates
        recent_updates = conn.execute('''
            SELECT COUNT(*) FROM live_learning_events 
            WHERE event_type = \"neural_weight_update\" 
            AND timestamp > datetime(\"now\", \"-5 minutes\")
        ''').fetchone()[0]
        
        if recent_updates > 0:
            print(f'⚡ {datetime.now().strftime(\"%H:%M:%S\")} - {recent_updates} neural updates in last 5 min')
        
        conn.close()
        time.sleep(60)
    except:
        time.sleep(60)
" > neural_monitor.log 2>&1 &

# Show live progress in THIS terminal
show_progress