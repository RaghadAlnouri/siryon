"""
Project Siryon Data & Dialect Corpus Module
Western Neo-Aramaic Dialects: Maaloula (Christian/Monastic), Jubb'adin (Oral Poetry), Bakh'a (Archaic Mountain)
In partnership with Enable Syria (go/enable-syria) & Heidelberg University MASC Speech Corpus.
"""

# Tri-Dialect Phrasebook Corpus
PHRASEBOOK_CORPUS = {
    "welcome_village": {
        "title": "Welcome to our village of sweets / Peace upon your arrival",
        "category": "Hospitality & Greetings",
        "english_literal": "In peace you have come to our village of sweet springs",
        "semitic_root_summary": "√š-y-n (Peace) • √ʔ-t-y (Come) • √q-r-y (Village) • √ḥ-l-w (Sweet)",
        "dialects": {
            "maaloula": {
                "name": "Maaloula (Christian / Monastic)",
                "sub_label": "Eastern Qalamoun • Monastic Substrate • Retains /ṯ/ & /ḏ/",
                "syriac_script": "ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ",
                "adapted_arabic": "بْشَيْنا تِيتُن لْقَرْيِتْنا حَلْواتا",
                "ipa": "/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/",
                "phonological_note": "Preserves historical voiceless interdental /ṯ/ in qaryēṯan (village) and word-initial prosthetic glottal stop /ʔb-/ before labials.",
                "audio_hint": "b-šay-na  tē-tun  l-qar-yē-ṯan  ḥal-wā-ta",
                "badge": "Monastic Standard"
            },
            "jubbadin": {
                "name": "Jubb'adin (Oral Poetry & Agrarian)",
                "sub_label": "Central Qalamoun • Poetic Cadence • /ṯ/ → /t/ Shift",
                "syriac_script": "ܒܫܰܝܢܳܐ ܐܶܬܰܝܬܽܘܢ ܠܩܰܪܝܶܬܰܢ ܚܰܠܘܳܬܳܐ",
                "adapted_arabic": "بشَيْنا إتَيْتُن لْقَرْيَتا حَلْواتا",
                "ipa": "/b-ˈʃajna ʔiˈtajtun l-qarˈjata ˈħalwata/",
                "phonological_note": "Spirantized /ṯ/ merges cleanly into stop /t/ (qaryata); strong stress on penultimate rhyming syllable characteristic of Ataba oral folk song.",
                "audio_hint": "b-šay-na  i-tay-tun  l-qar-ya-ta  ḥal-wā-ta",
                "badge": "Poetic Register"
            },
            "bakha": {
                "name": "Bakh'a (Archaic Mountain)",
                "sub_label": "High Altitude Qalamoun • Archaic Vowel Quality",
                "syriac_script": "ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܳܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ",
                "adapted_arabic": "بْشَيْنا إتَيْتون لْقَرْيوتَن حَلْواتا",
                "ipa": "/b-ˈʃajna ʔiˈtajtuːn l-qarˈjoːtʰan ˈħalwaːtʰa/",
                "phonological_note": "Archaic Canaanite-Aramaic back vowel shift /ā/ → /ō/ in pl./feminine nouns (qaryōṯan) preserved at 1,500m elevation.",
                "audio_hint": "b-šay-na  i-tay-tūn  l-qar-yō-ṯan  ḥal-wā-ṯa",
                "badge": "Archaic Mountain"
            }
        },
        "tokens_breakdown": [
            {"Token": "b-šayna", "Morpheme": "b- (in) + šayn-a (peace)", "Root": "√š-y-n (ܫܝܢ)", "Cognate": "Syr: ܒܫܝܢܐ | Heb: בְּשָׁלוֹם / שַׁלְוָה | Arab: بِسَلامة", "Status": "Verified"},
            {"Token": "ṯētun / itaytun", "Morpheme": "√ʔ-t-y (come) - 2nd Pl. Perf", "Root": "√ʔ-t-y (ܐܬܝ)", "Cognate": "Syr: ܐܬܝܬܘܢ | Arab: أَتَيْتُمْ | Heb: אֲתָאתֶם", "Status": "Verified"},
            {"Token": "l-qaryēṯan", "Morpheme": "l- (to) + qary-ēṯ-an (our village)", "Root": "√q-r-y (ܩܪܝ)", "Cognate": "Syr: ܠܩܪܝܬܐ | Arab: لِقَرْيَة | Heb: קִרְיָה", "Status": "Verified"},
            {"Token": "ḥalwāta", "Morpheme": "ḥalw-āṯ-a (sweets / fresh springs)", "Root": "√ḥ-l-w (ܚܠܘ)", "Cognate": "Syr: ܚܠܘܬܐ | Arab: حَلاوَة / حُلْوَى | Heb: חָלָב / חָלוּב", "Status": "Verified"}
        ]
    },
    "olive_harvest": {
        "title": "The ancient olive tree gave its oil upon the terrace",
        "category": "Agriculture & Terraced Groves",
        "english_literal": "The ancient olive tree poured its green oil from the rocky mountain slope",
        "semitic_root_summary": "√z-y-t (Olive/Oil) • √ṭ-w-r (Mountain) • √k-r-m (Vineyard/Grove)",
        "dialects": {
            "maaloula": {
                "name": "Maaloula (Christian / Monastic)",
                "sub_label": "Eastern Qalamoun",
                "syriac_script": "ܙܰܝܬܳܐ ܥܰܬܺܝܩܳܐ ܝܰܗܒ݂ ܡܫܚܶܗ ܥܰܠ ܛܽܘܪܳܐ",
                "adapted_arabic": "زَيْتا عَتِيقا يَھْب مِشْحِه عَل طُورا",
                "ipa": "/ˈzajta ʕaˈtʰiːqa ˈjaħb ˈmɪʃħeħ ʕal ˈtˤuːra/",
                "phonological_note": "Preserves Classical Aramaic mešḥā (oil) alongside zaytā (olive tree), distinct from Levantine Arabic zayt.",
                "audio_hint": "zay-ta  a-tī-qa  yahb  mish-heh  al  ṭū-ra",
                "badge": "Monastic Standard"
            },
            "jubbadin": {
                "name": "Jubb'adin (Oral Poetry & Agrarian)",
                "sub_label": "Central Qalamoun",
                "syriac_script": "ܙܰܝܬܳܐ ܕܩܰܠܰܡܽܘܢ ܐܰܫܦܰܥ ܙܰܝܬܶܗ ܒܟܰܪܡܳܐ",
                "adapted_arabic": "زَيْتا دْقَلَمون أشْفَع زَيْتِه بْكَرْما",
                "ipa": "/ˈzajta d-qalaˈmuːn ʔaʃˈfaʕ ˈzajteħ b-ˈkarma/",
                "phonological_note": "Uses poetic verb ašfaʕ (to overflow abundantly) reflective of olive harvest chants.",
                "audio_hint": "zay-ta  d-qa-la-mūn  ash-fa  zay-teh  b-kar-ma",
                "badge": "Poetic Register"
            },
            "bakha": {
                "name": "Bakh'a (Archaic Mountain)",
                "sub_label": "High Altitude Qalamoun",
                "syriac_script": "ܙܰܝܬܳܐ ܕܛܽܘܪܳܐ ܝܰܗܒ݂ ܡܫܚܳܐ ܒܪܰܡܬ݂ܳܐ",
                "adapted_arabic": "زَيْتا دْطُورا يَھْب مِشْحا بْرَمْتا",
                "ipa": "/ˈzajta d-ˈtˤuːra ˈjaħb ˈmɪʃħa b-ˈramtʰa/",
                "phonological_note": "Uses ramṯā (terrace/high plateau), preserving Old Aramaic topographical vocabulary.",
                "audio_hint": "zay-ta  d-ṭū-ra  yahb  mish-ha  b-ram-ta",
                "badge": "Archaic Mountain"
            }
        },
        "tokens_breakdown": [
            {"Token": "zaytā", "Morpheme": "zayt-ā (the olive/olive tree)", "Root": "√z-y-t (ܙܝܬ)", "Cognate": "Syr: ܙܝܬܐ | Heb: זַיִת | Arab: زَيْتُون", "Status": "Verified"},
            {"Token": "ṭūrā", "Morpheme": "ṭūr-ā (the mountain)", "Root": "√ṭ-w-r (ܛܘܪ)", "Cognate": "Syr: ܛܘܪܐ | Heb: צוּר / טוּר | Arab: طُور (طور سيناء)", "Status": "Verified"},
            {"Token": "mešḥā", "Morpheme": "mešḥ-ā (anointing oil / liquid olive oil)", "Root": "√m-š-ḥ (ܡܫܚ)", "Cognate": "Syr: ܡܫܚܐ | Heb: מָשִׁיחַ / מִשְׁחָה | Arab: مَسَحَ", "Status": "Verified"}
        ]
    },
    "blessing_house": {
        "title": "May bread, water, and peace never leave this roof",
        "category": "Household & Hearth Blessing",
        "english_literal": "Bread of the oven and cool spring water remain upon your household forever",
        "semitic_root_summary": "√l-ḥ-m (Bread) • √m-y-m (Water) • √b-y-t (House)",
        "dialects": {
            "maaloula": {
                "name": "Maaloula (Christian / Monastic)",
                "sub_label": "Eastern Qalamoun",
                "syriac_script": "ܠܚܶܡ ܬܰܢܽܘܪܳܐ ܘܡܰܝܳܐ ܩܰܪܺܝܪܶܐ ܒܒܰܝܬܰܟ݂",
                "adapted_arabic": "لْحِم تَنُّورا ومَيّا قَرِيرِه بْبَيْتَك",
                "ipa": "/lħɪm tʰanˈnuːra w-ˈmajja qaˈrjiːrɪ b-ˈbajtʰak/",
                "phonological_note": "Retains geminate /nn/ in tannūrā and plural adjective ending -ē (qarīrē).",
                "audio_hint": "l-him  tan-nū-ra  w-may-ya  qa-rī-reh  b-bay-tak",
                "badge": "Monastic Standard"
            },
            "jubbadin": {
                "name": "Jubb'adin (Oral Poetry & Agrarian)",
                "sub_label": "Central Qalamoun",
                "syriac_script": "ܠܚܶܡ ܒܰܪܟ݂ܳܐ ܘܡܰܝܳܐ ܕܥܰܝܢܳܐ ܒܕܳܪܰܟ݂",
                "adapted_arabic": "لْحِم بَرْكا ومَيّا دْعَيْنا بْدارَك",
                "ipa": "/lħɪm ˈbarka w-ˈmajja d-ʕajna b-ˈdaːrak/",
                "phonological_note": "Uses dārā (enclosed courtyard/home) in place of baytā for rhythmic cadence.",
                "audio_hint": "l-him  bar-ka  w-may-ya  d-ay-na  b-dā-rak",
                "badge": "Poetic Register"
            },
            "bakha": {
                "name": "Bakh'a (Archaic Mountain)",
                "sub_label": "High Altitude Qalamoun",
                "syriac_script": "ܠܚܶܡܳܐ ܘܡܰܝܳܐ ܕܓ݂ܰܒ݂ܪܳܐ ܩܰܝܳܡܺܝܢ ܒܩܰܪܝܳܬ݂ܰܢ",
                "adapted_arabic": "لْحِما ومَيّا دْغَبْرا قَيّامِين بْقَرْيوتَن",
                "ipa": "/lħɪma w-ˈmajja d-ˈɣabra qajjaːˈmiːn b-qarˈjoːtʰan/",
                "phonological_note": "Retains post-vocalic spirantized /ġ/ in ġabrā (man/heroic mountain host).",
                "audio_hint": "l-hi-ma  w-may-ya  d-ghab-ra  qay-yā-mīn",
                "badge": "Archaic Mountain"
            }
        },
        "tokens_breakdown": [
            {"Token": "lḥem tannūrā", "Morpheme": "lḥem (bread of) + tannūr-ā (clay oven)", "Root": "√l-ḥ-m (ܠܚܡ)", "Cognate": "Syr: ܠܚܡܐ | Heb: לֶחֶם | Arab: لَحْم (cognate semantic shift: food/flesh)", "Status": "Verified"},
            {"Token": "mayyā", "Morpheme": "mayy-ā (water - plural form)", "Root": "√m-y-m (ܡܝܐ)", "Cognate": "Syr: ܡܝܐ | Heb: מַיִם | Arab: مَاء / مِيَاه", "Status": "Verified"},
            {"Token": "bayt-ak", "Morpheme": "bayt- (house) + -ak (your m.sg)", "Root": "√b-y-t (ܒܝܬ)", "Cognate": "Syr: ܒܝܬܐ | Heb: בַּיִת | Arab: بَيْت", "Status": "Verified"}
        ]
    }
}

