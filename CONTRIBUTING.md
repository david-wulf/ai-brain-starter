# CONTRIBUTING.md — Konventionen (für Menschen)

Dieses Brain folgt dem **Open Knowledge Format (OKF)**, aktuell **Version 0.2**. Hier sind
die Regeln und die Typ-Taxonomie für die tägliche Pflege.

> Wo OKF definiert ist, welche Version genutzt wird, wo dieses Bundle bewusst von der Spec
> abweicht und wie bei einer neuen Version nachgezogen wird:
> **[okf/okf-spec.md](okf/okf-spec.md)**. Dieses Dokument hier ist die Hausordnung —
> strenger als die Spec, aber nie im Widerspruch zu ihr.

## Die wichtigsten Regeln in Kürze

- **Bundle-Root ist `okf/`.** Alles darunter ist Wissen, alles darüber (README, CLAUDE,
  dieses Dokument, Validator, `templates/`) ist Tooling.
- **Ein Konzept = eine Datei.** Pfad ohne `.md` = permanente ID.
- **`type` ist Pflicht** im Frontmatter. Alle anderen Felder optional.
- **Relative Markdown-Links** (`[Text](../bereich/konzept.md)`), **nie** `[[Wikilinks]]`
  oder `![[Embeds]]`.
- **Jeder Ordner hat eine `index.md`** mit verlinkter Liste seiner Konzepte.
- **Ein Thema, eine lebende Datei** — aktualisieren statt duplizieren.
- **`description` höchstens 200 Zeichen** — was steht drin, wann lese ich das; kein Zustand.
- **Ein Record beantwortet eine Frage** — ab 25 KB aufteilen prüfen, ab 40 KB fällig (Hub + Teile).
- **Abgeleitete Sichten deklarieren** — fasst ein Record den Zustand anderer zusammen,
  trägt er `abgeleitet_aus:` + `stand:` (siehe unten). Der Validator prüft die Aktualität.
- **Abhängigkeiten deklarieren** — `basiert_auf:` für Voraussetzungen, `blockiert_durch:` für
  offene Vorbedingungen. Was mehr als einen Record aufhält, bekommt einen eigenen Record.
- **Richtigstellen statt markieren** — veraltete Sachaussagen direkt im Text korrigieren (Historie
  in Git). Nur gekippte Entscheidungen bekommen eine einzeilige `> **Korrektur JJJJ-MM-TT:**`,
  immer mit ISO-Datum in derselben Zeile.
- **Keine erfundenen Fakten** — im Zweifel `status: draft` und Lücke notieren.
- **Nicht löschen**, sondern `status: deprecated` + `ersetzt_durch:` auf den Nachfolger.
- **`status` kennt genau drei Werte** (OKF v0.2): `draft` → `stable` → `deprecated`.
  Fehlt das Feld, gilt der Record laut Spec als `stable`.

## Frontmatter-Template

```yaml
---
type: project            # PFLICHT — aus der Taxonomie unten
title: Kurzer Anzeigename
description: Was steht drin — wann lese ich das. Max. 200 Zeichen, kein Zustand.
resource: https://...    # optional: kanonische Quelle/URI (Aufgabe, Doc, Dashboard, DOI)
criticality: hybrid      # Eigen-Extension: controlled | hybrid | flexible (sonst Typ-Default)
stale_after: 2026-09-30  # optional: nur für zeitgebundene Records (ISO 8601); fehlt = dauerhaft
abgeleitet_aus:          # Eigen-Extension: Quell-Records, deren Zustand dieser Record referiert
  - ../bereich/quelle.md
stand: 2026-08-12        # Eigen-Extension: bis hierhin nachgezogen (Pflicht bei abgeleitet_aus)
basiert_auf:             # Eigen-Extension: Records, auf deren Aussage dieser hier fußt
  - ../bereich/voraussetzung.md
geprueft:                # Eigen-Extension: je Voraussetzung das Datum der Nachprüfung
  - { quelle: ../bereich/voraussetzung.md, at: 2026-09-28 }
blockiert_durch:         # Eigen-Extension: offene Vorbedingungen (eigener Record, wenn mehrfach)
  - ../bereich/blocker.md
ersetzt_durch:           # Eigen-Extension: nur bei status: deprecated — Pfad auf den Nachfolger oder `keiner` (dann Begründung im Body)
umfang_ok: Begründung    # Eigen-Extension: nur für Records, die bewusst über 25 KB bleiben
tags: [beispiel, format]
generated:               # OKF v0.2 — löst das alte `timestamp` ab
  by: claude/opus-5.5    # wer den Inhalt erzeugt hat: human:<kuerzel> | claude/<modell> | <agent>
  at: 2026-07-26         # letzte inhaltliche Änderung (ISO 8601)
verified:                # OKF v0.2 — Bestätigungen; leere Liste = ungeprüft
  - { by: human:<kuerzel>, at: 2026-07-26 }
owner: <kuerzel>         # Eigen-Extension: wer besitzt das Konzept
status: stable           # draft | stable | deprecated (fehlt = stable)
---
```

