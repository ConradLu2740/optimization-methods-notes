# -*- coding: utf-8 -*-
# Beale 循环反例（课件 s082 / 第一册 §3.3）三种选主元规则对比演示
from fractions import Fraction as F

c = [F(0), F(0), F(0), F(-3,4), F(20), F(-1,2), F(6)]   # x1..x7
A = [[F(1), F(0), F(0), F(1,4), -8, -1, 9],
     [F(0), F(1), F(0), F(1,2), -12, F(-1,2), 3],
     [F(0), F(0), F(1), F(0), F(0), 1, F(0)]]
b = [F(0), F(0), F(1)]
A = [[F(v) for v in row] for row in A]
b = [F(v) for v in b]
m, n = 3, 7

def gauss_solve(M, rhs):
    """解 M x = rhs（方阵，Fraction 精确）"""
    k = len(M)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    for col in range(k):
        p = next(r for r in range(col, k) if aug[r][col] != 0)
        aug[col], aug[p] = aug[p], aug[col]
        pv = aug[col][col]
        aug[col] = [v / pv for v in aug[col]]
        for r in range(k):
            if r != col and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [aug[r][j] - f * aug[col][j] for j in range(k + 1)]
    return [aug[i][k] for i in range(k)]

def report(basis, rule, maxit=12):
    print("=" * 62)
    print("规则:", rule)
    basis = basis[:]
    seen = {}
    for it in range(maxit):
        B = [[A[i][j] for j in basis] for i in range(m)]
        xB = gauss_solve(B, b)
        y = gauss_solve([[B[i][j] for j in range(m)] for i in range(m)], [c[j] for j in basis])
        # y^T B = c_B  -> 解转置
        BT = [[B[j][i] for j in range(m)] for i in range(m)]
        y = gauss_solve(BT, [c[j] for j in basis])
        sigma = [c[j] - sum(y[i] * A[i][j] for i in range(m)) for j in range(n)]
        z = sum(c[basis[i]] * xB[i] for i in range(m))
        key = tuple(sorted(basis))
        loop = key in seen
        print("轮 %d | 基 %s | x_B=%s | z=%s%s" % (
            it, [j + 1 for j in basis],
            [str(v) for v in xB], z,
            "  <-- 基重复!" if loop else ""))
        if loop:
            print(">> 已回到见过的基，死循环。")
            return
        seen[key] = it
        # 入基
        neg = [j for j in range(n) if sigma[j] < 0]
        if not neg:
            print(">> sigma 全 >= 0，最优！x* =", end=" ")
            xs = [F(0)] * n
            for i, j in enumerate(basis): xs[j] = xB[i]
            print([(str(v), k + 1) for k, v in enumerate(xs) if v != 0], "z* =", z)
            return
        if rule == "最负sigma":
            q = min(neg, key=lambda j: sigma[j])
        else:  # Bland
            q = min(neg)
        d = gauss_solve(B, [A[i][q] for i in range(m)])
        print("   sigma 负列: %s | 入基 x%d (%s)" % (
            [(j + 1, str(sigma[j])) for j in neg], q + 1,
            "最负" if rule == "最负sigma" else "下标最小"))
        ratios = [(xB[i] / d[i], basis[i], i) for i in range(m) if d[i] > 0]
        if not ratios:
            print(">> 无正元素，无界。"); return
        rmin = min(r for r, _, _ in ratios)
        tied = [(bi, i) for r, bi, i in ratios if r == rmin]
        if len(tied) > 1:
            print("   比值并列 %s (比值=%s)!" % ([bi + 1 for bi, _ in tied], rmin))
            out_i = min(tied, key=lambda t: t[0])[1] if rule == "Bland" else tied[0][1]
            print("   出基选 x%d (%s)" % (basis[out_i] + 1,
                  "基变量下标最小" if rule == "Bland" else "取最上(随便)"))
        else:
            out_i = tied[0][1]
            print("   比值 min=%s, 出基 x%d" % (rmin, basis[out_i] + 1))
        basis[out_i] = q

report([0, 1, 2], "最负sigma", maxit=8)
report([0, 1, 2], "Bland", maxit=12)

# 摄动法第一轮：b(eps) = (eps, eps^2, eps^3)
print("=" * 62)
print("摄动法第一轮演示: b(e)=(e, e^2, e^3), x4 入基")
print("  x1 行比值 = e / (1/4) = 4e")
print("  x2 行比值 = e^2 / (1/2) = 2e^2")
print("  e 充分小 (0<e<1) 时 2e^2 < 4e  =>  min 比值 = x2 行, 出基 x2")
print("  原问题里两行并列取谁都有理, 摄动后唯一决定 -> 不会并列 -> 非退化")