# Woolaroo Visual Levant Object Catalog
WOOLAROO_OBJECTS = [
    {
        "id": "tannour_bread",
        "title": "Traditional Tannour Flatbread",
        "category": "Culinary Heritage",
        "emoji": "🫓",
        "aramaic_name_syr": "ܠܚܡܐ ܕܬܢܘܪܐ",
        "aramaic_name_arab": "لِحْما دْتَنّورا",
        "ipa": "/ˈlħɪma d-tanˈnuːra/",
        "root_cognate": "√l-ḥ-m (Bread) + Akkadian tinūru → Aramaic tannūrā",
        "desc": "Baked on the blazing clay inner walls of a sunken mountain Tannour oven in Maaloula and Jubb'adin. Often brushed with mountain sumac or wild thyme.",
        "sample_sentence": "We break tannour flatbread with every neighbor who crosses the mountain pass.",
        "audio_phonetic": "LHI-ma d-tan-NU-ra"
    },
    {
        "id": "qalamoun_olive_tree",
        "title": "Ancient Terraced Olive Tree",
        "category": "Agrarian Landscape",
        "emoji": "🫒",
        "aramaic_name_syr": "ܙܝܬܐ ܥܬܝܩܐ",
        "aramaic_name_arab": "زَيْتا عَتِيقا",
        "ipa": "/ˈzajta ʕaˈtʰiːqa/",
        "root_cognate": "√z-y-t (Olive) • Proto-Semitic *zayt-",
        "desc": "Centuries-old olive groves built on hand-laid limestone terraces (ramṯā) above the valleys of Maaloula and Bakh'a. Harvested by hand using cane beating poles.",
        "sample_sentence": "The olive tree is the anchor of our families; its oil lamps burned in the rock-cut chapels.",
        "audio_phonetic": "ZAY-ta a-TI-qa"
    },
    {
        "id": "saint_thecla_canyon",
        "title": "Faj Maaloula (The Sacred Mountain Gorge)",
        "category": "Sacred Geography",
        "emoji": "⛰️",
        "aramaic_name_syr": "ܦܓܐ ܕܛܘܪܐ",
        "aramaic_name_arab": "فَجّا دْطُورا",
        "ipa": "/ˈfadʒdʒa d-ˈtˤuːra/",
        "root_cognate": "√p-g-y (Cleft / Split Gorge) • Syriac paggā",
        "desc": "The narrow limestone canyon cleft through the Anti-Lebanon mountains where according to folklore the rock split open to shelter Saint Thecla.",
        "sample_sentence": "The wind sings through the narrow walls of the canyon in ancient Aramaic syllables.",
        "audio_phonetic": "FAJ-ja d-TU-ra"
    },
    {
        "id": "stone_press_grape",
        "title": "Ancient Basalt Grape Press (Maʕṣartā)",
        "category": "Viticulture",
        "emoji": "🍇",
        "aramaic_name_syr": "ܡܥܨܪܬܐ ܕܟܪܡܐ",
        "aramaic_name_arab": "مَعْصَرْتا دْكَرْما",
        "ipa": "/maʕˈsˤartʰa d-ˈkarma/",
        "root_cognate": "√ʕ-ṣ-r (Squeeze/Press) • √k-r-m (Vineyard)",
        "desc": "Carved directly into the limestone bedrock, used for pressing golden Qalamoun grapes into thick mountain grape molasses (dibs).",
        "sample_sentence": "Golden grape molasses is boiled over cedar embers in the chill October nights.",
        "audio_phonetic": "ma-SAR-ta d-KAR-ma"
    },
    {
        "id": "qalamoun_wool_loom",
        "title": "Traditional Hand-Loomed Wool Blanket",
        "category": "Textiles & Crafts",
        "emoji": "🧶",
        "aramaic_name_syr": "ܥܘܡܪܐ ܕܥܢܐ",
        "aramaic_name_arab": "عُمْرا دْعَنا",
        "ipa": "/ˈʕumra d-ˈʕana/",
        "root_cognate": "√ʕ-m-r (Wool / Thick Covering)",
        "desc": "Woven by village elders from raw sheep's wool dyed with walnut husks, pomegranate rind, and wild indigo from the valley.",
        "sample_sentence": "Wrap yourself in the mountain wool against the snows of Mount Hermon.",
        "audio_phonetic": "UM-ra d-A-na"
    }
]

