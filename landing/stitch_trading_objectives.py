#!/usr/bin/env python3
"""Stitch live Verodus trading-objectives chrome + rec Instant/Lite rules.

Loads styles, images, nav, footer, and markup from www.verodus.com via
<base href>. Rec Instant (no $200k, 5 valid days at +0.5% SOD, 6% trail
never locks) is injected locally. Reward cycles stay the live cards.
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "landing" / "trading-objectives.html"
REC = ROOT / "landing" / "to-rec.js"
LIVE_URL = "https://www.verodus.com/trading-objectives.html"


def fetch_live() -> str:
    local = Path("/tmp/verodus-trading-objectives.html")
    try:
        html = urllib.request.urlopen(LIVE_URL, timeout=20).read().decode("utf-8", "replace")
        local.write_text(html)
        return html
    except Exception:
        if local.exists():
            return local.read_text()
        fallback = Path("/tmp/trading-objectives.html")
        if fallback.exists():
            return fallback.read_text()
        raise


def stitch(html: str, rec: str) -> str:
    html = html.replace(
        '<meta charset="UTF-8">',
        '<meta charset="UTF-8">\n    <base href="https://www.verodus.com/">',
        1,
    )
    html = re.sub(
        r'<script type="application/json" id="weglot-data">.*?</script>',
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<script async="" src="https://cdn\.weglot\.com/[^"]+"[^>]*></script>',
        "",
        html,
        count=1,
    )
    if rec.strip() not in html:
        rec_block = (
            "\n    <script>\n"
            "    /* Rec Instant/Lite overlays. Chrome/CSS/nav/footer from verodus.com. */\n"
            f"{rec.rstrip()}\n"
            "    </script>\n"
        )
        if "</body>" not in html:
            raise SystemExit("</body> not found in live trading-objectives")
        html = html.replace("</body>", rec_block + "</body>", 1)
    return html


def main():
    live = fetch_live()
    rec = REC.read_text()
    out = stitch(live, rec)
    OUT.write_text(out)
    print(f"Wrote {OUT} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
