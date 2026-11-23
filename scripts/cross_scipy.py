# -*- coding: utf-8 -*-
"""scipy/HiGHS 交叉核对示例（练习题-大M法 的原问题）。
LP: min -x1 -3x2 -4x3
    s.t. x1+2x2+x3 <= 7 ; -(x1+4x2+x3) <= -10 ; x1+x2+4x3 = 7 ; x >= 0
"""
from scipy.optimize import linprog
import numpy as np
res = linprog(c=[-1, -3, -4],
              A_ub=[[1, 2, 1], [-1, -4, -1]],
              b_ub=[7, -10],
              A_eq=[[1, 1, 4]],
              b_eq=[7],
              bounds=[(0, None)] * 3,
              method="highs")
print(res.status, res.message)
print("x =", res.x, " z =", res.fun)