# Story Weaver Folktale Motifs
FOLKTALE_MOTIFS = [
    {
        "id": "speaking_cedar",
        "title": "🌲 The Shepherd & The Speaking Cedar on Mount Hermon",
        "prompt": "Write a bilingual Levantine folktale about a young shepherd from Jubb'adin who hears a hollow cedar tree speak in ancient Aramaic verse during a heavy winter snowstorm.",
        "preview": "A young shepherd discovers that the oldest cedar tree on the ridge remembers the kings of Aram-Damascus..."
    },
    {
        "id": "wise_grandmother",
        "title": "🫒 The Wise Elder of the Golden Olive Harvest",
        "prompt": "Write a bilingual folktale about an elder woman in Maaloula who teaches her granddaughter the secret song that makes the rocky olive trees yield golden oil even in drought.",
        "preview": "An oral legend about community solidarity, terraced stone walls, and the blessing of the mountain oil..."
    },
    {
        "id": "echoes_canyon",
        "title": "⛰️ The Three Echoes of Saint Thecla's Gorge",
        "prompt": "Write a traditional Qalamoun fable about three travelers through Faj Maaloula whose words echo back in three distinct mountain dialects: Maaloula, Jubb'adin, and Bakh'a.",
        "preview": "A riddle-folktale celebrating how three sister villages preserved Aramaic across centuries of isolation..."
    }
]

