"""Week 2 — Rules & transparency.

Static max drawdown is a 2-Step claim only. Instant uses a 6% trail that never
locks, so every static-drawdown asset carries the plan label.
"""

from style import BODY, CHIP_BLUE, DISCLAIMER, GOLD, HEADING, page
from render import render

SQ, PORTRAIT, STORY = (1080, 1080), (1080, 1350), (1080, 1920)


def static_key():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">
  <div class="chip" style="font-size:25px;padding:16px 30px;align-self:flex-start">
      2-Step Pro — not Instant</div>
  <div class="metal" style="font-size:132px">$10,000<br>= a fixed<br>$1,000 you<br>can lose</div>
  <div class="rule" style="width:320px"></div>
  <div class="h1" style="font-size:78px">It doesn’t move.</div>
  <div class="sub" style="font-size:29px;max-width:86%">Instant is different — a 6%
      limit that trails and never locks. Both are published before you pay.</div>
</div>"""
    return render("w2-static-key", page(*STORY, inner, legal=DISCLAIMER, seed=4), *STORY)


def static_diagram():
    def panel(title, tone, floor_desc, bars, outcome, outcome_color):
        return f"""
  <div class="card" style="flex:1;padding:40px 36px;display:flex;flex-direction:column;
       gap:24px;border-color:{tone}55">
    <div style="font-size:40px;font-weight:900;letter-spacing:.04em;
                text-transform:uppercase;color:{tone}">{title}</div>
    <div class="sub" style="font-size:25px;min-height:74px">{floor_desc}</div>
    <div style="position:relative;flex:1;border-left:1px solid rgba(255,255,255,.2);
                border-bottom:1px solid rgba(255,255,255,.2)">
      {bars}
    </div>
    <div style="font-size:29px;font-weight:800;color:{outcome_color};
                text-transform:uppercase;letter-spacing:.05em;min-height:76px">{outcome}</div>
  </div>"""

    def equity(points, color):
        pts = " ".join(f"{x},{y}" for x, y in points)
        return (f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" '
                f'style="position:absolute;inset:0;width:100%;height:100%">'
                f'<polyline points="{pts}" fill="none" stroke="{color}" '
                f'stroke-width="2.4" vector-effect="non-scaling-stroke"/></svg>')

    # same equity path in both panels; only the floor behaviour differs
    curve = [(0, 78), (14, 62), (28, 70), (42, 44), (58, 52), (72, 26), (86, 40), (100, 54)]
    trail = [(0, 96), (14, 84), (28, 84), (42, 66), (58, 66), (72, 48), (86, 48), (100, 48)]
    flat = [(0, 96), (100, 96)]

    def marker(x, y, color):
        # a plain div keeps the dot round; the SVGs above are stretched to fill
        return (f'<div style="position:absolute;left:{x}%;top:{y}%;width:22px;height:22px;'
                f'margin:-11px 0 0 -11px;border-radius:50%;background:{color};'
                f'box-shadow:0 0 0 6px {color}33"></div>')

    left = panel(
        "Trailing", "#e0655f",
        "The limit moves up every time you make a new high.",
        equity(curve, "#f5f5f5") + equity(trail, "#e0655f") + marker(96, 53, "#e0655f"),
        "Stopped out in profit", "#e0655f")
    right = panel(
        "Static", GOLD,
        "The limit is set from your starting balance and never moves.",
        equity(curve, "#f5f5f5") + equity(flat, GOLD),
        "Room stays yours", GOLD)

    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;gap:36px;padding-top:10px">
  <div>
    <div class="chip" style="font-size:24px;padding:14px 28px">2-Step Lite &amp; Pro</div>
    <div class="h1" style="font-size:88px;margin-top:24px">Static vs
        <span class="gold">trailing</span></div>
  </div>
  <div style="display:flex;gap:28px;flex:1">{left}{right}</div>
  <div class="sub" style="font-size:26px">Instant's limit trails and never locks.
      If you want static, buy Lite or Pro.</div>
</div>"""
    return render("w2-static-diagram", page(*STORY, inner, legal=DISCLAIMER, seed=8), *STORY)


