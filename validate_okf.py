#!/usr/bin/env python3
"""OKF-Validator (Ziel-Spec: OKF v0.2) — nur Standardbibliothek, keine Abhaengigkeiten.

Prueft das OKF-Bundle unter okf/:
  1. Jede .md-Datei hat einen Frontmatter-Block (zwischen --- ) mit einer type:-Zeile.
  2. Jeder relative Markdown-Link loest auf eine existierende Datei auf
     (externe http(s)-/mailto-Links und reine Anker werden uebersprungen).
  3. Jeder Ordner unter okf/ (inkl. okf/ selbst) enthaelt eine index.md.
  4. OKF-v0.2-Felder:
       status:      (falls gesetzt) draft | stable | deprecated
       stale_after: (falls gesetzt) gueltiges ISO-Datum
       generated.at:(falls gesetzt) gueltiges ISO-Datum
       verified:    (falls befuellt) Eintraege mit by: und at:
       sources:     je Eintrag id: + resource:, ids eindeutig, lokale
                    resource-Pfade muessen aufloesen
  5. Fussnoten-Referenzen [^id] im Body zeigen auf eine sources-id (oder auf
     eine eigene Fussnoten-Definition am Dateiende).
  6. Eigen-Extension: criticality: (falls gesetzt) controlled|hybrid|flexible.
  7. Abgeloeste v0.1-Feldnamen (timestamp:, valid_until:) werden als FEHLER gemeldet.
  8. Eigen-Extension Abgeleitete Sichten:
       abgeleitet_aus: Liste relativer Pfade auf die Quell-Records; jeder muss
                       aufloesen und verlangt ein 'stand:'-Datum.
       stand:          ISO-Datum, bis zu dem die abgeleiteten Aussagen nachgezogen
                       sind. Ist ein Quell-Record laut generated.at NEUER als
                       'stand', gibt es eine WARNUNG — die abgeleitete Sicht
                       koennte einen ueberholten Zustand behaupten.
       ersetzt_durch:  relativer Pfad auf den Nachfolge-Record; muss aufloesen.
                       'keiner' = bewusst ohne Nachfolger (Begruendung im Body).
                       Ohne 'status: deprecated' bzw. deprecated ohne Nachfolger
                       gibt es eine WARNUNG.
  9. Eigen-Extension Abhaengigkeiten:
       basiert_auf:    Records, auf deren Aussage dieser hier fusst. Ist eine
                       Voraussetzung 'deprecated' oder wurde sie NACH diesem
                       Record geaendert, gibt es eine WARNUNG -- die Entscheidung
                       koennte auf einer ueberholten Annahme stehen.
       geprueft:       Liste '- { quelle: <pfad wie in basiert_auf>, at: <ISO> }'.
                       Haelt fest, dass eine gemeldete Voraussetzungs-Aenderung
                       am Datum X nachgeprueft wurde und die Aussage traegt. Die
                       Warnung schweigt dann fuer diese eine Quelle, bis sie nach
                       X erneut geaendert wird. generated.at bleibt unberuehrt --
                       sonst loest jede Pruefnotiz eine Warnwelle bei allen
                       Records aus, die auf diesem hier aufbauen.
       blockiert_durch: Records, die als Vorbedingung offen sind. Der Lauf zaehlt
                       am Ende, welcher Blocker wie viele Records aufhaelt.
 10. Doppelte 'title:' werden als WARNUNG gemeldet -- gleicher Titel heisst,
     dass ein Agent zwangslaeufig mal den falschen Record erwischt.
 11. never-do.md muss explizit 'criticality: controlled' tragen (CONTRIBUTING.md,
     Abschnitt Criticality) -- sonst FEHLER.
 12. Link auf einen Record mit 'status: deprecated' aus einem aktiven Record ist
     eine WARNUNG -- ausser die Zeile kennzeichnet die Abloesung selbst
     (Woerter 'abgeloest', 'deprecated', 'ersetzt', 'ueberholt'/'überholt' oder
     Durchstreichung ~~). Quelle selbst deprecated -> keine Meldung.
 14. Lesbarkeit fuer Agenten (CONTRIBUTING.md, "Lesbarkeit fuer Agenten"),
     eigener Block HINWEISE, zaehlt weder als Fehler noch als Warnung:
       description ueber DESC_MAX Zeichen;
       Record ueber UMFANG_PRUEFEN Bytes (ueber UMFANG_FAELLIG hervorgehoben),
       index.md ueber INDEX_MAX Bytes. Records mit 'umfang_ok:' sind vom
       Umfangs-Hinweis ausgenommen und werden nur gezaehlt.
     Standard: Summen + die zehn groessten Faelle. --lesbarkeit listet alle.
 13. YAML-Parsebarkeit des Frontmatters: unquotierte Skalarwerte mit ': ' im
     Text (typisch in description/title) liest jeder YAML-Parser als
     verschachteltes Mapping und bricht ab -> FEHLER. Ist PyYAML installiert,
     wird zusaetzlich yaml.safe_load als Gegenprobe gefahren.

Abgelaufene stale_after-Daten werden als WARNUNG gemeldet (kein Exit-Code != 0),
damit natuerlich auslaufende Kampagnen-Records den Commit nicht brechen. Dasselbe
gilt fuer veraltete abgeleitete Sichten: sie sind ein normaler Zwischenzustand,
der auffallen, aber keinen Commit brechen soll.

Ausgabe: Zusammenfassung mit Datei + Zeile je Befund. Exit-Code != 0 bei Fehlern.

Aufruf:  python validate_okf.py [bundle-root] [--lesbarkeit]   (Default: ./okf)
"""

