#!/usr/bin/env python3
"""Typeset the Bhagavad Gita (Book 6, chapters 7-13) as a colour study edition,
and the family line of the Moon as a tree.

    python3 tools/make_gita_pdf.py          # writes build/gita/*.pdf

Outputs:
  build/gita/bhagavad-gita-told-simply.pdf   the Gita in 18 chapters, colour-coded
      by speaker, every explanation card placed right after the passage that uses
      it, a glossary, and the family tree as an appendix;
  build/gita/the-line-of-the-moon.pdf        the family tree on its own.

The Gita text and the explanations come straight from the novel's chapter files;
nothing is rewritten here. The family tree uses the Critical Edition (1.70,
1.90, 7.119) for the main line and marks clearly what comes from the Bhagavata
Purana (Book 9) instead. Needs the same packages as make_pdf.py.
"""
from __future__ import annotations

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
from make_pdf import BUILD, FONTS, ROOT, chromium_path, ensure_fonts  # noqa: E402

try:
    import markdown
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency ({e.name}); run: pip install markdown pypdf playwright")

OUT = BUILD / "gita"
BOOK6 = ROOT / "novel" / "book-06-bhishma"
FILES = ["07-arjunas-despair.md", "08-action.md", "09-the-steady-mind.md", "10-the-imperishable.md",
         "11-the-form-of-all.md", "12-the-field-and-the-strands.md", "13-freedom.md"]

# Where each of the 18 Gita chapters (CE 6.23-40) begins: (file, paragraph index).
STARTS = {1: (0, 1), 2: (0, 16), 3: (1, 1), 4: (1, 18), 5: (1, 33), 6: (2, 1), 7: (2, 18),
          8: (3, 1), 9: (3, 11), 10: (3, 21), 11: (4, 1), 12: (4, 20), 13: (5, 1), 14: (5, 12),
          15: (5, 21), 16: (6, 1), 17: (6, 8), 18: (6, 15)}
TITLES = {1: "Arjuna's Despair", 2: "The Self That Never Dies", 3: "Action",
          4: "Knowledge and Sacrifice", 5: "Giving Up and Doing", 6: "The Steady Mind",
          7: "Knowing Me Fully", 8: "The Imperishable", 9: "The Deepest Secret",
          10: "My Divine Powers", 11: "The Form of All", 12: "Love and Devotion",
          13: "The Field and Its Knower", 14: "The Three Strands", 15: "The Highest Person",
          16: "The Godlike and the Demonic", 17: "Three Kinds of Faith", 18: "Freedom"}

# Paragraphs whose speaker the simple rules below would get wrong: (file, paragraph) -> speaker.
OVERRIDES = {(0, 3): "Duryodhana", (0, 4): "Duryodhana", (0, 8): "Arjuna",
             **{(0, i): "Arjuna" for i in range(11, 15)},
             **{(4, i): "Arjuna" for i in range(4, 10)},
             **{(4, i): "Arjuna" for i in range(12, 16)}}

SPEAKERS = {  # name: (ink, tint, one line)
    "Krishna": ("#3b5578", "", "teacher and Arjuna's charioteer; Vasudeva, Keshava, Madhava"),
    "Arjuna": ("#8a4a3c", "", "the Pandava archer who will not fight; Partha, Dhananjaya"),
    "Sanjaya": ("#4f6b55", "", "the king's charioteer, who tells all of this with the sight Vyasa gave him"),
    "Dhritarashtra": ("#6b5e7d", "", "the blind king who asks what happened"),
    "Duryodhana": ("#8c6a3a", "", "Dhritarashtra's eldest son, speaking to his teacher Drona"),
}


# --------------------------------------------------------------------------- parsing

def chapter_parts(path: Path):
    s = path.read_text(encoding="utf-8")
    body = s.split("\n---\n", 1)[1]
    story, _, rest = body.partition("## Explanations")
    defs_text = rest.split("<!-- notes -->")[0]
    notes = rest.split("<!-- notes -->")[1] if "<!-- notes -->" in rest else ""
    paras = [re.sub(r"\s+", " ", p).strip() for p in story.split("\n\n") if p.strip()]
    defs = {}
    for m in re.finditer(r"^\[\^([^\]]+)\]:\s*(.*?)(?=^\[\^|\Z)", defs_text, re.S | re.M):
        defs[m.group(1)] = re.sub(r"\s+", " ", m.group(2)).strip()
    scenes = re.findall(r"^\| (.+?) \| (6\.\d+)\.[\d–-]+", notes, re.M)
    return paras, defs, scenes


def speaker_of(p: str, prev_quoted: str) -> str:
    if "said Dhritarashtra" in p:
        return "Dhritarashtra"
    m = re.search(r"said (Arjuna|Krishna)|(Arjuna|Krishna) said", p)
    if p.startswith("\"'"):
        return (m.group(1) or m.group(2)) if m else prev_quoted
    return "Sanjaya"


def split_def(text: str):
    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", text)
    term, rest = (m.group(1), m.group(2)) if m else ("", text)
    term = term.rstrip(".")
    parts = re.split(r"\*(What it means|What they mean|Everyday example|In the story|Note):\*", rest)
    secs = []
    if parts[0].strip():
        secs.append(("What it means", parts[0].strip()))
    for i in range(1, len(parts), 2):
        secs.append((parts[i], parts[i + 1].strip()))
    secs = [(lab, txt[:1].upper() + txt[1:]) for lab, txt in secs]
    return term, secs


def md_inline(text: str) -> str:
    out = markdown.markdown(text, extensions=["smarty"])
    return re.sub(r"^<p>|</p>$", "", out.strip())


# --------------------------------------------------------------------------- the Gita

WHEEL = """<svg class="{cls}" viewBox="-50 -50 100 100" aria-hidden="true">
<circle r="46" fill="none" stroke="currentColor" stroke-width="3"/>
<circle r="38" fill="none" stroke="currentColor" stroke-width="1"/>
<circle r="9" fill="none" stroke="currentColor" stroke-width="3"/>
<circle r="3" fill="currentColor"/>
{spokes}
{petals}
</svg>"""


def wheel(cls="wheel"):
    import math
    spokes, petals = [], []
    for i in range(8):
        a = i * math.pi / 4
        x1, y1, x2, y2 = 9 * math.cos(a), 9 * math.sin(a), 38 * math.cos(a), 38 * math.sin(a)
        spokes.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                      f'stroke="currentColor" stroke-width="2.4"/>')
        b = a + math.pi / 8
        px, py = 42 * math.cos(b), 42 * math.sin(b)
        petals.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2.2" fill="currentColor"/>')
    return WHEEL.format(cls=cls, spokes="\n".join(spokes), petals="\n".join(petals))


