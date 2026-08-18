"""
Project Siryon Prototype — Western Neo-Aramaic Living Web App
Maaloula • Jubb'adin • Bakh'a
Built with Streamlit & Google Gemini 2.0 Flash / Vertex AI
Partnership with Enable Syria (go/enable-syria) & Heidelberg University MASC
"""

import os
import json
import streamlit as st
import pandas as pd
import siryon_data

# Page configuration
st.set_page_config(
    page_title="Project Siryon • Western Neo-Aramaic Living Web App",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Syriac / Arabic / IPA typography & Levantine aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+Arabic:wght@400;600&family=Noto+Sans+Syriac:wght@400;600&display=swap');

.syriac-script {
    font-family: 'Noto Sans Syriac', 'Serto Jerusalem', 'Estrangelo Edessa', sans-serif;
    font-size: 1.65rem;
    line-height: 2.1rem;
    direction: rtl;
    text-align: right;
    color: #1e293b;
    background-color: #f8fafc;
    padding: 12px 16px;
    border-radius: 8px;
    border-right: 4px solid #b45309;
    margin-bottom: 8px;
}

.arabic-script {
    font-family: 'Noto Sans Arabic', sans-serif;
    font-size: 1.45rem;
    line-height: 2.0rem;
    direction: rtl;
    text-align: right;
    color: #334155;
    background-color: #fffbeb;
    padding: 10px 14px;
    border-radius: 8px;
    border-right: 4px solid #d97706;
    margin-bottom: 8px;
}

.ipa-script {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    color: #0f172a;
    background-color: #f1f5f9;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 10px;
    letter-spacing: 0.02em;
}

.card-container {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px;
    background: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    height: 100%;
}

.badge-monastic {
    background-color: #fef3c7;
    color: #92400e;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

.badge-poetic {
    background-color: #e0e7ff;
    color: #3730a3;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

.badge-archaic {
    background-color: #dcfce7;
    color: #166534;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

.root-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'asr_run' not in st.session_state:
    st.session_state['asr_run'] = False
if 'gold_standard_approved' not in st.session_state:
    st.session_state['gold_standard_approved'] = []
if 'selected_phrase_id' not in st.session_state:
    st.session_state['selected_phrase_id'] = "welcome_village"
if 'selected_woolaroo_id' not in st.session_state:
    st.session_state['selected_woolaroo_id'] = "tannour_bread"
if 'story_generated' not in st.session_state:
    st.session_state['story_generated'] = None
if 'gemini_api_key' not in st.session_state:
    st.session_state['gemini_api_key'] = os.environ.get("GEMINI_API_KEY", "")

# Helper function for Gemini Live Call
def call_gemini_grammar_prompt(api_key, phrase_text):
    """
    Invokes Gemini API zero-shot or uses the 2M-Token In-Context Semitic Grammar Prompt simulation.
    """
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = siryon_data.SEMITIC_GRAMMAR_PROMPT_TEMPLATE.format(query=phrase_text)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel('gemini-2.0-flash')
            prompt = siryon_data.SEMITIC_GRAMMAR_PROMPT_TEMPLATE.format(query=phrase_text)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            return f"⚠️ Gemini API connection note: {str(e2)}"

def call_gemini_story_weaver(api_key, folktale_prompt):
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        sys_instr = (
            "You are a bilingual Western Neo-Aramaic storyteller from the Qalamoun mountains. "
            "Write an evocative folktale in English with interwoven authentic Western Neo-Aramaic proverbs/dialogue "
            "showing exact Syriac Estrangelo script, Adapted Arabic script, and phonetic IPA."
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{sys_instr}\n\nPrompt: {folktale_prompt}"
        )
        return response.text
    except Exception as e:
        return None

# Sidebar Navigation & Settings
with st.sidebar:
    st.title("🏛️ Project Siryon")
    st.subheader("Western Neo-Aramaic Preservation & Generative Studio")
    st.caption("Maaloula • Jubb'adin • Bakh'a")
    st.divider()

    st.markdown("### 🔑 Gemini AI Configuration")
    api_key_input = st.text_input(
        "GEMINI_API_KEY",
        value=st.session_state['gemini_api_key'],
        type="password",
        placeholder="AIzaSy..."
    )
    if api_key_input != st.session_state['gemini_api_key']:
        st.session_state['gemini_api_key'] = api_key_input

    if st.session_state['gemini_api_key']:
        st.success("✅ Gemini API Key Active (2M-Token In-Context Semitic Grammar Ready)")
    else:
        st.info("ℹ️ Using Built-in Qalamoun Tri-Dialect Corpus (Enter GEMINI_API_KEY for live zero-shot inference)")

    st.divider()
    st.markdown("### 🔊 Mountain Ambience")
    st.caption("Qalamoun Field Recording (#1974-04 Ambience)")
    # Audio simulator as specified in prompt
    st.audio("https://actions.google.com/sounds/v1/ambiences/outdoor_field_wind.ogg")

    st.divider()
    st.markdown("### 🌍 Partnership & Corpus")
    st.markdown("""
    * **Heidelberg University MASC**: Maaloula Aramaic Speech Corpus
    * **Enable Syria**: `go/enable-syria` Qalamoun Heritage Initiative
    * **Argolis Vertex AI**: Zero-shot epigraphic alignment
    """)

# Header Banner
st.title("📖 Project Siryon: Living Western Neo-Aramaic Portal")
st.markdown("""
Western Neo-Aramaic (*Līšānā ʾArāmāyā*) is the sole living descendant of the language spoken across the Levant 2,000 years ago, preserved today in three highland villages of the Qalamoun mountain range: **Maaloula**, **Jubb'adin**, and **Bakh'a**.
""")

# Create the 3 main Tabs
tab1, tab2, tab3 = st.tabs([
    "📖 TAB 1: LEARN (Tri-Dialect Phrasebook)",
    "🎨 TAB 2: PLAY (Generative Studio & Woolaroo Camera)",
    "🔬 TAB 3: WORK (AI Epigraphy & Researcher Workbench)"
])

# ==============================================================================
# TAB 1: LEARN (Tri-Dialect Phrasebook)
# ==============================================================================
with tab1:
    st.header("📖 Tri-Dialect Western Neo-Aramaic Phrasebook")
    st.write(
        "Uses our **2M-Token In-Context Semitic Grammar Prompt zero-shot** to synthesize exact side-by-side dialect cards for "
        "Maaloula (Christian/Monastic), Jubb'adin (Oral Poetry), and Bakh'a (Archaic Mountain)."
    )

    col_sel, col_prompt_toggle = st.columns([3, 1])
    with col_sel:
        phrase_keys = list(siryon_data.PHRASEBOOK_CORPUS.keys())
        phrase_titles = [siryon_data.PHRASEBOOK_CORPUS[k]["title"] for k in phrase_keys]
        selected_idx = phrase_keys.index(st.session_state['selected_phrase_id']) if st.session_state['selected_phrase_id'] in phrase_keys else 0
        chosen_title = st.selectbox(
            "Select Qalamoun Phrase or In-Context Query:",
            options=phrase_titles,
            index=selected_idx
        )
        chosen_key = phrase_keys[phrase_titles.index(chosen_title)]
        st.session_state['selected_phrase_id'] = chosen_key

    with col_prompt_toggle:
        show_prompt_inspector = st.checkbox("🔍 View 2M-Token Prompt Engine", value=False)

    phrase_data = siryon_data.PHRASEBOOK_CORPUS[chosen_key]

    if show_prompt_inspector:
        with st.expander("2M-Token Zero-Shot In-Context Semitic Grammar Prompt", expanded=True):
            st.code(
                siryon_data.SEMITIC_GRAMMAR_PROMPT_TEMPLATE.format(query=phrase_data["english_literal"]),
                language="plaintext"
            )
            if st.session_state['gemini_api_key']:
                if st.button("🚀 Run Live Zero-Shot Inference on Gemini API"):
                    with st.spinner("Executing Zero-Shot In-Context Semitic Grammar Model..."):
                        live_res = call_gemini_grammar_prompt(st.session_state['gemini_api_key'], phrase_data["english_literal"])
                        if live_res:
                            st.markdown("#### Gemini Zero-Shot Inference Output:")
                            st.info(live_res)

    st.markdown(f"**English Translation:** `{phrase_data['english_literal']}`  •  **Semitic Roots:** `{phrase_data['semitic_root_summary']}`")

    # 3 Side-by-Side Dialect Cards
    d_col1, d_col2, d_col3 = st.columns(3)

    # 1. Maaloula
    with d_col1:
        m_data = phrase_data["dialects"]["maaloula"]
        st.markdown(
            f"""
            <div class="card-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-weight:700; font-size:1.1rem; color:#1e293b;">⛪ Maaloula</span>
                    <span class="badge-monastic">{m_data['badge']}</span>
                </div>
                <div style="font-size:0.8rem; color:#64748b; margin-bottom:12px;">{m_data['sub_label']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Exact Syriac Script (Estrangelo):</div>
                <div class="syriac-script">{m_data['syriac_script']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Adapted Arabic Script:</div>
                <div class="arabic-script">{m_data['adapted_arabic']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">IPA Phonetic Transliteration:</div>
                <div class="ipa-script">{m_data['ipa']}</div>
                <div style="font-size:0.82rem; color:#334155; background:#f8fafc; padding:8px; border-radius:6px; margin-bottom:10px;">
                    <strong>Phonology Law:</strong> {m_data['phonological_note']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔊 Audio Guide (Maaloula Cadence)", key="audio_m"):
            st.toast(f"Pronunciation Guide: {m_data['audio_hint']}", icon="🔊")

    # 2. Jubb'adin
    with d_col2:
        j_data = phrase_data["dialects"]["jubbadin"]
        st.markdown(
            f"""
            <div class="card-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-weight:700; font-size:1.1rem; color:#1e293b;">🌾 Jubb'adin</span>
                    <span class="badge-poetic">{j_data['badge']}</span>
                </div>
                <div style="font-size:0.8rem; color:#64748b; margin-bottom:12px;">{j_data['sub_label']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Exact Syriac Script (Estrangelo):</div>
                <div class="syriac-script">{j_data['syriac_script']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Adapted Arabic Script:</div>
                <div class="arabic-script">{j_data['adapted_arabic']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">IPA Phonetic Transliteration:</div>
                <div class="ipa-script">{j_data['ipa']}</div>
                <div style="font-size:0.82rem; color:#334155; background:#f8fafc; padding:8px; border-radius:6px; margin-bottom:10px;">
                    <strong>Phonology Law:</strong> {j_data['phonological_note']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔊 Audio Guide (Jubb'adin Poetic Cadence)", key="audio_j"):
            st.toast(f"Pronunciation Guide: {j_data['audio_hint']}", icon="🔊")

    # 3. Bakh'a
    with d_col3:
        b_data = phrase_data["dialects"]["bakha"]
        st.markdown(
            f"""
            <div class="card-container">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-weight:700; font-size:1.1rem; color:#1e293b;">🏔️ Bakh'a</span>
                    <span class="badge-archaic">{b_data['badge']}</span>
                </div>
                <div style="font-size:0.8rem; color:#64748b; margin-bottom:12px;">{b_data['sub_label']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Exact Syriac Script (Estrangelo):</div>
                <div class="syriac-script">{b_data['syriac_script']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">Adapted Arabic Script:</div>
                <div class="arabic-script">{b_data['adapted_arabic']}</div>
                <div style="font-size:0.75rem; font-weight:600; color:#475569;">IPA Phonetic Transliteration:</div>
                <div class="ipa-script">{b_data['ipa']}</div>
                <div style="font-size:0.82rem; color:#334155; background:#f8fafc; padding:8px; border-radius:6px; margin-bottom:10px;">
                    <strong>Phonology Law:</strong> {b_data['phonological_note']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔊 Audio Guide (Bakh'a High Altitude)", key="audio_b"):
            st.toast(f"Pronunciation Guide: {b_data['audio_hint']}", icon="🔊")

    st.divider()
    st.subheader("Comparative Semitic Root & Morphological Etymology")
    df_tokens = pd.DataFrame(phrase_data["tokens_breakdown"])
    st.table(df_tokens)


# ==============================================================================
# TAB 2: PLAY (Generative Studio & Woolaroo Camera)
# ==============================================================================
with tab2:
    st.header("🎨 PLAY: Woolaroo Object Camera & Aramaic Story Weaver")

    st.subheader("1. 📷 Woolaroo Levantine Object Simulator")
    st.write(
        "Pick a real Levantine cultural object from the Qalamoun highlands (traditional Tannour flatbread, terraced olive tree, "
        "Faj Maaloula mountain gorge) to view interactive visual Aramaic cards."
    )

    # Object Selector Pills
    obj_cols = st.columns(len(siryon_data.WOOLAROO_OBJECTS))
    for i, obj in enumerate(siryon_data.WOOLAROO_OBJECTS):
        with obj_cols[i]:
            selected = (st.session_state['selected_woolaroo_id'] == obj['id'])
            btn_style = "primary" if selected else "secondary"
            if st.button(f"{obj['emoji']} {obj['title']}", key=f"wobj_{obj['id']}", use_container_width=True):
                st.session_state['selected_woolaroo_id'] = obj['id']

    selected_obj = next(o for o in siryon_data.WOOLAROO_OBJECTS if o['id'] == st.session_state['selected_woolaroo_id'])

    # Display High-Craft Woolaroo Visual Card
    w_card_col1, w_card_col2 = st.columns([1, 2])
    with w_card_col1:
        st.markdown(
            f"""
            <div style="border:2px solid #b45309; border-radius:16px; padding:32px; text-align:center; background:#fffbeb;">
                <div style="font-size:4.5rem; margin-bottom:12px;">{selected_obj['emoji']}</div>
                <div style="font-weight:700; font-size:1.2rem; color:#78350f;">{selected_obj['title']}</div>
                <div style="font-size:0.85rem; color:#b45309; margin-top:4px;">{selected_obj['category']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with w_card_col2:
        st.markdown(
            f"""
            <div style="border:1px solid #cbd5e1; border-radius:12px; padding:20px; background:#ffffff;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.9rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Estrangelo Label</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; background:#f1f5f9; padding:4px 8px; border-radius:4px;">{selected_obj['root_cognate']}</span>
                </div>
                <div class="syriac-script" style="font-size:2.0rem; margin-top:8px;">{selected_obj['aramaic_name_syr']}</div>
                
                <div style="font-size:0.9rem; font-weight:700; color:#64748b; text-transform:uppercase; margin-top:12px;">Adapted Arabic Script Label</div>
                <div class="arabic-script" style="font-size:1.6rem;">{selected_obj['aramaic_name_arab']}</div>
                
                <div style="font-size:0.9rem; font-weight:700; color:#64748b; text-transform:uppercase; margin-top:12px;">IPA Transliteration</div>
                <div class="ipa-script">{selected_obj['ipa']}</div>
                
                <p style="margin-top:12px; color:#334155; line-height:1.5;"><strong>Cultural Context:</strong> {selected_obj['desc']}</p>
                <p style="color:#475569; font-style:italic;"><strong>Qalamoun Usage:</strong> "{selected_obj['sample_sentence']}"</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"🔊 Listen to Pronunciation ({selected_obj['audio_phonetic']})", key="wobj_audio"):
            st.toast(f"Pronouncing {selected_obj['aramaic_name_syr']} ({selected_obj['audio_phonetic']})", icon="🔊")

    st.divider()

    # The Aramaic Story Weaver
    st.subheader("2. 📜 The Aramaic Story Weaver (Bilingual Folktale Studio)")
    st.write(
        "Type a Qalamoun folktale prompt or select an oral legend motif. Watch Gemini weave a bilingual Levantine story "
        "with authentic Western Neo-Aramaic verse interlaid."
    )

    story_motif_titles = [m['title'] for m in siryon_data.FOLKTALE_MOTIFS]
    chosen_motif_title = st.selectbox("Choose a Qalamoun Oral Legend Motif:", options=story_motif_titles)
    chosen_motif = next(m for m in siryon_data.FOLKTALE_MOTIFS if m['title'] == chosen_motif_title)

    custom_story_prompt = st.text_area(
        "Or customize your folktale prompt:",
        value=chosen_motif['prompt'],
        height=90
    )

    if st.button("✨ Weave Bilingual Levantine Folktale (Gemini Generative Studio)", type="primary"):
        with st.spinner("Weaving bilingual Western Neo-Aramaic story with Gemini..."):
            ai_story = call_gemini_story_weaver(st.session_state['gemini_api_key'], custom_story_prompt)
            if ai_story:
                st.session_state['story_generated'] = ai_story
            else:
                # Authentic rich folklore fallback
                st.session_state['story_generated'] = f"""
### {chosen_motif['title']}
*A Bilingual Levantine Folktale from the Qalamoun Ridge • Maaloula & Jubb'adin Oral Tradition*

High above the limestone cliffs of Saint Thecla's gorge, where the wind carries the scent of wild mountain thyme and burning cedar wood, lived a young shepherd named Hanna. Every autumn when the first snow capped Mount Hermon, the village elders gathered around the sunken clay **tannūr** oven (*ܬܢܘܪܐ - tannūrā*).

As Hanna rested his hand against the gnarled bark of a thousand-year-old cedar tree on the ridge, the branches whispered in the ancient speech of the village:

> **Western Neo-Aramaic Proverb (Maaloula / Jubb'adin):**
> 
> **Syriac Estrangelo:** `ܫܠܳܡܳܐ ܥܰܠ ܛܽܘܪܳܐ ܕܢܳܛܰܪ ܙܰܝܬܶܗ ܘܠܶܫܳܢܶܗ`
> 
> **Adapted Arabic:** `شْلاما عَل طُورا دْناطَر زَيْتِه ولِشانِه`
> 
> **IPA Cadence:** `/ˈʃlaːma ʕal ˈtˤuːra d-ˈnaːtˤar ˈzajtʰeħ w-lɪˈʃaːneħ/`
> 
> *"Peace upon the mountain that guards its olive tree and its language."*

When the shepherd returned to the valley at twilight, the families broke warm flatbread (**lḥem tannūrā / ܠܚܡܐ ܕܬܢܘܪܐ**) and drank cold water from the village spring (**mayyā ḏ-ʕaynā / ܡܝܐ ܕܥܝܢܐ**), knowing that so long as the syllables of Qalamoun were spoken around the hearth, their village of sweet waters would endure.
"""
    if st.session_state['story_generated']:
        st.markdown(
            f"""
            <div style="border:1px solid #cbd5e1; border-radius:12px; padding:24px; background:#fafafa; margin-top:16px;">
                {st.session_state['story_generated']}
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# TAB 3: WORK (AI Epigraphy & Researcher Workbench)
# EXACT SPECIFICATION IMPLEMENTATION FROM PROTOTYPE + RICH FUNCTIONALITY
# ==============================================================================
with tab3:
    st.header("🔬 WORK: AI Epigraphy & MASC Researcher Workbench")
    st.write(
        "Simulates ingesting analog audio tapes from Heidelberg University’s **Maaloula Aramaic Speech Corpus (MASC)**. "
        "Runs Chirp/USM candidate ASR alignment, breaks down Semitic root tokens (`√ʔ-t-y`, `√q-r-y`), links cognates to "
        "Classical Syriac/Hebrew, and allows 1-click Gold Standard approval."
    )

    w_col1, w_col2 = st.columns([1, 2])

    with w_col1:
        st.subheader("Archival MASC Audio Tape Deck")
        selected_tape_title = st.selectbox(
            "Select Analog Reel Recording:",
            options=[t["title"] for t in siryon_data.MASC_TAPES]
        )
        current_tape = next(t for t in siryon_data.MASC_TAPES if t["title"] == selected_tape_title)

        st.markdown(
            f"""
            <div style="background:#0f172a; color:#f8fafc; padding:16px; border-radius:12px; margin-bottom:14px;">
                <div style="font-family:'JetBrains Mono',monospace; color:#38bdf8; font-size:0.8rem;">TAPE REEL ARCHIVE METADATA</div>
                <div style="font-weight:700; font-size:1.05rem; margin-top:4px;">{current_tape['tape_id']}</div>
                <div style="font-size:0.85rem; color:#94a3b8;">Speaker: {current_tape['speaker']}</div>
                <div style="font-size:0.85rem; color:#94a3b8;">Village: {current_tape['village']}</div>
                <div style="font-size:0.85rem; color:#4ade80;">SNR / Digitization: {current_tape['snr']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # EXACT line from prototype snippet:
        # Audio simulator
        st.audio("https://actions.google.com/sounds/v1/ambiences/outdoor_field_wind.ogg")

        # EXACT line from prototype snippet:
        if st.button("Run Auto-Segmentation & Chirp ASR Alignment", use_container_width=True):
            st.session_state['asr_run'] = True

        if st.session_state['gold_standard_approved']:
            st.divider()
            st.markdown("#### ✅ Heidelberg MASC Gold Standard Ledger")
            for item in st.session_state['gold_standard_approved']:
                st.success(f"Archived to Gold Standard: `{item}`")

    with w_col2:
        if st.session_state.get('asr_run', False):
            # EXACT Subheader from prototype snippet:
            st.subheader("ASR Candidate Transcriptions & Confidence")

            # EXACT Markdown block from prototype snippet:
            st.markdown("""
            * **Candidate 1 (IPA Aligned - 96.4% Conf):** `/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/`
            * **Candidate 2 (Syriac Estrangelo - 94.1% Conf):** `ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ`
            * **Candidate 3 (Adapted Arabic - 98.2% Conf):** `بْشَيْنا تِيتُن لْقَرْيِتْنا حَلْواتا`
            """)

            # EXACT Divider and Subheader from prototype snippet:
            st.divider()
            st.subheader("Morphological Token Decomposition")

            # EXACT Table block from prototype snippet:
            st.table([
                {"Token": "b-šayna", "Morpheme": "b- (in) + šayn-a (peace)", "Cognate": "Syr: ܒܫܝܢܐ | Heb: בְּשָׁלוֹם", "Status": "Verified"},
                {"Token": "ṯētun", "Morpheme": "√ʔ-t-y (come) - 2nd Pl. Perf", "Cognate": "Arab: أتيتم | Syr: ܐܬܝܬܘܢ", "Status": "Verified"},
                {"Token": "l-qaryēṯan", "Morpheme": "l- (to) + qary-ēṯ-an (our village)", "Cognate": "Arab: لقرية | Syr: ܠܩܪܝܬܐ", "Status": "Verified"}
            ])

            # EXACT Columns and Buttons from prototype snippet:
            col_a, col_b = st.columns(2)
            if col_a.button("✅ Approve to MASC Gold Standard", type="primary"):
                st.session_state['gold_standard_approved'].append(
                    "/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/ • ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ"
                )
                st.toast("Approved to MASC Gold Standard Corpus!", icon="✅")

            if col_b.button("🚩 Flag for Elder Review Circle"):
                st.toast("Flagged for Maaloula & Jubb'adin Elder Review Circle", icon="🚩")
        else:
            st.info("👈 Click **'Run Auto-Segmentation & Chirp ASR Alignment'** in the Tape Deck panel to inspect candidate alignments and Semitic root token decomposition.")

# ==============================================================================
# Footer - EXACT FOOTER SNIPPET FROM PROTOTYPE
# ==============================================================================
st.divider()
st.caption("Project Siryon Prototype • Built with Google Gemini 2.0 Flash & Argolis Vertex AI • Partnership with Enable Syria (`go/enable-syria`) & Heidelberg University")
st.caption("raghadalnouri@mpl-composed-augury-38028.c.googlers.com • expires in 15h 41m • Debug Bundle 2026.08.17.03_RC03")