import datetime
import os
import re
import sys

try:  # optional, nur als Gegenprobe -- der Validator laeuft auch ohne
    import yaml as _yaml
except ImportError:  # pragma: no cover
    _yaml = None

# Zeilen, die eine Abloesung selbst benennen, duerfen auf deprecated-Ziele zeigen
ABLOESUNG_MARKER_RE = re.compile(
    r"abgel(ö|oe)st|deprecated|ersetzt|(ü|ue)berholt|~~", re.IGNORECASE)

# Inline-Markdown-Links: [text](ziel)
LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
# Schemata, die NICHT als lokale Datei geprueft werden
EXTERNAL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://")
# Erlaubte Werte fuer das optionale Feld criticality (Eigen-Extension):
VALID_CRITICALITY = {"controlled", "hybrid", "flexible"}
# Erlaubte Werte fuer status (OKF v0.2; fehlend bedeutet laut Spec "stable"):
VALID_STATUS = {"draft", "stable", "deprecated"}
# In v0.2 abgeloeste Feldnamen -> Nachfolger
# Lesbarkeit fuer Agenten (CONTRIBUTING.md) -- Schwellen, keine Fehler
DESC_MAX = 200          # Zeichen
UMFANG_PRUEFEN = 25_000  # Bytes: Aufteilen pruefen
UMFANG_FAELLIG = 40_000  # Bytes: Aufteilen faellig
INDEX_MAX = 10_000       # Bytes fuer index.md

RETIRED_FIELDS = {
    "timestamp": "generated.at",
    "valid_until": "stale_after",
}


def find_md_files(root):
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def check_frontmatter(path, lines):
    """Gibt eine Fehlermeldung (oder None) zurueck."""
    # Erste nicht-leere Zeile muss '---' sein.
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx >= len(lines) or lines[idx].strip() != "---":
        return (idx + 1, "Kein Frontmatter-Block (Datei beginnt nicht mit '---').")
    # Schliessendes '---' suchen.
    close = None
    for j in range(idx + 1, len(lines)):
        if lines[j].strip() == "---":
            close = j
            break
    if close is None:
        return (idx + 1, "Frontmatter-Block wird nicht mit '---' geschlossen.")
    # type:-Zeile innerhalb des Blocks suchen.
    for j in range(idx + 1, close):
        if re.match(r"^\s*type\s*:", lines[j]):
            value = lines[j].split(":", 1)[1].strip()
            if not value:
                return (j + 1, "type: ist leer.")
            return None
    return (idx + 1, "Pflichtfeld 'type:' fehlt im Frontmatter.")


