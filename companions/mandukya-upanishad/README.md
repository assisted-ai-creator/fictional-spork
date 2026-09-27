# The Mandukya Upanishad, in plain English

A companion text. It is **not** part of the Mahabharata and not part of the
novel in this repository. It is kept here, in its own folder, as a
stand-alone reading.

The Mandukya is the shortest of the major Upanishads. In twelve short
passages it takes the sound **Om** and uses it as a map of your own mind:
waking, dreaming, dreamless sleep, and a fourth thing that runs underneath
all three.

On this page you will find, for each passage:

1. the Sanskrit, in Devanagari script;
2. the same Sanskrit in Roman letters (IAST), so you can sound it out;
3. a plain English translation;
4. **Hard words:** what the difficult terms mean;
5. **What it is saying:** a short explanation;
6. **A modern picture:** an everyday comparison to help it land.

The translation says only what the Sanskrit says. Everything under
"What it is saying" and "A modern picture" is explanation, not text, and
where the explanation comes from a traditional commentator it says so.

---

## How long is it?

| Measure | Count |
|---|---|
| Passages (mantras) | **12** |
| Sanskrit words, as written in Devanagari | **132** |
| Sanskrit words, with the sound-joins undone | **206** |
| Plain English translation below (the translation only, not the notes) | **538** |

**Why two Sanskrit counts?** Sanskrit runs words together when their sounds
meet. This is called *sandhi*, "joining". So *sarvam hi etat brahma ayam
ātmā* is written *sarvaṃ hyetadbrahmāyamātmā*: six words on paper as two. The
first count is what you see between the spaces. The second pulls every
word apart but keeps compound words (like *ekonaviṃśatimukhaḥ*,
"nineteen-mouthed") whole. The first number can shift a little between
printed editions, because editors split the joins in slightly different
places. The second is the steadier measure.

The twelve mantras are prose, not metrical verse, even though they are
usually called "verses". Neither count includes the opening words
*Hariḥ Om* or the peace chant, which are recited with the text but are not
part of it.

You can check the counts yourself:

```bash
python3 companions/mandukya-upanishad/count_words.py
```

| Mantra | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Written words | 10 | 5 | 7 | 6 | 18 | 10 | 19 | 9 | 11 | 14 | 14 | 9 | **132** |
| Separate words | 23 | 11 | 8 | 8 | 23 | 12 | 29 | 15 | 19 | 23 | 19 | 16 | **206** |

---

## Where the text comes from

* The Mandukya belongs to the **Atharvaveda**, the fourth of the Vedas.
* The Sanskrit given here is the standard text of twelve mantras, the one
  on which the teacher **Shankara** (Śaṅkara) wrote his commentary. It was
  checked word for word against two independent online copies
  (sanskritdocuments.org and shlokam.org), which agree with each other.
  The only differences between them are spelling-level: whether a join is
  written with a space, or *ॐ* is spelt *ओम्*. None of them changes the
  meaning.
* The **Mandukya Karika** of **Gaudapada** (Gauḍapāda) is a separate,
  later work: 215 verses of explanation in four chapters. It is often
  printed together with the Upanishad and is sometimes mistaken for part
  of it. It is not translated here. (One school, that of Madhva, treats
  some verses of the Karika's first chapter as scripture too. The twelve
  mantras are what everyone agrees on.)
* How much this little text was valued: the *Muktika Upanishad* (1.26)
  says, "The Mandukya alone is enough for those who seek freedom."

The English translation on this page is new, made directly from the
Sanskrit for this repository.

---

## Key words at a glance

You will meet these again and again. Each is explained in more detail at
the passage where it first appears.

| Word | Say it | Plain meaning |
|---|---|---|
| **Om** (*oṃ*, *oṅkāra*) | "om" | The sacred sound. Here it stands for everything that is. |
| **Akshara** (*akṣara*) | "uk-sha-ra" | A syllable. The same word also means "that which does not wear away". |
| **Brahman** | "brah-mun" | The one Reality behind everything. Not a god with a face, and not the god Brahma. |
| **Atman** (*ātman*) | "aat-mun" | The Self: what you really are, underneath body and thoughts. |
| **Pada** (*pāda*) | "paa-da" | A foot, or a quarter. The Self is said to have four. |
| **Matra** (*mātrā*) | "maa-traa" | A measure; here, one unit of sound. Om has three: A, U, M. |
| **Prajna** (*prajña*, *prajñā*) | "praj-nya" | Awareness, knowing. |
| **Vaishvanara** (*vaiśvānara*) | "vysh-vaa-na-ra" | "Common to all people": the Self as the waker. |
| **Taijasa** (*taijasa*) | "tie-ja-sa" | "The shining one": the Self as the dreamer. |
| **Prajna** (*prājña*) | "praaj-nya" | "The knowing one": the Self in deep, dreamless sleep. |
| **The Fourth** (*caturtha*) | "cha-tur-tha" | What is left when you look past all three states. |
| **Prapancha** (*prapañca*) | "pra-pun-cha" | The world "spread out" into many separate things. |
| **Advaita** | "ud-vy-ta" | "Not two": without a second. |
| **Shiva** (*śiva*) | "shi-va" | Here an adjective: good, kind, blessed. Not the name of the god. |

