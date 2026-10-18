# AI Brain Starter (OKF)

Ein Starter-Kit für ein **persönliches Wissens-Brain im [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)** —
eine kuratierte, verlinkte Markdown-Bibliothek, die in Obsidian gepflegt und von Agenten (z.B.
Claude Code) gelesen und erweitert werden kann. Kein Server, keine Datenbank, kein SDK — nur ein
Git-Repo aus Markdown-Dateien.

> **English:** A starter kit for a personal knowledge brain in the Open Knowledge Format — plain
> Markdown, Git, Obsidian, and a dependency-free Python validator. It ships the conventions
> (`CONTRIBUTING.md`), the agent rules (`CLAUDE.md`), 14 record templates and four CLI tools
> (validator, search, change log, open items).
> Documentation and templates are in German; the format itself is language-agnostic.

Das Kit ist die **Tooling-Schicht** eines gewachsenen Brains, aus dem der private Inhalt entfernt
wurde. Es enthält keine Wissens-Records außer zwei Beispielen — die schreibst du.

## Was drin ist

| Datei / Ordner | Rolle |
|---|---|
| `CONTRIBUTING.md` | die Hausordnung: Typ-Taxonomie, Frontmatter, Criticality, Abhängigkeitsfelder |
| `CLAUDE.md` | die Regeln, die der Agent liest — Zugriffsgrenzen, Workflows, Grundprinzipien |
| `okf/okf-spec.md` | wo OKF definiert ist, welche Version genutzt wird, bewusste Abweichungen |
| `templates/` | 14 Vorlagen, eine je Record-Typ |
| `validate_okf.py` | prüft Format, Links, Indizes, Felder, Abhängigkeiten — Exit ≠ 0 bei Fehlern |
| `chronik.py` | erntet die datierten Änderungsmarker: was wurde wann gekippt |
| `offene_punkte.py` | sammelt die offenen Punkte eines Bereichs als Leseliste |
| `suche.py` + `suche_testfragen.tsv` | findet den passenden Record (BM25F) und liest nur den nötigen Abschnitt; misst die eigene Trefferquote |
| `okf/` | Bundle-Skelett mit drei Bereichen und zwei Beispiel-Records |
| `.obsidian/app.json` | die drei formatkritischen Obsidian-Einstellungen |

Alle vier Skripte laufen mit der **Python-Standardbibliothek**, ohne Abhängigkeiten.

## Warum das mehr ist als „Notizen in Markdown"

Drei Mechanismen unterscheiden das Kit von einem leeren Ordner. Alle drei sind aus konkreten
Fehlern entstanden und werden maschinell geprüft:

- **`criticality`** — jeder Record sagt, wie deterministisch ein Agent ihn benutzen muss. Bei
  `controlled` gilt: fehlt der Record oder ist er veraltet, **hält der Agent an und fragt** statt
  aus dem Web zu rekonstruieren. Das ist die Regel, die halluzinierte Preise verhindert.
- **`abgeleitet_aus` + `stand`** — eine Übersicht, die den Zustand anderer Records zusammenfasst,
  deklariert ihre Quellen und ihr Nachzieh-Datum. Der Validator meldet, wenn eine Quelle inzwischen
  neuer ist. Ohne das behauptet die bequemste Datei im Repo den ältesten Stand.
- **`basiert_auf` / `blockiert_durch`** — worauf eine Entscheidung fußt und was sie aufhält, steht
  im Frontmatter statt im Fließtext. Kippt eine Voraussetzung, ist die Entscheidung neu zu bewerten;
  ein Blocker, der mehrere Records aufhält, wird zählbar.

## Erste Schritte

```bash
git clone <dein-fork> mein-brain && cd mein-brain
python validate_okf.py     # muss fehlerfrei durchlaufen
```

Dann **anpassen** — das ist der eigentliche Setup-Schritt. Die Vorlage ist absichtlich meinungsstark;
was nicht auf dich zutrifft, ist schlimmer als eine Lücke, weil der Agent es als Gesetz liest.