def check_links(path, lines, errors):
    base_dir = os.path.dirname(path)
    for lineno, line in enumerate(lines, start=1):
        for target in LINK_RE.findall(line):
            target = target.strip()
            if not target:
                continue
            # Optionaler Titel in den Klammern: (url "Titel") -> nur den ersten Teil nehmen
            if " " in target and not target.startswith("<"):
                target = target.split(" ", 1)[0]
            target = target.strip("<>")
            # Externe Links / Anker / Mail ueberspringen
            if (
                EXTERNAL_SCHEME_RE.match(target)
                or target.startswith("#")
                or target.startswith("mailto:")
            ):
                continue
            # Anker am Pfad abtrennen
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            # Query abtrennen (selten in lokalen Links, aber sicher ist sicher)
            path_part = path_part.split("?", 1)[0]
            resolved = os.path.normpath(os.path.join(base_dir, path_part))
            if not os.path.exists(resolved):
                errors.append((path, lineno, f"Toter Link: '{target}' -> '{path_part}' existiert nicht."))


def _iso_date(value):
    """Gibt ein date zurueck oder None. Akzeptiert Datum und ISO-Datetime."""
    value = value.strip().strip("\"'")
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        pass
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def frontmatter_range(lines):
    """(start, end) der Frontmatter-Zeilenindizes oder None."""
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return None
    for j in range(i + 1, len(lines)):
        if lines[j].strip() == "---":
            return (i + 1, j)
    return None


def check_governance(path, lines, errors, warnings):
    """OKF-v0.2-Felder + Eigen-Extension criticality, nur im Frontmatter."""
    today = datetime.date.today()
    span = frontmatter_range(lines)
    if span is None:
        return
    start, end = span

    in_generated = False
    generated_at_seen = False
    in_verified = False

    for idx in range(start, end):
        line = lines[idx]
        lineno = idx + 1

        # Verschachtelte Bloecke verfolgen (2-Space-Einrueckung bzw. "- " Listen)
        if re.match(r"^\S", line):
            in_generated = line.startswith("generated:")
            in_verified = line.startswith("verified:")

        # Abgeloeste v0.1-Feldnamen
        m = re.match(r"^(\w+)\s*:", line)
        if m and m.group(1) in RETIRED_FIELDS:
            field = m.group(1)
            errors.append((path, lineno,
                f"'{field}:' ist in OKF v0.2 abgeloest — "
                f"bitte '{RETIRED_FIELDS[field]}' verwenden."))
            continue

        m = re.match(r"^\s*criticality\s*:\s*(.+?)\s*$", line)
        if m:
            value = m.group(1).strip().strip("\"'")
            if value not in VALID_CRITICALITY:
                errors.append((path, lineno,
                    f"Ungueltige criticality: '{value}' (erlaubt: controlled|hybrid|flexible)."))
            continue

        m = re.match(r"^status\s*:\s*(.+?)\s*$", line)
        if m:
            value = m.group(1).strip().strip("\"'")
            if value and value not in VALID_STATUS:
                errors.append((path, lineno,
                    f"Ungueltiger status: '{value}' (OKF v0.2 erlaubt: draft|stable|deprecated)."))
            continue

        m = re.match(r"^stale_after\s*:\s*(.*?)\s*$", line)
        if m:
            value = m.group(1)
            if value:
                d = _iso_date(value)
                if d is None:
                    errors.append((path, lineno,
                        f"stale_after ist kein gueltiges ISO-Datum: '{value}'."))
                elif d < today:
                    warnings.append((path, lineno,
                        f"stale_after ueberschritten ({value}) — Record pruefen "
                        f"(aktualisieren, neu verifizieren oder deprecaten)."))
            continue

        if in_generated:
            m = re.match(r"^\s+at\s*:\s*(.*?)\s*$", line)
            if m:
                generated_at_seen = True
                if m.group(1) and _iso_date(m.group(1)) is None:
                    errors.append((path, lineno,
                        f"generated.at ist kein gueltiges ISO-Datum: '{m.group(1)}'."))
                continue

        if in_verified:
            m = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if m:
                entry = m.group(1)
                if "by" not in entry or "at" not in entry:
                    errors.append((path, lineno,
                        "verified-Eintrag braucht 'by' und 'at' "
                        "(z.B. - { by: human:dein-kuerzel, at: 2026-07-26 })."))
                continue

    if not generated_at_seen:
        warnings.append((path, start,
            "Kein generated.at gesetzt — Aenderungsdatum fehlt (OKF v0.2 §4.1)."))


