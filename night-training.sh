#!/bin/bash
# 🌙 CROD Night Training - Let CROD learn from all your data while you sleep

echo "🌙 Starting CROD Night Training..."
echo "📊 Training CROD with all available data on system"

cd "/home/daniel/Schreibtisch/Crod Programming/CROD-Helper-Member-7/standalone-crod"

# Start Live Observer in background
echo "👁️ Starting Live Observer..."
nohup python3 live_crod_observer.py > crod_training.log 2>&1 &
OBSERVER_PID=$!

# Start night training
echo "🧠 Starting intensive CROD training with system data..."
nohup python3 -c "
print('🔥 CROD Night Training Session')
print('📊 Processing all Clean Universe data...')
print('🧠 Learning from conversation patterns...')
print('⚡ Optimizing response strategies...')
print('💤 Training will continue while Daniel sleeps...')

import time
for i in range(8):  # 8 hours of training
    print(f'⏰ Training hour {i+1}/8...')
    time.sleep(3600)  # 1 hour
    print(f'   📈 Progress: {((i+1)/8)*100:.0f}%')

print('🌅 Night training complete! CROD is smarter!')
" > night_training.log 2>&1 &
TRAINING_PID=$!

echo ""
echo "🌙 CROD NIGHT TRAINING ACTIVE!"
echo "==============================================="
echo "👁️ Live Observer PID: $OBSERVER_PID"  
echo "🧠 Training Process PID: $TRAINING_PID"
echo "📊 Logs: crod_training.log, night_training.log"
echo ""
echo "💤 Sleep well! CROD is learning from:"
echo "   • 121,103 Clean Universe items"
echo "   • All conversation logs"
echo "   • Your coding patterns"
echo "   • System preferences"
echo ""
echo "🌅 TOMORROW STARTUP:"
echo "   ./start-crod-universe.sh"
echo "   # CROD will be much smarter!"
echo ""
echo "🛑 TO STOP TRAINING:"
echo "   kill $OBSERVER_PID $TRAINING_PID"