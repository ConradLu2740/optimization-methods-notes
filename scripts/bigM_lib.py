# -*- coding: utf-8 -*-
"""大M法公共库：符号 M 表示 (const, Mcoef)、标准形构建、检验数、单纯形迭代、表格打印。"""
from fractions import Fraction as F

def ffmt(v):
    return "%s" % F(v)

def Mfmt(v):
    c, m = v
    if m == 0:
        return "%s" % c
    if c == 0:
        return "M" if m == 1 else "-M" if m == -1 else "%sM" % m
    return "%s" % c + ("+" if m > 0 else "-") + ("M" if abs(m) == 1 else "%sM" % abs(m))

def sigma(cost, rows, basis):
    """sigma_j = c_j - sum_i c_{B_i} a_ij"""
    n = len(cost)
    out = []
    for j in range(n):
        sc, sm = cost[j]
        for i, bi in enumerate(basis):
            if rows[i][j] != 0:
                sc -= cost[bi][0] * rows[i][j]
                sm -= cost[bi][1] * rows[i][j]
        out.append((sc, sm))
    return out

def order(v):
    """(const, Mcoef) 全序：M 视为任意大正数，先比 M 系数。"""
    return (v[1], v[0])

def show(tag, cost, rows, basis):
    n = len(cost)
    print("=== %s ===" % tag)
    print("      " + "  ".join("%-11s" % ("x%d" % (j + 1)) for j in range(n)) + "  b")
    for i, r in enumerate(rows):
        print("x%-5d" % (basis[i] + 1) + "  ".join("%-11s" % ffmt(v) for v in r))
    print("sigma " + "  ".join("%-11s" % Mfmt(v) for v in sigma(cost, rows, basis)))
    print()

def build(c, A, b, slack, surplus, art):
    """slack/surplus/art 为约束行号列表；人工变量费用 = +M。"""
    nv = len(c)
    nsl, nsu, nar = len(slack), len(surplus), len(art)
    cost = [(F(c[j]), F(0)) for j in range(nv)] + [(F(0), F(0))] * (nsl + nsu) + [(F(0), F(1))] * nar
    rows, basis = [], [None] * len(A)
    for i in range(len(A)):
        row = [F(A[i][j]) for j in range(nv)] + [F(0)] * (nsl + nsu + nar)
        if i in slack:
            row[nv + slack.index(i)] = F(1)
            basis[i] = nv + slack.index(i)
        if i in surplus:
            row[nv + nsl + surplus.index(i)] = F(-1)
        if i in art:
            row[nv + nsl + nsu + art.index(i)] = F(1)
            basis[i] = nv + nsl + nsu + art.index(i)
        row.append(F(b[i]))
        rows.append(row)
    return cost, rows, basis

def pivot(cost, rows, basis, verbose=False):
    """执行一次迭代；返回 (enter, leave, ratio, pivot) 或 None(已最优)。"""
    n = len(cost)
    sg = sigma(cost, rows, basis)
    cand = [(order(sg[j]), j) for j in range(n) if j not in basis and order(sg[j]) < (0, 0)]
    if not cand:
        return None
    cand.sort()
    enter = cand[0][1]
    ratios = [(rows[i][n] / rows[i][enter], basis[i], i) for i in range(len(rows)) if rows[i][enter] > 0]
    if not ratios:
        raise RuntimeError("无界")
    lr = min(ratios, key=lambda r: (r[0], r[1]))[2]
    piv = rows[lr][enter]
    rows[lr] = [v / piv for v in rows[lr]]
    for i in range(len(rows)):
        if i != lr and rows[i][enter] != 0:
            f = rows[i][enter]
            rows[i] = [rows[i][j] - f * rows[lr][j] for j in range(n + 1)]
    old = basis[lr]
    basis[lr] = enter
    return enter, old, min(r[0] for r in ratios), piv
