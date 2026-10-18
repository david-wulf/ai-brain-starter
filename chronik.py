#!/usr/bin/env python3
"""Chronik aus dem Brain ernten — nur Standardbibliothek.

Beantwortet Fragen der Sorte „was habe ich wann wieder gekippt?", „was galt
vorher?" und „was hat sich seit dem 1. August geaendert?" — ohne dass dafuer
ein Wissensgraph noetig waere.

Die Historie steht bereits in den Records, nur als Konvention statt als Feld.
Dieses Skript erntet genau diese Konventionen:

  1. Durchgestrichene Listeneintraege mit Datum
     - ~~Punkt~~ — erledigt am 2026-08-07: ...
  2. Korrektur- und Aenderungsnotizen im Body
     > **Korrektur 2026-07-26:** ...   |   **Geaendert 2026-08-13:** ...
     **Ueberholt (2026-08-06)**  |  **Erledigt am 2026-08-05**  |  Nachtrag ...
  3. Abloesungen im Frontmatter
     status: deprecated + ersetzt_durch: <pfad>

Ausgegeben wird eine nach Datum sortierte Liste: was, wann, in welchem Record.
Das Datum stammt aus der Notiz selbst, nicht aus generated.at — deshalb bleibt
die Chronik richtig, auch wenn ein Record spaeter nochmal angefasst wird.

Aufruf:
  python chronik.py                                  # ganzes Bundle
  python chronik.py okf/privat/bereich               # nur ein Bereich
  python chronik.py okf --seit 2026-08-01            # ab Datum
  python chronik.py okf --seit 2026-08-01 --bis 2026-08-07
  python chronik.py okf/arbeit/projekt --art gekippt

Arten:
  erledigt   durchgestrichene Punkte und Erledigt-Notizen
  gekippt    Korrekturen, Aenderungen, ueberholte Aussagen — das eigentlich
             Interessante: wo eine fruehere Festlegung nicht mehr gilt
  abgeloest  Records mit status: deprecated
"""

import datetime
import os
import re
import sys

DATUM = r"(\d{4}-\d{2}-\d{2})"

# 1) Durchgestrichener Listeneintrag, Datum irgendwo dahinter
STRICH_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+~~(.+?)~~\s*(.*)$")

# 2) Aenderungs-/Korrekturnotizen im Body
GEKIPPT_RE = re.compile(
    r"(?:^|[>\s*_])(Korrektur|Ge(?:ä|ae)ndert|(?:Ü|Ue)berholt|Nicht mehr ma(?:ß|ss)geblich|"
    r"Widerrufen|Zur(?:ü|ue)ckgenommen|Verworfen|Aufgegeben|Revidiert)\b[^\n]{0,40}?" + DATUM,
    re.I)
ERLEDIGT_RE = re.compile(
    r"(?:^|[>\s*_])(Erledigt|Umgesetzt|Gegengepr(?:ü|ue)ft|Nachtrag|Behoben)\b[^\n]{0,40}?" + DATUM,
    re.I)

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return ("", "", "", text)
    fm = m.group(1)
    t = re.search(r"^title:\s*(.+)$", fm, re.M)
    st = re.search(r"^status:\s*(\S+)", fm, re.M)
    ers = re.search(r"^ersetzt_durch:\s*(\S+)", fm, re.M)
    return (t.group(1).strip() if t else "",
            st.group(1).strip() if st else "stable",
            ers.group(1).strip() if ers else "",
            text[m.end():])


def klartext(s, breite=120):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("~~", "").replace("`", "").replace(">", "").strip()
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= breite else s[: breite - 1] + "…"


def ernte(path, mit_index=False):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    if not mit_index and re.search(r"^type:\s*index\s*$", text, re.M):
        return []
    titel, status, ersetzt, body = frontmatter(text)
    titel = titel or os.path.basename(path)
    out = []

    if status == "deprecated":
        # Datum der Abloesung: erste Jahreszahl-Datumsangabe im Body, sonst leer
        m = re.search(DATUM, body)
        out.append((m.group(1) if m else "", "abgeloest",
                    f"Record abgeloest" + (f" → {ersetzt}" if ersetzt else ""), titel, path))

    for zeile in body.splitlines():
        m = STRICH_RE.match(zeile)
        if m:
            rest = m.group(2)
            d = re.search(DATUM, rest)
            out.append((d.group(1) if d else "", "erledigt",
                        klartext(m.group(1)), titel, path))
            continue
        for regex, art in ((GEKIPPT_RE, "gekippt"), (ERLEDIGT_RE, "erledigt")):
            t = regex.search(zeile)
            if t:
                out.append((t.group(2), art, klartext(zeile), titel, path))
                break
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else "okf"
    def opt(name):
        for i, a in enumerate(sys.argv):
            if a == "--" + name and i + 1 < len(sys.argv):
                return sys.argv[i + 1]
        return None
    seit, bis, art = opt("seit"), opt("bis"), opt("art")
    mit_index = "--index" in sys.argv

    if not os.path.isdir(root):
        print(f"FEHLER: '{root}' ist kein Ordner.", file=sys.stderr)
        return 2

    eintraege = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if name.lower().endswith(".md"):
                eintraege += ernte(os.path.join(dirpath, name), mit_index)

    if art:
        eintraege = [e for e in eintraege if e[1] == art]
    if seit:
        eintraege = [e for e in eintraege if e[0] and e[0] >= seit]
    if bis:
        eintraege = [e for e in eintraege if e[0] and e[0] <= bis]

    ohne_datum = [e for e in eintraege if not e[0]]
    mit_datum = sorted([e for e in eintraege if e[0]], key=lambda e: e[0], reverse=True)

    spanne = ""
    if seit or bis:
        spanne = f", {seit or 'Anfang'} bis {bis or 'heute'}"
    print(f"Chronik unter '{root}'{spanne}"
          + (f", nur '{art}'" if art else "")
          + f": {len(mit_datum)} datierte Eintraege\n")

    MARKE = {"gekippt": "↺", "erledigt": "✓", "abgeloest": "⇥"}
    letztes = None
    for datum, a, txt, titel, pfad in mit_datum:
        if datum != letztes:
            print(f"\n{datum}")
            letztes = datum
        print(f"  {MARKE.get(a, '·')} [{a}] {txt}")
        print(f"      {titel}  ({pfad})")

    if ohne_datum and not (seit or bis):
        print(f"\n{len(ohne_datum)} Eintraege ohne Datum (nicht einsortierbar):")
        for _, a, txt, titel, pfad in ohne_datum[:10]:
            print(f"  · [{a}] {txt}  — {pfad}")

    if mit_datum:
        print("\nLegende: ↺ gekippt/korrigiert · ✓ erledigt · ⇥ Record abgeloest.")
        print("Das Datum stammt aus der Notiz, nicht aus generated.at.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
