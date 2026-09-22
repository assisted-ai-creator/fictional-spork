# CLAUDE.md: working on this repository

This repo is a novel: **Vyasa's Mahabharata retold in plain English**, with
100% fidelity to the BORI Critical Edition (CE). Accuracy outranks
everything else.

## First, every session

```bash
tools/fetch_sources.sh            # fetch/verify the CE text (git-ignored) and build caches
python3 tools/build_index.py      # see where things stand
cat index/COVERAGE.md | head -30  # next uncovered verses
```

## Non-negotiable rules

1. **Canon = the CE constituted text.** Read `reference/CANON_POLICY.md`.
   Ganguli is a translation aid. Star (\*) and appendix (@) passages, the
   vulgate's extras, and anything from outside the epic are never narrated.
2. **Citation test.** Every sentence of narrative must trace to CE verses in
   the chapter's source map. No invented events, speeches, motives, names or
   descriptive "facts".
3. **Check before you claim.** Never state from memory what the text says.
   Use `tools/mbh.py show/search/check` and *read the verses*. Hit counts
   are not evidence. When a popular story comes up, check
   `reference/AUTHENTICITY_LEDGER.md` and add an entry if it's missing.
4. **House style**: `workbook/STYLE_GUIDE.md`. Plain, human, British spelling,
   no archaisms, no AI tells. Run `tools/style_check.py` on every chapter.
5. **Spellings** come from `workbook/names.json` only.
6. **Never commit the CE text** (`sources/ce/`, `sources/cache/`): it is
   licensed "for reference purposes only". Short quotations as evidence are
   fine.

## Chapter workflow

See `workbook/README.md`. In short: read the CE range (`mbh.py show X --all`),
read Ganguli (`mbh.py where X`, `mbh.py gshow Y`), write the source map, draft,
run `style_check.py`, update the workbook files and `names.json`, run
`build_index.py`, add a `CHANGELOG.md` entry, commit.

## Tools

| Command | Purpose |
|---------|---------|
| `tools/mbh.py show 1.94.80-94 [--all]` | Read CE verses (`--all` shows rejected passages, marked `*`/`@`) |
| `tools/mbh.py search PATTERN [-b N] [--all]` | Diacritic-insensitive CE search |
| `tools/mbh.py check SKT... -e ENG [-b N]` | Where does something occur: CE / rejected / Ganguli |
| `tools/mbh.py gshow 1.100` · `gsearch` · `gtoc` | Ganguli translation |
| `tools/mbh.py where 1.94` | Ganguli sections aligned with a CE adhyāya |
| `tools/mbh.py speakers 1.94` | Speaker changes in an adhyāya |
| `tools/style_check.py PATHS` | House-style lint and readability |
| `tools/build_index.py [--check]` | Regenerate `index/` and `workbook/NAMES.md` |
| `tools/compile_novel.py [--book N]` | Build the reading edition in `build/` |

## Git

Commit messages describe what changed (chapters written, ledger entries,
tools). Keep `CHANGELOG.md` current: every session adds an entry.
