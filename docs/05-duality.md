# 第 5 章：对偶、KKT 与最优性证书

> 来源：讲义 PDF 第 154～192 页；教材第 5 章。前半章建立最优性证书，后半章解释如何利用不同表示构造有用的对偶与不可行证书。

这一节不需要先理解所有抽象理论。先抓住一个问题：

> 如果已经找到一个可行方案，怎样证明不存在更好的方案？

对最小化问题，可行方案给出最优值的**上界**；如果再找到一个相同数值的**下界**，就能确认最优。

## 拉格朗日函数 {#base-01}

考虑：

$$
\min_x f_0(x),\qquad
f_i(x)\leq0,\quad h_j(x)=0.
$$

定义：

$$
L(x,\lambda,\nu)
=f_0(x)+\sum_i\lambda_i f_i(x)+\sum_j\nu_j h_j(x).
$$

其中：

- $\lambda_i$ 对应不等式约束；
- $\nu_j$ 对应等式约束；
- 构造对偶下界时要求 $\lambda_i\geq0$；
- $\nu_j$ 不限制正负。

乘子是新的辅助变量，不能和原来的决策变量 $x$ 混淆。

这里也不要把 $L$ 简单理解成“一定会惩罚所有违反约束的点”：我们接下来利用的是它在可行点上的下界性质。

## 为什么要求不等式乘子非负 {#base-02}

对任意可行点 $x$：

$$
f_i(x)\leq0,\qquad h_j(x)=0.
$$

如果 $\lambda_i\geq0$，就有：

$$
L(x,\lambda,\nu)\leq f_0(x).
$$

等式约束的贡献恒为零，所以 $\nu$ 无须非负。

## 对偶函数 {#base-03}

把乘子暂时固定，对 $x$ 求下确界：

$$
g(\lambda,\nu)=\inf_{x\in D}L(x,\lambda,\nu).
$$

这里 $D$ 是原函数的共同定义域。**求这个下确界时，不再要求 $x$ 满足那些已经放入拉格朗日函数的约束。**

如果又把所有原约束加回去，就不再是这里定义的标准对偶函数。

对任意原问题可行点 $x$ 和 $\lambda\geq0$：

$$
g(\lambda,\nu)\leq L(x,\lambda,\nu)\leq f_0(x).
$$

于是：

$$
g(\lambda,\nu)\leq p^\star.
$$

我们获得了原问题最优值的一个下界。某些乘子下 $g=-\infty$，这种下界没有实际帮助。

## 对偶问题与弱对偶 {#base-04}

既然每组允许的乘子都给出下界，就寻找最大的那个：

$$
\begin{aligned}
\max_{\lambda,\nu}\quad &g(\lambda,\nu)\\
\text{s.t.}\quad &\lambda\geq0.
\end{aligned}
$$

它叫**拉格朗日对偶问题**，最优值记为 $d^\star$。

$$
d^\star\leq p^\star
$$

叫作**弱对偶**。原问题即使非凸，这个下界关系也成立。

对偶函数总是关于乘子的凹函数，因为它是关于乘子的仿射函数族的逐点下确界。因此对偶问题是一个凹函数最大化问题；这不意味着原问题的最优值一定能通过对偶精确恢复。

## 强对偶与 Slater 条件 {#base-05}

如果：

$$
d^\star=p^\star,
$$

就叫**强对偶**；有限情形下 $p^\star-d^\star$ 称为最优对偶间隙。

不能把“原问题凸”直接替换成“必定强对偶”。

一个常用的充分条件是 **Slater 条件**。对于凸问题：

$$
\min_x f_0(x),\qquad f_i(x)\leq0,\quad Ax=b,
$$

若存在一个点 $\bar x$，满足：

$$
\bar x\in\operatorname{relint}D,\qquad
f_i(\bar x)<0,\quad\forall i,\qquad
A\bar x=b,
$$

则强对偶成立。

这里 $\operatorname{relint}$ 是**相对内部**，即在集合所在的最小仿射空间中看内部。例如一条线段在平面里没有通常意义的内部，但去掉两端后的部分是它的相对内部。

对于定义域是整个 $\mathbb R^n$ 的入门例子，可以先理解为：“找到一个满足等式，而且所有不等式都有余量的点。”

补充：

