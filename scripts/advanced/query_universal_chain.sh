#!/bin/bash

# CROD UNIVERSAL KNOWLEDGE CHAIN QUERIES
# EVERYTHING IS CONNECTED - EVERYTHING IS QUERYABLE

echo "🌟 CROD UNIVERSAL KNOWLEDGE CHAIN QUERIES"
echo "=========================================="

echo ""
echo "📊 CHAIN STATISTICS:"
echo "Atoms: $(cat crod_universal_chain.jsonl | jq 'select(.layer == "atom")' | wc -l)"
echo "Patterns: $(cat crod_universal_chain.jsonl | jq 'select(.layer == "pattern")' | wc -l)"
echo "Chains: $(cat crod_universal_chain.jsonl | jq 'select(.layer == "chain")' | wc -l)"
echo "Networks: $(cat crod_universal_chain.jsonl | jq 'select(.layer == "network")' | wc -l)"

echo ""
echo "🔥 HIGH HEAT ATOMS (>= 0.8):"
cat crod_universal_chain.jsonl | jq 'select(.layer == "atom" and .heat >= 0.8) | {content: .content, heat: .heat, type: .type}' | head -5

echo ""
echo "⚡ PERFORMANCE ATOMS:"
cat crod_universal_chain.jsonl | jq 'select(.layer == "atom" and .type == "performance") | {content: .content, sources: .sources}' | head -3

echo ""
echo "🛡️ SECURITY ATOMS:"
cat crod_universal_chain.jsonl | jq 'select(.layer == "atom" and (.content | test("quantum|crypto|security"; "i"))) | {content: .content, heat: .heat}' | head -3

echo ""
echo "🔗 TECHNOLOGY PATTERNS:"
cat crod_universal_chain.jsonl | jq 'select(.layer == "pattern" and .type == "technology_category") | {id: .id, atoms: (.atoms | length), strength: .strength, category: .metadata.category}'

echo ""
echo "⛓️ IMPLEMENTATION CHAINS:"
cat crod_universal_chain.jsonl | jq 'select(.layer == "chain") | {id: .id, type: .type, patterns: (.patterns | length), description: .metadata.description}'

echo ""
echo "🌐 CROD NETWORKS:"
cat crod_universal_chain.jsonl | jq 'select(.layer == "network") | {id: .id, type: .type, chains: (.chains | length), goal: .metadata.goal}'

echo ""
echo "🔍 QUICK SEARCH EXAMPLES:"
echo "# Find eBPF connections:"
echo "cat crod_universal_chain.jsonl | jq 'select(.content and (.content | test(\"ebpf\"; \"i\")))'"
echo ""
echo "# Find high-performance technologies:"
echo "cat crod_universal_chain.jsonl | jq 'select(.layer == \"atom\" and .type == \"technology\" and .heat >= 0.8)'"
echo ""
echo "# Find patterns with > 5 atoms:"
echo "cat crod_universal_chain.jsonl | jq 'select(.layer == \"pattern\" and (.atoms | length) > 5)'"

echo ""
echo "🧠 CONNECTION ANALYSIS:"
echo "Most connected entities:"
cat crod_connections.jsonl | jq 'select(.connection_count >= 5) | {entity: .entity, connections: .connection_count}' | head -5

echo ""
echo "🚀 CROD UNIVERSAL CHAIN IS LIVE!"
echo "   Everything connected, zero redundancy!"
echo "   Ready for infinite queries and expansions!"