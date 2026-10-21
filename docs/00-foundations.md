# 预备章：数学语言与计算基础

## 集合、属于与“所有满足条件的点” {#base-01}

$x\in C$ 表示“$x$ 属于集合 $C$”。

$$
C=\{x\in\mathbb R\mid x\geq 0\}
$$

读作“所有非负实数组成的集合”。竖线 $\mid$ 表示“满足”。

$\mathbb R$ 是实数集合；$\mathbb R^n$ 是由 $n$ 个实数组成的向量空间。$\forall$ 表示“对任意”，$\exists$ 表示“存在”。

## 标量、向量、矩阵 {#base-02}

**标量**是一个数，例如预算 $b=100$。

**向量**把多个数放在一起：

$$
x=\begin{bmatrix}x_1\\x_2\end{bmatrix}\in\mathbb R^2.
$$

可以把它理解成“购买第一种、第二种原料的数量”。

**矩阵**把多个线性关系放在一起：

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix},\qquad
Ax=
\begin{bmatrix}
x_1+2x_2\\
3x_1+4x_2
\end{bmatrix}.
$$

如果 $A\in\mathbb R^{m\times n}$、$x\in\mathbb R^n$，那么 $Ax\in\mathbb R^m$。不会做题时，先检查维度，常能发现错误。

## 转置与内积 {#base-03}

$x^T$ 表示把列向量转成行向量。

$$
a^Tx=\sum_{i=1}^n a_ix_i.
$$

例如：

$$
a=\begin{bmatrix}2\\3\end{bmatrix},
\quad
x=\begin{bmatrix}4\\5\end{bmatrix}
\quad\Longrightarrow\quad
a^Tx=2\cdot4+3\cdot5=23.
$$

内积可以表示总成本，也可以描述方向。两个向量的内积为零时，它们在欧氏意义下相互垂直。

## 范数：衡量一个向量有多大 {#base-04}

最常见的三个范数：

$$
\|x\|_1=\sum_i|x_i|,\qquad
\|x\|_2=\sqrt{\sum_i x_i^2},\qquad
\|x\|_\infty=\max_i|x_i|.
$$

对 $x=(3,-4)^T$：

$$
\|x\|_1=7,\qquad \|x\|_2=5,\qquad \|x\|_\infty=4.
$$

可以分别理解为“绝对值总量”“直线长度”“最大单项幅度”。以后看到 $\|Ax-b\|$，就是在用某种规则衡量误差向量的大小。

注意：

$$
\|x\|_2^2=x^Tx
$$

是欧氏范数的平方，它本身不再是范数，但仍是凸函数。

## 导数、偏导数、梯度 {#base-05}

一元函数的导数 $f'(x)$ 描述局部变化率。例如：

$$
f(x)=(x-2)^2,\qquad f'(x)=2(x-2).
$$

多元函数对每个变量分别求导，得到偏导数。把偏导数排成列向量，就是**梯度**：

$$
\nabla f(x)=
\begin{bmatrix}
\frac{\partial f}{\partial x_1}\\
\vdots\\
\frac{\partial f}{\partial x_n}
\end{bmatrix}.
$$

例如：

$$
f(x_1,x_2)=x_1^2+3x_2^2,
\qquad
\nabla f(x)=
\begin{bmatrix}2x_1\\6x_2\end{bmatrix}.
$$

局部一阶近似是：

$$
f(x+d)\approx f(x)+\nabla f(x)^Td.
$$

如果取 $d=-\eta\nabla f(x)$，其中 $\eta>0$，近似变化量为：

$$
-\eta\|\nabla f(x)\|_2^2\leq 0.
$$

这解释了为什么负梯度是一个自然的下降方向。实际下降还取决于步子是否足够小、是否仍在定义域中。

## Hessian：描述不同方向的弯曲程度 {#base-06}

Hessian，也叫海森矩阵，是二阶偏导数组成的矩阵：

$$
\nabla^2f(x)=
\left[\frac{\partial^2 f}{\partial x_i\partial x_j}\right]_{i,j=1}^n.
$$

对于 $f(x_1,x_2)=x_1^2+3x_2^2$：

$$
\nabla^2f(x)=
\begin{bmatrix}2&0\\0&6\end{bmatrix}.
$$

二阶近似是：

$$
f(x+d)\approx
f(x)+\nabla f(x)^Td+
\frac12d^T\nabla^2f(x)d.
$$

最后一项告诉我们函数沿方向 $d$ 的弯曲情况。

## 正定与半正定 {#base-07}

对称矩阵 $P=P^T$：

$$
P\succeq0
\quad\Longleftrightarrow\quad
z^TPz\geq0,\ \forall z,
$$

称为**半正定**。

$$
P\succ0
\quad\Longleftrightarrow\quad
z^TPz>0,\ \forall z\neq0,
$$

称为**正定**。

直觉：半正定表示沿任何方向的二次型都不会为负；正定表示非零方向上的二次型都严格为正。

对实对称矩阵：

- 所有特征值非负，等价于半正定。
- 所有特征值为正，等价于正定。

这里的 $\succeq0$ **不是“每个元素都非负”**。例如：

$$
P=\begin{bmatrix}1&2\\2&1\end{bmatrix}
$$

所有元素为正，但取 $z=(1,-1)^T$，有 $z^TPz=-2$，因此它不是半正定矩阵。

对于对称的 $2\times2$ 矩阵：

$$
P=\begin{bmatrix}a&b\\b&c\end{bmatrix},
$$

半正定当且仅当：

$$
a\geq0,\quad c\geq0,\quad ac-b^2\geq0.
$$

正定当且仅当 $a>0$ 且 $ac-b^2>0$。

## 二次函数的求导公式 {#base-08}

设 $P=P^T$，则：

$$
f(x)=\frac12x^TPx+q^Tx+r
$$

满足：

$$
\nabla f(x)=Px+q,\qquad \nabla^2f(x)=P.
$$

前面的 $\frac12$ 是为了让求导后不再多出一个 $2$。

如果 $P$ 不对称，梯度应为 $\frac12(P+P^T)x+q$；讨论二次型时通常直接使用对称矩阵。

**本节自检：** 能否算出 $\nabla(x_1^2+x_1x_2+2x_2^2)$？答案应为 $(2x_1+x_2,\ x_1+4x_2)^T$。
