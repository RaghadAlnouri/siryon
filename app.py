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
    page_title="Project Siryon • Western Neo-Aramaic Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Editorial, spacious custom styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,300..700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Arabic:wght@400;600&family=Noto+Sans+Syriac:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
}

.syriac-display {
    font-family: 'Noto Sans Syriac', 'Serto Jerusalem', 'Estrangelo Edessa', serif;
    font-size: 1.85rem;
    line-height: 2.3rem;
    direction: rtl;
    text-align: right;
    color: #0f172a;
    background-color: #fafaf9;
    padding: 16px 20px;
    border-radius: 10px;
    border-right: 4px solid #b45309;
    margin: 8px 0 14px 0;
}

.arabic-display {
    font-family: 'Noto Sans Arabic', sans-serif;
    font-size: 1.5rem;
    line-height: 2.1rem;
    direction: rtl;
    text-align: right;
    color: #334155;
    background-color: #fffbeb;
    padding: 12px 16px;
    border-radius: 10px;
    border-right: 4px solid #d97706;
    margin: 8px 0 14px 0;
}

.ipa-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    color: #1e293b;
    background-color: #f1f5f9;
    padding: 10px 14px;
    border-radius: 8px;
    margin: 8px 0 14px 0;
    letter-spacing: 0.02em;
}

.card-box {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 22px;
    background: #ffffff;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04);
    height: 100%;
}

.dialect-badge-m {
    background-color: #fef3c7;
    color: #92400e;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.dialect-badge-j {
    background-color: #e0e7ff;
    color: #3730a3;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.dialect-badge-b {
    background-color: #dcfce7;
    color: #166534;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.law-pill {
    font-size: 0.85rem;
    color: #475569;
    background: #f8fafc;
    border-left: 3px solid #64748b;
    padding: 10px 12px;
    border-radius: 6px;
    margin-top: 12px;
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

# Gemini Inference Helpers
def call_gemini_grammar_prompt(api_key, phrase_text):
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
        return f"⚠️ Gemini API connection note: {str(e)}"

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

# Sleek Editorial Top Bar & Settings Expander
col_logo, col_sub, col_cfg = st.columns([2, 3, 2])
with col_logo:
    st.markdown("### 🏛️ Project Siryon")
    st.caption("Living Western Neo-Aramaic Digital Portal • Maaloula, Jubb'adin & Bakh'a")
with col_sub:
    st.write("") # subtle spacing
with col_cfg:
    with st.popover("⚙️ Settings & Gemini API"):
        st.markdown("**AI Configuration**")
        api_key_input = st.text_input(
            "GEMINI_API_KEY",
            value=st.session_state['gemini_api_key'],
            type="password",
            placeholder="AIzaSy..."
        )
        if api_key_input != st.session_state['gemini_api_key']:
            st.session_state['gemini_api_key'] = api_key_input

        st.caption("Uses our 2M-Token In-Context Semitic Grammar Prompt zero-shot.")
        st.divider()
        st.markdown("**Mountain Ambience Audio**")
        st.caption("Qalamoun Field Ambience (#1974-04)")
        # Audio simulator
        st.audio("https://actions.google.com/sounds/v1/ambiences/outdoor_field_wind.ogg")

# Main Editorial Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📖 TAB 1: LEARN  (Tri-Dialect Phrasebook)",
    "🎨 TAB 2: PLAY  (Generative Studio & Woolaroo Camera)",
    "🔬 TAB 3: WORK  (AI Epigraphy & Researcher Workbench)"
])

