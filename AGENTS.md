# AGENTS.md

Die Regeln für Agenten in diesem Repo stehen in **[CLAUDE.md](CLAUDE.md)** — lies sie vollständig,
bevor du etwas tust. Sie gelten für jeden Agenten (Codex, Cursor, Copilot, Gemini …), nicht nur
für Claude. Details zu Typ-Taxonomie und Frontmatter: [CONTRIBUTING.md](CONTRIBUTING.md).

Diese Datei ist bewusst nur ein Verweis, damit es eine einzige gepflegte Regelquelle gibt.
Regeln nie hier ergänzen, sondern in CLAUDE.md.

## Einrichtung: das Brain aus anderen Projekten nutzen

Dieser Abschnitt ist keine Regel für die Arbeit im Repo, sondern eine Anleitung für Menschen.

Diese Datei wirkt nur, wenn der Agent **in diesem Ordner** arbeitet. Soll das Brain auch in
Chats zu anderen Projekten verfügbar sein, braucht es zusätzlich einen Verweis in der
**globalen** Anweisungsdatei des Agenten:

| Agent | Globale Datei | Geltungsbereich |
|---|---|---|
| Codex | `~/.codex/AGENTS.md` (Windows: `C:\Users\<name>\.codex\AGENTS.md`; bei gesetztem `CODEX_HOME` dort) | alle lokalen Codex-Chats |
| Claude Code | `~/.claude/CLAUDE.md` | alle Claude-Code-Sessions |

Projektanweisungen ergänzen die globale Datei oder überschreiben sie. Das Brain muss dafür
kein eigenes Projekt sein, ein fester Ordner reicht. Vorlage für die globale Datei (Pfad
anpassen):

```markdown
## Persönliche Wissensbasis

Mein Brain liegt unter: <absoluter Pfad zum Brain-Repo>
Einstieg: okf/index.md.

- Vor inhaltlichen Aufgaben dort nachschlagen. Für gezielte Fragen zuerst
  `python suche.py "<frage>"` im Brain-Ordner ausführen statt Index-Ketten abzulaufen.
- Wie mit dem Brain zu arbeiten ist, steht in dessen CLAUDE.md. Vor dem ersten Schreiben
  dort diese Datei lesen.
- Außerhalb des Brain-Ordners das Brain nur lesen. Erkenntnisse nur auf ausdrücklichen
  Wunsch eintragen, dann nach den Workflows aus CLAUDE.md (Destillat, Index, Validator).
```

Zwei Dinge leistet der Verweis nicht:

- **Keine Dateirechte.** Er sagt dem Agenten nur, wo das Brain liegt. Ob ein Chat außerhalb
  des Brain-Ordners dort lesen oder schreiben darf, regeln Sandbox und Freigaben des Agenten
  (bei Codex z. B. zusätzliche beschreibbare Ordner in `config.toml`).
- **Kein Chatgedächtnis.** Neue Chats bekommen, was im Brain steht, aber keine früheren
  Chatverläufe. Was bleiben soll, muss als Record ins Brain.
