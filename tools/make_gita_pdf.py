#!/usr/bin/env python3
"""Typeset the Bhagavad Gita (Book 6, chapters 7-13) as a plain black-and-white
study edition, and the family line of the Moon as simple lists and tables.

    python3 tools/make_gita_pdf.py          # writes build/gita/*.pdf

Outputs:
  build/gita/bhagavad-gita-told-simply.pdf   the Gita in 18 chapters, the speaker
      named at each change, every explanation boxed right after the passage that
      uses it, an index, and the family tree as an appendix;
  build/gita/the-line-of-the-moon.pdf        the family tree on its own.

The Gita text and the explanations come straight from the novel's chapter files;
nothing is rewritten here. The family tree uses the Critical Edition (1.70,
1.90, 7.119) for the main line and marks clearly what comes from the Bhagavata
Purana (Book 9) instead. Needs the same packages as make_pdf.py.
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_pdf import BUILD, ROOT, chromium_path, ensure_fonts  # noqa: E402

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

SPEAKERS = {
    "Dhritarashtra": "the blind king, who asks what happened",
    "Sanjaya": "the king's charioteer, who tells him all of it",
    "Duryodhana": "the king's eldest son, speaking to his teacher Drona",
    "Arjuna": "the Pandava archer, who does not want to fight; also called Partha and Dhananjaya",
    "Krishna": "Arjuna's charioteer and teacher; also called Vasudeva, Keshava and Madhava",
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

def card_html(no, term, secs):
    rows = "".join(f"<p><b>{lab}.</b> {md_inline(txt)}</p>" for lab, txt in secs)
    return f'<aside class="box"><p class="box-h"><b>{no}. {md_inline(term)}</b></p>{rows}</aside>'


def gita_html(chapters, glossary, pages=None):
    pages = pages or {}
    out = []
    cast = "".join(f"<tr><th>{name}</th><td>{desc}</td></tr>" for name, desc in SPEAKERS.items())
    out.append(f"""
<section class="front">
  <h1>How to read this book</h1>
  <p>The Bhagavad Gita, "the Song of the Lord", is a conversation between Krishna and the
  archer Arjuna on the battlefield of Kurukshetra, just before the great war. It is part of the
  Mahabharata, in Book 6, the Book of Bhishma. In the BORI Critical Edition it fills chapters 23 to
  40 of that Book: 700 verses in 18 chapters.</p>
  <p>In the epic, the Gita is not told as it happens. Sanjaya, the blind king Dhritarashtra's
  charioteer, comes back from the battlefield after ten days of fighting with the news that
  Bhishma has fallen. The king asks him to tell everything from the start, and so Sanjaya tells
  this too.</p>
  <p>This edition tells every verse, in order, in plain English. Nothing is added to what Krishna
  and Arjuna say.</p>
  <h2>Who is speaking</h2>
  <p>Whenever the speaker changes, the new speaker's name is printed in capitals above the
  passage.</p>
  <table class="cast">{cast}</table>
  <h2>The explanation boxes</h2>
  <p>A small number in the text, like this<sup class="fn">7</sup>, means an idea is explained in
  the box with that number. The box comes right after the passage. Each box has up to three parts:</p>
  <aside class="box"><p class="box-h"><b>7. A word from the text</b></p>
  <p><b>What it means.</b> A plain definition in a sentence or two.</p>
  <p><b>Everyday example.</b> An example from ordinary life. It is only an example, not the text.</p>
  <p><b>In the story.</b> A moment from the Mahabharata that shows the idea, with its verse
  reference.</p></aside>
  <p class="small">A reference such as "CE 6.24.13" means Book 6, chapter 24, verse 13 of the
  Critical Edition.</p>
</section>""")
    toc = "".join(
        f'<tr><td class="n">{c["num"]}</td><td>{c["title"]}</td><td class="ce">CE {c["ce"]}</td>'
        f'<td class="p">{pages.get(("c", c["num"]), "")}</td></tr>' for c in chapters)
    out.append(f"""<section class="toc"><h1>Contents</h1><table>{toc}
<tr class="gap"><td></td><td>Explanations index</td><td></td><td class="p">{pages.get("gloss", "")}</td></tr>
<tr><td></td><td>Appendix: The Line of the Moon (family tree)</td><td></td><td class="p">{pages.get("tree", "")}</td></tr>
</table></section>""")

    for c in chapters:
        scenes = "".join(f"<li>{md_inline(s)}</li>" for s in c["scenes"])
        out.append(f"""<section class="chapter">