---

## The peace chant

Before and after studying the Upanishads of the Atharvaveda, students
traditionally recite this prayer. The *Muktika Upanishad* names it as the
chant for this group, which includes the Mandukya. It comes from the
Rigveda (1.89.8–9). It is **not** one of the twelve mantras and is not
counted above.

> ॐ भद्रं कर्णेभिः शृणुयाम देवाः । भद्रं पश्येमाक्षभिर्यजत्राः ।
> स्थिरैरङ्गैस्तुष्टुवांसस्तनूभिः । व्यशेम देवहितं यदायुः ॥
> स्वस्ति न इन्द्रो वृद्धश्रवाः । स्वस्ति नः पूषा विश्ववेदाः ।
> स्वस्ति नस्तार्क्ष्यो अरिष्टनेमिः । स्वस्ति नो बृहस्पतिर्दधातु ॥
> ॐ शान्तिः शान्तिः शान्तिः ॥

> *oṃ bhadraṃ karṇebhiḥ śṛṇuyāma devāḥ, bhadraṃ paśyemākṣabhir yajatrāḥ,
> sthirair aṅgais tuṣṭuvāṃsas tanūbhiḥ, vyaśema devahitaṃ yad āyuḥ.
> svasti na indro vṛddhaśravāḥ, svasti naḥ pūṣā viśvavedāḥ,
> svasti nas tārkṣyo ariṣṭanemiḥ, svasti no bṛhaspatir dadhātu.
> oṃ śāntiḥ śāntiḥ śāntiḥ.*

Om. Gods, may our ears hear what is good. Holy ones, may our eyes see what
is good. With steady limbs and bodies, singing your praise, may we live out
the life the gods have given us.

May Indra, whose fame has grown great, keep us well. May Pushan, who knows
all things, keep us well. May Tarkshya, whose wheel-rim is never broken,
keep us well. May Brihaspati keep us well.

Om. Peace, peace, peace.

**Why "peace" three times?** A common traditional explanation is that it
asks for peace from three kinds of trouble: trouble from within (illness,
worry), trouble from other creatures, and trouble from forces beyond
anyone's control (storms, earthquakes). That is a later explanation, not
something the chant itself says.

---

## The Upanishad

Recitation traditionally begins with the words **हरिः ॐ** (*hariḥ oṃ*), a
short call to the divine before any sacred text.

### Mantra 1: Everything is Om

> ओमित्येतदक्षरमिदं सर्वं तस्योपव्याख्यानं भूतं भवद्भविष्यदिति सर्वमोङ्कार एव ।
> यच्चान्यत्त्रिकालातीतं तदप्योङ्कार एव ॥ १ ॥

> *omityetadakṣaramidaṃ sarvaṃ tasyopavyākhyānaṃ bhūtaṃ bhavadbhaviṣyaditi
> sarvamoṅkāra eva | yaccānyattrikālātītaṃ tadapyoṅkāra eva || 1 ||*

**Translation.** Om: this sound is all that is. Here is a closer account
of it. What has been, what is, and what will be: all of it is simply Om.
And whatever else there is, beyond these three times, that too is simply
Om.

**Hard words**

* **Akshara** (*akṣara*): "syllable". It also means "imperishable", from
  *a-* "not" and *kṣara* "wearing away". The double meaning is on purpose:
  the syllable Om stands for what never wears away.
* **Idam sarvam**: "all this". A standard Upanishad phrase for the whole
  world you can see, hear and touch.
* **Upavyakhyana** (*upavyākhyāna*): a "closer explanation". The text is
  telling you that the rest of the Upanishad unpacks this first line.
* **Trikala-atita** (*trikālātīta*): "gone beyond the three times", past,
  present and future.

**What it is saying.** The Upanishad opens with one bold claim. There is
one sound, Om, and it stands for *everything*: everything in time, and
whatever lies outside time as well. A name and the thing it names are
close partners. Here Om is treated as the name of the whole of reality.

**A modern picture.** Think of a film on a streaming service. When you
watch it, you see only one moment at a time: the past scenes are gone and
the future scenes have not come yet. But the whole film, beginning to end,
already exists as one file. And there is something that is not in any
scene at all: the screen it plays on. The Upanishad says Om covers all of
it: every scene, past, present and future, *and* the screen.

---

### Mantra 2: The Self is Brahman, and it has four quarters

> सर्वं ह्येतद्ब्रह्मायमात्मा ब्रह्म सोऽयमात्मा चतुष्पात् ॥ २ ॥

> *sarvaṃ hyetadbrahmāyamātmā brahma so'yamātmā catuṣpāt || 2 ||*

