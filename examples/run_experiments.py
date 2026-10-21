"""Run from any directory. Uses fixed, supplied-in-code data; no downloads."""
from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/".runtime").exists():sys.path.insert(0,str(ROOT/".runtime"))
from models import ridge, step_sequence, central_point
RESULTS=ROOT/"results"
RESULTS.mkdir(exist_ok=True)
data={"data_source":"self-authored deterministic teaching examples","randomness":"none",
      "ridge":{},"steps":{},"central_path":[]}
for lam in [0.,1.]:
    x,fit,size,value=ridge(lam)
    data["ridge"][str(lam)]={"x":x.tolist(),"fit_squared":fit,"size_squared":size,"objective":value}
for eta in [.25,.5,1.,1.1]:
    data["steps"][str(eta)]=step_sequence(eta)
for t in [1.,10.,100.]:
    x=central_point(t)
    lam=1/(t*(x-1))
    dual=lam-lam*lam/4
    data["central_path"].append({"t":t,"x":x,"multiplier":lam,"gap":x*x-dual,"theory_gap":1/t})
(RESULTS/"experiments.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print("Wrote results/experiments.json; ridge and central-path examples evaluated.")
