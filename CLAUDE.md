# CLAUDE.md — Regeln für Agenten

Persönliches Wissens-Brain im **Open Knowledge Format (OKF)**. Du liest und erweiterst es.
Details zu Typ-Taxonomie, Frontmatter und Soul/Memory-Schema: [CONTRIBUTING.md](CONTRIBUTING.md).

> **Diese Datei ist eine Vorlage.** Stellen in spitzen Klammern (`<account>`, `<kuerzel>`,
> `<Aufgabenwerkzeug>`) sind auszufüllen. Abschnitte, die als *Beispiel* markiert sind, ersetzt
> du durch deine eigenen — oder streichst sie. Was hier steht, liest der Agent als Gesetz;
> nicht zutreffende Regeln sind schlimmer als fehlende.

## Zuerst lesen
- Start: `okf/index.md` → `arbeit/`, `privat/` oder `methoden/` → Index des relevanten Bereichs → Konzepte.
- **Gezielte Frage → zuerst `python suche.py "<frage>"`** (im Account mit `--bereich`, im
  Arbeitskontext mit `--ohne-privat`) statt Index-Ketten abzulaufen. Bei großen Records nur den
  genannten Abschnitt lesen: `python suche.py --abschnitt <pfad> "<überschrift>"`. Die
  Criticality-Regeln gelten für Suchtreffer genauso.
- Bei Account-Arbeit (`arbeit/<account>`): zuerst `soul/profil.md` + `soul/never-do.md`; beim
  Schreiben von Content zusätzlich `soul/stil.md`, `soul/zielgruppe.md`, `soul/keyword-map.md`.
