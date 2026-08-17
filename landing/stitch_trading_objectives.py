#!/usr/bin/env python3
"""Stitch live Verodus trading-objectives chrome + rec Instant/Lite rules.

Loads styles, images, nav, footer, and markup from www.verodus.com via
<base href>. Rec Instant (no $200k, 5 valid days at +0.5% SOD, 6% trail
never locks) is injected locally. The five legal reward combinations are
the reward-cycle cards. 90% Weekly is not offered. On Demand still has
to meet Instant 5 valid days / eval 3 trading days.
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "landing" / "trading-objectives.html"
REC = ROOT / "landing" / "to-rec.js"
LIVE_URL = "https://www.verodus.com/trading-objectives.html"

REWARD_CYCLE_GRID = """<div class="reward-cycle-grid">
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcOnDemand">On Demand</div>
                    <div class="rc-pct">80%</div>
                    <div class="rc-label" data-i18n="content.rcRewardSplit">Reward Split</div>
                    <div class="rc-details">
                        <div class="rc-detail-row"><span data-i18n="content.span20">Request</span><span data-i18n="content.span21">Anytime</span></div>
                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcWeekly">Weekly</div>
                    <div class="rc-pct">80%</div>
                    <div class="rc-label" data-i18n="content.rcRewardSplit">Reward Split</div>
                    <div class="rc-details">
                        <div class="rc-detail-row"><span data-i18n="content.span16">Request every</span><span data-i18n="content.span17">7 days</span></div>
                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card rc-featured">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>
                    <div class="rc-pct">80%</div>
                    <div class="rc-label" data-i18n="content.rcRewardSplit">Reward Split</div>
                    <div class="rc-details">
                        <div class="rc-detail-row"><span data-i18n="content.span16">Request every</span><span data-i18n="content.span19">14 days</span></div>
                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcOnDemand">On Demand</div>
                    <div class="rc-pct">90%</div>
                    <div class="rc-label" data-i18n="content.rcRewardSplit">Reward Split</div>
                    <div class="rc-details">
                        <div class="rc-detail-row"><span data-i18n="content.span20">Request</span><span data-i18n="content.span21">Anytime</span></div>
                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>
                    <div class="rc-pct">90%</div>
                    <div class="rc-label" data-i18n="content.rcRewardSplit">Reward Split</div>
                    <div class="rc-details">
                        <div class="rc-detail-row"><span data-i18n="content.span16">Request every</span><span data-i18n="content.span19">14 days</span></div>
                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
            </div>
"""

RC_CENTER_CSS = """
    <style id="rec-reward-cycle-css">
      .reward-cycle-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1.2rem;
        max-width: 1100px;
        margin: 0 auto;
      }
      .reward-cycle-grid > .reward-cycle-card { grid-column: span 2; }
      .reward-cycle-grid > .reward-cycle-card:nth-child(4) { grid-column: 2 / span 2; }
      .reward-cycle-grid > .reward-cycle-card:nth-child(5) { grid-column: 4 / span 2; }
      @media (max-width: 760px) {
        .reward-cycle-grid { grid-template-columns: 1fr; }
        .reward-cycle-grid > .reward-cycle-card { grid-column: auto; }
      }
      #refundHighlightCard[hidden] { display: none !important; }
      .reward-highlight-grid.rh-no-refund {
        grid-template-columns: 1fr;
        max-width: 420px;
      }
    </style>
