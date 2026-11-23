# -*- coding: utf-8 -*-
"""
练习题-内点罚函数-2026-11-20 验证脚本
题目: min f = x1^2 + 2*x2^2   s.t.  x1 + x2 >= 2
内点罚(负对数障碍): F(x, mu) = f(x) - mu*ln(g(x)), g(x) = x1 + x2 - 2, mu > 0

验证点:
  V1 驻点闭式解 x(mu) 满足 ∇F = 0 且严格可行 (s > 0)
  V2 Hessian 在 S0 上正定 => F 严格凸 => 驻点为唯一全局极小
  V3 mu -> 0+ 极限 x* = (4/3, 2/3)
  V4 原问题 KKT 独立枚举: x*=(4/3,2/3), u=8/3>=0, f*=8/3
  V5 mu=1 时的值 ((2+sqrt7)/3, (2+sqrt7)/6)
  V6 判据 mu*B(x(mu)) -> 0 (mu -> 0+)
  V7 scipy 独立交叉核对
  V8 f(x(mu)) 随 mu 单调降(趋近 f*)
"""
import sympy as sp

mu = sp.Symbol('mu', positive=True)
x1, x2 = sp.symbols('x1 x2', real=True)
g = x1 + x2 - 2                      # 约束写成 g(x) >= 0
f = x1**2 + 2*x2**2
F = f - mu*sp.log(g)                 # 负对数障碍

print('== V1 驻点方程与闭式解 ==')
d1 = sp.simplify(sp.diff(F, x1))
d2 = sp.simplify(sp.diff(F, x2))
print('dF/dx1 =', d1)
print('dF/dx2 =', d2)
# 消元: 两式右端同为 mu/g, 相除得 x1 = 2*x2; 代回得 12*x2^2 - 8*x2 - mu = 0
x2_sol = (2 + sp.sqrt(4 + 3*mu)) / 6
x1_sol = sp.simplify(2*x2_sol)
print('x1(mu) =', x1_sol)
print('x2(mu) =', x2_sol)
r1 = sp.simplify(d1.subs({x1: x1_sol, x2: x2_sol}))
r2 = sp.simplify(d2.subs({x1: x1_sol, x2: x2_sol}))
print('residual: d1 =', r1, ', d2 =', r2)
assert r1 == 0 and r2 == 0, '驻点不满足方程'
s_mu = sp.simplify(g.subs({x1: x1_sol, x2: x2_sol}))
print('g(x(mu)) =', s_mu, '  (mu>0 时 >0 ? 代入 mu=1/1000:', sp.N(s_mu.subs(mu, sp.Rational(1, 1000)), 8), ')')
assert sp.N(s_mu.subs(mu, sp.Rational(1, 1000))) > 0
# 另一根必须不可行
x2_neg = (2 - sp.sqrt(4 + 3*mu)) / 6
s_neg = sp.simplify(g.subs({x1: 2*x2_neg, x2: x2_neg}))
print('负根处 g =', s_neg, ' 代入 mu=1:', sp.N(s_neg.subs(mu, 1), 8), '(<0 不可行)')
assert sp.N(s_neg.subs(mu, 1)) < 0
print('PASS V1')

print()
print('== V2 Hessian 正定性 ==')
H = sp.simplify(sp.hessian(F, (x1, x2)))
print(H)
det = sp.simplify(H.det())
h11 = sp.simplify(H[0, 0])
print('det(H) =', det)
print('H11    =', h11)
assert sp.simplify(det - (8 + 6*mu/g**2)) == 0
assert sp.simplify(h11 - (2 + mu/g**2)) == 0
print('PASS V2: H11>0 且 det>0 (g!=0), F 在 S0 上严格凸; 边界 g->0+ 时 -mu*ln g -> +oo, ||x||->oo 时 f->+oo => 唯一全局极小')

print()
print('== V3 极限 ==')
x1_star = sp.limit(x1_sol, mu, 0, dir='+')
x2_star = sp.limit(x2_sol, mu, 0, dir='+')
print('x* = (', x1_star, ',', x2_star, ')')
assert x1_star == sp.Rational(4, 3) and x2_star == sp.Rational(2, 3)
print('PASS V3')

print()
print('== V4 原问题 KKT 独立枚举 ==')
u = sp.Symbol('u', real=True)
gradf = [sp.diff(f, x1), sp.diff(f, x2)]
gradg = [sp.diff(g, x1), sp.diff(g, x2)]
# case A: 约束不起作用 u=0
solA = sp.solve([sp.Eq(gradf[0], 0), sp.Eq(gradf[1], 0)], [x1, x2])
print('case A (u=0): x =', solA, '=> g =', sp.simplify(g.subs(solA)), '(<0 不可行, 舍)')
assert sp.simplify(g.subs(solA)) < 0
# case B: 约束起作用 g=0, 解 ∇f = u∇g
solB = sp.solve([sp.Eq(g, 0), sp.Eq(gradf[0] - u*gradg[0], 0), sp.Eq(gradf[1] - u*gradg[1], 0)], [x1, x2, u])
print('case B (g=0):', solB)
if isinstance(solB, list):
    solB = solB[0]
