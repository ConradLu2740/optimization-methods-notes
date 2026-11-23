# -*- coding: utf-8 -*-
"""第六卷（2026-11-18）计算题精确验证：
1. 单纯形法（分数表 + Bland 防退化，scipy 交叉验证）
2. Fibonacci 一维搜索 n=6 三轮
3. 内点罚函数（负对数障碍）闭式解 + 极限 + KKT
4. BFGS 两步（分数）
5. CH7 无约束驻点判别
"""
from fractions import Fraction as F
import sympy as sp

print("=" * 70)
print("题1 单纯形法：min z = -2x1 -3x2  s.t. x1+x2<=5, x1+4x2<=12, x>=0")
print("=" * 70)

c = [F(-2), F(-3)]
A = [[F(1), F(1)], [F(1), F(4)]]
b = [F(5), F(12)]
m, n = 2, 2
# 标准形：加松弛变量 s1,s2（基）
T = [row[:] + [F(1) if i == j else F(0) for j in range(m)] + [b[i]] for i, row in enumerate(A)]
cb = [F(0)] * m
basis = [n + i for i in range(m)]

def show(T, cb, basis, tag):
    zj = [sum(cb[i] * T[i][j] for i in range(m)) for j in range(n + m)]
    net = [c[j] - zj[j] if j < n else F(0) for j in range(n + m)]  # min 化：检验数 = c - zj，负则进基
    hdr = "x1   x2   s1   s2   rhs"
    print(f"\n[{tag}] 基变量: {['x%d' % (v+1) for v in basis]}")
    print("        " + hdr)
    for i in range(m):
        cells = "  ".join(f"{str(T[i][j]):>4}" for j in range(n + m + 1))
        print(f"  row{i + 1}: {cells}")
    print("  检验数(c-zj): " + "  ".join(f"{str(net[j]):>4}" for j in range(n + m)))

show(T, cb, basis, "初始表")
for it in range(1, 6):
    # 课堂口径：检验数最负者进基（并列取 index 小）
    enter, best = None, F(0)
    for j in range(n):
        zj = sum(cb[i] * T[i][j] for i in range(m))
        if c[j] - zj < best:
            best, enter = c[j] - zj, j
    if enter is None:
        print(f"\n第 {it} 轮：检验数全 >= 0，达到最优")
        break
    # 出基：最小比值，Bland 并列取基变量 index 最小
    ratios = []
    for i in range(m):
        if T[i][enter] > 0:
            ratios.append((T[i][n + m] / T[i][enter], i))
    ratios.sort(key=lambda t: (t[0], basis[t[1]]))
    r, leave = ratios[0]
    piv = T[leave][enter]
    T[leave] = [v / piv for v in T[leave]]
    for i in range(m):
        if i != leave and T[i][enter] != 0:
            f0 = T[i][enter]
            T[i] = [T[i][j] - f0 * T[leave][j] for j in range(n + m + 1)]
    basis[leave] = enter
    cb = [c[v] if v < n else F(0) for v in basis]
    show(T, cb, basis, f"第 {it} 轮（x{enter+1} 进基）")
    zval = -sum(cb[i] * T[i][n + m] for i in range(m))
    print(f"  -> z = {zval}")

x = [F(0)] * n
for i, v in enumerate(basis):
    if v < n:
        x[v] = T[i][n + m]
print(f"\n最优解 x* = ({x[0]}, {x[1]}) = ({float(x[0]):.4f}, {float(x[1]):.4f}), z* = {-sum(c[j]*x[j] for j in range(n))}")

# scipy 交叉验证
from scipy.optimize import linprog
r = linprog([2, 3], A_ub=[[1, 1], [1, 4]], b_ub=[5, 12], bounds=[(0, None)] * 2, method="highs")
print(f"scipy 验证: x={r.x}, z={-r.fun}  (与分数解一致: {abs(r.x[0]-float(x[0]))<1e-9 and abs(r.x[1]-float(x[1]))<1e-9})")

print()
print("=" * 70)
print("题2 Fibonacci：min f(x)=x^2-3x+5, [a1,b1]=[0,4], 要求最终区间长<=0.5")
print("=" * 70)

# F0=F1=1（讲义口径）
fib = [1, 1]
while len(fib) < 10:
    fib.append(fib[-1] + fib[-2])
print("Fibonacci 数列 F0..:", fib[:9])
L0 = F(4)
delta = F(1, 2)
for nn in range(2, 9):
    if F(fib[nn]) >= L0 / delta:
        break
print(f"定 n: F_n >= L0/delta = {L0}/{delta} = {L0/delta} => n = {nn}, F_{nn} = {fib[nn]}")

def f(x):
    return x * x - 3 * x + 5

a, bb = F(0), F(4)
pts = {}
for k in range(1, 4):
    Lk = bb - a
    lam = a + F(fib[nn - k - 1]) / F(fib[nn - k + 1]) * Lk
    mu = a + F(fib[nn - k]) / F(fib[nn - k + 1]) * Lk
    fl, fm = f(lam), f(mu)
    print(f"\n第{k}轮: [{a}, {bb}]  L={Lk}")
    print(f"  lambda_{k} = {a} + F_{nn-k-1}/F_{nn-k+1}*{Lk} = {lam},  f={fl}")
    print(f"  mu_{k}      = {a} + F_{nn-k}/F_{nn-k+1}*{Lk} = {mu},  f={fm}")
    if fl <= fm:
        a, bb = a, mu
        print(f"  f(lambda)<=f(mu) => 舍右, 新区间 [{a}, {bb}]")
    else:
        a, bb = lam, bb
        print(f"  f(lambda)> f(mu) => 舍左, 新区间 [{a}, {bb}]")
