# -*- coding: utf-8 -*-
"""复核"0.618 法一维搜索"练习题（精确分数：0.618 = 309/500，0.382 = 191/500）。

min phi(lambda) = (lambda - 5/2)^2 + 1，初始区间 [a1,b1] = [0,4]（单峰，解析极小 2.5）
（1）取点公式与缩区间规则
（2）前 4 轮迭代表（区间/两点及函数值/舍去方向/新区间，注意旧点复用）
（3）最终区间长度 + 近似极小点，与解析解比误差
（4）精度 delta = 0.5：0.618 法至少几轮？Fibonacci 法定 n（F0=F1=1）？
"""
from fractions import Fraction as F

R = F(309, 500)          # 0.618
R1 = F(191, 500)         # 0.382 = 1 - 0.618


def phi(x):
    return (x - F(5, 2)) ** 2 + 1


def fmt(v, nd=6):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):.{nd}f}".rstrip("0").rstrip(".") if nd else str(v)


a, b = F(0), F(4)
print("=" * 78)
print("初始区间 [a1,b1] = [0, 4]，phi(lambda) = (lambda - 2.5)^2 + 1，解析极小 lambda* = 2.5, phi* = 1")
print("=" * 78)

lam = a + R1 * (b - a)
mu = a + R * (b - a)
print(f"lambda_1 = a1 + 0.382*(b1-a1) = {fmt(lam)}")
print(f"mu_1     = a1 + 0.618*(b1-a1) = {fmt(mu)}")

rows = []
for k in range(1, 5):
    fl, fm = phi(lam), phi(mu)
    if fl <= fm:
        new_a, new_b = a, mu          # 舍右段
        new_lam, new_mu = new_a + R1 * (new_b - new_a), lam   # 新算左点；旧左点留作新右点
        direction = "phi(lambda_k) <= phi(mu_k) -> 舍右段，b_{k+1} = mu_k，旧点 lambda_k 留作新 mu_{k+1}"
    else:
        new_a, new_b = lam, b         # 舍左段
        new_lam, new_mu = mu, new_a + R * (new_b - new_a)     # 旧右点留作新左点；新算右点
        direction = "phi(lambda_k) >  phi(mu_k) -> 舍左段，a_{k+1} = lambda_k，旧点 mu_k 留作新 lambda_{k+1}"
    rows.append((k, a, b, lam, mu, fl, fm, direction, new_a, new_b, new_lam, new_mu))
    print(f"\n第 {k} 轮：区间 [{fmt(a)}, {fmt(b)}]  (长 {fmt(b - a)})")
    print(f"   lambda_{k} = {fmt(lam)}  phi = {fmt(fl)}")
    print(f"   mu_{k}     = {fmt(mu)}  phi = {fmt(fm)}")
    print(f"   {direction}")
    print(f"   新区间 [{fmt(new_a)}, {fmt(new_b)}]  (长 {fmt(new_b - new_a)})")
    a, b = new_a, new_b
    lam, mu = new_lam, new_mu

print("\n" + "=" * 78)
L = b - a
print(f"4 轮后最终区间 [{fmt(a)}, {fmt(b)}]，长度 {fmt(L)}")
print(f"近似极小点：区间中点 {fmt((a + b) / 2)}；较优保留点 lambda_4 = 2.472（phi = {fmt(phi(F(309, 125)))}）")
print(f"解析极小 lambda* = 2.5, phi* = 1；中点误差 {fmt(abs((a + b) / 2 - F(5, 2)))}，较优点误差 {fmt(abs(F(309, 125) - F(5, 2)))}")
print(f"缩率校验：4 * 0.618^4 = {fmt(4 * R ** 4)}（与上式一致）")
print(f"区间含真极小 2.5：{a <= F(5, 2) <= b}")

print("\n--- 第 (4) 问：精度 delta = 0.5 ---")
need = None
for kk in range(1, 20):
    if 4 * R ** kk <= F(1, 2):
        need = kk
        break
print(f"0.618 法：4 * 0.618^k <= 0.5 => k >= {need} 轮迭代（4 轮才 {fmt(L)} > 0.5，自洽）")
print(f"   校验：4*0.618^{need-1} = {fmt(4 * R ** (need - 1))} > 0.5，4*0.618^{need} = {fmt(4 * R ** need)} <= 0.5")

# Fibonacci：F0=F1=1，取最小 n 使 F_n >= (b1-a1)/delta
Fib = [F(1), F(1)]
while Fib[-1] < 4 / F(1, 2):
    Fib.append(Fib[-1] + Fib[-2])
print(f"Fibonacci 数列（F0=F1=1）：{[int(x) for x in Fib]}")
target = 4 / F(1, 2)
n = min(i for i, x in enumerate(Fib) if x >= target)
print(f"   需 F_n >= (b1-a1)/delta = 4/0.5 = 8 => n = {n}（F_{n} = {int(Fib[n])}），终区间 <= 4/F_{n} = {fmt(4 / Fib[n])}")
print(f"   对比：0.618 需 {need} 轮；Fibonacci n = {n}（同精度下计算次数更少）")
