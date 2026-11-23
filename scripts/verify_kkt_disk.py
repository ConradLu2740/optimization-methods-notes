import sympy as sp

x1, x2, u = sp.symbols('x1 x2 u', real=True)
f = (x1 + 1)**2 + x2**2
g = x1**2 + x2**2 - 1          # feasible: g >= 0

gf = sp.Matrix([sp.diff(f, x1), sp.diff(f, x2)])
gg = sp.Matrix([sp.diff(g, x1), sp.diff(g, x2)])
print("grad f =", gf.T, " grad g =", gg.T)

# KKT: grad f = u*grad g, u>=0, g>=0
sol = sp.solve([sp.Eq(gf[0], u*gg[0]), sp.Eq(gf[1], u*gg[1]), sp.Eq(g, 0)],
               [x1, x2, u], dict=True)
print("active-boundary KKT candidates:", sol)

for s in sol:
    xs = (sp.nsimplify(s[x1]), sp.nsimplify(s[x2]))
    us = sp.nsimplify(s[u])
    print("candidate x* =", xs, " u =", us,
          " u>=0:", sp.simplify(us) >= 0)

# u = 0 branch (grad f = 0)
sol0 = sp.solve([sp.Eq(gf[0], 0), sp.Eq(gf[1], 0)], [x1, x2], dict=True)
print("u=0 branch:", sol0, " g there:", [sp.simplify(g.subs(s)) for s in sol0])

# second-order: H = f_xx - u*g_xx on critical cone
for xs, us in [((-1, 0), 0), ((1, 0), 2)]:
    Hf = sp.hessian(f, (x1, x2)); Hg = sp.hessian(g, (x1, x2))
    H = sp.simplify(Hf - us*Hg)
    d = sp.Matrix(sp.symbols('d1 d2', real=True))
    gd = gg.subs({x1: xs[0], x2: xs[1]}).T*d
    print(f"\nx*={xs}, u={us}, H={H.tolist()}, cone eq={sp.simplify(gd[0])}=0")
    # restrict: cone d1=0 -> d=(0,1)
    print("  d^T H d on cone (d=(0,1)):", sp.simplify((d.T*H*d)[0].subs({d[0]:0, d[1]:1})))
    print("  boundary f(theta)=2+2cos(theta) near this point?")
    th = sp.symbols('theta', real=True)
    fb = 2 + 2*sp.cos(th)
    print("  f on circle range:", (sp.simplify(fb.subs(th, 0)), sp.simplify(fb.subs(th, sp.pi))))
