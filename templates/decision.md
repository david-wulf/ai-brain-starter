---
type: decision
title: 
description: 
resource:            # optional: Link zur Aufgabe im Aufgabenwerkzeug (Ausführung lebt dort)
criticality: controlled
stale_after:         # optional: nur wenn die Entscheidung zeitgebunden gilt (ISO 8601)
tags: []
generated:
  by:                # wer den Inhalt erzeugt hat: human:dein-kuerzel | claude/<modell> | <agent>
  at:                # ISO 8601 — letzte inhaltliche Aenderung
verified: []         # Bestaetigungen: - { by: human:dein-kuerzel, at: 2026-07-26 }
sources: []           # OKF v0.2 — Belege: - { id: kurz-id, resource: <URL oder ../pfad.md>, title: ..., author: ..., last_modified: YYYY-MM-DD }
                     # Im Body per Fussnote referenzieren: [^kurz-id]
basiert_auf: []      # Eigen-Extension: Records, auf deren Aussage dieser hier fusst
blockiert_durch: []  # Eigen-Extension: offene Vorbedingungen (eigener Record, wenn mehrfach)
abgeleitet_aus: []   # Eigen-Extension: Quell-Records, deren Zustand dieser Record referiert
stand:               # Eigen-Extension: ISO 8601 - bis hierhin nachgezogen (Pflicht bei abgeleitet_aus)
ersetzt_durch:       # Eigen-Extension: nur bei status: deprecated - relativer Pfad auf den Nachfolger
owner: dein-kuerzel
status: stable
---

# Entscheidung

Was wurde entschieden? (kurz und klar)

# Begründung

**Der wichtigste Teil.** Warum? Welcher Kontext galt zum Zeitpunkt? Ohne das „Warum" wird die
Entscheidung später falsch verallgemeinert (z.B. ein Keyword für immer gemieden, obwohl sich
der Kontext geändert hat).

# Quelle

Woher stammt das? (z.B. Strategie-Call 2026-04-21, Kunden-Feedback, Meeting-Notiz)

# Konsequenzen / Outcome

Was folgt daraus (falls bekannt)?

# Geprüfte Historie (Challenge)

Welche früheren decisions/patterns wurden vor dieser Entscheidung geprüft? Widersprach etwas —
und warum entscheiden wir jetzt trotzdem so? Auch „nichts Einschlägiges gefunden" notieren.

- [Frühere Entscheidung](2026-01-01-beispiel.md) — Ergebnis des Abgleichs

# Verknüpfungen

- [Verwandtes Konzept](../konzept.md)
