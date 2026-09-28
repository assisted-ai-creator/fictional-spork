#!/usr/bin/env python3
"""Rewrap the prose of chapter files to a fixed width.

Only the narrative part is touched: the front matter, the title line, section
breaks (---) and everything after the `<!-- notes -->` marker are left as they
are. Paragraphs are separated by blank lines and rewrapped to WIDTH columns.
Footnote definitions (`[^label]: ...`) are rewrapped with a four-space
hanging indent, as Markdown footnotes need.

    python3 tools/reflow.py novel/book-01-adi/23-*.md
    python3 tools/reflow.py --check novel/**/*.md     # exit 1 if any would change
"""
from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

WIDTH = 80
MARKER = "<!-- notes -->"


def reflow_text(text: str, width: int = WIDTH) -> str:
    head, sep, rest = text.partition("\n---\n")
    if not text.startswith("---\n") or not sep:
        return text  # no front matter: leave alone
    body, msep, notes = rest.partition(MARKER)
    out = []
    for block in body.split("\n\n"):
        stripped = block.strip("\n")
        first = stripped.lstrip()
        if first.startswith("[^") and "]:" in first.split("\n", 1)[0]:
            # a footnote definition: rewrap with a hanging indent
            words = " ".join(stripped.split())
            out.append(textwrap.fill(words, width=width, subsequent_indent="    ",
                                     break_long_words=False, break_on_hyphens=False))
            continue
        if (not stripped or first.startswith(("#", "---", "|", "* ", "- ", ">"))
                or "\n    " in stripped):
            out.append(stripped)
            continue
        words = " ".join(stripped.split())
        out.append(textwrap.fill(words, width=width, break_long_words=False,
                                 break_on_hyphens=False))
    new_body = "\n\n".join(out)
    # keep the original leading/trailing blank lines around the body
    lead = body[: len(body) - len(body.lstrip("\n"))]
    trail = body[len(body.rstrip("\n")):]
    return head + sep + lead + new_body.strip("\n") + trail + msep + notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--check", action="store_true", help="report files that would change")
    args = ap.parse_args()
    changed = 0
    for p in map(Path, args.paths):
        old = p.read_text(encoding="utf-8")
        new = reflow_text(old)
        if new != old:
            changed += 1
            if args.check:
                print(f"would reflow: {p}")
            else:
                p.write_text(new, encoding="utf-8")
                print(f"reflowed: {p}")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
