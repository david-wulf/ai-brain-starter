---
type: meeting
title:               # z.B. "Kickoff Kunde X"
description: 
resource:            # optional: Kalender-/Doc-Link
criticality: hybrid
tags: []
generated:
  by:                # wer den Inhalt erzeugt hat: human:dein-kuerzel | claude/<modell> | <agent>
  at:                # Datum des Meetings (ISO 8601)
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
attendees:           # frei: Teilnehmer
---

# Kontext

Worum ging es, warum fand das Meeting statt?

# Entscheidungen

- Entscheidung (Was + Warum)

# Erkenntnisse

- Was wurde klar / festgehalten?

# Verknuepfungen

- [Betroffenes Projekt/Entitaet](../konzept.md)

<!-- Kein Transkript. Action Items sind Todos -> gehoeren ins Aufgabenwerkzeug, nicht hierher. -->
