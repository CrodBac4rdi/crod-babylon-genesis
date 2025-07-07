# 🚀 CROD - Getting Started in 30 Seconds

## Start Everything

```bash
./start-simple.sh
```

That's it. You now have:
- 🔌 Blockchain API running on http://localhost:4000
- 🎨 Dashboard running on http://localhost:8080

## Test It Works

```bash
# Create your first block
curl -X POST http://localhost:4000/genesis

# Mine a block
curl -X POST http://localhost:4000/mine \
  -H 'Content-Type: application/json' \
  -d '{"data":{"hello":"world"}}'

# See all blocks
curl http://localhost:4000/blocks
```

## What Else?

- 📊 Open http://localhost:8080 in your browser
- 📖 Read [docs/VISUAL-GUIDE.md](docs/VISUAL-GUIDE.md) for detailed testing
- 🧪 Run `cd engines/game-theory && npm test` to test Game Theory Engine
- 🤖 Run `cd neural && node demo.js` to see Neural Network demo

## Cleanup Old Files

Too many confusing scripts? Run:
```bash
./cleanup-old-scripts.sh
```

---

**That's it!** You're running a blockchain with AI capabilities. 🎉