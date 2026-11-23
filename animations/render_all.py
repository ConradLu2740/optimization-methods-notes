# -*- coding: utf-8 -*-
"""批量渲染脚本（HyperFrames CLI）。
依赖：Node + npx hyperframes；浏览器路径用 HYPERFRAMES_BROWSER_PATH 指定，
未设置时按平台给默认值（Windows 下为 Chrome 常规安装路径）。
subprocess 用参数列表调用，不走 shell，避免命令拼接。
"""
import os
import subprocess
import sys

env = dict(os.environ)
if not env.get("HYPERFRAMES_BROWSER_PATH"):
    if sys.platform.startswith("win"):
        env["HYPERFRAMES_BROWSER_PATH"] = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif sys.platform == "darwin":
        env["HYPERFRAMES_BROWSER_PATH"] = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:
        env["HYPERFRAMES_BROWSER_PATH"] = "/usr/bin/google-chrome"

jobs = [
  ("compositions/simplex.html",  "renders/01-单纯形法.mp4"),
  ("compositions/twophase.html","renders/02-两阶段法.mp4"),
  ("compositions/bigm.html",    "renders/03-大M法.mp4"),
  ("compositions/kkt.html",     "renders/04-KKT与二阶.mp4"),
  ("compositions/farkas.html",  "renders/05-Farkas画图.mp4"),
  ("compositions/fr.html",      "renders/06-FR共轭梯度.mp4"),
  ("compositions/dfp.html",     "renders/07-DFP拟牛顿.mp4"),
  ("compositions/sdnt.html",    "renders/08-最速下降vs牛顿.mp4"),
  ("compositions/line.html",    "renders/09-一维搜索.mp4"),
  ("compositions/zout.html",    "renders/10-Zoutendijk.mp4"),
  ("compositions/rosen.html",   "renders/11-Rosen投影.mp4"),
  ("compositions/penout.html",  "renders/12-外点罚函数.mp4"),
  ("compositions/penin.html",   "renders/13-内点罚函数.mp4"),
  ("compositions/convex.html",  "renders/14-凸集与凸函数.mp4"),
  ("compositions/modern.html",  "renders/15-现代vs传统.mp4"),
]
for comp, out in jobs:
    print("=== rendering", comp, "->", out, flush=True)
    r = subprocess.run(["npx", "hyperframes", "render", "-c", comp, "--output", out],
                       env=env, capture_output=True, text=True, shell=False, timeout=1200)
    tail = (r.stdout or "").strip().split("\n")[-2:]
    print("   rc=%d" % r.returncode, " || ".join(tail)[:300], flush=True)
print("ALL DONE", flush=True)