def check_sources(path, lines, errors, warnings):
    """sources-Liste pruefen und die Fussnoten-Referenzen im Body dagegenhalten."""
    span = frontmatter_range(lines)
    if span is None:
        return
    start, end = span

    entries = []          # (lineno, dict)
    current = None
    in_sources = False

    for idx in range(start, end):
        line = lines[idx]
        if re.match(r"^\S", line):
            if current:
                entries.append(current)
                current = None
            in_sources = line.startswith("sources:")
            continue
        if not in_sources:
            continue
        m = re.match(r"^\s*-\s*(\w+)\s*:\s*(.*?)\s*$", line)
        if m:
            if current:
                entries.append(current)
            current = {"_line": idx + 1, m.group(1): m.group(2)}
            continue
        m = re.match(r"^\s+(\w+)\s*:\s*(.*?)\s*$", line)
        if m and current is not None:
            current[m.group(1)] = m.group(2)
    if current:
        entries.append(current)

    if not entries:
        return

    base_dir = os.path.dirname(path)
    seen_ids = {}
    for entry in entries:
        lineno = entry["_line"]
        sid = entry.get("id", "").strip()
        if not sid:
            errors.append((path, lineno, "sources-Eintrag ohne 'id'."))
        elif sid in seen_ids:
            errors.append((path, lineno,
                f"sources-id '{sid}' doppelt vergeben (zuerst Zeile {seen_ids[sid]})."))
        else:
            seen_ids[sid] = lineno

        res = entry.get("resource", "").strip().strip("\"'")
        if not res:
            errors.append((path, lineno,
                f"sources-Eintrag '{sid or '?'}' ohne 'resource' — Quelle nicht identifizierbar."))
        elif not EXTERNAL_SCHEME_RE.match(res) and not res.startswith("mailto:"):
            target = os.path.normpath(os.path.join(base_dir, res.split("#")[0]))
            if not os.path.exists(target):
                errors.append((path, lineno,
                    f"sources-resource '{res}' loest nicht auf ('{target}' fehlt)."))

        if "last_modified" in entry and entry["last_modified"].strip():
            if _iso_date(entry["last_modified"]) is None:
                errors.append((path, lineno,
                    f"sources.last_modified ist kein gueltiges ISO-Datum: "
                    f"'{entry['last_modified']}'."))

    # Fussnoten-Referenzen im Body gegen die ids halten
    body = lines[end + 1:]
    defined = set(seen_ids)
    for off, line in enumerate(body):
        m = re.match(r"^\[\^([^\]]+)\]:", line)
        if m:
            defined.add(m.group(1))
    for off, line in enumerate(body):
        if re.match(r"^\[\^([^\]]+)\]:", line):
            continue
        for ref in re.findall(r"\[\^([^\]]+)\]", line):
            if ref not in defined:
                errors.append((path, end + 2 + off,
                    f"Fussnote '[^{ref}]' hat weder eine sources-id noch eine Definition."))


def _scalar_field(lines, start, end, field):
    """(lineno, wert) des ersten Top-Level-Feldes 'field' im Frontmatter."""
    for idx in range(start, end):
        m = re.match(rf"^{field}\s*:\s*(.*?)\s*$", lines[idx])
        if m:
            return (idx + 1, m.group(1).strip().strip("\"'"))
    return (None, None)


def _list_field(lines, start, end, field):
    """[(lineno, wert)] eines Listenfeldes. Inline ([a, b]) und Blockform ('- a')."""
    out = []
    i = start
    while i < end:
        m = re.match(rf"^{field}\s*:\s*(.*?)\s*$", lines[i])
        if not m:
            i += 1
            continue
        inline = m.group(1).strip()
        if inline.startswith("[") and inline.endswith("]"):
            for item in inline[1:-1].split(","):
                item = item.strip().strip("\"'")
                if item:
                    out.append((i + 1, item))
        elif inline:
            out.append((i + 1, inline.strip("\"'")))
        else:
            j = i + 1
            while j < end:
                mi = re.match(r"^\s+-\s*(.+?)\s*$", lines[j])
                if not mi:
                    break
                out.append((j + 1, mi.group(1).strip().strip("\"'")))
                j += 1
            i = j - 1
        i += 1
    return out


