#!/usr/bin/env python3
"""Offene Punkte aus dem Brain einsammeln — nur Standardbibliothek.

Beantwortet die Frage „woran arbeite ich hier weiter?", ohne dass die Punkte
dafuer aus den Records herausgeloest werden muessen. Sie bleiben, wo sie
hingehoeren — beim jeweiligen Konzept, mit ihrem Kontext.

Gesucht wird nach Abschnitten, deren Ueberschrift auf offene Arbeit hindeutet
(„Offene Punkte", „Was noch blockiert", „Naechste Schritte", „Offen", „Risiko /
Challenge", „Beobachtung", „Todo"). Daraus werden die Listeneintraege gezogen.
Gematcht wird auf **Wortgrenzen**: „Risikolebensversicherungen" ist eine
Vertragsart und kein offener Punkt, „Risiko / Challenge" dagegen schon.

**Erledigtes wird uebersprungen.** Im Brain gilt die Konvention, erledigte
Punkte durchzustreichen und stehen zu lassen (`- ~~Punkt~~ — erledigt am ...`)
statt sie zu loeschen. Ein Eintrag, der mit `~~` beginnt, zaehlt deshalb als
erledigt. Mit --alle werden sie mit ausgegeben.

Sortiert wird nach `generated.at` des Records, neueste zuerst — der Record, an
dem zuletzt gearbeitet wurde, steht oben.

Das Ergebnis ist eine Leseliste, keine Aufgabenliste: Todos gehoeren laut
CLAUDE.md ins Aufgabenwerkzeug. Was hier auftaucht und wirklich eine Aufgabe
ist, gehoert dorthin uebertragen und im Record durchgestrichen.

Aufruf:
  python offene_punkte.py                          # ganzes Bundle
  python offene_punkte.py okf/privat/bereich       # nur ein Bereich
  python offene_punkte.py okf/arbeit/projekt --alle
  python offene_punkte.py okf/privat/bereich --kurz # nur Zaehlung je Record
  python offene_punkte.py okf/privat/bereich --index # index.md mit auswerten

`index.md`-Records bleiben per Default aussen vor: Indizes sind Navigation, kein
Wissen (CONTRIBUTING.md), und ihre Aufzaehlungen sind Konzeptlisten, keine
offenen Punkte. Die maessgebliche Fassung steht immer im Detail-Record.
"""

import datetime
import os
import re
import sys

# Ueberschriften, die offene Arbeit fuehren.
# WORTGRENZEN sind noetig, nicht Teiltreffer: "Risikolebensversicherungen" enthaelt
# "risiko", ist aber eine Vertragsart und kein offener Punkt. Dasselbe gilt fuer
# "Restrisiko" (bewusst getragen) und "Offenlegung". Gesucht wird deshalb das
# Wort selbst, mit den ueblichen deutschen Endungen.
OFFEN_MUSTER = (
    r"\boffen(e|es|er|en|e\s+punkte)?\b",
    r"\bblockier\w*",
    r"\bn(ae|ä)chste[nr]?\s+schritt\w*",
    r"\btodo\b", r"\bto-do\b",
    r"\brisiko\b", r"\brisiken\b",
    r"\bchallenge\b",
    r"\bbeobachtung\w*",
    r"\bungekl(ae|ä)rt\w*",
    r"\bwas\s+fehlt\b",
    r"\bl(ue|ü)cke\w*",
)
OFFEN_RE = re.compile("|".join(OFFEN_MUSTER), re.I)

# Ueberschriften, die trotz Treffer NICHT gemeint sind
AUSNAHMEN = (
    "offene fragen beantwortet",
    "restrisiko",          # bewusst getragene, dokumentierte Risiken sind keine offenen Punkte
    "risiko getragen",
    "was geklaert ist", "was geklärt ist",
)

HEAD_RE = re.compile(r"^(#{1,4})\s+(.*?)\s*$")
ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+(.*?)\s*$")
FM_AT_RE = re.compile(r"^\s+at\s*:\s*(\S+)", re.M)