# ==============================================================================
# TAB 1: LEARN (Tri-Dialect Phrasebook) — Cleaned, Spacious & Progressive Disclosure
# ==============================================================================
with tab1:
    st.markdown("### Tri-Dialect Western Neo-Aramaic Phrasebook")
    st.caption("Compare living Western Neo-Aramaic across three highland villages of Qalamoun. Powered by our 2M-Token In-Context Semitic Grammar Prompt zero-shot.")
    
    # Clean Phrase Picker Row
    phrase_keys = list(siryon_data.PHRASEBOOK_CORPUS.keys())
    phrase_titles = [siryon_data.PHRASEBOOK_CORPUS[k]["title"] for k in phrase_keys]
    selected_idx = phrase_keys.index(st.session_state['selected_phrase_id']) if st.session_state['selected_phrase_id'] in phrase_keys else 0
    
    chosen_title = st.selectbox(
        "Select Qalamoun Phrase or Tradition:",
        options=phrase_titles,
        index=selected_idx,
        key="phrase_selector"
    )
    chosen_key = phrase_keys[phrase_titles.index(chosen_title)]
    st.session_state['selected_phrase_id'] = chosen_key
    phrase_data = siryon_data.PHRASEBOOK_CORPUS[chosen_key]

    # Literal translation banner
    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px 18px; margin-bottom:18px;">
            <span style="font-weight:600; color:#475569;">English Translation:</span> 
            <span style="font-size:1.05rem; color:#0f172a;">"{phrase_data['english_literal']}"</span>
            &nbsp;•&nbsp;
            <span style="font-size:0.88rem; color:#64748b; font-family:'JetBrains Mono',monospace;">{phrase_data['semitic_root_summary']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Mode Selector: View All 3 Side-by-Side OR Single Dialect Deep Dive
    view_mode = st.radio(
        "Display Mode:",
        options=["Side-by-Side Comparison (All 3 Dialects)", "Maaloula Only (Christian/Monastic)", "Jubb'adin Only (Oral Poetry)", "Bakh'a Only (Archaic Mountain)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    dialects = phrase_data["dialects"]
    
    # Render Dialect Cards
    if view_mode.startswith("Side-by-Side"):
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            m = dialects["maaloula"]
            st.markdown(
                f"""
                <div class="card-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-weight:700; font-size:1.15rem;">⛪ Maaloula</span>
                        <span class="dialect-badge-m">{m['badge']}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#64748b; margin-bottom:12px;">{m['sub_label']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Estrangelo Script</div>
                    <div class="syriac-display">{m['syriac_script']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Adapted Arabic Script</div>
                    <div class="arabic-display">{m['adapted_arabic']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">IPA Phonetic Cadence</div>
                    <div class="ipa-display">{m['ipa']}</div>
                    
                    <div class="law-pill"><strong>Phonological Shift:</strong> {m['phonological_note']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔊 Play Syllable Guide (Maaloula)", key="m_aud"):
                st.toast(f"Maaloula Phonetics: {m['audio_hint']}", icon="🔊")

        with d_col2:
            j = dialects["jubbadin"]
            st.markdown(
                f"""
                <div class="card-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-weight:700; font-size:1.15rem;">🌾 Jubb'adin</span>
                        <span class="dialect-badge-j">{j['badge']}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#64748b; margin-bottom:12px;">{j['sub_label']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Estrangelo Script</div>
                    <div class="syriac-display">{j['syriac_script']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Adapted Arabic Script</div>
                    <div class="arabic-display">{j['adapted_arabic']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">IPA Phonetic Cadence</div>
                    <div class="ipa-display">{j['ipa']}</div>
                    
                    <div class="law-pill"><strong>Phonological Shift:</strong> {j['phonological_note']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔊 Play Syllable Guide (Jubb'adin)", key="j_aud"):
                st.toast(f"Jubb'adin Phonetics: {j['audio_hint']}", icon="🔊")

        with d_col3:
            b = dialects["bakha"]
            st.markdown(
                f"""
                <div class="card-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-weight:700; font-size:1.15rem;">🏔️ Bakh'a</span>
                        <span class="dialect-badge-b">{b['badge']}</span>
                    </div>
                    <div style="font-size:0.82rem; color:#64748b; margin-bottom:12px;">{b['sub_label']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Estrangelo Script</div>
                    <div class="syriac-display">{b['syriac_script']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Adapted Arabic Script</div>
                    <div class="arabic-display">{b['adapted_arabic']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">IPA Phonetic Cadence</div>
                    <div class="ipa-display">{b['ipa']}</div>
                    
                    <div class="law-pill"><strong>Phonological Shift:</strong> {b['phonological_note']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔊 Play Syllable Guide (Bakh'a)", key="b_aud"):
                st.toast(f"Bakh'a Phonetics: {b['audio_hint']}", icon="🔊")
    else:
        # Single focused card view
        d_key = "maaloula" if "Maaloula" in view_mode else ("jubbadin" if "Jubb'adin" in view_mode else "bakha")
        single = dialects[d_key]
        st.markdown(
            f"""
            <div class="card-box" style="max-width:800px; margin:0 auto;">
                <div style="font-size:1.25rem; font-weight:700; color:#0f172a;">{single['name']}</div>
                <div style="font-size:0.88rem; color:#64748b; margin-bottom:16px;">{single['sub_label']}</div>
                <div style="font-size:0.78rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Script</div>
                <div class="syriac-display" style="font-size:2.1rem;">{single['syriac_script']}</div>
                <div style="font-size:0.78rem; font-weight:700; color:#64748b; text-transform:uppercase;">Adapted Arabic Script</div>
                <div class="arabic-display" style="font-size:1.75rem;">{single['adapted_arabic']}</div>
                <div style="font-size:0.78rem; font-weight:700; color:#64748b; text-transform:uppercase;">IPA Phonetic Cadence</div>
                <div class="ipa-display" style="font-size:1.15rem;">{single['ipa']}</div>
                <div class="law-pill"><strong>Phonological Shift:</strong> {single['phonological_note']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Progressive Disclosure Expanders so screen stays uncluttered
    with st.expander("🔬 Morphological Token Decomposition & Semitic Root Cognate Matrix"):
        st.write("Decomposition of Semitic triliteral roots and cross-linguistic cognates across Syriac, Hebrew, and Arabic.")
        st.table(pd.DataFrame(phrase_data["tokens_breakdown"]))

    with st.expander("🔍 Inspect 2M-Token In-Context Semitic Grammar Prompt Template"):
        st.code(
            siryon_data.SEMITIC_GRAMMAR_PROMPT_TEMPLATE.format(query=phrase_data["english_literal"]),
            language="plaintext"
        )
        if st.session_state['gemini_api_key']:
            if st.button("⚡ Execute Live Zero-Shot Prompt with Gemini API"):
                with st.spinner("Calling Gemini API..."):
                    res = call_gemini_grammar_prompt(st.session_state['gemini_api_key'], phrase_data["english_literal"])
                    if res:
                        st.info(res)


# ==============================================================================
# TAB 2: PLAY (Generative Studio & Woolaroo Camera) — Clean Sub-Navigation
# ==============================================================================
with tab2:
    play_sub = st.radio(
        "Choose Play Studio Mode:",
        options=["📷 Woolaroo Levantine Object Camera", "📜 The Aramaic Story Weaver (Bilingual Folktale Studio)"],
        horizontal=True
    )

    if "Woolaroo" in play_sub:
        st.markdown("### 📷 Woolaroo Levantine Object Discovery")
        st.caption("Select a Levantine highland artifact to inspect its visual Aramaic cards across Syriac, Adapted Arabic, and IPA script.")

        # Sleek 5-item pill bar
        w_pills = st.columns(len(siryon_data.WOOLAROO_OBJECTS))
        for i, obj in enumerate(siryon_data.WOOLAROO_OBJECTS):
            with w_pills[i]:
                active = (st.session_state['selected_woolaroo_id'] == obj['id'])
                if st.button(
                    f"{obj['emoji']} {obj['title']}",
                    key=f"w_pill_{obj['id']}",
                    type="primary" if active else "secondary",
                    use_container_width=True
                ):
                    st.session_state['selected_woolaroo_id'] = obj['id']

        selected_obj = next(o for o in siryon_data.WOOLAROO_OBJECTS if o['id'] == st.session_state['selected_woolaroo_id'])

        # Clean 2-column museum exhibit card
        c_visual, c_meta = st.columns([1, 2.2])
        with c_visual:
            st.markdown(
                f"""
                <div style="border:1px solid #e2e8f0; border-radius:14px; padding:38px 20px; text-align:center; background:#fafaf9;">
                    <div style="font-size:5.5rem; margin-bottom:14px;">{selected_obj['emoji']}</div>
                    <div style="font-weight:700; font-size:1.25rem; color:#0f172a;">{selected_obj['title']}</div>
                    <div style="font-size:0.82rem; color:#b45309; font-weight:600; text-transform:uppercase; margin-top:6px;">{selected_obj['category']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_meta:
            st.markdown(
                f"""
                <div class="card-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:0.78rem; font-weight:700; color:#64748b; text-transform:uppercase;">Etymological Cognate Root</span>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:0.85rem; background:#f1f5f9; color:#0f172a; padding:4px 8px; border-radius:6px;">{selected_obj['root_cognate']}</span>
                    </div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Syriac Estrangelo Label</div>
                    <div class="syriac-display" style="font-size:2.0rem; padding:10px 16px;">{selected_obj['aramaic_name_syr']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Adapted Arabic Script Label</div>
                    <div class="arabic-display" style="font-size:1.55rem; padding:10px 16px;">{selected_obj['aramaic_name_arab']}</div>
                    
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">IPA Phonetic Cadence</div>
                    <div class="ipa-display">{selected_obj['ipa']}</div>
                    
                    <p style="margin-top:14px; font-size:0.95rem; color:#334155; line-height:1.5;"><strong>Cultural Significance:</strong> {selected_obj['desc']}</p>
                    <p style="font-size:0.9rem; color:#475569; font-style:italic;"><strong>Qalamoun Proverb:</strong> "{selected_obj['sample_sentence']}"</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"🔊 Listen to Pronunciation • {selected_obj['audio_phonetic']}", key="aud_wobj"):
                st.toast(f"Syllable cadence: {selected_obj['audio_phonetic']}", icon="🔊")

    else:
        st.markdown("### 📜 The Aramaic Story Weaver (Bilingual Folktale Studio)")
        st.caption("Weave Qalamoun mountain legends with Gemini AI in bilingual English and Western Neo-Aramaic verse.")

        s_col_l, s_col_r = st.columns([1, 1.3])
        with s_col_l:
            story_motif_titles = [m['title'] for m in siryon_data.FOLKTALE_MOTIFS]
            chosen_motif_title = st.selectbox("Select Traditional Qalamoun Oral Motif:", options=story_motif_titles)
            chosen_motif = next(m for m in siryon_data.FOLKTALE_MOTIFS if m['title'] == chosen_motif_title)

            custom_story_prompt = st.text_area(
                "Customize Folktale Narrative Prompt:",
                value=chosen_motif['prompt'],
                height=110
            )

            if st.button("✨ Weave Bilingual Levantine Folktale", type="primary", use_container_width=True):
                with st.spinner("Weaving story with Gemini..."):
                    ai_story = call_gemini_story_weaver(st.session_state['gemini_api_key'], custom_story_prompt)
                    if ai_story:
                        st.session_state['story_generated'] = ai_story
                    else:
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
        with s_col_r:
            if st.session_state['story_generated']:
                st.markdown(
                    f"""
                    <div class="card-box" style="background:#fafaf9;">
                        {st.session_state['story_generated']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.info("👈 Choose a motif or type a prompt and click **'Weave Bilingual Levantine Folktale'** to read your bilingual story.")


# ==============================================================================
# TAB 3: WORK (AI Epigraphy & Researcher Workbench) — PRESERVES ALL PROTOTYPE SPECIFICATIONS
# ==============================================================================
with tab3:
    st.markdown("### AI Epigraphy & MASC Researcher Workbench")
    st.caption("Heidelberg University Maaloula Aramaic Speech Corpus (MASC) • Ingestion, USM/Chirp Alignment & Elder Gold Standard Review")

    w_col1, w_col2 = st.columns([1, 1.8])

    with w_col1:
        st.markdown("#### Archival Audio Ingestion Deck")
        selected_tape_title = st.selectbox(
            "Select Archival Tape Reel:",
            options=[t["title"] for t in siryon_data.MASC_TAPES]
        )
        current_tape = next(t for t in siryon_data.MASC_TAPES if t["title"] == selected_tape_title)

        st.markdown(
            f"""
            <div style="border:1px solid #cbd5e1; background:#f8fafc; padding:14px 18px; border-radius:10px; margin-bottom:12px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:600; color:#0284c7;">REEL ID: {current_tape['tape_id']}</div>
                <div style="font-size:0.9rem; font-weight:600; color:#0f172a; margin-top:2px;">{current_tape['speaker']}</div>
                <div style="font-size:0.82rem; color:#475569;">Community: {current_tape['village']}</div>
                <div style="font-size:0.82rem; color:#16a34a; font-family:'JetBrains Mono',monospace;">Transfer Quality: {current_tape['snr']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # EXACT PROTOTYPE LINE: Audio simulator
        st.audio("https://actions.google.com/sounds/v1/ambiences/outdoor_field_wind.ogg")

        # EXACT PROTOTYPE LINE: Run Auto-Segmentation button
        if st.button("Run Auto-Segmentation & Chirp ASR Alignment", use_container_width=True, type="primary"):
            st.session_state['asr_run'] = True

        if st.session_state['gold_standard_approved']:
            with st.expander(f"📚 Heidelberg MASC Gold Standard Archive ({len(st.session_state['gold_standard_approved'])})", expanded=True):
                for gitem in st.session_state['gold_standard_approved']:
                    st.success(gitem)

    with w_col2:
        if st.session_state.get('asr_run', False):
            # EXACT PROTOTYPE SUBHEADER
            st.subheader("ASR Candidate Transcriptions & Confidence")

            # EXACT PROTOTYPE MARKDOWN
            st.markdown("""
            * **Candidate 1 (IPA Aligned - 96.4% Conf):** `/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/`
            * **Candidate 2 (Syriac Estrangelo - 94.1% Conf):** `ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ`
            * **Candidate 3 (Adapted Arabic - 98.2% Conf):** `بْشَيْنا تِيتُن لْقَرْيِتْنا حَلْواتا`
            """)

            # EXACT PROTOTYPE DIVIDER & SUBHEADER
            st.divider()
            st.subheader("Morphological Token Decomposition")

            # EXACT PROTOTYPE TABLE
            st.table([
                {"Token": "b-šayna", "Morpheme": "b- (in) + šayn-a (peace)", "Cognate": "Syr: ܒܫܝܢܐ | Heb: בְּשָׁלוֹם", "Status": "Verified"},
                {"Token": "ṯētun", "Morpheme": "√ʔ-t-y (come) - 2nd Pl. Perf", "Cognate": "Arab: أتيتم | Syr: ܐܬܝܬܘܢ", "Status": "Verified"},
                {"Token": "l-qaryēṯan", "Morpheme": "l- (to) + qary-ēṯ-an (our village)", "Cognate": "Arab: لقرية | Syr: ܠܩܪܝܬܐ", "Status": "Verified"}
            ])

            # EXACT PROTOTYPE COLUMNS & BUTTONS
            col_a, col_b = st.columns(2)
            if col_a.button("✅ Approve to MASC Gold Standard", type="primary"):
                st.session_state['gold_standard_approved'].append(
                    "/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/ • ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ"
                )
                st.toast("Approved to MASC Gold Standard Archive!", icon="✅")
            if col_b.button("🚩 Flag for Elder Review Circle"):
                st.toast("Flagged for Qalamoun Elder Review Circle", icon="🚩")
        else:
            st.info("👈 Click **'Run Auto-Segmentation & Chirp ASR Alignment'** on the archival tape deck panel to run USM/Chirp epigraphy alignment.")

# ==============================================================================
# EXACT PROTOTYPE FOOTER
# ==============================================================================
st.divider()
st.caption("Project Siryon Prototype • Built with Google Gemini 2.0 Flash & Argolis Vertex AI • Partnership with Enable Syria (`go/enable-syria`) & Heidelberg University")
st.caption("raghadalnouri@mpl-composed-augury-38028.c.googlers.com • expires in 15h 41m • Debug Bundle 2026.08.17.03_RC03")