**Translation.** All this is Brahman. This Self is Brahman. And this Self
has four quarters.

**Hard words**

* **Brahman**: the one Reality behind and within everything. It comes
  from a root meaning "to grow, to be great". It is not the creator god
  Brahma, and not a person.
* **Atman** (*ātman*): "the Self". Not your name, body, job or
  personality, but the plain fact of *being aware* that sits underneath
  all of those.
* **Ayam atma** (*ayam ātmā*): "*this* Self". The word *ayam*, "this", is
  pointing close by: to your own Self, right here.
* **Chatushpat** (*catuṣpāt*): "four-footed", "having four quarters".
  *Pāda* means both "foot" and "quarter" (as a quarter-line of a verse, or
  a quarter of a coin).

**What it is saying.** In one breath the text makes two huge statements.
First, the whole universe is Brahman. Second, your own Self is that same
Brahman: what is deepest in you and what is deepest in everything are one
and the same. "This Self is Brahman" (*ayam ātmā brahma*) is counted by
the tradition as one of the four "great sayings" of the Upanishads.

Then it says the Self has four "quarters", and the next five mantras
describe them. The commentator Shankara adds a helpful warning: these are
not like the four legs of a cow, four separate parts standing side by
side. They are like the four quarters of an old coin, where you count the
first three up into the fourth, and so reach the whole.

**A modern picture.** Think of the air inside a balloon and the air in the
room. The rubber skin makes it *look* as if there are two airs, "mine" and
"the room's". Take away the skin and you see there was only ever one air.
The Upanishad says your Self and Brahman are like that.

For the four quarters, think of one person seen four ways: at their desk
by day, in their dreams at night, in deep sleep, and as the one who was
there through all three. Not four people. One person, four ways of being
found.

---

### Mantra 3: The first quarter, the waker

> जागरितस्थानो बहिष्प्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः स्थूलभुग्वैश्वानरः प्रथमः पादः ॥ ३ ॥

> *jāgaritasthāno bahiṣprajñaḥ saptāṅga ekonaviṃśatimukhaḥ
> sthūlabhugvaiśvānaraḥ prathamaḥ pādaḥ || 3 ||*

**Translation.** The first quarter is Vaishvanara, "the one common to all
people". Its home is the waking state. Its awareness faces outward. It has
seven limbs and nineteen mouths, and it feeds on the solid world.

**Hard words**

* **Jagarita-sthana** (*jāgarita-sthāna*): "whose place is waking".
* **Bahish-prajna** (*bahiṣ-prajña*): "aware of the outside".
* **Sapta-anga** (*saptāṅga*): "seven-limbed". The text does not list the
  seven. Shankara explains them from an older passage (*Chandogya
  Upanishad* 5.18.2) that pictures the universe as one cosmic person: the
  sky as the head, the sun as the eye, the wind as the breath, space as
  the trunk, water as the bladder, the earth as the feet, and the sacred
  fire as the mouth.
* **Ekonavimshati-mukha** (*ekonaviṃśati-mukha*): "nineteen-mouthed"
  (literally "twenty-less-one"). Again the text gives no list. Shankara
  counts them as the ways we take in and act on the world: the five
  senses, the five powers of action (speech, handling, moving, excreting,
  reproducing), the five vital breaths, and the mind, the intellect, the
  sense of "I", and memory or thought.
* **Sthula-bhuk** (*sthūla-bhuj*): "eater of the gross". *Sthūla* means
  solid, coarse, physical: things you can bump into.
* **Vaishvanara** (*vaiśvānara*): from *viśva* "all" and *nara* "person":
  "belonging to all people". The waking world is the one we all share.

**What it is saying.** This is you, now, awake. Your attention points
outward at a physical world. You take that world in through many
"mouths", your senses and faculties, and you "feed" on it: you see it,
touch it, use it. This state is called "common to all" because the waking
world is the one place where everyone meets.

**A modern picture.** Think of a computer's input ports: keyboard, mouse,
camera, microphone, network cable. The nineteen "mouths" are the ports
through which the waking world streams in. And the waking world is like an
online game with a shared server: you and millions of others log into the
*same* world, see the same street, and can bump into each other there.

---

### Mantra 4: The second quarter, the dreamer

> स्वप्नस्थानोऽन्तःप्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः प्रविविक्तभुक्तैजसो द्वितीयः पादः ॥ ४ ॥

> *svapnasthāno'ntaḥprajñaḥ saptāṅga ekonaviṃśatimukhaḥ
> praviviktabhuktaijaso dvitīyaḥ pādaḥ || 4 ||*

**Translation.** The second quarter is Taijasa, "the shining one". Its
home is the dream state. Its awareness faces inward. It has seven limbs
and nineteen mouths, and it feeds on the subtle world.

**Hard words**

