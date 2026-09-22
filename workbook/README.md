# The Workbook

Everything a writer needs to continue the novel. Start here.

| File | What it's for |
|------|---------------|
| [`NOVEL_PLAN.md`](NOVEL_PLAN.md) | The shape of the whole novel: 18 Books, sub-parvas, chapter plans |
| [`STYLE_GUIDE.md`](STYLE_GUIDE.md) | The house voice, with rules, banned patterns, targets and a worked example |
| [`CHAPTER_TEMPLATE.md`](CHAPTER_TEMPLATE.md) | Front matter and notes format for chapter files |
| [`names.json`](names.json) → [`NAMES.md`](NAMES.md) | Spellings, IAST, dialogue names, "never write" variants |
| [`CHARACTERS.md`](CHARACTERS.md) | Character bible: who people are *as the text shows them* |
| [`GLOSSARY.md`](GLOSSARY.md) | Sanskrit words the novel keeps, and how to gloss them |
| [`PLACES.md`](PLACES.md) | Places, with CE references |
| [`GENEALOGY.md`](GENEALOGY.md) | Family trees, with CE references |
| [`TIMELINE.md`](TIMELINE.md) | Internal chronology and war days |

Reference material lives in [`../reference/`](../reference/): the canon
policy, the authenticity ledger and the bibliography. Generated indexes live
in [`../index/`](../index/).

## The chapter workflow

1. **Pick the next range.** Check [`index/COVERAGE.md`](../index/COVERAGE.md)
   for the next uncovered verse and the chapter plan in `NOVEL_PLAN.md`.
2. **Read the CE** for the range, with the rejected passages shown so you
   know what *not* to include:
   ```bash
   python3 tools/mbh.py show 1.3 --all
   python3 tools/mbh.py speakers 1.3        # who speaks when
   ```
3. **Read Ganguli** for the same material, as a translation aid:
   ```bash
   python3 tools/mbh.py where 1.3           # which Ganguli sections
   python3 tools/mbh.py gshow 1.3
   ```
   Anything in Ganguli that is not in the CE stays out. If readers will
   miss it, note it and add or cite a ledger entry.
4. **Write a beat list** (the source map) before the prose: scene → CE verses.
5. **Draft** in the house style. Every sentence must pass the citation test.
6. **Check:**
   ```bash
   python3 tools/style_check.py novel/book-01-adi/04-*.md
   ```
7. **Update**: names (`names.json`), glossary, places, genealogy, timeline and
   character bible, with CE refs. Then rebuild the index:
   ```bash
   python3 tools/build_index.py
   ```
8. **Log** the chapter in [`CHANGELOG.md`](../CHANGELOG.md) and commit.

A chapter moves from `drafted` to `verified` only after a second, separate
pass that re-reads the CE range against the finished prose, sentence by
sentence.
