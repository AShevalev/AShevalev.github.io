"""Week 3 — Trust, founder access & first cohort.

Activity only. No payout figures anywhere in this set.
"""

from style import BODY, DISCLAIMER, GOLD, HEADING, LOGO_MARK, page
from render import render

SQ, PORTRAIT, STORY = (1080, 1080), (1080, 1350), (1080, 1920)

QUESTIONS = [
    ("q1", "Are you a scam?"),
    ("q2", "How do I know you’ll pay?"),
    ("q3", "Why should I trust you?"),
]


def ama_questions():
    out = []
    for i, (key, q) in enumerate(QUESTIONS):
        inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:44px">
  <div class="chip" style="font-size:26px;padding:18px 34px">Ask us anything</div>
  <div class="h1" style="font-size:118px;max-width:92%">{q}</div>
  <div class="rule" style="width:260px"></div>
  <div class="sub" style="font-size:30px">Founder AMA · answered on camera</div>
</div>"""
        out.append(render(f"w3-ama-{key}", page(*STORY, inner, seed=23 + i), *STORY))
    return out


def ama_thumb():
    inner = f"""
<div style="flex:1;display:flex;align-items:center;gap:52px">
  <img src="{LOGO_MARK}" style="height:230px;flex:none">
  <div style="display:flex;flex-direction:column;gap:26px">
    <div class="chip" style="font-size:26px;padding:16px 30px;align-self:flex-start">AMA</div>
    <div class="h1" style="font-size:74px">Meet the people behind
        <span class="gold">Verodus</span></div>
    <div class="sub" style="font-size:29px">The hard questions, answered on camera.</div>
  </div>
</div>"""
    return render("w3-ama-thumb", page(*SQ, inner, seed=27), *SQ)


def walkthrough_end():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:48px">
  <div class="h1" style="font-size:96px">See everything<br>
      <span class="gold">before you pay.</span></div>
  <div class="sub" style="font-size:33px;max-width:80%">Free trial · same rules ·
      TradeHub or Platform 5</div>
  <div class="pill" style="font-size:36px;padding:34px 58px">Start free — verodus.com</div>
</div>"""
    return render("w3-walkthrough-end", page(*STORY, inner, legal=DISCLAIMER, seed=31), *STORY)


def step_strip():
    """Transparent step chips for the top of the walkthrough recording."""
    steps = ["1 Start free", "2 Dashboard", "3 Rules", "4 Choose challenge"]
    chips = "".join(f"""
  <div class="chip">{s}</div>""" for s in steps)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:170px;background:transparent;
  font-family:"Inter Display","Inter",system-ui,sans-serif}}
.row{{display:flex;align-items:center;justify-content:center;gap:16px;height:100%}}
.chip{{padding:22px 30px;border-radius:999px;font-size:30px;font-weight:800;
  text-transform:uppercase;letter-spacing:.03em;white-space:nowrap;
  color:{GOLD};border:1px solid rgba(212,175,55,.6);
  background:rgba(7,0,59,.82);box-shadow:0 10px 30px rgba(0,0,0,.4)}}
</style></head><body><div class="row">{chips}</div></body></html>"""
    return render("w3-step-strip", html, 1080, 170)


def momentum():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:26px">
  <div class="eyebrow">Founding cohort</div>
  <div class="metal" style="font-size:340px;line-height:.8">[ N ]</div>
  <div class="h1" style="font-size:54px;max-width:86%">Founding traders joined this week</div>
  <div class="rule" style="width:260px;margin-top:10px"></div>
  <div class="sub" style="font-size:30px">Be early — founding pricing won’t last.</div>
</div>"""
    return render("w3-momentum", page(*SQ, inner, seed=35), *SQ)


def promise_1():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">
  <div class="chip" style="font-size:24px;padding:16px 30px;align-self:flex-start">
      As of [DATE]</div>
  <div class="h1" style="font-size:96px">The rules you start with are
      <span class="gold">the rules you finish with.</span></div>
  <div class="rule" style="width:320px"></div>
  <div class="sub" style="font-size:34px">No rule changes after you pay.<br>
      Published, dated, public.</div>
</div>"""
    return render("w3-promise-1", page(*PORTRAIT, inner, seed=39), *PORTRAIT)


def promise_2():
    clauses = [
        ("Instant", "No profit target · 3% daily · 6% trailing · 5 valid days"),
        ("1-Step", "10% target · 4% daily · 6% hybrid · fee refund"),
        ("2-Step Lite", "8% → 5% · 4% daily · 8% static · fee refund"),
        ("2-Step Pro", "10% → 5% · 5% daily · 10% static · fee refund"),
    ]
    rows = "".join(f"""
    <div style="padding:24px 0;border-bottom:1px solid rgba(212,175,55,.16)">
      <div style="font-size:32px;font-weight:800;color:{GOLD};text-transform:uppercase;
                  letter-spacing:.03em">{p}</div>
      <div class="sub" style="font-size:25px;margin-top:8px">{r}</div>
    </div>""" for p, r in clauses)
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px">
  <div>
    <div class="eyebrow">Published objectives</div>
    <div class="h1" style="font-size:66px;margin-top:20px">Screenshot this.</div>
  </div>
  <div class="card" style="padding:20px 40px">{rows}
    <div class="sub" style="font-size:23px;padding-top:24px">
        verodus.com/trading-objectives.html</div>
  </div>
</div>"""
    return render("w3-promise-2", page(*PORTRAIT, inner, legal=DISCLAIMER, seed=43), *PORTRAIT)


def build():
    ama_questions()
    ama_thumb()
    walkthrough_end()
    step_strip()
    momentum()
    promise_1()
    promise_2()


if __name__ == "__main__":
    build()