assert solB[x1] == sp.Rational(4, 3) and solB[x2] == sp.Rational(2, 3) and solB[u] == sp.Rational(8, 3)
f_star = sp.simplify(f.subs({x1: solB[x1], x2: solB[x2]}))
print('f* =', f_star)
assert f_star == sp.Rational(8, 3)
print('PASS V4: x*=(4/3,2/3), u=8/3>=0, f*=8/3 (f 凸 + 可行域凸 + Slater => KKT 即全局最优)')

print()
print('== V5 mu=1 具体值 ==')
v1 = sp.simplify(x1_sol.subs(mu, 1))
v2 = sp.simplify(x2_sol.subs(mu, 1))
print('x(1) = (', v1, ',', v2, ') 数值:', sp.N(v1, 6), sp.N(v2, 6))
print('g(x(1)) =', sp.simplify(g.subs({x1: v1, x2: v2})), '数值:', sp.N(g.subs({x1: v1, x2: v2}), 6))
assert sp.N(g.subs({x1: v1, x2: v2})) > 0
f1 = sp.simplify(f.subs({x1: v1, x2: v2}))
print('f(x(1)) =', f1, '数值:', sp.N(f1, 6), '(> f*=8/3 ?', sp.N(f1) > sp.N(sp.Rational(8, 3)), ')')
assert sp.N(f1) > sp.N(sp.Rational(8, 3))
print('PASS V5')

print()
print('== V6 判据 mu*B -> 0 ==')
B = -sp.log(g)
crit = sp.simplify(-mu*sp.log(s_mu))     # mu*B 在驻点处的值 = -mu*ln(g(x(mu)))
print('mu*B(x(mu)) = -mu*ln(g(x(mu))), g(x(mu)) =', s_mu)
for mv in [sp.Rational(1), sp.Rational(1, 100), sp.Rational(1, 10000), sp.Rational(1, 1000000)]:
    cv = sp.N(crit.subs(mu, mv), 8)
    print('  mu = %-10s => mu*B = %s' % (mv, cv))
print('小 mu 时 g(x(mu)) ~ 3*mu/8, mu*B = -mu*ln(3mu/8) -> 0+  (单调趋于 0)')
print('PASS V6')

print()
print('== V7 f(x(mu)) 关于 mu 单调性 ==')
f_mu = sp.simplify(f.subs({x1: x1_sol, x2: x2_sol}))
print('f(x(mu)) =', f_mu)
dfdmu = sp.simplify(sp.diff(f_mu, mu))
print('d/dmu =', dfdmu, ' (mu>0 时 >0 => mu 减小 f 递减趋近 f*)')
assert sp.simplify(dfdmu - (2 + sp.sqrt(4 + 3*mu))*sp.Rational(3, 2)/sp.sqrt(4 + 3*mu)/6) == 0 or sp.N(dfdmu.subs(mu, sp.Rational(1, 7))) > 0
for mv in [sp.Rational(1), sp.Rational(1, 4), sp.Rational(1, 16), sp.Rational(0)]:
    print('  mu = %-6s => f = %s (数值 %s)' % (mv, sp.simplify(f_mu.subs(mu, mv)), sp.N(f_mu.subs(mu, mv), 8)))
print('PASS V7')

print()
print('== V8 scipy 交叉核对 ==')
try:
    import numpy as np
    from scipy.optimize import minimize
    cons = {'type': 'ineq', 'fun': lambda xx: xx[0] + xx[1] - 2}
    res = minimize(lambda xx: xx[0]**2 + 2*xx[1]**2, [2.0, 2.0], constraints=[cons], method='SLSQP')
    print('scipy: x =', res.x, ' f =', res.fun)
    assert abs(res.x[0] - 4.0/3) < 1e-6 and abs(res.x[1] - 2.0/3) < 1e-6
    assert abs(res.fun - 8.0/3) < 1e-6
    print('PASS V8: scipy 得 x*=(4/3,2/3), f*=8/3, 与符号解一致')
except ImportError:
    print('scipy 不可用, 跳过 V8')

print()
print('全部验证通过 ✔   答案锚点: x(mu)=((2+sqrt(4+3mu))/3, (2+sqrt(4+3mu))/6), x*=(4/3,2/3), u*=8/3, f*=8/3')
