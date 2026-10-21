# 可复现的程序实验

本节三个代码块可以分别保存成 Python 文件运行，**只使用 Python 标准库，不需要安装额外包**。代码用于理解数学过程，不是通用优化求解器。

如果暂时不会 Python，可以先手算第一个实验的前四步，再把代码当作伪代码阅读。

## 实验一：观察梯度下降与步长 {#base-01}

~~~python
def f(x):
    return (x - 2.0) ** 2


def grad(x):
    return 2.0 * (x - 2.0)


def run(eta, steps=8):
    x = 0.0
    print(f"\nstep size = {eta}")
    for k in range(steps + 1):
        print(f"k={k:2d}, x={x:12.6f}, f={f(x):14.8f}")
        if k < steps:
            x -= eta * grad(x)


for eta in (0.25, 0.5, 1.0, 1.1):
    run(eta)
~~~

预期：

- $0.25$：$x$ 依次为 $0,1,1.5,1.75,\ldots$。
- $0.5$：一步到 $x=2$。
- $1.0$：在 $0$ 和 $4$ 之间振荡。
- $1.1$：误差交替变号且幅度增大。

思考：为什么 $0.75$ 也会在最优点两侧跳动，却仍然收敛？答案是误差因子 $1-2\eta=-0.5$ 的绝对值小于 $1$。

## 实验二：不用矩阵库求解最小二乘与岭回归 {#base-02}

本例使用[第 6 章](./06-approximation.md#base-04)的数据。展开后的梯度是：

$$
\nabla f_\lambda(x)=
\begin{bmatrix}
(2+\lambda)x_1+x_2-3\\
x_1+(2+\lambda)x_2-4
\end{bmatrix}.
$$

当 $\lambda=0$ 是普通最小二乘；当 $\lambda=1$ 是前面定义的岭回归。

~~~python
from math import hypot


def objective(x1, x2, lam):
    residuals = (x1 - 1.0, x2 - 2.0, x1 + x2 - 2.0)
    fit = 0.5 * sum(r * r for r in residuals)
    penalty = 0.5 * lam * (x1 * x1 + x2 * x2)
    return fit + penalty


def solve(lam, eta=0.25, tol=1e-10, max_iter=1000):
    x1, x2 = 0.0, 0.0
    for k in range(max_iter):
        g1 = (2.0 + lam) * x1 + x2 - 3.0
        g2 = x1 + (2.0 + lam) * x2 - 4.0
        residual = hypot(g1, g2)
        if residual <= tol:
            return x1, x2, k, residual
        # 两个梯度都在同一个旧点计算，然后同步更新。
        x1, x2 = x1 - eta * g1, x2 - eta * g2
    raise RuntimeError("Maximum number of iterations reached")


for lam in (0.0, 1.0):
    x1, x2, steps, residual = solve(lam)
    print(f"lambda = {lam}")
    print(f"x = ({x1:.9f}, {x2:.9f}), steps = {steps}")
    print(f"objective = {objective(x1, x2, lam):.9f}")
    print(f"gradient norm = {residual:.3e}\n")
~~~

预期结果，允许末尾有浮点误差：

| $\lambda$ | $x_1$ | $x_2$ | 包含正则项的目标值 |
|---:|---:|---:|---:|
| 0 | $2/3$ | $5/3$ | $1/6$ |
| 1 | $5/8$ | $9/8$ | $21/16$ |

两种模型的目标函数不同，不能直接拿它们各自的总目标值比较“哪个模型更好”。

本例 $\lambda=0$ 时 Hessian 特征值为 $1,3$，$\lambda=1$ 时为 $2,4$。步长 $0.25$ 分别不大于 $1/3$ 与 $1/4$，符合前面的保守选择。

## 实验三：投影与约束最优性 {#base-03}

~~~python
x = 4.0
eta = 0.1

for _ in range(30):
    gradient_step = x - eta * 2.0 * x
    x = max(gradient_step, 1.0)  # 投影到 [1, +infinity)

multiplier = 2.0 * x
primal_violation = max(1.0 - x, 0.0)
stationarity = abs(2.0 * x - multiplier)
complementarity = abs(multiplier * (1.0 - x))

print("x =", x)
print("ordinary gradient =", 2.0 * x)
print("multiplier =", multiplier)
print("primal violation =", primal_violation)
print("stationarity residual =", stationarity)
print("complementarity residual =", complementarity)
~~~

本例最后应得到：

$$
x=1,\qquad \lambda=2,\qquad \nabla f(x)=2.
$$

原始违约、驻点残差、互补松弛残差都为零，乘子也非负。普通梯度虽然不是零，但 KKT 条件成立。

代码中的乘子是利用这个特定例子的驻点方程恢复的；一般问题不能机械套用 $\lambda=2x$。

## 项目级复现与输出 {#project-run}

以上三个入门代码块只需标准库。全部图表与扩展核查使用 NumPy，图表额外使用 Matplotlib；PDF 调查工具需要 pypdf、pypdfium2 与 Pillow。

在项目根目录建立虚拟环境、安装 requirements.txt 后，可运行：

~~~bash
python examples/run_experiments.py
python scripts/generate_figures.py
python scripts/check_math.py
~~~

数据固定在 examples/models.py 中，路径均相对于脚本所在的项目目录。输出为 results/experiments.json 与 docs/assets/ 下的 SVG，没有网络下载或随机抽样。

扩展检查覆盖中心路径的精确间隙、逻辑损失的梯度、TV 的次梯度证书、D-optimal 的原始与对偶值、套利证书和矩阵分块消元等。具体实际运行结果见[验收报告](./report.md)。
