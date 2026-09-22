# Sources

This folder holds the texts the novel is checked against. Nothing in the
novel may rest on anything other than these sources (see
[`reference/CANON_POLICY.md`](../reference/CANON_POLICY.md)).

| # | Source | What it is | Role | In repo? |
|---|--------|-----------|------|----------|
| 1 | **Critical Edition (CE)**: *The Mahābhārata, for the first time critically edited*, Bhandarkar Oriental Research Institute (BORI), Pune, 1933–1966. Gen. eds. V. S. Sukthankar, S. K. Belvalkar, P. L. Vaidya. | Sanskrit text reconstructed from 1,259 manuscripts. 18 books, 1,995 adhyāyas, 73,816 verse units. | **Primary authority.** "Vyasa's Mahabharata" in this project means the CE constituted text. | No. Fetched by script (see licence note). |
| 1a | CE electronic text, GRETIL `mbh_01_u.htm`–`mbh_18_u.htm` | Entered by Muneo Tokunaga et al., revised by John D. Smith (Cambridge). Electronic text © BORI 1999. Unicode IAST. Also carries many **star (\*) passages** and **Appendix I (@) passages**: the lines the CE editors *rejected* as later additions. | Lets us tell "in the CE" apart from "only in rejected manuscript passages". | `sources/ce/gretil/` (git-ignored) |
| 2 | **Ganguli translation**: Kisari Mohan Ganguli, *The Mahabharata of Krishna-Dwaipayana Vyasa*, published by Pratap Chandra Roy, Calcutta, 1883–1896. | The only complete English translation in the public domain. Made from the **vulgate** (Nīlakaṇṭha/Bengal-Bombay) text, so it includes passages the CE rejected. | **Secondary.** Used as a translation aid and as evidence of what the vulgate contains. | `sources/ganguli/` (committed) |

## Where the files came from

| Source | Upstream | Pinned commit | Checksums |
|--------|----------|---------------|-----------|
| CE (GRETIL) | [github.com/INDOLOGY/gretil-mirror](https://github.com/INDOLOGY/gretil-mirror), path `gretil.sub.uni-goettingen.de/gretil/1_sanskr/2_epic/mbh/` (mirror of [GRETIL](http://gretil.sub.uni-goettingen.de/gretil.html), Göttingen) | `0baf718d8e450821eb0403c03aacc9a4a82316d7` (2026-02-21) | [`ce.sha256`](ce.sha256) |
| Ganguli | [github.com/aasi-archive/mbh](https://github.com/aasi-archive/mbh), `txt/maha01.txt`–`maha18.txt` (sacred-texts.com / Distributed Proofreaders digitisation, 2003; misnumbered sections corrected by AASI) | `3b6591bd1d6e3b10998eb2f7e859e5edb75445d9` (2023-09-22) | [`ganguli.sha256`](ganguli.sha256) |

Fetch or verify everything with:

```bash
tools/fetch_sources.sh          # no-op if present and checksums match
tools/fetch_sources.sh --force  # re-download
```

The script also builds `sources/cache/` (parsed text used by `tools/mbh.py`).

## Licence notes

* **CE electronic text.** The GRETIL file header says: *"Electronic text (C)
  Bhandarkar Oriental Research Institute, Pune, India, 1999 … THIS GRETIL TEXT
  FILE IS FOR REFERENCE PURPOSES ONLY! COPYRIGHT AND TERMS OF USAGE AS FOR
  SOURCE FILE."* We therefore **do not commit it**. We fetch it for reference,
  and the repo only holds short quotations used as evidence in
  `reference/AUTHENTICITY_LEDGER.md`, plus derived facts such as chapter
  counts and the concordance.
* **Ganguli.** The 1883–1896 translation is in the public domain. The
  sacred-texts.com digitisation credits are kept at the head of each file.
  The AASI repository that packages it is released under CC0.

## Known gaps in the sources

* Ganguli lacks sections 7.54, 7.55, 7.189 and 12.364, which are missing from
  the digitisation (noted upstream). The CE covers that material. Use
  `tools/mbh.py where` to find the CE adhyāya.
* Four CE apparatus lines are malformed upstream (1.186.3d\*1903, 3.62.17,
  3.83.82d, 4.21.67d\*457). All are star or appendix lines, not the constituted
  text. The parser warns about them and skips them.
* The star and appendix passages in the GRETIL file are **not the complete
  critical apparatus**. For example, Adi Appendix I No. 1 has Brahmā's visit to
  Vyāsa but not the Gaṇeśa-as-scribe lines. When something is missing from
  both the CE text and these passages, check Ganguli before calling it
  "not in any version".

## Numbering

* CE references: `BOOK.ADHYAYA.VERSE`, e.g. `1.94.88` (Bhīṣma's vow).
* Ganguli references: `G BOOK.SECTION`, e.g. `G 1.100`. Ganguli's section
  numbers drift away from the CE's adhyāya numbers (the vulgate splits and
  adds chapters). [`index/concordance.csv`](../index/concordance.csv) maps
  every CE adhyāya to its Ganguli section(s). It is built automatically by
  aligning proper names, is usually exact and sometimes off by one, so check
  both texts.
