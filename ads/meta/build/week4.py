"""Week 4 — Founding offer & conversion.

Only the two verified founding SKUs carry a price. Instant $25k+ is below or
near break-even, so the size ladder ships without stickers.
"""

from style import BODY, DISCLAIMER, GOLD, HEADING, page
from render import render

SQ, PORTRAIT, STORY = (1080, 1080), (1080, 1350), (1080, 1920)

BENEFITS = ["Try free first", "No time limit", "80% split · 90% on demand",
            "Fee back on evaluations"]


def offer_card():
    rows = "".join(f"""
    <div style="display:flex;align-items:center;gap:18px;padding:16px 0">
      <div style="width:12px;height:12px;border-radius:3px;background:{GOLD};
                  transform:rotate(45deg);flex:none"></div>
      <div style="font-size:31px;color:#f5f5f5;font-weight:500">{b}</div>
    </div>""" for b in BENEFITS)
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px">
  <div class="eyebrow">Founding cohort</div>
  <div class="metal" style="font-size:168px">Founding<br>pricing</div>
  <div class="chip" style="font-size:30px;padding:20px 36px;align-self:flex-start">
      Ends [DATE]</div>
  <div class="card" style="padding:26px 40px">{rows}</div>
  <div style="display:flex;gap:20px">
    <div class="card" style="flex:1;padding:26px 30px;text-align:center">
      <div class="metal" style="font-size:76px">$72</div>
      <div class="sub" style="font-size:24px;margin-top:8px">Instant $5k</div>
    </div>
    <div class="card" style="flex:1;padding:26px 30px;text-align:center">
      <div class="metal" style="font-size:76px">$36</div>
      <div class="sub" style="font-size:24px;margin-top:8px">1-Step $5k</div>
    </div>
  </div>
  <div class="pill" style="font-size:33px;padding:30px 52px;align-self:flex-start">
      Start your challenge — VERO35</div>
</div>"""
    return render("w4-offer-card", page(*STORY, inner, legal=DISCLAIMER, seed=47), *STORY)


def pricing():
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">
  <div class="h1" style="font-size:74px">Become a
      <span class="gold">founding trader</span></div>

  <div class="card" style="padding:34px 40px;display:flex;align-items:center;gap:30px">
    <div>
      <div class="metal" style="font-size:104px">$72</div>
    </div>
    <div style="flex:1">
      <div style="font-size:40px;font-weight:800;text-transform:uppercase;
                  color:{HEADING};letter-spacing:-.01em">Instant $5,000</div>
      <div class="sub" style="font-size:26px;margin-top:8px">No profit target ·
          3% daily · 6% trailing · no refund</div>
    </div>
    <div style="font-size:28px;color:{BODY};opacity:.55;text-decoration:line-through">$110</div>
  </div>

  <div class="card" style="padding:34px 40px;display:flex;align-items:center;gap:30px">
    <div>
      <div class="metal" style="font-size:104px">$36</div>
    </div>
    <div style="flex:1">
      <div style="font-size:40px;font-weight:800;text-transform:uppercase;
                  color:{HEADING};letter-spacing:-.01em">1-Step $5,000</div>
      <div class="sub" style="font-size:26px;margin-top:8px">10% target · 4% daily ·
          fee back on first reward</div>
    </div>
    <div style="font-size:28px;color:{BODY};opacity:.55;text-decoration:line-through">$55</div>
  </div>

  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap">
    <div class="chip" style="font-size:23px;padding:14px 26px">Try free</div>
    <div class="chip" style="font-size:23px;padding:14px 26px">80% split · 90% on demand</div>
    <div class="chip" style="font-size:23px;padding:14px 26px">Sizes to $200,000</div>
  </div>

  <div class="pill" style="font-size:32px;padding:30px 50px;align-self:flex-start">
      Start free — verodus.com</div>
  <div class="sub" style="font-size:24px">Founding pricing ends [DATE] · code VERO35</div>
</div>"""
    return render("w4-pricing", page(*PORTRAIT, inner, legal=DISCLAIMER, seed=51,
                                     legal_size=16), *PORTRAIT)


def sizes_ladder():
    # Instant $200k is not offered; the ladder lists evaluations at that tier
    sizes = [("$5,000", "Instant · 1-Step · Lite · Pro"),
             ("$10,000", "Instant · 1-Step · Lite · Pro"),
             ("$25,000", "Instant · 1-Step · Lite · Pro"),
             ("$50,000", "Instant · 1-Step · Lite · Pro"),
             ("$100,000", "Instant · 1-Step · Lite · Pro"),
             ("$200,000", "1-Step · Lite · Pro")]
    rows = "".join(f"""
    <div class="card" style="padding:22px 30px;display:flex;justify-content:space-between;
         align-items:center">
      <div style="font-size:40px;font-weight:800;color:{HEADING}">{s}</div>
      <div class="sub" style="font-size:24px">{plans}</div>
    </div>""" for s, plans in sizes)
    inner = f"""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px">
  <div>
    <div class="eyebrow">Account sizes</div>
    <div class="h1" style="font-size:70px;margin-top:18px">Pick your
        <span class="gold">tier</span></div>
  </div>
  {rows}
  <div class="sub" style="font-size:25px;margin-top:6px">Live prices at checkout with
      VERO35. Founding pair: Instant $5k $72 · 1-Step $5k $36.</div>
</div>"""
    return render("w4-sizes", page(*PORTRAIT, inner, legal=DISCLAIMER, seed=55,
                                   legal_size=16), *PORTRAIT)


def montage_open():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:42px">
  <div class="metal" style="font-size:196px">One<br>month<br>in</div>
  <div class="rule" style="width:280px"></div>
  <div class="h1" style="font-size:52px;line-height:1.2">Real rules.<br>Real people.<br>
      Real community.</div>
</div>"""
    return render("w4-montage-open", page(*STORY, inner, seed=59), *STORY)


def montage_end():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;
            align-items:center;text-align:center;gap:50px">
  <div class="h1" style="font-size:116px">Your turn<br>
      <span class="gold">to be early.</span></div>
  <div class="pill" style="font-size:36px;padding:34px 58px">Start free — verodus.com</div>
</div>"""
    return render("w4-montage-end", page(*STORY, inner, legal=DISCLAIMER, seed=63), *STORY)


def last_chance():
    inner = """
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:38px">
  <div class="chip" style="font-size:26px;padding:18px 32px;align-self:flex-start">
      Retargeting only</div>
  <div class="metal" style="font-size:150px">Founding<br>pricing<br>ends<br>tonight</div>
  <div class="rule" style="width:300px"></div>
  <div class="sub" style="font-size:32px">Try free · Fee back on evaluations ·
      Be a founding trader.</div>
  <div class="pill" style="font-size:34px;padding:32px 54px;align-self:flex-start">
      Start free — verodus.com</div>
</div>"""
    return render("w4-lastchance", page(*STORY, inner, legal=DISCLAIMER, seed=67), *STORY)


def build():
    offer_card()
    pricing()
    sizes_ladder()
    montage_open()
    montage_end()
    last_chance()


if __name__ == "__main__":
    build()
