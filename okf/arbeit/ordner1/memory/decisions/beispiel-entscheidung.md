---
type: decision
title: Ordner 1 — Kanal A vor Kanal B
description: "Warum der Beispiel-Account zuerst Kanal A ausbaut und Kanal B zurückstellt."
resource: https://example.org/aufgabe/123
criticality: controlled
tags: [beispiel, kanal]
basiert_auf:
  - ../../soul/profil.md
  - ../../../ordner2/beispiel-kennzahl.md
generated:
  by: claude/opus-5.5
  at: 2026-10-18
verified: []
owner: dein-kuerzel
status: stable
---

# Entscheidung

Kanal A wird zuerst ausgebaut, Kanal B bleibt bis auf Weiteres zurückgestellt.

# Begründung

Die [Beispiel-Kennzahl](../../../ordner2/beispiel-kennzahl.md) reagiert auf Kanal A messbar,
auf Kanal B nicht. Fällt diese Voraussetzung, ist die Entscheidung neu zu bewerten — deshalb
steht sie in `basiert_auf`, und der Validator meldet, wenn sie sich später ändert.

# Quelle

[Beispiel-Meeting vom 2026-10-01](../meetings/2026-10-01-beispiel-meeting.md). Die Umsetzung
lebt als Aufgabe im Aufgabenwerkzeug (`resource:`), nicht hier.

# Geprüfte Historie (Challenge)

Nach `type: decision` und `type: pattern` in `arbeit/ordner1/` gesucht: kein Widerspruch. Das
[Muster zu Betreffzeilen](../patterns/beispiel-muster.md) betrifft Kanal A und stützt die Wahl.