- 等式约束仍要求精确成立，不存在“严格小于的等式”。
- 对仿射不等式可以使用更弱的版本，不必严格满足。
- Slater 是充分条件，没满足它不等于强对偶一定失败。
- 在最优值有限时，Slater 还保证存在达到对偶最优值的乘子；它不自动保证原问题取得最优解。

## 完整推导一个一维对偶问题 {#base-06}

原问题：

$$
\min_x x^2,\qquad x\geq1.
$$

先写成 $1-x\leq0$，因此：

$$
L(x,\lambda)=x^2+\lambda(1-x),\qquad\lambda\geq0.
$$

固定 $\lambda$，对所有 $x\in\mathbb R$ 最小化：

$$
\frac{\partial L}{\partial x}=2x-\lambda=0
\quad\Longrightarrow\quad x=\frac{\lambda}{2}.
$$

代回：

$$
g(\lambda)
=\lambda-\frac{\lambda^2}{4}.
$$

所以对偶问题是：

$$
\max_{\lambda\geq0}\left(\lambda-\frac{\lambda^2}{4}\right).
$$

令导数为零：

$$
1-\frac{\lambda}{2}=0
\quad\Longrightarrow\quad
\lambda^\star=2,\qquad d^\star=1.
$$

原问题显然有 $x^\star=1,p^\star=1$。因此：

$$
d^\star=p^\star=1.
$$

同时 $x=2$ 严格满足不等式，符合 Slater 条件。

## 对偶间隙可以用作“答案有多准”的证据 {#base-07}

如果 $x$ 原可行，$(\lambda,\nu)$ 对偶可行，且两边目标值有限：

$$
g(\lambda,\nu)\leq p^\star\leq f_0(x).
$$

因此：

$$
0\leq f_0(x)-p^\star
\leq f_0(x)-g(\lambda,\nu).
$$

右边是一个可计算的误差上界。它不要求我们事先知道真正的 $p^\star$。

## 乘子的敏感性解释：选读 {#base-08}

把不等式放宽成：

$$
f_i(x)\leq u_i.
$$

记最优值为 $p(u)$。在强对偶、最优乘子存在等条件下，原点处的最优乘子提供：

$$
p(u)\geq p(0)-(\lambda^\star)^Tu.
$$

如果 $p(u)$ 在 $0$ 处可微，则：

$$
\frac{\partial p}{\partial u_i}(0)=-\lambda_i^\star.
$$

它衡量约束放宽一点时，最优目标能改善多少。

对上面的一维问题，将 $1-x\leq0$ 改为 $1-x\leq u$，在 $u=0$ 附近：

$$
p(u)=(1-u)^2,\qquad p'(0)=-2=-\lambda^\star.
$$

“乘子是影子价格”的说法需要这些条件，也取决于约束的写法与单位，不是一个脱离模型的固定价格。

若等式也扰动为 $h(x)=v$，完整的对偶下界为 $p(u,v)\geq p(0,0)-(\lambda^\star)^Tu-(\nu^\star)^Tv$；可微时对 $v_j$ 的导数为 $-\nu_j^\star$。因为等式乘子可以正也可以负，改变等式右端对最优值的影响也没有统一方向。

## 四组条件 {#base-09}

考虑可微问题：

$$
\min_x f_0(x),\qquad
f_i(x)\leq0,\quad Ax=b.
$$

候选点 $x^\star$ 和乘子 $(\lambda^\star,\nu^\star)$ 的 KKT 条件是：

**第一组：原始可行性**

$$
f_i(x^\star)\leq0,\qquad Ax^\star=b.
$$

**第二组：对偶可行性**

$$
\lambda_i^\star\geq0.
$$

**第三组：互补松弛**

$$
\lambda_i^\star f_i(x^\star)=0,\qquad\forall i.
$$

**第四组：驻点条件**

$$
\nabla f_0(x^\star)
+\sum_i\lambda_i^\star\nabla f_i(x^\star)
+A^T\nu^\star=0.
$$

这里假设点位于可微函数的共同开定义域中。不可微目标或额外集合约束，需要使用相应的次梯度、法锥等扩展形式。

## 互补松弛到底是什么意思 {#base-10}

对某个约束 $f_i(x)\leq0$：

