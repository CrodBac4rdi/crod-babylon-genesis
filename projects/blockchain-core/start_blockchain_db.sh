#!/bin/bash

echo "🚀 Starting CROD Blockchain with PostgreSQL"
echo "========================================="

# Start Postgres if not running
if ! docker ps | grep -q crod-postgres-new; then
    echo "📦 Starting PostgreSQL..."
    docker run -d --name crod-postgres-new \
        -e POSTGRES_USER=crod \
        -e POSTGRES_PASSWORD=crod2025 \
        -e POSTGRES_DB=crod_blockchain \
        -p 5433:5432 \
        postgres:15-alpine
    
    echo "⏳ Waiting for PostgreSQL to start..."
    sleep 10
fi

# Start blockchain
echo "🔗 Starting Blockchain with DB..."
docker run --rm -d --name crod-blockchain-db \
    --network host \
    -v $(pwd):/app \
    -w /app \
    -e DB_HOST=localhost \
    -e DB_PORT=5433 \
    elixir:1.15 \
    elixir blockchain_with_db.ex

echo "⏳ Waiting for blockchain to start..."
sleep 20

echo ""
echo "✅ Blockchain with DB is running!"
echo ""
echo "🌐 Access Points:"
echo "  - API: http://localhost:8001"
echo "  - PgAdmin: http://localhost:5050 (if started)"
echo ""
echo "🔧 Test Commands:"
echo "  - View stats: curl http://localhost:8001/stats | jq ."
echo "  - View blocks: curl http://localhost:8001/blocks | jq ."
echo "  - Add transaction: curl -X POST http://localhost:8001/transaction/new -H 'Content-Type: application/json' -d '{\"from\":\"test\",\"to\":\"crod\",\"amount\":50}'"
echo "  - Mine block: curl -X POST http://localhost:8001/mine"
echo ""
echo "📊 Database access:"
echo "  psql -h localhost -p 5433 -U crod -d crod_blockchain"
echo "  Password: crod2025"