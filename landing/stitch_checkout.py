#!/usr/bin/env python3
"""Stitch live Verodus checkout chrome + rec add-on logic.

Loads styles, images, nav, footer, and markup from www.verodus.com via
<base href>. Rec billing and the Blue Guardian-style quantity selector
are injected locally.
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "landing" / "checkout.html"
LOGIC = ROOT / "landing" / "checkout-logic.js"
LIVE_URL = "https://www.verodus.com/checkout.html"

QTY_HTML = """
                    <div class="co-qty-box" id="coQtyBox">
                        <div class="co-qty-kicker">Quantity</div>
                        <div class="co-qty-label">Number of accounts to purchase</div>
                        <div class="co-tabs co-qty-tabs" id="coQty"></div>
                    </div>
"""

QTY_CSS = """
    <style id="co-qty-css">
      .co-qty-box { margin: .85rem 0 0; }
      .co-qty-kicker {
        color: var(--text-on-dark, #cbd5e1);
        margin-bottom: .2rem;
        font-size: .9rem;
        font-weight: 700;
      }
      .co-qty-label {
        color: var(--text-on-theme-dim, #e2e8f0a6);
        margin-bottom: .55rem;
        font-size: .75rem;
      }
      .co-qty-tabs { flex-wrap: wrap; gap: .4rem; display: flex; }
      .co-qty-tabs .co-tab {
        flex: 1 1 calc(50% - .4rem);
        justify-content: center;
        min-width: 0;
        padding: .5rem .6rem;
        font-size: .78rem;
      }
      @media (width <= 960px) {
        .co-summary-col { position: static; }
      }
      @media (width <= 640px) {
        .co-qty-tabs .co-tab { flex: 1 1 calc(50% - .4rem); font-size: .72rem; padding: .45rem .4rem; }
      }
      .co-coupon-feedback.ok { color: #34d399; }
      .co-coupon-feedback.err { color: #f87171; }
    </style>
"""


def fetch_live() -> str:
    local = Path("/tmp/verodus-checkout.html")
    try:
        html = urllib.request.urlopen(LIVE_URL, timeout=20).read().decode("utf-8", "replace")
        local.write_text(html)
        return html
    except Exception:
        if local.exists():
            return local.read_text()
        raise


def extract_countries(html: str) -> str:
    m = re.search(r"var COUNTRIES = \[.*?^\s*\];", html, re.S | re.M)
    if not m:
        raise SystemExit("COUNTRIES array not found in live checkout")
    return m.group(0)


def stitch(html: str, logic: str, countries: str) -> str:
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
    html = html.replace(
        '<link rel="stylesheet" href="checkout.css?v=20260730nobanner">',
        '<link rel="stylesheet" href="checkout.css?v=20260730nobanner">\n' + QTY_CSS,
        1,
    )

    html = re.sub(
        r'\s*<li id="co-order-terms-platform5-only">I confirm that I am not a U\.S\. citizen or resident\.</li>\s*',
        "\n",
        html,
        count=1,
    )

    needle = """                    <div class="co-summary-row">
                        <span class="co-summary-row-label">Account Size</span>
                        <span class="co-summary-row-value" id="sumSize">$5K</span>
                    </div>"""
    if needle not in html:
        raise SystemExit("Account Size summary block not found")
    html = html.replace(needle, needle + "\n" + QTY_HTML, 1)

    # Drop the live orchestra script; keep overlays / header / footer.
    marker = "    <script>\n    (function () {"
    idx = html.find(marker)
    if idx < 0:
        marker = "<script>\n    (function () {"
        idx = html.find(marker)
    if idx < 0:
        raise SystemExit("Live checkout script marker not found")
    chrome = html[:idx].rstrip() + "\n\n"

    rec = (
        "    <script>\n"
        "    /* Rec add-on billing. Chrome/CSS/nav/footer from verodus.com. */\n"
        f"    {countries}\n\n"
        f"{logic.rstrip()}\n"
        "    </script>\n"
        "</body>\n"
        "</html>\n"
    )
    # logic.js is already an IIFE; wrap as a script body without extra function
    if logic.strip().startswith("(function ()"):
        rec = (
            "    <script>\n"
            "    /* Rec add-on billing. Chrome/CSS/nav/footer from verodus.com. */\n"
            f"    {countries}\n\n"
            f"{logic.strip()}\n"
            "    </script>\n"
            "</body>\n"
            "</html>\n"
        )
    return chrome + rec


def main():
    live = fetch_live()
    countries = extract_countries(live)
    logic = LOGIC.read_text()
    out = stitch(live, logic, countries)
    OUT.write_text(out)
    print(f"Wrote {OUT} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
