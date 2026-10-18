#!/usr/bin/env python3
"""Suche im OKF-Brain -- nur Standardbibliothek.

Findet die Records, die zu einer Frage passen, damit ein Agent gezielt eine oder
zwei Dateien (oder nur einen Abschnitt) liest statt Index-Ketten abzulaufen.

Verfahren: BM25F ueber gewichtete Felder (Titel x3, description x2, tags x2,
Pfad x1.5, Ueberschriften x1.5, Body x0.3), Laengennormierung je Feld -- ein
langer Body drueckt den Titel-Treffer nicht weg. Deutsche Komposita werden
naeherungsweise erfasst, in beide Richtungen und mit reduziertem Gewicht:
Suchwort steckt im Dokumentwort ("preis" -> "linkpreise") und Dokumentwort
steckt im Suchwort ("therapieansaetze" -> "therapien", "schreibstil" -> "stil").
Zusammengesetzte Suchwoerter werden zusaetzlich zerlegt, wenn beide Teile im
Bestand vorkommen ("kontextfenster" -> "kontext" + "fenster"). Warum-Fragen
heben decision- und pattern-Records leicht an.

Aufrufe (aus dem Repo-Root):
  python suche.py "warum relative Links"                Top 8 Treffer
  python suche.py "…" -n 15 --bereich arbeit/projekt
  python suche.py "…" --ohne-privat                     Arbeitskontext: privat/ ausblenden
  python suche.py "…" --typ decision                    nur ein Typ
  python suche.py "…" --json                            maschinenlesbar (z.B. fuer einen MCP)
  python suche.py --gliederung <pfad>                   Ueberschriften + Groesse je Abschnitt
  python suche.py --abschnitt <pfad> "<ueberschrift>"   nur diesen Abschnitt ausgeben
  python suche.py --test [datei]                        Trefferquote gegen suche_testfragen.tsv

Je Treffer: Pfad, type, criticality (Feld oder Typ-Default laut CLAUDE.md),
status, Groesse, gekuerzte description und der Abschnitt, der am besten passt.
"""

import glob
import json
import math
import os
import re
import sys

ROOT = "okf"
FELD_GEWICHT = {"title": 3.0, "description": 2.0, "tags": 2.0,
                "pfad": 1.5, "ueberschriften": 1.5, "body": 0.3}
FELD_B = {"title": 0.3, "description": 0.5, "tags": 0.3,
          "pfad": 0.3, "ueberschriften": 0.5, "body": 0.75}
K1 = 1.2
TEIL_GEWICHT = 0.5   # Suchwort steckt in einem laengeren Dokumentwort
TEIL_MIN = 5         # ab dieser Laenge des Suchworts
ZERLEG_GEWICHT = 0.4  # Dokumentwort steckt im (zusammengesetzten) Suchwort
ZERLEG_MIN = 4        # Mindestlaenge des Dokumentworts
INDEX_FAKTOR = 0.6   # index.md sind Wegweiser, keine Antworten

CRIT_DEFAULT = {"reference": "controlled", "metric": "controlled",
                "decision": "controlled", "note": "flexible",
                "source": "flexible", "pattern": "flexible"}

STOPP = set("""
der die das den dem des ein eine einer eines einem einen und oder aber nicht
ist sind war wird werden wurde hat haben hatte mit von vom zu zum zur im in am an
auf aus bei fuer fur ueber unter nach vor wie was wer wo wann warum welche welcher
welches ich du er sie es wir ihr man mein meine dein unser als auch noch schon nur
so dann denn doch ja nein kein keine sich mir mich dir dich uns euch dass ob wenn
the a an of to and or is are for on with by from as at be this that it how what
""".split())

UMLAUT = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
                        "Ä": "ae", "Ö": "oe", "Ü": "ue"})


