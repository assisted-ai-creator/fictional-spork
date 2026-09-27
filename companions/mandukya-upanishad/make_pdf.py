#!/usr/bin/env python3
"""Typeset companions/mandukya-upanishad/README.md as a designed PDF.

    python3 companions/mandukya-upanishad/make_pdf.py [--out PATH]

Needs `pip install markdown playwright` and a Chromium (set CHROMIUM, or
the one under /opt/pw-browsers is used). Fonts are fetched once from npm
(Fontsource packages, SIL Open Font License) into build/fonts/mandukya:
Tiro Devanagari Sanskrit for the Sanskrit, EB Garamond for the English.
Page numbers and running heads are CSS @page margin boxes, so no PDF
post-processing is needed.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FONTS = ROOT / "build" / "fonts" / "mandukya"
PACKAGES = {
    "@fontsource/tiro-devanagari-sanskrit": [
        "tiro-devanagari-sanskrit-devanagari-400-normal.woff2",
        "tiro-devanagari-sanskrit-latin-400-normal.woff2",
    ],
    "@fontsource/eb-garamond": [
        f"eb-garamond-{s}-{w}-{st}.woff2"
        for s in ("latin", "latin-ext")
        for w in (400, 500, 600)
        for st in ("normal", "italic")
    ],
}
DEVA = re.compile(r"[ऀ-ॿ]")


def fetch_fonts() -> None:
    FONTS.mkdir(parents=True, exist_ok=True)
    for pkg, files in PACKAGES.items():
        if all((FONTS / f).exists() for f in files):
            continue
        with tempfile.TemporaryDirectory() as tmp:
            out = subprocess.run(["npm", "pack", "-q", pkg], cwd=tmp,
                                 check=True, capture_output=True, text=True)
            tgz = Path(tmp) / out.stdout.strip().splitlines()[-1]
            with tarfile.open(tgz) as tar:
                for f in files:
                    src = tar.extractfile(f"package/files/{f}")
                    (FONTS / f).write_bytes(src.read())


def font_css() -> str:
    rules = []
    for f in PACKAGES["@fontsource/tiro-devanagari-sanskrit"]:
        rules.append(f"@font-face{{font-family:'Tiro Sanskrit';"
                     f"src:url('{(FONTS / f).as_uri()}');}}")
    for f in PACKAGES["@fontsource/eb-garamond"]:
        _, _, subset, w, st = re.match(
            r"(eb)-(garamond)-(latin(?:-ext)?)-(\d+)-(\w+)", f).groups()
        rng = ("U+0000-00FF,U+2000-206F,U+2013-2014" if subset == "latin"
               else "U+0100-024F,U+1E00-1EFF,U+0300-036F")
        rules.append(f"@font-face{{font-family:'EB Garamond';font-weight:{w};"
                     f"font-style:{st};unicode-range:{rng};"
                     f"src:url('{(FONTS / f).as_uri()}');}}")
    return "\n".join(rules)


def prepare_markdown(md: str) -> str:
    # The PDF has its own title page; drop the H1 and the shell snippet.
    md = re.sub(r"\A# .*\n", "", md)
    md = re.sub(r"You can check the counts yourself:\n\n```bash\n.*?```\n\n",
                "", md, flags=re.S)
    # Keep the line breaks of Devanagari verse lines.
    lines = md.split("\n")
    for i, line in enumerate(lines[:-1]):
        if (line.startswith("> ") and DEVA.search(line)
                and lines[i + 1].startswith("> ")):
            lines[i] = line + "  "
    return "\n".join(lines)


def decorate(body: str) -> str:
    # Sanskrit and transliteration panels.
    # Markdown merges the two adjacent quotes into one, with two paragraphs.
    body = re.sub(r"<blockquote>\s*(<p>[^<]*[ऀ-ॿ](?:(?!</p>).)*</p>)\s*<p>(.*?)</p>\s*</blockquote>",
                  r'<div class="verse"><div class="sa">\1</div><div class="iast">\2</div></div>',
                  body, flags=re.S)
    body = body.replace("<p><strong>Translation.</strong>",
                        '<p class="translation"><span class="label">Translation</span>')
    body = body.replace("<p><strong>Hard words</strong></p>",
                        '<h4 class="label-h">Hard words</h4>')
    body = body.replace("<p><strong>What it is saying.</strong>",
                        '<h4 class="label-h">What it is saying</h4><p>')
    # "A modern picture" runs to the next <hr> or heading.
    body = re.sub(r"<p><strong>A modern picture\.</strong>(.*?)(?=<hr />|<h[23])",
                  r'<aside class="picture"><h4>A modern picture</h4><p>\1</aside>',
                  body, flags=re.S)
    # Mantra sections: number badge, one mantra per page.
    def mantra(m):
        return (f'<section class="mantra"><div class="badge">{m.group(1)}</div>'
                f'<h3><span class="kicker">Mantra {m.group(1)}</span>{m.group(2)}</h3>')
    body = re.sub(r"<h3>Mantra (\d+): (.*?)</h3>", mantra, body)
    body = re.sub(r"(<section class=\"mantra\">.*?)(?=<section class=\"mantra\">|<h2)",
                  r"\1</section>", body, flags=re.S)
    body = body.replace("<hr />", "")
    body = re.sub(r"<h2>", '<h2 class="part">', body)
    return body


CSS = r"""
:root{--ink:#1d2433;--soft:#4a5165;--saffron:#b8561b;--gold:#c99a3b;
--paper:#fbf7ef;--panel:#f3eadb;--line:#e2d5bd;--indigo:#27335a}
@page{size:A4;margin:22mm 20mm 22mm 20mm;
 @top-left{content:"The Mandukya Upanishad";font:italic 9pt 'EB Garamond';color:#8a7d66}
 @top-right{content:"माण्डूक्योपनिषत्";font:9pt 'Tiro Sanskrit';color:#8a7d66}
 @bottom-center{content:counter(page);font:10pt 'EB Garamond';color:#8a7d66}}
@page cover{margin:0;@top-left{content:none}@top-right{content:none}@bottom-center{content:none}}
html{background:var(--paper)}
body{font-family:'EB Garamond','Tiro Sanskrit',serif;font-size:11.6pt;line-height:1.55;
 color:var(--ink);margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;hyphens:auto}
.cover{page:cover;height:297mm;width:210mm;box-sizing:border-box;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;
 background:radial-gradient(circle at 50% 38%,#fff8ea 0,#f6ead3 45%,#ecdcbd 100%);
 border:10mm solid var(--indigo);outline:1.2mm solid var(--gold);outline-offset:-14mm;page-break-after:always}
.cover .om{font-family:'Tiro Sanskrit';font-size:150pt;line-height:1;color:var(--saffron);margin-bottom:6mm}
.cover h1{font-weight:500;font-size:34pt;letter-spacing:.04em;margin:0;color:var(--indigo)}
.cover .skt{font-family:'Tiro Sanskrit';font-size:22pt;color:var(--soft);margin:3mm 0 10mm}
.cover .rule{width:40mm;height:0;border-top:1px solid var(--gold);margin:0 auto 8mm}
.cover .sub{font-size:14pt;font-style:italic;max-width:120mm;color:var(--soft)}
.cover .foot{margin-top:24mm;font-size:10.5pt;letter-spacing:.12em;text-transform:uppercase;color:#8a7d66}
h2.part{font-weight:500;font-size:21pt;color:var(--indigo);margin:0 0 5mm;padding-bottom:2mm;
 border-bottom:1.5px solid var(--gold);break-before:page;break-after:avoid}
h2.part:first-of-type{break-before:auto}
h3{break-after:avoid}
p{margin:0 0 2.6mm;orphans:3;widows:3}
a{color:var(--saffron);text-decoration:none}
code{font-size:.9em}
table{border-collapse:collapse;width:100%;margin:3mm 0 5mm;font-size:10.4pt;break-inside:avoid}
th{background:var(--indigo);color:#fff;font-weight:500;text-align:left;padding:1.6mm 2.2mm}
td{padding:1.4mm 2.2mm;border-bottom:1px solid var(--line);vertical-align:top}
tr:nth-child(even) td{background:#f6efe2}
ul,ol{padding-left:6mm;margin:0 0 3mm}
li{margin-bottom:1.4mm}
blockquote{margin:3mm 0;padding:3mm 5mm;background:var(--panel);border-left:3px solid var(--gold)}
blockquote p{font-family:'Tiro Sanskrit','EB Garamond';margin:0}
section.mantra{break-before:page;position:relative}
.badge{position:absolute;right:0;top:0;width:15mm;height:15mm;border-radius:50%;
 background:var(--saffron);color:#fff;font-size:19pt;font-weight:600;text-align:center;line-height:15mm}
section.mantra h3{font-weight:500;font-size:20pt;color:var(--indigo);margin:0 20mm 5mm 0;line-height:1.2}
.kicker{display:block;font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--saffron);
 font-weight:600;margin-bottom:1mm}
.verse{background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--saffron);
 border-radius:2mm;padding:5mm 6mm;margin:0 0 5mm;break-inside:avoid;text-align:center}
.verse .sa p{font-family:'Tiro Sanskrit';font-size:15.5pt;line-height:1.75;margin:0;color:#2a1f14}
.verse .iast{font-size:10.6pt;color:var(--soft);margin-top:3mm;padding-top:3mm;border-top:1px dashed #d4c4a4}
.translation{font-size:13.4pt;line-height:1.55;border-left:3px solid var(--indigo);padding:1mm 0 1mm 5mm;margin:0 0 5mm}
.label{display:block;font-size:9pt;letter-spacing:.2em;text-transform:uppercase;color:var(--indigo);font-weight:600;margin-bottom:1mm}
h4.label-h{font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--saffron);font-weight:600;
 margin:5mm 0 2mm;break-after:avoid}
section.mantra ul li{margin-bottom:1.8mm}
aside.picture{background:#eef1f7;border:1px solid #d3d9e8;border-radius:2mm;padding:4mm 5mm 2mm;margin:5mm 0 2mm;break-inside:avoid}
aside.picture h4{margin:0 0 2mm;font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--indigo)}
aside.picture h4::before{content:"◆ ";color:var(--gold)}
em{font-style:italic}
"""


def build(out: Path) -> None:
    fetch_fonts()
    md = prepare_markdown((HERE / "README.md").read_text())
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "smarty"])
    body = decorate(body)
    cover = """<div class="cover"><div class="om">ॐ</div>
<h1>The Mandukya Upanishad</h1><div class="skt">माण्डूक्योपनिषत्</div><div class="rule"></div>
<div class="sub">The twelve mantras in plain English, with the Sanskrit,
the hard words explained, and pictures from everyday life</div>
<div class="foot">Atharvaveda · 12 mantras · 206 words</div></div>"""
    html = (f"<!doctype html><html lang='en-GB'><head><meta charset='utf-8'>"
            f"<title>The Mandukya Upanishad</title><style>{font_css()}{CSS}</style>"
            f"</head><body>{cover}{body}</body></html>")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        page_path = f.name
    exe = os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe)
        page = browser.new_page()
        page.goto(Path(page_path).as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        browser.close()
    os.unlink(page_path)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=HERE / "mandukya-upanishad.pdf")
    build(ap.parse_args().out.resolve())
