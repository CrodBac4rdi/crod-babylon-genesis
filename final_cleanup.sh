#!/bin/bash

echo "🧹 FINAL CROD CLEANUP - Moving redundant stuff to alt/"
echo "===================================================="
echo ""

cd "/home/daniel/Schreibtisch/Crod Programming"

# Create alt directory if not exists
mkdir -p alt

# Move all the redundant database attempts
echo "📦 Moving redundant database attempts..."
mv -f ULTIMATE-MEGA-DATABASE alt/ 2>/dev/null && echo "  ✓ ULTIMATE-MEGA-DATABASE → alt/"
mv -f COMPLETE-CROD-UNIVERSE alt/ 2>/dev/null && echo "  ✓ COMPLETE-CROD-UNIVERSE → alt/"
mv -f FINAL-CROD-UNIVERSE alt/ 2>/dev/null && echo "  ✓ FINAL-CROD-UNIVERSE → alt/"
mv -f REALLY-COMPLETE-CROD-UNIVERSE alt/ 2>/dev/null && echo "  ✓ REALLY-COMPLETE-CROD-UNIVERSE → alt/"

# Move all the builder scripts
echo -e "\n📜 Moving old builder scripts..."
cd CROD-Helper-Member-7
mv -f build_*_database*.js ../alt/ 2>/dev/null
mv -f build_*UNIVERSE*.js ../alt/ 2>/dev/null
mv -f scan_*.js ../alt/ 2>/dev/null
echo "  ✓ All database builders → alt/"

# Move deduplication tools (we have the report)
mv -f deduplicate_*.py ../alt/ 2>/dev/null
mv -f cleanup_*.py ../alt/ 2>/dev/null
echo "  ✓ Deduplication tools → alt/"

# Move old dashboard attempts
echo -e "\n🖥️  Cleaning up dashboard directory..."
cd dashboard
rm -rf node_modules 2>/dev/null
rm -rf venv 2>/dev/null
rm -rf .kube 2>/dev/null  # K8s cache
mv -f *.html ../alt/ 2>/dev/null  # Old HTML dashboards
mv -f *-server.js ../alt/ 2>/dev/null  # Old servers
echo "  ✓ Dashboard cleaned"

cd ../..

# Move backup directory
mv -f CLEANUP-BACKUP alt/ 2>/dev/null && echo "  ✓ CLEANUP-BACKUP → alt/"

# Keep only CLEAN-CROD-UNIVERSE
echo -e "\n✅ KEEPING:"
echo "  • CLEAN-CROD-UNIVERSE (82MB - the final clean version)"
echo "  • CROD-Helper-Member-7 (working directory)"
echo "  • DEDUPLICATION_REPORT.json (analysis results)"

echo -e "\n📊 Current structure:"
echo "."
echo "├── CLEAN-CROD-UNIVERSE/     ✨ THE GOOD STUFF"
echo "├── CROD-Helper-Member-7/    💻 Working directory"
echo "├── DEDUPLICATION_REPORT.json 📊 Analysis"
echo "├── alt/                     🗄️  Old stuff (80MB+)"
echo "└── CROD-STATUS-2025-01-03.md 📄 Status doc"

# Check sizes
echo -e "\n💾 Space usage:"
du -sh CLEAN-CROD-UNIVERSE 2>/dev/null
du -sh CROD-Helper-Member-7 2>/dev/null
du -sh alt 2>/dev/null

echo -e "\n✨ Cleanup complete! Everything redundant is in alt/"