print(f"\n三轮后区间 [{a}, {bb}] 长 {bb-a}")
print(f"第4轮取点: lambda_4 = a + F1/F5*L, mu_4 = a + F2/F5*L（F1=F2=1 => 两点重合）")
print(f"最终区间长度上界 = L0/F_n = {L0}/{fib[nn]} = {L0/fib[nn]} <= {delta}: {L0/fib[nn] <= delta}")

print()
print("=" * 70)
print("题3 内点罚函数：min x1^2+2x2^2 s.t. x1+x2>=1（负对数障碍 B=f-mu*ln(x1+x2-1)）")
print("=" * 70)
x1, x2, mu = sp.symbols("x1 x2 mu", positive=True)
g = x1 + x2 - 1
B = x1 ** 2 + 2 * x2 ** 2 - mu * sp.log(g)
sol = sp.solve([sp.diff(B, x1), sp.diff(B, x2)], [x1, x2], dict=True)
print("驻点方程解:", sol)
s = (-1 + sp.sqrt(1 + 3 * mu)) / 2
xs1 = (1 + sp.sqrt(1 + 3 * mu)) / 3
xs2 = (1 + sp.sqrt(1 + 3 * mu)) / 6
print(f"s(mu) = x1+x2-1 = {sp.simplify(xs1 + xs2 - 1)}")
print(f"x1(mu) = {xs1}, x2(mu) = {xs2}")
print(f"mu->0 极限: x1->{sp.limit(xs1, mu, 0)}, x2->{sp.limit(xs2, mu, 0)}")
for mv in [F(1, 100), F(1, 10), F(1)]:
    mf = float(mv)
    x1v = (1 + (1 + 3 * mf) ** 0.5) / 3
    x2v = (1 + (1 + 3 * mf) ** 0.5) / 6
    print(f"  mu={mv}: x=({x1v:.4f}, {x2v:.4f}), f={x1v**2 + 2*x2v**2:.6f}")
# KKT 验证 (2/3,1/3)
u = sp.symbols("u")
kkt = sp.solve([2 * sp.Rational(2, 3) - u, 4 * sp.Rational(1, 3) - u], [u])
print(f"KKT 乘子 u = {kkt}, f* = {sp.Rational(2,3)**2 + 2*sp.Rational(1,3)**2}")
# scipy 验证原问题
r = linprog([0, 0], A_ub=[[-1, -1]], b_ub=[-1], bounds=[(None, None)] * 2)
from scipy.optimize import minimize
res = minimize(lambda v: v[0] ** 2 + 2 * v[1] ** 2, [1.0, 1.0],
               constraints={"type": "ineq", "fun": lambda v: v[0] + v[1] - 1})
print(f"原问题数值解: x={res.x}, f={res.fun}")

print()
print("=" * 70)
print("题4 BFGS：min x1^2+2x2^2-2x1-6x2, 初点 (2,2)")
print("=" * 70)

def bfgs_two_steps():
    A_mat = sp.Matrix([[1, 0], [0, 2]])
    bb_vec = sp.Matrix([1, 3])
    x = sp.Matrix([2, 2])
    H = sp.eye(2)
    for k in range(1, 4):
        g = A_mat * x - bb_vec
        print(f"\n第{k}迭代: x^({k}) = {x.T}, g^({k}) = {g.T}, f = {(x.T*A_mat*x/2 - bb_vec.T*x)[0]}")
        if g == sp.zeros(2, 1):
            print("  g=0，终止")
            break
        p = -H * g
        print(f"  p = -H*g = {p.T}")
        # 精确线搜 alpha = -g^T p / (p^T A p)
        denom = (p.T * A_mat * p)[0]
        alpha = (-(g.T * p)[0]) / denom
        print(f"  alpha = -g^Tp/(p^TAp) = {alpha}")
        x_new = x + alpha * p
        print(f"  x^({k+1}) = {x_new.T} = ({[str(v) for v in x_new]})")
        g_new = A_mat * x_new - bb_vec
        s = x_new - x
        y = g_new - g
        ys = (y.T * s)[0]
        rho = 1 / ys
        print(f"  s={s.T}, y={y.T}, y^Ts={ys}, rho={rho}")
        H = (sp.eye(2) - rho * s * y.T) * H * (sp.eye(2) - rho * y * s.T) + rho * s * s.T
        print(f"  H_{k+1} = {H.tolist()}")
        # 共轭检验 p_{k+1}^T A s_k = 0
        pn = -H * g_new
        conj = (pn.T * A_mat * s)[0]
        print(f"  下一步 p^({k+1}) = {pn.T}, 共轭检验 p^TAs = {conj}")
        x = x_new

bfgs_two_steps()
print(f"\nx* 理论解 A^-1 b = {sp.Matrix([[1,0],[0,2]]).inv()*sp.Matrix([1,3])}, f* = {-11/2}")

print()
print("=" * 70)
print("题5 无约束驻点：f(x1,x2)=x1^3+x2^3-3x1x2")
print("=" * 70)
X1, X2 = sp.symbols("x1 x2")
f5 = X1 ** 3 + X2 ** 3 - 3 * X1 * X2
grad = [sp.diff(f5, X1), sp.diff(f5, X2)]
print("梯度:", grad)
crit = sp.solve(grad, [X1, X2], dict=True)
print("驻点:", crit)
H5 = sp.hessian(f5, (X1, X2))
print("Hessian:", H5.tolist())
for pt in crit:
    p = {X1: pt[X1], X2: pt[X2]}
    Hv = H5.subs(p)
    ev = Hv.eigenvals()
    print(f"  驻点 {p}: H={Hv.tolist()}, 特征值={ev}, f={f5.subs(p)}")