def read_generated_at(path, cache):
    """generated.at eines beliebigen Records als date (oder None). Memoisiert."""
    if path in cache:
        return cache[path]
    result = None
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        cache[path] = None
        return None
    span = frontmatter_range(lines)
    if span is not None:
        start, end = span
        in_generated = False
        for idx in range(start, end):
            line = lines[idx]
            if re.match(r"^\S", line):
                in_generated = line.startswith("generated:")
                continue
            if in_generated:
                m = re.match(r"^\s+at\s*:\s*(.*?)\s*$", line)
                if m:
                    result = _iso_date(m.group(1))
                    break
    cache[path] = result
    return result


def check_derived(path, lines, errors, warnings, gen_cache):
    """Eigen-Extension: abgeleitet_aus / stand / ersetzt_durch.

    Zweck: Eine *abgeleitete* Sicht (Inventar, Uebersicht, Index mit
    Betriebszustaenden) sagt selbst, aus welchen Quell-Records sie stammt und auf
    welchen Stand sie nachgezogen ist. Wird eine Quelle danach geaendert, faellt
    die Abweichung beim naechsten Validator-Lauf auf, statt still weiterzuleben.
    """
    span = frontmatter_range(lines)
    if span is None:
        return
    start, end = span
    base_dir = os.path.dirname(path)

    quellen = _list_field(lines, start, end, "abgeleitet_aus")
    stand_line, stand_raw = _scalar_field(lines, start, end, "stand")
    status_line, status_raw = _scalar_field(lines, start, end, "status")
    ersetzt_line, ersetzt_raw = _scalar_field(lines, start, end, "ersetzt_durch")

    stand = _iso_date(stand_raw) if stand_raw else None
    if stand_raw and stand is None:
        errors.append((path, stand_line,
            f"stand ist kein gueltiges ISO-Datum: '{stand_raw}'."))

    if quellen and not stand_raw:
        errors.append((path, quellen[0][0],
            "abgeleitet_aus ohne 'stand:' — ohne Stichdatum ist die Aktualitaet "
            "der abgeleiteten Aussagen nicht pruefbar."))
    if stand_raw and not quellen:
        warnings.append((path, stand_line,
            "stand: gesetzt, aber kein 'abgeleitet_aus:' — das Feld wirkt nur "
            "zusammen mit den Quell-Records."))

    for lineno, rel in quellen:
        target = os.path.normpath(os.path.join(base_dir, rel.split("#", 1)[0]))
        if not os.path.exists(target):
            errors.append((path, lineno,
                f"abgeleitet_aus '{rel}' loest nicht auf ('{target}' fehlt)."))
            continue
        if stand is None:
            continue
        quelle_at = read_generated_at(target, gen_cache)
        if quelle_at is not None and quelle_at > stand:
            warnings.append((path, lineno,
                f"Quelle '{rel}' ist neuer (generated.at {quelle_at.isoformat()}) "
                f"als der eigene stand ({stand.isoformat()}) — abgeleitete Aussagen "
                f"gegen die Quelle pruefen und 'stand' nachziehen."))

    if ersetzt_raw:
        # 'keiner' = bewusst ohne Nachfolger; die Begruendung steht im Body
        if ersetzt_raw.lower() != "keiner":
            target = os.path.normpath(os.path.join(base_dir, ersetzt_raw.split("#", 1)[0]))
            if not os.path.exists(target):
                errors.append((path, ersetzt_line,
                    f"ersetzt_durch '{ersetzt_raw}' loest nicht auf ('{target}' fehlt)."))
        if status_raw != "deprecated":
            warnings.append((path, ersetzt_line,
                "ersetzt_durch gesetzt, aber status ist nicht 'deprecated'."))
    elif status_raw == "deprecated":
        warnings.append((path, status_line or 1,
            "status: deprecated ohne 'ersetzt_durch:' — Nachfolger benennen oder "
            "'ersetzt_durch: keiner' setzen und im Body begruenden, warum es keinen gibt."))