RULES = [
    ("a", "No time limit", "Trade at your own pace."),
    ("b", "Static max loss", "Set on day one, never moves — 2-Step Lite &amp; Pro."),
    ("c", "80% split", "Every two weeks. 90% on demand is an add-on."),
    ("d", "Fee back on first reward", "100% refund on evaluations. Instant excluded."),
    ("e", "Scale to $1,000,000", "Grow with measured performance."),
]


def rule_tiles():
    out = []
    for i, (key, head, support) in enumerate(RULES):
        size = 150 if len(head) < 16 else 118
        inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:38px">
  <div class="eyebrow">Rule {i + 1} of 5</div>
  <div class="metal" style="font-size:{size}px">{head}</div>
  <div class="rule" style="width:300px"></div>
  <div class="sub" style="font-size:36px;font-weight:300">{support}</div>
</div>"""
        out.append(render(f"w2-rule-{key}", page(*PORTRAIT, inner, seed=13 + i), *PORTRAIT))
    return out


def plans():
    cols = [
        ("Instant", False, ["None", "6% trailing", "3%", "5 valid", "No"]),
        ("1-Step", False, ["10%", "6% hybrid", "4%", "None", "Yes"]),
        ("2-Step Lite", False, ["8% → 5%", "8% static", "4%", "5 + 5", "Yes"]),
        ("2-Step Pro", True, ["10% → 5%", "10% static", "5%", "5 + 5", "Yes"]),
    ]
    labels = ["Profit target", "Max drawdown", "Daily limit", "Min days", "Fee refund"]

    head = "".join(
        f"""<div style="flex:1;text-align:center;padding:14px 4px;border-radius:12px;
            background:{'linear-gradient(180deg,' + CHIP_BLUE + ',#2a4fae)' if hl else 'transparent'};
            font-size:26px;font-weight:800;text-transform:uppercase;letter-spacing:-.01em;
            white-space:nowrap;color:{'#fff' if hl else GOLD}">{name}</div>"""
        for name, hl, _ in cols)

    rows = ""
    for r, label in enumerate(labels):
        cells = "".join(
            f"""<div style="flex:1;text-align:center;font-size:26px;white-space:nowrap;
                font-weight:{800 if hl else 500};color:{'#fff' if hl else BODY}">{vals[r]}</div>"""
            for _, hl, vals in cols)
        rows += f"""
    <div style="display:flex;align-items:center;padding:24px 0;
                border-top:1px solid rgba(212,175,55,.16)">
      <div style="width:210px;font-size:23px;color:{GOLD};font-weight:700;
                  text-transform:uppercase;letter-spacing:.03em">{label}</div>
      <div style="flex:1;display:flex">{cells}</div>
    </div>"""

    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">
  <div class="h1" style="font-size:80px">Choose your <span class="gold">path</span></div>
  <div class="card" style="padding:30px 30px">
    <div style="display:flex;align-items:center">
      <div style="width:210px"></div>
      <div style="flex:1;display:flex;gap:4px">{head}</div>
    </div>
    {rows}
  </div>
  <div class="sub" style="font-size:25px">80% every 2 weeks · 90% on demand · Sizes $5,000–$200,000
      · 175+ countries</div>
</div>"""
    return render("w2-plans", page(*SQ, inner, legal=DISCLAIMER, seed=19, legal_size=16), *SQ)


def caption_chips():
    """Transparent overlay chips for the screen-share short."""
    texts = ["No time limit", "Static drawdown — 2-Step", "Fee refund on first reward"]
    out = []
    for i, t in enumerate(texts):
        html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:920px;height:150px;background:transparent;
  font-family:"Inter Display","Inter",system-ui,sans-serif}}
.wrap{{display:flex;align-items:center;height:100%;padding:0 20px}}
.chip{{display:inline-flex;align-items:center;gap:18px;padding:26px 44px;
  border-radius:999px;background:linear-gradient(180deg,#f0dc9a,{GOLD});
  color:#0f172a;font-size:42px;font-weight:900;text-transform:uppercase;
  letter-spacing:.04em;box-shadow:0 14px 40px rgba(0,0,0,.45)}}
</style></head><body><div class="wrap"><div class="chip">{t}</div></div></body></html>"""
        out.append(render(f"w2-chip-{i + 1}", html, 920, 150))
    return out


def build():
    static_key()
    static_diagram()
    rule_tiles()
    plans()
    caption_chips()


if __name__ == "__main__":
    build()
