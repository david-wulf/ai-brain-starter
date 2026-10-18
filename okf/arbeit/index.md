---
type: index
title: Arbeit — Einstieg
description: Beruflicher Bereich. Enthält im Auslieferungszustand nur einen Beispiel-Record.
abgeleitet_aus:
  - beispiel-decision.md
stand: 2026-09-28
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

## Konzepte

- [Beispiel: Entscheidung](beispiel-decision.md) — zeigt `basiert_auf`, „Geprüfte Historie", einen
  Prüfvermerk zu einer geänderten Voraussetzung und Fußnoten-Belege

> Dieser Index trägt `abgeleitet_aus` + `stand`, weil er den Zustand anderer Records referiert.
> Ändert sich eine Quelle, meldet `validate_okf.py`, dass hier nachzuziehen ist.
