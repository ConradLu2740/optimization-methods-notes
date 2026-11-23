# opt-animations — 《最优化方法与应用》知识点动画系列

用 HyperFrames（HTML + GSAP 时间线 → 渲染 MP4）把课程考点做成 48-71 秒的讲解动画。
视觉规范见 [DESIGN.md](DESIGN.md)（深色数字黑板 + 荧光笔），全系列共用一套。

## 已成片 15 个（renders/ 目录）

| # | 知识点 | 成片 | 时长 | 核心内容 |
|---|---|---|---|---|
| 01 | 单纯形法 | [01-单纯形法.mp4](renders/01-单纯形法.mp4) | 64s | 几何直觉 + 两迭代表格 + 最优判别 |
| 02 | 两阶段法 ★点名 | [02-两阶段法.mp4](renders/02-两阶段法.mp4) | 71s | 缺单位列⇒加人工；w*=0 判据卡；删列换目标 |
| 03 | 大M法 | [03-大M法.mp4](renders/03-大M法.mp4) | 63s | 符号 M 检验数；先比 M 系数；三迭代 |
| 04 | KKT+二阶 | [04-KKT与二阶.mp4](renders/04-KKT与二阶.mp4) | 56s | 两 KKT 点；临界锥毙掉点②；五步 SOP |
| 05 | Farkas 画图 ★必考 | [05-Farkas画图.mp4](renders/05-Farkas画图.mp4) | 50s | 三种形式；锥内/锥外二图；30 秒画法 |
| 06 | FR 共轭梯度 ★点名 | [06-FR共轭梯度.mp4](renders/06-FR共轭梯度.mp4) | 58s | λ₁=5/18、β₁=4/81、λ₂=9/20 两步终止 |
| 07 | DFP 拟牛顿 ★点名 | [07-DFP拟牛顿.mp4](renders/07-DFP拟牛顿.mp4) | 58s | p/q、H₂ 矩阵、割线验证、两步到 (1,0) |
| 08 | 最速下降 vs 牛顿 | [08-最速下降vs牛顿.mp4](renders/08-最速下降vs牛顿.mp4) | 56s | 锯齿 vs 一步到位；阻尼/修正两帖药 |
| 09 | 一维搜索 0.618/Fibonacci | [09-一维搜索.mp4](renders/09-一维搜索.mp4) | 58s | 迭代表（旧点复用）；下标易错点 |
| 10 | Zoutendijk | [10-Zoutendijk.mp4](renders/10-Zoutendijk.mp4) | 50s | 活动集⇒A₁；方向 LP 得 d=(1,1) |
| 11 | Rosen 投影 | [11-Rosen投影.mp4](renders/11-Rosen投影.mp4) | 48s | M=(0,1)、P_N=diag(1,0)、d=(−4,0) |
| 12 | 外点罚函数 | [12-外点罚函数.mp4](renders/12-外点罚函数.mp4) | 52s | 两例闭式解；μ↑；判据 μP<ε |
| 13 | 内点罚函数 | [13-内点罚函数.mp4](renders/13-内点罚函数.mp4) | 52s | 负对数障碍；x(μ) 闭式；u*=8/3 |
| 14 | 凸集与凸函数 | [14-凸集与凸函数.mp4](renders/14-凸集与凸函数.mp4) | 52s | 定义验证两步放缩；Hessian；上镜图 |
| 15 | 现代 vs 传统 | [15-现代vs传统.mp4](renders/15-现代vs传统.mp4) | 50s | 差别 5 + 联系 4；光谱图；NP-hard 原理 |

所有计算题数字都先用分数脚本复算再写进动画；每个片子渲染前过
`lint` + `check`（布局/对比度/动效 0 error）。

## ⚠️ 全系列统一口径（2026-11-22 定）

**σ = cⱼ − c_BᵀB⁻¹Aⱼ；入基取最负 σ；最优判别 σ 全部 ≥ 0。**
依据：第一册 §3.2 课件例题表、复习课答题材料题4 易错点、考前速览公式卡，三处一致。

## 怎么加一个新动画

1. `python gencss.py <前缀> <场景数> "<系列名>" "<徽章文字>" > /tmp/css.txt`
   —— 输出标准视觉规范（改 ID 前缀避免跨 composition 冲突）。
2. 在 `compositions/` 新建 `<name>.html`：`<template>` 包整篇，根 div 带
   `data-composition-id`，末尾注册 `window.__timelines["<name>"]`。
3. `python mount.py <name> <秒数>` —— 自动挂到 index.html 并续接时间轴。
4. `python build_fonts.py` —— 按当前所有动画的用字重新生成中文字体子集。
5. 检查与渲染：
   ```powershell
   $env:HYPERFRAMES_BROWSER_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
   npx hyperframes lint
   npx hyperframes check .
   npx hyperframes render -c compositions/<name>.html --output "renders/<编号>-<名称>.mp4"
   ```

## 踩过的坑（改代码前必读）

- **同一元素上不要叠两条 `from` 补间**：后一条会把前一条 immediateRender
  刚设成的值当成自己的"结束值"，元素永远停在初始态。宽选择器
  （`#sX .mathbox`）和窄选择器（`#sX .rightX .mathbox`）同时用就会触发——
  **宽的那条必须写到 `.leftX` 一级**。
- **`from` 补间在它的起始时刻之前一直保持起始态**：所以别用
  `tl.from("#sX .rightX div", ...)` 这种会圈进面板自身的选择器；要单点一个 class。
- 同一元素多条 `fromTo` 时，除最早那条外都要加 `immediateRender: false`。
- 子 composition 里字体路径写 `../assets/fonts/xxx.woff2`。
- 下标/上标用 `<sub>/<sup>` 标签，别用 Unicode 字符（中文字体没有）；
  JS 里动态设文本用 `innerHTML`。
- 场景 2 以上默认 `opacity: 0`，转场 `fromTo` 的目标态必须显式写 `opacity: 1`。
- 底部固定栏用 `top` 定位，别用 `bottom`。
- 每个数字先用分数脚本算一遍再写进 HTML。
