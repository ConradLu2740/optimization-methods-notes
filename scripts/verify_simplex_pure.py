"""复核选定题目：单纯形纯表（<= only，无人工变量，最小化，3 次迭代）。

min z = -4x1 - 3x2 - 5x3
s.t.
  2x1 + 3x2 + 3x3 <= 20
  2x1 + 2x2 + 4x3 <= 24
  5x1 +  x2 + 2x3 <= 22
  x >= 0
"""
import itertools
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

c = [F(-4), F(-3), F(-5)]
A = [[F(2), F(3), F(3)],
     [F(2), F(2), F(4)],
     [F(5), F(1), F(2)]]
b = [F(20), F(24), F(22)]
m, n = 3, 3
N = n + m

basis = [n + i for i in range(m)]
T = [[F(0)] * (N + 1) for _ in range(m)]
for i in range(m):
    for j in range(n):
        T[i][j] = A[i][j]
    T[i][n + i] = F(1)
    T[i][N] = b[i]


def fmt(fr):
    fr = F(fr)
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def name(j):
    return f"x{j+1}" if j < n else f"x{n + (j - n) + 1}"


def sigma(T):
    s = [F(0)] * N
    for j in range(N):
        val = F(0)
        for i in range(m):
            cb = c[basis[i]] if basis[i] < n else F(0)
            val += cb * T[i][j]
        s[j] = val - (c[j] if j < n else F(0))
    return s


def dump(k, T, s, note=""):
    print(f"\n===== 表 {k} 基: {[name(j) for j in basis]} {note}")
    print("        " + " ".join(f"{name(j):>8}" for j in range(N)) + f"{'b':>8}")
    for i in range(m):
        print(f"  行{i+1}   " + " ".join(f"{fmt(T[i][j]):>8}" for j in range(N)) + f"{fmt(T[i][N]):>8}")
    print("  sigma  " + " ".join(f"{fmt(s[j]):>8}" for j in range(N)))


steps = []
for k in range(10):
    s = sigma(T)
    dump(k, T, s)
    pos = [j for j in range(N) if s[j] > 0]
    if not pos:
        x = [F(0)] * n
        for i, bi in enumerate(basis):
            if bi < n:
                x[bi] = T[i][N]
        z = sum(c[j] * x[j] for j in range(n))
        print(f"\n>>> 最优：x* = {[fmt(v) for v in x]}, z* = {fmt(z)}")
        break
    e = max(pos, key=lambda j: (s[j], -j))
    ratios = [(T[i][N] / T[i][e], i) for i in range(m) if T[i][e] > 0]
    rmin, r = min(ratios, key=lambda t: (t[0], t[1]))
    print(f">>> 入基 {name(e)} (sigma={fmt(s[e])})，出基 {name(basis[r])} (比值 {fmt(rmin)}，行 {r+1})")
    steps.append((name(e), name(basis[r]), fmt(rmin)))
    piv = T[r][e]
    T[r] = [v / piv for v in T[r]]
    for i in range(m):
        if i != r and T[i][e] != 0:
            f = T[i][e]
            T[i] = [T[i][j] - f * T[r][j] for j in range(N + 1)]
    basis[r] = e

print("\n迭代序列:", steps)

# scipy 交叉
r = linprog(c=[float(t) for t in c], A_ub=[[float(t) for t in row] for row in A],
            b_ub=[float(t) for t in b], bounds=[(0, None)] * 3, method="highs")
print("scipy:", r.x, r.fun, "| 与精确解一致:",
      all(abs(float(v) - t) < 1e-9 for v, t in zip([x], r.x)) if False else
      abs(r.fun - float(z)) < 1e-9 and all(abs(a - bb) < 1e-9 for a, bb in zip(r.x, [float(v) for v in x])))

# 顶点枚举：{3 个约束} + {3 个坐标平面 x_j=0} 共 6 个超平面取 3；可行性 = Av<=b 且 v>=0
Aa = np.vstack([np.array(A, dtype=float), np.eye(3)])
ba = np.hstack([np.array(b, dtype=float), np.zeros(3)])
Af, bf = np.array(A, dtype=float), np.array(b, dtype=float)
verts = []
for comb in itertools.combinations(range(6), 3):
    M = Aa[list(comb)]
    if abs(np.linalg.det(M)) < 1e-9:
        continue
    v = np.linalg.solve(M, ba[list(comb)])
    if np.all(v >= -1e-9) and np.all(Af @ v <= bf + 1e-9):
        t = tuple(F(t).limit_denominator(1000) for t in v)
        if t not in verts:
            verts.append(t)
print(f"\n可行顶点 {len(verts)} 个:")
for v in verts:
    val = sum(c[i] * v[i] for i in range(3))
    print("  ", tuple(fmt(t) for t in v), " z =", fmt(val), "<= 最优" if val >= z else "  ！！！更优")
opt = [v for v in verts if sum(c[i] * v[i] for i in range(3)) == z]
print("取到 z* 的顶点数 =", len(opt), "（应为 1，验证唯一最优）")