def build_gita():
    """Return (list of Gita chapters, glossary). Each chapter: dict with num, title, ce, scenes, blocks."""
    files = [chapter_parts(BOOK6 / f) for f in FILES]
    order = sorted(STARTS.items(), key=lambda kv: kv[1])
    chapters, glossary, fn_no = [], [], 0
    seen = {}
    prev_quoted = "Krishna"
    for idx, (num, (fi, pi)) in enumerate(order):
        nxt = order[idx + 1][1] if idx + 1 < len(order) else (len(files), 0)
        paras = []
        for f in range(fi, nxt[0] + 1 if nxt[1] > 0 else nxt[0]):
            if f >= len(files):
                break
            ps = files[f][0]
            lo = pi if f == fi else 1
            hi = nxt[1] if f == nxt[0] else len(ps)
            paras += [(f, i, ps[i]) for i in range(lo, hi)]
        ce = f"6.{22 + num}"
        scenes = [sc for f in {x[0] for x in paras} for sc, ref in files[f][2] if ref == ce]
        blocks, last_sp = [], None
        for f, i, p in paras:
            sp = OVERRIDES.get((f, i)) or speaker_of(p, prev_quoted)
            if p.startswith("\"'") and sp in ("Arjuna", "Krishna"):
                prev_quoted = sp
            cards = []

            def mark(m, f=f):
                nonlocal fn_no
                label = m.group(1)
                if label not in seen:
                    fn_no += 1
                    seen[label] = fn_no
                    term, secs = split_def(files[f][1][label])
                    cards.append((fn_no, term, secs))
                    glossary.append((term, fn_no, num))
                return f'<sup class="fn">{seen[label]}</sup>'
            text = re.sub(r"\[\^([^\]]+)\]", mark, p)
            blocks.append({"speaker": sp, "show": sp != last_sp, "html": md_inline(text), "cards": cards})
            last_sp = sp
        chapters.append({"num": num, "title": TITLES[num], "ce": ce, "scenes": scenes, "blocks": blocks})
    return chapters, glossary


SEC_CLASS = {"What it means": "mean", "What they mean": "mean", "Everyday example": "ex",
             "In the story": "story", "Note": "note"}
SEC_ICON = {"mean": "◆", "ex": "☀", "story": "❖", "note": "✎"}


def card_html(no, term, secs):
    rows = []
    for lab, txt in secs:
        c = SEC_CLASS.get(lab, "note")
        rows.append(f'<div class="sec {c}"><div class="lab"><span>{SEC_ICON[c]}</span> {lab}</div>'
                    f'<div class="txt">{md_inline(txt)}</div></div>')
    return (f'<aside class="card" id="card-{no}"><div class="card-h"><span class="num">{no}</span>'
            f'<span class="term">{md_inline(term)}</span></div>{"".join(rows)}</aside>')


def gita_html(chapters, glossary, pages=None):
    pages = pages or {}
    out = []
    # opening pages
    key = "".join(
        f'<div class="key-row"><span class="swatch" style="background:{ink}"></span>'
        f'<b style="color:{ink}">{name}</b><span class="key-desc">{desc}</span></div>'
        for name, (ink, tint, desc) in SPEAKERS.items())
    out.append(f"""
<section class="front">
  <h1 class="front-h">How to read this book</h1>
  <p class="lead">The Bhagavad Gita, "the Song of the Lord", is a conversation between
  Krishna and the archer Arjuna on the battlefield of Kurukshetra, just before the great war.
  It is part of the Mahabharata, in Book 6, the Book of Bhishma. In the BORI Critical Edition
  it fills chapters 23 to 40 of that Book: 700 verses in 18 chapters.</p>
  <p>In the epic, the Gita is not told as it happens. Sanjaya, the blind king
  Dhritarashtra's charioteer, comes back from the battlefield after ten days of fighting
  with the news that Bhishma has fallen. The king asks him to tell everything, from the start,
  and so Sanjaya tells this too.</p>
  <p>This edition tells every verse, in order, in plain English. Nothing is added to what
  Krishna and Arjuna say. The explanations are kept apart, in numbered boxes,
  placed right after the passage that uses the idea for the first time.</p>
  <h2 class="front-h2">Who is speaking</h2>
  <p class="small">Each passage has a thin coloured rule down its left side. The speaker's name appears
  whenever the speaker changes.</p>
  <div class="key">{key}</div>
  <h2 class="front-h2">The explanation boxes</h2>
  <div class="card-demo">
    <aside class="card"><div class="card-h"><span class="num">7</span><span class="term">A word from the text</span></div>
    <div class="sec mean"><div class="lab"><span>◆</span> What it means</div><div class="txt">A plain definition in a sentence or two.</div></div>
    <div class="sec ex"><div class="lab"><span>☀</span> Everyday example</div><div class="txt">An example from ordinary life. It is only an example, not the text.</div></div>
    <div class="sec story"><div class="lab"><span>❖</span> In the story</div><div class="txt">A moment from the Mahabharata that shows the idea, with its verse reference in the Critical Edition.</div></div>
    </aside>
  </div>
  <p class="small">References such as "CE 6.24.13" mean Book 6, chapter 24, verse 13 of the
  Critical Edition. Gita chapter 1 is CE 6.23, and Gita chapter 18 is CE 6.40.</p>
</section>""")
    toc = "".join(
        f'<li><span class="toc-n">{c["num"]}</span><span class="toc-t">{c["title"]}</span>'
        f'<span class="toc-ce">CE {c["ce"]}</span><span class="toc-p">{pages.get(("c", c["num"]), "")}</span></li>'
        for c in chapters)
    out.append(f"""<section class="toc"><h1 class="front-h">Contents</h1><ol>{toc}</ol>
<p class="toc-extra">Explanations index <span>{pages.get("gloss", "")}</span></p>
<p class="toc-extra">The Line of the Moon: a family tree <span>{pages.get("tree", "")}</span></p></section>""")

    for c in chapters:
        scenes = "".join(f"<li>{md_inline(s)}</li>" for s in c["scenes"])
        out.append(f"""<section class="chapter">
<header class="ch-head"><div class="ch-band">{wheel("ch-wheel")}
<div class="ch-no"><span class="ch-word">Chapter</span><span class="ch-num">{c["num"]}</span></div></div>
<h1 class="ch-title">{c["title"]}</h1><div class="ch-ce">Bhagavad Gita {c["num"]} · CE {c["ce"]}</div>
<ul class="ch-scenes">{scenes}</ul></header>""")
        for b in c["blocks"]:
            ink, tint, _ = SPEAKERS[b["speaker"]]
            tag = f'<div class="tag" style="color:{ink}">{b["speaker"]}</div>' if b["show"] else ""
            out.append(f'<div class="para" style="border-left-color:{ink}">{tag}<p>{b["html"]}</p></div>')
            out += [card_html(*cd) for cd in b["cards"]]
        out.append('<div class="ch-end">' + wheel("end-wheel") + "</div></section>")

    rows = "".join(
        f'<li><span class="g-term">{md_inline(t)}</span><span class="g-dots"></span>'
        f'<span class="g-ref">card {n} · ch. {ch}</span></li>'
        for t, n, ch in sorted(glossary, key=lambda g: re.sub(r"[^a-z]", "", g[0].lower())))
    out.append(f'<section class="gloss"><h1 class="front-h">Explanations index</h1>'
               f'<p class="small">Every idea explained in this book, in alphabetical order, with the '
               f'number of its card and the Gita chapter where it first appears.</p><ul>{rows}</ul></section>')
    return "\n".join(out)


