#!/usr/bin/env python3
"""Typeset the drafted Books as a printable PDF.

    python3 tools/make_pdf.py                    # all drafted Books, A4
    python3 tools/make_pdf.py --books 1-3        # a range of Books
    python3 tools/make_pdf.py --size 6x9         # trade paperback trim
    python3 tools/make_pdf.py --out build/x.pdf

Unlike the other tools this one needs third-party packages, so it is best
run from a virtualenv:

    pip install markdown pypdf playwright

It drives the Chromium that Playwright finds (set CHROMIUM to a binary to
override; web sessions have one under /opt/pw-browsers). The typeface is EB
Garamond (SIL Open Font License), fetched once from npm into build/fonts;
without it the PDF falls back to the system serif.

What goes in: the reading text only, as in tools/compile_novel.py (front
matter and notes blocks are dropped). The PDF has a title page, the note to
the reader, a contents list with page numbers, a title page for each Book,
each chapter on a new page, running heads, page numbers and PDF bookmarks.

How: the book is laid out once as HTML and printed by Chromium. The chapter
start pages are read back from the PDF's bookmarks and written into the
contents list, and the book is printed again. A second Chromium pass prints
the running heads and page numbers on blank pages of the same size, which
are then stamped onto the book's pages.
"""
from __future__ import annotations

import argparse
import datetime
import glob
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_index import BOOKS, ROOT, load_chapters, load_structure  # noqa: E402

try:
    import markdown
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency ({e.name}); run: pip install markdown pypdf playwright")

BUILD = ROOT / "build"
FONTS = BUILD / "fonts"
NUMBER_WORDS = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen"]

SIZES = {
    # width, height, margins (top, outer, bottom, inner), body size, leading
    "a4": ("210mm", "297mm", ("26mm", "29mm", "27mm", "31mm"), "12.5pt", 1.42),
    "6x9": ("6in", "9in", ("17mm", "15mm", "19mm", "18mm"), "10.5pt", 1.38),
}


# --------------------------------------------------------------------------- fonts

def ensure_fonts() -> list[Path]:
    """EB Garamond woff2 files from the @fontsource npm package, cached in build/fonts."""
    want = [f"eb-garamond-{sub}-{w}-{st}.woff2"
            for sub in ("latin", "latin-ext") for w in (400, 500, 600) for st in ("normal", "italic")]
    have = [FONTS / f for f in want if (FONTS / f).exists()]
    if len(have) == len(want):
        return have
    FONTS.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["npm", "pack", "-q", "@fontsource/eb-garamond"], cwd=tmp, check=True,
                           capture_output=True)
            tgz = glob.glob(os.path.join(tmp, "*.tgz"))[0]
            subprocess.run(["tar", "xzf", tgz], cwd=tmp, check=True)
            for f in want:
                src = Path(tmp) / "package" / "files" / f
                if src.exists():
                    (FONTS / f).write_bytes(src.read_bytes())
    except Exception as e:  # noqa: BLE001
        print(f"note: could not fetch EB Garamond ({e}); using the system serif", file=sys.stderr)
    return [FONTS / f for f in want if (FONTS / f).exists()]


def font_css(files: list[Path]) -> str:
    out = []
    for f in files:
        m = re.match(r"eb-garamond-(latin(?:-ext)?)-(\d+)-(normal|italic)\.woff2", f.name)
        sub, weight, style = m.groups()
        rng = ("U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, "
               "U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
               if sub == "latin" else
               "U+0100-02AF, U+0304, U+0308, U+0329, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, "
               "U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF")
        out.append(f"@font-face {{ font-family: 'EB Garamond'; font-style: {style}; font-weight: {weight}; "
                   f"src: url('{f.as_uri()}') format('woff2'); unicode-range: {rng}; }}")
    return "\n".join(out)


# --------------------------------------------------------------------------- content

def md(text: str) -> str:
    # Keep the line breaks of verse set in blockquotes.
    lines = [(ln.rstrip() + "  ") if ln.lstrip().startswith(">") else ln for ln in text.splitlines()]
    body = markdown.markdown("\n".join(lines), extensions=["smarty", "footnotes"], output_format="html")
    return body.replace("<hr />", '<hr class="break">').replace("<hr>", '<hr class="break">')


def load(books: set[int]):
    chapters, problems = load_chapters(load_structure())
    for p in problems:
        print("PROBLEM  " + p, file=sys.stderr)
    out = []
    for c in chapters:
        m = c["meta"]
        if m.get("status") == "planned" or m.get("book") not in books:
            continue
        story = c["text"].strip()
        story = re.sub(r"\A#\s+.*\n", "", story, count=1).strip()  # our own heading replaces it
        out.append({"book": m["book"], "chapter": m["chapter"], "title": m["title"], "html": md(story)})
    return out


