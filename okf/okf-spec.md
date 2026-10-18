---
type: reference
title: OKF-Spec — Quelle, genutzte Version, Abweichungen
description: Wo das Open Knowledge Format definiert ist, welche Version dieses Bundle nutzt und wo es bewusst von der Spec abweicht.
resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
criticality: hybrid
tags: [okf, brain, format, governance]
generated:
  by: claude/opus-5.5
  at: 2026-09-28
verified: []
owner: dein-kuerzel
status: stable
---

# Kurzfassung

- **Genutzte Version:** OKF **v0.2** (veröffentlicht 2026-07-24)
- **Normative Quelle:** [okf/SPEC.md im Repo GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- **Deklariert im Bundle:** `okf_version: "0.2"` im Frontmatter von [index.md](index.md)

Dieser Record ist `criticality: hybrid`: Er ist die Autorität dafür, **welche Version** dieses
Bundle anzielt und **wo es abweicht**. Für Detailfragen zum Format darf die verlinkte SPEC.md
herangezogen werden — sie darf diesem Record aber nicht widersprechen. Tut sie es, ist eine
Spec-Aktualisierung fällig (siehe Update-Prozedur unten).

> **Hinweis zum Abruf:** Web-Abrufe der Rohdatei liefern reproduzierbar veraltete Cache-Stände.
> Im Zweifel im Browser prüfen oder das Repo klonen. Die Feldformen von v0.2 lassen sich
> zusätzlich gegen den [Ankündigungs-Blogpost](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals)
> und das v0.2-Beispielbundle `okf/bundles/acme_retail/` im selben Repo sichern.

# Wo OKF definiert ist

OKF ist **ausschließlich** im Google-Cloud-Repo `GoogleCloudPlatform/knowledge-catalog`
spezifiziert. Es gibt keine zweite normative Fundstelle: keine eigene Domain, kein
Standardisierungsgremium, keine RFC. Alles andere ist Sekundärliteratur.

| Was | Wo | Rolle |
|---|---|---|
| Spezifikation | [okf/SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) | **normativ** — die einzige verbindliche Quelle |
| v0.2-Ankündigung | [OKF v0.2 adds trust signals](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals) | Autoren-Blog mit Feldbeispielen |
| v0.1-Ankündigung | [How the OKF can improve data sharing](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) | Sekundärquelle, Juni 2026 |
| Kontext & Referenz-Agent | [okf/README.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md) | erklärend, Referenz-Agent + Visualizer |
| Beispiel-Bundles | [okf/bundles/](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/bundles) | GA4, Stack Overflow, Bitcoin, `acme_retail` (v0.2-Beispiel) |
| Produkt-Andockung | [Knowledge Catalog](https://cloud.google.com/products/knowledge-catalog) | GCP-Dienst, der OKF ingestiert — für ein privates Brain **nicht** nötig |

Das Repo ist kein offizielles Google-Produkt (eigener Disclaimer); OKF ist ausdrücklich in
Entwicklung.

# Kern der Spec

Ein **Bundle** ist ein Verzeichnisbaum aus Markdown-Dateien. Eine Datei = ein **Konzept**; der
Pfad ohne `.md` ist die **Konzept-ID**. Jede Nicht-Reserved-Datei braucht einen
YAML-Frontmatter-Block mit nicht-leerem `type` — das bleibt auch in v0.2 die **einzige** harte
Pflicht. Eigene Felder sind ausdrücklich erlaubt. Reservierte Dateinamen: `index.md` und
`log.md` — nie für Konzepte verwenden. Konsumenten müssen tolerant sein: unbekannte
`type`-Werte, fehlende Felder, tote Links und fehlende Indizes dürfen ein Bundle nicht
disqualifizieren.

## Was v0.2 ergänzt

v0.2 ist ein **additiver Minor-Bump**: ein v0.1-Bundle bleibt unverändert gültig. Neu sind vier
Familien optionaler Frontmatter-Felder, die je eine Frage beantworten, **bevor** ein Konsument
den Body liest:

| Familie | Felder | Beantwortet |
|---|---|---|
| Provenienz | `sources` (je Eintrag `id`, `resource`, `title`, `author`, `usage_count`, `last_modified`) | Woraus ist das entstanden? |
| Trust | `generated: { by, at }`, `verified: [ { by, at } ]` | Wer hat es erzeugt, wer bestätigt? |
| Frische & Lifecycle | `status` (`draft` → `stable` → `deprecated`, fehlend = `stable`), `stale_after` (absolutes Datum) | Ist es noch gültig? |
| Attestierung | neuer Typ `Attested Computation` mit `runtime`, `parameters`, `executor`, `attester` | Wurde die Zahl auf dem sanktionierten Weg berechnet? |

Aus `verified` leitet ein Konsument den **Trust-Tier** ab: kein `verified` = *unverified*, nur
maschinelle Bestätiger = *machine-confirmed*, ein `human:<id>`-Bestätiger = *human-reviewed*.
Bewusst **kein** Credibility-Score — OKF speichert Signale, keine Urteile.

Zwei Ablösungen (v0.2-Konsumenten dürfen auf die alte Form zurückfallen): `timestamp` →
`generated.at` und die Body-Liste `# Citations` → `sources`.

# Wie dieses Bundle v0.2 nutzt

| Feld | Regelung |
|---|---|
| `generated.at` | **Pflicht in der Praxis.** Ersetzt das alte `timestamp`. Der Validator warnt, wenn es fehlt. |
| `generated.by` | Bei jedem neuen/geänderten Record setzen: `human:<kuerzel>`, `claude/<modell>` oder `<agent>`. |
| `verified` | Leere Liste als Default. Wird gesetzt, wenn ein Mensch den Record durchgesehen hat: `- { by: human:<kuerzel>, at: <ISO-Datum> }`. Nie stellvertretend setzen. |
| `status` | Nur `draft` / `stable` / `deprecated`. |
| `stale_after` | Absolutes ISO-Datum, nur für zeitgebundene Records. Der Validator warnt bei Überschreitung, bricht aber nicht. |
| `sources` | `id` + `resource` sind Pflicht (Validator). Interne Quellen zeigen als relativer Pfad auf die `source`-Notiz, nicht direkt auf die externe URL. Body-Links bleiben zusätzlich bestehen. |
| Fußnoten `[^id]` | Belegter Satz bekommt `[^<source-id>]`. Der Validator prüft, dass jede Referenz auf eine `sources`-id oder eine eigene Definition zeigt. |
| `Attested Computation` | Nicht genutzt. Relevant erst, wenn Agenten aus dem Brain heraus Kennzahlen berechnen und ausweisen. |
| `criticality` | Eigen-Extension ohne Spec-Pendant — steuert das Retrieval-Verhalten von Agenten, siehe [CLAUDE.md](../CLAUDE.md). |
| `abgeleitet_aus` + `stand` | Eigen-Extension. Ein Record, der den Zustand anderer Records zusammenfasst, nennt seine Quellen und das Datum, bis zu dem er nachgezogen ist. Der Validator warnt, wenn eine Quelle laut `generated.at` neuer ist als `stand`. Kein Spec-Pendant: OKF datiert Records, aber nicht ihre Abhängigkeit voneinander. |
| `basiert_auf` / `blockiert_durch` | Eigen-Extension. `basiert_auf` nennt Records, auf deren Aussage dieser hier fußt — der Validator warnt, wenn die Voraussetzung `deprecated` oder jünger ist als der abhängige Record. `blockiert_durch` nennt offene Vorbedingungen; der Validator zählt aus, welche wie viele Records aufhält. |
| `ersetzt_durch` | Eigen-Extension. Maschinenlesbarer Nachfolger bei `status: deprecated` — die Spec kennt den Status, aber nicht das Ziel. |
| `geprueft` | Eigen-Extension. Liste `{ quelle, at }` je `basiert_auf`-Eintrag: Datum, an dem eine gemeldete Änderung der Voraussetzung nachgeprüft wurde und die Aussage trug. Der Validator vergleicht die Quelle dann gegen dieses Datum statt gegen `generated.at` — so löst eine Prüfnotiz keine Folge-Warnungen aus und verdeckt keine weiteren Voraussetzungen. Regeln: [CONTRIBUTING.md](../CONTRIBUTING.md), Abschnitt „Abhängigkeiten“. |
| `umfang_ok` | Eigen-Extension. Begründung, warum ein Record bewusst über 25 KB bleibt (z.B. eine Tabelle, die nur als Ganzes Sinn ergibt). Der Validator nimmt ihn dann vom Umfangs-Hinweis aus und zählt ihn nur. Regeln: [CONTRIBUTING.md](../CONTRIBUTING.md), Abschnitt „Lesbarkeit für Agenten“. |
| `owner` | Eigen-Extension. Wer das Konzept besitzt. |

# Abweichungen dieses Bundles von v0.2

Alle bewusst, alle konformitätsverträglich — beim nächsten Versions-Update erneut prüfen:

| # | Spec sagt | Dieses Bundle macht | Warum / Status |
|---|---|---|---|
| 1 | Bundle-absolute Links `/bereich/konzept.md` sind **empfohlen** | ausschließlich **relative** Links `../bereich/konzept.md` | Relative Links sind explizit erlaubt. Absolute Pfade zeigen in Obsidian und im lokalen Dateisystem ins Leere. **Konform.** |
| 2 | `index.md` enthält **kein** Frontmatter; erlaubt nur in der Root-`index.md` | **jede** `index.md` hat Frontmatter mit `type: index` | Weiche Abweichung. Der Validator erzwingt `type` überall; die Konformitätsregel verlangt das nur für Nicht-Reserved-Dateien, und Konsumenten müssen es tolerieren. **Bewusst.** |
| 3 | Non-Goal: keine feste Typ-Taxonomie | **geschlossene** Taxonomie (`project`, `playbook`, `pattern`, …) | Strenger als die Spec, nicht im Widerspruch. Taxonomie: [CONTRIBUTING.md](../CONTRIBUTING.md). **Konform.** |
| 4 | Producer dürfen eigene Felder ergänzen | `criticality`, `owner`, `abgeleitet_aus`, `stand`, `ersetzt_durch`, `basiert_auf`, `blockiert_durch`, `geprueft`, `umfang_ok` | Ausdrücklich vorgesehene Extension. **Konform.** |
| 5 | optionale `log.md` je Ebene für Änderungshistorie | wird **nicht** genutzt (Historie liegt in Git) | Optional. **Konform.** |
| 6 | Quellen gehören in `sources` (löst `# Citations` ab) | `sources` **plus** weiterhin `source`-Notizen und Body-Links | Die Notizen sind Destillate mit eigenem Wert, kein bloßer Zitat-Anhang. `sources` verweist auf sie statt sie zu ersetzen. **Konform.** |
| 7 | `generated.at` als ISO-8601-**Datetime** | reines ISO-**Datum** (`2026-08-24`) | ISO 8601 deckt beides ab; Datum reicht für Handpflege. **Konform.** |
| 8 | `sources`-Einträge tragen Credibility-Signale wie `usage_count` | nur `id`, `resource`, `title`, `author`, `last_modified` | `usage_count` existiert für redaktionelle Quellen nicht sinnvoll. Alle Felder sind optional. **Konform.** |
| 9 | `usage_window: { from, to }` (im Beispielbundle) | nicht genutzt | Bezieht sich auf Nutzungszeiträume von Datenquellen. Ohne Anwendung. **Konform.** |

# Update-Prozedur bei neuer OKF-Version

1. **Prüfen:** [SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
   öffnen und die Zeile „Version X.Y" mit der Kurzfassung oben vergleichen. Für Benachrichtigung:
   im Repo *Watch → Custom → Releases* aktivieren oder die
   [Commit-Historie der Datei](https://github.com/GoogleCloudPlatform/knowledge-catalog/commits/main/okf/SPEC.md)
   beobachten.
2. **Einordnen:** Minor-Bump = rückwärtskompatible Ergänzungen, meist neue optionale Felder.
   Major-Bump (0.x → 1.0) = mögliche Breaking Changes bei Pflichtfeldern oder reservierten
   Dateinamen — dann Punkt 3–7 vollständig durchgehen.
3. **Nutzungstabelle und Abweichungstabelle** oben durchgehen: Was ist überholt, aufgelöst oder
   neu problematisch?
4. **Bestand migrieren:** Feldumbenennungen skriptgestützt und **nur innerhalb des
   Frontmatter-Blocks**; vorher ein Tarball-Backup ziehen (der Git-Stand ist oft nicht sauber).
5. **Tooling nachziehen:** `templates/` (alle 14 Vorlagen), `validate_okf.py` (Enum-Werte,
   abgelöste Feldnamen als Fehler), [CONTRIBUTING.md](../CONTRIBUTING.md),
   [CLAUDE.md](../CLAUDE.md), [README.md](../README.md).
6. **Validieren:** `python validate_okf.py` muss fehlerfrei durchlaufen.
7. **Version deklarieren:** `okf_version` in [index.md](index.md) hochsetzen und in diesem Record
   Version, Prüfdatum und Nutzungstabelle aktualisieren.

# Verknüpfungen

- [Brain-Einstieg](index.md) — Bundle-Root, trägt die `okf_version`-Deklaration
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Konventionen und Typ-Taxonomie für Menschen
- [CLAUDE.md](../CLAUDE.md) — Regeln für Agenten (Criticality, Mandantentrennung, Workflows)
- [README.md](../README.md) — Überblick, Validator, Obsidian-Setup
