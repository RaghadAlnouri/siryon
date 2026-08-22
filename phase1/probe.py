#!/usr/bin/env python3
import json, os, subprocess, sys, urllib.error, urllib.request

MODEL    = os.environ.get("MODEL", "gemini-2.5-pro")
KEY      = os.environ.get("GEMINI_API_KEY")
PROJECT  = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

SKETCH = """REFERENCE: Western Neo-Aramaic (Maaloula dialect)
Only surviving spoken descendant of WESTERN Aramaic. Three Qalamoun villages
in Syria: Maaloula, Jubb'adin, Bakh'a. NOT Assyrian Neo-Aramaic/Turoyo/Mandaic
(those are Eastern Aramaic).
PHONOLOGY: retains interdentals th/dh (Jubb'adin merges them to t/d); retains
pharyngeals h-dot and ayin; q is a uvular stop; long vowels take a macron.
MORPHOLOGY: Semitic triliteral roots. Nouns usually end -a. Feminines often
-tha/-etha. Possessives suffix to the noun: -an 'our', -ax 'your(sg)', -eh
'his'. Verb suffix -tun = 2nd person plural perfect.
PROCLITICS: b- 'in/with', l- 'to', d- relative/genitive, w- 'and'.
VOCAB: shayna peace (sh-y-n); qaryetha village (q-r-y); halwa sweet (h-l-w);
zayta olive (z-y-t); lahma bread (l-h-m); thetun 'you(pl) came'; tura
mountain; maya water."""

TASK = """For the Western Neo-Aramaic item below give:
1. TRANSLATION into English.
2. MORPHOLOGY token by token: consonantal root, prefixes, suffixes, and the
   grammatical function of each.
3. CONFIDENCE high/medium/low, and say what you are unsure of.
Be precise. If you do not know, say so. Do not invent cognates."""

ITEMS = [
 ("greeting-01", "b-shayna thetun l-qaryethan halwata",
  "in-peace you(pl).came to-village-our sweet ~ 'welcome to our lovely village'"),
 ("root-shyn", "shayna",   "'peace', root sh-y-n; cf Syriac shayna, Heb shalom"),
 ("root-qry",  "qaryetha", "'village', root q-r-y; fem ending -etha"),
 ("root-zyt",  "zayta",    "'olive', root z-y-t; cf Arabic zaytun"),
 ("root-lhm",  "lahma",    "'bread', root l-h-m; cf Heb lehem, Arabic lahm"),
]

if KEY:
    MODE = "apikey"
    URL  = (f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{MODEL}:generateContent?key={KEY}")
    HDR  = {"Content-Type": "application/json"}
elif PROJECT:
    MODE = "vertex"
    try:
        tok = subprocess.check_output(["gcloud","auth","print-access-token"],
                                      text=True, stderr=subprocess.PIPE).strip()
    except Exception as e:
        sys.exit(f"gcloud token failed -> run 'gcloud auth login'  ({e})")
    URL = (f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}"
           f"/locations/{LOCATION}/publishers/google/models/{MODEL}:generateContent")
    HDR = {"Content-Type":"application/json","Authorization":f"Bearer {tok}"}
else:
    sys.exit('Set GEMINI_API_KEY=... or GOOGLE_CLOUD_PROJECT=...')

def call(p):
    body = json.dumps({"contents":[{"role":"user","parts":[{"text":p}]}],
                       "generationConfig":{"temperature":0.0}}).encode()
    try:
        with urllib.request.urlopen(
                urllib.request.Request(URL, data=body, headers=HDR), timeout=180) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        return f"[HTTP {e.code}] {e.read().decode(errors='replace')[:600]}"
    except Exception as e:
        return f"[network error] {e}"
    c = d.get("candidates") or []
    if not c: return f"[no candidates] {json.dumps(d)[:400]}"
    return "".join(x.get("text","") for x in c[0]["content"]["parts"]).strip()

print(f"mode={MODE} model={MODEL}")
if "--check" in sys.argv:
    print(call("Reply with exactly: OK")); sys.exit()

out=[]
for i,(iid,latin,ref) in enumerate(ITEMS,1):
    print(f"\n{'='*70}\n[{i}/{len(ITEMS)}] {iid} -> {latin}\nreference: {ref}")
    a = call(f"{TASK}\n\nITEM\n  {latin}")
    print("\n--- A. ZERO-SHOT ---\n"+a)
    b = call(f"{SKETCH}\n{'='*70}\n\n{TASK}\n\nITEM\n  {latin}")
    print("\n--- B. IN-CONTEXT ---\n"+b)
    out.append({"id":iid,"zero_shot":a,"in_context":b})
json.dump(out, open("probe_results.json","w"), ensure_ascii=False, indent=2)
print("\nsaved probe_results.json")
