# Style Guide: the voice of the novel

> **In one line:** a storyteller by an evening fire, telling the oldest story
> they know to people they love. They speak plainly and warmly, they never
> hurry the big moments, and they never add a word the story did not say.

This guide sets the house voice. It was chosen after studying how the most
readable retellings and plain-language writers work (see §9, *Research
basis*). Every chapter is written to it and checked against it with
`tools/style_check.py`.

---

## 1. The voice

* **Plain.** Everyday English words. Short and medium sentences. One
  thing happens per sentence.
* **Human.** It sounds like a person telling a story aloud, not like a
  translation or a report. It has rhythm: short sentences for blows and
  shocks, longer ones for journeys and grief.
* **Grave when the story is grave.** The Mahabharata is about death, duty,
  love and ruin. Plain does not mean flippant. No jokes the text doesn't make,
  and no modern slang.
* **Faithful.** Everything in [`reference/CANON_POLICY.md`](../reference/CANON_POLICY.md)
  applies. The style serves the text. It never decorates it with invented
  facts.

**Think of it as** R. K. Narayan's clarity, Rajagopalachari's directness and
the spoken, campfire presence of Neil Gaiman's *Norse Mythology*, held to the
completeness and accuracy of a translation.

## 2. Sentences

1. **Average 12–16 words.** Most sentences run under 20 words. A long
   sentence is fine when it flows, but follow it with a short one.
2. **Active voice.** "Drona asked for his thumb," not "His thumb was asked
   for by Drona."
3. **Keep subject and verb close.** Put the doer first, then the deed.
4. **Vary the rhythm.** Three sentences of the same length and shape in a row
   is a signal to rewrite.
5. **Paragraphs: one to five sentences.** Each new speaker gets a new
   paragraph.
6. **Past tense, third person** for the story. The frame narrators speak in
   the first person when they speak.

## 3. Words

1. **Everyday words first.** *began*, not *commenced*; *went*, not
   *proceeded*; *enough*, not *sufficient*; *help*, not *assist*.
2. **No archaic English:** no *thou, thee, thy, hath, doth, verily, lo,
   behold, ere, wherefore, O king*. People address each other as they would
   aloud: "My king," "Mother," "Janamejaya."
3. **Sanskrit words are kept only when English has no true equivalent**
   (dharma, rakshasa, gandharva, apsaras, kshatriya, swayamvara…). Each is
   explained the first time it appears, in the sentence itself, not in a
   footnote: *"a rakshasa, one of the man-eating night-walkers of the
   forest."* After that, use it plainly. The full list is in
   [`GLOSSARY.md`](GLOSSARY.md).
