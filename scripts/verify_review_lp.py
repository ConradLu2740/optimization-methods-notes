# -*- coding: utf-8 -*-
"""复习课 LP 三题精确复验：题4 单纯形 / 题5 大M / 题6 两阶段
数值以 (const, mcoef) 表示 a + b*M。单纯形表按最小化口径：
检验数行 rho_j = c_j - z_j（x_j 增加 1 时 z 的增长率），入基取最负者。
"""
from fractions import Fraction as F

def L(a=F(0), b=F(0)): return (F(a), F(b))
def add(u, v): return (u[0]+v[0], u[1]+v[1])
def sub(u, v): return (u[0]-v[0], u[1]-v[1])
def mul(u, s): return (u[0]*s, u[1]*s)
def fmt(u):
    a, b = u
    if b == 0: return str(a)
    if a == 0: return 'M' if b == 1 else f'{b}M'
    return f'{a}+{b}M' if b > 0 else f'{a}{b}M'

def neg_test(rho):
    """rho<0 判定（M 为大正数）：M 系数<0 判负；M 系数=0 才看常数项。"""
    return rho[1] < 0 or (rho[1] == 0 and rho[0] < 0)

def show(T, basis, zc, names, tag):
    print(f'--- {tag} 表：基 = {[names[k] for k in basis]} ---')
    print('       ', ' '.join(f'{h:>6}' for h in names), '   rhs')
    for i in range(len(T)):
        print(f'{names[basis[i]]:>6}', ' '.join(f'{fmt(v):>6}' for v in T[i]))
    print('cj-zj ', ' '.join(f'{fmt(v):>6}' for v in zc))
    print()

def simplex_core(T, basis, c_ext, names, tag='', forbid=(), log=True, tie='low_index', art_cols=()):
    """T: m x (N+1) 线性对矩阵；basis: 长度 m；c_ext: 长度 N 的费用。
    tie: 比值测试并列时的偏好，'low_index'=基本变量下标小者出基（Bland），
         'art_first'=优先让人工变量出基。"""
    m = len(T); N = len(T[0]) - 1
    it = 0
    while True:
        z = [L() for _ in range(N+1)]
        for i in range(m):
            cb = c_ext[basis[i]]
            for j in range(N+1):
                z[j] = add(z[j], (cb[0]*T[i][j][0], cb[1]*T[i][j][0]))
        zc = [sub(c_ext[j], z[j]) for j in range(N)] + [z[N]]
        if log: show(T, basis, zc, names, f'{tag}{it}')
        cand = [j for j in range(N) if j not in forbid and neg_test(zc[j])]
        if not cand:
            print(f'{tag} 最优，检验数全非负，z* = {fmt(zc[N])}')
            break
        enter = min(cand, key=lambda j: (zc[j][1], zc[j][0]))
        pos = [i for i in range(m) if T[i][enter][0] > 0]
        if not pos: raise RuntimeError('unbounded')
        ratios = [(T[i][N][0]/T[i][enter][0], basis[i], i) for i in pos]
        rmin = min(r[0] for r in ratios)
        tied = [r for r in ratios if r[0] == rmin]
        if tie == 'art_first':
            r = min(tied, key=lambda r: (0 if r[1] in art_cols else 1, r[1], r[2]))[2]
        else:
            r = min(tied, key=lambda r: (r[1], r[2]))[2]
        pv = T[r][enter][0]
        T[r] = [mul(v, F(1)/pv) for v in T[r]]
        for i in range(m):
            if i != r and T[i][enter][0] != 0:
                f = T[i][enter][0]
                T[i] = [sub(T[i][j], mul(T[r][j], f)) for j in range(N+1)]
        basis[r] = enter
        it += 1
        if it > 40: raise RuntimeError('cycle')
    x = [F(0)]*(N)
    for i in range(m): x[basis[i]] = T[i][N][0]
    return x, zc[N]

def auto_basis(A, m, N):
    basis = [None]*m
    for j in range(N):
        col = [A[i][j] for i in range(m)]
        if col.count(F(1)) == 1 and col.count(F(0)) == m-1:
            i = col.index(F(1))
            if basis[i] is None: basis[i] = j
    return basis

