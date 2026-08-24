"""Verodus house style for launch creatives.

Tokens come from verodus.com/brand-kit.html, not from an invented palette:
gold #d4af37, page gradient #07003B -> #1B2B8E, Inter, official logo PNGs.
"""

import base64
import pathlib

BRAND_DIR = pathlib.Path(__file__).resolve().parents[1] / "brand"

GOLD = "#d4af37"
GOLD_LIGHT = "#f0dc9a"
GOLD_DEEP = "#a8862b"
BG_START = "#07003B"
BG_END = "#1B2B8E"
CTA_TEXT = "#0f172a"
HEADING = "#f5f5f5"
BODY = "#cbd5e1"
CHIP_BLUE = "#3b6fe0"

DISCLAIMER = (
    "Verodus only provides services of simulated trading and educational tools "
    "for traders. Verodus does not act as a broker and does not accept any "
    "deposits. All accounts we provide to our clients are demo accounts with "
    "fictitious funds and any trading is in a simulated environment only. 18+."
)
DISCLAIMER_SHORT = (
    "Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+."
)


def _data_uri(name: str) -> str:
    raw = (BRAND_DIR / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


LOGO_WORDMARK = _data_uri("Verodus-logo.png")
LOGO_MARK = _data_uri("Verodus-logo-only.png")


def candles(count: int = 26, seed: int = 7) -> str:
    """Faint candlestick texture for the lower third of the frame."""
    import random

    rng = random.Random(seed)
    bars = []
    for i in range(count):
        x = i * (100 / count)
        body = rng.uniform(6, 30)
        top = rng.uniform(4, 42)
        wick = body + rng.uniform(6, 22)
        bars.append(
            f'<rect x="{x + 0.6:.2f}" y="{top - (wick - body) / 2:.2f}" '
            f'width="0.35" height="{wick:.2f}" fill="{GOLD}"/>'
            f'<rect x="{x:.2f}" y="{top:.2f}" width="2.1" '
            f'height="{body:.2f}" fill="{GOLD}" rx="0.3"/>'
        )
    return (
        '<svg class="candles" viewBox="0 0 100 60" preserveAspectRatio="none" '
        'xmlns="http://www.w3.org/2000/svg">' + "".join(bars) + "</svg>"
    )


BASE_CSS = f"""
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
  width: 100%; height: 100%;
  background: {BG_START};
  font-family: "Inter Display", "Inter", system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  color: {HEADING};
}}

.frame {{
  position: relative;
  width: 100%; height: 100%;
  overflow: hidden;
  background:
    radial-gradient(120% 80% at 82% 6%, rgba(212,175,55,.20) 0%, rgba(212,175,55,0) 55%),
    radial-gradient(90% 70% at 10% 96%, rgba(27,43,142,.75) 0%, rgba(7,0,59,0) 60%),
    linear-gradient(163deg, {BG_START} 0%, #0d0752 46%, {BG_END} 100%);
  display: flex; flex-direction: column;
}}

/* thin gold inner keyline */
.frame::after {{
  content: ""; position: absolute; inset: 26px;
  border: 1px solid rgba(212,175,55,.22);
  border-radius: 6px; pointer-events: none;
}}

.candles {{
  position: absolute; left: 0; right: 0; bottom: 0;
  width: 100%; height: 34%;
  opacity: .085; pointer-events: none;
}}

.vignette {{
  position: absolute; inset: 0; pointer-events: none;
  background:
    linear-gradient(to bottom, rgba(0,0,0,0) 58%, rgba(3,0,26,.62) 100%),
    radial-gradient(115% 85% at 50% 42%, rgba(0,0,0,0) 42%, rgba(0,0,0,.55) 100%);
}}

.body {{
  position: relative; z-index: 2;
  flex: 1; display: flex; flex-direction: column;
  padding: 78px 84px 0;
}}

/* ---------- type ---------- */
.eyebrow {{
  font-size: 26px; font-weight: 700; letter-spacing: .30em;
  text-transform: uppercase; color: {GOLD};
}}
.h1 {{
  font-weight: 900; letter-spacing: -.022em; line-height: .92;
  text-transform: uppercase; color: {HEADING};
}}
.gold {{
  background: linear-gradient(178deg, {GOLD_LIGHT} 4%, {GOLD} 48%, {GOLD_DEEP} 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}}
.metal {{
  font-weight: 900; letter-spacing: -.035em; line-height: .84;
  text-transform: uppercase;
  background: linear-gradient(176deg, #fff6dc 2%, {GOLD_LIGHT} 22%, {GOLD} 56%, #8f6f1f 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 10px 26px rgba(0,0,0,.55));
}}
.sub {{
  color: {BODY}; font-weight: 400; line-height: 1.34; letter-spacing: -.005em;
}}
.rule {{
  height: 1px; background: linear-gradient(90deg, {GOLD} 0%, rgba(212,175,55,0) 92%);
}}

/* ---------- components ---------- */
.card {{
  background: linear-gradient(168deg, rgba(255,255,255,.075), rgba(255,255,255,.022));
  border: 1px solid rgba(212,175,55,.32);
  border-radius: 20px;
}}
.pill {{
  display: inline-flex; align-items: center; gap: 14px;
  background: linear-gradient(180deg, {GOLD_LIGHT}, {GOLD});
  color: {CTA_TEXT}; font-weight: 800; text-transform: uppercase;
  letter-spacing: .06em; border-radius: 999px;
  box-shadow: 0 18px 44px rgba(212,175,55,.24);
}}
.chip {{
  display: inline-flex; align-items: center;
  border: 1px solid rgba(212,175,55,.5);
  border-radius: 999px; color: {GOLD};
  font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
}}

/* ---------- lockup ---------- */
.lockup {{
  position: relative; z-index: 3;
  display: flex; flex-direction: column; align-items: center; gap: 18px;
  padding: 30px 0 44px;
}}
.lockup img {{ display: block; }}
.legal {{
  color: {BODY}; opacity: .52; text-align: center;
  max-width: 78%; line-height: 1.4;
}}
"""


def page(width: int, height: int, inner: str, extra_css: str = "",
         legal: str = DISCLAIMER_SHORT, logo_h: int = 36,
         seed: int = 7, legal_size: int = 17) -> str:
    """Wrap asset markup in the shared frame + logo lockup."""
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
{BASE_CSS}
@page {{ size: {width}px {height}px; margin: 0; }}
html, body {{ width: {width}px; height: {height}px; }}
.legal {{ font-size: {legal_size}px; }}
{extra_css}
</style></head>
<body><div class="frame">
{candles(seed=seed)}
<div class="vignette"></div>
<div class="body">
{inner}
</div>
<div class="lockup">
  <img src="{LOGO_WORDMARK}" style="height:{logo_h}px">
  <div class="legal">{legal}</div>
</div>
</div></body></html>"""