* **Svapna-sthana** (*svapna-sthāna*): "whose place is dream".
* **Antah-prajna** (*antaḥ-prajña*): "aware of the inside".
* **Pravivikta-bhuk** (*pravivikta-bhuj*): "eater of the fine, the
  separate". The objects of a dream are made of mind-stuff alone, finer
  than solid things and set apart from the outer world.
* **Taijasa**: from *tejas*, "light, brilliance". In a dream there is no
  sun, yet the scenes are lit. The mind supplies its own light.

**What it is saying.** When you dream, your awareness turns inward. You
still have a body in the dream, and you still see, hear, walk and talk:
the same "seven limbs and nineteen mouths". But everything you meet is
made by your own mind, and lit by your own mind.

**A modern picture.** A dream is like a virtual-reality headset where your
own mind is the headset, the game designer, the graphics card *and* the
player. You can drive a car you don't own through a city that doesn't
exist, meet people who never lived, and it all feels completely real until
you wake. And unlike the shared server of waking life, this game runs on
one machine only: nobody else can enter your dream.

---

### Mantra 5: The third quarter, deep sleep

> यत्र सुप्तो न कञ्चन कामं कामयते न कञ्चन स्वप्नं पश्यति तत्सुषुप्तम् ।
> सुषुप्तस्थान एकीभूतः प्रज्ञानघन एवानन्दमयो ह्यानन्दभुक्चेतोमुखः प्राज्ञस्तृतीयः पादः ॥ ५ ॥

> *yatra supto na kañcana kāmaṃ kāmayate na kañcana svapnaṃ paśyati
> tatsuṣuptam | suṣuptasthāna ekībhūtaḥ prajñānaghana evānandamayo
> hyānandabhukcetomukhaḥ prājñastṛtīyaḥ pādaḥ || 5 ||*

**Translation.** Deep sleep is when the sleeper wants nothing at all and
sees no dream at all. The third quarter is Prajna, "the knowing one". Its
home is deep sleep. In it everything has become one. It is simply a solid
mass of awareness. It is made of bliss, and it tastes bliss. Awareness is
its mouth.

**Hard words**

* **Sushupta** (*suṣupta*): "deep sleep", sleep with no dreams.
* **Ekibhuta** (*ekībhūta*): "become one". The many things of waking and
  dream have all melted together.
* **Prajnana-ghana** (*prajñāna-ghana*): "a mass of awareness". *Ghana*
  means solid, dense, packed together, as in a thick cloud. Nothing is
  separate or picked out. It is awareness with no *object*.
* **Ananda-maya** (*ānanda-maya*): "made of bliss"; **ananda-bhuk**
  (*ānanda-bhuj*): "enjoyer of bliss". *Ānanda* is deep joy or ease, not
  excitement.
* **Cheto-mukha** (*ceto-mukha*): "whose mouth is awareness". Two readings
  are possible. Plainly, it takes in nothing but awareness itself.
  Shankara reads *mukha* as "doorway": deep sleep is the door through
  which awareness goes out again into dream and waking.
* **Prajna** (*prājña*): "the knowing one". The name is a little
  surprising, since in deep sleep we don't know anything. The point is
  that awareness is still there, only with nothing in front of it.

**What it is saying.** In dreamless sleep, desire stops and pictures stop.
You are not *nothing*: you are awareness with all the furniture removed.
And it feels good. Everyone longs for deep sleep, and no one complains of
having slept too well. This mantra says that ease comes from what you are,
not from anything you had.

**A modern picture.** Think of a laptop with its lid closed. Every file
and program is still there, saved, but nothing is open on the screen and
nothing is running in front of you. Open the lid and the whole desktop
springs back. And there is a famous point for reflection that teachers of
this text have long used: when you wake from a deep sleep you say, "I
slept so well, I knew nothing at all." But if you were not there, who
noticed that you knew nothing?

---

### Mantra 6: What the third quarter really is

> एष सर्वेश्वर एष सर्वज्ञ एषोऽन्तर्याम्येष योनिः सर्वस्य प्रभवाप्ययौ हि भूतानाम् ॥ ६ ॥

> *eṣa sarveśvara eṣa sarvajña eṣo'ntaryāmyeṣa yoniḥ sarvasya
> prabhavāpyayau hi bhūtānām || 6 ||*

**Translation.** This is the lord of all. This is the knower of all. This
is the controller within. This is the womb of everything, for it is where
beings come from and where they go back to.

**Hard words**

* **Sarveshvara** (*sarveśvara*): "lord of all".
* **Sarvajna** (*sarvajña*): "all-knowing".
* **Antaryami** (*antaryāmin*): "the inner controller", the one who
  guides every being from inside.
* **Yoni**: "womb, source, birthplace".
* **Prabhava-apyaya** (*prabhava-apyaya*): "coming forth and going back",
  origin and dissolution.

**What it is saying.** "This" points back to the third quarter, the
deep-sleep Self. That can seem strange: how can deep sleep be the lord of
all? Think about what happens every morning. Your dream-world and your
waking world both spring out of deep sleep, and at night they both sink
back into it. On the scale of the universe, the same seed-state is where
all beings come from and where they return. Seen that way, it is the
source and the ruler of everything that unfolds from it. Shankara reads
this as the Self in its role as God, the cause of the world.