**Felder ohne Wert weglassen:** kein leeres `resource:`, kein `verified:` ohne Eintrag, kein
`stale_after:` ohne Datum. Ein fehlendes `verified` heißt „ungeprüft". Für `generated.by` gilt
eine Schreibweise: `claude/<modell>` mit Punkt in der Version, z. B. `claude/opus-5.5`.

### `generated` und `verified` (OKF v0.2)

Ein Brain wie dieses wird überwiegend von Agenten geschrieben und von einem Menschen kuratiert —
genau die Situation, für die v0.2 die Trust-Felder eingeführt hat:

- **`generated.by`** — wer den *Inhalt* erzeugt hat. Bei jeder inhaltlichen Änderung mitsetzen.
- **`generated.at`** — ISO-Datum der letzten inhaltlichen Änderung. Ersetzt `timestamp`
  vollständig; der Validator warnt, wenn es fehlt. Reine Verweis-Ergänzungen (Verwandtes,
  Index-Zeile, Querverweis) sind keine inhaltliche Änderung und lassen es unverändert.
- **`verified`** — Liste unabhängiger Bestätigungen, jeweils `{ by, at }`. Ein Eintrag mit
  `by: human:<kuerzel>` hebt den Record auf den Trust-Tier *human-reviewed*. Leere Liste heißt
  *unverified* — das ist ein ehrlicher Zustand, kein Makel.
- Faustregel: Ein Record mit `criticality: controlled` **sollte** mindestens eine
  menschliche Bestätigung tragen. Bestätigungen werden beim Durchsehen nachgetragen, nicht
  pauschal gesetzt — und ein Agent trägt sie **nie** stellvertretend ein.

### `sources` und Fußnoten (OKF v0.2)

`sources` listet die Materialien, aus denen ein Konzept abgeleitet ist — **nicht** jeden Link,
der im Text vorkommt. Faustregel: Stützt die Quelle eine Behauptung, gehört sie in `sources`;
führt sie nur weiter, bleibt sie ein normaler Body-Link.

```yaml
sources:
  - id: studie-2026-institut          # kurz, stabil, eindeutig im Dokument
    resource: ../quellen/studie-2026-institut.md   # URL oder relativer Pfad
    title: Titel der Studie
    author: Vorname Nachname
    last_modified: 2026-07-22
```

- **`id` und `resource` sind Pflicht** — der Validator bricht sonst ab. `title`, `author` und
  `last_modified` sind Credibility-Signale: OKF speichert Signale, **kein** Bewertungsurteil.
- **Interne Quellen** zeigen als relativer Pfad auf die `source`-Notiz in
  `okf/arbeit/quellen/`, nicht direkt auf die externe URL — die steht in der Notiz.
- **Body-Links bleiben.** `sources` ersetzt sie nicht; der Graph und die Lesbarkeit leben davon.
- **Fußnoten für einzelne Aussagen:** Hinter einen belegten Satz `[^<source-id>]` setzen. Es
  braucht **keine** Fußnoten-Definition am Dateiende, wenn die `id` in `sources` steht — der
  Validator löst gegen beides auf und meldet Referenzen ins Leere.

  ```markdown
  Umsatz wird erst nach Ablauf der Rückgabefrist anerkannt. [^revenue-policy]
  ```

## Lesbarkeit für Agenten: `description` und Umfang

Ein Agent findet Wissen in zwei Schritten: Er liest `description`s (in Indizes, Suchtreffern,
Frontmattern) und entscheidet daran, welche Datei er öffnet — dann liest er die **ganze** Datei.
Beide Schritte kosten Kontext. Lange Descriptions machen den ersten Schritt teuer und veralten
schnell, große Dateien machen den zweiten teuer: Wer einen Absatz braucht, bezahlt alles. Die
zwei Regeln hier halten beide Schritte billig.

### `description`: höchstens 200 Zeichen — was steht drin, wann lese ich das

Die `description` ist ein **Filter**, keine Zusammenfassung. Sie beantwortet genau zwei Fragen:

1. **Was steht drin?** Gegenstand und Aspekte, die der Record abdeckt.
2. **Wann lese ich das?** Der Anlass, bei dem ein Agent diesen Record braucht.

Muster: `<Gegenstand> — <Aspekte>. Lesen bei <Anlass>.`