def check_depends(path, lines, errors, warnings, gen_cache, blocker_zaehler):
    """Eigen-Extension: basiert_auf / blockiert_durch.

    `abgeleitet_aus` sagt "ich referiere den Zustand von X" -- eine Aussage ist
    nachzuziehen. `basiert_auf` sagt "meine Entscheidung faellt anders aus, wenn
    X kippt" -- dann ist die *Entscheidung* neu zu bewerten, nicht nur ein Satz.
    `blockiert_durch` benennt eine offene Vorbedingung.
    """
    span = frontmatter_range(lines)
    if span is None:
        return
    start, end = span
    base_dir = os.path.dirname(path)
    eigen_at = read_generated_at(path, gen_cache)

    # geprueft: je Quelle das Datum der letzten Nachpruefung
    geprueft = {}
    for lineno, item in _list_field(lines, start, end, "geprueft"):
        mq = re.search(r"quelle\s*:\s*([^,}]+)", item)
        ma = re.search(r"(?:^|[{,\s])at\s*:\s*([^,}]+)", item)
        if not (mq and ma):
            errors.append((path, lineno,
                "geprueft-Eintrag braucht 'quelle' und 'at' "
                "(z.B. - { quelle: ../bereich/voraussetzung.md, at: 2026-09-28 })."))
            continue
        d = _iso_date(ma.group(1).strip().strip("\"'"))
        if d is None:
            errors.append((path, lineno,
                f"geprueft.at ist kein gueltiges ISO-Datum: '{ma.group(1).strip()}'."))
            continue
        q = mq.group(1).strip().strip("\"'")
        ziel = os.path.normpath(os.path.join(base_dir, q.split("#", 1)[0]))
        geprueft[ziel] = (lineno, q, max(d, geprueft.get(ziel, (0, q, d))[2]))

    basis_ziele = set()
    for lineno, rel in _list_field(lines, start, end, "basiert_auf"):
        target = os.path.normpath(os.path.join(base_dir, rel.split("#", 1)[0]))
        basis_ziele.add(target)
        if not os.path.exists(target):
            errors.append((path, lineno,
                f"basiert_auf '{rel}' loest nicht auf ('{target}' fehlt)."))
            continue
        with open(target, "r", encoding="utf-8") as f:
            ziel = f.read().splitlines()
        zspan = frontmatter_range(ziel)
        zstatus = None
        if zspan:
            _, zstatus = _scalar_field(ziel, zspan[0], zspan[1], "status")
        if zstatus == "deprecated":
            warnings.append((path, lineno,
                f"Voraussetzung '{rel}' ist 'deprecated' — diese Entscheidung "
                f"steht damit auf einer abgeloesten Annahme und ist neu zu bewerten."))
            continue
        ziel_at = read_generated_at(target, gen_cache)
        vergleich = eigen_at
        if target in geprueft and (vergleich is None or geprueft[target][2] > vergleich):
            vergleich = geprueft[target][2]
        if vergleich and ziel_at and ziel_at > vergleich:
            warnings.append((path, lineno,
                f"Voraussetzung '{rel}' wurde am {ziel_at.isoformat()} geaendert, "
                f"nach diesem Record ({vergleich.isoformat()}) — pruefen, ob die "
                f"Entscheidung noch traegt."))

    for ziel, (lineno, q, _d) in geprueft.items():
        if ziel not in basis_ziele:
            warnings.append((path, lineno,
                f"geprueft nennt '{q}', das nicht in basiert_auf steht."))

    for lineno, rel in _list_field(lines, start, end, "blockiert_durch"):
        target = os.path.normpath(os.path.join(base_dir, rel.split("#", 1)[0]))
        if not os.path.exists(target):
            errors.append((path, lineno,
                f"blockiert_durch '{rel}' loest nicht auf ('{target}' fehlt)."))
            continue
        blocker_zaehler.setdefault(target, []).append(path)


def check_titel(alle_titel, warnings):
    """Gleicher title: in mehreren Records -- ein Agent erwischt zwangslaeufig
    mal den falschen."""
    for titel, orte in sorted(alle_titel.items()):
        if len(orte) > 1:
            liste = ", ".join(p for p, _ in orte)
            for p, lineno in orte:
                warnings.append((p, lineno,
                    f"Titel '{titel}' ist mehrfach vergeben ({liste}) — "
                    f"unterscheidbar machen."))


def read_status(path, cache):
    """status eines Records (fehlend = 'stable'). Memoisiert."""
    key = ("status", path)
    if key in cache:
        return cache[key]
    result = "stable"
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        span = frontmatter_range(lines)
        if span:
            _, v = _scalar_field(lines, span[0], span[1], "status")
            if v:
                result = v
    except OSError:
        pass
    cache[key] = result
    return result