<p class="ch-no">Chapter {c["num"]}</p><h1 class="ch-title">{c["title"]}</h1>
<p class="ch-ce">Bhagavad Gita {c["num"]} · CE {c["ce"]}</p>
<div class="ch-scenes"><b>In this chapter</b><ul>{scenes}</ul></div>""")
        for b in c["blocks"]:
            if b["show"]:
                out.append(f'<p class="who">{b["speaker"]}</p>')
            out.append(f'<p class="text">{b["html"]}</p>')
            out += [card_html(*cd) for cd in b["cards"]]
        out.append("</section>")

    rows = "".join(
        f'<li><span>{md_inline(t)}</span><span class="dots"></span><span>{n}</span></li>'
        for t, n, ch in sorted(glossary, key=lambda g: re.sub(r"[^a-z]", "", g[0].lower())))
    out.append(f'<section class="gloss"><h1>Explanations index</h1>'
               f'<p class="small">Every idea explained in this book, in alphabetical order, with the '
               f'number of its box.</p><ul>{rows}</ul></section>')
    return "\n".join(out)



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
        scenes = [sc for f in sorted({x[0] for x in paras}) for sc, ref in files[f][2] if ref == ce]
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


# --------------------------------------------------------------------------- the family tree

MBH_PURU = [  # CE 1.90.11-46: (king, wife, note, verse)
    ("Puru", "Kausalya", "", "1.90.11"), ("Janamejaya", "Ananta", "performed three horse sacrifices", "1.90.11–12"),
    ("Prachinvat", "a woman of the Ashmakas", "conquered the East", "1.90.12–13"),
    ("Samyati", "Varangi", "", "1.90.14"), ("Ahampati", "Bhanumati", "", "1.90.15"),
    ("Sarvabhauma", "Sunanda of Kekaya", "", "1.90.16"), ("Jayatsena", "Sushuva of Vidarbha", "", "1.90.17"),
    ("Arachina", "Maryada of Vidarbha", "", "1.90.18"), ("Mahabhauma", "Suyajna", "", "1.90.19"),
    ("Ayutanayin", "Bhasa", "", "1.90.20"), ("Akrodhana", "Karandu of Kalinga", "", "1.90.21"),
    ("Devatithi", "Maryada of Videha", "", "1.90.22"), ("Richa", "Sudeva of Anga", "", "1.90.23"),
    ("Riksha", "Jvala, Takshaka's daughter", "", "1.90.24"), ("Matinara", "the river Sarasvati", "", "1.90.25–26"),
    ("Tamsu", "Kalindi", "", "1.90.28"), ("Ilina", "Rathantari", "had five sons", "1.90.29"),
    ("Dushyanta", "Shakuntala", "", "1.90.30"), ("Bharata", "Sunanda of Kashi", "the Bharatas are named after him", "1.90.34; 1.69.49"),
    ("Bhumanyu", "Jaya", "", "1.90.35"), ("Suhotra", "Suvarna of the Ikshvakus", "", "1.90.36"),
    ("Hastin", "Yashodhara", "founded Hastinapura", "1.90.36–37"), ("Vikunthana", "Sudeva", "", "1.90.38"),
    ("Ajamidha", "five wives", "had 124 sons", "1.90.39"), ("Samvarana", "Tapati, the Sun's daughter", "", "1.90.40"),
    ("Kuru", "Shubhangi", "", "1.90.41"), ("Viduratha", "Sampriya of Magadha", "", "1.90.42"),
    ("Arugvat", "Amrita of Magadha", "", "1.90.43"), ("Parikshit", "Suyasha", "", "1.90.44"),
    ("Bhimasena", "Sukumari of Kekaya", "", "1.90.45"), ("Pratipa", "Sunanda of the Shibis", "also called Paryashravas", "1.90.45–46"),
]
BHP_PURU = ["Puru", "Janamejaya", "Prachinvat", "Pravira", "Manusyu", "Charupada", "Sudyu", "Bahugava", "Samyati",
            "Ahamyati", "Raudrashva", "Riteyu", "Rantinava", "Sumati", "Rebhi", "Dushyanta", "Bharata",
            "Vitatha (Bharadvaja, given to Bharata by the Maruts)", "Manyu", "Brihatkshatra", "Hastin", "Ajamidha",
            "Riksha", "Samvarana", "Kuru", "Jahnu", "Suratha", "Viduratha", "Sarvabhauma", "Jayasena", "Radhika",
            "Ayutayu", "Akrodhana", "Devatithi", "Riksha", "Dilipa", "Pratipa"]
BHP_AFTER = ["Janamejaya", "Shatanika", "Sahasranika", "Ashvamedhaja", "Asimakrishna",
             "Nemichakra (when the river sweeps Hastinapura away, he lives at Kaushambi)", "Chitraratha",
             "Shuchiratha", "Vrishtiman", "Sushena", "Sunitha", "Nrichakshu", "Sukhinala", "Pariplava", "Sunaya",
             "Medhavin", "Nripanjaya", "Durva", "Timi", "Brihadratha", "Sudasa", "Shatanika", "Durdamana",
             "Mahinara", "Dandapani", "Nimi", "Kshemaka"]
BHP_YADU = ["Yadu", "Kroshtu", "Vrijinavan", "Svahita", "Vishadgu", "Chitraratha", "Shashabindu", "Prithushravas",
            "Dharma", "Ushanas", "Rucaka", "Jyamagha", "Vidarbha", "Kratha", "Kunti", "Vrishni", "Nirvriti",
            "Dasharha", "Vyoma", "Jimuta", "Vikriti", "Bhimaratha", "Navaratha", "Dasharatha", "Shakuni",
            "Karambhi", "Devarata", "Devakshatra", "Madhu", "Kuruvasha", "Anu", "Puruhotra", "Ayu", "Satvata",
            "Vrishni", "Yudhajit", "Anamitra", "Vrishni", "Chitraratha", "Viduratha", "Shura", "Bhajamana", "Shini",
            "Bhoja", "Hridika", "Devamidha", "Shura", "Vasudeva"]


def arrows(names):
    return " → ".join(names)


def tree_html(standalone=False):
    head = "The Line of the Moon" if standalone else "Appendix: The Line of the Moon"
    rows = "".join(f'<tr><td class="n">{i}</td><td><b>{k}</b></td><td>{w}</td><td>{n}</td><td class="ce">{v}</td></tr>'
                   for i, (k, w, n, v) in enumerate(MBH_PURU, 1))
    return f"""<section class="tree">
