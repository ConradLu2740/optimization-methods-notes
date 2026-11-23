# -*- coding: utf-8 -*-
"""练习题-大M法-2026-11-19 出题验证。
题面：min z = -x1 - 3x2 - 4x3
 s.t. x1 + 2x2 + x3 <= 7   -> x4 松弛
      x1 + 4x2 + x3 >= 10  -> x5 剩余 + x6 人工
      x1 + x2 + 4x3 = 7    -> x7 人工
      x >= 0
"""
from fractions import Fraction as F
from itertools import combinations
from bigM_lib import build, sigma, order, show, pivot, Mfmt

c = [F(-1), F(-3), F(-4)]
A = [[F(1), F(2), F(1)], [F(1), F(4), F(1)], [F(1), F(1), F(4)]]
b = [F(7), F(10), F(7)]
cost, rows, basis = build(c, A, b, slack=[0], surplus=[1], art=[1, 2])
print("初始基:", ["x%d" % (i + 1) for i in basis], "（x6、x7 为人工变量，费用 +M）")
show("初始表", cost, rows, basis)

it = 0
while True:
    it += 1
    sg = sigma(cost, rows, basis)
    r = pivot(cost, rows, basis)
    if r is None:
        print("所有检验数 >= 0，迭代停止。共 %d 次迭代。\n" % (it - 1))
        break
    enter, old, ratio, piv = r
    print(">>> 迭代 %d: x%d 入基, x%d 出基; 入基列检验数 %s; 比值 %s; 主元 %s" %
          (it, enter + 1, old + 1, Mfmt(sg[enter]), ratio, piv))
    show("迭代 %d 后" % it, cost, rows, basis)

x = [F(0)] * len(cost)
for i, bi in enumerate(basis):
    x[bi] = rows[i][-1]
z = sum(cost[j][0] * x[j] for j in range(len(cost)))
zm = sum(cost[j][1] * x[j] for j in range(len(cost)))
print("解:", ", ".join("x%d = %s" % (j + 1, x[j]) for j in range(3)))
print("z* =", z, "；M 系数 =", zm, "（应为 0）")
print("其余:", ", ".join("x%d = %s" % (j + 1, x[j]) for j in range(3, len(cost))))

# ---- 独立复核 1：标准形顶点枚举 ----
cols = []
for j in range(3): cols.append([A[i][j] for i in range(3)])
cols.append([F(1) if i == 0 else F(0) for i in range(3)])
cols.append([F(-1) if i == 1 else F(0) for i in range(3)])
cols.append([F(1) if i == 1 else F(0) for i in range(3)])
cols.append([F(1) if i == 2 else F(0) for i in range(3)])
m, total = 3, 7
sols = []
for comb in combinations(range(total), 3):
    M = [[cols[j][i] for j in comb] + [b[i]] for i in range(m)]
    for col in range(3):
        p = next((r for r in range(col, 3) if M[r][col] != 0), None)
        if p is None: break
        M[col], M[p] = M[p], M[col]
        pv = M[col][col]; M[col] = [v / pv for v in M[col]]
        for r in range(3):
            if r != col and M[r][col] != 0:
                f = M[r][col]; M[r] = [M[r][k] - f * M[col][k] for k in range(4)]
    else:
        xv = [M[i][3] for i in range(3)]
        if all(v >= 0 for v in xv):
            full = [F(0)] * total
            for k, j in enumerate(comb): full[j] = xv[k]
            if all(sum(cols[j][i] * full[j] for j in range(total)) == b[i] for i in range(m)):
                zz = sum(c[j] * full[j] for j in range(3))
                sols.append((zz, tuple(full)))
print("\n顶点枚举：可行基本解 %d 个" % len(sols))
for s in sorted(sols):
    mark = "  <== 最优" if s[0] == min(t[0] for t in sols) else ""
    print("   z = %-6s x = %s%s" % (s[0], s[1], mark))
best = min(sols)
print("唯一最优？", sum(1 for s in sols if s[0] == best[0]) == 1,
      "；与大M结果一致？", best[1][:3] == tuple(x[:3]) and best[0] == z)