# --------------------------------------------------------------------------- the family tree

def node(name, sub="", cls="", ref=""):
    s = f'<span class="n-sub">{sub}</span>' if sub else ""
    r = f'<span class="n-ref">{ref}</span>' if ref else ""
    return f'<div class="node {cls}"><span class="n-name">{name}</span>{s}{r}</div>'


def chain(items, cls="", start=None):
    """A vertical line of generations. items: (name, wife/notes, ref)."""
    out = ['<ol class="chain">']
    for i, it in enumerate(items):
        name, sub, ref = (list(it) + ["", ""])[:3]
        gen = f'<span class="gen">{start + i}</span>' if start is not None else ""
        out.append(f"<li>{gen}{node(name, sub, cls, ref)}</li>")
    out.append("</ol>")
    return "".join(out)


MBH_PURU = [  # CE 1.90.11-46: king ═ wife
    ("Puru", "═ Kausalya", "1.90.11"), ("Janamejaya", "═ Ananta · three horse sacrifices", ""),
    ("Prachinvat", "═ a woman of the Ashmakas · \"Conqueror of the East\"", "1.90.12"),
    ("Samyati", "═ Varangi", ""), ("Ahampati", "═ Bhanumati", ""), ("Sarvabhauma", "═ Sunanda of Kekaya", ""),
    ("Jayatsena", "═ Sushuva of Vidarbha", ""), ("Arachina", "═ Maryada of Vidarbha", ""),
    ("Mahabhauma", "═ Suyajna", ""), ("Ayutanayin", "═ Bhasa", "1.90.19"), ("Akrodhana", "═ Karandu of Kalinga", ""),
    ("Devatithi", "═ Maryada of Videha", ""), ("Richa", "═ Sudeva of Anga", ""), ("Riksha", "═ Jvala, Takshaka's daughter", ""),
    ("Matinara", "═ the river Sarasvati", "1.90.25"), ("Tamsu", "═ Kalindi", ""), ("Ilina", "═ Rathantari · five sons", ""),
    ("Dushyanta", "═ Shakuntala", "1.90.30"), ("Bharata", "═ Sunanda of Kashi", "1.90.34"),
    ("Bhumanyu", "═ Jaya", ""), ("Suhotra", "═ Suvarna of the Ikshvakus", ""),
    ("Hastin", "═ Yashodhara · founded Hastinapura", "1.90.36"), ("Vikunthana", "═ Sudeva", ""),
    ("Ajamidha", "124 sons; Samvarana carries the line", "1.90.39"), ("Samvarana", "═ Tapati, the Sun's daughter", ""),
    ("Kuru", "═ Shubhangi", "1.90.41"), ("Viduratha", "═ Sampriya of Magadha", ""),
    ("Arugvat", "═ Amrita of Magadha", ""), ("Parikshit", "═ Suyasha", ""), ("Bhimasena", "═ Sukumari of Kekaya", ""),
    ("Pratipa (Paryashravas)", "═ Sunanda of the Shibis", "1.90.45"),
]
BHP_PURU = [  # Bhagavata Purana 9.20.2-9.22.11
    ("Puru", "", "9.20.2"), ("Janamejaya", "", ""), ("Prachinvat", "", ""), ("Pravira", "", ""), ("Manusyu", "", ""),
    ("Charupada", "", ""), ("Sudyu", "", ""), ("Bahugava", "", ""), ("Samyati", "", "9.20.3"), ("Ahamyati", "", ""),
    ("Raudrashva", "ten sons by the apsaras Ghritachi", "9.20.3–5"), ("Riteyu", "", ""), ("Rantinava", "", "9.20.6"),
    ("Sumati", "", ""), ("Rebhi", "", "9.20.7"), ("Dushyanta", "═ Shakuntala", "9.20.7"), ("Bharata", "", ""),
    ("Vitatha", "Bharadvaja, given to Bharata by the Maruts", "9.20.35–39"), ("Manyu", "", "9.21.1"),
    ("Brihatkshatra", "", ""), ("Hastin", "founded Hastinapura", "9.21.20"), ("Ajamidha", "", "9.21.21"),
    ("Riksha", "", "9.22.3"), ("Samvarana", "═ Tapati", ""), ("Kuru", "", "9.22.4"), ("Jahnu", "", ""),
    ("Suratha", "", "9.22.9"), ("Viduratha", "", "9.22.10"), ("Sarvabhauma", "", ""), ("Jayasena", "", ""),
    ("Radhika", "", ""), ("Ayutayu", "", ""), ("Akrodhana", "", "9.22.11"), ("Devatithi", "", ""), ("Riksha", "", ""),
    ("Dilipa", "", ""), ("Pratipa", "", "9.22.11"),
]
BHP_AFTER = [  # Bhagavata Purana 9.22.35-45
    ("Janamejaya", "brothers Shrutasena, Bhimasena, Ugrasena · the snake sacrifice", "9.22.35–37"),
    ("Shatanika", "learns the Veda from Yajnavalkya", "9.22.38"), ("Sahasranika", "", "9.22.39"),
    ("Ashvamedhaja", "", ""), ("Asimakrishna", "", ""),
    ("Nemichakra", "when the river sweeps away Hastinapura, he lives at Kaushambi", "9.22.39–40"),
    ("Chitraratha", "", "9.22.40"), ("Shuchiratha", "", ""), ("Vrishtiman", "", "9.22.41"), ("Sushena", "", ""),
    ("Sunitha", "", ""), ("Nrichakshu", "", ""), ("Sukhinala", "", ""), ("Pariplava", "", "9.22.42"), ("Sunaya", "", ""),
    ("Medhavin", "", ""), ("Nripanjaya", "", ""), ("Durva", "", ""), ("Timi", "", ""), ("Brihadratha", "", "9.22.43"),
    ("Sudasa", "implied by \"son of Sudasa\"", ""), ("Shatanika", "", ""), ("Durdamana", "", ""), ("Mahinara", "", ""),
    ("Dandapani", "", "9.22.44"), ("Nimi", "", ""),
    ("Kshemaka", "\"With King Kshemaka the line comes to its end in the Kali age\"", "9.22.45"),
]
BHP_YADU = [  # Bhagavata Purana 9.23.20-9.24.30 (the line that leads to Vasudeva)
    ("Yadu", "sons Sahasrajit, Kroshtu, Nala, Ripu", "9.23.20"), ("Kroshtu", "", "9.23.30"), ("Vrijinavan", "", ""),
    ("Svahita", "", "9.23.31"), ("Vishadgu", "", ""), ("Chitraratha", "", ""), ("Shashabindu", "", ""),
    ("Prithushravas", "", "9.23.33"), ("Dharma", "", ""), ("Ushanas", "", "9.23.34"), ("Rucaka", "", ""),
    ("Jyamagha", "", "9.23.35"), ("Vidarbha", "", "9.23.39"), ("Kratha", "", "9.24.1"), ("Kunti", "", "9.24.3"),
    ("Vrishni", "", ""), ("Nirvriti", "", ""), ("Dasharha", "", ""), ("Vyoma", "", ""), ("Jimuta", "", "9.24.4"),
    ("Vikriti", "", ""), ("Bhimaratha", "", ""), ("Navaratha", "", ""), ("Dasharatha", "", ""), ("Shakuni", "", "9.24.5"),
    ("Karambhi", "", ""), ("Devarata", "", ""), ("Devakshatra", "", ""), ("Madhu", "", ""), ("Kuruvasha", "", ""),
    ("Anu", "", ""), ("Puruhotra", "", "9.24.6"), ("Ayu", "", ""), ("Satvata", "seven sons, among them Vrishni and Andhaka", "9.24.6–7"),
    ("Vrishni", "", "9.24.12"), ("Yudhajit", "", ""), ("Anamitra", "his son Shini is Satyaki's grandfather", "9.24.12–14"),
    ("Vrishni", "", "9.24.14"), ("Chitraratha", "", "9.24.15"), ("Viduratha", "", "9.24.18"), ("Shura", "", "9.24.26"),
    ("Bhajamana", "", ""), ("Shini", "", ""), ("Bhoja", "or Svayambhoja", "9.24.26"), ("Hridika", "sons Devamidha, Shatadhanu, Kritavarma", "9.24.26–27"),
    ("Devamidha", "", ""), ("Shura", "═ Marisha · ten sons and five daughters", "9.24.27–31"),
]