**A modern picture.** A seed and a tree. The whole oak, with every leaf
and branch, is folded up in the acorn, not yet spread out. The acorn is
the "womb" of the tree. The third quarter is like the acorn of both your
dream-world and your waking world.

---

### Mantra 7: The Fourth

> नान्तःप्रज्ञं न बहिष्प्रज्ञं नोभयतःप्रज्ञं न प्रज्ञानघनं न प्रज्ञं नाप्रज्ञम् ।
> अदृष्टमव्यवहार्यमग्राह्यमलक्षणमचिन्त्यमव्यपदेश्यमेकात्मप्रत्ययसारं प्रपञ्चोपशमं शान्तं शिवमद्वैतं चतुर्थं मन्यन्ते स आत्मा स विज्ञेयः ॥ ७ ॥

> *nāntaḥprajñaṃ na bahiṣprajñaṃ nobhayataḥprajñaṃ na prajñānaghanaṃ na
> prajñaṃ nāprajñam | adṛṣṭamavyavahāryamagrāhyamalakṣaṇamacintyam
> avyapadeśyamekātmapratyayasāraṃ prapañcopaśamaṃ śāntaṃ śivamadvaitaṃ
> caturthaṃ manyante sa ātmā sa vijñeyaḥ || 7 ||*

**Translation.** It is not aware of what is inside, not aware of what is
outside, and not aware of both together. It is not a mass of awareness. It
is not knowing, and it is not unknowing. It cannot be seen. It cannot be
used or dealt with. It cannot be grasped. It has no marks to know it by.
It cannot be thought of. It cannot be put into words. Its very substance
is the sure sense of one single Self. In it the spread-out world falls
still. It is peace. It is good. It is one without a second. This is what
the wise take to be the Fourth. That is the Self. That is what is to be
known.

**Hard words**

* **Na ... na ... na**: "not ... not ... not". The first six phrases say
  what the Fourth is *not*: not the dreamer (aware inside), not the waker
  (aware outside), not the in-between state of half-waking, not deep
  sleep (the mass of awareness), not a knower of things, and not a blank
  unconscious lump either.
* **Avyavaharya** (*avyavahārya*): "not open to dealings". You cannot pick
  it up, trade it, point at it, or do anything with it.
* **Alakshana** (*alakṣaṇa*): "without marks". It has no colour, shape,
  size or feature by which to recognise it.
* **Avyapadeshya** (*avyapadeśya*): "that cannot be named or pointed out".
* **Ekatma-pratyaya-sara** (*ekātma-pratyaya-sāra*): "whose essence is the
  sense of the one Self". Shankara explains: in waking, dream and sleep
  there is always the same one "I am", and that single, unbroken
  awareness is how the Fourth is known.
* **Prapancha-upashama** (*prapañca-upaśama*): "the stilling of the
  spread-out world". *Prapañca* is the world spread out into many; the
  word is related to "five" (*pañca*), and is often linked to the five
  elements. *Upaśama* is "calming, going quiet".
* **Shanta** (*śānta*): "at peace". **Shiva** (*śiva*): "good, blessed,
  kind". **Advaita**: "not two".
* **Chaturtha** (*caturtha*): "the fourth". The famous word *turīya*,
  also "fourth", is **not** used in the Mandukya itself. It comes from
  later writers, including Gaudapada.
* **Manyante**: "they consider, they think of it as". The text is
  reporting what the wise hold.

**What it is saying.** This is the heart of the Upanishad. The Fourth is
not a fourth *state* that comes after sleep, like a fourth room at the end
of a corridor. It is what was present in all three rooms all along: the
bare awareness in which waking, dreaming and sleeping come and go.

That is why the text describes it almost entirely by saying "not". Any
description would turn it into an object, something seen, and it is the
one that does the seeing. So the text strips away every label until only
the Self is left. And then it ends with a command in two words: *sa
vijñeyaḥ*, "that is to be known". Everything before this was the map. This
is the place the map points to.

**A modern picture.** Think of a cinema screen. The film shows a fire, and
the screen does not burn. It shows a flood, and the screen does not get
wet. It shows a night scene, and the screen does not go dark in itself.
The screen is not one of the scenes. It is what every scene appears on.
When the film ends, the screen is still there.

Or think of a string of pearls. The pearls are waking, dreaming and
sleeping. The thread runs through every pearl, holds them all together,
and is hidden by them. The *Bhagavad Gita* (7.7) uses this same image:
"All this is strung on me, like pearls on a thread." The Fourth is the
thread.

---

### Mantra 8: The Self as the sound Om

> सोऽयमात्माध्यक्षरमोङ्कारोऽधिमात्रं पादा मात्रा मात्राश्च पादा अकार उकारो मकार इति ॥ ८ ॥