def front_note() -> str:
    front = ROOT / "novel" / "00-front-matter.md"
    text = front.read_text(encoding="utf-8")
    # The title and subtitle are set on the title page; keep the rest.
    text = re.sub(r"\A#\s.*\n+##\s.*\n+(---\n+)?", "", text)
    return md(text)


def build_html(chs, books, size, fonts, toc_pages=None, date=None) -> str:
    w, h, (mt, mo, mb, mi), fs, lh = SIZES[size]
    first, last = min(books), max(books)
    span = f"Book {NUMBER_WORDS[first]}" if first == last else \
        f"Books {NUMBER_WORDS[first]} to {NUMBER_WORDS[last]}"
    titles = " · ".join(BOOKS[b][1] for b in sorted(books))
    toc_pages = toc_pages or {}

    def pg(key):
        return str(toc_pages.get(key, "000"))

    parts = []
    parts.append(f"""
<section class="title-page">
  <div class="t-main">The Mahabharata</div>
  <div class="t-sub">Vyasa’s Epic, Told in Plain English</div>
  <div class="t-orn">❦</div>
  <div class="t-span">{span}</div>
  <div class="t-books">{html.escape(titles)}</div>
  <div class="t-foot">Retold from the Critical Edition<br>of the Bhandarkar Oriental Research Institute</div>
</section>
<section class="edition">
  <p>This volume contains {span} of the eighteen Books of the Mahabharata,
  retold in plain English from the constituted text of the Critical Edition. Passages that the Critical
  Edition sets aside are not narrated.</p>
  <p>Working draft, compiled {date}.</p>
</section>
<section class="note"><h1 class="front">A Note to the Reader</h1>{front_note()}</section>
""")
    # Contents
    toc = ['<section class="contents"><h1 class="front">Contents</h1>']
    for b in sorted(books):
        toc.append(f'<div class="toc-book"><span class="tb">Book {NUMBER_WORDS[b]}: '
                   f'{html.escape(BOOKS[b][1])}</span><span class="pg">{pg(("b", b))}</span></div>')
        for c in (c for c in chs if c["book"] == b):
            toc.append(f'<div class="toc-ch"><span class="n">{c["chapter"]}</span>'
                       f'<span class="t">{html.escape(c["title"])}</span><span class="dots"></span>'
                       f'<span class="pg">{pg(("c", b, c["chapter"]))}</span></div>')
    toc.append("</section>")
    parts.append("\n".join(toc))
    # Books and chapters
    for b in sorted(books):
        parva, title = BOOKS[b]
        parts.append(f'<section class="book-title"><div class="bk-n">Book {NUMBER_WORDS[b]}</div>'
                     f'<h1 class="bk">{html.escape(title)}</h1>'
                     f'<div class="bk-p">The {html.escape(parva)} Parva</div></section>')
        for c in (c for c in chs if c["book"] == b):
            parts.append(f'<section class="chapter"><div class="ch-n">Chapter {c["chapter"]}</div>'
                         f'<h2 class="ch">{html.escape(c["title"])}</h2>'
                         f'<div class="ch-orn">❧</div>{c["html"]}</section>')

    css = f"""
{font_css(fonts)}
@page {{ size: {w} {h}; margin: {mt} {mo} {mb} {mi}; }}
html {{ font-family: 'EB Garamond', 'Liberation Serif', 'FreeSerif', serif; font-size: {fs};
        line-height: {lh}; color: #111; font-kerning: normal;
        font-variant-ligatures: common-ligatures; font-feature-settings: 'kern', 'liga', 'onum'; }}
body {{ margin: 0; }}
p {{ margin: 0; text-align: justify; hyphens: auto; text-indent: 1.3em; orphans: 2; widows: 2; }}
section {{ break-before: page; }}
section:first-child {{ break-before: auto; }}
h1, h2 {{ font-weight: 500; break-after: avoid; }}
em {{ font-style: italic; }}
blockquote {{ margin: 0.8em 2em; font-style: italic; }}
blockquote p {{ text-indent: 0; text-align: left; }}
blockquote em {{ font-style: normal; }}
blockquote + p, h1 + p, h2 + p, .ch-orn + p, hr + p, .front + p {{ text-indent: 0; }}
hr.break {{ border: 0; height: 1.4em; margin: 0.5em 0 0.4em; text-align: center; break-after: avoid; }}
hr.break::after {{ content: '*\\2003*\\2003*'; font-size: 1.05em; color: #333; }}

.title-page {{ text-align: center; padding-top: 22%; }}
.t-main {{ font-size: 3.1em; font-weight: 500; letter-spacing: 0.04em; line-height: 1.1; }}
.t-sub {{ font-size: 1.35em; font-style: italic; margin-top: 0.6em; }}
.t-orn {{ font-size: 1.6em; margin: 2.2em 0 1.8em; }}
.t-span {{ font-variant: small-caps; letter-spacing: 0.12em; font-size: 1.15em; }}
.t-books {{ font-style: italic; margin-top: 0.4em; }}
.t-foot {{ margin-top: 38%; font-size: 0.95em; font-variant: small-caps; letter-spacing: 0.06em; }}
.edition {{ padding-top: 60%; font-size: 0.9em; }}
.edition p {{ text-indent: 0; text-align: left; margin-bottom: 0.8em; }}
h1.front {{ text-align: center; font-size: 1.6em; margin: 1.5em 0 1.4em; letter-spacing: 0.03em; }}
.note h1:not(.front), .note h2, .note h3 {{ display: none; }}
.note p {{ margin-bottom: 0.1em; }}

.contents h1.front {{ margin-bottom: 1em; }}
.toc-book {{ display: flex; font-variant: small-caps; letter-spacing: 0.06em; font-weight: 500;
            margin: 1.1em 0 0.35em; break-after: avoid; }}
.toc-book .tb {{ flex: 1; }}
.toc-ch {{ display: flex; align-items: baseline; font-size: 0.95em; line-height: 1.32; }}
.toc-ch .n {{ width: 2.2em; text-align: right; padding-right: 0.8em; font-variant-numeric: oldstyle-nums; }}
.toc-ch .dots {{ flex: 1; border-bottom: 1px dotted #888; margin: 0 0.4em; transform: translateY(-0.25em); }}
.pg {{ min-width: 2.2em; text-align: right; font-variant-numeric: oldstyle-nums; }}

.book-title {{ text-align: center; padding-top: 30%; }}
.bk-n {{ font-variant: small-caps; letter-spacing: 0.2em; font-size: 1.2em; }}
h1.bk {{ font-size: 2.6em; margin: 0.35em 0 0.4em; letter-spacing: 0.02em; }}
.bk-p {{ font-style: italic; font-size: 1.1em; }}

.chapter {{ padding-top: 12%; }}
.ch-n {{ text-align: center; font-variant: small-caps; letter-spacing: 0.16em; font-size: 1.0em; }}
h2.ch {{ text-align: center; font-size: 1.75em; margin: 0.25em 0 0.2em; line-height: 1.2; }}
.ch-orn {{ text-align: center; font-size: 1.1em; margin: 0.2em 0 1.6em; color: #444; }}
"""
    return (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
            f'<title>The Mahabharata</title><style>{css}</style></head><body>'
            + "\n".join(parts) + "</body></html>")


