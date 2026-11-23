# -*- coding: utf-8 -*-
"""按当前所有 composition 的实际用字，下载 Noto Serif SC 子集并注入 @font-face。
每新增一个动画后跑一次：python build_fonts.py

安全约定：只允许访问 https 且主机在 ALLOWED_HOSTS 白名单内的 URL，
请求前先校验 scheme/host，避免把任意字符串当 URL 发起服务端请求。
"""
import io, os, re, socket, urllib.parse, urllib.request

ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
EXTRA = "σ θ λ μ β ω Ω ∇ ≥ ≤ ≠ ≈ ± × ÷ ∈ ∉ ⊂ ∪ ∩ ∀ ∃ ⇒ → ← ↕ ↑ ↓ √ ∞ ∑ ∏ ∫ ∮ ≡ ①②③④⑤⑥⑦⑧⑨⑩ ★ ☆ ✓ ✗ ◆ ● ○ ■ □ ▲ △ ◇ † ‡ § ¶ – — ’ “ ” … ‰ ′ ″ ½ ⅓ ⅔ ¼ ¾ º ª ⁿ ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉ ⁺ ⁻ ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ α γ δ ε ζ η ι κ ν ξ ρ τ υ φ χ ψ"
FONT_DIR = "assets/fonts"
WEIGHTS = [("400", "notoserifsc-400.woff2"), ("700", "notoserifsc-700.woff2")]


def fetch(url):
    """校验 scheme/host 后才发请求；重定向不跟随（urllib 默认不跟随 https->https 之外的跳转）。"""
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https":
        raise ValueError("只允许 https: %s" % url)
    if p.hostname not in ALLOWED_HOSTS:
        raise ValueError("主机不在白名单: %s" % p.hostname)
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60
    ).read()


def collect_chars():
    chars = set(EXTRA.replace(" ", ""))
    files = ["index.html"] + ["compositions/" + f for f in sorted(os.listdir("compositions")) if f.endswith(".html")]
    for f in files:
        txt = io.open(f, encoding="utf-8").read()
        txt = re.sub(r"<[^>]+>", "", txt)          # strip tags, keep text
        txt = re.sub(r"&[a-z]+;", "", txt)          # strip entities
        chars |= {ch for ch in txt if ord(ch) > 127}
    return "".join(sorted(chars))


def download(text):
    os.makedirs(FONT_DIR, exist_ok=True)
    for weight, fname in WEIGHTS:
        url = "https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght=%s&text=%s" % (
            weight, urllib.parse.quote(text))
        css = fetch(url).decode()
        src = re.search(r"url\(([^)]+)\)", css).group(1)
        data = fetch(src)
        assert data[:4] == b"wOF2", "not woff2"
        io.open(os.path.join(FONT_DIR, fname), "wb").write(data)
        print("  %s: %d bytes" % (fname, len(data)))


def faces_css():
    rules = []
    for weight, fname in WEIGHTS:
        rules.append('@font-face { font-family: "Noto Serif SC"; font-style: normal; font-weight: %s; '
                     'src: url("../%s/%s") format("woff2"); font-display: block; }' % (weight, FONT_DIR, fname))
    return "/*FONT-FACES-BEGIN*/\n      " + "\n      ".join(rules) + "\n      /*FONT-FACES-END*/"


def inject():
    files = ["compositions/" + f for f in sorted(os.listdir("compositions")) if f.endswith(".html")]
    block = faces_css()
    for f in files:
        s = io.open(f, encoding="utf-8").read()
        s = re.sub(r"/\*FONT-FACES-BEGIN\*/.*?/\*FONT-FACES-END\*/\n?", "", s, flags=re.S)
        s = s.replace("<style>", "<style>\n      " + block, 1)
        s = s.replace('"ZCOOL XiaoWei", "Microsoft YaHei", sans-serif', '"Noto Serif SC", serif')
        s = s.replace('"ZCOOL XiaoWei", serif', '"Noto Serif SC", serif')
        io.open(f, "w", encoding="utf-8").write(s)
        print("  injected ->", f)


if __name__ == "__main__":
    text = collect_chars()
    print("subset chars:", len(text))
    download(text)
    inject()
    print("done")