- Wiederkehrende Aufgabe → `pattern`-Records, strategische Frage → `decision`-Records. **Beide
  über den `type` suchen, nicht über den Ordner** — außerhalb der Accounts gibt es kein `memory/`
  (Details unter „Challenge vor jeder decision").

## Denkrahmen (immer mitlaufen lassen)

*Beispiel — ersetze ihn durch deinen eigenen Denkrahmen oder streiche den Abschnitt.*

Hier steht der Rahmen, den der Agent bei **jeder** nennenswerten Aufgabe anlegen soll. Das
Beispiel unten ist Robert Fritz' **Structural Tension**:

1. **Vision** benennen — welches *Endergebnis* (nicht: Problem, nicht: Prozess) soll entstehen?
2. **Aktuelle Realität** ehrlich beschreiben — wo stehen wir wirklich (ohne Beschönigung/Drama)?
3. **Die Diskrepanz halten und handeln** — die Lücke ist der Treibstoff; nicht durch „realistisch
   sein" (Vision senken) oder Wegschauen (Realität verzerren) vorzeitig auflösen.

Leitfrage statt „Wie mache ich das Problem weg?": **„Welches Ergebnis will ich erschaffen — und
welche Struktur muss ich dafür annehmen?"**

Zwei Konstruktionsprinzipien, die für jeden Denkrahmen an dieser Stelle gelten:

- **Den Rahmen anwenden, ohne ihn aufdringlich zu erwähnen.** Er prägt das Vorgehen, nicht die
  Wortwahl. Ein Agent, der in jedem Absatz seine Methode benennt, arbeitet nicht damit — er zitiert sie.
- **Die Theorie gehört ins Brain, nicht hierher.** In `okf/methoden/` als eigener Record, von
  hier aus verlinkt. Diese Datei sagt *dass* der Rahmen gilt, nicht *was* er im Detail besagt.

## Antwortform (gegenüber dem Menschen — nicht für Brain-Records)
- **Antwort zuerst:** Der **erste Satz** beantwortet die Frage. Begründung, Kontext, Einschränkungen
  und Alternativen kommen danach. Bei „ja, aber" steht das Ja im ersten Satz, das Aber im zweiten.
  Gilt auch für unangenehme Befunde und für „weiß ich nicht" (siehe Criticality → `controlled`).
  Kein Vorlauf, der die Frage wiederholt oder ankündigt, was gleich kommt.
- **Fork statt Dump:** Steht eine Entscheidung an, endet der Turn mit **nummerierten
  Anschlussoptionen** statt mit allen Wegen gleichzeitig ausgebreitet. Zwei bis vier Optionen,
  je eine Zeile, jede eine **Handlung** („1. Maßnahme im Record eintragen", „2. Erst die Zahlen
  prüfen"). Der Mensch wählt per Nummer. Ist nur ein Weg sinnvoll: diesen nennen, kein Scheinmenü
  bauen. Rückfragen zum Auftrag gebündelt stellen, nicht einzeln nacheinander.

*Angelehnt an das DEJAN Chat Protocol (dejan.ai). Die übrigen Regeln von dort sind hier bereits
abgedeckt — „Verify before asserting" durch Grundprinzip 7, „Stay in scope" durch „Im Projekt
bleiben".*

## Projektarbeit (Zugriff & Grenzen)
- **Privat ist tabu:** In Arbeits-/Client-Kontext nie `okf/privat/` heranziehen.
- **Im Projekt bleiben:** Primärkontext ist der aktuelle Account; schreibe Ergebnisse nur ins
  aktuelle Projekt, nicht in andere.
- **Geteiltes Wissen lesen:** `arbeit/quellen/`, account-übergreifende Fachmethodik unter
  `arbeit/` und `methoden/` gelten account-übergreifend.
- **Wessen Marke?** Nicht der Auftraggeber entscheidet, sondern **für wen das Artefakt entsteht**.
  - **Im Mandat für den Kunden erstellt** — Report, Analyse, Audit, Auswertung, Slides zum Ergebnis
    — trägt **dessen** CI. Grundlage ist ein `design-system.md` im Mandatsordner
    (`arbeit/<account>/`); fehlt es, wird es zuerst erfasst statt improvisiert.
  - **Asset, das beim Kunden erscheint** (Website-Content, Grafik für dessen Blog, Post in dessen
    Kanal) trägt ebenfalls **dessen** CI.
  - **Eigenauftritt und Akquise** (Angebot, Pitch, Rechnung, eigene Website, Vortrag, Fallstudie
    unter eigener Marke) trägt **deine** CI (Record unter `arbeit/<firma>/`,
    `criticality: controlled`, Farben und Schriften exakt).

  *Im Ursprungs-Brain stand die Regel zuerst andersherum („Beratungs-Deliverable = deine CI")
  und wurde gekippt. Welche Grenze für dich gilt, ist eine Entscheidung — schreib sie hier auf,
  sonst rät der Agent bei jedem Report neu.*
- **Werkzeug-Grenzen deklarieren:** Externe Werkzeuge (Aufgabenverwaltung, CRM, Analytics-Zugänge)
  gehören meist nur zu **einem** Account. Schreib hier auf, welches Werkzeug in welchem Kontext
  benutzt werden darf — sonst legt der Agent die Aufgabe eines Kunden im Projekt eines anderen an.
  Beispiel: *„`<Aufgabenwerkzeug>` nur im Kontext `arbeit/<account-a>`, nicht bei
  `arbeit/<account-b>`. Dort leben Maßnahmen und Status im jeweiligen Projekt-Brain."*
- **Methoden sind bereichsübergreifend:** `okf/methoden/` darf in **Arbeit und privat**
  herangezogen werden — ist also nicht tabu, anders als `privat/`.
- **Mandantentrennung mit Lern-Ausnahme:** Vertrauliche Details eines Kunden nie in die Arbeit
  für einen anderen übernehmen. Aus `memory/patterns/` + `memory/decisions/` anderer Projekte
  darfst du aber *methodische* Learnings ziehen („was hat dort funktioniert, was wäre hier einen
  Versuch wert") — als Anregung, ohne kundenspezifische Inhalte zu übertragen.

## Criticality — Retrieval-Verhalten
Vor dem Verwenden eines Records dessen `criticality` bestimmen (Feld, sonst Typ-Default). Sie steuert, wie
deterministisch der Abruf sein muss:
- **controlled:** Ausschließlich den freigegebenen Record nutzen. Fehlt er, ist er `status: deprecated`
  oder `stale_after` überschritten → **anhalten und nachfragen**, niemals aus Web/RAG/Erinnerung
  rekonstruieren. „Ich weiß es nicht" ist hier die richtige Antwort statt einer geratenen.
- **hybrid:** Record ist Autorität und Startpunkt; ergänzende Details aus Tools erlaubt, dürfen ihm nicht widersprechen.
- **flexible:** frei aus jeder Quelle.

Default bei fehlendem Feld (Details: CONTRIBUTING.md): `reference`/`metric`/`decision` → controlled;
`note`/`source`/`pattern` → flexible; alles andere → hybrid. `never-do.md` ist explizit `controlled`.

`stale_after` in der Vergangenheit = Record veraltet: controlled → wie fehlend behandeln,
hybrid → nicht mehr als Autorität verwenden. Beim **Schreiben** gilt: zeitgebundene Records
(Kampagnen, Promos, Snapshots) bekommen `stale_after`; volatile Einzelfakten im Body (Preise,
Rankings, Traffic-/Marktzahlen, Feature-Stände) mit `(Stand: YYYY-MM, Quelle)` datieren.

## NIE ins Brain
- **Zugangsdaten** (Passwörter, PINs, API-Keys, Tokens, Logins). **Erlaubt** sind dagegen
  Identifikations- und Geschäftsnummern (Kontonummer/IBAN, Steuer- und USt-IdNr., Vertrags-,
  Versicherungs- und Darlehensnummern) und technische Kennungen ohne Zugangswirkung (Tenant-/App-IDs,
  Projekt-IDs, öffentliche IPs). Sie bei Reviews nicht entfernen und nicht als Befund melden —
  tabu ist, was Zugang verschafft, nicht was etwas identifiziert.
- **Rohmaterial** (Mails, Transkripte, Protokolle, Briefings) — nur das Destillat. Office- und
  Datenexporte (`.docx`/`.doc`, `.xlsx`/`.xls`, `.csv`) fängt die `.gitignore` deshalb pauschal ab:
  Sie landen im Repo-Root oder in `_inbox/`, werden destilliert und danach gelöscht.
- **Todos** — die gehören ins `<Aufgabenwerkzeug>`. Das Durable (die Entscheidung + Warum) kommt
  als `decision` ins Brain und verlinkt per `resource:` auf die Aufgabe.

## Grundprinzipien
1. **OKF-konform:** Bundle-Root `okf/`. Ein Konzept = eine `.md`. Pfad ohne `.md` = permanente ID.
   Genutzte Version, normative Quelle und bewusste Abweichungen: [okf/okf-spec.md](okf/okf-spec.md).
2. **`type` ist Pflicht** im YAML-Frontmatter (Taxonomie: CONTRIBUTING.md).
3. **Nur relative Markdown-Links** (`[Text](../bereich/konzept.md)`) — nie `[[Wikilinks]]`/`![[Embeds]]`.
4. **Ein Thema, eine lebende Datei:** aktualisieren statt duplizieren, dann `generated.by` +
   `generated.at` setzen (OKF v0.2; die Felder lösen das alte `timestamp` ab). Ein bestehendes
   `verified` bei inhaltlicher Änderung **leeren** — die alte Bestätigung gilt nicht mehr.
   **Nur eine geänderte Aussage zählt als inhaltlich.** Reine Verweis-Ergänzungen (Verwandtes,
   Index-Zeile, Querverweis) lassen `generated` unverändert — sonst meldet der Validator bei
   jedem Record, der per `basiert_auf` daran hängt, eine geänderte Voraussetzung.
5. **`index.md` mitpflegen** beim Anlegen/Umbenennen; beim Umbenennen alle Links mitziehen.
6. **Quellen verlinken:** `resource:` im Frontmatter und/oder Body-Link; externe Literatur als
   `source` in `okf/arbeit/quellen/` und von dort in die Konzepte verlinken. Stützt eine Quelle
   eine Behauptung, zusätzlich in `sources:` aufnehmen (`id` + `resource` sind Pflicht) und den
   belegten Satz im Body mit `[^<id>]` markieren. Reine Weiterführungs-Links bleiben Body-Links.
7. **Keine erfundenen Fakten:** im Zweifel `status: draft` + Lücke im Body notieren.
   `status` kennt nur `draft` | `stable` | `deprecated` (OKF v0.2; fehlend = `stable`).
   `verified` **nie** stellvertretend für den Menschen setzen — nur er trägt `human:<kuerzel>` ein.
8. **Nicht löschen,** sondern `status: deprecated` + `ersetzt_durch:` (relativer Pfad auf den
   Nachfolger) + Link im Body.
9. **Beziehungen deklarieren** — drei Felder, drei verschiedene Konsequenzen:
   - `abgeleitet_aus:` + `stand:` — der Record *referiert* den Zustand anderer (Inventar, Index mit
     Betriebszuständen). Ändert sich eine Quelle, ist hier eine **Aussage** nachzuziehen und `stand`
     hochzusetzen. Die `description` zählt mit — sie wird zuerst gelesen und veraltet am leichtesten.
   - `basiert_auf:` — die Entscheidung *fußt* auf der Aussage eines anderen Records. Kippt die
     Voraussetzung, ist die **Entscheidung** neu zu bewerten — und das Ergebnis der Nachprüfung
     gehört datiert in den Record (Workflow unten).
   - `blockiert_durch:` — offene Vorbedingung. Was **mehr als einen** Record aufhält, bekommt einen
     **eigenen Record**; sonst ist der Engpass nirgends zählbar.
10. **Richtigstellen, nur Kipppunkte datieren:** Der Fließtext sagt immer den aktuellen Stand —
   veraltete Sachaussagen direkt korrigieren, keine Korrektur-Blöcke oder Durchstreichungen; die
   Historie liegt in Git. Nur eine **gekippte Entscheidung/Empfehlung** bekommt eine einzeilige
   `> **Korrektur JJJJ-MM-TT:**` — **mit ISO-Datum in derselben Zeile**, sonst fällt sie aus
   `chronik.py` heraus. Alte Blöcke beim nächsten Bearbeiten einarbeiten.
11. **Am Ende `python validate_okf.py`** laufen lassen, Fehler beheben, Warnungen mit dem Ergebnis
   berichten.

## Workflows (immer Destillat, kein Rohtext)
- **Betriebszustand geändert (Dienste, Infrastruktur, Kampagnen-/Projektstatus):** zuerst den
  **Detail-Record** ändern — er ist die Quelle. Dann den Validator laufen lassen: seine
  Warnungen zeigen, welche Inventare und Indizes nachzuziehen sind. Nie den Zustand nur in der
  Übersicht ändern; sie ist abgeleitet, nicht maßgeblich.
- **Validator meldet „Voraussetzung wurde später geändert":** Die Warnung heißt nicht, dass die
  Entscheidung gekippt ist — sie heißt, dass sie **ungeprüft** ist. Prüfen, indem du im geänderten
  Quell-Record nachsiehst, *welche* Größen sich geändert haben, und sie gegen die Größen stellst,
  auf denen dieser Record wirklich fußt. Eine Quelle kann sich stark ändern, ohne die tragende
  Aussage zu berühren.
  Dann das Ergebnis **datiert in den Record schreiben** — Blockzitat oben im Body:
  `> **Voraussetzung geprüft JJJJ-MM-TT:** <Quelle> wurde am <Datum> geändert — <was sich änderte>.
  <Warum die Aussage trägt / warum nicht.>` — und im Frontmatter je geprüfter Quelle
  `geprueft: - { quelle: <pfad wie in basiert_auf>, at: JJJJ-MM-TT }` eintragen. **`generated.at`
  nicht anfassen** — sonst warnt jeder Record, der auf diesem aufbaut, und weitere gemeldete
  Voraussetzungen desselben Records verschwinden ungeprüft (Details: CONTRIBUTING.md). Ohne diesen Vermerk
  kommt die Warnung bei jedem Lauf wieder und der nächste Leser muss den Vergleich neu anstellen:
  das Wissen war da, nur nicht im Brain. Trägt die Aussage **nicht** mehr, ist es keine Prüfnotiz,
  sondern eine Korrektur (Grundprinzip 10) und ggf. ein `status: deprecated`.
- **Widersprechen sich zwei Records:** nicht dem folgen, der zuerst gelesen wurde. `generated.at`
  beider vergleichen, den älteren richtigstellen (Grundprinzip 10: Sachaussage direkt korrigieren,
  bei gekippter Entscheidung eine datierte Zeile) und den Widerspruch benennen.
- **Frage nach einem Einzelobjekt (eine URL, ein Gerät, ein Kunde):** Die Antwort besteht aus
  **zwei** Teilen — dem Record zu diesem Objekt **und allen** übergreifenden Records des
  Bereichs. Eine bereichsweite Festlegung gilt für **jedes** Objekt mit, auch wenn sie es nicht
  namentlich nennt. Nur den Einzel-Record zu lesen beantwortet die Frage nicht — die Antwort
  sieht aber vollständig aus. Leg dafür eine feste Ordnertrennung an, z.B.
  `<bereich>/einzeln/` und `<bereich>/uebergreifend/`.
- **Maßnahme betrifft mehrere Objekte:** an **jedem** betroffenen Ort vermerken, nicht nur beim
  naheliegenden „Haupt"-Record. Jeder Ort beschreibt seine eigene Sicht — was dort passiert ist,
  was dort offen ist — plus Link auf die Gegenstelle. Die Begründung bleibt einmalig in der
  `decision`.
- **Quelle** (Artikel/Paper): `source`-Notiz in `okf/arbeit/quellen/` — 3–6 Kernpunkte +
  `resource:`-Link aufs Original + relative Links zu betroffenen Konzepten. Kein Volltext.
- **Meeting:** Destillat (Datum, Teilnehmer, Kontext, Entscheidungen + Warum, Erkenntnisse) im
  `meetings/`-Unterordner des Bereichs. Action Items → `<Aufgabenwerkzeug>`. Große Entscheidungen
  ggf. als eigenen `decision`-Knoten rausziehen und verlinken.
- **Inbox (`_inbox/`):** Capture → Destillieren → Rohdatei löschen. Kein Archiv. Sensibles
  (Befunde, Verträge, alles mit Identifikatoren) gehört nicht ins Git/Remote — schwärzen oder
  gar nicht erst ablegen.
- **Deliverables (`_outputs/`):** Reports raus, Erkenntnisse rein. Durables ins passende
  `okf/`-Konzept destillieren; die Report-Datei selbst nicht ins `okf/` oder den Root.
- **Neue Erfahrung:** `decision` → `memory/decisions/` (mit Warum + Quelle, optional `resource:`
  auf die Aufgabe); wiederkehrendes Muster → `memory/patterns/`. Soul nur bewusst ändern.
- **Challenge vor jeder decision:** Vor jeder neuen Entscheidung und jeder strategischen Empfehlung
  im Geltungsbereich nach `^type: decision` und `^type: pattern` **greppen** — über den Typ, nie über
  den Ordner. Ein erheblicher Teil der Entscheidungen liegt nicht in einem `memory/decisions/`;
  außerhalb der Accounts gibt es das Schema gar nicht. Geltungsbereich ist der Account- bzw.
  Bereichsordner; andere Projekte nur methodisch (siehe Mandantentrennung).
  Widerspricht die Historie dem Vorhaben → die Fundstellen **wörtlich vorhalten**, nicht still
  überschreiben. Geprüfte Records in der neuen decision unter „Geprüfte Historie" verlinken. Auch
  „nichts gefunden" ist ein Ergebnis — **mit Angabe, welcher Bereich durchsucht wurde.**

## Werkzeuge im Repo-Root

Alle vier nur Standardbibliothek, aus dem Repo-Root aufzurufen:

| Skript | Beantwortet | Wann |
|---|---|---|
| `python validate_okf.py` | Ist das Brain formal in Ordnung? Welche Vorbedingung blockiert am meisten? | **immer am Ende einer Änderung** |
| `python offene_punkte.py <bereich>` | Woran hier weiterarbeiten? | bei „was ist offen" |
| `python chronik.py <bereich> --art gekippt` · `--seit JJJJ-MM-TT` | Was wurde wann gekippt, was hat sich seit X geändert? | bei Fragen zur Historie |
| `python suche.py "<frage>"` · `--abschnitt <pfad> "<überschrift>"` | Welcher Record beantwortet das — und welcher Abschnitt darin? | **vor dem Lesen**, bei jeder gezielten Frage |

`validate_okf.py` meldet Fehler (Exit ≠ 0) und Warnungen (brechen nichts): überschrittenes
`stale_after`, veraltete abgeleitete Sichten, wacklige Voraussetzungen, `deprecated` ohne
Nachfolger, doppelte Titel, Links auf abgelöste Records.
Dazu der Block **Lesbarkeit** (reine Hinweise): `description` über 200 Zeichen, Records über
25 KB, `index.md` über 10 KB. **Beim Anlegen oder Ändern eines Records** die Regeln aus
CONTRIBUTING.md („Lesbarkeit für Agenten") einhalten: `description` = was steht drin + wann
lesen, kein Zustand; ein Record beantwortet eine Frage, sonst Hub + Teile.

## Neuer Typ nötig?
Ergänze ihn **im selben Arbeitsschritt** in [CONTRIBUTING.md](CONTRIBUTING.md) (Ein-Satz-Definition).

## Beim Kompaktieren behalten
Die 11 Grundprinzipien, die Antwortform, offene Validator-Befunde und die Liste geänderter Dateien.