- 若 $f_i(x^\star)<0$，约束没有卡在边界，必须有 $\lambda_i^\star=0$。
- 若 $\lambda_i^\star>0$，则必须有 $f_i(x^\star)=0$。
- 若 $f_i(x^\star)=0$，乘子仍可能为零。

最后一点容易漏掉。**约束活跃，不等于乘子一定严格为正。**

例如 $\min_{x\geq0}x^2$ 的最优点是 $0$，非负约束活跃，但对应乘子为 $0$。

## KKT 什么时候能证明最优 {#base-11}

| 情形 | 可以得出的结论 |
|---|---|
| 可微凸问题，找到满足全部 KKT 的点与乘子 | 足以证明它们原始、对偶最优 |
| 可微凸问题满足 Slater，且考察一个原始最优点 | 存在使它满足 KKT 的乘子 |
| 一般非凸问题 | 在适当约束资格条件下，KKT 通常是局部最优的必要条件，通常不充分 |

因此：

> 对可微凸问题，KKT 是充分条件；加入 Slater 等适当条件后，才可将它完整地用于“最优当且仅当存在 KKT 乘子”的判断。

不应只写“所有优化问题最优时都一定满足 KKT”，也不能只检查驻点条件就宣布最优。

## 为什么凸问题里 KKT 足够 {#base-12}

假设全部 KKT 成立：

1. $\lambda^\star\geq0$，使 $L(x,\lambda^\star,\nu^\star)$ 关于 $x$ 凸。
2. 驻点条件说明 $x^\star$ 全局最小化这个拉格朗日函数。
3. 原始可行性与互补松弛说明：

$$
L(x^\star,\lambda^\star,\nu^\star)=f_0(x^\star).
$$

于是：

$$
g(\lambda^\star,\nu^\star)=f_0(x^\star).
$$

可行上界与对偶下界相等，最优性得到证明。

## 例题一：边界最优点 {#base-13}

$$
\min_x x^2,\qquad 1-x\leq0.
$$

写出：

$$
L=x^2+\lambda(1-x).
$$

KKT 条件：

$$
x\geq1,\qquad
\lambda\geq0,\qquad
\lambda(1-x)=0,\qquad
2x-\lambda=0.
$$

分类讨论：

- 若 $\lambda=0$，驻点条件给出 $x=0$，违反 $x\geq1$，排除。
- 因而 $\lambda>0$，互补松弛给出 $x=1$。
- 驻点条件再给出 $\lambda=2$。

检查全部条件成立，且问题凸：

$$
x^\star=1,\qquad\lambda^\star=2,\qquad p^\star=1.
$$

这里 $\nabla f_0(1)=2\neq0$，但目标梯度和约束梯度的加权和为零。

## 例题二：看见约束活跃与不活跃的切换 {#base-14}

$$
\min_{x\geq0}(x-a)^2,
$$

其中 $a$ 是已知参数，约束函数为 $-x$。

$$
L=(x-a)^2-\lambda x.
$$

KKT：

$$
x\geq0,\quad
\lambda\geq0,\quad
\lambda x=0,\quad
2(x-a)-\lambda=0.
$$

若 $a>0$，取 $x=a$，约束有余量，$\lambda=0$。

若 $a<0$，无约束最优点在可行域外，所以取 $x=0$，驻点条件给出 $\lambda=-2a>0$。

若 $a=0$，$x=0,\lambda=0$。

合起来：

$$
x^\star=\max\{a,0\},\qquad
\lambda^\star=\max\{-2a,0\}.
$$

这也就是把 $a$ 投影到非负半轴。

## 例题三：只有等式约束 {#base-15}

$$
\begin{aligned}
\min_{x_1,x_2}\quad &\frac12(x_1^2+x_2^2)\\
\text{s.t.}\quad &x_1+x_2=1.
\end{aligned}
$$

拉格朗日函数：

$$
L=\frac12(x_1^2+x_2^2)+\nu(x_1+x_2-1).
$$

驻点与可行性：

$$
x_1+\nu=0,\qquad
x_2+\nu=0,\qquad
x_1+x_2=1.
$$

因此：

$$
x_1^\star=x_2^\star=\frac12,\qquad
\nu^\star=-\frac12,\qquad
p^\star=\frac14.
$$

等式乘子为负完全正常。

更一般地，等式约束凸二次问题的 KKT 可以写成线性方程：

