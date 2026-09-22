# Canon Policy: what counts as "Vyasa's Mahabharata"

This project retells **Vyasa's Mahabharata and nothing else**. This document
says exactly what that means, which sources decide questions, and what the
novel may and may not do with them. Every chapter is checked against it.

---

## 1. The problem

The Mahabharata was handed down for well over a thousand years in hundreds of
handwritten copies, in many scripts and regions. Copyists added passages,
some small and some very large. By the 1800s the printed "standard" text
(the **vulgate**, edited with Nīlakaṇṭha's 17th-century commentary) held a
great deal that the oldest manuscripts lack. Retellings, plays, regional
epics, folk theatre, novels and television then added more on top of that.

So "the Mahabharata most people know" contains three layers:

1. the text as far back as scholarship can recover it;
2. later additions found in some manuscripts (and in the vulgate);
3. stories from outside the epic altogether.

## 2. Our answer: the Critical Edition is canon

Between 1919 and 1966 the Bhandarkar Oriental Research Institute (BORI),
Pune, compared **1,259 manuscripts** and published the **Critical Edition
(CE)**. It is the oldest form of the text that the evidence supports. Its
editors kept a passage only when the manuscript traditions agreed on it.
Passages found only in some lines of transmission were moved into the
footnotes ("star passages", marked \*) or into **Appendix I** (longer
insertions).

**In this project, "Vyasa's Mahabharata" means the constituted text of the
Critical Edition: the 18 parvas, 1,995 adhyāyas.**

We accept the CE's limits honestly. It is a reconstruction that was never
one physical manuscript. Scholars still debate some of its choices. But it is
the only standard that is public, reasoned, and checkable verse by verse, and
it is what nearly all modern scholarly translations follow (van Buitenen,
Smith, Debroy). No other source gets the final word over it.

## 3. Source hierarchy

| Tier | Source | Status in the novel |
|------|--------|---------------------|
| **1** | **CE constituted text** (`tools/mbh.py show`) | **Canon.** Every event, speech, name and detail in the narrative must rest on it. |
| 2 | **Ganguli's English translation** (vulgate-based, 1883–1896) | **Translation aid only.** Used to understand the Sanskrit. Its content counts only where the CE agrees. |
| 3 | **Rejected passages**: CE star (\*) and Appendix (@) lines, and anything in Ganguli/the vulgate that the CE lacks | **Not canon.** Never narrated. May be *mentioned* in a chapter's endnotes when readers would expect it (e.g. Gaṇeśa as scribe). |
| ✗ | **Outside the epic**: Harivaṃśa (a supplement, outside the 18 parvas), the Purāṇas (Bhāgavata, Skanda, etc.), regional epics (Tamil, Kannada, Telugu, Bengali, Odia, etc.), Sanskrit plays (Bhāsa's *Ūrubhaṅga* and *Karṇabhāra*, Bhaṭṭa Nārāyaṇa's *Veṇīsaṃhāra*), folk theatre, modern novels (*Mrityunjaya*, *Yajnaseni*, *The Palace of Illusions*, *Parva*, *Jaya*), film and TV | **Excluded.** May appear only in endnotes that flag a popular misconception, as recorded in [`AUTHENTICITY_LEDGER.md`](AUTHENTICITY_LEDGER.md). |

When the CE and Ganguli differ, **the CE wins**. When the CE is unclear, say
so in the notes. Do not settle the question by borrowing from Tier 3.

## 4. Fidelity rules for the novel

The novel is a *retelling in plain English*, not a translation. That gives us
freedom of **language**, never of **content**.

### Allowed

* **Plain-English paraphrase** of narration and speeches.
* **Compressing repetition**: stacked epithets, formulaic battle catalogues,
  repeated praise, as long as no event, name that matters, or fact is lost.
  (Long lists may be summarised: "and many other kings, whose names the
  Pandavas knew by heart" is **not** allowed, because the text doesn't say
  that. Use "and many other kings" instead.)
* **Clarifying**: naming the speaker, spelling out who "he" is, adding the
  relationship the text assumes ("Bhishma, their great-uncle").
* **Showing what the text states**: tears, trembling, a flushed face, raised
  hair, a sigh "like a snake". The epic is full of bodily emotion. Use it.
* **Interior thought** when the text reports it ("he thought…", "his heart
  burned"), or when a speech states the feeling outright.
* **Scene transitions** that assert nothing new ("The night passed.").
* **Endnotes** on context, meaning and divergences (see §6).

### Forbidden

* **New events, characters, names, objects or places**, including famous
  later ones (see the ledger: Vrushali, Bhanumati, Barbarika, Aravan's
  self-sacrifice, Shakuni's bone dice…).
* **New dialogue content**: no speech may say something the character does
  not say in the CE. Short acknowledgements are fine only where the text
  reports the act ("She agreed" may become "'I will,' she said").
* **Invented motives or psychology** beyond what the text states or clearly
  shows. Where the text is silent on why, the novel is silent too.
* **Resolving ambiguity by fiat.** If the text leaves something open (Kṛṣṇa's
  role in the disrobing, for example), the novel leaves it open.
* **Rationalising or modernising**: no "explaining away" the miraculous, and
  no added miracles. Numbers (armies, ages, years) are kept as stated.
* **Commentary in the narrative voice** ("This shows that dharma…"). Let the
  characters argue; the narrator reports.

### The citation test

> Every sentence of narrative must be traceable to a verse range in the
> chapter's source map. If a reader could quote a sentence as "something that
> happens in the Mahabharata", it must actually happen in the CE.

A sentence that fails the test is cut, or rewritten until it passes.

### Texture: the grey zone

A novel needs some physical texture. It is allowed only when it is **drawn
from the text** (the epic describes cities, weapons, forests, sacrifices and
battles in detail, so use those descriptions) or when it is **neutral and adds
no fact** (light, silence, the passage of night). Test: *does this detail
tell the reader anything they could repeat as a fact about the story?* If
yes, it needs a verse.

## 5. Frames and voices

The CE is a story within a story within a story. The novel keeps them:

* **Ugraśravas (Sauti)** tells Śaunaka's sages in the Naimiṣa forest (Book 1
  opening).
* **Vaiśaṃpāyana** tells King Janamejaya at the snake sacrifice (most of the
  epic).
* **Sañjaya** tells blind Dhṛtarāṣṭra about the war (Books 6–10), using the
  divine sight Vyāsa gave him.
* Characters tell their own inset stories (Nala, Sāvitrī, Rāma…).

Frames are used lightly: at the openings, where the text returns to them, and
where they carry weight (a father hearing of his sons' deaths).

## 6. Endnotes

Each chapter file ends with a notes block (removed from the reading edition
by `tools/compile_novel.py`):

1. **Source map**: which CE verses each scene comes from.
2. **Divergences**: anything readers may expect but will not find, with a
   pointer to the ledger (e.g. "The CE has no Kṛṣṇa invocation here; see
   L-19").
3. **Choices**: how an unclear passage was read, and why.

## 7. Changing this policy

This policy is the project's constitution. Changes must be recorded in
[`CHANGELOG.md`](../CHANGELOG.md) with a reason, and chapters affected by
the change must be re-checked. One likely future option is a **vulgate
companion edition** that includes famous Tier-3 episodes in clearly marked
boxes. If that is ever wanted, it goes in a separate build, never mixed into
the canon text.
