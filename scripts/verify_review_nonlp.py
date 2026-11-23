"""复习课练习题 题7-11 的精确分数复验脚本。"""
from fractions import Fraction as F
import itertools

# ============ 题7 KKT ============
print('======== 题7 KKT ========')
# min x1^2 - x2 - 3x3
# s.t. g1 = -x1-x2-x3 >= 0 ;  h = x1^2+2x2-x3 = 0
# L = f - u1*g1 - v*h
# dL/dx1 = 2x1 + u1 - 2*v*x1 = 0
# dL/dx2 = -1 + u1 - 2*v = 0
# dL/dx3 = -3 + u1 + v = 0
# g1 = 0: x1+x2+x3 = 0 ;  h=0: x1^2+2x2-x3=0
# 情形A: g1 起作用 (x1+x2+x3=0)
#  由后两式: u1 = 1+2v, u1 = 3-v  => 1+2v = 3-v => v=2/3, u1=7/3
#  x1: 2x1 + 7/3 - 4x1/3 = 0 => (2/3)x1 = -7/3 => x1 = -7/2
#  x3 = x1^2+2x2 = 49/4+2x2 ; x2 = -x1-x3 = 7/2 - 49/4 - 2x2
#    => 3x2 = 7/2-49/4 = 14/4-49/4 = -35/4 => x2 = -35/12
#  x3 = 49/4 - 35/6 = 147/12-70/12 = 77/12
x7 = (F(-7,2), F(-35,12), F(77,12))
u1 = F(7,3); v = F(2,3)
g1 = -x7[0]-x7[1]-x7[2]
h = x7[0]**2 + 2*x7[1] - x7[2]
print('x* =', x7, 'u1 =', u1, 'v =', v)
print('g1 =', g1, '(=0)', 'h =', h, '(=0)')
print('KKT dL/dx = (0,0,0):',
      [2*x7[0]+u1-2*v*x7[0], -1+u1-2*v, -3+u1+v])
# 临界锥: 约束线性化 dg1 = -(d1+d2+d3)=0, dh = 2x1 d1 + 2 d2 - d3 = 0
# => d1+d2+d3=0, -7 d1 + 2 d2 - d3 = 0
# d3 = -d1-d2 => -7d1+2d2+d1+d2 = 0 => -6d1+3d2=0 => d2=2d1, d3=-3d1
# nabla^2_xx L = diag(2-2v, 0, 0) = diag(2/3,0,0)
# d^T H d = (2/3) d1^2
for d1 in [F(1), F(2), F(-3,5)]:
    d = (d1, 2*d1, -3*d1)
    quad = (F(2)-2*v)*d[0]**2
    print(f'  d={d}: d^T nabla^2L d = {quad}')
# 消元法复核（全局）
# x3 = x1^2+2x2, x2 = (-x1-x1^2)/3
# f = x1^2 - x2 - 3x3 = x1^2 - x2 - 3x1^2 - 6x2 = -2x1^2 -7x2 = -2x1^2 + 7(x1+x1^2)/3
import numpy as np
def f7(x1):
    x2 = (-x1-x1**2)/3
    x3 = x1**2+2*x2
    return x1**2 - x2 - 3*x3
# 精确: f = (-6x1^2 + 7x1 + 7x1^2)/3 = (x1^2+7x1)/3
def f7ex(x1):
    return (x1**2+7*x1)/3
for x1 in [F(-7,2), F(-3), F(0), F(1)]:
    assert f7(x1) == f7ex(x1), x1
print('消元复核: f(x1) = (x1^2+7x1)/3, x1* = -7/2, f* =', f7ex(F(-7,2)))
# 数值扫描: 沿消元曲线全体可行点
vals = [f7ex(F(i,10)) for i in range(-100, 101)]
print('扫描 x1∈[-10,10] 步长0.1: min =', min(vals), 'at', [F(i,10) for i in range(-100,101)][vals.index(min(vals))])

# ============ 题8 最速下降 vs 牛顿方向 ============
print()
print('======== 题8 ========')
x = (F(1), F(1))
g = (4*x[0], 2*x[1])   # (4,2)
H = [[F(4), F(0)], [F(0), F(2)]]
print('grad f =', g)
print('最速下降方向 d = -grad =', (-g[0], -g[1]))
# 牛顿: d = -H^{-1} g
det = H[0][0]*H[1][1] - H[0][1]*H[1][0]
Hinv = [[H[1][1]/det, -H[0][1]/det], [-H[1][0]/det, H[0][0]/det]]
dn = (-(Hinv[0][0]*g[0]+Hinv[0][1]*g[1]), -(Hinv[1][0]*g[0]+Hinv[1][1]*g[1]))
print('Hinv =', Hinv, ' 牛顿方向 d =', dn)