> *so'yamātmādhyakṣaramoṅkāro'dhimātraṃ pādā mātrā mātrāśca pādā akāra
> ukāro makāra iti || 8 ||*

**Translation.** This same Self, taken as a syllable, is Om. Taken part by
part: the quarters are the parts, and the parts are the quarters. The
parts are the sound A, the sound U, and the sound M.

**Hard words**

* **Adhyakshara** (*adhyakṣara*): "with regard to the syllable", looking
  at the Self in terms of sound.
* **Adhimatra** (*adhimātra*): "with regard to the measures", looking at
  it part by part.
* **Matra** (*mātrā*): a measure, a unit of sound.
* **Akara, ukara, makara** (*akāra, ukāra, makāra*): "the sound A", "the
  sound U", "the sound M". *-kāra* just means "the sound of".

**What it is saying.** Now the Upanishad joins its two themes, Om and the
Self. In Sanskrit, when A and U meet, they blend into O, so "A-U-M" is
spoken as "Om". The text matches each sound to one of the quarters.
Mantras 9 to 12 go through them one by one.

**A modern picture.** Try it. Say "Om" very slowly: "aaa ... ooo ...
mmm". Notice your mouth. On A it is open. On U it rounds and moves
forward. On M the lips close and the sound hums inside. Then, when the
sound stops, there is silence. Four things: three sounds and the silence
after them. Keep that in mind for the next four mantras.

---

### Mantra 9: A is the waker

> जागरितस्थानो वैश्वानरोऽकारः प्रथमा मात्राऽऽप्तेरादिमत्त्वाद्वाऽऽप्नोति ह वै सर्वान्कामानादिश्च भवति य एवं वेद ॥ ९ ॥

> *jāgaritasthāno vaiśvānaro'kāraḥ prathamā mātrā''pterādimattvādvā''pnoti
> ha vai sarvānkāmānādiśca bhavati ya evaṃ veda || 9 ||*

**Translation.** Vaishvanara, whose home is waking, is the sound A, the
first part. This is because A reaches everywhere, or because A comes
first. Whoever knows this reaches all their desires and becomes first.

**Hard words**

* **Apti** (*āpti*): "reaching, pervading, getting".
* **Adimattva** (*ādimattva*): "being first, having a beginning".
* **Ya evam veda** (*ya evaṃ veda*): "whoever knows this". A stock phrase
  in the Vedas, used to announce the reward that comes from a piece of
  knowledge.

**What it is saying.** The text plays on sounds, as the Vedas often do.
The reasons it gives for A both start with A: *āpti*, "reaching", and
*ādi*, "first". A reaches everywhere: in Sanskrit script every consonant
carries a built-in A (*ka*, *ga*, *ta* ...), so A is hidden in almost
every sound you make. And A is first: it is the first letter of the
Sanskrit alphabet. In the *Bhagavad Gita* (10.33), Krishna says, "Among
letters, I am A."

The waking state is like that. It is the first state, the one we take as
the starting point, and it seems to reach everywhere. The promise at the
end is a traditional "fruit" statement. It says what the one who
understands this will gain.

**A modern picture.** A is the first letter not only in Sanskrit but in
the Greek, Latin and English alphabets too. It is also the first sound
most of us make when we open our mouths without shaping them, as in "ah"
at the doctor's. The waking world is like that "ah": the open, default,
first setting.

---

### Mantra 10: U is the dreamer

> स्वप्नस्थानस्तैजस उकारो द्वितीया मात्रोत्कर्षादुभयत्वाद्वोत्कर्षति ह वै ज्ञानसन्ततिं समानश्च भवति नास्याब्रह्मवित्कुले भवति य एवं वेद ॥ १० ॥

> *svapnasthānastaijasa ukāro dvitīyā mātrotkarṣādubhayatvādvotkarṣati ha
> vai jñānasantatiṃ samānaśca bhavati nāsyābrahmavitkule bhavati ya evaṃ
> veda || 10 ||*

**Translation.** Taijasa, whose home is dream, is the sound U, the second
part. This is because U is raised higher, or because U stands between the
two. Whoever knows this raises the flow of knowledge higher and becomes
balanced. In their family no one is born who does not know Brahman.

**Hard words**

* **Utkarsha** (*utkarṣa*): "raising up, being higher". U comes after A
  and is, in that sense, a step above it; dream is a finer, more inward
  state than waking.
* **Ubhayatva** (*ubhayatva*): "being of both", standing in the middle.
  U sits between A and M, just as dream sits between waking and deep
  sleep.
* **Jnana-santati** (*jñāna-santati*): "the stream of knowledge", knowledge
  that flows on and continues.
* **Samana** (*samāna*): "equal, the same, even". The text does not say
  equal to what. It can be read as "even-minded", or as "treated as an
  equal by everyone". This translation takes the first.
* **Abrahmavit** (*abrahmavid*): "one who does not know Brahman".