$$
\begin{bmatrix}
P&A^T\\
A&0
\end{bmatrix}
\begin{bmatrix}
x\\\nu
\end{bmatrix}
=
\begin{bmatrix}
-q\\b
\end{bmatrix}.
$$

是否能够唯一解出，还需要看这个块矩阵是否非奇异，例如 $P\succ0$ 且 $A$ 行满秩是常用的充分条件。

## 三类可以直接推导的对偶 {#standard-duals}

先考虑最小欧氏范数解：

$$
\min_x x^Tx,\qquad Ax=b.
$$

写 $L=x^Tx+\nu^T(Ax-b)$，对 $x$ 求最小得到 $x=-A^T\nu/2$，代回：

$$
g(\nu)=-\frac14\nu^TAA^T\nu-b^T\nu.
$$

即使 $A$ 不满秩，这个对偶函数的表达式仍有意义；此处没有求 $(AA^T)^{-1}$。

对于标准 LP：

$$
\min c^Tx,\qquad Ax=b,\quad x\geq0,
$$

将非负约束写成 $-x\leq0$：

$$
L=(c+A^T\nu-\lambda)^Tx-b^T\nu.
$$

对全部 $x\in\mathbb R^n$ 求下确界时，若线性系数不为零，就能沿某个方向趋于 $-\infty$。因此有限下界必须满足 $c+A^T\nu-\lambda=0$。消去 $\lambda\geq0$：

$$
\max_\nu -b^T\nu,\qquad c+A^T\nu\geq0.
$$

如果最初选择 $\nu^T(b-Ax)$，符号会改变，但对偶值与实际内容一致。不要从其他写法直接抄乘子符号。

若原 LP 采用 $\min c^Tx,\ Ax\leq b$、变量不另作符号限制，则同样消去自由的 $x$ 得到 $\max_{\lambda\geq0}-b^T\lambda$，约束 $A^T\lambda+c=0$。它和标准等式形式的对偶是不同表示，不应混抄约束。

对于严格凸二次目标 $\min x^TPx,\ Ax\leq b,\ P\succ0$：

$$
g(\lambda)=-\frac14\lambda^TAP^{-1}A^T\lambda-b^T\lambda,
\qquad\lambda\geq0.
$$

它与使用 $\frac12x^TPx$ 时的系数不同。推导中令 $2Px+A^T\lambda=0$，可避免记错 $1/4$。

## 对偶范数、共轭与残差重写 {#norm-duals}

范数的对偶范数定义为：

$$
\|y\|_*=\sup_{\|x\|\leq1}y^Tx.
$$

它给出 $y^Tx\leq\|x\|\|y\|_*$。欧氏范数的对偶还是欧氏范数；一范数与无穷范数互为对偶。

对范数函数，其凸共轭为对偶单位球的指示函数：

$$
(\|\cdot\|)^*(y)=
\begin{cases}0,&\|y\|_*\leq1,\\+\infty,&\text{否则}.\end{cases}
$$

若 $\|y\|_*\leq1$，由上面的不等式，$y^Tx-\|x\|\leq0$，且 $x=0$ 取等；若超过 $1$，沿一个使内积超过范数的方向不断放大，得到 $+\infty$。

对 $\min\|x\|,\ Ax=b$，使用拉格朗日项 $\nu^T(b-Ax)$，得到：

$$
\max_\nu b^T\nu,\qquad\|A^T\nu\|_*\leq1.
$$

对 $\min\|Ax-b\|$，先引入残差 $r=Ax-b$，使用 $\nu^T(r-Ax+b)$，分别对 $r,x$ 取下确界：

$$
\max_\nu b^T\nu,\qquad A^T\nu=0,\quad\|\nu\|_*\leq1.
$$

这个例子说明：同一个原始问题的等价表示可以产生不同外观、不同用途的对偶。

更一般地：

$$
\min f(x),\quad Ax\leq b,\ Cx=d
$$

的对偶函数可由共轭写成：

$$
g(\lambda,\nu)
=-f^*(-A^T\lambda-C^T\nu)-b^T\lambda-d^T\nu.
$$

负熵 $f(x)=\sum_i x_i\log x_i$（采用合适的非负域延拓）的共轭是 $\sum_i e^{y_i-1}$，因此熵模型也可以系统地构造对偶。