# ============ 题9 FR 共轭梯度 ============
print()
print('======== 题9 FR 共轭梯度 ========')
# min 0.5x1^2 + x2^2 ; A = diag(1,2), b=0
A = [[F(1), F(0)], [F(0), F(2)]]
def grad(x):
    return (A[0][0]*x[0]+A[0][1]*x[1], A[1][0]*x[0]+A[1][1]*x[1])
x1 = (F(4), F(4))
g1 = grad(x1)
d1 = (-g1[0], -g1[1])
Ad = (A[0][0]*d1[0]+A[0][1]*d1[1], A[1][0]*d1[0]+A[1][1]*d1[1])
lam = -(g1[0]*d1[0]+g1[1]*d1[1])/(d1[0]*Ad[0]+d1[1]*Ad[1])
x2 = (x1[0]+lam*d1[0], x1[1]+lam*d1[1])
print('x^(1) =', x1, 'g^(1) =', g1, 'd^(1) =', d1)
print('lambda_1 =', lam, 'x^(2) =', x2)
g2 = grad(x2)
beta = (g2[0]**2+g2[1]**2)/(g1[0]**2+g1[1]**2)
d2 = (-g2[0]+beta*d1[0], -g2[1]+beta*d1[1])
print('g^(2) =', g2, 'beta_1 =', beta, 'd^(2) =', d2)
Ad2 = (A[0][0]*d2[0]+A[0][1]*d2[1], A[1][0]*d2[0]+A[1][1]*d2[1])
lam2 = -(g2[0]*d2[0]+g2[1]*d2[1])/(d2[0]*Ad2[0]+d2[1]*Ad2[1])
x3 = (x2[0]+lam2*d2[0], x2[1]+lam2*d2[1])
print('lambda_2 =', lam2, 'x^(3) =', x3, '（应为 (0,0)）')
# 校验共轭性
print('d1^T A d2 =', d1[0]*Ad2[0]+d1[1]*Ad2[1], '（应为 0）')

# ============ 题10 DFP ============
print()
print('======== 题10 DFP ========')
# min x1^2+3x2^2 ; A = diag(2,6), grad = (2x1, 6x2)
A = [[F(2), F(0)], [F(0), F(6)]]
def grad(x):
    return (A[0][0]*x[0]+A[0][1]*x[1], A[1][0]*x[0]+A[1][1]*x[1])
x0 = (F(1), F(-1))
H = [[F(2), F(1)], [F(1), F(1)]]
print('x^(0) =', x0, 'H1 =', H)
g = grad(x0)
print('g^(0) =', g)
d = (-(H[0][0]*g[0]+H[0][1]*g[1]), -(H[1][0]*g[0]+H[1][1]*g[1]))
print('d^(0) = -H1 g =', d)
Ad = (A[0][0]*d[0]+A[0][1]*d[1], A[1][0]*d[0]+A[1][1]*d[1])
lam = -(g[0]*d[0]+g[1]*d[1])/(d[0]*Ad[0]+d[1]*Ad[1])
x1 = (x0[0]+lam*d[0], x0[1]+lam*d[1])
print('lambda_0 =', lam, 'x^(1) =', x1)
g1 = grad(x1)
p = (x1[0]-x0[0], x1[1]-x0[1])
q = (g1[0]-g[0], g1[1]-g[1])
print('p =', p, 'q =', q)
# DFP: H+ = H + p p^T/(p^T q) - H q q^T H/(q^T H q)
ptq = p[0]*q[0]+p[1]*q[1]
Hq = (H[0][0]*q[0]+H[0][1]*q[1], H[1][0]*q[0]+H[1][1]*q[1])
qtHq = q[0]*Hq[0]+q[1]*Hq[1]
print('p^T q =', ptq, 'q^T H q =', qtHq)
H2 = [[H[i][j] + p[i]*p[j]/ptq - Hq[i]*Hq[j]/qtHq for j in range(2)] for i in range(2)]
print('H2 =', [[str(v) for v in row] for row in H2])
d2 = (-(H2[0][0]*g1[0]+H2[0][1]*g1[1]), -(H2[1][0]*g1[0]+H2[1][1]*g1[1]))
print('d^(1) =', d2)
# 一步到位检验: 对二次函数, DFP 的 H2 d2 是否给出最优方向(直线指向 x*=0)?
Ad2 = (A[0][0]*d2[0]+A[0][1]*d2[1], A[1][0]*d2[0]+A[1][1]*d2[1])
lam2 = -(g1[0]*d2[0]+g1[1]*d2[1])/(d2[0]*Ad2[0]+d2[1]*Ad2[1])
x2 = (x1[0]+lam2*d2[0], x1[1]+lam2*d2[1])
print('lambda_1 =', lam2, 'x^(2) =', x2, '（应为 (0,0)）')
# 校验共轭性
print('d^(0)^T A d^(1) =', d[0]*Ad2[0]+d[1]*Ad2[1], '（应为 0）')
# 拟牛顿条件 H2 q = p ?
Hq2 = (H2[0][0]*q[0]+H2[0][1]*q[1], H2[1][0]*q[0]+H2[1][1]*q[1])
print('H2 q =', Hq2, 'p =', p)