def tree_html(standalone=False):
    legend = "".join(f'<span class="lg {c}">{t}</span>' for c, t in [
        ("src", "gods and first ancestors"), ("king", "kings of the main line"), ("kaurava", "Kauravas"),
        ("pandava", "Pandavas"), ("yadava", "Yadavas"), ("bhp", "only in the Bhagavata Purana")])
    head = ("<h1 class='front-h'>The Line of the Moon</h1>" if standalone else
            "<h1 class='front-h'>Appendix: The Line of the Moon</h1>")
    return f"""<section class="tree">
{head}
<p class="lead">The Pandavas and the Kauravas belong to the "line of the Moon", the royal house that
begins with Soma, the Moon, and his son Budha. This tree follows the Mahabharata itself, the BORI
Critical Edition (CE), and adds, clearly marked, what the Bhagavata Purana says where the Mahabharata
differs or stops.</p>
<div class="legend">{legend}<span class="lg wife">═ married</span></div>

<h2 class="t-h2">1. Two beginnings</h2>
<p>The Mahabharata tells the start of the line in two ways. Both are in the Critical Edition.</p>
<div class="two">
  <div class="col"><div class="col-h">The Sun's side · CE 1.90.7 and 1.70</div>
  {chain([("Daksha", "the lord of creatures"), ("Aditi", "his daughter"), ("Vivasvat", "the Sun"), ("Manu", ""),
          ("Ila", "“both his mother and his father” (1.70.16)")], "src")}</div>
  <div class="col"><div class="col-h">The Moon's side · CE 7.119.4</div>
  {chain([("Atri", "the seer"), ("Soma", "the Moon"), ("Budha", "the planet Mercury")], "src")}
  <div class="bhp-note">The Bhagavata Purana joins the two: Budha is the father and Ila the mother
  of Pururavas (9.14.14–15).</div></div>
</div>
<div class="merge">▼ ▼</div>
{chain([("Pururavas", "═ Urvashi, the apsaras · six sons", "1.70.21–22"), ("Ayus", "", "1.90.7"),
        ("Nahusha", "once ruled as Indra", "1.70.27"), ("Yayati", "═ Devayani · ═ Sharmishtha", "1.90.8")], "king")}
<div class="branch5">
  <div>{node("Yadu", "Devayani's son · the Yadavas", "yadava", "1.90.10")}</div>
  <div>{node("Turvasu", "Devayani's son", "king")}</div>
  <div>{node("Druhyu", "Sharmishtha's son", "king")}</div>
  <div>{node("Anu", "Sharmishtha's son", "king")}</div>
  <div>{node("Puru", "Sharmishtha's son, the youngest, who took his father's old age · the Pauravas", "king", "1.70.40–45")}</div>
</div>

<h2 class="t-h2">2. From Puru to Pratipa</h2>
<p>Here the two books give different lists. The Mahabharata's prose list (CE 1.90) names every
queen. The Bhagavata's list (9.20–22) takes another route, with some of the same names in other
places. Both end with Pratipa, Shantanu's father. The Mahabharata's short verse list at CE 1.89
differs again; it is not drawn here.</p>
<div class="two">
  <div class="col"><div class="col-h">Mahabharata · CE 1.90</div>{chain(MBH_PURU, "king", 1)}</div>
  <div class="col bhp"><div class="col-h">Bhagavata Purana · 9.20–22</div>{chain(BHP_PURU, "bhp", 1)}</div>
</div>

<h2 class="t-h2 pb">3. Pratipa's family: the Kurus and the Pandavas</h2>
<p class="small">From here the two books agree on the main line. References are to the Critical Edition.</p>
<div class="fam">
  <div class="gen-row">{node("Pratipa", "═ Sunanda", "king", "1.90.46")}</div>
  <div class="gen-row three">
    {node("Devapi", "went to the forest as a boy", "king")}
    {node("Shantanu", "═ Ganga · ═ Satyavati", "king", "1.90.47–51")}
    {node("Bahlika", "", "king")}
  </div>
  <div class="gen-row four">
    {node("Bhishma", "Devavrata, son of Ganga · vowed never to marry", "king", "1.90.50")}
    {node("Chitrangada", "Satyavati's son · killed young by a gandharva", "king", "1.90.53")}
    {node("Vichitravirya", "Satyavati's son ═ Ambika, Ambalika · died childless", "king", "1.90.54–55")}
    {node("Vyasa", "Satyavati's son by Parashara, before her marriage", "src", "1.90.52")}
  </div>
  <p class="mid">At Satyavati's request Vyasa fathers sons for his brother's line (1.90.56–60).</p>
  <div class="gen-row three">
    {node("Dhritarashtra", "born blind · ═ Gandhari", "kaurava", "1.90.60–61")}
    {node("Pandu", "═ Kunti · ═ Madri", "pandava", "1.90.63")}
    {node("Vidura", "", "king", "1.90.60")}
  </div>
  <div class="two">
    <div class="col kaur">
      <div class="col-h">Dhritarashtra's children</div>
      {node("A hundred sons by Gandhari", "the chief four: Duryodhana, Duhshasana, Vikarna, Chitrasena", "kaurava", "1.90.61–62")}
      {node("Duhshala", "one daughter", "kaurava", "1.107.37")}
      {node("Yuyutsu", "son by a vaishya woman who served the king", "kaurava", "1.107.35–36")}
    </div>
    <div class="col pand">
      <div class="col-h">Pandu's sons, born to his wives by the gods</div>
      {node("Yudhishthira", "Kunti's son by Dharma", "pandava", "1.90.69")}
      {node("Bhima", "Kunti's son by the Wind", "pandava")}
      {node("Arjuna", "Kunti's son by Indra", "pandava")}
      {node("Nakula · Sahadeva", "Madri's twins by the two Ashvins", "pandava", "1.90.72")}
    </div>
  </div>
  <h3 class="t-h3">The Pandavas' wives and sons · CE 1.90.82–89</h3>
  <table class="sons">
    <tr><th></th><th>by Draupadi</th><th>by another wife</th></tr>
    <tr><td class="who">Yudhishthira</td><td>Prativindhya</td><td>Yaudheya, by Devika, daughter of Govasana of the Shibis</td></tr>
    <tr><td class="who">Bhima</td><td>Sutasoma</td><td>Sarvaga, by Baladhara of Kashi · Ghatotkacha, by the rakshasi Hidimba</td></tr>
    <tr><td class="who">Arjuna</td><td>Shrutakirti</td><td>Abhimanyu, by Subhadra, Krishna's sister · Iravan, by a daughter of the naga king (6.86.6) · Babhruvahana, by Chitrangada of Manipura (1.209.24)</td></tr>
    <tr><td class="who">Nakula</td><td>Shatanika</td><td>Niramitra, by Karenumati of Chedi</td></tr>
    <tr><td class="who">Sahadeva</td><td>Shrutakarman</td><td>Suhotra, by Vijaya of Madra</td></tr>
  </table>
  <p class="small bhp-note">The Bhagavata (9.22.29–32) names some of these differently: Bhima's son by Draupadi is
  Shrutasena, Yudhishthira's other son is Devaka, and it names Iravan's mother as Ulupi.</p>
</div>

<h2 class="t-h2 pb">4. After the war</h2>
<div class="two">
  <div class="col"><div class="col-h">Mahabharata · CE 1.90.90–95</div>
  {chain([("Abhimanyu", "═ Uttara, Virata's daughter", "1.90.90"),
          ("Parikshit", "born dead, brought back to life by Krishna · ═ Madravati", "1.90.91–93"),
          ("Janamejaya", "═ Vapushtama · sons Shatanika and Shanku", "1.90.94"),
          ("Shatanika", "═ a princess of Videha", "1.90.95"),
          ("Ashvamedhadatta", "the last name in the Mahabharata's list", "1.90.95")], "pandava")}
  <div class="endnote">The Mahabharata's own list stops here.</div></div>
  <div class="col bhp"><div class="col-h">Bhagavata Purana · 9.22.33–45</div>
  {chain([("Abhimanyu", "", "9.22.33"), ("Parikshit", "saved from Ashvatthama's weapon by Krishna", "9.22.34")] + BHP_AFTER, "bhp")}
  </div>
</div>

<h2 class="t-h2 pb">5. Yadu's line: Krishna, Kunti and Satyaki</h2>
<p>The Mahabharata gives only the last steps: "In Yadu's line was Devamidha; his son was Shura; Shura's son
was Vasudeva" (CE 7.119.6–7), and Shura's daughter Pritha was given to his friend Kuntibhoja, and so is
called Kunti (CE 1.104.1–3). The Bhagavata fills in the whole line.</p>
<div class="two">
  <div class="col bhp"><div class="col-h">Bhagavata Purana · 9.23–24</div>{chain(BHP_YADU, "bhp", 1)}</div>
  <div class="col">
    <div class="col-h">Shura's children</div>
    {node("Vasudeva", "Shura's son · ═ Devaki, Rohini and others (Bhagavata 9.24.45)", "yadava", "7.119.7")}
    <div class="sub-list">
      {node("Krishna", "Devaki's son · her eighth, says the Bhagavata (9.24.53–55)", "yadava")}
      {node("Balarama", "Krishna's elder brother, Rohini's son (Bhagavata 9.24.46)", "yadava")}
      {node("Subhadra", "Krishna's sister · ═ Arjuna · mother of Abhimanyu", "yadava", "1.90.85")}
    </div>
    {node("Pritha (Kunti)", "Shura's daughter, given to Kuntibhoja · ═ Pandu · before her marriage, mother of Karna by the Sun", "pandava", "1.104.1–3")}
    <div class="col-h" style="margin-top:14px">Satyaki's line</div>
    {chain([("Shini", "", "7.119.8"), ("Satyaka", "his father, as the name Satyaki says", "1.211.11"), ("Satyaki (Yuyudhana)", "“Shini's grandson”", "6.55.75")], "yadava")}
    <div class="col-h" style="margin-top:14px">Kritavarma</div>
    {node("Kritavarma", "“Hardikya”, son of Hridika · in the Bhagavata, Devamidha's brother (9.24.27)", "yadava", "1.211.11")}
  </div>
</div>

<h2 class="t-h2 pb">6. And the families of today?</h2>
<div class="today">
<p>The Mahabharata's list ends with <b>Ashvamedhadatta</b>, Janamejaya's grandson (CE 1.90.95). The
Bhagavata Purana carries the line some twenty-five reigns further, to <b>Kshemaka</b>, and says in so many
words that the line of the Moon ends with him in the Kali age (9.22.45).</p>
<p>Neither text names any later king of this house, and neither links it to any family alive today.
Many Indian families and clans do keep a tradition of descent from the line of the Moon, the
<i>Chandravanshi</i> or <i>Somavanshi</i>. For example, the Jadeja and Bhati Rajputs trace themselves to
Yadu and Krishna, and the Tomars (Tanwars) to the Pandavas. These are family traditions, and they are
honoured as such. But no text or record joins them, name by name, to Kshemaka or to Ashvamedhadatta. So
no one can honestly draw the last branch of this tree down to the present day, and this book does not try.</p>
</div>
</section>"""