"""


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


def replace_element(html: str, needle: str, replacement: str, eat_trailing_ws: bool = False) -> str:
    start = html.find(needle)
    if start < 0:
        raise SystemExit(f"needle not found: {needle}")
    i = start
    depth = 0
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            gt = html.find(">", i)
            if gt < 0:
                break
            i = gt + 1
            continue
        if html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                if eat_trailing_ws:
                    while i < len(html) and html[i] in " \t\r\n":
                        i += 1
                return html[:start] + replacement + html[i:]
            continue
        i += 1
    raise SystemExit(f"unclosed element starting at {needle}")


def strip_element(html: str, needle: str) -> str:
    if needle not in html:
        return html
    return replace_element(html, needle, "", eat_trailing_ws=True)


def stitch(html: str, rec: str) -> str:
    html = html.replace("\r\n", "\n")
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
    html = re.sub(
        r'(data-i18n="content.p6">)[^<]*',
        r'\1Possible combinations. Weekly cannot be combined with On Demand or 90%.',
        html,
        count=1,
    )
    html = re.sub(
        r'(data-i18n="content.p7">)All reward request intervals are based on calendar days, not trading days\.[^<]*',
        r'\1All reward request intervals are based on calendar days, not trading days. On Demand still has to meet the plan trading-day rule before the first request.',
        html,
        count=1,
    )
    html = re.sub(
        r'(data-i18n-html="content.p8"><strong>)First Payout:',
        r'\1Payouts:',
        html,
        count=1,
    )

    qpf_badge_old = '<span class="badge badge-red" id="qpfNewsBadge">Restricted</span>'
    qpf_desc_old = (
        '<div class="eval-guide-desc" id="qpfNewsDesc">Not allowed to open or close a position ±2 min around high-impact (red folder) news events.</div>\n'
        '                        <div class="eval-guide-desc">* Unless News Trading Addon purchased.</div>'
    )
    qpf_js_old = "if (qpfBadge) qpfBadge.className = 'badge badge-red';"
    funded_news_old = (
        '                        <span class="badge badge-red">Restricted</span>\n'
        '                    </div>\n'
        '                    <div class="guide-desc">±2m window around high-impact news events. Profits deducted on violation.</div>'
    )
    for label, needle in (
        ("eval news desc", 'data-i18n="pricing.evalNewsDesc">'),
        ("QPF news badge", qpf_badge_old),
        ("QPF news desc", qpf_desc_old),
        ("updateEvalNewsCard", qpf_js_old),
        ("renderFundedGuides news", funded_news_old),
    ):
        if needle not in html:
            raise SystemExit(f"news-included needle not found: {label}")

    html = re.sub(
        r'(data-i18n="pricing.evalNewsDesc">)[^<]*',
        r'\1News trading is permitted.',
        html,
        count=1,
    )
    html = html.replace(
        qpf_badge_old,
        '<span class="badge badge-green" id="qpfNewsBadge">Allowed</span>',
        1,
    )
    html = html.replace(
        qpf_desc_old,
        '<div class="eval-guide-desc" id="qpfNewsDesc">News trading is permitted.</div>',
        1,
    )
    html = html.replace(
        qpf_js_old,
        "if (qpfBadge) { qpfBadge.className = 'badge badge-green'; qpfBadge.textContent = 'Allowed'; }",
        1,
    )
    html = html.replace(
        funded_news_old,
        '                        <span class="badge badge-green">Allowed</span>\n'
        '                    </div>\n'
        '                    <div class="guide-desc">News trading is permitted.</div>',
        1,
    )

    html = strip_element(html, '<div class="rc-combo-wrap" id="rcComboWrap">')
    html = re.sub(
        r"\n        \.rc-combo-wrap \{.*?\n        \}\n",
        "\n",
        html,
        count=1,
        flags=re.S,
    )

    html = replace_element(html, '<div class="reward-cycle-grid">', REWARD_CYCLE_GRID)
    html = html.replace(
        ".rc-details { display:grid; grid-template-rows:auto auto auto; gap:0.55rem; margin-top:auto; border-top:1px solid var(--border-subtle); padding-top:1rem; }",
        ".rc-details { display:grid; grid-template-rows:auto auto; gap:0.55rem; margin-top:auto; border-top:1px solid var(--border-subtle); padding-top:1rem; }",
        1,
    )
    if 'id="rec-reward-cycle-css"' not in html:
        html = html.replace("</head>", RC_CENTER_CSS + "</head>", 1)

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