# ============ 题11-1 Zoutendijk 方向条件 ============
print()
print('======== 题11-1 Zoutendijk ========')
# min x1^2+2x2^2  s.t. g1=x1+x2-1>=0, g2=x2-1>=0
# x=(1,1): g1=1>0 **不起作用**, g2=0 **起作用**; nabla f=(2,4), nabla g2=(0,1)
nf = (F(2), F(4)); ng1 = (F(1), F(1)); ng2 = (F(0), F(1))
print('x=(1,1): nabla f =', nf, 'nabla g1 =', ng1, '(g1=1>0 不起作用)', 'nabla g2 =', ng2, '(g2=0 起作用)')
print('Zoutendijk 条件: nabla f^T d<0 且 nabla g2^T d>0  =>  2d1+4d2<0 且 d2>0')
for d in [(-3,1), (-2,1), (-5,2), (0,-1), (-1,0), (-4,1), (-10,3)]:
    dd = (F(d[0]), F(d[1]))
    ok = (nf[0]*dd[0]+nf[1]*dd[1] < 0) and (ng2[0]*dd[0]+ng2[1]*dd[1] > 0)
    print(f'  d={dd}: 可行下降? {ok}   (nabla f^T d = {nf[0]*dd[0]+nf[1]*dd[1]}, d2 = {dd[1]})')

# ============ 题11-2 Rosen 梯度投影 ============
print()
print('======== 题11-2 Rosen ========')
M = [[F(0), F(1)]]          # 起作用约束只有 g2=x2-1
MMt = [[sum(M[0][k]*M[0][k] for k in range(2))]]   # [[1]]
MMt_inv = [[F(1)]]
tmp = [[sum(MMt_inv[i][k]*M[k][j] for k in range(1)) for j in range(2)] for i in range(1)]
print('M =', M, ' MM^T =', MMt, ' (MM^T)^-1 M =', tmp)
PN = [[(F(1) if i == j else F(0)) - sum(M[k][i]*tmp[k][j] for k in range(1)) for j in range(2)] for i in range(2)]
print('P_N(M) = I - M^T(MM^T)^-1 M =', PN)
d = (-(PN[0][0]*nf[0]+PN[0][1]*nf[1]), -(PN[1][0]*nf[0]+PN[1][1]*nf[1]))
print('d = -P_N(M) nabla f =', d)
Md = (M[0][0]*d[0]+M[0][1]*d[1])
print('M d =', Md, '(应为0)', ' nabla f^T d =', nf[0]*d[0]+nf[1]*d[1], '(应<0)')
# Th12.2.2 乘子判别的前提是 P_N(M)∇f = 0（本题 P_N∇f=(2,0)≠0，前提不成立），
# 故不走乘子判别，直接由 Th12.2.1 得方向；d≠0 即说明 (1,1) 不是 KKT 点。
u = MMt_inv[0][0]*(M[0][0]*nf[0]+M[0][1]*nf[1])
print('（仅供参考）w =', u, '；但 P_N∇f≠0 ⇒ Th12.2.2 前提不成立，无需判 u 的符号')
# KKT 复核: nabla f = u*nabla g2 ?  (2,4) = u(0,1) 无解 => 确非 KKT
print('KKT 复核: (2,4)=u*(0,1) 无解 => (1,1) 非 KKT 点')

