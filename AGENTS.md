# AGENTS.md

Die Regeln für Agenten in diesem Repo stehen in **[CLAUDE.md](CLAUDE.md)** — lies sie vollständig,
bevor du etwas tust. Sie gelten für jeden Agenten (Codex, Cursor, Copilot, Gemini …), nicht nur
für Claude. Details zu Typ-Taxonomie und Frontmatter: [CONTRIBUTING.md](CONTRIBUTING.md).

Diese Datei ist bewusst nur ein Verweis, damit es eine einzige gepflegte Regelquelle gibt.
Regeln nie hier ergänzen, sondern in CLAUDE.md.

## Einrichtung: ein Brain für mehrere Agenten

*Anleitung für Menschen, keine Regel für die Arbeit im Repo.*

Das Brain ist ein einziger Markdown-Ordner. Jeder Agent bekommt nur einen **Verweis** darauf,
nie eine eigene Kopie. So bleibt die Wissensbasis eine einzige Quelle, egal welches Werkzeug
gerade arbeitet.

Diese `AGENTS.md` wirkt nur, wenn der Agent direkt in diesem Ordner arbeitet. Für alle anderen
Fälle gibt es zwei Wege:

| Werkzeug | Zugang zum Brain | Wo eintragen |
|---|---|---|
| Codex | globale Anweisungsdatei | `~/.codex/AGENTS.md` (Windows: `C:\Users\<name>\.codex\AGENTS.md`; bei gesetztem `CODEX_HOME` dort) |
| Claude Code | globale Anweisungsdatei | `~/.claude/CLAUDE.md` |
| ChatGPT | Projekt mit Projektanweisungen | in der ChatGPT-App unter Projekte |

### Codex und Claude Code: globale Anweisungsdatei

Die globale Datei gilt für jeden lokalen Chat, auch in fremden Projekten. Projektanweisungen
ergänzen oder überschreiben sie. Das Brain muss dafür kein eigenes Projekt sein; ein fester
Ordner reicht. Vorlage (Pfad anpassen):

```markdown
## Persönliche Wissensbasis

Mein Brain liegt unter: <absoluter Pfad zum Brain-Repo>
Einstieg: okf/index.md.

- Vor inhaltlichen Aufgaben dort nachschlagen. Für gezielte Fragen zuerst
  `python suche.py "<frage>"` im Brain-Ordner ausführen statt Index-Ketten abzulaufen.
- Wie mit dem Brain zu arbeiten ist, steht in dessen CLAUDE.md. Vor dem ersten Schreiben
  diese Datei lesen.
- Außerhalb des Brain-Ordners das Brain nur lesen. Erkenntnisse nur auf ausdrücklichen
  Wunsch eintragen, dann nach den Workflows aus CLAUDE.md (Destillat, Index, Validator).
```

### ChatGPT: Projekt „Mein Brain“

1. In der ChatGPT-App ein Projekt „Mein Brain“ anlegen.
2. Den lokalen Brain-Ordner verbinden. Das geht nur in der Desktop-App im Work-Modus und
   nicht in jedem Konto. Fehlt die Option, bleibt nur das Hochladen der Markdown-Dateien —
   dann siehe die Warnung unten.
3. In die Projektanweisungen schreiben: „Lies zuerst `okf/index.md` und die Regeln in
   `CLAUDE.md`. Nutze die Brain-Dateien, die zur Frage passen.“
4. Gespräche, die das Brain brauchen, in diesem Projekt starten. Dort sind beliebig viele
   getrennte Chats möglich; alle anderen Gespräche laufen wie gewohnt außerhalb. Für einen
   einzelnen Chat außerhalb lassen sich passende Dateien auch einzeln anhängen.

**Hochladen ist eine Kopie.** Sie veraltet mit der nächsten Änderung am Brain, und was ChatGPT
dort ändert, kommt nicht zurück. Hochgeladene Dateien taugen zum Ausprobieren, als dauerhafter
Zugang nur der verbundene lokale Ordner.

### Was ein Verweis nicht leistet

- **Keine Dateirechte.** Er sagt dem Agenten nur, wo das Brain liegt. Ob ein Chat außerhalb
  des Brain-Ordners dort lesen oder schreiben darf, regeln Sandbox und Freigaben des Werkzeugs
  (bei Codex z. B. zusätzliche beschreibbare Ordner in `config.toml`).
- **Kein Chatgedächtnis.** Neue Chats bekommen, was im Brain steht, aber keine früheren
  Chatverläufe. Was bleiben soll, muss als Record ins Brain.
- **Keine Datenhoheit.** Was ein Cloud-Werkzeug aus dem Brain liest, geht an dessen Anbieter,
  auch wenn der Ordner lokal liegt. Was nicht dorthin soll, gehört nicht in den freigegebenen
  Ordner.