4. **Do not translate a word into something false.** An *asura* is not a
   "demon" (asuras are the gods' elder rivals), and *dharma* is not simply
   "religion". Keep the word and explain it.
5. **Numbers** are words in narration ("a hundred sons", "eighteen days",
   "twelve years"). Large numbers from the text are kept exactly.
6. **British spelling** (honour, colour, armour, grey), the convention of
   Indian English.

## 4. Dialogue

The epic is mostly speech: vows, quarrels, pleading, teaching. Dialogue is
where the novel lives.

1. **People sound like people.** Contractions are fine in speech ("I won't",
   "don't"). They are rarer in narration.
2. **Keep the argument, cut the padding.** Long speeches keep every point the
   speaker makes, in the speaker's order. Stacked epithets and repeated
   compliments ("O best of the Bharatas, O tiger among men") go.
3. **Break long speeches** into paragraphs at each turn of the argument.
   Let listeners react only where the text shows them reacting.
4. **Speech tags:** mostly *said* and *asked*. Use *cried*, *whispered*,
   *shouted* only where the text shows it. Never tags like *hissed* or
   *breathed* that add an emotion the text lacks.
5. **Epithets in dialogue.** Characters may use a few traditional names for
   each other, as listed in [`NAMES.md`](NAMES.md): Partha for Arjuna,
   Keshava or Madhava for Krishna, Panchali for Draupadi. The narrator
   always uses the main name.

## 5. Emotion and the body

The epic shows feeling through the body, and so do we:

* tears, choked voices, trembling, fainting;
* hair standing on end (from fear *or* joy: the text uses both);
* breathing hard "like a snake";
* eyes red with anger, lips quivering, fists pressed together.

**Use what the text gives, at the moment it gives it.** Do not add feelings.
If the text reports only an action, report only the action and let the
reader feel it. This is where "human" comes from: restraint, and trust in
the reader.

## 6. Description and images

1. **Take descriptions from the text.** The epic describes cities, weapons,
   forests, chariots and battlefields richly. Use its details, compressed.
2. **Keep the epic's own similes** ("like a lion among deer", "like fire fed
   with butter"). Use one at a time, and never invent new ones that add
   meaning.
3. **Adjectives sparingly.** One good one beats three. No stacked
   triplets.
4. **Neutral texture only** where the text gives none: night falling, a
   silence, a road. It must assert nothing that could be quoted as a fact.

## 7. Structure

* **Chapters of about 2,500–4,500 words**, each built from a continuous CE
  range listed in its front matter.
* **Titles are plain** and name what happens: *The Fisherman's Price*,
  not *Shadows of Destiny*.
* **Open in the scene**, not with a summary. End on the turn: the moment
  things change.
* **Frames.** Open the book, and the war books, with the frame. Return to it
  only where the text does and where it matters (Sañjaya telling a father
  about his sons).
* **Quotation marks and the frame.** While Ugraśravas (the bard) tells a story
  inside his own frame (CE 1.1–1.54), his whole narration sits inside double
  quotes, with the characters' speech in single quotes. From Vaiśaṃpāyana's
  telling on (CE 1.57 onwards), the story is plain narrative prose with
  ordinary double quotes for speech. The frame returns as a line of dialogue
  only where the CE has Janamejaya ask a question or has a speaker label change
  back to the frame.

## 8. Never write these

These patterns make prose sound machine-made or second-hand. `tools/style_check.py`
flags them.

**Words and phrases:** delve, tapestry, testament, intricate, pivotal,
crucial, vibrant, realm, beacon, embark, journey (as metaphor), unwavering,
resonate, underscore, foster, landscape (as metaphor), "a symphony of",
"a dance of", "it is important to note", "it is worth noting", "little did
he know", "in that moment", "suddenly" (as a crutch), "couldn't help but",
"a sense of", "palpable", "the weight of", "echoed through", "sent shivers",
"eyes that held", "a testament to", "stands as".

**Patterns:**

* **Reflexive threes** ("brave, noble and wise"). Use a three only when the text has three.
* **"Not X, but Y" reveals** ("It was not anger. It was grief.")
* **Trailing *-ing* clauses** that add vague weight ("…, leaving a legacy that
  would echo for generations").
* **Em dashes** as all-purpose punctuation: at most about three per thousand
  words. Prefer commas, full stops, parentheses.
* **Narrator verdicts on significance** ("a moment that would change
  everything"). The story shows significance. The narrator does not announce it.
* **Foreshadowing the text doesn't make.** Where the text itself foretells (curses,
  prophecies, Sañjaya's asides), keep it. Do not add more.
* **Summary endings** that restate the chapter's meaning.
* **Modern idiom and slang:** okay, guys, deal with it, process (feelings), trauma, toxic.

## 9. Research basis

What we took, and from where:

| Source | What it teaches |
|--------|-----------------|
| R. K. Narayan, *The Mahabharata: A Shortened Modern Prose Version* (1978) | Economy and clarity. Reviewers praise it as concise and well written but call it at times "passionless", so we keep his clarity and restore the emotion the text itself carries. |
| C. Rajagopalachari, *Mahabharata* (1951) | Direct, unornamented prose for a broad Indian readership. |
| Neil Gaiman, *Norse Mythology* (2017) | Reviewers note it "feels more like verbal storytelling" and are surprised by its economy. The narrator is present but never intrusive, which suits our frames (Sauti, Vaiśaṃpāyana, Sañjaya). |
| US federal plain-language guidelines (plainlanguage.gov, Digital.gov) | Common words, active voice, short sentences ("usually fewer than 20 words"), writing for a 6th–8th grade reading level. |
| George Orwell, "Politics and the English Language" (1946) | No stale figures of speech, no long word where a short one will do, cut every word you can, active over passive, no jargon when an everyday word exists. |
| WikiProject AI Cleanup, "Signs of AI writing" (Wikipedia) | The list in §8: vocabulary such as *delve, tapestry, testament, pivotal*; reflexive threes; negative parallelism; em-dash overuse; trailing clauses; phantom authorities; "it's important to note". |

## 10. Readability targets

Measured by `python3 tools/style_check.py novel/...`:

| Measure | Target | Hard limit |
|---------|--------|-----------|
| Average sentence length | 12–16 words | ≤ 20 |
| Flesch Reading Ease | 70–85 | ≥ 60 |
| Flesch–Kincaid grade | 5–8 | ≤ 9 |
| Sentences over 35 words | < 3% | < 6% |
| Em dashes per 1,000 words | ≤ 3 | ≤ 6 |
| Banned words/patterns | 0 | 0 |

The numbers are guides, not goals. A chapter that scores well but reads
flatly still fails. Read every chapter aloud, or in your head at speaking
pace, before marking it done.

---

## 11. Worked example: Bhīṣma's vow (CE 1.94.68–94)

**Ganguli (1883), faithful but hard going:**

> "Chief of fishermen, thou best of men, listen to what I say in the presence
> of these assembled kings. Ye kings, I have already relinquished my right to
> the throne, I shall now settle the matter of my children. O fisherman, from
> this day I adopt the vow of Brahmacharya (study and meditation in
> celibacy). If I die sonless, I shall yet attain to regions of perennial
> bliss in heaven!"

**House style**, with every sentence traceable to a verse:

> The fisher-king received him with honour and spoke to him in front of the
> assembled kings. "You alone are guardian enough for Shantanu. But I am the
> girl's father, so I must say one thing. I see a single danger in this match,
> and it is a great one. Whoever has you for a rival, gandharva or asura,
> will never live in peace."
>
> Devavrata answered with the kings listening. "Then hear what I promise, and
> know it is true. No one born, or yet to be born, would dare say it. I will do
> as you ask. The son she bears will be our king."
>
> The fisherman pressed on. "You have made that promise in front of kings, and
> it is worthy of you. I do not doubt it. But the children you may have are
> another matter, and there my doubt is great."
>
> Devavrata understood. For his father's sake, he gave his answer.
>
> "King of the fishermen, listen, and let these kings hear it too. I have
> already given up the throne. Now I settle the question of children. From
> this day I will live as a celibate. I will have no son, and still the worlds
> of heaven will be mine for ever."
>
> The fisherman's hair stood on end with joy. "Then I give her," he said.
>
> From the sky, the apsarases, the gods and the seers rained down flowers.
> "This is Bhishma," they cried, *the one who does the terrible thing*.
>
> He turned to the young woman. "Mother, get into the chariot. We are going
> home."

Notice: *hair stood on end with joy* is the text's own image
(*saṃprahṛṣṭatanūruhaḥ*, 1.94.89). "Gandharva or asura" keeps the
text's words (1.94.75). Nothing is added, and it reads like a story.

*This excerpt is shortened to show the voice.* It leaves out the fisherman's
middle points (1.94.70–73: that even Indra would regret refusing such a
match, that Satyavatī's true father often praised Śaṃtanu, and that he once
refused the sage Asita). The chapter itself must keep them, because dropping
facts breaks the canon policy.

---

## 12. Chapter checklist

Before a chapter is marked `verified`:

- [ ] Every scene is in the source map, and every sentence passes the citation test.
- [ ] Nothing from the ledger's ⚠️/❌ lists slipped in.
- [ ] Names match [`NAMES.md`](NAMES.md). New Sanskrit terms are explained on first use.
- [ ] `tools/style_check.py` passes with no banned patterns and readability in range.
- [ ] Read through at speaking pace. Rewrite any line you would not say aloud.
- [ ] Front matter updated (`status`, `words`), index rebuilt, changelog entry added.

## 13. The Bhagavad Gita (Book 6, CE 6.23–40)

The author asked for the Gita to be told in full, in **very simple English**,
with **footnotes** that explain its ideas. This is the one place in the novel
where the reading text carries footnotes.

1. **Every verse is kept**, in order. Simple words, short sentences, but the
   meaning of each verse unchanged. Where a verse is hard, say plainly what it
   says and put the difficulty in the notes block (*Choices*), not in the text.
2. **Forms of address are trimmed** to a name now and then (Arjuna, Partha,
   Krishna). The frame stays: Sanjaya tells it (double quotes), the speakers
   speak in single quotes.
3. **Footnotes** go on a key word the first time it matters in a chapter,
   using Markdown footnotes with labels unique across the novel
   (`[^b6c7-1]`). The definitions sit at the end of the story text, before
   `<!-- notes -->`, under a `## Explanations` heading. Each footnote has:
   * **What it means**: a plain definition in one or two sentences;
   * **An everyday example**, marked as an example (it is not the text);
   * **In the story**, where one fits: a moment from the Mahabharata that
     shows the idea, **cited to the CE and checked** like any other claim.
     Never a vulgate or popular story.
4. **Footnotes explain; they do not add.** They do not tell the reader which
   school of interpretation is right, and they do not put new teachings in
   Krishna's mouth. Where commentators differ, say so briefly.
5. The readability targets apply to the footnotes too.
