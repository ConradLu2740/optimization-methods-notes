# -*- coding: utf-8 -*-
"""外点罚函数法练题验证（2026-11-18）：
min x1^2 + 2*x2^2  s.t.  x1 + x2 = 3
F(x,sigma) = f + sigma*(x1+x2-3)^2
"""
import sympy as sp

x1, x2, sig = sp.symbols("x1 x2 sigma", positive=True)
F = x1 ** 2 + 2 * x2 ** 2 + sig * (x1 + x2 - 3) ** 2

print("F(x,sigma) =", F)
sol = sp.solve([sp.diff(F, x1), sp.diff(F, x2)], [x1, x2], dict=True)
print("驻点解:", sol)
assert len(sol) == 1
x1s, x2s = sol[0][x1], sol[0][x2]
print(f"x1(sigma) = {sp.simplify(x1s)},  x2(sigma) = {sp.simplify(x2s)}")
print(f"sigma->oo: x1->{sp.limit(x1s, sig, sp.oo)}, x2->{sp.limit(x2s, sig, sp.oo)}")
print(f"f* = {sp.Rational(2)**2 + 2*sp.Rational(1)**2}")

# 每步无约束问题的全局性：F 的 Hessian 正定
H = sp.hessian(F, (x1, x2))
print("Hessian:", H.tolist(), "主子式:", H[0, 0], H.det())
assert H[0, 0] > 0 and H.det() > 0  # 对 sigma>0 恒成立

# 原问题最优性：拉格朗日 L = f - v*(x1+x2-3)
v = sp.symbols("v")
kkt = sp.solve([2 * x1 - v, 4 * x2 - v, x1 + x2 - 3], [x1, x2, v])
print("原问题 KKT 解:", kkt)  # 期望 x1=2, x2=1, v=4

# 数值抽查（沿罚函数轨线）
for sv in [1, 10, 100, 1000]:
    x1v = float(x1s.subs(sig, sv))
    x2v = float(x2s.subs(sig, sv))
    fv = x1v ** 2 + 2 * x2v ** 2
    Fv = fv + sv * (x1v + x2v - 3) ** 2
    print(f"sigma={sv:5}: x=({x1v:.4f}, {x2v:.4f}), f={fv:.4f}, F={Fv:.4f}")
print("全部验证通过")