# ============ 题11-3 罚函数法 ============
print()
print('======== 题11-3 罚函数 ========')
# min x1^2+2x2^2 s.t. g1=x1+x2-1>=0, g2=x2-1>=0
# 直接判定: 可行域 {x2>=1, x1>=1-x2}; 目标单调增 => x*=(0,1), z*=2
print('直接判定: x*=(0,1), z*=2')
# --- 内点(障碍)法 ---
# F = f + mu*(1/g1 + 1/g2), 严格内点 g1>0, g2>0
# 驻点: 2x1 - mu/g1^2 = 0 ; 4x2 - mu/g1^2 - mu/g2^2 = 0
# 记 s=x1+x2-1, t=x2-1 (s,t>0): 2(s-t)=mu/s^2, 4(1+t)=mu/s^2+mu/t^2
# 渐近: s~ (mu/2)^(1/3), t~ sqrt(mu)/2  => x1=s-t->0, x2=1+t->1
print('内点法 F = f + mu*(1/(x1+x2-1) + 1/(x2-1))')
import mpmath as mp
def inner_solve(mu):
    def F1(S, T): return 2*(S-T) - mu/S**2
    def F2(S, T): return 4*(1+T) - mu/S**2 - mu/T**2
    # 渐近猜测作起点: s~(mu/2)^(1/3), t~sqrt(mu)/2
    S0 = max((mu/2.0)**(1.0/3.0), 1e-12); T0 = max(mu**0.5/2.0, 1e-12)
    best = None
    for f in (1.0, 0.3, 3.0, 0.1, 10.0):
        try:
            r = mp.findroot(lambda S, T: (F1(S,T), F2(S,T)), (S0*f, T0*f), tol=1e-30, maxsteps=500)
            S, T = float(r[0]), float(r[1])
            if S > 0 and T > 0:
                val = F1(S,T)**2+F2(S,T)**2
                if best is None or val < best[0]: best = (val, S, T)
        except Exception:
            pass
    return best
for muv in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
    b = inner_solve(muv)
    if b:
        _, S, T = b
        x1, x2 = S-T, 1+T
        print(f'  mu={muv:g}: x1={x1:.8f}, x2={x2:.8f}, f={x1**2+2*x2**2:.8f}')
    else:
        print(f'  mu={muv:g}: 求解失败')
print('  预期 mu->0: (x1,x2)->(0,1), f->2')
# --- 外点法 ---
# F = f + mu*[(max{0,-g1})^2 + (max{0,-g2})^2]
# 两约束皆违反区(δ1=1-x1-x2>0, δ2=1-x2>0):
#   ∂F/∂x1 = 2x1 - 2mu δ1 = 0                     (A)
#   ∂F/∂x2 = 4x2 - 2mu δ1 - 2mu δ2 = 0             (B)
#   δ2 = (2-x1)/(2+mu) ;  δ1 = [2-x1(3+mu)]/(2+mu)
#   x1[(2+mu)+mu(3+mu)] = 2mu  =>  x1 = 2mu/(mu^2+4mu+2)
#   x2 = 1-δ2 = mu(mu+2)/(mu^2+4mu+2)
print('外点法: 全违反区闭式解 x1(mu)=2mu/(mu^2+4mu+2), x2(mu)=mu(mu+2)/(mu^2+4mu+2)')
def ext(mu):
    return (2*mu/(mu**2+4*mu+2), mu*(mu+2)/(mu**2+4*mu+2))
for muv in [F(1), F(10), F(100), F(1000)]:
    x1e, x2e = ext(muv)
    d1 = 1-x1e-x2e; d2 = 1-x2e
    fv = x1e**2+2*x2e**2
    print(f'  mu={muv}: x=({float(x1e):.6f},{float(x2e):.6f}), f={float(fv):.6f}, '
          f'违反量=({float(d1):.6f},{float(d2):.6f})')
    assert d1 > 0 and d2 > 0
# 闭式解确为 F 的全局最小(多起点数值复核, 覆盖四个区域)
print('外点法数值复核(闭式解 vs 多起点全局最小):')
import numpy as np
from scipy.optimize import minimize
for muv in [1.0, 10.0, 100.0, 1000.0]:
    def Fe(z, mu=muv):
        x1, x2 = z
        p = 0.0
        if 1-x1-x2 > 0: p += (1-x1-x2)**2
        if 1-x2 > 0: p += (1-x2)**2
        return x1**2+2*x2**2+mu*p
    best = None
    for st in [[0.0,0.5],[0.0,1.5],[0.5,0.5],[-1.0,1.0],[1.0,1.0],[0.0,0.0],[2.0,0.0],[0.5,2.0]]:
        r = minimize(Fe, st, method='Nelder-Mead', options={'xatol':1e-14,'fatol':1e-16,'maxiter':20000})
        if best is None or r.fun < best.fun: best = r
    xe = ext(muv)
    Fe_closed = Fe([xe[0], xe[1]])
    ok = abs(best.fun-Fe_closed) < 1e-7 and abs(best.x[0]-xe[0]) < 1e-4 and abs(best.x[1]-xe[1]) < 1e-4
    print(f'  mu={muv:g}: 数值最小 x=({best.x[0]:.10f},{best.x[1]:.10f}) F={best.fun:.10f}; '
          f'闭式 x=({float(xe[0]):.10f},{float(xe[1]):.10f}) F={Fe_closed:.10f}; 一致? {ok}')
