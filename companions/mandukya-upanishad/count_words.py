#!/usr/bin/env python3
"""Count the Mandukya Upanishad in verses and words.

The Sanskrit below is the standard text of the twelve mantras (the one
Shankara comments on), cross-checked against two independent online
copies. "Hariḥ om" at the start and the peace chant are recitation
formulas, not part of the twelve mantras, so they are not counted.

Two word counts are given because Sanskrit glues words together:
  * written words: what you see between spaces in Devanagari;
  * separate words: the same text with the sound-joins (sandhi) undone,
    compounds kept whole, as listed in PADAS below.

Optional: `pip install indic_transliteration` to print IAST.
"""

MANTRAS = [
    "ओमित्येतदक्षरमिदं सर्वं तस्योपव्याख्यानं भूतं भवद्भविष्यदिति सर्वमोङ्कार एव । यच्चान्यत्त्रिकालातीतं तदप्योङ्कार एव ॥",
    "सर्वं ह्येतद्ब्रह्मायमात्मा ब्रह्म सोऽयमात्मा चतुष्पात् ॥",
    "जागरितस्थानो बहिष्प्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः स्थूलभुग्वैश्वानरः प्रथमः पादः ॥",
    "स्वप्नस्थानोऽन्तःप्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः प्रविविक्तभुक्तैजसो द्वितीयः पादः ॥",
    "यत्र सुप्तो न कञ्चन कामं कामयते न कञ्चन स्वप्नं पश्यति तत्सुषुप्तम् । सुषुप्तस्थान एकीभूतः प्रज्ञानघन एवानन्दमयो ह्यानन्दभुक्चेतोमुखः प्राज्ञस्तृतीयः पादः ॥",
    "एष सर्वेश्वर एष सर्वज्ञ एषोऽन्तर्याम्येष योनिः सर्वस्य प्रभवाप्ययौ हि भूतानाम् ॥",
    "नान्तःप्रज्ञं न बहिष्प्रज्ञं नोभयतःप्रज्ञं न प्रज्ञानघनं न प्रज्ञं नाप्रज्ञम् । अदृष्टमव्यवहार्यमग्राह्यमलक्षणमचिन्त्यमव्यपदेश्यमेकात्मप्रत्ययसारं प्रपञ्चोपशमं शान्तं शिवमद्वैतं चतुर्थं मन्यन्ते स आत्मा स विज्ञेयः ॥",
    "सोऽयमात्माध्यक्षरमोङ्कारोऽधिमात्रं पादा मात्रा मात्राश्च पादा अकार उकारो मकार इति ॥",
    "जागरितस्थानो वैश्वानरोऽकारः प्रथमा मात्राऽऽप्तेरादिमत्त्वाद्वाऽऽप्नोति ह वै सर्वान्कामानादिश्च भवति य एवं वेद ॥",
    "स्वप्नस्थानस्तैजस उकारो द्वितीया मात्रोत्कर्षादुभयत्वाद्वोत्कर्षति ह वै ज्ञानसन्ततिं समानश्च भवति नास्याब्रह्मवित्कुले भवति य एवं वेद ॥",
    "सुषुप्तस्थानः प्राज्ञो मकारस्तृतीया मात्रा मितेरपीतेर्वा मिनोति ह वा इदं सर्वमपीतिश्च भवति य एवं वेद ॥",
    "अमात्रश्चतुर्थोऽव्यवहार्यः प्रपञ्चोपशमः शिवोऽद्वैत एवमोङ्कार आत्मैव संविशत्यात्मनाऽऽत्मानं य एवं वेद ॥",
]

# The same text with sandhi undone (compounds kept as one word).
PADAS = [
    "om iti etat akṣaram idam sarvam tasya upavyākhyānam bhūtam bhavat bhaviṣyat iti sarvam oṅkāraḥ eva yat ca anyat trikālātītam tat api oṅkāraḥ eva",
    "sarvam hi etat brahma ayam ātmā brahma saḥ ayam ātmā catuṣpāt",
    "jāgaritasthānaḥ bahiṣprajñaḥ saptāṅgaḥ ekonaviṃśatimukhaḥ sthūlabhuk vaiśvānaraḥ prathamaḥ pādaḥ",
    "svapnasthānaḥ antaḥprajñaḥ saptāṅgaḥ ekonaviṃśatimukhaḥ praviviktabhuk taijasaḥ dvitīyaḥ pādaḥ",
    "yatra suptaḥ na kañcana kāmam kāmayate na kañcana svapnam paśyati tat suṣuptam suṣuptasthānaḥ ekībhūtaḥ prajñānaghanaḥ eva ānandamayaḥ hi ānandabhuk cetomukhaḥ prājñaḥ tṛtīyaḥ pādaḥ",
    "eṣaḥ sarveśvaraḥ eṣaḥ sarvajñaḥ eṣaḥ antaryāmī eṣaḥ yoniḥ sarvasya prabhavāpyayau hi bhūtānām",
    "na antaḥprajñam na bahiṣprajñam na ubhayataḥprajñam na prajñānaghanam na prajñam na aprajñam adṛṣṭam avyavahāryam agrāhyam alakṣaṇam acintyam avyapadeśyam ekātmapratyayasāram prapañcopaśamam śāntam śivam advaitam caturtham manyante saḥ ātmā saḥ vijñeyaḥ",
    "saḥ ayam ātmā adhyakṣaram oṅkāraḥ adhimātram pādāḥ mātrāḥ mātrāḥ ca pādāḥ akāraḥ ukāraḥ makāraḥ iti",
    "jāgaritasthānaḥ vaiśvānaraḥ akāraḥ prathamā mātrā āpteḥ ādimattvāt vā āpnoti ha vai sarvān kāmān ādiḥ ca bhavati yaḥ evam veda",
    "svapnasthānaḥ taijasaḥ ukāraḥ dvitīyā mātrā utkarṣāt ubhayatvāt vā utkarṣati ha vai jñānasantatim samānaḥ ca bhavati na asya abrahmavit kule bhavati yaḥ evam veda",
    "suṣuptasthānaḥ prājñaḥ makāraḥ tṛtīyā mātrā miteḥ apīteḥ vā minoti ha vā idam sarvam apītiḥ ca bhavati yaḥ evam veda",
    "amātraḥ caturthaḥ avyavahāryaḥ prapañcopaśamaḥ śivaḥ advaitaḥ evam oṅkāraḥ ātmā eva saṃviśati ātmanā ātmānam yaḥ evam veda",
]


def written(text):
    return [w for w in text.split() if w not in ("।", "॥")]


def main():
    tw = tp = 0
    print(f"{'Mantra':>6} {'written':>8} {'separate':>9}")
    for i, (m, p) in enumerate(zip(MANTRAS, PADAS), 1):
        w, s = len(written(m)), len(p.split())
        tw, tp = tw + w, tp + s
        print(f"{i:>6} {w:>8} {s:>9}")
    print(f"{'Total':>6} {tw:>8} {tp:>9}")
    try:
        from indic_transliteration import sanscript as s
        print()
        for i, m in enumerate(MANTRAS, 1):
            print(i, s.transliterate(m, s.DEVANAGARI, s.IAST))
    except ImportError:
        pass


if __name__ == "__main__":
    main()