# MASC Analog Tape Recordings Simulator
MASC_TAPES = [
    {
        "tape_id": "MASC-1974-04B",
        "title": "Reel #1974-04B: Elder Boutros on the 1950 Winter Harvest in Maaloula",
        "speaker": "Boutros Nader (Age 78 at recording)",
        "village": "Maaloula (Christian Quarter)",
        "duration": "01:24 min sample",
        "snr": "28.4 dB (Restored 48kHz Digital Transfer)",
        "candidates": [
            {
                "label": "Candidate 1 (IPA Aligned - 96.4% Conf)",
                "transcription": "/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/",
                "confidence": 96.4,
                "script_type": "IPA Phonetic Alignment"
            },
            {
                "label": "Candidate 2 (Syriac Estrangelo - 94.1% Conf)",
                "transcription": "ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ",
                "confidence": 94.1,
                "script_type": "Syriac Estrangelo Script"
            },
            {
                "label": "Candidate 3 (Adapted Arabic - 98.2% Conf)",
                "transcription": "بْشَيْنا تِيتُن لْقَرْيِتْنا حَلْواتا",
                "confidence": 98.2,
                "script_type": "Adapted Arabic Qalamoun Script"
            }
        ],
        "decomposition": [
            {"Token": "b-šayna", "Morpheme": "b- (in) + šayn-a (peace)", "Cognate": "Syr: ܒܫܝܢܐ | Heb: בְּשָׁלוֹם", "Status": "Verified"},
            {"Token": "ṯētun", "Morpheme": "√ʔ-t-y (come) - 2nd Pl. Perf", "Cognate": "Arab: أتيتم | Syr: ܐܬܝܬܘܢ", "Status": "Verified"},
            {"Token": "l-qaryēṯan", "Morpheme": "l- (to) + qary-ēṯ-an (our village)", "Cognate": "Arab: لقرية | Syr: ܠܩܪܝܬܐ", "Status": "Verified"}
        ]
    },
    {
        "tape_id": "MASC-1981-12A",
        "title": "Reel #1981-12A: Jubb'adin Wedding Quatrain (Ataba & Mijana Oral Chant)",
        "speaker": "Hanna & Mariam Simaan",
        "village": "Jubb'adin (Central Qalamoun)",
        "duration": "00:58 min sample",
        "snr": "31.0 dB (Heidelberg Acoustic Archive)",
        "candidates": [
            {
                "label": "Candidate 1 (IPA Aligned - 97.1% Conf)",
                "transcription": "/lħɪm ˈbarka w-ˈmajja d-ʕajna b-ˈdaːrak/",
                "confidence": 97.1,
                "script_type": "IPA Phonetic Alignment"
            },
            {
                "label": "Candidate 2 (Syriac Estrangelo - 95.3% Conf)",
                "transcription": "ܠܚܶܡ ܒܰܪܟ݂ܳܐ ܘܡܰܝܳܐ ܕܥܰܝܢܳܐ ܒܕܳܪܰܟ݂",
                "confidence": 95.3,
                "script_type": "Syriac Estrangelo Script"
            },
            {
                "label": "Candidate 3 (Adapted Arabic - 97.9% Conf)",
                "transcription": "لْحِم بَرْكا ومَيّا دْعَيْنا بْدارَك",
                "confidence": 97.9,
                "script_type": "Adapted Arabic Qalamoun Script"
            }
        ],
        "decomposition": [
            {"Token": "lḥem barkā", "Morpheme": "lḥem (bread) + barkā (blessed)", "Cognate": "Syr: ܒܪܟܬܐ | Heb: בְּרָכָה", "Status": "Verified"},
            {"Token": "mayyā ḏ-ʕaynā", "Morpheme": "mayyā (water) + ḏ-ʕaynā (of spring)", "Cognate": "Arab: ماء العين | Heb: מֵי עַיִן", "Status": "Verified"},
            {"Token": "b-dārak", "Morpheme": "b- (in) + dār-ak (your courtyard)", "Cognate": "Arab: دار | Heb: דּוֹר / דִּירָה", "Status": "Verified"}
        ]
    }
]

