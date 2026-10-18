---
type: decision
title: Beispiel — Relative Links statt bundle-absoluter Pfade
description: Dieses Bundle verlinkt ausschließlich relativ, damit es lokal und in Obsidian funktioniert.
resource:
criticality: controlled
stale_after:
tags: [beispiel, format]
generated:
  by: human:dein-kuerzel
  at: 2026-08-24
verified: []
sources: []
basiert_auf:
  - ../okf-spec.md
geprueft:
  - { quelle: ../okf-spec.md, at: 2026-09-28 }
blockiert_durch: []
abgeleitet_aus: []
stand:
ersetzt_durch:
owner: dein-kuerzel
status: stable
---

> **Voraussetzung geprüft 2026-09-28:** [OKF-Spezifikation](../okf-spec.md) wurde am 2026-09-28
> geändert — neu sind nur die Eigen-Extensions `umfang_ok` und `geprueft` in Nutzungs- und Abweichungstabelle. Die
> Link-Regel (Abweichung Nr. 1) ist unberührt; die Entscheidung trägt damit weiter.

# Entscheidung

Alle internen Links sind **relative Markdown-Links** (`[Text](../methoden/beispiel-playbook.md)`) — nie
bundle-absolute Pfade (`/bereich/konzept.md`), nie Obsidian-Wikilinks (`[[...]]`).

# Begründung

Die Spec empfiehlt bundle-absolute Pfade, erlaubt relative aber ausdrücklich. Absolute Pfade
zeigen im lokalen Dateisystem und in Obsidian ins Leere — das Bundle wäre nur noch in einem
Werkzeug navigierbar, das den Bundle-Root kennt. Wikilinks binden es an Obsidian und machen es
unportabel. Der Preis der relativen Variante: Beim Verschieben einer Datei müssen die Links
mitgezogen werden. Das nimmt Obsidian einem ab, wenn `alwaysUpdateLinks` an ist.

# Quelle

Abwägung beim Aufsetzen des Bundles, gegen die Spec-Empfehlung geprüft — siehe Abweichung #1 in
[okf-spec](../okf-spec.md).

# Konsequenzen / Outcome

`validate_okf.py` prüft die Auflösbarkeit jedes relativen Links und bricht bei toten Links ab.
Die drei Obsidian-Einstellungen in `.obsidian/app.json` sind damit **nicht optional**.

# Geprüfte Historie (Challenge)

Nichts Einschlägiges gefunden — durchsucht wurde `okf/` im Auslieferungszustand. Dieser Abschnitt
gehört auch dann in jede `decision`, wenn er leer ausfällt: „nichts gefunden, hier gesucht" ist
ein Ergebnis, „kein Abschnitt" ist eine Lücke.

# Verknüpfungen

- [OKF-Spec](../okf-spec.md) — Abweichungstabelle
- [Arbeit](index.md)
