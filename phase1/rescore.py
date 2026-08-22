import json, glob, sqlite3, collections, random

d  = json.load(open("bench_results.json"))
db = glob.glob("**/aramaic_corpus.db", recursive=True)[0]
c  = sqlite3.connect(db)

rows = c.execute("""select s.sentence_id, t.token_id, t.token_form, l.citation_form, l.root
 from Tokens t join Sentences s on t.sentence=s.sentence_id
 join Types ty on t.type=ty.type_id join Lemmas l on ty.lemma=l.lemma_id
 order by s.sentence_id, t.token_id""").fetchall()
S = collections.OrderedDict()
for sid, tid, form, lem, root in rows:
    S.setdefault(sid, []).append({"form":form, "lemma":lem or "", "root":root or ""})

# reproduce the exact split used by masc_bench.py
usable = [s for s in S if 5 <= len(S[s]) <= 18]
random.Random(20260821).shuffle(usable)
train = usable[:40]
seen  = {t["form"] for i in train for t in S[i]}

def nm(x): return (x or "").strip().lower().replace("-","").replace(" ","")
def strict(p,g): return any(nm(p)==nm(a) for a in str(g).split("/") if a.strip())
def lenient(p,g):
    if strict(p,g): return True
    parts=[w for alt in str(g).split("/") for w in alt.split() if w.strip()]
    return any(nm(p)==nm(w) for w in parts)
def pc(a,b): return f"{100.0*a/b:5.1f}% ({a}/{b})" if b else "   n/a"

for cond, blob in d["results"].items():
    st = {k:[0,0] for k in ("ls","ll","us","ul")}
    hi = {"s":[0,0], "l":[0,0]}
    for sid, pred in blob["preds"].items():
        gold = S.get(int(sid))
        if not gold: continue
        by = {}
        for p in pred:
            if isinstance(p,dict) and p.get("token"): by.setdefault(str(p["token"]),p)
        for g in gold:
            p  = by.get(g["form"])
            ls = bool(p) and strict(p.get("lemma"), g["lemma"])
            ll = bool(p) and lenient(p.get("lemma"), g["lemma"])
            st["ls"][1]+=1; st["ls"][0]+=ls
            st["ll"][1]+=1; st["ll"][0]+=ll
            if g["form"] not in seen:
                st["us"][1]+=1; st["us"][0]+=ls
                st["ul"][1]+=1; st["ul"][0]+=ll
            if p and str(p.get("confidence","")).lower()=="high":
                hi["s"][1]+=1; hi["s"][0]+= (not ls)
                hi["l"][1]+=1; hi["l"][0]+= (not ll)
    print(f"\n=== {cond} ===")
    print(f"  lemma     strict {pc(*st['ls'])}   lenient {pc(*st['ll'])}")
    print(f"  UNSEEN    strict {pc(*st['us'])}   lenient {pc(*st['ul'])}   <- GATE 1 (>=45%)")
    print(f"  conf-error strict {pc(*hi['s'])}  lenient {pc(*hi['l'])}   <- GATE 2 (<25%)")
