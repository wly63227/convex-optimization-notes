from pathlib import Path
import csv,json,re,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"
parser=argparse.ArgumentParser()
parser.add_argument("--write-baseline",action="store_true")
parser.add_argument("--allow-missing-sources",action="store_true",help="CI only: do not claim verification of absent private source PDFs")
args=parser.parse_args()
manifest=json.loads((ROOT/"sources/manifest.json").read_text(encoding="utf-8"))
actual={p.name for p in ROOT.glob("*.pdf")}
expected={x["file"] for x in manifest}
assert actual<=expected,"New PDF detected: run source investigation first"
if not args.allow_missing_sources:assert actual==expected,"PDF missing: run source investigation first"
verified_sources=0
for x in manifest:
    if x["file"] not in actual:continue
    assert hashlib.sha256((ROOT/x["file"]).read_bytes()).hexdigest()==x["sha256"],"source changed: "+x["file"]
    verified_sources+=1
topics=list(csv.DictReader((ROOT/"sources/topics.tsv").open(encoding="utf-8"),delimiter="\t"))
assert len({x["id"] for x in topics})==len(topics)
pages_path=ROOT/"sources/pages.json"
if pages_path.exists():
    pages=json.loads(pages_path.read_text(encoding="utf-8"))
    assert [x["page"] for x in pages]==list(range(1,403))
    assert all(x["coverage"] in ["mapped","structural"] and x["visual_review"]!="pending" for x in pages)
else:
    assert args.allow_missing_sources,"pages.json absent: rebuild the source inventory"
    pages=[None]*json.loads((ROOT/"sources/stats.json").read_text(encoding="utf-8"))["lecture_pages"]
    assert len(re.findall(r'<span id="pdf-\d+">',(DOCS/"coverage.md").read_text(encoding="utf-8")))==402
for x in topics:
    assert "{#"+x["anchor"]+"}" in (DOCS/(x["file"]+".md")).read_text(encoding="utf-8"),x

snapshot={"chapters":{},"knowledge_ids":[x["id"] for x in topics],
 "original_beginner_sha256":hashlib.sha256((ROOT/"凸优化从零开始学习笔记.md").read_bytes()).hexdigest()}
mds=list(DOCS.glob("*.md"))
for path in mds:
    s=path.read_text(encoding="utf-8")
    assert "\ufffd" not in s,path
    assert len(re.findall(r"^\$\$$",s,re.M))%2==0,("math delimiter",path)
    assert len(re.findall(r"^~~~",s,re.M))%2==0,("code fence",path)
    stack=[]
    for kind,env in re.findall(r"\\(begin|end)\{([^}]+)\}",s):
        if kind=="begin":stack.append(env)
        else:assert stack and stack.pop()==env,(path,env)
    assert not stack,path
    link_text=re.sub(r"~~~.*?~~~","",s,flags=re.S)
    link_text=re.sub(r"^\$\$\n.*?^\$\$","",link_text,flags=re.M|re.S)
    link_text=re.sub(r"\$[^$\n]*\$","",link_text)
    for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)",link_text):
        if "://" in link or link.startswith("mailto:"):continue
        name,_,anchor=link.partition("#")
        target=(path.parent/name).resolve() if name else path
        assert target.exists(),("missing link",path.name,link)
        if anchor and target.suffix==".md":
            ts=target.read_text(encoding="utf-8")
            assert "{#"+anchor+"}" in ts or 'id="'+anchor+'"' in ts,("anchor",path.name,link)
    if path.stem[:2].isdigit() or path.stem=="appendix-numerics":
        snapshot["chapters"][path.name]={
          "characters":len(s),
          "anchors":re.findall(r"\{#([^}]+)\}",s),
          "formulas":[hashlib.sha256(m.strip().encode()).hexdigest() for m in re.findall(r"^\$\$\n(.*?)^\$\$",s,re.M|re.S)]}
baseline=ROOT/"sources/baseline.json"
if args.write_baseline:
    baseline.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Baseline explicitly written; review this change before committing.")
elif baseline.exists():
    old=json.loads(baseline.read_text(encoding="utf-8"))
    assert old["original_beginner_sha256"]==snapshot["original_beginner_sha256"],"original beginner notes modified"
    assert set(old["knowledge_ids"])<=set(snapshot["knowledge_ids"]),"knowledge IDs removed"
    for name,b in old["chapters"].items():
        n=snapshot["chapters"].get(name);assert n,("chapter removed",name)
        assert n["characters"]>=b["characters"]*.95,("unexpected content reduction",name)
        assert set(b["anchors"])<=set(n["anchors"]),("stable anchor removed",name)
        assert set(b["formulas"])<=set(n["formulas"]),("formula changed/removed: inspect and deliberately update baseline",name)
else:
    print("No baseline yet: initialize explicitly after final review.")
summary={"markdown_files":len(mds),"knowledge_points":len(topics),"lecture_pages":len(pages),"source_hashes_verified":verified_sources,"status":"passed"}
(ROOT/"results").mkdir(exist_ok=True)
(ROOT/"results/content-checks.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary))
