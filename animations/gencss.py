import sys
TPL = """    <style>
      [data-composition-id="@P@"] { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; overflow: hidden; font-family: "Noto Serif SC", serif; color: #e9eef8; }
      [data-composition-id="@P@"] .mono { font-family: "IBM Plex Mono", Consolas, monospace; font-variant-numeric: tabular-nums; }
      #bg@P@ { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; background-color: #0e1526; z-index: 0; }
      #bg@P@ .grid { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px;
        background-image: linear-gradient(rgba(143,163,200,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(143,163,200,0.055) 1px, transparent 1px);
        background-size: 80px 80px; }
      #glow@P@ { position: absolute; left: 320px; top: -280px; width: 1280px; height: 1280px; border-radius: 50%;
        background: radial-gradient(circle, rgba(255,197,61,0.10) 0%, rgba(255,197,61,0.035) 38%, rgba(255,197,61,0) 70%); }
      #glow@P@b { position: absolute; left: -340px; bottom: -440px; width: 1080px; height: 1080px; border-radius: 50%;
        background: radial-gradient(circle, rgba(90,169,255,0.09) 0%, rgba(90,169,255,0.03) 40%, rgba(90,169,255,0) 70%); }
      #chrome-top@P@ { position: absolute; top: 36px; left: 64px; right: 64px; display: flex; justify-content: space-between; align-items: center; z-index: 20; }
      #series-label@P@ { font-size: 21px; color: #8fa3c8; letter-spacing: 0.06em; }
      #topic-badge@P@ { font-size: 22px; color: #ffc53d; border: 1.5px solid rgba(255,197,61,0.55); border-radius: 999px; padding: 8px 22px; letter-spacing: 0.04em; }
      #chrome-bottom@P@ { position: absolute; left: 64px; right: 64px; top: 972px; z-index: 20; }
      #cap-row@P@ { display: flex; justify-content: space-between; align-items: baseline; gap: 40px; }
      #step-label@P@ { font-size: 21px; color: #8fa3c8; white-space: nowrap; }
      #caption@P@ { font-size: 27px; color: #e9eef8; flex: 1; text-align: center; }
      #topic-foot@P@ { font-size: 21px; color: #8fa3c8; white-space: nowrap; }
      #prog-track@P@ { margin-top: 14px; height: 3px; width: 100%; background: rgba(143,163,200,0.18); border-radius: 2px; overflow: hidden; }
      #prog@P@ { height: 100%; width: 100%; background: #ffc53d; transform-origin: left center; transform: scaleX(0); }
      .scene@P@ { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; overflow: hidden; z-index: 1; }
"""
for i in range(2, int(sys.argv[2]) + 1):
    TPL += "      #s%d@P@ { z-index: %d; opacity: 0; }\n" % (i, i)
TPL += """      #s1@P@ .wrap { position: absolute; left: 150px; top: 250px; width: 1620px; }
      #s1@P@ .kicker { font-size: 26px; color: #ffc53d; letter-spacing: 0.22em; margin-bottom: 26px; }
      #s1@P@ h1 { font-size: 140px; font-weight: 400; line-height: 1.06; letter-spacing: 0.01em; margin: 0 0 30px 0; }
      #s1@P@ h1 .hl { color: #ffc53d; }
      #s1@P@ .sub { font-size: 33px; color: #8fa3c8; margin-bottom: 44px; }
      #s1@P@ .badges { display: flex; gap: 18px; margin-bottom: 52px; }
      #s1@P@ .badge { font-size: 24px; color: #e9eef8; border: 1.5px solid rgba(143,163,200,0.45); border-radius: 999px; padding: 10px 26px; }
      #s1@P@ .badge.hot { color: #0e1526; background: #ffc53d; border-color: #ffc53d; font-weight: 500; }
      #s1@P@ .formula { font-size: 29px; color: #3ecf8e; letter-spacing: 0.02em; border-left: 4px solid #3ecf8e; padding-left: 22px; }
      .panel@P@ { background: #17233f; border: 1px solid rgba(143,163,200,0.22); border-radius: 14px; padding: 26px 30px; }
      .panel-title@P@ { font-size: 24px; color: #8fa3c8; margin-bottom: 18px; letter-spacing: 0.03em; }
      .grid@P@ { position: absolute; left: 64px; top: 112px; width: 1800px; display: flex; gap: 44px; align-items: flex-start; }
      .left@P@ { width: 1090px; }
      .right@P@ { width: 666px; }
      .mathbox@P@ { font-family: "IBM Plex Mono", Consolas, monospace; font-variant-numeric: tabular-nums; font-size: 27px; line-height: 1.9; color: #e9eef8; background: rgba(90,169,255,0.07); border: 1px solid rgba(90,169,255,0.25); border-radius: 10px; padding: 18px 22px; margin: 14px 0; }
      .mathbox@P@ .lbl { color: #8fa3c8; }
      .mathbox@P@ .hi { color: #ffc53d; }
      .step@P@ { display: flex; gap: 18px; align-items: flex-start; margin-bottom: 18px; }
      .step@P@ .sn { font-family: "IBM Plex Mono", Consolas, monospace; font-size: 25px; color: #0e1526; background: #5aa9ff; border-radius: 8px; min-width: 46px; height: 46px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
      .step@P@ .st { font-size: 26px; line-height: 1.5; padding-top: 5px; }
      .step@P@ .st b { color: #ffc53d; font-weight: 400; }
      .step@P@ .st .mono { color: #3ecf8e; }
      .verdict@P@ { margin-top: 18px; border-radius: 12px; padding: 20px 24px; font-size: 27px; line-height: 1.5; }
      .verdict@P@.ok { background: rgba(62,207,142,0.10); border: 1.5px solid rgba(62,207,142,0.5); color: #3ecf8e; }
      .verdict@P@.warn { background: rgba(255,197,61,0.10); border: 1.5px solid rgba(255,197,61,0.5); color: #ffc53d; }
      .formcard@P@ { background: #17233f; border: 1px solid rgba(143,163,200,0.22); border-radius: 14px; padding: 22px 26px; margin-bottom: 20px; }
      .formcard@P@ .fh { font-size: 28px; color: #ffc53d; margin-bottom: 10px; }
      .formcard@P@ .fl { font-size: 25px; line-height: 1.6; color: #e9eef8; }
      .formcard@P@ .fl .mono { color: #3ecf8e; }
      .ans-big@P@ { font-family: "IBM Plex Mono", Consolas, monospace; font-variant-numeric: tabular-nums; font-size: 50px; color: #ffc53d; margin-bottom: 6px; }
      .ans-big@P@ .lbl { font-size: 28px; color: #8fa3c8; }
      .ans-card@P@ { background: #17233f; border: 1.5px solid rgba(255,197,61,0.45); border-radius: 16px; padding: 28px 32px; }
      .ans-warn@P@ { margin-top: 20px; font-size: 23px; color: #ff9b9b; border-top: 1px solid rgba(143,163,200,0.25); padding-top: 16px; line-height: 1.6; }
    </style>
    <div id="bg@P@"><div class="grid"></div><div id="glow@P@"></div><div id="glow@P@b"></div></div>
    <div id="chrome-top@P@">
      <div id="series-label@P@" class="mono">@SERIES@</div>
      <div id="topic-badge@P@">@BADGE@</div>
    </div>
"""
out = TPL.replace("@P@", sys.argv[1]).replace("@SERIES@", sys.argv[3]).replace("@BADGE@", sys.argv[4])
print(out, end="")
