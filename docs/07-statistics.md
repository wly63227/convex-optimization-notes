# 第 7 章：统计估计、检测与实验设计

> 来源：讲义 PDF 第 218～242 页；教材第 7 章的对应主题。教材还包括非参数分布估计、Chebyshev 与 Chernoff 界等未在这份讲义中展开的内容，本章不把它们冒充讲义已讲内容。

前面把 $A,b$ 当成已知数字。本章追问：如果数字来自带噪声的测量，为什么某一种误差函数是合理的？如果能选择测量方式，又怎样让估计更准确？

## 概率语言的最小预备 {#probability}

随机变量 $Y$ 表示观察前不确定的结果；$y$ 表示已经观察到的具体值。分布参数 $\theta$ 是待估计的量。密度 $p_\theta(y)$ 不等于“连续变量恰好等于 $y$ 的概率”，概率应通过区域上的积分得到。

期望 $\mathbb EY$ 是分布平均，协方差：

$$
\Sigma=\mathbb E[(Y-\mathbb EY)(Y-\mathbb EY)^T]
$$

衡量各方向的变化与关联。任意 $v$ 满足 $v^T\Sigma v=\operatorname{var}(v^TY)\geq0$，所以协方差半正定。

“独立同分布”（IID）同时要求观测互相独立、具有相同分布。只有独立时，联合密度才可以直接写成边缘密度的乘积。

## 最大似然：数据固定以后选择参数 {#mle}

观察到数据 $y$ 后，把 $p_\theta(y)$ 看成关于 $\theta$ 的函数，叫似然。最大似然估计选择：

$$
\widehat\theta\in\arg\max_\theta p_\theta(y).
$$

在正似然区域，对数严格递增，因此可以最大化对数似然 $\ell(\theta)=\log p_\theta(y)$。独立观测的乘积便变为和，既便于求导，也减轻数值下溢。

若对固定数据 $y$，$\ell(\theta)$ 对参数是凹函数，则这是凸优化。注意：要求的是**关于参数的凹性**，不是“数据密度关于观测值是对数凹”就自动足够；还要检查参数如何进入模型。

## 噪声假设决定拟合损失 {#noise-models}

设：

$$
y_i=a_i^T\theta+v_i,\quad i=1,\ldots,m,
$$

其中 $a_i\in\mathbb R^n$ 和 $y_i$ 已知，$\theta\in\mathbb R^n$ 未知，$v_i$ 独立同分布。联合对数似然是：

$$
\ell(\theta)=\sum_i\log p_v(y_i-a_i^T\theta).
$$

若 $v_i\sim N(0,\sigma^2)$，且 $\sigma>0$ 已知：

$$
\ell(\theta)
=-\frac m2\log(2\pi\sigma^2)
-\frac1{2\sigma^2}\sum_i(y_i-a_i^T\theta)^2.
$$

第一项与 $\theta$ 无关，因此最大似然就是最小二乘。若噪声独立、方差不同，则相应得到按方差倒数加权的最小二乘，而不是一律相同权重。

若噪声是尺度 $s>0$ 已知的 Laplace 分布：

$$
p_v(u)=\frac1{2s}e^{-|u|/s},
$$

则负对数似然去掉常数后为 $\sum_i|y_i-a_i^T\theta|/s$，对应一范数拟合。

若噪声均匀分布于 $[-s,s]$，则所有满足 $|y_i-a_i^T\theta|\leq s$ 的参数具有相同似然，最大似然变为一个可行性问题。

所以“哪种误差最好”取决于模型假设与目标，不能把平方误差当作没有前提的真理。

## 逻辑回归：分类问题为何能有凸目标 {#logistic}

每个观测包含特征 $u_i\in\mathbb R^n$ 与标签 $y_i\in\{0,1\}$。令参数 $a\in\mathbb R^n,b\in\mathbb R$，得分 $z_i=a^Tu_i+b$，假设：

$$
\mathbb P(y_i=1\mid u_i)=\sigma(z_i)
=\frac{e^{z_i}}{1+e^{z_i}}.
$$

独立样本的负对数似然为：

$$
F(a,b)=\sum_i\bigl[\log(1+e^{z_i})-y_iz_i\bigr].
$$