def stamm(w):
    """Sehr leichte Stammform: haeufige deutsche/englische Endungen ab."""
    if len(w) <= 5:
        return w
    for suf in ("ungen", "heiten", "keiten", "ungen", "ern", "en", "er",
                "es", "e", "n", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def tokens(text):
    text = text.translate(UMLAUT).lower()
    out = []
    for w in re.findall(r"[a-z0-9]+", text):
        if w in STOPP or len(w) < 2:
            continue
        out.append(stamm(w))
    return out


def frontmatter(text):
    m = re.match(r"\s*---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).split("\n"):
        mm = re.match(r"^([a-z_]+)\s*:\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip("\"'")
    return fm, text[m.end():]


def abschnitte(body):
    """Liste (ueberschrift, ebene, text) -- Text vor der ersten Ueberschrift = ''."""
    teile, aktuell, ebene, puffer = [], "", 0, []
    in_code = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            teile.append((aktuell, ebene, "\n".join(puffer)))
            aktuell, ebene, puffer = m.group(2).strip(), len(m.group(1)), []
        else:
            puffer.append(line)
    teile.append((aktuell, ebene, "\n".join(puffer)))
    return teile


def lade(root=ROOT):
    docs = []
    for path in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm, body = frontmatter(text)
        secs = abschnitte(body)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        felder = {
            "title": tokens(fm.get("title", "")),
            "description": tokens(fm.get("description", "")),
            "tags": tokens(fm.get("tags", "")),
            "pfad": tokens(rel.replace("-", " ").replace("/", " ")[:-3]),
            "ueberschriften": tokens(" ".join(s[0] for s in secs)),
            "body": tokens(body),
        }
        tf = {}
        for feld, toks in felder.items():
            zaehl = {}
            for t in toks:
                zaehl[t] = zaehl.get(t, 0) + 1
            tf[feld] = zaehl
        laenge = {feld: len(toks) for feld, toks in felder.items()}
        typ = fm.get("type", "")
        crit = fm.get("criticality") or CRIT_DEFAULT.get(typ, "hybrid")
        if os.path.basename(path) == "never-do.md":
            crit = "controlled"
        docs.append({
            "pfad": path.replace(os.sep, "/"), "rel": rel, "tf": tf, "len": laenge,
            "type": typ, "criticality": crit, "status": fm.get("status", "stable"),
            "stale_after": fm.get("stale_after", ""), "title": fm.get("title", ""),
            "description": fm.get("description", ""), "bytes": len(text.encode("utf-8")),
            "abschnitte": secs,
        })
    return docs


def suche(docs, frage, n=8, bereich=None, ohne_privat=False, typ=None):
    q = list(dict.fromkeys(tokens(frage)))
    if not q:
        return []
    warum = bool(re.search(r"\b(warum|wieso|weshalb|why)\b", frage.lower()))
    kandidaten = [d for d in docs
                  if (not bereich or d["rel"].startswith(bereich.strip("/").removeprefix("okf/")))
                  and not (ohne_privat and d["rel"].startswith("privat/"))
                  and (not typ or d["type"] == typ)]
    if not kandidaten:
        return []
    N = len(kandidaten)
    avg = {f: (sum(d["len"][f] for d in kandidaten) / N) or 1.0 for f in FELD_GEWICHT}
    vokabular = set()
    for d in kandidaten:
        for zaehl in d["tf"].values():
            vokabular.update(zaehl)
    # Komposita im Suchwort zerlegen: "kontextfenster" -> "kontext" + "fenst"
    for t in list(q):
        if len(t) < 8:
            continue
        for i in range(4, len(t) - 3):
            links, rechts = t[:i], t[i:]
            if links not in vokabular and links.endswith("s") and links[:-1] in vokabular:
                links = links[:-1]   # Fugen-s
            rechts = rechts if rechts in vokabular else stamm(rechts)
            if links in vokabular and rechts in vokabular and len(rechts) >= 4:
                for teil in (links, rechts):
                    if teil not in q:
                        q.append(teil)
                break
    # Suchwort -> {dokumentwort: gewicht}
    erweiterung = {}
    for t in q:
        liste = {t: 1.0} if t in vokabular else {}
        for v in vokabular:
            if v == t:
                continue
            if len(t) >= TEIL_MIN and t in v:
                liste[v] = max(liste.get(v, 0), TEIL_GEWICHT)
            elif len(v) >= ZERLEG_MIN and len(t) > len(v) and v in t:
                liste[v] = max(liste.get(v, 0), ZERLEG_GEWICHT)
        erweiterung[t] = list(liste.items())
    df = {}
    for d in kandidaten:
        for t, liste in erweiterung.items():
            if any(v in zaehl for zaehl in d["tf"].values() for v, _g in liste):
                df[t] = df.get(t, 0) + 1
    ergebnisse = []
    for d in kandidaten:
        score, treffer = 0.0, []
        for t, liste in erweiterung.items():
            f = 0.0
            for feld, zaehl in d["tf"].items():
                roh = sum(zaehl.get(v, 0) * g for v, g in liste)
                if roh:
                    b = FELD_B[feld]
                    f += FELD_GEWICHT[feld] * roh / (1 - b + b * d["len"][feld] / avg[feld])
            if not f:
                continue
            idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
            score += idf * f * (K1 + 1) / (f + K1)
            treffer.append(t)
        if not score:
            continue
        # Abdeckung belohnen: wer mehr verschiedene Suchwoerter trifft, steht vorn
        score *= (len(treffer) / len(q)) ** 0.5
        if d["rel"].endswith("index.md"):
            score *= INDEX_FAKTOR
        if warum and d["type"] in ("decision", "pattern"):
            score *= 1.3   # Warum-Fragen beantworten Decisions (CLAUDE.md)
        if d["status"] == "deprecated":
            score *= 0.5
        ergebnisse.append((score, d, treffer))
    ergebnisse.sort(key=lambda x: -x[0])
    return [(s, d, bester_abschnitt(d, erweiterung)) for s, d, _t in ergebnisse[:n]]


def bester_abschnitt(d, erweiterung):
    best, best_score = None, 0.0
    for titel, _ebene, text in d["abschnitte"]:
        if not titel:
            continue
        toks = tokens(titel) * 3 + tokens(text)
        menge = {}
        for t in toks:
            menge[t] = menge.get(t, 0) + 1
        s = 0.0
        for liste in erweiterung.values():
            hit = sum(menge.get(v, 0) * g for v, g in liste)
            s += math.log(1 + hit)
        if s > best_score:
            best, best_score = titel, s
    return best


def veraltet(d):
    import datetime
    try:
        return bool(d["stale_after"]) and \
            datetime.date.fromisoformat(d["stale_after"][:10]) < datetime.date.today()
    except ValueError:
        return False


def ausgabe(ergebnisse, als_json=False):
    if als_json:
        print(json.dumps([{
            "pfad": d["pfad"], "score": round(s, 2), "type": d["type"],
            "criticality": d["criticality"], "status": d["status"],
            "veraltet": veraltet(d), "kb": round(d["bytes"] / 1000, 1),
            "title": d["title"], "description": d["description"],
            "abschnitt": ab} for s, d, ab in ergebnisse], ensure_ascii=False, indent=1))
        return
    if not ergebnisse:
        print("Keine Treffer.")
        return
    for i, (s, d, ab) in enumerate(ergebnisse, 1):
        marken = [d["type"] or "?", d["criticality"]]
        if d["status"] != "stable":
            marken.append(d["status"].upper())
        if veraltet(d):
            marken.append("STALE")
        desc = d["description"]
        desc = desc if len(desc) <= 160 else desc[:157] + "…"
        print(f"{i:>2}. {d['pfad']}  [{' · '.join(marken)} · {d['bytes'] / 1000:.0f} KB]  ({s:.1f})")
        if desc:
            print(f"    {desc}")
        if ab and d["bytes"] > 8000:
            print(f"    → Abschnitt: \"{ab}\"")


def gliederung(pfad):
    with open(pfad, encoding="utf-8") as f:
        _fm, body = frontmatter(f.read())
    for titel, ebene, text in abschnitte(body):
        if titel:
            print(f"{'  ' * (ebene - 1)}{titel}  ({len(text.encode('utf-8')) / 1000:.1f} KB)")


def abschnitt(pfad, ueberschrift):
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    fm, body = frontmatter(text)
    secs = abschnitte(body)
    ziel = ueberschrift.lower()
    for i, (titel, ebene, inhalt) in enumerate(secs):
        if titel and ziel in titel.lower():
            print(f"{pfad} — type: {fm.get('type', '?')}, criticality: "
                  f"{fm.get('criticality') or CRIT_DEFAULT.get(fm.get('type', ''), 'hybrid')}, "
                  f"status: {fm.get('status', 'stable')}, generated.at: siehe Datei\n")
            print(f"{'#' * ebene} {titel}{inhalt}")
            for titel2, ebene2, inhalt2 in secs[i + 1:]:
                if ebene2 <= ebene:
                    break
                print(f"{'#' * ebene2} {titel2}{inhalt2}")
            return 0
    print(f"Keine Überschrift mit '{ueberschrift}' in {pfad}. Gliederung:", file=sys.stderr)
    gliederung(pfad)
    return 1


def test(datei="suche_testfragen.tsv"):
    docs = lade()
    fragen = []
    with open(datei, encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            teile = line.rstrip("\n").split("\t")
            fragen.append((teile[0], teile[1], teile[2] if len(teile) > 2 else ""))
    at = {1: 0, 3: 0, 5: 0}
    fehl = []
    for frage, erwartet, bereich in fragen:
        erg = suche(docs, frage, n=5, bereich=bereich or None)
        pfade = [d["rel"] for _s, d, _a in erg]
        rang = pfade.index(erwartet) + 1 if erwartet in pfade else None
        for k in at:
            if rang and rang <= k:
                at[k] += 1
        if rang != 1:
            fehl.append((frage, erwartet, rang, pfade[:3]))
    n = len(fragen)
    print(f"{n} Testfragen — Treffer@1: {at[1]}/{n}  @3: {at[3]}/{n}  @5: {at[5]}/{n}")
    for frage, erwartet, rang, top in fehl:
        print(f"\n  „{frage}“ — erwartet {erwartet}, Rang {rang or '>5'}")
        for p in top:
            print(f"      {p}")
    return 0 if at[3] >= 0.8 * n else 1


def main(argv):
    # Windows-Konsolen (cp1252) kennen z.B. den Pfeil nicht -- ersetzen statt abbrechen
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--test":
        return test(*argv[1:2])
    if argv[0] == "--gliederung" and len(argv) >= 2:
        gliederung(argv[1])
        return 0
    if argv[0] == "--abschnitt" and len(argv) >= 3:
        return abschnitt(argv[1], argv[2])
    n, bereich, typ, ohne_privat, als_json, frage = 8, None, None, False, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "-n":
            n = int(argv[i + 1]); i += 1
        elif a == "--bereich":
            bereich = argv[i + 1]; i += 1
        elif a == "--typ":
            typ = argv[i + 1]; i += 1
        elif a == "--ohne-privat":
            ohne_privat = True
        elif a == "--json":
            als_json = True
        else:
            frage.append(a)
        i += 1
    ausgabe(suche(lade(), " ".join(frage), n, bereich, ohne_privat, typ), als_json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
