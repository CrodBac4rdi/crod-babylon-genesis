# CROD Phoenix Polyglot

Ein moderner, flacher Polyglot-Stack für echte KI, ML und verteilte Systeme.

## Struktur

- `crod-phoenix/` – Elixir/Phoenix Orchestrator
- `polyglot/` – Polyglotte Module (Python, Rust, Go, JS, etc.)
- `programme/` – Alle CROD-Programme, jeweils in eigenem Unterordner
- `docs/phoenix-polyglot-docs/` – Visuals, Architekturdiagramme, Doku

## Visuals

![Polyglot City](docs/phoenix-polyglot-docs/polyglot-city-architecture.svg)

![System Overview](docs/phoenix-polyglot-docs/architecture-overview.svg)

## Quickstart

```bash
cd crod-phoenix
mix phx.server
# oder
cd polyglot/python && python main.py
```

## Weitere Infos

- ER-Diagramme: `polyglot/markdown/erdiagram_*.md`
- Technische Übersichten: `polyglot/markdown/architecture-overview.md`

---

**Hinweis:**
Alle Elixir- und Polyglot-Quellen sind jetzt übersichtlich in einem gemeinsamen Ordner. Die wichtigsten Visuals und Doku sind direkt im README und in `docs/` eingebunden.
