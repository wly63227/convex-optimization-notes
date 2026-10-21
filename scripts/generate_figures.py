"""Scientific figures; no source PDF screenshots are republished."""
from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/".runtime").exists():sys.path.insert(0,str(ROOT/".runtime"))
sys.path.insert(0,str(ROOT/"examples"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from models import ridge,step_sequence,central_point,huber,exact_gradient_path
OUT=ROOT/"docs"/"assets"
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,
 "axes.spines.right":False,"axes.grid":True,"grid.alpha":.16,"svg.fonttype":"path",
 "figure.facecolor":"white","axes.facecolor":"white","axes.prop_cycle":plt.cycler(color=["#176b62","#b35a32","#5368a8","#777777"])})

def save(fig,name):
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT/f"{name}.svg",metadata={"Date":None},bbox_inches="tight")
    fig.savefig(ROOT/"tmp"/f"{name}.png",dpi=135,bbox_inches="tight")
    plt.close(fig)

(ROOT/"tmp").mkdir(exist_ok=True)
fig,axs=plt.subplots(1,2,figsize=(8,3.7))
for ax in axs:
 ax.set(xlim=(-1.25,1.25),ylim=(-1.25,1.25),xlabel="$x_1$",ylabel="$x_2$")
 ax.set_aspect("equal")
 ax.add_patch(Circle((0,0),1,color="#176b62",alpha=.15))
 ax.plot([-.9,.9],[0,0],"o--",color="#b35a32")
axs[0].set_title("Convex disk")
axs[1].add_patch(Circle((0,0),.5,color="white",zorder=2))
axs[1].plot([-.9,.9],[0,0],"o--",color="#b35a32",zorder=3)
axs[1].set_title("Nonconvex annulus")
save(fig,"convex-sets")

fig,ax=plt.subplots(figsize=(7.2,4))
x=np.linspace(-1.3,2.3,350)
ax.plot(x,x*x,label="$f(x)=x^2$",lw=2)
ax.plot([-1,2],[1,4],"o--",label="Chord between -1 and 2")
ax.plot(x,2*x-1,":",label="Tangent at x=1",lw=2)
ax.set(xlabel="$x$",ylabel="Value",ylim=(-3,6))
ax.legend()
save(fig,"chord-tangent")

fig,ax=plt.subplots(figsize=(7.2,4))
ls=np.r_[0,np.logspace(-3,3,180)]
vals=[ridge(l) for l in ls]
ax.plot([v[1] for v in vals],[v[2] for v in vals],lw=2)
for lam in [0,1,10]:
 _,fit,size,_=ridge(lam)
 ax.plot(fit,size,"o")
 ax.annotate(f"$\\lambda={lam}$",(fit,size),xytext=(8,6),textcoords="offset points")
ax.set(xlabel="$\\|Ax-b\\|_2^2$",ylabel="$\\|x\\|_2^2$")
save(fig,"regularization")

fig,ax=plt.subplots(figsize=(7.2,4))
u=np.linspace(-2.5,2.5,400)
ax.plot(u,u*u,label="Square")
ax.plot(u,np.abs(u),"--",label="Absolute")
ax.plot(u,huber(u),":",lw=2.5,label="Huber, M=1")
ax.plot(u,np.maximum(0,np.abs(u)-.5),"-.",label="Deadzone, a=0.5")
ax.set(xlabel="Residual",ylabel="Penalty")
ax.legend()
save(fig,"penalties")

fig,axs=plt.subplots(1,2,figsize=(8,3.7))
z=np.linspace(-6,6,400)
axs[0].plot(z,1/(1+np.exp(-z)),lw=2)
axs[0].set(xlabel="Score z",ylabel="Probability of label 1",ylim=(-.03,1.03))
axs[1].plot(z,np.logaddexp(0,z),label="Label 0",lw=2)
axs[1].plot(z,np.logaddexp(0,z)-z,"--",label="Label 1",lw=2)
axs[1].set(xlabel="Score z",ylabel="Negative log-likelihood")
axs[1].legend()
save(fig,"logistic")

fig,ax=plt.subplots(figsize=(7.2,4))
x=np.linspace(.015,.985,400)
ax.plot(x,-np.log(x)-np.log(1-x),label="Each bound once")
ax.plot(x,-2*np.log(x)-np.log(1-x),"--",label="Lower bound twice")
ax.axvline(.5,ls=":",color="#176b62")
ax.axvline(2/3,ls=":",color="#b35a32")
ax.set(xlabel="$x$ in (0,1)",ylabel="Barrier",ylim=(1,9))
ax.legend()
save(fig,"analytic-center")

fig,ax=plt.subplots(figsize=(6.5,4))
x=np.linspace(-2,2,100)
ax.axvline(0,color="#176b62",label="Decision boundary")
ax.axvline(-1,color="#5368a8",ls="--",label="Margin boundaries")
ax.axvline(1,color="#5368a8",ls="--")
ax.scatter([-1,-1.5,-1.8],[-.7,.1,1],marker="x",s=70,label="Class -1")
ax.scatter([1,1.5,1.8],[.6,-.4,1],marker="o",s=45,label="Class +1")
ax.annotate("",(-1,-1.1),(1,-1.1),arrowprops={"arrowstyle":"<->","color":"#b35a32"})
ax.text(0,-1.35,"2 / ||a||",ha="center")
ax.set(xlim=(-2.3,2.3),ylim=(-1.6,1.6),xlabel="$z_1$",ylabel="$z_2$")
ax.set_aspect("equal")
ax.legend(loc="upper center",bbox_to_anchor=(.5,1.26),ncol=2,fontsize=8)
save(fig,"margin")

fig,ax=plt.subplots(figsize=(7.2,4))
xx,yy=np.meshgrid(np.linspace(-11,11,260),np.linspace(-4,4,220))
ax.contour(xx,yy,.5*(xx*xx+10*yy*yy),levels=[1,5,15,35,55,80],colors="#c4ced3")
path=exact_gradient_path()
ax.plot(path[:,0],path[:,1],"o-",markersize=3,label="Gradient + exact line search")
ax.plot([10,0],[1,0],"s--",markersize=5,label="Newton, full step")
ax.set(xlabel="$x_1$",ylabel="$x_2$",xlim=(-1.5,11),ylim=(-1.8,1.8))
ax.set_aspect("equal",adjustable="box")
ax.legend(loc="lower left",fontsize=9)
save(fig,"descent")

fig,ax=plt.subplots(figsize=(7.2,4))
for eta,style in zip([.25,.5,1,1.1],["-","--",":","-."]):
 p=step_sequence(eta)
 ax.plot([q["k"] for q in p],[q["error"] for q in p],style,marker="o",markersize=3,label=f"eta={eta}")
ax.set(xlabel="Iteration k",ylabel="Absolute error |x-2|",xticks=range(9))
ax.legend()
save(fig,"step-sizes")

fig,ax=plt.subplots(figsize=(7.2,4))
x=np.linspace(1.006,2.4,500)
for t,style in zip([1,3,10],["-","--",":"]):
 y=x*x-np.log(x-1)/t
 ax.plot(x,y,style,label=f"t={t}")
 c=central_point(t)
 ax.plot(c,c*c-np.log(c-1)/t,"o")
ax.axvline(1,color="#777777",ls="-.")
ax.set(xlabel="$x > 1$",ylabel="$x^2-\\log(x-1)/t$",ylim=(.5,8))
ax.legend()
save(fig,"barrier")
print("Generated 10 SVG figures and temporary PNGs for visual QA.")
