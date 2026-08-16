#!/usr/bin/env python3
"""Render the Verodus Open Graph card (1200x630) with headless Chrome."""

from __future__ import annotations

import base64
import pathlib
import shutil
import subprocess
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "google-chrome"
WORDMARK_URL = "https://www.verodus.com/images/logo.png"
MARK_URL = "https://www.verodus.com/images/Verodus-Logo-Only.png"

GOLD = "#d4af37"
GOLD_LIGHT = "#f0dc9a"
BG_START = "#07003B"
BG_END = "#1B2B8E"
HEADING = "#f5f5f5"
BODY = "#cbd5e1"

FLAGS = [
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-first-run",
    "--disable-dev-shm-usage",
    "--disable-extensions",
    "--hide-scrollbars",
    "--force-device-scale-factor=1",
    "--virtual-time-budget=4000",
    "--default-background-color=00000000",
]


def _data_uri(url: str) -> str:
    local = ROOT.parents[1] / "brand" / pathlib.Path(url).name.replace("logo.png", "Verodus-logo.png")
    if local.exists():
        raw = local.read_bytes()
    else:
        raw = urllib.request.urlopen(url, timeout=30).read()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def html() -> str:
    wordmark = _data_uri(WORDMARK_URL)
    mark = _data_uri(MARK_URL)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
  body {{
    font-family: Inter, system-ui, sans-serif;
    color: {HEADING};
    -webkit-font-smoothing: antialiased;
  }}
  .frame {{
    width: 1200px; height: 630px; position: relative; overflow: hidden;
    background:
      radial-gradient(90% 80% at 88% 12%, rgba(212,175,55,.22) 0%, rgba(212,175,55,0) 52%),
      radial-gradient(70% 80% at 8% 100%, rgba(27,43,142,.85) 0%, rgba(7,0,59,0) 58%),
      linear-gradient(155deg, {BG_START} 0%, #0c0650 48%, {BG_END} 100%);
    padding: 52px 64px 44px;
    display: flex; flex-direction: column;
  }}
  .watermark {{
    position: absolute; right: -90px; top: 70px; width: 620px; height: 620px;
    opacity: .10; pointer-events: none;
  }}
  .top {{
    display: flex; align-items: center; justify-content: space-between;
    position: relative; z-index: 1;
  }}
  .logo {{ height: 44px; width: auto; display: block; }}
  .eyebrow {{
    font-size: 15px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase;
    color: {GOLD}; border: 1px solid rgba(212,175,55,.45);
    background: rgba(212,175,55,.12); padding: 8px 16px; border-radius: 999px;
  }}
  h1 {{
    position: relative; z-index: 1;
    margin-top: 54px; font-size: 72px; font-weight: 800; line-height: .98;
    letter-spacing: -.035em; max-width: 820px;
  }}
  h1 em {{ font-style: normal; color: {GOLD}; }}
  .sub {{
    position: relative; z-index: 1;
    margin-top: 22px; font-size: 26px; font-weight: 500; color: {BODY};
    line-height: 1.35; max-width: 760px;
  }}
  .chips {{
    position: relative; z-index: 1;
    display: flex; gap: 12px; margin-top: auto; padding-top: 36px;
  }}
  .chip {{
    font-size: 18px; font-weight: 600; color: {GOLD_LIGHT};
    border: 1px solid rgba(212,175,55,.35); background: rgba(7,0,59,.35);
    padding: 10px 18px; border-radius: 999px;
  }}
  .disclaimer {{
    position: relative; z-index: 1;
    margin-top: 22px; font-size: 13px; font-weight: 500; color: rgba(203,213,225,.72);
    letter-spacing: .01em;
  }}
</style>
</head>
<body>
  <div class="frame">
    <img class="watermark" alt="" src="{mark}">
    <div class="top">
      <img class="logo" alt="Verodus" src="{wordmark}">
      <span class="eyebrow">Prop firm</span>
    </div>
    <h1>Get funded.<br>Trade with up to <em>$1M</em>.</h1>
    <p class="sub">Trade Forex, equities &amp; crypto. Keep up to 90% profit split.</p>
    <div class="chips">
      <span class="chip">1-Step from $36</span>
      <span class="chip">Instant from $59</span>
      <span class="chip">2-Step from $39</span>
    </div>
    <p class="disclaimer">The fee is not trading capital. Performance rewards are discretionary and not guaranteed.</p>
  </div>
</body>
</html>
"""


def render(out: pathlib.Path, width: int = 1200, height: int = 630, timeout: float = 45.0) -> pathlib.Path:
    if out.exists():
        out.unlink()
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        src = tmp / "og.html"
        src.write_text(html(), encoding="utf-8")
        proc = subprocess.Popen(
            [
                CHROME,
                *FLAGS,
                f"--window-size={width},{height}",
                f"--screenshot={out}",
                f"--user-data-dir={tmp}/profile",
                src.as_uri(),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + timeout
        stable = 0
        last = -1
        while time.time() < deadline:
            time.sleep(0.35)
            if out.exists():
                size = out.stat().st_size
                stable = stable + 1 if size == last and size > 0 else 0
                last = size
                if stable >= 2:
                    break
            if proc.poll() is not None and out.exists():
                break
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError(f"render failed: {out}")
    print(f"wrote {out.name}  {width}x{height}  {out.stat().st_size // 1024} KB")
    return out


def to_webp(png: pathlib.Path) -> pathlib.Path | None:
    webp = png.with_suffix(".webp")
    cwebp = shutil.which("cwebp")
    if not cwebp:
        print("cwebp not installed — skipping webp")
        return None
    subprocess.check_call([cwebp, "-q", "90", str(png), "-o", str(webp)])
    print(f"wrote {webp.name}  {webp.stat().st_size // 1024} KB")
    return webp


if __name__ == "__main__":
    png = render(ROOT / "og-default.png")
    to_webp(png)
