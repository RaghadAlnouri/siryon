#!/usr/bin/env python3
import argparse, collections, glob, json, os, random, re, sqlite3, subprocess
import sys, urllib.error, urllib.request

MODEL=os.environ.get("MODEL","gemini-3.1-pro-preview")
KEY=os.environ.get("GEMINI_API_KEY"); PROJECT=os.environ.get("GOOGLE_CLOUD_PROJECT")
LOC=os.environ.get("GOOGLE_CLOUD_LOCATION","us-central1")
if KEY:
    URL=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"
    HDR={"Content-Type":"application/json"}
elif PROJECT:
    tk=subprocess.check_output(["gcloud","auth","print-access-token"],text=True).strip()
    URL=(f"https://{LOC}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOC}"
         f"/publishers/google/models/{MODEL}:generateContent")
    HDR={"Content-Type":"application/json","Authorization":f"Bearer {tk}"}
else: sys.exit("Set GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT")

def call(p):
    b=json.dumps({"contents":[{"role":"user","parts":[{"text":p}]}],
                  "generationConfig":{"temperature":0.0}}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(URL,data=b,headers=HDR),timeout=300) as r:
            d=json.load(r)
    except urllib.error.HTTPError as e: return f"[HTTP {e.code}] {e.read().decode()[:200]}"
    except Exception as e: return f"[err] {e}"
    c=d.get("candidates") or []
    return "".join(x.get("text","") for x in c[0]["content"]["parts"]) if c else "[none]"

def parse(t):
    m=re.search(r"\[.*\]",t,re.S)
    try: return json.loads(m.group(0)) if m else []
    except Exception: return []

def load(db):
    c=sqlite3.connect(db)
    rows=c.execute("""select s.sentence_id,s.full_sentence,t.token_id,t.token_form,
        l.citation_form,l.root from Tokens t
        join Sentences s on t.sentence=s.sentence_id
        join Types ty on t.type=ty.type_id
        join Lemmas l on ty.lemma=l.lemma_id
        order by s.sentence_id,t.token_id""").fetchall()
    S=collections.OrderedDict()
    for sid,full,_,form,lem,root in rows:
        S.setdefault(sid,{"text":full,"toks":[]})
        S[sid]["toks"].append({"form":form,"lemma":lem or "","root":root or ""})
    return S

TASK="""You are analysing Maaloula Aramaic (Western Neo-Aramaic) in scholarly
Latin transliteration. For EVERY token of the sentence below give:
  token, lemma (dictionary citation form), root (consonantal root e.g. "sh-y-n";
  "" for particles/proper nouns), confidence ("high"/"medium"/"low").
Return ONLY a JSON array, no prose, no markdown fence:
[{"token":"...","lemma":"...","root":"...","confidence":"high"}]"""

def gold_str(s): return " ".join(f"{t['form']}<{t['lemma']}|{t['root']}>" for t in s["toks"])
def prompt(s,ex):
    p=""
    if ex:
        p+="Annotated examples from the same corpus, format token<lemma|root>.\nAlternate lemmas separated by '/'.\n\n"
        p+="\n".join(gold_str(e) for e in ex)+"\n\n"+"="*60+"\n\n"
    return p+TASK+"\n\nSENTENCE\n"+s["text"]+"\n"

def nm(x): return (x or "").strip().lower().replace("-","").replace(" ","")
def ok(p,g): return any(nm(p)==nm(a) for a in str(g).split("/") if a.strip())

def score(S,P,seen):
    st={"lemma":[0,0],"root":[0,0],"seen":[0,0],"unseen":[0,0],"hi":0,"hiw":0}
    for sid,pred in P.items():
        by={}
        for p in pred:
            if isinstance(p,dict) and p.get("token"): by.setdefault(str(p["token"]),p)
        for g in S[sid]["toks"]:
            p=by.get(g["form"]); L=bool(p) and ok(p.get("lemma"),g["lemma"])
            st["lemma"][1]+=1; st["lemma"][0]+=L
            if g["root"]:
                st["root"][1]+=1; st["root"][0]+= bool(p) and ok(p.get("root"),g["root"])
            k="seen" if g["form"] in seen else "unseen"
            st[k][1]+=1; st[k][0]+=L
            if p and str(p.get("confidence","")).lower()=="high":
                st["hi"]+=1; st["hiw"]+= (not L)
    return st

def pc(a,b): return f"{100.0*a/b:5.1f}%  ({a}/{b})" if b else "   n/a"
def rep(n,st):
    print(f"\n--- {n} ---")
    print(f"  lemma accuracy       {pc(*st['lemma'])}")
    print(f"  root  accuracy       {pc(*st['root'])}")
    print(f"  lemma, SEEN types    {pc(*st['seen'])}")
    print(f"  lemma, UNSEEN types  {pc(*st['unseen'])}   <-- the real test")
    if st["hi"]: print(f"  'high confidence' but WRONG: {pc(st['hiw'],st['hi'])}")

a=argparse.ArgumentParser()
a.add_argument("--test",type=int,default=60); a.add_argument("--train",type=int,default=40)
a.add_argument("--min-tok",type=int,default=5); a.add_argument("--max-tok",type=int,default=18)
a.add_argument("--seed",type=int,default=20260821); A=a.parse_args()

db=glob.glob("**/aramaic_corpus.db",recursive=True)
if not db: sys.exit("aramaic_corpus.db not found")
S=load(db[0]); print(f"loaded {len(S)} sentences")
use=[s for s in S if A.min_tok<=len(S[s]["toks"])<=A.max_tok]
random.Random(A.seed).shuffle(use)
tr,te=use[:A.train],use[A.train:A.train+A.test]
ex=[S[i] for i in tr]; seen={t["form"] for i in tr for t in S[i]["toks"]}
nt=sum(len(S[i]["toks"]) for i in te)
nu=sum(1 for i in te for t in S[i]["toks"] if t["form"] not in seen)
print(f"train {len(tr)} | test {len(te)} ({nt} tokens, {nu} unseen)\nmodel {MODEL}\n")

out={}
for cond,E in (("A_zero_shot",[]),("B_in_context",ex)):
    P={}
    for n,sid in enumerate(te,1):
        P[sid]=parse(call(prompt(S[sid],E)))
        print(f"\r  {cond}: {n}/{len(te)}",end="",flush=True)
    print(); out[cond]={"stats":score(S,P,seen),
                        "preds":{str(k):v for k,v in P.items()}}
    rep(cond,out[cond]["stats"])
json.dump({"model":MODEL,"results":out},open("bench_results.json","w"),
          ensure_ascii=False,indent=2)
print("\nsaved bench_results.json")