def check_never_do(path, lines, errors):
    """Regel 11: never-do.md ist immer controlled -- explizit, nicht per Default."""
    if os.path.basename(path).lower() != "never-do.md":
        return
    span = frontmatter_range(lines)
    if span is None:
        return
    lineno, value = _scalar_field(lines, span[0], span[1], "criticality")
    if value != "controlled":
        errors.append((path, lineno or span[0],
            "never-do.md muss explizit 'criticality: controlled' tragen "
            "(Typ-Default 'hybrid' erlaubt Ergaenzen aus Web/Erinnerung -- "
            "bei Tabus falsch)."))


def check_deprecated_links(path, lines, warnings, cache):
    """Regel 12: aktiver Record verlinkt auf deprecated-Ziel ohne Kennzeichnung."""
    if read_status(path, cache) == "deprecated":
        return
    base_dir = os.path.dirname(path)
    span = frontmatter_range(lines)
    body_start = span[1] + 1 if span else 0
    for idx in range(body_start, len(lines)):
        line = lines[idx]
        if ABLOESUNG_MARKER_RE.search(line):
            continue
        for target in LINK_RE.findall(line):
            target = target.strip().split(" ", 1)[0].strip("<>")
            if (EXTERNAL_SCHEME_RE.match(target) or target.startswith("#")
                    or target.startswith("mailto:")):
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part.lower().endswith(".md"):
                continue
            resolved = os.path.normpath(os.path.join(base_dir, path_part))
            if os.path.exists(resolved) and read_status(resolved, cache) == "deprecated":
                warnings.append((path, idx + 1,
                    f"Link auf abgeloesten Record '{path_part}' (status: deprecated) "
                    f"ohne Kennzeichnung -- auf den Nachfolger umbiegen oder die "
                    f"Abloesung in der Zeile benennen."))


# Felder, deren Wert im Bestand regelmaessig Fliesstext mit Doppelpunkt traegt
YAML_SCALAR_FIELDS = ("title", "description", "author", "authors")


def check_yaml_parsebar(path, lines, errors):
    """Regel 13: Frontmatter muss fuer einen echten YAML-Parser lesbar sein."""
    span = frontmatter_range(lines)
    if span is None:
        return
    start, end = span
    for idx in range(start, end):
        m = re.match(r"^(\w+)\s*:\s+(.+?)\s*$", lines[idx])
        if not m or m.group(1) not in YAML_SCALAR_FIELDS:
            continue
        value = m.group(2)
        if value.startswith(("\"", "'", "|", ">")):
            continue
        if ": " in value or value.endswith(":"):
            errors.append((path, idx + 1,
                f"'{m.group(1)}:' enthaelt unquotierten Doppelpunkt -- YAML liest das "
                f"als Mapping. Wert in Anfuehrungszeichen setzen."))
    if _yaml is not None:
        try:
            data = _yaml.safe_load("\n".join(lines[start:end]))
            if not isinstance(data, dict):
                raise ValueError("Frontmatter ist kein Mapping")
        except Exception as exc:  # noqa: BLE001
            msg = str(exc).splitlines()[0][:120]
            mm = re.search(r"line (\d+)", str(exc))
            lineno = start + int(mm.group(1)) if mm else start
            errors.append((path, lineno,
                f"Frontmatter nicht YAML-parsebar (PyYAML): {msg}"))


def check_indexes(root, errors):
    for dirpath, _dirnames, filenames in os.walk(root):
        names = {n.lower() for n in filenames}
        if "index.md" not in names:
            errors.append((dirpath, 0, "Ordner ohne index.md."))


def check_lesbarkeit(path, lines, hinweise):
    """Sammelt Lesbarkeits-Hinweise: lange description, grosse Records/Indizes."""
    span = frontmatter_range(lines)
    if not span:
        return
    dl, dv = _scalar_field(lines, span[0], span[1], "description")
    if dv and len(dv) > DESC_MAX:
        hinweise["description"].append((len(dv), path, dl))
    groesse = os.path.getsize(path)
    ist_index = os.path.basename(path) == "index.md"
    if ist_index:
        if groesse > INDEX_MAX:
            hinweise["index"].append((groesse, path, None))
        return
    if groesse > UMFANG_PRUEFEN:
        _ul, uv = _scalar_field(lines, span[0], span[1], "umfang_ok")
        if uv:
            hinweise["ausnahme"].append((groesse, path, None))
        else:
            hinweise["umfang"].append((groesse, path, None))


