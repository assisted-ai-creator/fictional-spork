# Changelog

All notable changes to the novel and its workbook. Newest first.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions: `0.BOOK.N`, with the minor number tracking the Book being drafted.

## [Unreleased]

### Novel: Book 1 (Adi Parva), chapters 1–7 drafted
- Ch 1 *The Storyteller in the Forest* (CE 1.1.1–101); Ch 2 *When I Heard*
  (1.1.102–210); Ch 3 *The Hundred Parts* (1.2); Ch 4 *The Teacher's Pupils*
  (1.3.1–84); Ch 5 *The Queen's Earrings* (1.3.85–195); Ch 6 *The Fire's
  Witness* (1.4–7); Ch 7 *Half a Life* (1.8–12). About 18,900 words, all
  style-checked. Each chapter has a verse-level source map and notes on
  divergences and reading choices.
- Fidelity catches recorded in chapter notes: Agni's reply to Puloman is only
  a rejected star passage (\*220), so the novel gives no invented speech;
  the lament verses found only in the vulgate are left out; the number of
  snakes at 1.3.142 is read as 28,800 (the vulgate has 28,008).

### Reference
- Ledger **L-62**: "Parashurama" never appears in the CE. The CE calls him Rama
  Jamadagnya or Bhargava Rama.

### Workbook
- `names.json`: +27 people (frame, Paushya and Pauloma stories, gods), including
  two distinct Dhaumyas.
- `NOVEL_PLAN.md`: the CE's own list of the hundred parts (1.2.34–69);
  chapter rows for chapters 1–3 updated to their actual ranges.

## [0.1.0] - 2026-09-22

The foundation: sources, tools, canon rules, the verified ledger, the house
style and the workbook. Book 1 drafting begins.

### Sources
- Added the **K. M. Ganguli translation** (1883–1896, public domain), all 18
  books, from the sacred-texts digitisation packaged by AASI, pinned to
  commit `3b6591b`, with SHA-256 checksums (`sources/ganguli.sha256`).
- Added `tools/fetch_sources.sh` to fetch the **BORI Critical Edition**
  electronic text (GRETIL, Tokunaga/Smith, © BORI 1999, reference use only)
  from the INDOLOGY GRETIL mirror, pinned to commit `0baf718`, verified by
  checksum and not committed. The file includes many CE star and Appendix I
  passages, which lets the project tell CE text apart from rejected
  interpolations.
- Added `sources/ce_structure.json`: verse counts for all 1,995 adhyāyas
  (73,815 verses), used for coverage tracking.

### Tools
- `tools/mbh.py`: CE and Ganguli parsers; `show`, `search`, `check`,
  `speakers`, `stats`, `gshow`, `gsearch`, `gtoc`, `where`, `concordance`.
  Matching is diacritic-insensitive.
- `index/concordance.csv`: automatic alignment of all 1,995 CE adhyāyas to
  Ganguli's 2,113 sections, by proper-name overlap with a monotonic
  assignment. Spot-checked, including the Gītā (CE 6.23–40 = G 6.25–42).
- `tools/style_check.py`: readability, banned words and patterns, archaisms,
  name spellings, and a watch-list of non-Vyasa names.
- `tools/build_index.py`: generates `index/CONTENTS.md`,
  `index/COVERAGE.md` (verse-level), `index/CHARACTER_INDEX.md` and
  `workbook/NAMES.md`. Validates chapter front matter and CE spans.
- `tools/compile_novel.py`: builds the reading edition and collected notes.

### Reference
- `reference/CANON_POLICY.md`: the CE constituted text is canon; source
  tiers; fidelity rules; the citation test.
- `reference/AUTHENTICITY_LEDGER.md`: **61 verified entries**, each with
  evidence, including: Ganesha as scribe ⚠️; Karna refused at the
  swayamvara ⚠️; "a blind man's son is blind" ❌; Krishna at the disrobing 🔶;
  Draupadi's hair vow ❌; the akshaya patra 🔶; Urvashi's curse ⚠️;
  Abhimanyu in the womb ⚠️; Krishna hiding the sun for Jayadratha ⚠️;
  Barbarika, Vrushali, Bhanumati, Aravan's sacrifice ❌.
- `reference/BIBLIOGRAPHY.md`.

### Workbook
- `STYLE_GUIDE.md`: the house voice, researched from Narayan,
  Rajagopalachari, Gaiman's *Norse Mythology*, the US plain-language
  guidelines, Orwell and Wikipedia's "Signs of AI writing". Includes a
  worked example (Bhishma's vow, CE 1.94).
- `NOVEL_PLAN.md`: 18 Books, about 429 chapters; Book 1 sub-parvas
  confirmed against the CE; the first chapter plan.
- `names.json` / `NAMES.md` (60 people, 7 watch-list names), `CHARACTERS.md`
  (with the CE's list of divine portions, 1.61.63–98), `GLOSSARY.md`,
  `PLACES.md`, `GENEALOGY.md`, `TIMELINE.md` (war chronology from CE
  1.2.26–28), `CHAPTER_TEMPLATE.md`, `README.md`.
- `CLAUDE.md`: rules and workflow for future sessions.