**What it is saying.** Again the reasons sound like the letter: *utkarṣa*
and *ubhaya* both start with U. Dream is the middle state. It borrows its
pictures from waking and melts back into sleep, so it is a bridge between
the two. The reward promised is a spiritual one: understanding grows and
is handed on, so that wisdom runs in the family.

**A modern picture.** U is like the middle layer of a sandwich, or the
middle stop on a train line. You cannot get from waking to deep sleep
without passing through the dream-station, however briefly. And
"knowledge flowing on in the family" is like a household where the love of
learning is passed down, so that every child grows up with it.

---

### Mantra 11: M is deep sleep

> सुषुप्तस्थानः प्राज्ञो मकारस्तृतीया मात्रा मितेरपीतेर्वा मिनोति ह वा इदं सर्वमपीतिश्च भवति य एवं वेद ॥ ११ ॥

> *suṣuptasthānaḥ prājño makārastṛtīyā mātrā miterapītervā minoti ha vā
> idaṃ sarvamapītiśca bhavati ya evaṃ veda || 11 ||*

**Translation.** Prajna, whose home is deep sleep, is the sound M, the
third part. This is because M measures, or because in M everything merges.
Whoever knows this measures all this world and becomes the place where it
merges.

**Hard words**

* **Miti**: "measuring". **Minoti**: "measures".
* **Apiti** (*apīti*): "going into, merging, dissolving".

**What it is saying.** The word-play is *miti*, "measuring", which starts
with M. Shankara gives a vivid explanation. When you chant "Om" again and
again, A and U seem to go *into* M as the lips close, and come *out* of it
again as the next Om begins. It is like grain being poured into a
measuring pot and poured out again. Deep sleep does the same with the
waking and dream worlds: every night they pour into it, and every morning
they pour out.

The one who understands this "measures" the world, meaning they see it
for what it is, and becomes the place where it is gathered in.

**A modern picture.** Think of pressing "save and close" on every open
window. All the work is gathered up and folded into one place, and
nothing is lost. The closing M, with the lips shut and the sound humming
inside, is that gathering.

---

### Mantra 12: The silence after Om

> अमात्रश्चतुर्थोऽव्यवहार्यः प्रपञ्चोपशमः शिवोऽद्वैत एवमोङ्कार आत्मैव संविशत्यात्मनाऽऽत्मानं य एवं वेद ॥ १२ ॥

> *amātraścaturtho'vyavahāryaḥ prapañcopaśamaḥ śivo'dvaita evamoṅkāra
> ātmaiva saṃviśatyātmanā''tmānaṃ ya evaṃ veda || 12 ||*

**Translation.** The Fourth has no parts. It cannot be dealt with. In it
the spread-out world falls still. It is good, and it is one without a
second. So Om is the Self itself. Whoever knows this, by their own self
enters the Self.

**Hard words**

* **Amatra** (*amātra*): "without measure, without parts". The Fourth is
  not a fourth letter. It has no sound of its own.
* **Samvishati** (*saṃviśati*): "enters, goes home into, merges".
* **Atmana atmanam** (*ātmanā ātmānam*): "by the Self, into the Self".

**What it is saying.** The three sounds A, U and M match waking, dream and
sleep. The Fourth matches no sound. It is the silence out of which Om
rises and back into which it falls. So the whole of Om, sounds and silence
together, *is* the Self.

The last line is striking. The knower does not travel anywhere or become
anything new. They enter the Self *by* the Self, like a wave settling
back into the ocean it never left. In recitation the final words *ya evaṃ
veda*, "whoever knows this", are usually said twice, to mark the end of
the text.

**A modern picture.** Strike a bell. It rings, the sound swells, fades,
and then there is silence. That silence is not "nothing". It was there
before the bell was struck, it held the whole ring from start to finish,
and it is still there after. Nothing you do to the bell can break it. The
Upanishad's last word is that the silence is what you are.

---

## The whole map in one table

| Quarter | Name | State | Awareness | Feeds on | Sound |
|---|---|---|---|---|---|
| 1st | Vaishvanara, "common to all" | Waking | Faces outward | The solid world | **A** |
| 2nd | Taijasa, "the shining one" | Dreaming | Faces inward | The subtle, mind-made world | **U** |
| 3rd | Prajna, "the knowing one" | Deep sleep | A single mass of awareness | Bliss | **M** |
| The Fourth | (no name given) | Not a state: present in all three | Neither inward, outward nor massed | Nothing: the world falls still here | **Silence** |

---

## The translation straight through

For reading without the notes.

1. Om: this sound is all that is. Here is a closer account of it. What has
   been, what is, and what will be: all of it is simply Om. And whatever
   else there is, beyond these three times, that too is simply Om.
2. All this is Brahman. This Self is Brahman. And this Self has four
   quarters.
3. The first quarter is Vaishvanara, "the one common to all people". Its
   home is the waking state. Its awareness faces outward. It has seven
   limbs and nineteen mouths, and it feeds on the solid world.
