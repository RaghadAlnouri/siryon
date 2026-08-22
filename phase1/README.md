# Phase 1 — Does a grammar in context help Gemini read Maaloula Aramaic?

A small, pre-registered benchmark on **Western Neo-Aramaic** (Maaloula dialect, ISO 639-3 `amw`) — the only surviving spoken descendant of Western Aramaic.

The question: for a language with effectively no training data, does supplying linguistic material **at inference time** make Gemini reliable enough to be useful to a scholarly archive?

---

## Result

Measured on **576 held-out tokens** (60 sentences), against the MASC gold standard. 40 annotated sentences supplied as in-context examples.

| Metric | Zero-shot | In-context | |
|---|---|---|---|
| Lemma accuracy | 38.7% | **57.6%** | |
| Root accuracy | 28.0% | **72.0%** | |
| Lemma, seen types | — | 70.9% | |
| **Lemma, unseen types** | 27.5% | **49.9%** | **gate ≥45% — cleared** |
| **Confident-error** | 45.1% | **29.2%** | **gate <25% — missed by 4.2 pts** |

Figures are lenient-scored (see *Scoring* below). Model: `gemini-3.1-pro-preview`, temperature 0, seed `20260821`.

### The pre-registered gate

Both thresholds were fixed on **21 August 2026, before the in-context run finished**:

> Unseen-word lemma accuracy must reach **45%**, *and* confident-error must
> fall below **25%**. Both, or stop.

**One cleared, one missed.** We are reporting it as it fell rather than moving the second bar afterwards.

### What the numbers mean

- **Unseen types are the real test.** These are word types absent from the in-context examples, so the 1.8× gain is not lookup.
- **Root accuracy is the strongest signal** — 28% → 72%. Consonantal roots are the deep structural layer of a Semitic language.
- **Confident-error is the honest problem.** In-context, the model asserts "high confidence" on 81% of tokens and is still wrong on 29% of those. It cannot tell you which. That is disqualifying for an archive, and it is the reason the reliability gate exists.

---

## Scripts

| File | What it does |
|---|---|
| `inventory.sh` | Downloads MASC (~830 MB) from Zenodo, unpacks it, inventories structure, licence and audio |
| `masc_bench.py` | The benchmark. Builds a held-out split from the SQLite gold standard, runs both arms, scores |
| `rescore.py` | Re-scores `bench_results.json` offline (strict vs lenient). No API calls |
| `probe.py` | A 5-item smoke test. Useful for checking connectivity; **not** a benchmark |

### Reproduce

```bash
bash inventory.sh  # once, ~830 MB
export GEMINI_API_KEY="..."  # or GOOGLE_CLOUD_PROJECT for Vertex
export MODEL=gemini-3.1-pro-preview
python3 -u masc_bench.py --test 60 --train 40
python3 rescore.py
```

Standard library only — no pip install. Both a public-API key and a Vertex service path are supported.

---

## Method

**Task.** Given a Maaloula Aramaic sentence in scholarly Latin transliteration, produce for every token: the lemma (dictionary citation form), the consonantal root, and a self-reported confidence.

**Gold standard.** MASC's SQLite database, joined Tokens → Types → Lemmas, giving citation form and root per token across 64,845 tokens / 5,484 sentences / 45 speakers.

**Arms.**
- **A — zero-shot.** Sentence only, no support material.
- **B — in-context.** 40 annotated sentences prepended.
- **C — grammar in context.** Not yet run. Blocked: Arnold's *Das Neuwestaramäische* Band 5 (Grammatik, 410 pp) exists only in print.

**Controls.** Test sentences are held out and never appear in the prompt. Accuracy is reported separately for seen and unseen word types — the latter separates generalisation from copying. Confidence is elicited per token so calibration is measured, not assumed.

---

## Scoring

MASC cites verbs as paired stems (`iḏmex yiḏmux`, `amar yīmar`). Zero-shot has no way to know that convention, so we report two scores:
- **Strict** — exact match against the full citation form.
- **Lenient** — accepts either stem of a paired citation.

The gap is instructive. Arm A gains ~5 points under lenient scoring; Arm B's scores are identical under both, because it learned the convention perfectly from the examples. So roughly 5 points of the apparent A→B gain was formatting, not linguistics. Headline figures above use lenient scoring, which is the fairer comparison.

---

## Data

Not redistributed in this repository. `inventory.sh` fetches it directly.

The Maaloula Aramaic Speech Corpus (MASC) — Ghattas Eid, Esther Seyffarth, Emad Rihan, Werner Arnold, Ingo Plag (Heinrich Heine University Düsseldorf).
- Data: https://doi.org/10.5281/zenodo.6496714
- Paper: https://aclanthology.org/2022.lrec-1.699/
- Licence: CC BY-NC 4.0 — non-commercial.

MASC digitises Arnold's printed transcriptions from *Das Neuwestaramäische* Bände III and IV, under permission obtained from Harrassowitz.

> ⚠️ The non-commercial term is real and it binds. This benchmark is research use. Any public-facing product built on this corpus needs an explicit reuse grant from the depositors.

---

## Limitations

Read these before citing anything above.
- **Arm C has not run.** The reliability gate was, in substance, a test of the grammar — and this run had 40 corpus examples instead. Arnold's grammar is the untested variable.
- **One dialect.** Maaloula only. Jubb'adin and Bakh'a are untested, and the three are genuinely distinct.
- **Small n.** 576 tokens, 363 unseen. The 49.9% figure carries a 95% CI of roughly ±5 points, whose lower bound brushes the 45% gate.
- **Self-reported confidence.** "High confidence" is the model's own label, not a calibrated probability.
- **The model already knows something.** Zero-shot identifies the language and cites the right scholarship unprompted. The gain here is reliability, not raw capability — see the confident-error column.

---

## Licence

Code in this directory: same licence as the parent repository. MASC is CC BY-NC 4.0 and is not included here.
