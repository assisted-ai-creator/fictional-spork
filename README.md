# The Mahabharata: Vyasa's Epic, Told in Plain English

A complete retelling of Vyasa's Mahabharata as a novel in simple, human
English. It is **faithful to the Critical Edition** (Bhandarkar Oriental
Research Institute, Pune) and leaves out every later addition, folk tale and
modern invention.

> **Status:** Book 1 (Ādi Parva) drafted in full: 92 chapters, all 225 adhyāyas.
> Book 2 (Sabhā Parva) next. See
> [`index/CONTENTS.md`](index/CONTENTS.md) and
> [`index/COVERAGE.md`](index/COVERAGE.md).

## What makes this different

* **Nothing invented.** Every sentence traces to verses of the Critical
  Edition (the *citation test*). Each chapter ends with a source map.
* **Real vs. later additions, checked.** The
  [Authenticity Ledger](reference/AUTHENTICITY_LEDGER.md) records, with
  evidence, what is really in the text. For example: in the Critical
  Edition, Krishna does not hide the sun for Jayadratha's death, Draupadi
  never says "a blind man's son is blind", and Ganesha does not write the poem.
* **Plain and human.** A storyteller's voice, with no archaic English and no
  padding. See the [Style Guide](workbook/STYLE_GUIDE.md).

## Repository map

| Folder | Contents |
|--------|----------|
| [`novel/`](novel/) | The novel: `book-NN-parva/NN-title.md`, one file per chapter |
| [`workbook/`](workbook/) | The writer's workbook: plan, style, names, characters, glossary, places, genealogy, timeline |
| [`reference/`](reference/) | Canon policy, authenticity ledger, bibliography |
| [`index/`](index/) | Generated indexes: contents, coverage, character index, CE↔Ganguli concordance |
| [`sources/`](sources/) | Source texts and provenance (the Ganguli translation is committed; the CE is fetched) |
| [`tools/`](tools/) | Python tools: read/search sources, check style, rebuild the index, compile |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed, session by session |

## Quick start

```bash
tools/fetch_sources.sh                        # fetch + verify sources, build caches
python3 tools/mbh.py show 1.94.86-94          # read Bhishma's vow in the CE
python3 tools/mbh.py check urvas -e Urvasi -b 3   # is Urvashi's curse in the CE?
python3 tools/style_check.py novel/           # lint chapters
python3 tools/build_index.py                  # refresh index/
python3 tools/compile_novel.py                # reading edition -> build/manuscript.md
```

Python 3.9+ and git. No other dependencies.

## Sources and licences

* Critical Edition electronic text © BORI 1999 (GRETIL, reference use). It is
  not redistributed here: `tools/fetch_sources.sh` downloads it.
* K. M. Ganguli's translation (1883–1896) is in the public domain.
* The novel text and project files are the author's work.