# --------------------------------------------------------------------------- styling and output

EXTRA_FONTS = {"cinzel": ["cinzel-latin-600-normal.woff2", "cinzel-latin-700-normal.woff2"],
               "source-sans-3": ["source-sans-3-latin-400-normal.woff2", "source-sans-3-latin-600-normal.woff2",
                                 "source-sans-3-latin-700-normal.woff2", "source-sans-3-latin-400-italic.woff2"]}


def ensure_extra_fonts() -> dict:
    have = {}
    for pkg, files in EXTRA_FONTS.items():
        if not all((FONTS / f).exists() for f in files):
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    subprocess.run(["npm", "pack", "-q", f"@fontsource/{pkg}"], cwd=tmp, check=True,
                                   capture_output=True)
                    subprocess.run(["tar", "xzf", glob.glob(os.path.join(tmp, "*.tgz"))[0]], cwd=tmp, check=True)
                    for f in files:
                        src = Path(tmp) / "package" / "files" / f
                        if src.exists():
                            (FONTS / f).write_bytes(src.read_bytes())
            except Exception as e:  # noqa: BLE001
                print(f"note: could not fetch {pkg} ({e})", file=sys.stderr)
        have[pkg] = [FONTS / f for f in files if (FONTS / f).exists()]
    return have