## 非凸问题也能得到凸下界：二分组 {#partition}

令 $x_i\in\{-1,1\}$ 表示第 $i$ 个对象分到哪一组。对称矩阵 $W$ 给出配对成本：

$$
\min_x x^TWx,\qquad x_i^2=1.
$$

原问题离散且通常非凸。对等式引入自由乘子 $\nu_i$：

$$
L=x^T(W+\operatorname{diag}\nu)x-\mathbf1^T\nu.
$$

若矩阵存在负特征方向，下确界为 $-\infty$；若半正定，二次项在 $x=0$ 取最小值 $0$。于是：

$$
\max_\nu-\mathbf1^T\nu,\qquad
W+\operatorname{diag}\nu\succeq0.
$$

这是 SDP，给原问题下界。不能因为对偶是凸的，就断言这个离散问题已经被精确解决。

## 对偶的几何解释 {#dual-geometry}

只有一个不等式时，把每个 $x$ 映成平面上的点 $(u,t)=(f_1(x),f_0(x))$。原问题是在 $u\leq0$ 部分找最低的 $t$。

固定 $\lambda\geq0$，直线 $t+\lambda u=\gamma$ 从下方托住所有可达到的点，能取到的最大截距 $\gamma$ 就是 $g(\lambda)$。

强对偶意味着存在一个非竖直支撑方向，使截距刚好达到原最优值。Slater 的严格可行点帮助排除只剩竖直支撑的退化情形。这是前面分离超平面与对偶之间的联系。

## 不可行证书与 Farkas 引理 {#alternatives}

“找不到可行解”可能只是算法没找到；不可行证书则是一段可以单独核查的数学证明。

例如系统：

$$
Ax=b,\qquad x\geq0
$$

不可行，当且仅当存在 $y$：

$$
A^Ty\geq0,\qquad b^Ty<0.
$$

两个系统不可能同时可行：否则 $b^Ty=x^TA^Ty\geq0$，与负值矛盾。Farkas 引理还保证两者恰有一个可行。把 $y$ 正比例放大，可以把负值规范为 $b^Ty=-1$。

讲义也使用以下等价的强择一定理：

$$
Ax\leq0,\quad c^Tx<0
$$

与

$$
A^Ty+c=0,\quad y\geq0
$$

恰有一组可解。对一般非线性可行性问题，如果存在 $\lambda\geq0$ 使 $\inf_x[\sum_i\lambda_if_i(x)+\sum_j\nu_jh_j(x)]>0$，同样能证明原约束不可行；反过来能否总找到这样的证书，需要额外条件。

## 无套利例子：线性证书的一个解释 {#arbitrage}

这里仅讨论讲义的有限状态数学模型。设 $p\in\mathbb R^n$ 是资产价格，$V\in\mathbb R^{m\times n}$ 是不同状态下的到期支付矩阵，$x$ 为允许正负的持仓。

讲义所定义的套利是：

$$
p^Tx<0,\qquad Vx\geq0.
$$

按 Farkas 引理，不存在这种组合，当且仅当有 $y\geq0$ 满足 $V^Ty=p$。如果第一种资产的价格与所有状态的支付都为 $1$，就推出 $\mathbf1^Ty=1$，从而 $y$ 可以解释为风险中性概率。

这一结论针对“初始成本严格为负、到期支付非负”的特定套利定义；不能不经说明就换成更强的其他套利定义。

讲义第 192 页给出的四状态三资产例子可核算为：

$$
V=\begin{bmatrix}
1&0.5&0\\1&0.8&0\\1&1&1\\1&1.3&4
\end{bmatrix},
\quad
p=(1,0.9,0.3)^T,
\quad
x=(6.2,-7.7,1.5)^T.
$$

逐项计算 $Vx=(2.35,0.04,0,2.19)^T\geq0$，$p^Tx=-0.28<0$，验证套利证书。讲义上的成本数字为 $-0.2$；本笔记按显示的输入值核算并记录这一差异。

换成 $\widetilde p=(1,0.8,0.7)^T$，可取精确概率 $y=(11/30,7/30,3/10,1/10)^T$，满足 $V^Ty=\widetilde p$、总和为 $1$。这是对讲义舍入概率的自编精确化，不是照录原表。