- [ ] **Kürzel setzen:** `dein-kuerzel` in `templates/*.md`, `okf/**/*.md` und den Doku-Dateien
      durch dein eigenes ersetzen (betrifft `owner:` und `human:<kuerzel>`).
- [ ] **Bereiche benennen:** `okf/arbeit`, `okf/privat`, `okf/methoden` umbenennen oder reduzieren —
      und die Erwähnungen in `CLAUDE.md`, `CONTRIBUTING.md` und `okf/index.md` mitziehen.
- [ ] **Denkrahmen in `CLAUDE.md`** ersetzen oder streichen. Der mitgelieferte (Structural Tension)
      ist ein Beispiel, keine Empfehlung für dich.
- [ ] **`<Aufgabenwerkzeug>` in `CLAUDE.md`** durch deins ersetzen und die Werkzeug-Grenzen
      aufschreiben: welches Tool darf in welchem Kontext benutzt werden?
- [ ] **Beispiel-Records löschen:** `okf/arbeit/beispiel-decision.md`, `okf/methoden/beispiel-playbook.md`
      — samt der Einträge in den jeweiligen `index.md` und der Beispielzeilen in `suche_testfragen.tsv`.
- [ ] **Remote prüfen:** Ein Brain enthält früher oder später Sensibles. Ein öffentliches Repo ist
      dafür der falsche Ort — nimm einen privaten Remote oder eine selbstgehostete Instanz.
- [ ] **Obsidian öffnen** und die drei Einstellungen unten gegenprüfen.
- [ ] `python validate_okf.py` — muss nach allem noch fehlerfrei sein.

Danach: erstes Konzept anlegen — Vorlage aus [`templates/`](templates/) kopieren, in den richtigen
Bereich legen, Frontmatter ausfüllen, in der `index.md` des Ordners verlinken.

## Aufbau

- Der **Bundle-Root ist `okf/`**. Alles darunter ist Wissen, alles darüber ist Tooling.
- **Ein Konzept = eine Markdown-Datei.** Der Pfad innerhalb von `okf/` ohne `.md` ist die
  permanente Konzept-ID (z.B. `arbeit/projekt/thema.md` → `arbeit/projekt/thema`).
- Jede Datei beginnt mit **YAML-Frontmatter**; einziges Pflichtfeld ist `type`. In der Praxis
  trägt jeder Record zusätzlich `generated.at` (Änderungsdatum) und `status`.
- **Abgeleitete Sichten deklarieren ihre Quellen** über `abgeleitet_aus:` + `stand:`.
- Verlinkung über **relative Standard-Markdown-Links** (`[Text](../bereich/konzept.md)`).
  Niemals Obsidian-Wikilinks (`[[...]]`) oder Embeds (`![[...]]`) — sonst ist das Bundle
  nicht portabel.
- Jeder Ordner hat eine `index.md` mit verlinkter Liste seiner Konzepte.

### Bereiche

Drei Bereiche unter `okf/`: **`arbeit/`** (beruflich), **`privat/`** (persönlich) und
**`methoden/`** (allgemeine Denk- und Schaffenswerkzeuge). In Arbeits-/Client-Kontext ist
`privat/` tabu — `methoden/` dagegen ist bereichsübergreifend und in beiden Welten nutzbar.

Das ist ein Vorschlag, keine Vorgabe der Spec. Die Trennung hat aber einen Zweck: Sie macht die
Zugriffsregel in `CLAUDE.md` **baulich** durchsetzbar statt nur gedanklich.

## Rollen

- **Du (Mensch):** kuratierst, entscheidest, was durable ist, und legst die Struktur fest.
  Konventionen siehe [CONTRIBUTING.md](CONTRIBUTING.md).