# 2M-Token In-Context Semitic Grammar Prompt Template
SEMITIC_GRAMMAR_PROMPT_TEMPLATE = """
[SYSTEM: VERTEX AI / GEMINI 2.0 FLASH WESTERN NEO-ARAMAIC ZERO-SHOT GRAMMAR ENGINE]
CORPUS_TOKEN_COUNT: 1,940,280 tokens (Heidelberg MASC + Enable Syria Qalamoun Field Grammar)
DIALECT_TRIAD: Maaloula (Monastic/Christian), Jubb'adin (Oral Poetry/Agrarian), Bakh'a (Archaic Mountain)
PHONOLOGICAL_LAWS:
1. Interdental Fricative Retention: Maaloula /ṯ/ & /ḏ/ vs Jubb'adin Stop Merger (/t/ & /d/).
2. Archaic Back-Vowel Raising: Bakh'a /ā/ -> /ō/ in plural & feminine suffixes (-ōṯan).
3. Prosthetic Glottal Onset: /ʔb-/ before initial labial consonants in Maaloula.
4. Lexical Substrates: Liturgical Syriac borrowings in Maaloula vs pastoral Canaanite-Aramaic cognates in Bakh'a.

INPUT_QUERY: "{query}"

GENERATE_ANALYSIS_JSON:
Provide an authentic, three-dialect Western Neo-Aramaic output including:
- Exact Syriac Estrangelo script with vowel diacritics
- Adapted Arabic script with Qalamoun sukoon/vowel marking
- IPA transcription
- Etymological Semitic root token decomposition (√x-y-z)
"""