def bigm_solve(A, b, c, names, art_cols=(), log=True):
    """art_cols: A 中已是恒等列、但按人工变量计费（费用 M）的列下标。"""
    m = len(A); N = len(A[0])
    basis = auto_basis(A, m, N)
    art_rows = [i for i in range(m) if basis[i] is None]
    A2 = [row[:] + [F(1) if i in art_rows else F(0) for i in range(m)] for row in A]
    for k, i in enumerate(art_rows): basis[i] = N + k
    N2 = N + len(art_rows)
    c_ext = [L(c[j]) for j in range(N2)]
    for j in list(art_cols) + list(range(N, N2)):
        c_ext[j] = L(0, 1)                              # 人工变量费用 M
    T = [[L(A2[i][j]) for j in range(N2)] + [L(b[i])] for i in range(m)]
    x, z = simplex_core(T, basis, c_ext, names, tag='大M ', log=log)
    return x[:N], z

def two_phase(A, b, c, names, art_cols=(), log=True, tie='low_index'):
    """第一阶段：人工变量费用 1，最小化 w；第二阶段：原费用，禁人工列。
    art_cols: A 中已是恒等列、按人工变量处理的列下标。"""
    m = len(A); N = len(A[0])
    basis = auto_basis(A, m, N)
    art_rows = [i for i in range(m) if basis[i] is None]
    A2 = [row[:] + [F(1) if i in art_rows else F(0) for i in range(m)] for row in A]
    for k, i in enumerate(art_rows): basis[i] = N + k
    N2 = N + len(art_rows)
    art = list(art_cols) + list(range(N, N2))
    T = [[L(A2[i][j]) for j in range(N2)] + [L(b[i])] for i in range(m)]
    # ---- 阶段一 ----
    c1 = [L(0) for _ in range(N2)]
    for j in art: c1[j] = L(1)
    x1, w = simplex_core(T, basis, c1, names, tag='P1 ', log=log, tie=tie, art_cols=art)
    if w[0] != 0: raise RuntimeError('phase1 infeasible, w=%s' % fmt(w))
    # 人工变量仍留在基里 -> 逐行旋出
    for i in range(m):
        if basis[i] in art:
            piv = [j for j in range(N) if T[i][j][0] != 0]
            if piv:
                j = piv[0]
                pv = T[i][j][0]
                T[i] = [mul(v, F(1)/pv) for v in T[i]]
                for k in range(m):
                    if k != i and T[k][j][0] != 0:
                        f = T[k][j][0]
                        T[k] = [sub(T[k][q], mul(T[i][q], f)) for q in range(N2+1)]
                basis[i] = j
    # ---- 阶段二 ----
    c2 = [L(c[j]) for j in range(N2)]
    for j in art: c2[j] = L(0)
    x, z = simplex_core(T, basis, c2, names, tag='P2 ', log=log, forbid=art)
    return x[:N], z

def vertex_enum(rows, nv, c, tol=F(0)):
    """rows: [(coeffs, rhs, 'le'/'eq')]；nv 个变量；枚举全部顶点，返回可行顶点 z 列表（精确分数）。"""
    import itertools
    rows = [([F(v) for v in co], F(rh), op) for co, rh, op in rows]
    c = [F(v) for v in c]
    pts = []
    for comb in itertools.combinations(range(len(rows)), nv):
        Am = [rows[i][0] for i in comb]; bm = [rows[i][1] for i in comb]
        # 高斯消元解 nv x nv
        M = [list(row) + [b] for row, b in zip(Am, bm)]
        singular = False
        for col in range(nv):
            p = None
            for r in range(col, nv):
                if M[r][col] != 0: p = r; break
            if p is None: singular = True; break
            M[col], M[p] = M[p], M[col]
            pv = M[col][col]
            M[col] = [v/pv for v in M[col]]
            for r in range(nv):
                if r != col and M[r][col] != 0:
                    f = M[r][col]
                    M[r] = [M[r][q] - f*M[col][q] for q in range(nv+1)]
        if singular: continue
        x = [M[i][nv] for i in range(nv)]
        if any(v < 0 for v in x): continue
        ok = True
        for co, rh, op in rows:
            s = sum(co[j]*x[j] for j in range(nv))
            if op == 'le' and s > rh + tol: ok = False; break
            if op == 'ge' and s < rh - tol: ok = False; break
            if op == 'eq' and s != rh: ok = False; break
        if ok: pts.append(tuple(x))
    out = []
    for p in set(pts):
        out.append((p, sum(c[j]*p[j] for j in range(nv))))
    return out