- **Agent (z.B. Claude):** liest und erweitert das Brain nach den Regeln in
  [CLAUDE.md](CLAUDE.md), hält Indizes aktuell und lässt am Ende den Validator laufen.

## Validator

```bash
python validate_okf.py
```

Prüft: Frontmatter mit `type:` in jeder `.md` unter `okf/`, Auflösbarkeit aller relativen
Links, `index.md` in jedem Ordner, die OKF-v0.2-Felder (`status`, `stale_after`, `generated.at`,
`verified`, `sources` inkl. Fußnoten) und die Eigen-Extensions `criticality`, `abgeleitet_aus` /
`stand`, `basiert_auf` / `geprueft` / `blockiert_durch` sowie `ersetzt_durch`. Außerdem: `never-do.md` muss explizit
`criticality: controlled` tragen, und das Frontmatter muss für einen echten YAML-Parser lesbar
sein (unquotierter Doppelpunkt in `description`/`title` ist ein Fehler; ist PyYAML installiert,
läuft es als Gegenprobe mit). Exit-Code ≠ 0 bei Fehlern.

Warnungen brechen nichts, sind aber der eigentliche Nutzen: überschrittenes `stale_after`,
veraltete abgeleitete Sichten, wacklige Voraussetzungen, `deprecated` ohne Nachfolger, doppelte
Titel, Links auf abgelöste Records (außer die Zeile benennt die Ablösung selbst). Am Ende jedes Laufs zählt er aus, welche Vorbedingung wie viele Records blockiert.

