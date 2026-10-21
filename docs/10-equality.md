# 第 10 章：等式约束与不可行起点牛顿法

> 来源：讲义 PDF 第 327～352 页；教材第 10 章。假设 $f$ 凸且二阶连续可微，$A\in\mathbb R^{p\times n}$ 行满秩，问题最优值有限且取得。对具体线性系统还需要检查非奇异性。

## 从零空间消元理解约束 {#elimination}

考虑 $\min f(x),\ Ax=b$。与无约束问题不同，只有满足 $Ad=0$ 的方向才能从可行点继续保持可行。

找到一个特解 $\widehat x$ 和满列秩矩阵 $F\in\mathbb R^{n\times(n-p)}$，其列张成 $A$ 的零空间：

$$
x=\widehat x+Fz.
$$

优化变量变为 $z$，得到无约束问题 $\min_z f(\widehat x+Fz)$。它的梯度和 Hessian 为 $F^T\nabla f$ 与 $F^T\nabla^2fF$。

例如资源分配 $\sum_i x_i=B$，可以消去 $x_n=B-\sum_{i<n}x_i$。但显式形成零空间基可能破坏稀疏性，因此“变量更少”不必然计算更快。

## 二次问题的 KKT 矩阵何时可逆 {#kkt-matrix}

对 $\frac12x^TPx+q^Tx$，$P\succeq0$：

$$
\begin{bmatrix}P&A^T\\A&0\end{bmatrix}
\begin{bmatrix}x^\star\\\nu^\star\end{bmatrix}
=\begin{bmatrix}-q\\b\end{bmatrix}.
$$

在 $A$ 行满秩的前提下，块矩阵非奇异等价于 $P$ 在非零可行方向上正定：

$$
Ad=0,\ d\neq0\Longrightarrow d^TPd>0.
$$

也等价于 $P+A^TA\succ0$。所以不必要求 $P$ 在所有方向都正定，约束可以去掉原来的平坦方向。

例如 $P=\operatorname{diag}(1,0)$、约束 $x_2=1$，目标在全空间不严格凸，却在可行线上有唯一最优点 $(0,1)$。

## 可行起点牛顿法 {#feasible-newton}

在可行点 $x$ 上最小化二次近似，要求 $Ad=0$：

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}d\\w\end{bmatrix}
=\begin{bmatrix}-g\\0\end{bmatrix},
\quad H=\nabla^2f(x),\ g=\nabla f(x).
$$

得到 $d$ 后做回溯更新 $x^+=x+td$。由于 $Ad=0$，精确算术下任何步长都保持等式。

由第一行左乘 $d^T$、利用 $Ad=0$：

$$
g^Td=-d^THd.
$$

因此约束牛顿减量为 $\delta=\sqrt{d^THd}=\sqrt{-g^Td}$。一般不能用无约束的 $\sqrt{g^TH^{-1}g}$ 替换它。

在零空间坐标里做普通牛顿法，映回原空间恰好得到这个方向，因此两种方法在合适线搜索下共享相应的收敛分析。

## 不可行起点：目标暂时上升也可能有进展 {#infeasible-newton}

如果一开始 $Ax\neq b$，就不能用 $Ad=0$ 保持错误的等式值。把最优性条件合成残差：

$$
r(x,\nu)=
\begin{bmatrix}
\nabla f(x)+A^T\nu\\
Ax-b
\end{bmatrix}.
$$

线性化 $r(x+d,\nu+\Delta\nu)=0$：

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}d\\\Delta\nu\end{bmatrix}
=-
\begin{bmatrix}\nabla f(x)+A^T\nu\\Ax-b\end{bmatrix}.
$$

选择步长时检查残差范数充分减小，同时保证新点位于目标定义域。因为可行性本身需要修复，$f(x)$ 不必每步下降。

第二行给 $A(x+td)-b=(1-t)(Ax-b)$。完整步长 $t=1$ 会在精确算术下消除线性可行性残差；数值实现应使用容差，而不是比较浮点数是否完全等于零。

## 用 Schur 补求方向 {#implementation}

对一般右端：

$$
Hv+A^Tw=-g,\qquad Av=-h.
$$

若 $H\succ0$，消去 $v$：

$$
AH^{-1}A^Tw=h-AH^{-1}g,\qquad
Hv=-(g+A^Tw).
$$

由于 $A$ 行满秩，Schur 矩阵正定。$H^{-1}A^T$ 通过多右端求解获得。

当 $H$ 只在零空间上正定、全空间奇异时，完整 KKT 仍可能可逆，但上述显式消元不能直接使用；可选零空间法或适当的对称不定分解。

## 解析中心的三种解法 {#analytic-center}

对 $\min-\sum_i\log x_i,\ Ax=b,\ x>0$：

1. 原始可行牛顿法要求 $x^0>0,\ Ax^0=b$；
2. 对偶牛顿法要求 $A^T\nu^0>0$；
3. 不可行起点法只要求 $x^0>0$，再联合修复残差。

对偶是：

$$
\max_\nu -b^T\nu+\sum_i\log(A^T\nu)_i+n.
$$

最优时 $x_i=1/(A^T\nu)_i$。三种方法有不同起点要求，不能只比较迭代曲线就断言其中某种普遍更优。

在这个例子中，Hessian 为 $\operatorname{diag}(x_i^{-2})$，三种方法的核心都归结为求解 $ADA^Tw=h$，其中 $D$ 为正对角矩阵。每步成本可能相近，即使表面变量不同。

## 网络流的稀疏结构 {#network-flow}

有向图每条弧有一个流量 $x_j$。关联矩阵的一列在弧流出节点为 $+1$、流入节点为 $-1$。删除一个冗余节点方程，得到约化关联矩阵 $A$：

$$
\min_x\sum_j\phi_j(x_j),\qquad Ax=b.
$$

连通图的约化矩阵行满秩。若各边成本二阶导为正，Hessian 是正对角矩阵，Schur 矩阵 $AH^{-1}A^T$ 是约化加权图 Laplacian，其非零模式由连接关系决定。

节点总供需必须平衡；删除一个节点方程并不是允许丢失质量守恒。约化表示依赖该平衡关系。

## 矩阵变量的牛顿步 {#matrix-center}

考虑 $\min_{X\succ0}-\log\det X$，约束 $\operatorname{tr}(A_iX)=b_i$，其中 $A_i$ 为已知对称矩阵。

梯度是 $-X^{-1}$，Hessian 对方向 $\Delta X$ 的作用为 $X^{-1}\Delta X X^{-1}$，因此可行牛顿方程为：

$$
X^{-1}\Delta X X^{-1}+\sum_jw_jA_j=X^{-1},
\qquad \operatorname{tr}(A_i\Delta X)=0.
$$

两侧乘 $X$：

$$
\Delta X=X-\sum_jw_jXA_jX.
$$

代回约束，在当前点可行时：

$$
\sum_j\operatorname{tr}(A_iXA_jX)w_j=b_i.
$$

这是关于 $p$ 个乘子的系统。约束矩阵在对称矩阵空间中线性独立时，系数矩阵正定。先求 $w$ 再恢复 $\Delta X$，避免直接构造一个以全部矩阵元素为变量的巨大稠密系统。

典型主要成本为 $O(pn^3+p^2n^2+p^3)$，而直接解全部元素系统可能付出 $O((n^2+p)^3)$。具体结构还可能继续降低成本。
