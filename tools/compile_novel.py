#!/usr/bin/env python3
"""Stitch the chapters into a reading edition.

    python3 tools/compile_novel.py            # build/manuscript.md + build/notes.md
    python3 tools/compile_novel.py --book 1   # one Book only

The reading edition drops each chapter's front matter and its notes block
(everything after `<!-- notes -->`). The notes are gathered, Book by Book,
into build/notes.md. Only chapters with status drafted/verified/revised
are included.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_index import BOOKS, ROOT, load_chapters, load_structure  # noqa: E402

BUILD = ROOT / "build"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", type=int)
    args = ap.parse_args(argv)

    chapters, problems = load_chapters(load_structure())
    for p in problems:
        print("PROBLEM  " + p, file=sys.stderr)
    front = ROOT / "novel" / "00-front-matter.md"
    body = [front.read_text(encoding="utf-8").strip()] if front.exists() and not args.book else []
    notes = ["# Notes\n"]
    current = None
    for c in chapters:
        m = c["meta"]
        if m.get("status") == "planned" or (args.book and m.get("book") != args.book):
            continue
        if m.get("book") != current:
            current = m.get("book")
            parva, title = BOOKS[current]
            body.append(f"\n\n# Book {current}: {title}\n\n*{parva} Parva*\n")
            notes.append(f"\n## Book {current}: {title}\n")
        raw = c["file"].read_text(encoding="utf-8")
        story = c["text"].strip()
        body.append("\n\n" + story)
        if "<!-- notes -->" in raw:
            n = raw.split("<!-- notes -->", 1)[1].strip()
            n = n.replace("## Notes", f"### Chapter {m.get('chapter')}: {m.get('title')}", 1)
            notes.append("\n" + n)
    BUILD.mkdir(exist_ok=True)
    suffix = f"-book{args.book:02d}" if args.book else ""
    (BUILD / f"manuscript{suffix}.md").write_text("\n".join(body).strip() + "\n", encoding="utf-8")
    (BUILD / f"notes{suffix}.md").write_text("\n".join(notes).strip() + "\n", encoding="utf-8")
    print(f"wrote build/manuscript{suffix}.md and build/notes{suffix}.md")


if __name__ == "__main__":
    main()
