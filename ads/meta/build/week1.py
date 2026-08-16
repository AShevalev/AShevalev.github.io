"""Week 1 — Launch & free trial."""

from style import (BODY, DISCLAIMER, DISCLAIMER_SHORT, GOLD, HEADING,
                   LOGO_MARK, page)
from render import render

SQ, PORTRAIT, STORY = (1080, 1080), (1080, 1350), (1080, 1920)


def manifesto_open():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:40px">
  <div class="eyebrow">Launch day</div>
  <div class="metal" style="font-size:250px">We are<br>live</div>
  <div class="rule" style="width:280px"></div>
  <div class="sub" style="font-size:40px;letter-spacing:.06em;text-transform:uppercase;
              font-weight:600;color:#f5f5f5">Verodus is officially launched</div>
</div>"""
    return render("w1-manifesto-open", page(*STORY, inner, legal=DISCLAIMER_SHORT,
                                            logo_h=42, seed=3), *STORY)


def manifesto_end():
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:56px">
  <img src="{LOGO_MARK}" style="height:300px">
  <div class="h1 gold" style="font-size:76px;line-height:1.06">Clear rules.<br>
      Founder-run.<br>No hype.</div>
  <div class="pill" style="font-size:34px;padding:32px 56px;margin-top:14px">
      Try it free — verodus.com</div>
</div>"""
    return render("w1-manifesto-end", page(*STORY, inner, legal=DISCLAIMER,
                                           logo_h=34, seed=11), *STORY)


def tryfree_1():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:44px">
  <div class="eyebrow">Free trial</div>
  <div class="metal" style="font-size:158px">Trade the<br>platform<br>free</div>
  <div class="rule" style="width:340px"></div>
  <div class="sub" style="font-size:52px;font-weight:300;color:#f5f5f5">
      No card. No risk.</div>
</div>"""
    return render("w1-tryfree-1", page(*PORTRAIT, inner, seed=5), *PORTRAIT)


def tryfree_2():
    steps = [
        ("1", "Free trial", "Same rules. Same platforms. $0."),
        ("2", "Read the rules", "Every objective published upfront."),
        ("3", "Then decide", "Instant $5k $72 · 1-Step $5k $36."),
    ]
    rows = "".join(f"""
  <div class="card" style="display:flex;align-items:center;gap:38px;padding:44px 46px">
    <div class="metal" style="font-size:88px;min-width:74px">{n}</div>
    <div>
      <div style="font-size:46px;font-weight:800;letter-spacing:-.02em;
                  text-transform:uppercase;color:{HEADING}">{title}</div>
      <div class="sub" style="font-size:29px;margin-top:10px">{note}</div>
    </div>
  </div>""" for n, title, note in steps)
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px">
  <div class="eyebrow" style="margin-bottom:8px">How it works</div>
  {rows}
</div>"""
    return render("w1-tryfree-2", page(*PORTRAIT, inner, seed=9), *PORTRAIT)


def tryfree_3():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:46px">
  <div class="h1" style="font-size:96px">New firm.<br><span class="gold">Nothing
      to hide.</span></div>
  <div class="sub" style="font-size:34px;max-width:78%">Test-drive Verodus free
      before you pay a cent. Then VERO35 at checkout.</div>
  <div class="pill" style="font-size:36px;padding:34px 60px">Start free · verodus.com</div>
</div>"""
    return render("w1-tryfree-3", page(*PORTRAIT, inner, legal=DISCLAIMER, seed=15),
                  *PORTRAIT)


def discord():
    channels = [("# rules", "Every objective, plain English"),
                ("# founders-chat", "Founders answer daily"),
                ("# support", "24/7 live help")]
    rows = "".join(f"""
    <div style="display:flex;align-items:baseline;gap:16px;padding:22px 0;
                border-bottom:1px solid rgba(212,175,55,.16)">
      <div style="font-size:32px;font-weight:800;color:{GOLD};min-width:270px">{c}</div>
      <div class="sub" style="font-size:24px">{d}</div>
    </div>""" for c, d in channels)
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">
  <div>
    <div class="eyebrow">Discord</div>
    <div class="h1" style="font-size:86px;margin-top:22px">Join the
        <span class="gold">founding community</span></div>
    <div class="sub" style="font-size:32px;margin-top:22px">Where the first Verodus
        traders hang out.</div>
  </div>
  <div class="card" style="padding:34px 44px">{rows}
    <div class="chip" style="font-size:24px;padding:14px 26px;margin-top:28px">
        Founder answers daily</div>
  </div>
</div>"""
    return render("w1-discord", page(*SQ, inner, seed=21), *SQ)


def logo_bug():
    """Transparent corner bug for burned-in video overlays."""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0}} html,body{{width:520px;height:150px;background:transparent}}
.wrap{{display:flex;align-items:center;height:100%;padding:0 24px}}
img{{height:56px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.6))}}
</style></head><body><div class="wrap">
<img src="{LOGO_MARK.replace('data:image/png;base64,', 'data:image/png;base64,')}">
</div></body></html>"""
    return render("w1-logo-bug", html, 520, 150)


def build():
    manifesto_open()
    manifesto_end()
    tryfree_1()
    tryfree_2()
    tryfree_3()
    discord()
    logo_bug()


if __name__ == "__main__":
    build()
