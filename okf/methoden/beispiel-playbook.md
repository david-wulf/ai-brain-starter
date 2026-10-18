---
type: playbook
title: Beispiel — Eine Quelle destillieren
description: Soll-Vorgehen, um aus einem Artikel oder Paper eine source-Notiz zu machen, die in einem Jahr noch etwas wert ist.
resource:
criticality: hybrid
tags: [beispiel, quellen]
generated:
  by: human:dein-kuerzel
  at: 2026-08-20
verified: []
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format — SPEC.md
    author: GoogleCloudPlatform/knowledge-catalog
basiert_auf: []
blockiert_durch: []
abgeleitet_aus: []
stand:
ersetzt_durch:
owner: dein-kuerzel
status: stable
---

# Wozu

Dieser Record ist ein **Beispiel** — er zeigt, wie ein `playbook` in diesem Bundle aussieht, und
beschreibt zugleich einen Ablauf, den du wirklich brauchen wirst. Lösche ihn, sobald du eigene
Records hast, oder schreib ihn um.

# Vorgehen

1. **Lesen und schließen.** Erst den Artikel zu Ende lesen, dann das Fenster zumachen. Wer beim
   Lesen mitschreibt, schreibt Sätze ab statt Erkenntnisse.
2. **Drei bis sechs Kernpunkte** aus dem Kopf notieren. Was nicht hängengeblieben ist, war für
   dich nicht der Kern — auch wenn der Autor es fett gesetzt hat.
3. **`resource:` setzen** — URL oder DOI des Originals. Ohne Rückweg ist die Notiz eine
   Behauptung.
4. **In die betroffenen Konzepte verlinken.** Eine Quelle, die nirgends eingeht, hat nichts
   verändert und muss nicht gespeichert werden.
5. **Kein Volltext.** Das Original bleibt beim Original. Ein Konzept = eine Datei; der Pfad ohne
   `.md` ist die permanente ID. [^okf-spec]

# Wann nicht

Wenn du den Artikel nur „mal aufheben" willst. Dafür ist ein Bookmark da. Ins Brain kommt, was
dein Vorgehen ändert.

# Verknüpfungen

- [Methoden](index.md)
- [OKF-Spec](../okf-spec.md) — Formatgrundlage
