# Chapter Template

Copy this into `novel/book-NN-slug/NN-short-title.md`. Keep the front matter
keys exactly. `tools/build_index.py` reads them.

````markdown
---
book: 1
chapter: 4
title: The Teacher's Pupils
ce: [1.3.1-89]
status: drafted
summary: One sentence on what happens.
---

# The Teacher's Pupils

(Story text in the house style: see workbook/STYLE_GUIDE.md.)

<!-- notes -->
## Notes

**Source map**

| Scene | CE |
|-------|----|
| Saramā curses Janamejaya's brothers | 1.3.1–8 |
| … | … |

**Divergences.** Popular versions add … (ledger L-NN). The CE has …

**Choices.** Where the CE is unclear, say how it was read and why.
````

## Field reference

| Key | Meaning |
|-----|---------|
| `book` | 1–18 (the parva) |
| `chapter` | Chapter number within the Book |
| `title` | Plain title that names what happens |
| `ce` | List of CE spans: `1.3`, `1.4-7`, `1.1.1-100`, `1.1.101-1.2.30` |
| `status` | `planned` → `drafted` (written, source-checked by the author) → `verified` (second full pass against CE and ledger, style check clean) → `revised` (later edits after verification) |
| `summary` | One line, used in indexes |

## Notes block

Everything after `<!-- notes -->` is removed from the reading edition by
`tools/compile_novel.py` and gathered into `build/notes.md`. The source map
is required. Divergences and choices are required whenever they apply.