<h1>{head}</h1>
<p>The Pandavas and the Kauravas belong to one royal family, called the "line of the Moon".
These pages follow that family from its start to the end of the Mahabharata, using the
Mahabharata's own lists (BORI Critical Edition, "CE"). Where the <i>Bhagavata Purana</i>, a later
text, gives more or gives something different, it is shown in a separate box marked
<b>Bhagavata Purana</b>. Those boxes are not from the Mahabharata.</p>
<p class="small">How to read the lists: "A → B" means B was A's child; "m." means "married".</p>

<h2>1. Where the family begins</h2>
<p>The Mahabharata tells the start in two ways.</p>
<p class="line">Daksha → Aditi → Vivasvat (the Sun) → Manu → Ila → <b>Pururavas</b> <span class="ce">CE 1.90.7</span></p>
<p class="line">Atri → Soma (the Moon) → Budha → <b>Pururavas</b> <span class="ce">CE 7.119.4</span></p>
<p>In the first version, Ila was "both his mother and his father" (CE 1.70.16).</p>
<div class="bhp"><b>Bhagavata Purana.</b> It joins the two: Budha, son of the Moon, is Pururavas's
father, and Ila is his mother (9.14.14–15).</div>
<p class="line"><b>Pururavas</b> (m. Urvashi) → Ayus → Nahusha → <b>Yayati</b> <span class="ce">CE 1.90.7</span></p>
<p>Yayati had two wives and five sons (CE 1.90.8–10):</p>
<table class="plain">
<tr><th>Mother</th><th>Sons</th></tr>
<tr><td>Devayani</td><td><b>Yadu</b> (from him come the Yadavas, Krishna's people) and Turvasu</td></tr>
<tr><td>Sharmishtha</td><td>Druhyu, Anu and <b>Puru</b> (from him come the Pauravas: the Kurus and the Pandavas)</td></tr>
</table>

<h2 class="pb">2. From Puru to Pratipa</h2>
<p>Each king below is the son of the king above him. The Mahabharata names each king's wife
(CE 1.90.11–46).</p>
<table class="plain kings"><tr><th></th><th>King</th><th>Wife</th><th>Note</th><th>CE</th></tr>{rows}</table>
<div class="bhp"><b>Bhagavata Purana (9.20–22).</b> It gives a different list for these
generations: {arrows(BHP_PURU)}. The Mahabharata has a third, shorter list in verse at
CE 1.89, which also differs.</div>

<h2 class="pb">3. Shantanu's family: the Kurus and the Pandavas</h2>
<ul class="ft">
<li><b>Pratipa</b> m. Sunanda <span class="ce">CE 1.90.46</span>
  <ul>
  <li><b>Devapi</b>, who went to the forest as a boy</li>
  <li><b>Shantanu</b> <span class="ce">1.90.47–53</span>
    <ul>
    <li>m. Ganga: <b>Bhishma</b></li>
    <li>m. Satyavati: <b>Chitrangada</b> (killed young by a gandharva) and <b>Vichitravirya</b>
      (m. Ambika and Ambalika; died without children)</li>
    </ul></li>
  <li><b>Bahlika</b></li>
  </ul></li>
</ul>
<p>Before her marriage, Satyavati had a son by the seer Parashara: <b>Vyasa</b> (CE 1.90.52).
When Vichitravirya died childless, she asked Vyasa to father sons for his brother's line
(CE 1.90.56–60). They were:</p>
<ul class="ft">
<li><b>Dhritarashtra</b>, born blind, m. Gandhari
  <ul><li><b>a hundred sons</b>, the eldest Duryodhana, then Duhshasana, Vikarna, Chitrasena and the rest <span class="ce">1.90.61–62</span></li>
  <li><b>Duhshala</b>, their one sister <span class="ce">1.107.37</span></li>
  <li><b>Yuyutsu</b>, his son by a vaishya woman <span class="ce">1.107.35–36</span></li></ul></li>
<li><b>Pandu</b>, m. Kunti and Madri. Under a curse, he asked his wives to have sons by the gods. <span class="ce">1.90.63–72</span>
  <ul><li>Kunti's sons: <b>Yudhishthira</b> (by Dharma), <b>Bhima</b> (by the Wind), <b>Arjuna</b> (by Indra)</li>
  <li>Madri's sons: <b>Nakula</b> and <b>Sahadeva</b>, twins (by the two Ashvins)</li></ul></li>
<li><b>Vidura</b></li>
</ul>
<p>Before her marriage Kunti also had a son by the Sun: <b>Karna</b>.</p>

<h3>The Pandavas' wives and sons (CE 1.90.82–88)</h3>
<table class="plain">
<tr><th></th><th>Son by Draupadi</th><th>Other wives and sons</th></tr>
<tr><td><b>Yudhishthira</b></td><td>Prativindhya</td><td>m. Devika: Yaudheya</td></tr>
<tr><td><b>Bhima</b></td><td>Sutasoma</td><td>m. Baladhara of Kashi: Sarvaga. By the rakshasi Hidimba: Ghatotkacha</td></tr>
<tr><td><b>Arjuna</b></td><td>Shrutakirti</td><td>m. Subhadra, Krishna's sister: Abhimanyu. By a daughter of the naga king: Iravan (6.86.6). By Chitrangada of Manipura: Babhruvahana (1.209.24)</td></tr>
<tr><td><b>Nakula</b></td><td>Shatanika</td><td>m. Karenumati of Chedi: Niramitra</td></tr>
<tr><td><b>Sahadeva</b></td><td>Shrutakarman</td><td>m. Vijaya of Madra: Suhotra</td></tr>
</table>
<div class="bhp"><b>Bhagavata Purana (9.22.29–32).</b> Some names differ: Bhima's son by Draupadi
is Shrutasena, Yudhishthira's other son is Devaka, and Iravan's mother is named as Ulupi.</div>

<h2 class="pb">4. After the war</h2>
<p class="line">Arjuna m. Subhadra → <b>Abhimanyu</b> m. Uttara → <b>Parikshit</b> m. Madravati →
<b>Janamejaya</b> m. Vapushtama → <b>Shatanika</b> (and his brother Shanku) m. a princess of Videha →
<b>Ashvamedhadatta</b> <span class="ce">CE 1.90.90–95</span></p>
<p>Parikshit was born dead, and Krishna brought him back to life (CE 1.90.90–92).
<b>Ashvamedhadatta is the last name in the Mahabharata's list.</b></p>
<div class="bhp"><b>Bhagavata Purana (9.22.35–45).</b> It carries the line on:
Parikshit → {arrows(BHP_AFTER)}. It then says the line of the Moon comes to an end with King Kshemaka,
in the Kali age (9.22.45).</div>

<h2>5. Krishna's family, and how he is related to the Pandavas</h2>
<p class="line">Yadu → … → Devamidha → Shura → <b>Vasudeva</b> <span class="ce">CE 7.119.6–7</span></p>
<ul class="ft">
<li><b>Shura</b>
  <ul><li><b>Vasudeva</b>, father of <b>Krishna</b> (Devaki's son). Krishna's elder brother was <b>Balarama</b>, and his sister <b>Subhadra</b> married Arjuna (1.90.85).</li>
  <li><b>Pritha</b>, given as a girl to King Kuntibhoja, and so called <b>Kunti</b>. She married Pandu. <span class="ce">1.104.1–3</span></li></ul></li>
</ul>
<p>So Kunti was Krishna's aunt, and the Pandavas were his cousins. Satyaki, Krishna's
kinsman who fights for the Pandavas, is the grandson of Shini, of the same clan (CE 7.119.8; 6.55.75).</p>
<div class="bhp"><b>Bhagavata Purana (9.23–24).</b> It gives the whole line from Yadu:
{arrows(BHP_YADU)}. It says Krishna was the eighth son of Vasudeva and Devaki, and Balarama the son of
Vasudeva and Rohini (9.24.46, 53–55).</div>

<h2>6. And families alive today?</h2>
<p>The Mahabharata's list ends with <b>Ashvamedhadatta</b> (CE 1.90.95). The Bhagavata Purana goes
on to <b>Kshemaka</b>, and says the line ends with him (9.22.45). Neither text names any later king
of this family, and neither links it to anyone alive today.</p>
<p>Many Indian families and clans keep a tradition that they descend from the line of the Moon
(<i>Chandravanshi</i> or <i>Somavanshi</i>). For example, the Jadeja and Bhati Rajputs trace
themselves to Yadu and Krishna, and the Tomars (Tanwars) to the Pandavas. These are family
traditions. No text joins them, name by name, to the kings above.</p>
</section>"""


# --------------------------------------------------------------------------- styling and output

def font_faces(garamond) -> str:
    out = []
    for f in garamond:
        m = re.search(r"(\d{3})-(normal|italic)", f.name)
        out.append(f"@font-face{{font-family:'EB Garamond';src:url('{f.as_uri()}');font-weight:{m.group(1)};"
                   f"font-style:{m.group(2)};}}")
    return "\n".join(out)


CSS = r"""
@page { size: A4; margin: 20mm 22mm 22mm 22mm; }
body { font-family:'EB Garamond', Georgia, serif; font-size:12.5pt; line-height:1.5; color:#000; background:#fff; margin:0; }
section { break-before: page; }
h1 { font-size:22pt; font-weight:600; margin:0 0 14px; }
h2 { font-size:15pt; font-weight:600; margin:24px 0 8px; }
h3 { font-size:13pt; font-weight:600; margin:18px 0 6px; }
p { margin:0 0 9px; }
.small { font-size:10.5pt; color:#444; }
.pb { break-before: page; }
sup.fn { font-size:8pt; font-weight:600; margin-left:1px; }

/* opening pages */
table { border-collapse:collapse; }
.cast { margin:6px 0 10px; font-size:11.5pt; }
.cast th { text-align:left; padding:3px 16px 3px 0; font-weight:600; vertical-align:top; white-space:nowrap; }
.cast td { padding:3px 0; }
.toc table { width:100%; font-size:12.5pt; }
.toc td { padding:5px 4px; border-bottom:1px solid #ddd; }
.toc td.n { width:28px; text-align:right; padding-right:12px; }
.toc td.ce { color:#555; font-size:10.5pt; width:70px; }
.toc td.p { text-align:right; width:30px; }
.toc tr.gap td { padding-top:18px; }

/* chapters */
.ch-no { font-size:12pt; letter-spacing:.15em; text-transform:uppercase; margin:10mm 0 2px; }
.ch-title { font-size:26pt; margin:0 0 2px; }
.ch-ce { font-size:10.5pt; color:#555; margin:0 0 12px; }
.ch-scenes { border:1px solid #000; padding:8px 12px; margin:0 0 20px; font-size:11pt; }
.ch-scenes ul { margin:4px 0 0; padding-left:18px; }
.who { font-size:10pt; font-weight:600; letter-spacing:.12em; text-transform:uppercase; margin:16px 0 3px; }
.text { text-align:justify; hyphens:auto; }

/* explanation boxes */
.box { break-inside:avoid; border:1px solid #000; padding:8px 12px 2px; margin:10px 0 16px; font-size:11.2pt; line-height:1.42; }
.box p { margin:0 0 6px; }
.box-h { font-size:12.5pt; }

/* index */
.gloss ul { list-style:none; padding:0; columns:2; column-gap:28px; font-size:11pt; }
.gloss li { display:flex; gap:4px; break-inside:avoid; padding:1px 0; }
.gloss .dots { flex:1; border-bottom:1px dotted #888; margin:0 3px 5px; }

/* family tree */
.line { font-size:12.5pt; line-height:1.7; }
.ce { font-size:9.5pt; color:#555; white-space:nowrap; margin-left:4px; }
.bhp { border:1px dashed #000; padding:8px 12px; margin:10px 0 14px; font-size:11pt; line-height:1.55; }
table.plain { width:100%; font-size:11pt; margin:6px 0 12px; }
table.plain th { text-align:left; font-weight:600; border-bottom:1px solid #000; padding:4px 6px; }
table.plain td { border-bottom:1px solid #ddd; padding:4px 6px; vertical-align:top; }
table.kings td { padding:2px 6px; }
table.kings td.n { color:#555; width:18px; text-align:right; }
table.kings td.ce { margin:0; }
ul.ft, ul.ft ul { list-style:none; margin:0; padding:0; }
ul.ft { margin:8px 0 12px; }
ul.ft ul { margin-left:10px; }
ul.ft ul li { position:relative; padding:2px 0 2px 18px; }
ul.ft ul li::before { content:""; position:absolute; left:0; top:0; bottom:0; border-left:1px solid #000; }
ul.ft ul li:last-child::before { bottom:auto; height:0.95em; }
ul.ft ul li::after { content:""; position:absolute; left:0; top:0.95em; width:12px; border-top:1px solid #000; }
ul.ft > li { padding:2px 0; }

/* cover */
.cover { height:297mm; width:210mm; position:relative; margin:0; text-align:center; }
.cover .t1 { position:absolute; top:38%; width:100%; font-size:36pt; font-weight:600; }
.cover .rule { position:absolute; top:47%; left:40%; width:20%; border-top:1px solid #000; }
.cover .t2 { position:absolute; top:50%; width:100%; font-size:16pt; font-style:italic; }
.cover .t4 { position:absolute; bottom:25mm; width:100%; font-size:10.5pt; color:#444; }
"""


def page_doc(body: str, fonts: str, cover=False) -> str:
    page_css = "@page { size:A4; margin:0; }" if cover else ""
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><style>{fonts}\n{CSS}\n{page_css}</style>"
            f"</head><body>{body}</body></html>")


def cover_html(title, line, foot):
    return (f'<div class="cover"><div class="t1">{title}</div><div class="rule"></div>'
            f'<div class="t2">{line}</div><div class="t4">{foot}</div></div>')


FOOTER = ("<div style=\"width:100%;font-family:Georgia,serif;font-size:8pt;color:#555;display:flex;"
          "justify-content:space-between;padding:0 22mm;\"><span>{left}</span>"
          "<span><span class='pageNumber'></span></span><span>{right}</span></div>")


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
    faces = font_faces(ensure_fonts())
    chapters, glossary = build_gita()
    date = datetime.date.today().strftime("%-d %B %Y")
    with sync_playwright() as pw:
        # the Gita, with its contents page numbers filled in on the second pass
        cov, body = OUT / "cover.pdf", OUT / "body.pdf"
        render(pw, page_doc(cover_html("The Bhagavad Gita", "told simply, with plain explanations",
                                       f"From the Mahabharata, Book 6 (BORI Critical Edition 6.23–40) · {date}"),
                            faces, cover=True), cov, None)
        wanted = {("c", c["num"]): f"Bhagavad Gita {c['num']} · CE {c['ce']}" for c in chapters}
        wanted.update({"gloss": "Explanations index Every idea", "tree": "Appendix: The Line of the Moon"})
        pages = {}
        for _ in range(2):
            doc = gita_html(chapters, glossary, pages) + tree_html()
            render(pw, page_doc(doc, faces), body, ("The Bhagavad Gita", "Mahabharata, Book 6"))
            pages = find_pages(body, wanted)
        merge([cov, body], OUT / "bhagavad-gita-told-simply.pdf")

        cov2, body2 = OUT / "cover2.pdf", OUT / "body2.pdf"
        render(pw, page_doc(cover_html("The Line of the Moon", "a family tree of the Kurus and the Pandavas",
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
