# -*- coding: utf-8 -*-
"""复核"Zoutendijk + Rosen 求可行下降方向"练习题（CH12 深度口径：只到求方向）。

第一部分（Zoutendijk，线性约束）：
  min f = x1^2 + 2x2^2 + x1x2 - 2x1 - 6x2
  s.t. x1 + x2 <= 4 ; x1 + 3x2 <= 6 ; x >= 0
  x0 = (3, 1)  （两个约束均起作用）
  求可行下降方向：解 LP  max -grad_f^T d  s.t. A1 d >= 0, -1 <= d <= 1

第二部分（Rosen 梯度投影）：
  min f = x1^2 + 2x2^2 - 2x1 - 2x2
  s.t. x1 + x2 >= 2 ; x >= 0
  (a) x = (1, 1)：d = -P_N(M) grad_f
  (b) x = (4/3, 2/3)：投影是否为 0？是否 KKT？
"""
import itertools
from fractions import Fraction as F


def fmt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def mat_inv(M):
    """分数矩阵求逆（高斯-约当）。"""
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] + [F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [A[r][k] - f * A[col][k] for k in range(2 * n)]
    return [row[n:] for row in A]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(col) for col in zip(*A)]


print("=" * 72)
print("第一部分：Zoutendijk（线性约束，LP (12.1.10) 型）")
print("=" * 72)
# f = x1^2 + 2x2^2 + x1x2 - 2x1 - 6x2
# grad = (2x1 + x2 - 2, 4x2 + x1 - 6)
x0 = (F(3), F(1))
gf = (2 * x0[0] + x0[1] - 2, 4 * x0[1] + x0[0] - 6)
print("x0 =", [fmt(v) for v in x0], " grad f(x0) =", [fmt(v) for v in gf])
# g1 = 4 - x1 - x2 >= 0 -> grad (-1,-1) ; g2 = 6 - x1 - 3x2 >= 0 -> grad (-1,-3)
A1 = [[F(-1), F(-1)], [F(-1), F(-3)]]
print("A1 =", [[fmt(v) for v in row] for row in A1])
print("检查 x0 处约束值：g1 =", fmt(4 - x0[0] - x0[1]), " g2 =", fmt(6 - x0[0] - 3 * x0[1]),
      " -> 均 0，两个约束都起作用")

# LP: max -gf^T d  s.t. A1 d >= 0, -1 <= d_j <= 1
# 不等式统一为 <= 形式：-A1 d <= 0 -> [[1,1],[1,3]] d <= 0
G = [[F(1), F(1)], [F(1), F(3)]]
h = [F(0), F(0)]
box_lo, box_hi = [F(-1)] * 2, [F(1)] * 2
# 顶点枚举：约束为 2 个线性 + 4 个边界 = 6 个超平面取 2
Ga = G + [[F(1), F(0)], [F(-1), F(0)], [F(0), F(1)], [F(0), F(-1)]]
ha = h + [box_hi[0], -box_lo[0], box_hi[1], -box_lo[1]]
verts = []
for comb in itertools.combinations(range(6), 2):
    M = [Ga[i] for i in comb]
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if det == 0:
        continue
    rhs = [ha[i] for i in comb]
    d1 = (rhs[0] * M[1][1] - rhs[1] * M[0][1]) / det
    d2 = (M[0][0] * rhs[1] - M[1][0] * rhs[0]) / det
    d = (d1, d2)
    if all(sum(Ga[i][j] * d[j] for j in range(2)) <= ha[i] for i in range(6)):
        if d not in verts:
            verts.append(d)
print("\nLP 可行域顶点：")
best, bestval = None, None
for d in verts:
    val = -(gf[0] * d[0] + gf[1] * d[1])   # max -gf^T d
    print("   d =", [fmt(v) for v in d], "  -grad_f^T d =", fmt(val))
    if bestval is None or val > bestval:
        best, bestval = d, val
print("\n>>> LP 最优：d* =", [fmt(v) for v in best], " 最优值 =", fmt(bestval))
print(">>> 方向（去掉归一化）∝ (-3, 1)")
d = (F(-3), F(1))
print("验证：grad_f^T d =", fmt(gf[0] * d[0] + gf[1] * d[1]), "(<0 下降)")
print("      A1 d =", [fmt(sum(A1[i][j] * d[j] for j in range(2))) for i in range(2)], "(均 >=0 可行)")
print(">>> LP 最优值", fmt(bestval), "> 0  => x0 不是 KKT 点（Th12.1.2 口径）")

print()
print("=" * 72)
print("第二部分：Rosen 梯度投影")
print("=" * 72)
# f = x1^2 + 2x2^2 - 2x1 - 2x2 -> grad = (2x1 - 2, 4x2 - 2)


def grad2(x):
    return (2 * x[0] - 2, 4 * x[1] - 2)


def proj_null(M):
    """P_N(M) = I - M^T (M M^T)^-1 M"""
    Mt = transpose(M)
    MMt = matmul(M, Mt)
    inv = mat_inv(MMt)
    PR = matmul(Mt, matmul(inv, M))
    return [[(F(1) if i == j else F(0)) - PR[i][j] for j in range(2)] for i in range(2)]


# 起作用约束：g = x1 + x2 - 2 >= 0 -> grad (1,1)
for label, x in [("(a) x = (1,1)", (F(1), F(1))), ("(b) x = (4/3,2/3)", (F(4, 3), F(2, 3)))]:
    g = grad2(x)
    M = [[F(1), F(1)]]
    PN = proj_null(M)
    png = [sum(PN[i][j] * g[j] for j in range(2)) for i in range(2)]
    d = [-v for v in png]
    print(f"\n{label}: grad f = {[fmt(v) for v in g]}")
    print("   M =", [[fmt(v) for v in r] for r in M], " P_N(M) =", [[fmt(v) for v in r] for r in PN])
    print("   P_N grad f =", [fmt(v) for v in png])
    print("   d = -P_N grad f =", [fmt(v) for v in d])
    if any(v != 0 for v in d):
        print("   验证：grad_f^T d =", fmt(sum(g[i] * d[i] for i in range(2))), "(<0 下降)",
              "；grad_g^T d =", fmt(d[0] + d[1]), "(=0 沿约束面)")
    else:
        print("   => d = 0：投影为 0，KKT 点（Th12.2.2 口径）")

# f* 与全局性
xb = (F(4, 3), F(2, 3))
fstar = xb[0] ** 2 + 2 * xb[1] ** 2 - 2 * xb[0] - 2 * xb[1]
print("\n(b) 点沿约束线参数化验证：x1=t, x2=2-t -> f = 3t^2-8t+4, t=4/3 取极小")
print("   f* =", fmt(fstar))
print("   Hessian = diag(2,4) 正定 + Slater(x=(3/2,1)) => 凸规划，KKT 即全局最优")
# scipy 交叉
try:
    import numpy as np
    from scipy.optimize import minimize
    r = minimize(lambda v: v[0] ** 2 + 2 * v[1] ** 2 - 2 * v[0] - 2 * v[1], [0.0, 2.0],
                 constraints=[{"type": "ineq", "fun": lambda v: v[0] + v[1] - 2}],
                 bounds=[(0, None), (0, None)], method="SLSQP")
    print("   scipy/SLSQP:", np.round(r.x, 9), round(r.fun, 9),
          "| 一致:", abs(r.x[0] - 4 / 3) < 1e-7 and abs(r.x[1] - 2 / 3) < 1e-7 and abs(r.fun + 4 / 3) < 1e-7)
except Exception as e:
    print("   scipy 跳过:", e)