def font_faces(garamond, extra) -> str:
    out = []
    for f in garamond:
        m = re.search(r"(\d{3})-(normal|italic)", f.name)
        out.append(f"@font-face{{font-family:'EB Garamond';src:url('{f.as_uri()}');font-weight:{m.group(1)};"
                   f"font-style:{m.group(2)};}}")
    fam = {"cinzel": "Cinzel", "source-sans-3": "Source Sans 3"}
    for pkg, files in extra.items():
        for f in files:
            m = re.search(r"(\d{3})-(normal|italic)", f.name)
            out.append(f"@font-face{{font-family:'{fam[pkg]}';src:url('{f.as_uri()}');font-weight:{m.group(1)};"
                       f"font-style:{m.group(2)};}}")
    return "\n".join(out)


CSS = r"""
@page { size: A4; margin: 20mm 20mm 22mm 20mm; }
:root { --accent:#8a6d3b; --ink:#2a2622; --head:#27324f; --rule:#ddd6c8; --muted:#7a7166; --paper:#ffffff; }
html { background: var(--paper); }
body { font-family:'EB Garamond', Georgia, serif; font-size:12.2pt; line-height:1.52; color:var(--ink); margin:0; }
.sans, .tag, .lab, .card-h, .ch-ce, .ch-scenes, .key, .small, .legend, .node, .col-h, .toc, .gloss, table.sons { font-family:'Source Sans 3', Arial, sans-serif; }
h1, h2, h3 { font-weight:600; }
section { break-before: page; }
.front-h { font-family:'Cinzel', serif; font-size:21pt; font-weight:600; color:var(--head); letter-spacing:.04em; margin:0 0 12px;
  border-bottom:1px solid var(--accent); padding-bottom:6px; }
.front-h2, .t-h2 { font-family:'Cinzel', serif; font-size:13.5pt; font-weight:600; color:var(--head); margin:22px 0 6px; letter-spacing:.03em; }
.t-h3 { font-family:'Cinzel', serif; font-size:11.5pt; color:var(--head); margin:16px 0 6px; }
.lead { font-size:13pt; }
.small { font-size:9.6pt; color:var(--muted); }
.key { margin:10px 0; } .key-row { display:flex; align-items:center; gap:10px; margin:6px 0; font-size:10.5pt; }
.swatch { width:3px; height:16px; display:inline-block; flex:none; }
.key-row b { width:105px; flex:none; font-weight:600; } .key-desc { color:#555; }
.card-demo { margin:8px 0 10px; }

/* contents */
.toc ol { list-style:none; padding:0; margin:14px 0; }
.toc li { display:flex; align-items:baseline; gap:12px; padding:6px 0; border-bottom:1px solid #eeeae2; font-size:11.5pt; }
.toc-n { font-family:'Cinzel', serif; color:var(--accent); width:22px; text-align:right; font-size:11pt; flex:none; }
.toc-t { flex:1; color:var(--ink); } .toc-ce { color:var(--muted); font-size:9.5pt; width:62px; }
.toc-p { width:28px; text-align:right; color:var(--ink); }
.toc-extra { display:flex; justify-content:space-between; margin:10px 0 0; color:var(--head); }
.toc-extra span { color:var(--ink); }

/* chapter openers */
.ch-head { margin-bottom:20px; text-align:center; padding-top:6mm; }
.ch-band { position:relative; height:auto; color:var(--accent); }
.ch-wheel { display:none; }
.ch-no { display:flex; flex-direction:column; align-items:center; }
.ch-word { font-family:'Cinzel', serif; letter-spacing:.3em; font-size:9.5pt; color:var(--muted); }
.ch-num { font-family:'Cinzel', serif; font-size:40pt; line-height:1.1; color:var(--accent); }
.ch-title { font-family:'Cinzel', serif; font-size:22pt; font-weight:600; color:var(--head); margin:4px 0 2px; }
.ch-ce { font-size:9pt; color:var(--muted); letter-spacing:.12em; text-transform:uppercase; }
.ch-scenes { list-style:none; margin:14px auto 0; padding:8px 0; border-top:1px solid var(--rule); border-bottom:1px solid var(--rule);
  font-size:9.4pt; color:#5e574e; max-width:80%; }
.ch-scenes li { margin:1px 0; display:inline; } .ch-scenes li + li::before { content:" · "; color:var(--accent); }
.ch-end { text-align:center; margin:18px 0 0; } .end-wheel { width:22px; height:22px; color:#c9bca3; }

/* speech */
.para { position:relative; border-left:2px solid var(--ink); padding:1px 0 1px 12px; margin:0 0 9px; }
.para p { margin:0; text-align:justify; hyphens:auto; }
.tag { display:block; font-size:7.8pt; font-weight:600; letter-spacing:.16em; text-transform:uppercase; margin:6px 0 2px; }
sup.fn { font-family:'Source Sans 3', sans-serif; font-size:7pt; font-weight:600; color:var(--accent); margin-left:1px; vertical-align:4px; }

/* explanation cards */
.card { break-inside:avoid; margin:8px 0 14px 14px; border:1px solid var(--rule); border-radius:3px; background:#fbfaf7;
  font-size:10pt; line-height:1.42; }
.card-h { display:flex; align-items:baseline; gap:8px; padding:6px 12px 3px; border-bottom:1px solid #ece7dc; }
.card-h .num { color:var(--accent); font-weight:600; font-size:9pt; flex:none; }
.card-h .num::after { content:"."; }
.card-h .term { font-family:'EB Garamond', serif; font-weight:600; font-size:12.5pt; color:var(--head); }
.sec { padding:4px 12px 5px; }
.sec .lab { font-size:7.5pt; font-weight:600; letter-spacing:.12em; text-transform:uppercase; margin-bottom:0; }
.sec .lab span { display:none; }
.sec .txt { font-family:'EB Garamond', serif; font-size:11pt; }
.sec.mean .lab { color:#4a5a78; } .sec.ex .lab { color:#8a6d3b; } .sec.story .lab { color:#55705c; } .sec.note .lab { color:#6b5e7d; }

/* glossary */
.gloss ul { list-style:none; padding:0; columns:2; column-gap:26px; font-size:9.6pt; }
.gloss li { display:flex; gap:4px; break-inside:avoid; padding:2px 0; }
.g-term { font-family:'EB Garamond', serif; font-size:11pt; } .g-dots { flex:1; border-bottom:1px dotted #ccc4b5; margin:0 3px 5px; }
.g-ref { color:var(--muted); white-space:nowrap; }

/* family tree */
.tree p { margin:6px 0; }
.legend { display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 4px; font-size:8.8pt; }
.lg { padding:1px 8px; border-radius:2px; border:1px solid; border-left-width:3px; background:#fff; color:#444; }
.lg.src { border-color:#c9b27d; } .lg.king { border-color:#8795b3; } .lg.kaurava { border-color:#b58c86; }
.lg.pandava { border-color:#8fa996; } .lg.yadava { border-color:#9d91b3; } .lg.bhp { border-color:#aaa; border-style:dashed; }
.lg.wife { border-color:#ddd; color:#666; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin:8px 0; }
.col-h { font-weight:600; font-size:9pt; color:var(--head); letter-spacing:.08em; text-transform:uppercase;
  border-bottom:1px solid var(--rule); padding-bottom:3px; margin-bottom:6px; }
ol.chain { list-style:none; padding:0 0 0 18px; margin:0; position:relative; }
ol.chain::before { content:""; position:absolute; left:8px; top:10px; bottom:10px; border-left:1px solid #cfc7b8; }
ol.chain li { position:relative; margin:0 0 3px; break-inside:avoid; }
ol.chain li::before { content:""; position:absolute; left:-10px; top:11px; width:10px; border-top:1px solid #cfc7b8; }
.gen { position:absolute; left:-44px; top:4px; width:22px; text-align:right; font-family:'Source Sans 3',sans-serif;
  font-size:7.5pt; color:#b0a795; }
ol.chain:has(.gen) { padding-left:40px; } ol.chain:has(.gen)::before { left:30px; } ol.chain:has(.gen) li::before { left:-10px; }
.node { display:inline-flex; flex-wrap:wrap; align-items:baseline; gap:4px 7px; padding:2px 9px; border-radius:2px;
  border:1px solid #ddd6c8; border-left:3px solid; background:#fff; font-size:9pt; line-height:1.25; max-width:100%; box-sizing:border-box; }
.n-name { font-family:'EB Garamond', serif; font-weight:600; font-size:11.2pt; color:var(--ink); }
.n-sub { color:#6a6258; font-size:8.4pt; margin-left:3px; } .n-ref { color:#a39a88; font-size:7.6pt; }
.node.src { border-left-color:#c9b27d; } .node.king { border-left-color:#8795b3; }
.node.kaurava { border-left-color:#b58c86; } .node.pandava { border-left-color:#8fa996; }
.node.yadava { border-left-color:#9d91b3; }
.node.bhp { border:1px dashed #b8b8b8; border-left:3px dashed #aaa; background:#fcfcfc; }
.col.bhp .col-h { color:#777; }
.bhp-note { font-size:9pt; color:#666; border:1px dashed #c4c4c4; border-radius:2px; padding:5px 9px; margin:8px 0; }
.merge { text-align:center; color:#bfb49f; letter-spacing:40px; margin:4px 0; }
.branch5 { display:grid; grid-template-columns:repeat(5, 1fr); gap:6px; margin:10px 0 4px; border-top:1px solid #cfc7b8; padding-top:8px; }
.branch5 .node { display:flex; flex-direction:column; gap:1px; height:100%; }
.fam .gen-row { display:flex; justify-content:center; gap:10px; margin:8px 0; position:relative; }
.fam .gen-row .node { flex:1; flex-direction:column; align-items:flex-start; gap:1px; }
.fam .gen-row:first-child .node { flex:0 0 45%; }
.fam .gen-row + .gen-row { border-top:1px solid #cfc7b8; padding-top:8px; }
.fam .col .node { display:flex; flex-direction:column; gap:1px; margin:0 0 5px; }
.mid { text-align:center; font-style:italic; color:#6a6258; font-size:10.5pt; }
table.sons { width:100%; border-collapse:collapse; font-size:9pt; }
table.sons th { text-align:left; color:var(--head); padding:4px 6px; font-size:8pt; font-weight:600; letter-spacing:.08em;
  text-transform:uppercase; border-bottom:1px solid var(--rule); }
table.sons td { border-bottom:1px solid #eeeae2; padding:4px 6px; vertical-align:top; }
table.sons td.who { font-family:'EB Garamond', serif; font-weight:600; font-size:11pt; white-space:nowrap; }
.sub-list { margin:4px 0 8px 16px; border-left:1px solid #cfc7b8; padding-left:8px; }
.sub-list .node { display:flex; margin:0 0 4px; }
.col .node { display:flex; flex-direction:column; gap:1px; margin:0 0 5px; }
ol.chain .node { display:inline-flex; flex-direction:row; }
.endnote { font-size:9pt; color:var(--muted); font-style:italic; margin:6px 0 0 18px; }
.today { border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); padding:6px 4px; }
.pb { break-before: page; }

/* cover */
.cover { break-before:auto; height:297mm; width:210mm; position:relative; overflow:hidden; margin:0;
  background:#f7f4ee; color:var(--head); text-align:center; }
.cover .big-wheel { position:absolute; left:50%; top:30%; width:70mm; height:70mm; transform:translate(-50%,-50%); color:#b59a63; }
.cover .ring { display:none; }
.cover .t1 { position:absolute; top:52%; width:100%; font-family:'Cinzel', serif; font-size:34pt; font-weight:600; color:var(--head); letter-spacing:.05em; }
.cover .t2 { position:absolute; top:60%; width:100%; font-family:'Cinzel', serif; font-size:13pt; letter-spacing:.35em; color:var(--accent); }
.cover .t3 { position:absolute; top:66%; width:100%; font-family:'EB Garamond', serif; font-size:14pt; color:#5e574e; font-style:italic; }
.cover .t4 { position:absolute; bottom:24mm; width:100%; font-family:'Source Sans 3', sans-serif; font-size:8.5pt; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); }
.cover .band { position:absolute; bottom:16mm; left:35%; width:30%; height:0; border-top:1px solid #b59a63; }
"""


