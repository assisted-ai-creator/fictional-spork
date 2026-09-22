#!/usr/bin/env python3
"""Mahabharata source toolkit for the novel project.

Reads two sources and answers the questions a writer needs while working:

  * The BORI Critical Edition (CE), GRETIL electronic text, in IAST.
    Lines are tagged as the constituted text ("main"), star passages ("star",
    marked * in the edition) or Appendix I passages ("app", marked @).
    Star and appendix passages are what the CE editors REJECTED as later
    additions; only "main" lines count as the CE text.
  * The Ganguli translation (1883-1896), made from the vulgate (Nilakantha)
    text, which still contains many passages the CE rejected.

Commands (run `mbh.py <command> -h` for options):

  show 1.57            CE adhyaya 1.57 (constituted text only)
  show 1.57.1-20 --all CE verses 1-20 with star/appendix passages too
  search urvasi -b 3   diacritic-insensitive search in the CE
  gshow 1.63           Ganguli section 1.63
  gsearch Urvasi -b 3  search the Ganguli translation (regex, case-insensitive)
  gtoc 1               Ganguli section list with sub-parva names
  check PATTERN...     where does a word/phrase occur: CE main / star / app / Ganguli
  where 1.57           Ganguli sections aligned with CE 1.57 (needs concordance)
  speakers 1.57        speaker changes ("X uvaca") in a CE adhyaya
  stats                adhyaya and verse counts per book
  build-cache          parse sources into sources/cache/ (run after fetching)
  concordance          rebuild index/concordance.csv (CE adhyaya -> Ganguli)

References are BOOK.ADHYAYA[.VERSE[-VERSE]] for the CE and BOOK.SECTION for
Ganguli. Search patterns are matched after "skeleton" normalisation on both
sides (diacritics removed, aspirates and sibilants collapsed), so `krishna`,
`krsna` and `kṛṣṇa` all find the same lines.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CE_DIR = ROOT / "sources" / "ce" / "gretil"
GANGULI_DIR = ROOT / "sources" / "ganguli"
CACHE_DIR = ROOT / "sources" / "cache"
CE_CACHE = CACHE_DIR / "ce_lines.tsv"
GANGULI_CACHE = CACHE_DIR / "ganguli_sections.json"
CONCORDANCE = ROOT / "index" / "concordance.csv"

BOOK_NAMES = {
    1: "Adi", 2: "Sabha", 3: "Aranyaka (Vana)", 4: "Virata", 5: "Udyoga",
    6: "Bhishma", 7: "Drona", 8: "Karna", 9: "Shalya", 10: "Sauptika",
    11: "Stri", 12: "Shanti", 13: "Anushasana", 14: "Ashvamedhika",
    15: "Ashramavasika", 16: "Mausala", 17: "Mahaprasthanika", 18: "Svargarohana",
}

# --------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------

def fold(s: str) -> str:
    """Lower-case and strip diacritics; vocalic r/l become ri/li."""
    s = s.lower()
    for a, b in (("ṛ", "ri"), ("ṝ", "ri"), ("ḷ", "li"), ("ḹ", "li")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


_ASPIRATE = re.compile(r"([kgcjtdpbs])h")
_NASAL = re.compile(r"m(?=[bcdfgjklnpqrstvwxz])")


def skel(s: str) -> str:
    """Lossy skeleton used for matching IAST against Ganguli's spellings.

    kṛṣṇa, Krishna -> krisna ; yudhiṣṭhira, Yudhishthira -> yudistira ;
    saṃjaya, Sanjaya -> sanjaya ; vaiśaṃpāyana, Vaisampayana -> vaisanpayana
    """
    s = fold(s).replace("w", "v")
    s = _ASPIRATE.sub(r"\1", s)
    s = _NASAL.sub("n", s)
    return s


# --------------------------------------------------------------------------
# Critical Edition
# --------------------------------------------------------------------------

# ID = book,adhyaya.verse + optional pada/prose letter + optional star (*) or
# appendix (@) passage number; then a tab (a space in a few places; book 10
# uses a literal "<>") and the text.
_CE_ID = re.compile(r"^(\d{2}),(\d{3})\.(\d{3})([a-zA-Z]?(?:[*@]\d+[A-Za-z]?[_=]\d+(?:\([^)\s]*\)?)?)?)")
_CE_LINE = re.compile(_CE_ID.pattern + r"[\t ]+(.*)$")


class CELine:
    __slots__ = ("book", "adhyaya", "verse", "suffix", "kind", "text")

    def __init__(self, book, adhyaya, verse, suffix, kind, text):
        self.book, self.adhyaya, self.verse = book, adhyaya, verse
        self.suffix, self.kind, self.text = suffix, kind, text

    @property
    def ref(self) -> str:
        return f"{self.book}.{self.adhyaya}.{self.verse}"

    @property
    def raw_id(self) -> str:
        return f"{self.book:02d},{self.adhyaya:03d}.{self.verse:03d}{self.suffix}"


def _classify(suffix: str) -> str:
    if "@" in suffix:
        return "app"
    if "*" in suffix:
        return "star"
    return "main"


def parse_ce_file(path: Path):
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = html.unescape(re.sub(r"<[^>]+>", "", raw.replace("<>", "\t"))).rstrip()
        m = _CE_LINE.match(line)
        if not m:
            if _CE_ID.match(line) and line.strip() != _CE_ID.match(line).group(0):
                print(f"warning: unparsed CE line in {path.name}: {line[:80]}", file=sys.stderr)
            continue
        book, adh, verse, suffix, text = m.groups()
        yield CELine(int(book), int(adh), int(verse), suffix, _classify(suffix), text.strip())


def build_ce_cache() -> int:
    files = sorted(CE_DIR.glob("mbh_[0-9][0-9]_u.htm"))
    if not files:
        sys.exit(f"No CE files in {CE_DIR}. Run tools/fetch_sources.sh first.")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    with CE_CACHE.open("w", encoding="utf-8") as out:
        for f in files:
            for ln in parse_ce_file(f):
                out.write(f"{ln.book}\t{ln.adhyaya}\t{ln.verse}\t{ln.suffix}\t{ln.kind}\t{ln.text}\n")
                n += 1
    return n


_ce_cache: list[CELine] | None = None


def ce_lines() -> list[CELine]:
    global _ce_cache
    if _ce_cache is None:
        if not CE_CACHE.exists():
            build_ce_cache()
        rows = []
        with CE_CACHE.open(encoding="utf-8") as f:
            for row in f:
                b, a, v, suf, kind, text = row.rstrip("\n").split("\t", 5)
                rows.append(CELine(int(b), int(a), int(v), suf, kind, text))
        _ce_cache = rows
    return _ce_cache


def ce_adhyaya_index() -> dict[tuple[int, int], list[CELine]]:
    idx: dict[tuple[int, int], list[CELine]] = defaultdict(list)
    for ln in ce_lines():
        if ln.adhyaya > 0:
            idx[(ln.book, ln.adhyaya)].append(ln)
    return idx


def parse_ref(ref: str):
    """'1.57' -> (1, 57, None, None); '1.57.3-9' -> (1, 57, 3, 9); '1.57.3' -> (1,57,3,3)."""
    m = re.fullmatch(r"(\d+)\.(\d+)(?:\.(\d+)(?:-(\d+))?)?", ref.strip())
    if not m:
        raise ValueError(f"bad reference: {ref!r} (use BOOK.ADHYAYA[.VERSE[-VERSE]])")
    b, a, v1, v2 = m.groups()
    v1 = int(v1) if v1 else None
    v2 = int(v2) if v2 else v1
    return int(b), int(a), v1, v2


def format_verses(lines: list[CELine], show_all: bool, ids: bool) -> str:
    """Group pada-lines into verses; speaker lines shown in brackets."""
    out = []
    cur_key, cur_parts = None, []

    def flush():
        if cur_key is not None and cur_parts:
            label, kind = cur_key
            mark = {"main": " ", "star": "*", "app": "@"}[kind]
            out.append(f"{mark}{label:>10}  " + " / ".join(cur_parts))

    for ln in lines:
        if ln.kind != "main" and not show_all:
            continue
        if ln.kind == "main" and ln.suffix == "" :
            flush()
            cur_key, cur_parts = None, []
            out.append(f"{'':>11}  [{ln.text}]")
            continue
        if ln.kind == "main":
            key = (f"{ln.adhyaya}.{ln.verse}", "main")
        else:
            # e.g. suffix "d*0018_01" -> label "1.3d*18" (star passage 18 after pada d)
            m = re.match(r"([a-zA-Z]?)([*@])(\d+)", ln.suffix)
            label = f"{ln.adhyaya}.{ln.verse}{m.group(1)}{m.group(2)}{int(m.group(3))}" if m else ln.raw_id
            key = (label, ln.kind)
        if ids:
            flush()
            cur_key, cur_parts = None, []
            mark = {"main": " ", "star": "*", "app": "@"}[ln.kind]
            out.append(f"{mark}{ln.raw_id:<24} {ln.text}")
            continue
        if key != cur_key:
            flush()
            cur_key, cur_parts = key, []
        cur_parts.append(ln.text)
    flush()
    return "\n".join(out)


def cmd_show(args):
    idx = ce_adhyaya_index()
    for ref in args.refs:
        b, a, v1, v2 = parse_ref(ref)
        lines = idx.get((b, a))
        if not lines:
            print(f"== CE {b}.{a}: not found", file=sys.stderr)
            continue
        if v1 is not None:
            lines = [ln for ln in lines if v1 <= ln.verse <= v2]
        nmain = len({ln.verse for ln in idx[(b, a)] if ln.kind == "main"})
        print(f"== CE {b}.{a} ({BOOK_NAMES[b]}), {nmain} verses" + (f", showing {v1}-{v2}" if v1 else ""))
        print(format_verses(lines, args.all, args.ids))
        print()


def _compile(pattern: str, exact: bool):
    if exact:
        return re.compile(pattern, re.I), (lambda s: s)
    return re.compile(skel(pattern), re.I), skel


def cmd_search(args):
    rx, norm = _compile(args.pattern, args.exact)
    kinds = {"main"} | ({"star", "app"} if args.all else set())
    n = 0
    for ln in ce_lines():
        if args.book and ln.book != args.book:
            continue
        if ln.kind not in kinds:
            continue
        if rx.search(norm(ln.text)):
            n += 1
            if n <= args.limit:
                mark = {"main": " ", "star": "*", "app": "@"}[ln.kind]
                print(f"{mark}{ln.raw_id:<24} {ln.text}")
    print(f"-- {n} line(s)" + (f", first {args.limit} shown" if n > args.limit else ""), file=sys.stderr)


# --------------------------------------------------------------------------
# Ganguli
# --------------------------------------------------------------------------

_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s):
        v = _ROMAN[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def parse_ganguli_book(book: int) -> list[dict]:
    text = (GANGULI_DIR / f"maha{book:02d}.txt").read_text(encoding="utf-8", errors="replace")
    text = text.replace("\r", "")
    body = text.split("\nFOOTNOTES\n")[0]
    lines = body.split("\n")
    use_roman = any(re.fullmatch(r"SECTION [IVXLCDM]+", l.strip()) for l in lines)
    head = re.compile(r"SECTION ([IVXLCDM]+)") if use_roman else re.compile(r"(\d{1,3})")
    sections, cur, subparva = [], None, ""
    for l in lines:
        s = l.strip()
        m = head.fullmatch(s)
        if m:
            if cur:
                sections.append(cur)
            num = roman(m.group(1)) if use_roman else int(m.group(1))
            cur = {"book": book, "section": num, "subparva": subparva, "lines": []}
            continue
        if cur is None:
            continue
        pm = re.fullmatch(r"\[?\(([^()]*Parva[^()]*)\)\]?", s, flags=re.I)
        if pm and not any(x.strip() for x in cur["lines"]):
            name = re.sub(r"\s+continued\.?$", "", pm.group(1).strip(), flags=re.I)
            subparva = cur["subparva"] = name
            continue
        cur["lines"].append(l)
    if cur:
        sections.append(cur)
    for sec in sections:
        sec["text"] = "\n".join(sec.pop("lines")).strip()
    return sections


def build_ganguli_cache() -> int:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data = {b: parse_ganguli_book(b) for b in range(1, 19)}
    GANGULI_CACHE.write_text(json.dumps(data), encoding="utf-8")
    return sum(len(v) for v in data.values())


_g_cache = None


def ganguli() -> dict[int, list[dict]]:
    global _g_cache
    if _g_cache is None:
        if not GANGULI_CACHE.exists():
            build_ganguli_cache()
        raw = json.loads(GANGULI_CACHE.read_text(encoding="utf-8"))
        _g_cache = {int(k): v for k, v in raw.items()}
    return _g_cache


def ganguli_section(book: int, section: int) -> dict | None:
    for sec in ganguli()[book]:
        if sec["section"] == section:
            return sec
    return None


def cmd_gshow(args):
    for ref in args.refs:
        m = re.fullmatch(r"(\d+)\.(\d+)(?:-(\d+))?", ref)
        if not m:
            sys.exit(f"bad Ganguli reference {ref!r} (use BOOK.SECTION[-SECTION])")
        b, s1 = int(m.group(1)), int(m.group(2))
        s2 = int(m.group(3)) if m.group(3) else s1
        for s in range(s1, s2 + 1):
            sec = ganguli_section(b, s)
            if not sec:
                print(f"== Ganguli {b}.{s}: not found", file=sys.stderr)
                continue
            print(f"== Ganguli {b}.{s} ({sec['subparva']})")
            print(sec["text"])
            print()


def cmd_gsearch(args):
    rx = re.compile(args.pattern, re.I)
    n = 0
    for b, secs in ganguli().items():
        if args.book and b != args.book:
            continue
        for sec in secs:
            paras = re.split(r"\n\s*\n", sec["text"])
            for p in paras:
                flat = " ".join(p.split())
                if rx.search(flat):
                    n += 1
                    if n <= args.limit:
                        mm = rx.search(flat)
                        lo, hi = max(0, mm.start() - args.width), min(len(flat), mm.end() + args.width)
                        print(f"G {b}.{sec['section']} ({sec['subparva']}): ...{flat[lo:hi]}...")
    print(f"-- {n} paragraph(s)" + (f", first {args.limit} shown" if n > args.limit else ""), file=sys.stderr)


def cmd_gtoc(args):
    for sec in ganguli()[args.book]:
        first = " ".join(sec["text"].split())[:args.width]
        print(f"{args.book}.{sec['section']:<4} {sec['subparva'][:28]:<28} {first}")


# --------------------------------------------------------------------------
# Evidence check: where does something occur?
# --------------------------------------------------------------------------

def cmd_check(args):
    """Report occurrences of Sanskrit pattern(s) in CE main/star/app and an
    English pattern in Ganguli. The verdict is only a hint: read the passages."""
    counts = Counter()
    hits = defaultdict(list)
    rxs = [re.compile(skel(p), re.I) for p in args.sanskrit]
    for ln in ce_lines():
        if args.book and ln.book != args.book:
            continue
        t = skel(ln.text)
        if all(rx.search(t) for rx in rxs):
            counts[ln.kind] += 1
            hits[ln.kind].append(ln)
    print(f"Sanskrit pattern(s): {args.sanskrit}" + (f" (book {args.book})" if args.book else ""))
    for kind, label in (("main", "CE constituted text"), ("star", "CE star passages (rejected)"), ("app", "CE Appendix I (rejected)")):
        print(f"  {label:<32} {counts[kind]:>5}")
        for ln in hits[kind][: args.limit]:
            print(f"      {ln.raw_id:<24} {ln.text}")
    if args.english:
        rx = re.compile(args.english, re.I)
        g = []
        for b, secs in ganguli().items():
            if args.book and b != args.book:
                continue
            for sec in secs:
                flat = " ".join(sec["text"].split())
                for mm in rx.finditer(flat):
                    g.append((b, sec["section"], sec["subparva"], flat[max(0, mm.start() - 90): mm.end() + 90]))
        print(f"  {'Ganguli (vulgate) matches':<32} {len(g):>5}")
        for b, s, sp, ctx in g[: args.limit]:
            print(f"      G {b}.{s} ({sp}): ...{ctx}...")
    main, rej = counts["main"], counts["star"] + counts["app"]
    if main:
        verdict = "attested in the CE constituted text"
    elif rej:
        verdict = "only in passages the CE rejected (interpolation)"
    elif args.english and g:
        verdict = "in Ganguli/vulgate only (interpolation, not in CE)"
    else:
        verdict = "not found in CE or Ganguli (check spellings before concluding)"
    print(f"  Hint: {verdict}")


# --------------------------------------------------------------------------
# Speakers and stats
# --------------------------------------------------------------------------

def cmd_speakers(args):
    idx = ce_adhyaya_index()
    for ref in args.refs:
        b, a, _, _ = parse_ref(ref)
        print(f"== CE {b}.{a}")
        for ln in idx.get((b, a), []):
            if ln.kind == "main" and ln.suffix == "":
                print(f"  {ln.verse:>4}  {ln.text}")


def cmd_stats(args):
    per = defaultdict(lambda: {"adhyayas": set(), "verses": set(), "star": 0, "app": 0})
    for ln in ce_lines():
        if ln.adhyaya == 0:
            continue
        p = per[ln.book]
        p["adhyayas"].add(ln.adhyaya)
        if ln.kind == "main" and ln.suffix != "":
            p["verses"].add((ln.adhyaya, ln.verse))
        elif ln.kind == "star":
            p["star"] += 1
        elif ln.kind == "app":
            p["app"] += 1
    g = ganguli()
    print(f"{'Book':<22}{'CE adhy.':>9}{'CE verses':>10}{'star ln':>9}{'app ln':>8}{'Ganguli secs':>13}")
    tot = Counter()
    for b in range(1, 19):
        p = per[b]
        row = (len(p["adhyayas"]), len(p["verses"]), p["star"], p["app"], len(g[b]))
        tot.update(dict(zip(("a", "v", "s", "p", "g"), row)))
        print(f"{b:>2} {BOOK_NAMES[b]:<19}{row[0]:>9}{row[1]:>10}{row[2]:>9}{row[3]:>8}{row[4]:>13}")
    print(f"{'Total':<22}{tot['a']:>9}{tot['v']:>10}{tot['s']:>9}{tot['p']:>8}{tot['g']:>13}")


# --------------------------------------------------------------------------
# Concordance: CE adhyaya -> Ganguli section(s), by aligning proper names
# --------------------------------------------------------------------------

_CAP = re.compile(r"(?<=[a-z,;:] )([A-Z][a-z]{3,}(?:-[a-z]{2,})*)")


def _ganguli_name_stems() -> Counter:
    """Capitalised words that occur mid-sentence in Ganguli (mostly names)."""
    c = Counter()
    for secs in ganguli().values():
        for sec in secs:
            flat = " ".join(sec["text"].split())
            for w in _CAP.findall(flat):
                c[_gstem(w)] += 1
    return c


def _gstem(word: str) -> str:
    w = re.sub(r"'s$", "", word).replace("-", "")
    s = skel(w)
    if len(s) > 4 and s.endswith("s"):
        s = s[:-1]
    return s


def _load_concordance() -> dict[str, list[str]]:
    if not CONCORDANCE.exists():
        return {}
    out = {}
    with CONCORDANCE.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["ce"]] = row["ganguli"].split(";") if row["ganguli"] else []
    return out


def build_concordance(verbose: bool = False) -> None:
    stems_all = _ganguli_name_stems()
    # Keep stems that look like names: frequent enough, not English words.
    english = set("""this that with from have were been their there which when what
        whom whose then than they them into upon unto thus these those also even
        such very being having like will shall would should could might must
        mighty great king lord hero sire monarch there here after before""".split())
    stems = {s for s, n in stems_all.items() if n >= 3 and len(s) >= 4 and s not in english}
    stem_by_len = defaultdict(set)
    for s in stems:
        stem_by_len[len(s)].add(s)
    lens = sorted(stem_by_len)

    def ce_bag(lines):
        bag = Counter()
        for ln in lines:
            if ln.kind != "main":
                continue
            for w in skel(ln.text).split():
                for L in lens:
                    if L > len(w):
                        break
                    if w[:L] in stem_by_len[L]:
                        bag[w[:L]] += 1
        return bag

    def g_bag(text):
        bag = Counter()
        for w in _CAP.findall(" ".join(text.split())):
            s = _gstem(w)
            if s in stems:
                bag[s] += 1
        return bag

    idx = ce_adhyaya_index()
    rows = []
    for book in range(1, 19):
        adhs = sorted(a for (b, a) in idx if b == book)
        secs = ganguli()[book]
        A = [ce_bag(idx[(book, a)]) for a in adhs]
        G = [g_bag(s["text"]) for s in secs]
        # IDF over both sides of this book
        df = Counter()
        for bag in A + G:
            df.update(set(bag))
        N = len(A) + len(G)
        idf = {t: math.log((N + 1) / (d + 0.5)) for t, d in df.items()}

        def vec(bag):
            v = {t: (1 + math.log(c)) * idf[t] for t, c in bag.items()}
            norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
            return {t: x / norm for t, x in v.items()}

        VA, VG = [vec(b) for b in A], [vec(b) for b in G]

        def sim(i, j):
            a, g = VA[i], VG[j]
            if len(a) > len(g):
                a, g = g, a
            return sum(x * g.get(t, 0.0) for t, x in a.items())

        n, m = len(VA), len(VG)
        # Monotonic assignment: every Ganguli section j goes to one CE adhyaya
        # a(j), non-decreasing in j. Several sections may share an adhyaya
        # (the vulgate splits chapters and adds interpolated ones). Skipping CE
        # adhyayas costs SKIP each, since the vulgate rarely lacks CE text.
        # A weak positional prior breaks ties where names are sparse.
        SKIP, PRIOR = 0.5, 0.1

        def score(i, j):
            prior = 1.0 - abs(i / max(n - 1, 1) - j / max(m - 1, 1))
            return sim(i, j) + PRIOR * prior

        NEG = -1e18
        D = [[NEG] * n for _ in range(m)]
        P = [[-1] * n for _ in range(m)]
        for i in range(n):
            D[0][i] = score(i, 0) - SKIP * i
        for j in range(1, m):
            prev = D[j - 1]
            run_best, run_arg = NEG, -1   # max over i' <= i-2 of prev[i'] + SKIP*i'
            for i in range(n):
                if i >= 2 and prev[i - 2] + SKIP * (i - 2) > run_best:
                    run_best, run_arg = prev[i - 2] + SKIP * (i - 2), i - 2
                best, arg = prev[i], i                      # same adhyaya
                if i >= 1 and prev[i - 1] > best:           # next adhyaya
                    best, arg = prev[i - 1], i - 1
                if run_arg >= 0 and run_best - SKIP * (i - 1) > best:  # skip some
                    best, arg = run_best - SKIP * (i - 1), run_arg
                D[j][i], P[j][i] = best + score(i, j), arg
        last = max(range(n), key=lambda i: D[m - 1][i] - SKIP * (n - 1 - i))
        assign = [0] * m
        i = last
        for j in range(m - 1, -1, -1):
            assign[j] = i
            i = P[j][i]
        mapping = defaultdict(list)
        for j, i in enumerate(assign):
            mapping[i].append(j)
        prev_js = [0]
        for i, a in enumerate(adhs):
            js = mapping.get(i)
            note = ""
            if not js:          # no section of its own: merged into a neighbour
                js, note = prev_js[-1:], "merged"
            prev_js = js
            gs = [secs[j] for j in js]
            best = max(sim(i, j) for j in js)
            rows.append({
                "ce": f"{book}.{a}",
                "ganguli": ";".join(f"{book}.{s['section']}" for s in gs),
                "subparva": gs[0]["subparva"],
                "similarity": f"{best:.2f}",
                "note": note,
                "first_words_ganguli": " ".join(gs[0]["text"].split())[:70],
            })
        if verbose:
            print(f"book {book}: {n} CE adhyayas, {m} Ganguli sections", file=sys.stderr)
    CONCORDANCE.parent.mkdir(parents=True, exist_ok=True)
    with CONCORDANCE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {CONCORDANCE.relative_to(ROOT)} ({len(rows)} CE adhyayas)", file=sys.stderr)


def cmd_where(args):
    conc = _load_concordance()
    if not conc:
        sys.exit("No concordance yet: run `mbh.py concordance`.")
    for ref in args.refs:
        b, a, _, _ = parse_ref(ref)
        print(f"CE {b}.{a} -> Ganguli {', '.join(conc.get(f'{b}.{a}', ['?']))}")


# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("show", help="print CE text for references")
    p.add_argument("refs", nargs="+")
    p.add_argument("--all", action="store_true", help="include star (*) and appendix (@) passages")
    p.add_argument("--ids", action="store_true", help="one line per pada-line with raw IDs")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="search the CE")
    p.add_argument("pattern")
    p.add_argument("-b", "--book", type=int)
    p.add_argument("--all", action="store_true", help="also search star/appendix passages")
    p.add_argument("--exact", action="store_true", help="regex on IAST as written")
    p.add_argument("-n", "--limit", type=int, default=40)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("gshow", help="print Ganguli section(s)")
    p.add_argument("refs", nargs="+")
    p.set_defaults(func=cmd_gshow)

    p = sub.add_parser("gsearch", help="search Ganguli (regex)")
    p.add_argument("pattern")
    p.add_argument("-b", "--book", type=int)
    p.add_argument("-n", "--limit", type=int, default=40)
    p.add_argument("-w", "--width", type=int, default=100)
    p.set_defaults(func=cmd_gsearch)

    p = sub.add_parser("gtoc", help="Ganguli sections of a book")
    p.add_argument("book", type=int)
    p.add_argument("-w", "--width", type=int, default=70)
    p.set_defaults(func=cmd_gtoc)

    p = sub.add_parser("check", help="classify where a pattern occurs")
    p.add_argument("sanskrit", nargs="+", help="skeleton pattern(s); all must match the same line")
    p.add_argument("-e", "--english", help="regex to search in Ganguli")
    p.add_argument("-b", "--book", type=int)
    p.add_argument("-n", "--limit", type=int, default=8)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("where", help="Ganguli sections for CE adhyayas")
    p.add_argument("refs", nargs="+")
    p.set_defaults(func=cmd_where)

    p = sub.add_parser("speakers", help="speaker lines in CE adhyayas")
    p.add_argument("refs", nargs="+")
    p.set_defaults(func=cmd_speakers)

    p = sub.add_parser("stats", help="counts per book")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("build-cache", help="parse sources into sources/cache/")
    p.set_defaults(func=lambda a: print(
        f"CE lines: {build_ce_cache()}, Ganguli sections: {build_ganguli_cache()}", file=sys.stderr))

    p = sub.add_parser("concordance", help="rebuild index/concordance.csv")
    p.add_argument("-v", "--verbose", action="store_true")
    p.set_defaults(func=lambda a: build_concordance(a.verbose))

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
