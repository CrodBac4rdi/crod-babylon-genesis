#!/bin/bash

# CROD Research Query Examples
# Use these to query the research database

echo "🔍 CROD RESEARCH QUERY EXAMPLES"
echo "================================"

echo ""
echo "📊 High Impact, Low Effort Technologies:"
cat research_consolidated.jsonl | jq 'select(.type == "implementation_priority" and .effort == "low" and .impact == "high")'

echo ""
echo "⚠️ Critical Security Requirements:"
cat research_consolidated.jsonl | jq 'select(.urgency == "critical" or .type == "security_requirement")'

echo ""
echo "🚀 Performance Benchmarks > 1M ops/sec:"
cat research_consolidated.jsonl | jq 'select(.type == "performance_benchmark" and .value > 1000000)'

echo ""
echo "💰 Free Performance Gains:"
cat research_consolidated.jsonl | jq 'select(.type == "cost_analysis" and .category == "free_performance_gains")'

echo ""
echo "🌐 Browser Technologies:"
cat research_consolidated.jsonl | jq 'select(.type == "browser_capability")'

echo ""
echo "⏰ Technologies Available Q3 2025:"
cat research_consolidated.jsonl | jq 'select(.availability == "Q3 2025" or (.data.availability? // empty) == "Q3 2025")'

echo ""
echo "🏗️ Architecture Patterns:"
cat research_consolidated.jsonl | jq 'select(.type == "architecture_pattern")'

echo ""
echo "📈 Market Trends:"
cat research_consolidated.jsonl | jq 'select(.type == "market_trend")'

echo ""
echo "🛒 Vendor Products under $3k:"
cat research_consolidated.jsonl | jq 'select(.type == "vendor_product" and (.price_range | test("\\$[0-9]+-[0-2][0-9][0-9][0-9]")))'

echo ""
echo "⚡ CROD Current vs Future Gap:"
cat research_consolidated.jsonl | jq 'select(.type == "crod_current_state")'