每项都是 log-sum-exp 减仿射函数，因此凸。进一步令 $\widetilde u_i=(u_i,1)$、$\theta=(a,b)$：

$$
\nabla F=\sum_i(\sigma(z_i)-y_i)\widetilde u_i,
$$

$$
\nabla^2F
=\sum_i\sigma(z_i)(1-\sigma(z_i))
\widetilde u_i\widetilde u_i^T\succeq0.
$$

这个推导也说明了为什么不能直接拿均方误差套在任意非线性分类模型上，就断言问题凸。

凸性仍不保证有限参数最优点。数据完全线性可分时，无正则逻辑回归可能靠无限放大参数不断降低损失。正则化、约束和数据条件是另一个层面的设计。

![逻辑回归概率与两种标签的损失](./assets/logistic.svg)

左图纵轴是概率，范围为 $[0,1]$；右图是损失，数值不受这个范围限制。它们不是同一类量。

## 高斯协方差：换成精度矩阵后凸性变清楚 {#covariance}

设 $y_1,\ldots,y_N\in\mathbb R^n$ 来自已知零均值高斯模型 $N(0,\Sigma)$，未知 $\Sigma\succ0$。定义：

$$
Y=\frac1N\sum_{k=1}^Ny_ky_k^T.
$$

因为均值已知为零，这里不减样本均值，且使用极大似然的 $1/N$，不是无偏样本方差中的 $1/(N-1)$。

由多元高斯密度推得：

$$
\ell(\Sigma)
=-\frac N2\left[n\log(2\pi)+\log\det\Sigma
+\operatorname{tr}(\Sigma^{-1}Y)\right].
$$

迹的出现来自 $y_k^T\Sigma^{-1}y_k=\operatorname{tr}(\Sigma^{-1}y_ky_k^T)$，再对样本求和。

令精度矩阵 $S=\Sigma^{-1}\succ0$，去掉正比例因子和常数，变成：

$$
\max_{S\succ0}\log\det S-\operatorname{tr}(SY).
$$

目标凹，因此是凸优化。若 $Y\succ0$，驻点为 $S^{-1}=Y$，即 $\widehat\Sigma=Y$。若 $Y$ 奇异，不能直接在正定域中套用这个结论：无约束的正定协方差 MLE 可能不存在。

讲义第 225～226 页把高斯归一化常数写成了 $-2\pi n$，本笔记由密度公式核正为 $-n\log(2\pi)$。这个常数不改变最优点，但完整似然公式应该正确。

## 稀疏精度矩阵与条件独立 {#sparse-precision}

对于非退化多元高斯分布，$S_{ij}=0$ 表示第 $i,j$ 个分量在给定其他分量后条件独立。它不表示这两个分量无条件独立。

可以通过凸模型鼓励稀疏：

$$
\min_{S\succ0}-\log\det S+\operatorname{tr}(SY)
+\lambda\sum_{i\neq j}|S_{ij}|,\qquad\lambda\geq0.
$$

三项分别控制高斯拟合、数据一致性和非对角稀疏性。讲义的四维小样本例子展示了正则估计与直接逆经验协方差的差别；那组具体随机样本未提供，因此这里不把它的估计误差数字当作本项目重新实验的结果。

## 二元假设检验可以是线性规划 {#testing}

观察离散状态 $X\in\{1,\ldots,n\}$，两个假设分别对应已知概率向量 $p,q$。

令 $t_k\in[0,1]$ 表示观察到状态 $k$ 后选择假设 1 的概率。选择假设 2 的概率就是 $1-t_k$。约定假设 2 是“阳性”，则：

$$
P_{\mathrm{fp}}=\sum_kp_k(1-t_k),\qquad
P_{\mathrm{fn}}=\sum_kq_kt_k.
$$

这两个错误概率都是变量 $t$ 的仿射函数。加权目标：

$$
P_{\mathrm{fp}}+\lambda P_{\mathrm{fn}}
=\sum_k[p_k+(\lambda q_k-p_k)t_k].
$$

各个 $t_k$ 可以单独选择：

