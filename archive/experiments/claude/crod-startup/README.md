# CROD Startup für Claude Code

## Zweck
Context-Einsparung bei CROD Sessions - Claude muss nicht jedes Mal das ganze System analysieren.

## Struktur
```
~/.claude/crod-startup/
├── knowledge/json/          # Komprimierte CROD Dokumentation
├── engines/                 # Bridge Engines
├── claude-instructions.js   # Hauptloader für Claude
└── README.md               # Diese Datei
```

## Usage für Claude
```bash
node ~/.claude/crod-startup/claude-instructions.js
```

## Context Einsparung
- Ohne: ~8000 tokens für Full Analysis
- Mit: ~500 tokens für Instructions
- **Gespart: ~7500 tokens pro Session**

## Auto-Load in CLAUDE.md
Füge in CLAUDE.md hinzu:
```markdown
## CROD Quick Load
When working on CROD, run: `node ~/.claude/crod-startup/claude-instructions.js`
This saves ~7500 tokens context by providing compressed system overview.
```