Eine Warnung ist erst abgearbeitet, wenn das **Ergebnis der Prüfung datiert im Record steht** —
sonst kommt sie beim nächsten Lauf wieder und niemand weiß, ob schon jemand hingesehen hat.
Für eine geänderte Voraussetzung heißt das: Prüfnotiz im Body plus `geprueft: - { quelle, at }`
im Frontmatter — **nicht** `generated.at` hochsetzen, sonst warnen alle Records, die darauf
aufbauen (Konvention: [CONTRIBUTING.md](CONTRIBUTING.md#abhängigkeiten-basiert_auf-und-blockiert_durch)).

Dazu der Block **„Lesbarkeit"**: zählt `description`s über 200 Zeichen, Records über 25 KB (über
40 KB als „fällig" markiert) und `index.md` über 10 KB und zeigt je die zehn größten Fälle. Das
sind **Hinweise**, weder Fehler noch Warnung. `--lesbarkeit` listet alle Fälle. Records, die
bewusst groß bleiben, tragen `umfang_ok: <Begründung>`. Regeln:
[CONTRIBUTING.md](CONTRIBUTING.md#lesbarkeit-für-agenten-description-und-umfang).

## Suche — den passenden Record finden

```bash
python suche.py "warum relative Links"
python suche.py "…" --bereich arbeit/projekt
python suche.py "…" --ohne-privat --typ decision -n 5
python suche.py --gliederung okf/okf-spec.md
python suche.py --abschnitt okf/okf-spec.md "Abweichungen dieses Bundles von v0.2"
python suche.py --test
```

BM25F über Titel, `description`, Tags, Pfad, Überschriften und (schwach gewichtet) den Body,
mit Näherung für deutsche Komposita. Je Treffer: Pfad, `type`, `criticality`, `status`, Größe,
gekürzte `description` und bei größeren Records der Abschnitt, der am besten passt — den liest
man dann mit `--abschnitt` statt der ganzen Datei. `--json` liefert dasselbe maschinenlesbar
(etwa als Grundlage für einen Such-MCP).

Warum überhaupt eine Suche: Ab ein paar hundert Records läuft ein Agent sonst Index-Ketten ab
und liest ganze Dateien, um einen Absatz zu finden. Die Suche macht aus „drei Indizes und zwei
40-KB-Records" einen Aufruf und einen Abschnitt.

`--test` misst die Trefferquote gegen [suche_testfragen.tsv](suche_testfragen.tsv) (Frage,
erwarteter Pfad, optional Bereich) und bricht mit Exit ≠ 0, wenn weniger als 80 % der Fragen
den erwarteten Record unter den ersten drei finden. Die mitgelieferten drei Fragen zielen auf
die Beispiel-Records — ersetze sie durch deine eigenen und ergänze eine Zeile, sobald eine
Suche danebengeht. So fällt auf, wenn eine Umstrukturierung das Finden verschlechtert.

## Chronik — was wann gekippt wurde

```bash
python chronik.py okf/privat/bereich --art gekippt
```

Erntet die datierten Änderungsmarker aus den Records (`> **Korrektur JJJJ-MM-TT:**`,
`~~durchgestrichen~~ — erledigt am …`, `status: deprecated`) und gibt sie als Chronik aus.
Seit der Regel „richtigstellen, nur Kipppunkte datieren" (CONTRIBUTING.md) tragen nur noch
gekippte Entscheidungen eine Datumszeile — reine Sachkorrekturen stehen direkt im Text, ihre
Historie liegt in Git. Die Chronik zeigt damit genau die Kipppunkte. Arten:
`gekippt`, `erledigt`, `abgeloest`. Weitere Flags: `--seit JJJJ-MM-TT`, `--bis JJJJ-MM-TT`.

Das Datum stammt aus der Notiz, nicht aus `generated.at` — die Chronik bleibt also richtig,
auch wenn ein Record später nochmal angefasst wird.

## Offene Punkte einsammeln

```bash
python offene_punkte.py okf/privat/bereich
```

Listet die offenen Punkte der Records eines Bereichs, neueste zuerst. Durchgestrichene Einträge
gelten als erledigt und werden übersprungen; `index.md` bleibt außen vor (`--index` nimmt sie dazu,
`--alle` auch die erledigten, `--kurz` nur die Zählung je Record). Einträge, die nach „erledigt"
klingen, aber nicht durchgestrichen sind, werden mit `?` markiert.

Das Ergebnis ist eine **Leseliste, keine Aufgabenliste** — Todos gehören ins Aufgabenwerkzeug.

## Obsidian

Der Ordner ist zugleich ein Obsidian-Vault. Die formatkritischen Einstellungen liegen
versioniert in `.obsidian/app.json` und müssen so bleiben:

```json
{
  "useMarkdownLinks": true,
  "alwaysUpdateLinks": true,
  "newLinkFormat": "relative"
}
```

Entspricht in der UI: Einstellungen → Dateien & Links → **„[[Wikilinks]] verwenden" aus**,
**„Neue Linkformatierung" = „Relativer Pfad zur Datei"**, **„Links automatisch aktualisieren" an**.
Ohne das schreibt Obsidian Wikilinks und das Bundle ist nicht mehr portabel.

Versioniert wird nur die Konfiguration, nicht der Sitzungs-State (`workspace*.json`, Caches
— siehe `.gitignore`).

## OKF-Version

Dieses Bundle zielt auf **OKF v0.2** (deklariert als `okf_version` im Frontmatter von
`okf/index.md`). Übernommen sind `generated: { by, at }`, `verified: [ { by, at } ]`,
`status: draft|stable|deprecated`, `stale_after` sowie `sources` mit Fußnoten-Attribution
(`[^source-id]`). Nicht übernommen: der Typ `Attested Computation`.

Normative Quelle, die vollständige Nutzungs- und Abweichungstabelle sowie die Update-Prozedur
bei einer neuen Spec-Version stehen in **[okf/okf-spec.md](okf/okf-spec.md)**.

OKF ist kein offizielles Google-Produkt und ausdrücklich in Entwicklung. Dieses Kit steht in
keiner Verbindung zu Google oder den Spec-Autoren.

## Lizenz

[MIT](LICENSE) — nimm es, ändere es, veröffentliche deine Variante. Attribution ist nett,
aber nicht nötig.