- $p_k>\lambda q_k$ 时取 $t_k=1$；
- $p_k<\lambda q_k$ 时取 $t_k=0$；
- 相等时任意 $t_k\in[0,1]$ 都最优。

这就是似然比检验。若 $q_k=0$，直接使用上面的比较，不需要除以零。

若追求两种错误中的较大者最小，写成：

$$
\min_{t,s}s,\qquad
P_{\mathrm{fp}}\leq s,\quad P_{\mathrm{fn}}\leq s,\quad0\leq t\leq1.
$$

这是 LP，而且最优检测器可能需要随机化。

**讲义数据的自编计算。** 对：

$$
p=(0.70,0.20,0.05,0.05),\quad
q=(0.10,0.10,0.70,0.10),
$$

取 $t=(1,2/3,0,0)$，两种错误都为 $1/6$。用权重 $\lambda=2$，任意检测器的 $P_{\mathrm{fp}}+2P_{\mathrm{fn}}$ 至少为 $1/2$，因此两种错误不可能同时小于 $1/6$。这同时给出了 minimax 解和最优性证书。

## 实验设计：先选择怎样测量 {#design}

现在未知参数为 $\theta\in\mathbb R^n$，可选择的测量向量来自 $v_1,\ldots,v_p$。每次测量满足 $y=a^T\theta+w$，噪声独立且为 $N(0,1)$。

若信息矩阵可逆，最小二乘估计误差协方差为：

$$
E=\left(\sum_{i=1}^m a_ia_i^T\right)^{-1}.
$$

将第 $k$ 种向量测量 $m_k$ 次，信息矩阵变成 $\sum_km_kv_kv_k^T$。整数次数模型通常难求；使用比例 $w_k=m_k/m$：

$$
w_k\geq0,\quad\sum_kw_k=1,\qquad
M(w)=\sum_kw_kv_kv_k^T,
$$

得到连续松弛，$E=(mM(w))^{-1}$。

不同标量化衡量不同误差：

- D-optimal：最小化 $-\log\det M(w)$，控制置信椭球体积；
- A-optimal：最小化 $\operatorname{tr}(M(w)^{-1})$，控制总方差；
- E-optimal：最大化 $\lambda_{\min}(M(w))$，控制最差方向。

所有逆矩阵表达式都要求 $M(w)\succ0$。候选向量必须张成需要估计的空间，否则不能在所有方向上获得有限精度。

连续比例乘回 $m$ 后一般不是整数；取整必须保持总测量次数，并检查秩，不能自动声称取整后仍最优。

## D-optimal 的对偶与椭球解释 {#design-dual}

考虑 $\min_w-\log\det M(w)$，$w$ 位于单纯形。引入 $X=M(w)$ 与矩阵乘子 $Z$、单纯形等式乘子 $\nu$。对 $X\succ0$ 最小化：

$$
-X^{-1}+Z=0\quad\Longrightarrow\quad X=Z^{-1}.
$$

对 $w\geq0$ 取下确界，要求 $v_k^TZv_k\leq\nu$，得到对偶：

$$
\max_{Z\succ0,\nu}\log\det Z+n-\nu,
\qquad v_k^TZv_k\leq\nu.
$$

在候选向量张成全空间等条件下，$\nu>0$。令 $W=Z/\nu$，关于 $\nu$ 的项为 $n\log\nu-\nu$，它在 $\nu=n$ 时最大，于是：

$$
\max_{W\succ0}\log\det W+n\log n,\qquad
v_k^TWv_k\leq1.
$$

这相当于寻找包含所有候选向量、中心在原点的最小体积椭球。互补松弛：

$$
w_k(1-v_k^TWv_k)=0
$$

说明被分配正测量比例的向量必须落在该椭球边界。

**手算例题。** $v_1=(1,0)^T,v_2=(0,1)^T$ 时，$M=\operatorname{diag}(w,1-w)$。最大化行列式 $w(1-w)$ 得到 $w=1/2$。信息矩阵为 $I/2$，对偶 $W=I$，两边最优值都为 $2\log2$。

本章没有要求读者先记住统计公式：每个模型应回到“观测分布是什么、哪一个量未知、为什么取这个损失或误差标准”来理解。