def page_doc(body: str, fonts: str, cover=False) -> str:
    page_css = "@page { size:A4; margin:0; }" if cover else ""
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><style>{fonts}\n{CSS}\n{page_css}</style>"
            f"</head><body>{body}</body></html>")


def cover_html(title, sub, line, foot):
    return (f'<div class="cover"><div class="ring"></div>{wheel("big-wheel")}'
            f'<div class="t1">{title}</div><div class="t2">{sub}</div><div class="t3">{line}</div>'
            f'<div class="t4">{foot}</div><div class="band"></div></div>')


FOOTER = ("<div style=\"width:100%;font-family:Georgia,serif;font-size:8pt;color:#9a8763;display:flex;"
          "justify-content:space-between;padding:0 19mm;\"><span>{left}</span>"
          "<span>— <span class='pageNumber'></span> —</span><span>{right}</span></div>")


def render(pw, html_text: str, out: Path, footer: tuple[str, str] | None):
    exe = chromium_path()
    browser = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
    page = browser.new_page()
    page.set_default_timeout(0)
    src = out.with_suffix(".html")
    src.write_text(html_text, encoding="utf-8")
    page.goto(src.as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    opts = dict(path=str(out), format="A4", print_background=True, prefer_css_page_size=True, outline=True)
    if footer:
        opts.update(display_header_footer=True, header_template="<span></span>",
                    footer_template=FOOTER.format(left=footer[0], right=footer[1]))
    page.pdf(**opts)
    browser.close()
    src.unlink(missing_ok=True)


def find_pages(pdf: Path, wanted: dict) -> dict:
    """wanted: key -> text on the page; returns key -> the page number printed in its footer."""
    r = PdfReader(str(pdf))
    texts = [re.sub(r"\s+", "", p.extract_text() or "").lower() for p in r.pages]
    found = {}
    for key, needle in wanted.items():
        needle = re.sub(r"\s+", "", needle).lower()
        for i, t in enumerate(texts):
            if needle in t and i + 1 not in found.values():
                found[key] = i + 1  # the number printed in the footer
                break
    return found


def merge(parts: list[Path], out: Path):
    w = PdfWriter()
    for p in parts:
        w.append(str(p))
    w.write(str(out))
    for p in parts:
        p.unlink(missing_ok=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    faces = font_faces(ensure_fonts(), ensure_extra_fonts())
    chapters, glossary = build_gita()
    date = datetime.date.today().strftime("%-d %B %Y")
    with sync_playwright() as pw:
        # the Gita, with its contents page numbers filled in on the second pass
        cov, body = OUT / "cover.pdf", OUT / "body.pdf"
        render(pw, page_doc(cover_html("The Bhagavad Gita", "TOLD SIMPLY", "with plain explanations of every idea",
                                       f"From the Mahabharata · Book of Bhishma · BORI Critical Edition 6.23–40 · {date}"),
                            faces, cover=True), cov, None)
        wanted = {("c", c["num"]): f"Bhagavad Gita {c['num']} · CE {c['ce']}" for c in chapters}
        wanted.update({"gloss": "Explanations index Every idea", "tree": "Appendix: The Line of the Moon"})
        pages = {}
        for _ in range(2):
            doc = gita_html(chapters, glossary, pages) + tree_html()
            render(pw, page_doc(doc, faces), body, ("The Bhagavad Gita · told simply", "Mahabharata, Book 6"))
            pages = find_pages(body, wanted)
        merge([cov, body], OUT / "bhagavad-gita-told-simply.pdf")

        cov2, body2 = OUT / "cover2.pdf", OUT / "body2.pdf"
        render(pw, page_doc(cover_html("The Line of the Moon", "A FAMILY TREE",
                                       "from the Moon to the Pandavas and beyond, as the texts give it",
                                       f"Mahabharata (BORI Critical Edition) · Bhagavata Purana, Book 9 · {date}"),
                            faces, cover=True), cov2, None)
        render(pw, page_doc(tree_html(standalone=True), faces), body2, ("The Line of the Moon", "Family tree"))
        merge([cov2, body2], OUT / "the-line-of-the-moon.pdf")
    for f in ("bhagavad-gita-told-simply.pdf", "the-line-of-the-moon.pdf"):
        p = OUT / f
        print(f"wrote {p.relative_to(ROOT)} ({len(PdfReader(str(p)).pages)} pages)")
    missing = [k for k in wanted if k not in pages]
    if missing:
        print(f"note: page numbers not found for {missing}", file=sys.stderr)


if __name__ == "__main__":
    main()
