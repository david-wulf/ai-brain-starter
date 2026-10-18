---
type: index
title: Arbeit — Einstieg
description: Beruflicher Bereich. Enthält im Auslieferungszustand fiktive Beispielordner und -Records.
abgeleitet_aus:
  - beispiel-decision.md
  - ordner1/index.md
  - ordner2/index.md
  - quellen/index.md
stand: 2026-10-18
generated:
  by: claude/opus-5.5
  at: 2026-10-18
owner: dein-kuerzel
status: stable
---

# Arbeit

Hier lebt alles Berufliche. Bewährte Unterteilung — anlegen, sobald du sie brauchst, nicht auf Vorrat:

| Ordner | Inhalt |
|---|---|
| `quellen/` | destillierte Literatur-/Artikelnotizen (`type: source`) |
| `<account>/` | ein Account/Kunde mit `soul/` + `memory/` (Schema: [CONTRIBUTING.md](../../CONTRIBUTING.md)) |
| `<methodik>/` | account-übergreifende Fachmethodik deines Handwerks |
| `<firma>/` | wie es bei dieser konkreten Firma ist (CI, Domains, Assets) |

## Beispielordner (fiktiv, zum Löschen gedacht)

- [ordner1](ordner1/index.md) — ein Account mit `soul/` + `memory/`: Profil (`entity`), Never-Do
  (`guideline`), Entscheidung (`decision`), Muster (`pattern`), Meeting (`meeting`)
- [ordner2](ordner2/index.md) — account-übergreifendes Fachwissen: Kennzahl (`metric`), Prozess (`process`)
- [quellen](quellen/index.md) — destillierte Literatur (`source`)

Benenne die Ordner nach deinen eigenen Accounts und Themen — `ordner1`/`ordner2` sind Platzhalter.

## Konzepte

- [Beispiel: Entscheidung](beispiel-decision.md) — zeigt `basiert_auf`, „Geprüfte Historie", einen
  Prüfvermerk zu einer geänderten Voraussetzung und Fußnoten-Belege

> Dieser Index trägt `abgeleitet_aus` + `stand`, weil er den Zustand anderer Records referiert.
> Ändert sich eine Quelle, meldet `validate_okf.py`, dass hier nachzuziehen ist.
