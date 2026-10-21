"""Independent analytic and numerical checks for published examples."""
from pathlib import Path
import sys, re, json, io, contextlib
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/".runtime").exists():sys.path.insert(0,str(ROOT/".runtime"))
sys.path.insert(0,str(ROOT/"examples"))
import numpy as np
from models import A,B,ridge,step_sequence,central_point,tv_step,exact_gradient_path
checks=[]
def check(name,condition):
    if not bool(condition):raise AssertionError(name)
    checks.append(name)
def near(a,b,tol=1e-9):return np.allclose(a,b,atol=tol,rtol=tol)

for lam,expected,value in [(0,[2/3,5/3],1/6),(1,[5/8,9/8],21/16)]:
    x,fit,size,obj=ridge(lam)
    check(f"ridge lambda={lam}: analytic coefficients",near(x,expected))
    check(f"ridge lambda={lam}: gradient",near(A.T@(A@x-B)+lam*x,0))
    check(f"ridge lambda={lam}: objective",near(obj,value))
for eta in [.25,.5,.75,1.,1.1]:
    seq=step_sequence(eta)
    check(f"step recurrence eta={eta}",all(near(p["x"]-2,-2*(1-2*eta)**p["k"]) for p in seq))
for t in [.5,1.,10.,100.]:
    x=central_point(t);lam=1/(t*(x-1))
    check(f"central t={t}: stationarity",near(2*t*x-1/(x-1),0))
    check(f"central t={t}: gap",near(x*x-(lam-lam*lam/4),1/t))

# Logistic gradient, independently differentiated by symmetric differences.
U=np.array([[1.,0.,1.],[-1.,2.,1.],[.5,1.,1.]])
y=np.array([1.,0.,1.]);theta=np.array([.2,-.3,.1])
def loss(th):
    z=U@th
    return float(np.sum(np.logaddexp(0,z)-y*z))
z=U@theta;p=1/(1+np.exp(-z))
g=U.T@(p-y)
eps=1e-5
fd=np.array([(loss(theta+eps*np.eye(3)[i])-loss(theta-eps*np.eye(3)[i]))/(2*eps) for i in range(3)])
check("logistic: finite-difference gradient",near(g,fd,1e-7))
H=U.T@np.diag(p*(1-p))@U
check("logistic: PSD Hessian",np.linalg.eigvalsh(H).min()>-1e-12)

# TV optimum is certified by an explicit subgradient, not by our solver.
D=np.array([[-1.,1.,0.,0.],[0.,-1.,1.,0.],[0.,0.,-1.,1.]])
obs=np.array([0.,0.,2.,2.])
for lam in [.25,1.,2.,3.]:
    x=tv_step(lam)
    s=np.array([.5,1.,.5]) if lam<=2 else np.array([1.,2.,1.])/lam
    check(f"TV lambda={lam}: stationarity",near(x-obs+lam*D.T@s,0))
    check(f"TV lambda={lam}: valid subgradient",all(abs(si)<=1+1e-12 and (abs(di)<1e-12 or near(si,np.sign(di))) for di,si in zip(D@x,s)))

pp=np.array([.7,.2,.05,.05]);qq=np.array([.1,.1,.7,.1]);det=np.array([1.,2/3,0.,0.])
check("detector: equal minimax errors",near([pp@(1-det),qq@det],[1/6,1/6]))
check("detector: scalar dual certificate",near(np.minimum(pp,2*qq).sum(),.5))
M=np.eye(2)/2;W=np.eye(2)
check("D-optimal: primal/dual equality",near(-np.linalg.slogdet(M)[1],np.linalg.slogdet(W)[1]+2*np.log(2)))
V=np.array([[1,.5,0],[1,.8,0],[1,1,1],[1,1.3,4.]])
price=np.array([1,.9,.3]);x=np.array([6.2,-7.7,1.5])
check("arbitrage: exact displayed input",near(price@x,-.28) and np.min(V@x)>-1e-12)
rn=np.array([11/30,7/30,3/10,1/10])
check("arbitrage: precise risk-neutral distribution",near(V.T@rn,[1,.8,.7]) and near(rn.sum(),1))
check("Schur: hand example",near(np.array([[2,1],[1,3]])@np.array([.2,.6]),[1,2]))

P=np.diag([1.,0.]);eq=np.array([[0.,1.]])
K=np.block([[P,eq.T],[eq,np.zeros((1,1))]])
solution=np.linalg.solve(K,[0,0,1])
check("KKT: singular Hessian / invertible KKT",near(solution,[0,1,0]))
diag=np.diag([2.,3.,4.]);L=np.array([[1.],[2.],[-1.]])
rhs=np.array([1.,-2.,3.]);di=np.linalg.solve(diag,np.eye(3))
wood=di-di@L@np.linalg.solve(np.eye(1)+L.T@di@L,L.T@di)
check("Woodbury: direct solve comparison",near(wood@rhs,np.linalg.solve(diag+L@L.T,rhs)))
path=exact_gradient_path()
val=lambda x:.5*(x[0]**2+10*x[1]**2)
check("exact line search: objective decreases",all(val(a)>val(b) for a,b in zip(path,path[1:])))
check("GP scaling: analytic minimum",near(4*(1/np.sqrt(2))**2+(1/np.sqrt(2))**-2,4))
check("analytic center: repeated lower bound",-2/(2/3)+1/(1-2/3)<1e-10)
check("self-concordance erratum: wrong formula not convex",1/.75**2-1/(1-.75)**2<0)

# Execute only the three self-authored standalone snippets in the experiment page.
text=(ROOT/"docs/experiments.md").read_text(encoding="utf-8")
blocks=re.findall(r"~~~python\n(.*?)\n~~~",text,re.S)
check("standalone snippet count",len(blocks)==3)
for i,code in enumerate(blocks,1):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code,f"published_example_{i}","exec"),{})
    checks.append(f"published standalone example {i}: executed")

out=ROOT/"results";out.mkdir(exist_ok=True)
(out/"math-checks.json").write_text(json.dumps({"passed":len(checks),"checks":checks},ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Passed {len(checks)} mathematical and executable-example checks.")
