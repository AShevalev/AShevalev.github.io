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
                        <div class="co-qty-copy">
                            <div class="co-qty-kicker">Quantity</div>
                            <div class="co-qty-label">Number of accounts to purchase</div>
                        </div>
                        <div class="co-qty-stepper" id="coQty">
                            <button type="button" class="co-qty-btn" id="coQtyMinus" aria-label="Decrease quantity">&minus;</button>
                            <span class="co-qty-value" id="coQtyValue">1</span>
                            <button type="button" class="co-qty-btn" id="coQtyPlus" aria-label="Increase quantity">+</button>
                        </div>
                    </div>
"""

QTY_CSS = """
    <style id="co-qty-css">
      .co-qty-box {
        justify-content: space-between; align-items: center; gap: 1rem;
        margin: .85rem 0 0; display: flex;
      }
      .co-qty-copy { min-width: 0; }
      .co-qty-kicker {
        color: #fff;
        margin: 0;
        font-size: .95rem;
        font-weight: 700;
        line-height: 1.2;
      }
      .co-qty-label {
        color: var(--text-on-theme-dim, #e2e8f0a6);
        margin: .2rem 0 0;
        font-size: .75rem;
        line-height: 1.3;
      }
      .co-qty-stepper {
        border: 1px solid var(--border-on-theme, #ffffff26);
        border-radius: 999px;
        flex-shrink: 0; align-items: center;
        min-width: 118px; height: 40px;
        display: flex;
      }
      .co-qty-btn {
        color: #fff; cursor: pointer; background: 0 0; border: none;
        flex: 1; height: 100%; padding: 0;
        font-size: 1.15rem; line-height: 1;
      }
      .co-qty-btn:disabled { opacity: .35; cursor: default; }
      .co-qty-value {
        color: #fff; min-width: 1.4rem; text-align: center;
        font-size: .95rem; font-weight: 700;
      }
      .co-refund-note {
        color: var(--text-on-theme-dim, #e2e8f0a6);
        margin: .55rem 0 0;
        font-size: .75rem;
        line-height: 1.4;
      }
      .co-refundable.is-hidden { display: none; }
      @media (width <= 960px) {
        .co-summary-col { position: static; }
      }
      @media (width <= 400px) {
        .co-qty-box { align-items: flex-start; flex-direction: column; gap: .65rem; }
        .co-qty-stepper { width: 100%; }
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

    total_needle = """                    <div class="co-summary-total">
                        <span class="co-total-label">Total</span>
                        <span class="co-total-amount" id="sumTotal">$65</span>
                    </div>"""
    if total_needle not in html:
        raise SystemExit("Total summary block not found")
    html = html.replace(total_needle, total_needle + "\n" + QTY_HTML, 1)

    html = html.replace(
        '<input type="text" id="coCoupon" placeholder="Coupon code" autocomplete="off">',
        '<input type="text" id="coCoupon" placeholder="Coupon code" autocomplete="off" value="VERO35">',
        1,
    )
    html = html.replace(
        '<div class="co-coupon-feedback" id="coCouponFeedback" aria-live="polite"></div>',
        '<div class="co-coupon-feedback ok" id="coCouponFeedback" aria-live="polite">Coupon applied.</div>',
        1,
    )

    refund_old = """                    <div class="co-refundable" id="coRefundable">
                        <span class="co-refundable-pill">
                            <svg class="co-refundable-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <circle cx="12" cy="12" r="9"></circle>
                                <polyline points="8 12 11 15 16 9"></polyline>
                            </svg>
                            <span class="co-refundable-label">Refundable on first payout</span>
                        </span>
                    </div>"""
    refund_new = """                    <div class="co-refundable" id="coRefundable">
                        <span class="co-refundable-pill" id="coRefundablePill">
                            <svg class="co-refundable-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                <circle cx="12" cy="12" r="9"></circle>
                                <polyline points="8 12 11 15 16 9"></polyline>
                            </svg>
                            <span class="co-refundable-label" id="coRefundableLabel">Refundable on first payout excluding add-on fees.</span>
                        </span>
                        <div class="co-refund-note" id="coRefundNote"></div>
                    </div>"""
    if refund_old not in html:
        raise SystemExit("Refundable pill block not found")
    html = html.replace(refund_old, refund_new, 1)

    html = html.replace(
        '<div class="modal-foot text-normal">Add-on eligibility and rules apply per program terms.</div>',
        '<div class="modal-foot text-normal">Add-on fees are not refundable. Eligibility and rules apply per program terms.</div>',
        1,
    )

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
