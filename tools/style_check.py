#!/usr/bin/env python3
"""Check novel chapters against the house style (workbook/STYLE_GUIDE.md).

    python3 tools/style_check.py novel/                 # every chapter
    python3 tools/style_check.py novel/book-01-adi/01-*.md
    python3 tools/style_check.py --strict novel/        # exit 1 on any error

Reports readability (Flesch, Flesch-Kincaid, sentence length), em-dash rate,
banned words and patterns, archaic English, name misspellings from
workbook/names.json, and names that are not in Vyasa's text (watch-list).
Only the story text is checked: front matter and the notes block after
`<!-- notes -->` are ignored.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMES = ROOT / "workbook" / "names.json"

# (regex, message). Errors must be fixed; warnings need a human look.
BANNED = [
    (r"\bdelv(e|es|ed|ing)\b", "AI-tell word"),
    (r"\btapestr(y|ies)\b", "AI-tell word"),
    (r"\btestament\b", "AI-tell word"),
    (r"\bintricate(ly)?\b", "AI-tell word"),
    (r"\bpivotal\b", "AI-tell word"),
    (r"\bcrucial\b", "AI-tell word"),
    (r"\bvibrant\b", "AI-tell word"),
    (r"\brealms?\b", "AI-tell word"),
    (r"\bbeacon\b", "AI-tell word"),
    (r"\bembark(s|ed|ing)?\b", "AI-tell word"),
    (r"\bunwavering\b", "AI-tell word"),
    (r"\bresonat(e|es|ed|ing)\b", "AI-tell word"),
    (r"\bunderscor(e|es|ed|ing)\b", "AI-tell word"),
    (r"\bfoster(s|ed|ing)?\b", "AI-tell word"),
    (r"\bpalpable\b", "AI-tell word"),
    (r"\ba (symphony|dance) of\b", "AI-tell phrase"),
    (r"\bit(?: i|')s (important|worth) (to note|noting)\b", "AI-tell phrase"),
    (r"\blittle did (he|she|they|anyone) know\b", "cliché"),
    (r"\bin that moment\b", "cliché"),
    (r"\bcould(n't| not) help but\b", "cliché"),
    (r"\ba sense of\b", "vague phrase"),
    (r"\bthe weight of\b", "cliché"),
    (r"\bechoed through\b", "cliché"),
    (r"\bsent shivers\b", "cliché"),
    (r"\beyes that held\b", "cliché"),
    (r"\bstands? as\b", "puffery"),
    # Archaic English
    (r"\b(thou|thee|thy|thine|hath|doth|hast|verily|wherefore|ere|unto)\b", "archaic English"),
    (r"\bO (king|monarch|best|son|tiger|lord|bull|chief|foremost|great|mighty|scorcher)\b", "archaic vocative"),
    (r"\blo\b[,!]", "archaic English"),
    # Modern idiom
    (r"\b(okay|guys|toxic|trauma|traumatized|process(ed|ing)? (his|her|their) (grief|feelings))\b", "modern idiom"),
]

WARN = [
    (r"\bsuddenly\b", "'suddenly': is it earned?"),
    (r"\bjourney\b", "'journey': literal travel only"),
    (r"\blandscape\b", "'landscape': literal only"),
    (r"\bIt (was|is) not [^.!?]{1,50}[.!?] It (was|is)\b", "'not X. It was Y' construction"),
    (r"\bnot (just|only|merely) [^.!?,]{1,40}, but\b", "'not just X, but Y' construction"),
    (r"\b(color|honor|armor|gray|center|favor|neighbor|valor|rumor|harbor|labor|behavior|jewelry|plow|traveled|traveling|defense|offense)\b", "American spelling (house style is British)"),
]


def story_text(path: Path) -> tuple[str, int]:
    """Return the story text (no front matter, no notes) and its first line number."""
    raw = path.read_text(encoding="utf-8")
    offset = 0
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            offset = raw[: end + 4].count("\n")
            raw = raw[end + 4:]
    raw = raw.split("<!-- notes -->")[0]
    return raw, offset


def words_of(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def syllables(word: str) -> int:
    w = word.lower().strip("'’-")
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:es|ed|e)$", "", w) or w
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups))


def sentences_of(text: str) -> list[str]:
    body = re.sub(r"^#.*$", "", text, flags=re.M)          # drop headings
    body = re.sub(r"\[\^[^\]]+\]:?", "", body)              # drop footnote marks
    body = re.sub(r"\s+", " ", body)
    parts = re.split(r"(?<=[.!?])[\"'”’)]*\s+(?=[\"'“‘(]*[A-Z])", body)
    return [p for p in parts if words_of(p)]


def load_names():
    if not NAMES.exists():
        return [], []
    data = json.loads(NAMES.read_text(encoding="utf-8"))
    flags = []
    for p in data.get("people", []):
        for v in p.get("flag", []):
            flags.append((re.compile(rf"\b{re.escape(v)}\b"), f"spelling: use '{p['name']}', not '{v}'"))
    watch = [(re.compile(w["match"], re.I | re.S), f"not in Vyasa? {w['name']} ({w['ledger']}): {w['note']}")
             for w in data.get("not_vyasa", [])]
    return flags, watch


def check(path: Path, name_flags, watch) -> dict:
    text, offset = story_text(path)
    lines = text.split("\n")
    errors, warnings = [], []

    def scan(patterns, bucket, flags=re.I):
        for rx, msg in patterns:
            crx = rx if isinstance(rx, re.Pattern) else re.compile(rx, flags)
            for i, line in enumerate(lines, start=offset + 1):
                for m in crx.finditer(line):
                    bucket.append(f"{path.name}:{i}: {msg}: '{m.group(0)}'")

    scan(BANNED, errors)
    scan(WARN, warnings)
    scan(name_flags, errors, 0)
    for rx, msg in watch:                      # may span lines
        for m in rx.finditer(text):
            ln = offset + 1 + text[: m.start()].count("\n")
            warnings.append(f"{path.name}:{ln}: {msg}")

    ws = words_of(text)
    sents = sentences_of(text)
    n_w, n_s = len(ws), max(1, len(sents))
    n_syl = sum(syllables(w) for w in ws)
    asl = n_w / n_s
    asw = n_syl / max(1, n_w)
    fre = 206.835 - 1.015 * asl - 84.6 * asw
    fk = 0.39 * asl + 11.8 * asw - 15.59
    long_pct = 100 * sum(1 for s in sents if len(words_of(s)) > 35) / n_s
    dashes = text.count("—") + text.count(" -- ")
    dash_rate = 1000 * dashes / max(1, n_w)

    metrics = {"words": n_w, "sentences": n_s, "avg_sentence": asl, "flesch": fre,
               "fk_grade": fk, "long_pct": long_pct, "dash_per_1000": dash_rate}
    limits = [("avg_sentence", asl <= 20, "average sentence length > 20 words"),
              ("flesch", fre >= 60, "Flesch Reading Ease < 60"),
              ("fk_grade", fk <= 9, "Flesch-Kincaid grade > 9"),
              ("long_pct", long_pct < 6, "over 6% of sentences exceed 35 words"),
              ("dash_per_1000", dash_rate <= 6, "more than 6 em dashes per 1,000 words")]
    for _, ok, msg in limits:
        if not ok and n_w >= 300:
            errors.append(f"{path.name}: {msg}")
    return {"path": path, "metrics": metrics, "errors": errors, "warnings": warnings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any chapter has errors")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print problems")
    args = ap.parse_args(argv)

    files = []
    for p in map(Path, args.paths):
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    files = [f for f in files if not f.name.startswith(("00-", "README"))]
    name_flags, watch = load_names()
    bad = 0
    for f in files:
        r = check(f, name_flags, watch)
        m = r["metrics"]
        if not args.quiet or r["errors"] or r["warnings"]:
            shown = f.resolve()
            shown = shown.relative_to(ROOT) if shown.is_relative_to(ROOT) else shown
            print(f"{shown}: {m['words']} words, "
                  f"avg sentence {m['avg_sentence']:.1f}, Flesch {m['flesch']:.0f}, "
                  f"grade {m['fk_grade']:.1f}, long {m['long_pct']:.1f}%, "
                  f"dashes/1k {m['dash_per_1000']:.1f}")
        for e in r["errors"]:
            print("  ERROR  " + e)
        for w in r["warnings"]:
            print("  warn   " + w)
        bad += bool(r["errors"])
    if args.strict and bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