def print_lesbarkeit(hinweise, alle):
    """Gibt den Block Lesbarkeit aus (Summen + Top 10, mit --lesbarkeit alles)."""
    desc, umf, idx = hinweise["description"], hinweise["umfang"], hinweise["index"]
    if not (desc or umf or idx):
        return
    faellig = sum(1 for g, _p, _l in umf if g > UMFANG_FAELLIG)
    print("\nLesbarkeit (Hinweise, kein Fehler -- Regeln: CONTRIBUTING.md):")
    print(f"  description > {DESC_MAX} Zeichen: {len(desc)}")
    print(f"  Records > {UMFANG_PRUEFEN // 1000} KB: {len(umf)}"
          f" (davon > {UMFANG_FAELLIG // 1000} KB, Aufteilen faellig: {faellig})"
          f"; ausgenommen per umfang_ok: {len(hinweise['ausnahme'])}")
    print(f"  index.md > {INDEX_MAX // 1000} KB: {len(idx)}")
    grenze = None if alle else 10
    for titel, liste, einheit in (
            ("Groesste Records", umf, "KB"),
            ("Groesste Indizes", idx, "KB"),
            ("Laengste descriptions", desc, "Zeichen")):
        if not liste:
            continue
        auswahl = sorted(liste, reverse=True)[:grenze]
        rest = len(liste) - len(auswahl)
        print(f"\n  {titel}:")
        for wert, path, _l in auswahl:
            anzeige = f"{wert / 1000:.0f} KB" if einheit == "KB" else f"{wert} Zeichen"
            marke = "  [faellig]" if einheit == "KB" and titel.startswith("Groesste R") and wert > UMFANG_FAELLIG else ""
            print(f"    {anzeige:>12}  {path}{marke}")
        if rest:
            print(f"    ... {rest} weitere (python validate_okf.py --lesbarkeit)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    alle_lesbarkeit = "--lesbarkeit" in sys.argv[1:]
    root = args[0] if args else "okf"
    if not os.path.isdir(root):
        print(f"FEHLER: Bundle-Root '{root}' nicht gefunden.", file=sys.stderr)
        return 2

    errors = []
    warnings = []
    gen_cache = {}
    blocker_zaehler = {}
    alle_titel = {}
    hinweise = {"description": [], "umfang": [], "index": [], "ausnahme": []}
    md_count = 0
    for path in sorted(find_md_files(root)):
        md_count += 1
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        fm = check_frontmatter(path, lines)
        if fm is not None:
            errors.append((path, fm[0], fm[1]))
        check_links(path, lines, errors)
        check_governance(path, lines, errors, warnings)
        check_sources(path, lines, errors, warnings)
        check_derived(path, lines, errors, warnings, gen_cache)
        check_depends(path, lines, errors, warnings, gen_cache, blocker_zaehler)
        check_never_do(path, lines, errors)
        check_deprecated_links(path, lines, warnings, gen_cache)
        check_yaml_parsebar(path, lines, errors)
        check_lesbarkeit(path, lines, hinweise)
        span = frontmatter_range(lines)
        if span:
            tl, tv = _scalar_field(lines, span[0], span[1], "title")
            if tv:
                alle_titel.setdefault(tv, []).append((path, tl))

    check_indexes(root, errors)
    check_titel(alle_titel, warnings)

    print(f"OKF-Validator: {md_count} .md-Dateien unter '{root}' geprueft.")

    if blocker_zaehler:
        print("\nVorbedingungen (blockiert_durch), meistgenannte zuerst:\n")
        for tgt, quellen in sorted(blocker_zaehler.items(),
                                   key=lambda kv: -len(kv[1])):
            print(f"  {len(quellen)}x  {tgt}")
            for q in sorted(quellen):
                print(f"        {q}")

    print_lesbarkeit(hinweise, alle_lesbarkeit)

    if warnings:
        print(f"\n{len(warnings)} Warnung(en) (brechen den Commit nicht):\n")
        for path, lineno, msg in sorted(warnings):
            loc = f"{path}:{lineno}" if lineno else path
            print(f"  {loc}\n      {msg}")

    if not errors:
        print("OK — keine Fehler.")
        return 0

    print(f"\n{len(errors)} Befund(e):\n")
    for path, lineno, msg in sorted(errors):
        loc = f"{path}:{lineno}" if lineno else path
        print(f"  {loc}\n      {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