# --------------------------------------------------------------------------- rendering

def chromium_path():
    if os.environ.get("CHROMIUM"):
        return os.environ["CHROMIUM"]
    found = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
    return found[-1] if found else None


def render(pw, html_text: str, out: Path, size: str):
    w, h = SIZES[size][:2]
    exe = chromium_path()
    browser = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
    page = browser.new_page()
    page.set_default_timeout(0)
    src = out.with_suffix(".html")
    src.write_text(html_text, encoding="utf-8")
    page.goto(src.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    page.pdf(path=str(out), width=w, height=h, prefer_css_page_size=True, print_background=True,
             outline=True, tagged=True)
    browser.close()


def outline_pages(pdf: Path):
    """Map ('b', book) and ('c', book, chapter) to 0-based page indexes, from the PDF's bookmarks."""
    r = PdfReader(str(pdf))
    flat = []

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                flat.append((it.title.strip(), r.get_destination_page_number(it)))
    walk(r.outline)
    return flat, len(r.pages)


def page_map(flat, chs, books):
    """Assign the bookmarks (in reading order) to Books and chapters."""
    keys = []
    for b in sorted(books):
        keys.append((("b", b), BOOKS[b][1]))
        for c in (c for c in chs if c["book"] == b):
            keys.append((("c", b, c["chapter"]), c["title"]))
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731
    pages, i = {}, 0
    for key, title in keys:
        while i < len(flat) and norm(flat[i][0]) != norm(title):
            i += 1
        if i == len(flat):
            raise SystemExit(f"could not find bookmark for {key} {title!r}")
        pages[key] = flat[i][1]
        i += 1
    return pages


def stamp(pw, body_pdf: Path, pages: dict, chs, books, size: str, out: Path):
    """Print running heads and folios on blank pages and merge them onto the book."""
    w, h, (mt, mo, mb, mi), fs, _ = SIZES[size]
    total = len(PdfReader(str(body_pdf)).pages)
    starts = sorted((p, k) for k, p in pages.items())
    title_of = {("c", c["book"], c["chapter"]): c["title"] for c in chs}
    book_pages = {p for k, p in pages.items() if k[0] == "b"}
    chapter_starts = {p for k, p in pages.items() if k[0] == "c"}
    first_body = min(pages.values())
    divs = []
    for i in range(total):
        cur = None
        for p, k in starts:
            if p <= i:
                cur = k
        head = folio = ""
        if i >= 2:  # no folio on the title and edition pages
            folio = str(i + 1)
        if i in book_pages:
            folio = ""
        if cur and cur[0] == "c" and i not in chapter_starts and i >= first_body:
            b = cur[1]
            left = f"Book {NUMBER_WORDS[b]}: {BOOKS[b][1]}"
            head = f'<span class="l">{html.escape(left)}</span><span class="r">{html.escape(title_of[cur])}</span>'
        divs.append(f'<div class="pg"><div class="head">{head}</div><div class="folio">{folio}</div></div>')
    css = f"""
{font_css(ensure_fonts())}
@page {{ size: {w} {h}; margin: 0; }}
body {{ margin: 0; font-family: 'EB Garamond', 'Liberation Serif', serif; font-size: {fs}; }}
.pg {{ width: {w}; height: {h}; position: relative; break-after: page; overflow: hidden; }}
.head {{ position: absolute; top: calc({mt} - 11mm); left: {mi}; right: {mo}; display: flex;
         justify-content: space-between; font-size: 0.8em; font-variant: small-caps;
         letter-spacing: 0.08em; color: #444; border-bottom: 0.3pt solid #999; padding-bottom: 1.5mm; }}
.head:empty {{ border: 0; }}
.folio {{ position: absolute; bottom: calc({mb} - 13mm); left: 0; right: 0; text-align: center;
          font-size: 0.9em; font-variant-numeric: oldstyle-nums; color: #333; }}
"""
    overlay = out.with_name(out.stem + ".overlay.pdf")
    html_text = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(divs)}</body></html>"
    exe = chromium_path()
    browser = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
    page = browser.new_page()
    page.set_default_timeout(0)
    src = overlay.with_suffix(".html")
    src.write_text(html_text, encoding="utf-8")
    page.goto(src.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    page.pdf(path=str(overlay), width=w, height=h, prefer_css_page_size=True)
    browser.close()

    writer = PdfWriter(clone_from=str(body_pdf))
    ov = PdfReader(str(overlay))
    assert len(ov.pages) == len(writer.pages), (len(ov.pages), len(writer.pages))
    for bp, op in zip(writer.pages, ov.pages):
        bp.merge_page(op)
    writer.add_metadata({"/Title": "The Mahabharata: Vyasa's Epic, Told in Plain English",
                         "/Subject": ", ".join(f"Book {b}: {BOOKS[b][1]}" for b in sorted(books)),
                         "/Creator": "tools/make_pdf.py"})
    writer.page_mode = "/UseOutlines"
    # Stamping copies the overlay's font resources onto every page; fold the copies together.
    for pg_ in writer.pages:
        pg_.compress_content_streams()
    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    with open(out, "wb") as f:
        writer.write(f)
    for tmp in (overlay, src):
        tmp.unlink(missing_ok=True)


# --------------------------------------------------------------------------- main

def parse_books(spec: str | None, available: set[int]) -> set[int]:
    if not spec:
        return available
    out = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out |= set(range(int(a), int(b or a) + 1))
    return out & available


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--books", help="e.g. 1-3 or 2,3 (default: every drafted Book)")
    ap.add_argument("--size", choices=sorted(SIZES), default="a4")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)

    all_chs = load(set(BOOKS))
    books = parse_books(args.books, {c["book"] for c in all_chs})
    if not books:
        sys.exit("no drafted chapters in that range")
    chs = [c for c in all_chs if c["book"] in books]
    first, last = min(books), max(books)
    name = f"mahabharata-book{first:02d}" + (f"-{last:02d}" if last != first else "") + f"-{args.size}.pdf"
    out = (args.out or BUILD / name).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    fonts = ensure_fonts()
    date = datetime.date.today().strftime("%-d %B %Y")
    body = out.with_name(out.stem + ".body.pdf")

    with sync_playwright() as pw:
        pages = {}
        for attempt in range(3):
            render(pw, build_html(chs, books, args.size, fonts, {k: v + 1 for k, v in pages.items()}, date),
                   body, args.size)
            flat, total = outline_pages(body)
            new = page_map(flat, chs, books)
            if new == pages:
                break
            pages = new
            print(f"pass {attempt + 1}: {total} pages", file=sys.stderr)
        stamp(pw, body, pages, chs, books, args.size, out)
    body.unlink(missing_ok=True)
    body.with_suffix(".html").unlink(missing_ok=True)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} "
          f"({len(PdfReader(str(out)).pages)} pages, {len(chs)} chapters)")


if __name__ == "__main__":
    main()
