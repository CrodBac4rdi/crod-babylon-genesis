# Sicherheitstipps für CROD

- Niemals Passwörter oder Secrets im Klartext in Code oder docker-compose.yml speichern.
- Nutze Umgebungsvariablen und .env-Dateien (siehe .env.example).
- Führe regelmäßig `npm audit`, `pip-audit`, `cargo audit` aus.
- Halte alle Abhängigkeiten aktuell.
- Nutze Linting und statische Codeanalyse für alle Sprachen.
- Überwache Logs und setze Alerts für verdächtige Aktivitäten.
- Nutze sichere Standardkonfigurationen für Datenbanken und Message-Broker.
