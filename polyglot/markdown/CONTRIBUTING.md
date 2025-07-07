# Beitrag zu CROD

Danke, dass du zu CROD beitragen möchtest!

## Wie du beitragen kannst

- Fehler melden: Erstelle ein Issue mit einer klaren Beschreibung und ggf. Schritten zur Reproduktion.
- Feature-Requests: Beschreibe neue Ideen als Issue, idealerweise mit Use-Case.
- Code beitragen: Forke das Repo, erstelle einen Feature- oder Bugfix-Branch (`feature/<name>`, `bugfix/<name>`), mache einen Pull Request.

## Entwicklungs-Setup

- Lies die README.md für den Schnellstart.
- Nutze die vorhandenen Docker- und Compose-Dateien (`docker-compose up`).
- Frontend: `cd crod-gui && npm install && npm run dev`
- Backend: Siehe `blockchain/` (Elixir, Python, Rust) und `crod-core/`
- .env-Dateien: Kopiere `.env.example` zu `.env` und passe sie an.

## Code-Richtlinien

- Schreibe Tests für neue Features und Bugfixes (Unit, Integration, ggf. End-to-End).
- Halte dich an Linting/Formatierung (siehe unten).
- Dokumentiere öffentliche Funktionen, APIs und Schnittstellen.
- Schreibe sprechende Commits (z.B. `feat: neues Konsensprotokoll`, `fix: Race Condition im Mining`).
- Nutze Pull Requests für alle Änderungen am Haupt-Repo.

## Linting & Formatierung

- Frontend: `npx eslint .` und `npx prettier --check .`
- Python: `black . && flake8 .`
- Rust: `cargo fmt && cargo clippy`
- Elixir: `mix format && mix credo`

## Tests

- Frontend: `npm test` (Jest/React Testing Library empfohlen)
- Backend:
  - Python: `pytest`
  - Elixir: `mix test`
  - Rust: `cargo test`
- Schreibe Tests für alle neuen Features und Bugfixes.

## Security

- Niemals Passwörter oder Secrets im Klartext commiten.
- Nutze `.env`-Dateien und Umgebungsvariablen (siehe `.env.example`).
- Führe regelmäßig `npm audit`, `pip-audit`, `cargo audit` aus.

## Pull Requests

- Beschreibe, was du geändert hast und warum.
- Verweise auf Issues, falls relevant (`closes #123`).
- Stelle sicher, dass alle Linter und Tests erfolgreich laufen.
- Mindestens ein Review von einer anderen Person erforderlich.

## Weiterführende Links

- [README.md](./README.md)
- [API-EXAMPLES.md](./API-EXAMPLES.md)
- [INTERFACES.md](./INTERFACES.md)
- [SECURITY-TIPS.md](./SECURITY-TIPS.md)