def frontmatter(text):
    """(titel, generated.at als str oder '') aus dem Frontmatter."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return ("", "")
    fm = m.group(1)
    t = re.search(r"^title:\s*(.+)$", fm, re.M)
    at = ""
    g = re.search(r"^generated:\s*\n((?:\s+\w+:.*\n)*)", fm, re.M)
    if g:
        a = FM_AT_RE.search(g.group(1))
        if a:
            at = a.group(1).strip().strip("\"'")
    return (t.group(1).strip() if t else "", at)


def ist_offen_ueberschrift(titel):
    low = titel.lower()
    if any(a in low for a in AUSNAHMEN):
        return False
    return bool(OFFEN_RE.search(low))


def erledigt(eintrag):
    """Konvention im Brain: durchgestrichener Eintrag = erledigt, bleibt stehen."""
    return eintrag.lstrip("*_ ").startswith("~~")


# Woerter, die auf Erledigung hindeuten, ohne dass durchgestrichen wurde
FERTIG_WORT_RE = re.compile(r"\b(erledigt|umgesetzt|geloest|gelöst|behoben|eingerichtet)\b", re.I)


def verdacht_erledigt(eintrag):
    """Nicht durchgestrichen, klingt aber nach erledigt -> Konvention pruefen."""
    return not erledigt(eintrag) and bool(FERTIG_WORT_RE.search(eintrag))


def sammle(path, alle=False):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    titel, at = frontmatter(text)
    lines = text.splitlines()
    treffer = []
    in_abschnitt = None
    ebene = 0
    for line in lines:
        h = HEAD_RE.match(line)
        if h:
            neu_ebene, neu_titel = len(h.group(1)), h.group(2)
            if in_abschnitt is not None and neu_ebene <= ebene:
                in_abschnitt = None
            if ist_offen_ueberschrift(neu_titel):
                in_abschnitt, ebene = neu_titel, neu_ebene
            continue
        if in_abschnitt is None:
            continue
        it = ITEM_RE.match(line)
        if not it:
            continue
        eintrag = it.group(1).strip()
        if not eintrag:
            continue
        if erledigt(eintrag) and not alle:
            continue
        treffer.append((in_abschnitt, eintrag, erledigt(eintrag)))
    abgeleitet = bool(re.search(r"^abgeleitet_aus\s*:\s*\S", text, re.M))
    ist_index = bool(re.search(r"^type:\s*index\s*$", text, re.M))
    return {"pfad": path, "titel": titel or os.path.basename(path),
            "at": at, "punkte": treffer, "abgeleitet": abgeleitet,
            "index": ist_index}


def klartext(s, breite=150):
    """Markdown-Auszeichnung fuer die Konsole entschaerfen."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)   # Links -> Linktext
    s = s.replace("**", "").replace("~~", "").replace("`", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= breite else s[: breite - 1] + "…"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    root = args[0] if args else "okf"
    alle = "--alle" in flags
    kurz = "--kurz" in flags
    mit_index = "--index" in flags

    if not os.path.isdir(root):
        print(f"FEHLER: '{root}' ist kein Ordner.", file=sys.stderr)
        return 2

    records, uebersprungen = [], []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.lower().endswith(".md"):
                continue
            r = sammle(os.path.join(dirpath, name), alle)
            if not r["punkte"]:
                continue
            if r["index"] and not mit_index:
                uebersprungen.append(r)
                continue
            records.append(r)

    records.sort(key=lambda r: (r["at"] or "0000-00-00"), reverse=True)
    gesamt = sum(len(r["punkte"]) for r in records)

    heute = datetime.date.today().isoformat()
    print(f"Offene Punkte unter '{root}' (Stand {heute}): "
          f"{gesamt} in {len(records)} Records"
          + (" — inkl. erledigter" if alle else "")
          + (f"; {len(uebersprungen)} index.md uebersprungen (--index zeigt sie)"
             if uebersprungen else "") + "\n")

    for r in records:
        marke_sicht = "  [abgeleitete Sicht]" if r["abgeleitet"] else ""
        print(f"{r['at'] or '????-??-??'}  {r['titel']}{marke_sicht}")
        print(f"  {r['pfad']}  ({len(r['punkte'])})")
        if kurz:
            print()
            continue
        letzter = None
        for abschnitt, eintrag, done in r["punkte"]:
            if abschnitt != letzter:
                print(f"    [{abschnitt}]")
                letzter = abschnitt
            marke = "x" if done else ("?" if verdacht_erledigt(eintrag) else "-")
            print(f"      {marke} {klartext(eintrag)}")
        print()

    if not records:
        print("Keine offenen Punkte gefunden.")
    else:
        print("Legende: '-' offen · '?' klingt nach erledigt, ist aber nicht "
              "durchgestrichen — Konvention pruefen · 'x' erledigt (nur mit --alle).")
        print("[abgeleitete Sicht] = Record mit 'abgeleitet_aus', wiederholt Punkte "
              "aus seinen Quellen.")
        print("Was hiervon eine echte Aufgabe ist, gehoert ins Aufgabenwerkzeug — "
              "im Record dann durchstreichen, nicht loeschen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
