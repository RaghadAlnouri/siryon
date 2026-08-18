# 🏛️ Project Siryon: Living Western Neo-Aramaic Portal

**Project Siryon** is an interactive, living web application dedicated to the preservation, linguistic analysis, visual object discovery, and AI epigraphy of **Western Neo-Aramaic** (*Līšānā ʾArāmāyā*), the sole surviving descendant of the Aramaic dialects spoken across the ancient Levant 2,000 years ago. Today, Western Neo-Aramaic survives in three highland villages in the Anti-Lebanon (Qalamoun) mountain range of Syria:
* **Maaloula** (Christian / Monastic quarter)
* **Jubb'adin** (Oral Poetry & Agrarian community)
* **Bakh'a** (Archaic High-Altitude Mountain dialect)

Built with **Streamlit**, **Google Gemini 2.0 Flash / Vertex AI**, and designed in partnership with **Enable Syria (`go/enable-syria`)** and **Heidelberg University’s Maaloula Aramaic Speech Corpus (MASC)**.

---

## 🏗️ Interactive Architecture (The Three Tabs)

### 📖 Tab 1: LEARN (Tri-Dialect Phrasebook & 2M-Token In-Context Semitic Grammar Engine)
* **2M-Token In-Context Semitic Grammar Prompt Zero-Shot Engine**: Configurable with your `GEMINI_API_KEY` to run zero-shot morphological and phonetic synthesis across all three Qalamoun dialects.
* **Side-by-Side Dialect Cards**: Displays parallel cards for **Maaloula**, **Jubb'adin**, and **Bakh'a**:
  * Exact **Syriac Estrangelo script** with vowel diacritics
  * **Adapted Arabic script** with Qalamoun phonological vowel marks
  * **IPA phonetic transliteration** highlighting phonological shifts (e.g., interdental retention `/ṯ/` in Maaloula vs. stop merger `/t/` in Jubb'adin; Canaanite back-vowel shift `/ā/ → /ō/` in Bakh'a)
  * **Audio pronunciation guide & phonological laws**
* **Comparative Semitic Root Etymology Matrix**: Decomposes triliteral roots (`√š-y-n`, `√ʔ-t-y`, `√q-r-y`, `√z-y-t`, `√l-ḥ-m`) and cross-links cognates in Classical Syriac, Biblical/Mishnaic Hebrew, and Classical Arabic.

### 🎨 Tab 2: PLAY (Generative Studio & Woolaroo Camera)
* **📷 Woolaroo Levantine Object Simulator**:
  * Users pick real Levantine cultural artifacts (*Traditional Tannour Flatbread*, *Ancient Terraced Olive Tree*, *Saint Thecla's Mountain Gorge / Faj Maaloula*, *Ancient Basalt Grape Press*, *Traditional Qalamoun Wool Blanket*).
  * Displays visual cultural cards with multi-script Aramaic labels, IPA cadence, root etymology, and Qalamoun daily life usage.
* **📜 The Aramaic Story Weaver (Bilingual Folktale Studio)**:
  * Select traditional Qalamoun folktale motifs (*The Shepherd & The Speaking Cedar on Mount Hermon*, *The Wise Elder of the Golden Olive Harvest*, *The Three Echoes of Saint Thecla's Gorge*) or enter custom folktale prompts.
  * Weaves bilingual English & Western Neo-Aramaic folktales with interlinear Syriac/Arabic proverbs.

### 🔬 Tab 3: WORK (AI Epigraphy & Researcher Workbench)
* **Heidelberg University MASC Tape Ingestion Simulator**:
  * Simulates ingesting analog audio tapes from Heidelberg University’s Maaloula Aramaic Speech Corpus (`Reel #1974-04B: Elder Boutros on the 1950 Winter Harvest`, `Reel #1981-12A: Jubb'adin Wedding Quatrain`).
* **Chirp / USM Candidate ASR Alignment**:
  * Displays multi-modal ASR candidate alignments with confidence scores:
    * `Candidate 1 (IPA Aligned - 96.4% Conf):` `/ʔb-ˈʃajna ˈtʰeːtun l-qarˈjeːtʰan ˈħalwata/`
    * `Candidate 2 (Syriac Estrangelo - 94.1% Conf):` `ܒܫܰܝܢܳܐ ܐܶܬ݂ܰܝܬ݁ܽܘܢ ܠܩܰܪܝܺܬ݂ܰܢ ܚܰܠܘܳܬ݂ܳܐ`
    * `Candidate 3 (Adapted Arabic - 98.2% Conf):` `بْشَيْنا تِيتُن لْقَرْيِتْنا حَلْواتا`
* **Morphological Token Decomposition & Gold Standard Approval**:
  * Token-by-token breakdown (`b-šayna`, `ṯētun`, `l-qaryēṯan`).
  * **1-Click Gold Standard Approval (`✅ Approve to MASC Gold Standard`)** to record alignments into the archival ledger or **Flag for Elder Review Circle (`🚩 Flag for Elder Review Circle`)**.

---

## 🚀 Running Locally

1. **Clone or navigate to the repository**:
   ```bash
   cd siryon
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API Key (Optional for live zero-shot inference)**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Launch the web application**:
   ```bash
   streamlit run app.py
   ```

---

## 📑 Project Structure

* `app.py`: Main interactive Streamlit application implementing Tabs 1, 2, and 3.
* `siryon_data.py`: Multi-script Western Neo-Aramaic dialect corpus, Woolaroo object data, folktale motifs, and MASC analog audio tape simulations.
* `requirements.txt`: Python dependencies (`streamlit`, `google-genai`, `pandas`, `numpy`).
