---
type: source
title:               # Titel des Papers/Artikels
description: 
resource:            # PFLICHT in der Praxis: URL oder DOI des Originals
criticality: flexible
tags: []
generated:
  by:                # wer den Inhalt erzeugt hat: human:dein-kuerzel | claude/<modell> | <agent>
  at:                # Datum, an dem du es gelesen/aufgenommen hast
verified: []         # Bestaetigungen: - { by: human:dein-kuerzel, at: 2026-07-26 }
sources:              # OKF v0.2 — hier das Original selbst
  - id: original
    resource:         # gleiche URL/DOI wie oben
    title:
    author:
basiert_auf: []      # Eigen-Extension: Records, auf deren Aussage dieser hier fusst
blockiert_durch: []  # Eigen-Extension: offene Vorbedingungen (eigener Record, wenn mehrfach)
abgeleitet_aus: []   # Eigen-Extension: Quell-Records, deren Zustand dieser Record referiert
stand:               # Eigen-Extension: ISO 8601 - bis hierhin nachgezogen (Pflicht bei abgeleitet_aus)
ersetzt_durch:       # Eigen-Extension: nur bei status: deprecated - relativer Pfad auf den Nachfolger
owner: dein-kuerzel
status: stable
authors:             # frei: Autor(en)
---

# Was nehme ich mit

- Kernerkenntnis 1
- Kernerkenntnis 2
- Kernerkenntnis 3

# Warum relevant

Wofuer ist das nuetzlich? Was aendert es an meinem Denken/Vorgehen?

# Verknuepfungen

- [Betroffene Entitaet/Playbook](../bereich/konzept.md)

<!-- Kein Volltext, kein PDF-Inhalt. Nur Destillat + Link aufs Original. -->