def main():
    print('======== 题4 单纯形法 ========')
    A4 = [[F(1),F(1),F(1),F(0),F(1),F(0),F(0)],
        [F(4),F(-1),F(1),F(2),F(0),F(1),F(0)],
        [F(-1),F(1),F(2),F(3),F(0),F(0),F(1)]]
    c4 = [F(3),F(-5),F(-2),F(-1),F(0),F(0),F(0)]
    n4 = ['x1','x2','x3','x4','s1','s2','s3']
    x4, z4 = bigm_solve(A4, [F(4),F(6),F(12)], c4, n4, log=True)
    print('题4 最优 x =', x4[:4], ' z* =', z4)
    rows4 = [((1,1,1,0), 4, 'le'), ((4,-1,1,2), 6, 'le'), ((-1,1,2,3), 12, 'le')]
    for j in range(4):
        e = [0]*4; e[j] = 1
        rows4.append((tuple(e), 0, 'ge'))
    v4 = vertex_enum(rows4, 4, c4)
    for p, z in sorted(v4, key=lambda t: t[1]):
        print('  顶点', p, 'z =', z)

    # ================= 题5：大M =================
    print('======== 题5 大M法 ========')
    A5 = [[F(1),F(-2),F(1),F(0),F(1),F(0),F(0)],
        [F(-4),F(1),F(2),F(-1),F(0),F(1),F(0)],
        [F(-2),F(0),F(1),F(0),F(0),F(0),F(1)]]
    c5 = [F(-3),F(1),F(1),F(0),F(0),F(0),F(0)]
    n5 = ['x1','x2','x3','x4','s1','a1','a2']
    x5, z5 = bigm_solve(A5, [F(11),F(3),F(1)], c5, n5, art_cols=(5,6), log=True)
    print('题5 最优 x =', x5[:4], ' z* =', z5)
    # 题5 消元复核：-2x1+x3=1 -> x3=1+2x1；-4x1+x2+2x3-x4=3 -> x4=x2-1；
    # x1-2x2+x3<=11 -> 3x1-2x2<=10；min -3x1+x2+x3 = min -x1+x2+1
    print('题5 消元复核: x*=(4,1,9,0), z*=-2')

    # ================= 题6：两阶段 =================
    print('======== 题6 两阶段法 ========')
    # 列: x1,x2,x3, s1(行1), a1(行2), a2(行3)
    A6 = [[F(-1),F(2),F(1),F(1),F(0),F(0)],
        [F(-4),F(4),F(-1),F(0),F(1),F(0)],
        [F(1),F(0),F(-1),F(0),F(0),F(1)]]
    c6 = [F(1),F(-1),F(0),F(0),F(0),F(0)]
    n6 = ['x1','x2','x3','x4','a1','a2']
    x6, z6 = two_phase(A6, [F(2),F(4),F(0)], c6, n6, art_cols=(4,5), log=True, tie='art_first')
    print('题6 最优 x =', x6[:3], ' z* =', z6)
    # 题6 消元复核：x1-x3=0 -> x3=x1；-4x1+4x2-x3=4 -> x2=(3x1+4)/4；
    # -x1+2x2+x3<=2 -> x1+2x2<=2 -> 9x1/2+2<=2 -> x1<=0 => x1=0
    print('题6 消元复核: x1=0, x2=1, x3=0, z = -1')


if __name__ == '__main__':
    main()