4. The second quarter is Taijasa, "the shining one". Its home is the dream
   state. Its awareness faces inward. It has seven limbs and nineteen
   mouths, and it feeds on the subtle world.
5. Deep sleep is when the sleeper wants nothing at all and sees no dream
   at all. The third quarter is Prajna, "the knowing one". Its home is
   deep sleep. In it everything has become one. It is simply a solid mass
   of awareness. It is made of bliss, and it tastes bliss. Awareness is its
   mouth.
6. This is the lord of all. This is the knower of all. This is the
   controller within. This is the womb of everything, for it is where
   beings come from and where they go back to.
7. It is not aware of what is inside, not aware of what is outside, and
   not aware of both together. It is not a mass of awareness. It is not
   knowing, and it is not unknowing. It cannot be seen. It cannot be used
   or dealt with. It cannot be grasped. It has no marks to know it by. It
   cannot be thought of. It cannot be put into words. Its very substance
   is the sure sense of one single Self. In it the spread-out world falls
   still. It is peace. It is good. It is one without a second. This is
   what the wise take to be the Fourth. That is the Self. That is what is
   to be known.
8. This same Self, taken as a syllable, is Om. Taken part by part: the
   quarters are the parts, and the parts are the quarters. The parts are
   the sound A, the sound U, and the sound M.
9. Vaishvanara, whose home is waking, is the sound A, the first part.
   This is because A reaches everywhere, or because A comes first.
   Whoever knows this reaches all their desires and becomes first.
10. Taijasa, whose home is dream, is the sound U, the second part. This is
    because U is raised higher, or because U stands between the two.
    Whoever knows this raises the flow of knowledge higher and becomes
    balanced. In their family no one is born who does not know
    Brahman.
11. Prajna, whose home is deep sleep, is the sound M, the third part. This
    is because M measures, or because in M everything merges. Whoever
    knows this measures all this world and becomes the place where it
    merges.
12. The Fourth has no parts. It cannot be dealt with. In it the spread-out
    world falls still. It is good, and it is one without a second. So Om
    is the Self itself. Whoever knows this, by their own self enters the
    Self.

---

## Things people often get wrong

* **"Turiya" is not in the text.** The Mandukya calls the Fourth simply
  *caturtha*, "the fourth". *Turīya* comes from later writers.
* **Gaudapada's Karika is not the Upanishad.** The 215 verses of the
  *Mandukya Karika* are a separate commentary-poem, printed alongside it.
* **The lists of "seven limbs" and "nineteen mouths" are not in the
  text.** The Upanishad gives only the numbers. The lists come from
  Shankara's commentary.
* **The Fourth is not a fourth state.** The text says it is *not* like any
  of the three. It is what is present through them.
* **The name.** *Māṇḍūkya* is the name of a Vedic line of teachers.
  *Maṇḍūka* does mean "frog", and popular accounts sometimes build a story
  on that, but the Upanishad itself says nothing about frogs.

---

## Translation choices

A few places where the Sanskrit allows more than one fair reading, and
what this translation chose.

* **Mantra 1, *akṣara*:** "sound" or "syllable" in the translation; the
  second meaning, "imperishable", is explained in the notes.
* **Mantra 5, *cetomukha*:** "awareness is its mouth", the literal
  reading; Shankara's "doorway" reading is given in the notes.
* **Mantra 7, *manyante*:** "what the wise take to be". The verb only
  says "they consider"; "the wise" makes the unnamed subject clear.
* **Mantra 7, *ekātma-pratyaya-sāra*:** "its very substance is the sure
  sense of one single Self". *Pratyaya* can mean a thought, a firm
  conviction, or a means of knowing.
* **Mantra 10, *samāna*:** "balanced", in the sense of even-minded; the
  other reading, "treated as an equal", is given in the notes.
* **Mantra 12, *saṃviśaty ātmanā ''tmānam*:** "by their own self enters
  the Self". The same word *ātman* serves both as "one's own self" and
  "the Self"; the capital letter marks the second.
* **"They/their"** is used for "whoever knows this" where the Sanskrit
  uses the grammatical masculine for any person.

---

## Sources

* Sanskrit text: the standard twelve-mantra text of the Mandukya
  Upanishad, as commented on by Shankara; checked against the copies at
  sanskritdocuments.org (encoded by M. Giridhar, proofread by John
  Manetta) and shlokam.org. The Sanskrit is ancient and free of
  copyright.
* Peace chant: Rigveda 1.89.8–9, assigned to the Atharvaveda Upanishads
  in the *Muktika Upanishad*.
* Traditional explanations are credited to Shankara's commentary
  (*Māṇḍūkya Upaniṣad Bhāṣya*) where they are used.
* Other passages quoted: *Chandogya Upanishad* 5.18.2; *Bhagavad Gita*
  7.7 and 10.33; *Muktika Upanishad* 1.26.
* The English translation and all explanations are original to this
  repository.