**Nicht in die `description`:** Betriebszustand („läuft", „noch ohne Konten", „installiert am …"),
Status (`draft` steht im Feld `status`), Zahlen, Preise, Rankings, offene Punkte, Ergebnisse von
Entscheidungen. All das gehört in den **Body**, wo es datiert wird und der Validator es verfolgen
kann. Ausnahme: Bei Ereignis-Records (Meetings, Chargen) ist das Datum Teil der Identität und darf
drinstehen.

| Schlecht (Zustand, 400+ Zeichen) | Gut (Filter, unter 200) |
|---|---|
| „Am 2026-09-23 in Container 136 installiert — Gateway v0.2.8 in Docker Compose mit Postgres und Redis … Läuft und ist healthy, aber noch ohne Konten, ohne Reverse-Proxy-Namen …" | „API-Gateway in Container 136 — Installation, Compose-Aufbau, Netz, offene Härtung. Lesen bei Betrieb, Update oder Zweckfrage gegenüber dem Proxy." |

Nebeneffekt: Enthält die `description` keinen Zustand, kann sie auch nicht veralten — das
entschärft den Fall aus dem Abschnitt [Abgeleitete Sichten](#abgeleitete-sichten-abgeleitet_aus--stand).

Der Validator meldet jede `description` über 200 Zeichen im Block **Lesbarkeit**. Ein Bestand
wird nicht auf einen Schlag umgeschrieben, sondern **beim nächsten Anfassen** des Records gekürzt.

**So wird eine zu lange `description` gekürzt, ohne dass etwas verloren geht:** Die alte Fassung
wandert **wörtlich** als Block direkt unter das Frontmatter —
`> **Kurzfassung** — bis JJJJ-MM-TT als description geführt, unverändert übernommen.` — und
die neue `description` folgt dem Muster oben. `generated.at` bleibt dabei **unverändert**: Das
Kürzen ist keine inhaltliche Änderung, und ein neues Datum würde über `basiert_auf` falsche
Warnungen auslösen oder echte verdecken (die Voraussetzung wäre dann scheinbar nicht mehr jünger
als die Entscheidung). Den Kurzfassung-Block beim nächsten inhaltlichen Anfassen des Records in
die datierten Abschnitte einarbeiten und entfernen.

### Umfang: ein Record beantwortet eine Frage — ab 25 KB aufteilen

**Faustwerte** (1 KB ≈ 250–300 Tokens deutscher Text):

| Umfang | Bedeutung |
|---|---|
| bis 15 KB | Normalfall |
| über 25 KB | **Aufteilen prüfen** — Validator meldet im Block Lesbarkeit |
| über 40 KB | **Aufteilen fällig** — Validator hebt es hervor |
| `index.md` über 10 KB | Index trägt Inhalt, der in die Detail-Records gehört |

**Der eigentliche Test ist nicht die Größe**, sondern: *Lässt sich der Record mit einer
`description` unter 200 Zeichen ehrlich beschreiben?* Wenn nicht, beantwortet er mehr als eine
Frage und ist zu teilen — auch unter 25 KB.

**So wird geteilt (Hub + Teile):**

1. **Der alte Pfad bleibt als Hub.** Er ist die permanente ID; eingehende Links bleiben gültig.
   Der Hub wird kurz: worum es geht, die Kernaussagen in wenigen Sätzen, je Teil ein Link mit
   einer Zeile „wann lesen". Der Hub bekommt **kein** `abgeleitet_aus`, solange er keinen
   Zustand der Teile behauptet.
2. **Teile als Geschwister mit Präfix:** `katalog.md` → `katalog-technik.md`,
   `katalog-inhalt.md` … Kein neuer Ordner, keine zweite `index.md` — die Teile stehen
   eingerückt unter dem Hub in der vorhandenen `index.md`. Erst ab etwa acht Teilen einen
   Unterordner anlegen. Überschriften beim Verschieben **nicht umbenennen**, dann bleiben Anker
   gleich und nur der Dateiname im Link ändert sich. Referenzfall im Ursprungs-Brain: ein
   Faktoren-Katalog von 76 KB wurde zu einem Hub von 10 KB plus sechs Teilen zwischen 5 und 18 KB.
3. **Schnitt nach Fragen, nicht nach Länge.** Jeder Teil beantwortet eine Frage, die jemand
   tatsächlich stellt. Die H1/H2-Gliederung ist ein Hinweis, keine Vorgabe.
4. **Frontmatter je Teil vollständig:** eigener `type` (ein Teil darf einen anderen Typ haben als
   der Hub), `criticality` nur übernehmen, wenn sie für den Teil gilt, `sources` nur die, die der
   Teil zitiert — samt Fußnoten. `verified` leer. **`generated.at` bleibt beim Datum des
   Originals**, solange der Inhalt nur verschoben und nicht geändert wird — sonst meldet der
   Validator bei allen Records, die per `basiert_auf` auf den Hub zeigen, eine Änderung, die
   es inhaltlich nicht gab. Erst wer den Inhalt eines Teils ändert, setzt ein neues Datum.
5. **Nichts geht verloren:** Datierte Korrekturen und Durchstreichungen wandern mit dem Absatz,
   zu dem sie gehören. Nicht umformulieren beim Verschieben.
6. **Links nachziehen:** Anker-Links auf den Hub (`hub.md#abschnitt`) auf den neuen Teil
   umbiegen — `grep -rn "hub.md#"`; der Validator prüft Anker nicht. Teile in die `index.md`
   des Ordners aufnehmen.

**Typ-spezifisch:**

- **`decision`** behält Entscheidung, Warum und „Geprüfte Historie". Umsetzungsdetails,
  Installationsschritte und Verlaufsprotokolle wandern in einen `system`- oder `process`-Record,
  auf den die Decision verlinkt.
- **Register und Tabellen** nach Zeitraum oder Charge teilen — oder, wenn die Tabelle nur als
  Ganzes Sinn ergibt, mit `umfang_ok: <Begründung>` im Frontmatter ausnehmen. Der Validator
  zählt diese Ausnahmen mit, meldet sie aber nicht.

## Typ-Taxonomie

Verwende einen dieser Werte im Feld `type`:

- **`project`** — ein abgegrenzter Effort: Ziel, Strategie, Entscheidungen, Learnings, Links
  zu Aufgaben/Quellen.
- **`playbook`** — wiederholbares, durables Wissen einer Methode/Strategie (Soll-Vorgehen).
- **`pattern`** — empirisches Erfahrungswissen pro Aufgabentyp: „was funktioniert / was bricht
  regelmäßig" (Ist-Wissen aus dem Tun). Abgegrenzt vom `playbook`: rauer, wachsend, beobachtet.
- **`process`** — fester Ablauf/Checkliste.
- **`guideline`** — Standard/Stilregel.
- **`system`** — Tooling/Infrastruktur (MCP-Setup, Datenbank-Config, Dienst im Heimnetz).
- **`entity`** — ein Thema/Begriff/Marke als Wissensknoten.
- **`metric`** — definierte Kennzahl.
- **`decision`** — eine getroffene Entscheidung samt Begründung (Was + Warum).
- **`reference`** — interne Fakten/Stammdaten (z.B. Property-Formate, Zugänge ohne Geheimnisse).
- **`note`** — alles andere Durable, das noch keinen festen Typ hat.
- **`source`** — eine externe Quelle (Paper, Artikel) als **destillierte** Notiz: Kernpunkte
  + `resource:`-Link aufs Original. Kein Volltext. Liegt in `okf/arbeit/quellen/` (Literatur zur
  Arbeit) bzw. `okf/methoden/quellen/` (Methodenquellen).
- **`meeting`** — destilliertes Ergebnis eines Meetings: Entscheidungen, Erkenntnisse, Kontext.
  Kein Transkript, keine Todos. Liegt im `meetings/`-Unterordner des jeweiligen Bereichs.

### Strukturell (kein Wissens-Konzept)

- **`index`** — reservierter Typ für die `index.md`-Navigationsdateien. Kein inhaltliches
  Konzept, nur Wegweiser.

> Braucht ein Konzept partout einen neuen Typ, ergänze ihn hier mit einer Ein-Satz-Definition
> — im selben Arbeitsschritt, in dem du das Konzept anlegst.

## Criticality (Governance)

Das optionale Feld `criticality:` sagt dem Agenten, **wie deterministisch** er einen Record nutzen darf —
abgeleitet aus der Frage „Was kostet es, wenn das hier falsch ist?". `type` bleibt einziges Pflichtfeld.

- **`controlled`** — falsch = rechtlich/kommerziell/Reputations-Risiko (Preise, Budgets, zugesagte
  Leistungen, freigegebene Claims, Stammdaten, harte Tabus). Der Agent nutzt **nur** diesen
  Record; fehlt er oder ist er `deprecated` → anhalten und nachfragen, nicht raten, kein Web/RAG-Ersatz.
- **`hybrid`** — wiederverwendet & qualitätsrelevant (Soul: Profil, Zielgruppe, Stil, Keyword-Map;
  Playbooks, Projekte). Record ist Autorität und Ausgangspunkt; Ergänzung aus Web/Connectors erlaubt,
  ohne ihm zu widersprechen.
- **`flexible`** — billig, wenn falsch (`_inbox`, Brainstorms, `note`, `source`, rohe `pattern`). RAG/Web frei.

**Du taggst nur die Ausnahmen.** Fehlt das Feld, gilt ein Default je `type`:

- `controlled`: `reference`, `metric`, `decision`
- `flexible`: `note`, `source`, `pattern`
- `hybrid`: alles andere (`entity`, `playbook`, `process`, `project`, `guideline`, `system`, `meeting`)

Ein explizit gesetztes `criticality:` schlägt den Typ-Default immer. Wichtigster Sonderfall:
**`never-do.md`** ist ein `guideline` (Default `hybrid`), muss aber explizit auf `controlled` stehen.

### Gültigkeit: `stale_after` + Claim-Datierung

- **`stale_after:`** — ISO-Datum für **zeitgebundene** Records (laufende Kampagnen, Promos,
  Quartals-Snapshots). Fehlt das Feld → der Record gilt als dauerhaft. Überschritten heißt:
  `controlled` → wie fehlend behandeln (anhalten, nachfragen), `hybrid` → nicht mehr als
  Autorität verwenden. Der Validator meldet das als **weiche Warnung** (bricht den Commit nicht);
  ein periodischer Health-Sweep listet die Fälle zur Entscheidung.
- **Claim-Datierung** — volatile **Einzelfakten im Body** (Preise, Rankings, Traffic-/Marktzahlen,
  Feature-Stände) mit `(Stand: YYYY-MM, Quelle)` markieren. `generated.at` sagt nur, wann die
  Datei zuletzt angefasst wurde — nicht, wie frisch jeder Fakt darin ist. Dauerhafte Aussagen
  (Methoden, Definitionen, Positionierung) brauchen keine Marke.

## Abgeleitete Sichten (`abgeleitet_aus` + `stand`)

Manche Records fassen den Zustand **anderer** Records zusammen: ein Inventar, eine
Bereichs-Übersicht, eine `index.md`, die Betriebszustände nennt. Solche Sichten sind bequem
und genau deshalb gefährlich — sie sehen aktuell aus, während die Quelle längst weiter ist.
Ein Agent liest die Übersicht zuerst und hält sie für die Wahrheit.

Deshalb sagt eine abgeleitete Sicht selbst, woraus sie stammt und wie weit sie nachgezogen ist:

```yaml
abgeleitet_aus:                        # relative Pfade auf die Quell-Records
  - dienst-a.md
  - dienst-b.md
stand: 2026-08-07                      # bis hierhin sind die Aussagen nachgezogen
```

**Der Validator prüft das.** Ist ein Quell-Record laut `generated.at` neuer als `stand`,
gibt es eine **Warnung** mit beiden Daten — der Commit bricht nicht, aber der Fall wird
sichtbar. Fehlt `stand` bei gesetztem `abgeleitet_aus`, ist es ein **Fehler**: ohne
Stichdatum lässt sich nichts prüfen. Nicht auflösende Pfade sind ebenfalls ein Fehler.

**Wann setzen:** sobald ein Record den Zustand eines anderen *referiert*, statt ihn zu
*besitzen*. Faustregel: Musst du beim Ändern von A überlegen, ob B nachgezogen werden muss,
dann gehört A in Bs `abgeleitet_aus`.

**Wann nicht:** bei normaler inhaltlicher Verlinkung. Ein `playbook`, das eine Methode
erklärt und dabei auf ein Konzept verweist, leitet nichts ab. `abgeleitet_aus` ist keine
zweite Link-Liste, sondern eine Abhängigkeitserklärung mit Prüfpflicht — je kürzer, desto
belastbarer.

**Reihenfolge beim Ändern einer Quelle:** Quelle aktualisieren → `python validate_okf.py` →
gemeldete abgeleitete Sichten nachziehen → dort `stand` hochsetzen. Nicht umgekehrt, und
nicht „mache ich später" — später ist genau der Zustand, den diese Felder verhindern sollen.

> **Warum es die Regel gibt.** Der Anlassfall im Ursprungs-Brain: Ein Inventar-Record behauptete
> fünf Tage lang, ein Dienst laufe wegen einer fehlenden Konfigurationsdatei nicht — obwohl der
> Detail-Record seit fünf Tagen den am laufenden System gegengeprüften Gegenbeweis trug.
> Dieselbe überholte Aussage stand zusätzlich in der `description` des Detail-Records selbst und
> in der Bereichs-`index.md`; für einen zweiten Dienst dasselbe Muster an zwei weiteren Stellen.
> Der Fehler war nicht fehlendes Wissen — er war eine abgeleitete Sicht, die ihre eigene
> Veraltung nicht anzeigen konnte.

**Die `description` ist auch eine abgeleitete Sicht.** Sie ist die Zeile, die ein Agent
zuerst liest, und sie veraltet am leichtesten, weil sie beim Ändern des Bodys gern
vergessen wird. Bei jeder inhaltlichen Änderung mitlesen und mitziehen.

## Abhängigkeiten: `basiert_auf` und `blockiert_durch`

Zwei Felder, die beantworten, was ein Ordner voller Dateien sonst nicht beantwortet: **worauf steht
diese Entscheidung, und was hält sie auf.**

```yaml
basiert_auf:                       # Records, auf deren Aussage dieser hier fußt
  - dienst-a.md
blockiert_durch:                   # offene Vorbedingungen
  - hardware-ausbau.md
```

**`basiert_auf`** ist nicht dasselbe wie `abgeleitet_aus`. Der Unterschied ist die Konsequenz:

- `abgeleitet_aus` → eine **Aussage** ist nachzuziehen (Inventar-Zeile, Index-Eintrag).
- `basiert_auf` → die **Entscheidung** ist neu zu bewerten. Kippt die Voraussetzung, kippt womöglich
  die Entscheidung selbst.

Der Validator warnt, wenn eine Voraussetzung `deprecated` ist oder **nach** dem eigenen Record
geändert wurde. Der Anlassfall im Ursprungs-Brain: Zwei Architektur-Entscheidungen bauten beide
darauf, dass ein Werkzeug Berechtigungen pro Zugangsschlüssel kennt. Am Tag X wurde am laufenden
System gemessen, dass die freie Version das **nicht** kann. Zwei Entscheidungen an einer
widerlegten Annahme — vorher nirgends sichtbar, weil die Annahme nur im Fließtext stand.

**Die Warnung schließen — datiert, nicht im Kopf.** Eine gemeldete Voraussetzung ist nicht
automatisch gekippt, sie ist *ungeprüft*. Die Prüfung vergleicht nicht zwei Records, sondern die
**Größen**: was hat sich in der Quelle konkret geändert, und fußt dieser Record auf genau diesen
Größen? Eine Quelle kann sich stark ändern, ohne die tragende Aussage zu berühren.

Das Ergebnis gehört an zwei Stellen in den Record — als Blockzitat oben in den Body (für den
Leser) und als Eintrag in `geprueft:` im Frontmatter (für den Validator), **je Quelle einer**:

```yaml
basiert_auf:
  - ../bereich/quelle.md
geprueft:
  - { quelle: ../bereich/quelle.md, at: 2026-09-28 }   # Pfad genau wie in basiert_auf
```

```markdown
> **Voraussetzung geprüft 2026-09-28:** [Quell-Record](../bereich/quelle.md) wurde am 2026-09-20
> geändert — <was sich konkret änderte>. An <den Größen, auf denen dieser Record fußt> hat sich
> nichts geändert. Die Entscheidung trägt damit weiter.
```

Der Validator schweigt dann für **diese eine Quelle**, bis sie nach dem Prüfdatum erneut geändert
wird. **`generated.at` bleibt unverändert** — eine Prüfnotiz ist keine inhaltliche Änderung.

> **Warum nicht einfach `generated.at` hochsetzen?** So stand es bis 2026-09-28 in der Regel, und
> ein Durchgang über 22 Warnungen im Ursprungs-Brain hat zwei Fehler gezeigt: (1) Jeder hochgesetzte Record löst bei
> allen Records, die auf *ihm* aufbauen, eine neue Warnung aus — geändert hat sich dort aber nur
> die Prüfnotiz. Aus 22 Warnungen wurden Folge-Warnungen in der nächsten Ebene, beim Schließen
> wieder die nächste. (2) Hat ein Record mehrere gemeldete Voraussetzungen, verdeckt das
> Hochsetzen nach der ersten Prüfung **alle übrigen ungeprüft**. `geprueft:` je Quelle behebt beides.

Ohne diesen Vermerk meldet der Validator denselben Fall bei jedem Lauf, und der nächste Leser muss
den Vergleich von vorn anstellen — das Wissen existierte, stand aber nicht im Brain. Trägt die
Aussage **nicht** mehr, ist es keine Prüfnotiz, sondern eine Korrektur (siehe „Änderungen im Body —
richtigstellen, nur Kipppunkte datieren"), dann ändert sich der Inhalt und `generated.at` wird hochgesetzt; je nach Tragweite
zusätzlich `status: deprecated` + `ersetzt_durch:`. Auch „in der Quelle stand nur eine
Prüfnotiz, inhaltlich hat sich nichts bewegt" ist ein Ergebnis und wird so hingeschrieben.

**`blockiert_durch`** macht Vorbedingungen zählbar. Steht ein Blocker in mehreren Records als
Nebensatz, ist er nirgends als der Engpass erkennbar, der er ist. Deshalb gilt: **Was mehr als einen
Record aufhält, bekommt einen eigenen Record** und wird von dort referenziert. Der Validator listet
am Ende jedes Laufs, welche Vorbedingung wie viele Records blockiert.

## Änderungen im Body — richtigstellen, nur Kipppunkte datieren

**Der Fließtext sagt immer den aktuellen Stand.** Ist eine Sachaussage falsch oder veraltet
(Zahl, Pfad, Name, Konfiguration, erledigter Punkt), wird sie **direkt richtiggestellt** — kein
Korrektur-Block, keine Durchstreichung. Die Historie liegt in Git (`git log -p <datei>`).

**Datiert bleibt nur, was gekippt ist:** eine Entscheidung, Empfehlung oder Annahme, auf die
sich andere verlassen haben und die jetzt nicht mehr gilt. Dafür eine einzeilige Notiz an der
Stelle, an der die neue Aussage steht:

```markdown
> **Korrektur 2026-08-12:** Bis hierher galt X; seit … gilt Y, weil …
```

Bestehende Korrektur-Blöcke und Durchstreichungen werden beim nächsten Bearbeiten des Records
eingearbeitet: Sachkorrekturen in den Text, Kipppunkte auf eine Zeile verdichtet.

> **Warum nicht jede Änderung markieren?** Im Ursprungs-Brain galt zuerst „nicht überschreiben,
> sondern markieren" für jede überholte Aussage. Das ließ Korrektur-Blöcke neben dem falschen
> Fließtext stehen — der Leser (Mensch wie Agent) fand die falsche Aussage zuerst. Was sich nur
> sachlich geändert hat, braucht keine Spur im Text; Git hat sie ohnehin.

Erkannte Schlüsselwörter, jeweils mit ISO-Datum in derselben Zeile: *Korrektur, Geändert, Überholt,
Verworfen, Aufgegeben, Zurückgenommen, Widerrufen, Revidiert* sowie *Erledigt, Umgesetzt,
Gegengeprüft, Nachtrag, Behoben*.

Das ist keine Kosmetik: `chronik.py` erntet genau diese Marker und beantwortet daraus „was habe ich
wann gekippt", „was galt vorher" und „was hat sich seit Datum X geändert". **Ohne Datum in der Zeile
fällt der Eintrag aus der Chronik heraus.**

## Ablösung: `ersetzt_durch`

Records werden nicht gelöscht, sondern auf `status: deprecated` gesetzt — zusätzlich
maschinenlesbar, wohin der Verweis geht:

```yaml
status: deprecated
ersetzt_durch: nachfolger-record.md
```

Der Validator prüft, dass der Pfad auflöst, und warnt bei `deprecated` ohne Nachfolger sowie
bei `ersetzt_durch` ohne `deprecated`. Gibt es wirklich keinen Nachfolger, bleibt das Feld
leer und der Body begründet es.

## Sonderfall: Ereignisse vs. Themen

Die „ein Thema, eine Datei"-Regel gilt für **Themen**. **Ereignisse und externe Quellen**
sind naturgemäß pro Vorkommen eine Datei:

- Jedes Meeting → eine `meeting`-Datei (mit Datum im Dateinamen, z.B. `2026-06-16-kunde-x.md`).
- Jede externe Quelle → eine `source`-Datei in `okf/arbeit/quellen/` bzw. `okf/methoden/quellen/`.

Diese verlinken auf die jeweiligen Themen-Konzepte (`entity`, `project`, `playbook`), statt
deren Inhalt zu duplizieren.

## Soul/Memory — Account-Kontext

Für „Accounts" (eine eigene Marke/Site, jeder Kunde unter `arbeit/<account>/`) gilt ein Zwei-Schichten-
Schema, damit das volle Kontextwissen sauber lebt:

```
<account>/
├── soul/            # STABIL — Änderungen mit Reibung, vom Lead verantwortet
│   ├── index.md
│   ├── profil.md         (entity)     — was der Account wirklich ist
│   ├── zielgruppe.md     (entity)     — Sorgen, Sprache, Einwände
│   ├── stil.md           (guideline)  — Voice/Stil
│   ├── keyword-map.md    (reference)  — Themen/Keywords
│   └── never-do.md       (guideline)  — was nie tun (+ Warum)
└── memory/          # DYNAMISCH — leicht zu ergänzen
    ├── index.md
    ├── decisions/        — type: decision (Entscheidung + Warum + Quelle)
    ├── patterns/         — type: pattern  (was funktioniert/bricht)
    └── meetings/         — type: meeting  (Destillat, kein Protokoll)
```

- **Unterordner entstehen erst mit ihrem ersten Record.** `memory/decisions/`, `patterns/` und
  `meetings/` werden nicht auf Vorrat mit leerem `index.md` angelegt; bis dahin sagt der
  Eltern-Index in einer Zeile, dass es noch nichts gibt. Der Baum oben zeigt das volle Schema,
  nicht den Pflichtbestand. Grund aus dem Ursprungs-Brain: Sieben `meetings/`-Ordner enthielten
  nur ihren Index — leere Ordner sahen nach Bestand aus und kosteten bei jeder Pfadsuche einen
  Lesevorgang.

- **Soul** = stabiles Markenwissen. Nicht jede Beiläufigkeit rein, sonst verwässert die Schicht.
- **Memory** = Erfahrungswissen aus dem Tun. Jede neue Entscheidung/Erkenntnis sofort als
  gesourcten Eintrag.
- **Dieses Schema gilt nur für Accounts.** In Bereichen ohne Account-Charakter (Heimnetz,
  Finanzen, allgemeine Fachmethodik) liegen `decision`- und `pattern`-Records direkt im
  Bereichsordner — das ist richtig so und soll nicht nachträglich in ein `memory/`-Schema
  gezwungen werden. **Folge für das Suchen:** Der Bestand an Entscheidungen wird über den `type`
  gefunden, nie über den Ordnerpfad. Im Ursprungs-Brain lag die **Mehrheit** der `decision`- und
  `pattern`-Records außerhalb eines `memory/`-Ordners; eine pfadbasierte Suche findet die
  Minderheit und sieht dabei vollständig aus. Die Regel dazu steht in [CLAUDE.md](CLAUDE.md)
  unter „Challenge vor jeder decision".
- **Todos gehören nicht hierher** — die leben im Aufgabenwerkzeug. Das Durable (die Entscheidung
  + Warum) kommt als `decision` ins Brain und verlinkt per `resource:` auf die Aufgabe.
- **Keine Rohdaten** (Transkripte, Exporte, Credentials). „Store the lesson, not the raw data."

## Werkzeuge

Im Repo-Root, alle nur Standardbibliothek:

- `python validate_okf.py` — Format, Links, Indizes, Felder. **Am Ende jeder Änderung.** Listet
  außerdem aus, welche Vorbedingung (`blockiert_durch`) wie viele Records aufhält, und fasst im
  Block **Lesbarkeit** zu lange Descriptions und zu große Records zusammen (`--lesbarkeit` listet
  alle statt der zehn größten).
- `python offene_punkte.py <bereich>` — sammelt die offenen Punkte der Records ein.
- `python chronik.py <bereich> --art gekippt` — erntet die datierten Änderungsmarker.
- `python suche.py "<frage>"` — findet die passenden Records (BM25 über Titel, Description,
  Tags, Überschriften, Pfad). `--abschnitt <pfad> "<überschrift>"` liest nur einen Abschnitt.
  `--test` prüft die Trefferquote gegen `suche_testfragen.tsv`.

Details und Flags: [README.md](README.md).

## Pflege (gegen den „stale brain")

Ein veraltetes Brain ist schlimmer als keins — die KI klingt dann selbstsicher mit altem Kontext.

- Memory niedrigschwellig ergänzen; Soul nur bewusst ändern.
- Periodisch (z.B. quartalsweise) konsolidieren: Duplikate zusammenführen, veraltete Notizen
  raus bzw. `status: deprecated`, Konflikte auflösen, und je Soul-Datei fragen: „Ist das noch wahr?"
- **Wöchentlicher Health-Sweep** (z.B. als geplanter Agenten-Lauf, montags): prüft Staleness,
  tote Links, überschrittene `stale_after`, Verweise auf `deprecated`-Records und Widersprüche
  zwischen `decision`-Einträgen. Report landet in `_outputs/` — der Sweep ändert nichts selbst.
- **Abgeleitete Sichten** nachziehen, sobald der Validator sie meldet — das ist der billigste
  Pflege-Hebel überhaupt, weil er den Fall benennt statt ihn suchen zu lassen.

## Namenskonventionen

- Dateinamen: kleingeschrieben, Bindestriche statt Leerzeichen, ohne Umlaute
  (`projekt-kickoff.md`, `werkzeug-auswahl.md`).
- Meetings: `YYYY-MM-DD-kurz-titel.md`.
- Decisions in `memory/decisions/`: `YYYY-MM-DD-kurz-titel.md` mit dem Entscheidungsdatum.
- Quellen (`type: source`): `<thema>-<autor>.md`, bei mehreren Teilen eines Autors
  `<thema>-<autor>-<jahr>.md`. Bestehende Ausnahmen bleiben, neue Records folgen der Regel.
- Tags: klein, ASCII statt Umlaute (`persoenlichkeit`), Bindestriche, Bereichstag im Plural
  (`methoden`). Keine Tags, die ein Frontmatter-Feld doppeln (`deprecated`, `draft`) oder den
  Ordner wiederholen.
- `source`-Records dürfen zusätzlich `authors:` (Autor oder Organisation des Originals) und
  `source_type:` führen — Eigen-Extensions, nur für diesen Typ.
- Welten unter `okf/`: `arbeit/` (beruflich), `privat/` (persönlich) und `methoden/`
  (bereichsübergreifende Denk-/Schaffenswerkzeuge). In Arbeits-/Client-Kontext ist `privat/`
  tabu; `methoden/` ist es **nicht**.
- Unterordner legst du an, wenn du sie brauchst — nicht auf Vorrat. Ein Ordner mit einer Datei
  ist eine Datei mit Overhead.

> **Die Trennlinie, die am häufigsten schiefgeht:** `methoden/` trägt, *wie man etwas macht* —
> anwendbar auch von jemand anderem. `arbeit/<firma>/` trägt, *wie es bei dieser
> Firma konkret ist*. Farbwerte, Logo-Dateien und Domainlisten sind Instanz, nicht Methode.
> Im Ursprungs-Brain gab es dafür erst eine eigene Welt `personal-branding/`, die beides mischte
> — sie wurde aufgelöst, weil sich an jedem Record die Frage „Methode oder Instanz?" neu stellte.
