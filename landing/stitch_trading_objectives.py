#!/usr/bin/env python3
"""Stitch live Verodus trading-objectives chrome + rec Instant/Lite rules.

Loads styles, images, nav, footer, and markup from www.verodus.com via
<base href>. Rec Instant (no $200k, 5 valid days at +0.5% SOD, 6% trail
never locks) is injected locally. Weekly is rec 80%. The three legal
combinations are the reward-cycle cards. On Demand still has to meet
Instant 5 valid days / 1-Step 3 trading days.
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


def strip_element(html: str, needle: str) -> str:
    start = html.find(needle)
    if start < 0:
        return html
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
                while i < len(html) and html[i] in " \t\r\n":
                    i += 1
                return html[:start] + html[i:]
            continue
        i += 1
    return html


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
        r'(data-i18n="content.rcWeekly">Weekly</div>\s*<div class="rc-pct">)70%',
        r'\g<1>80%',
        html,
        count=1,
    )
    html = re.sub(
        r'(data-i18n="content.p6">)[^<]*',
        r'\1Possible combinations. Pick one — Weekly and On Demand cannot be combined.',
        html,
        count=1,
    )
    html = re.sub(
        r'(data-i18n="content.p7">)All reward request intervals are based on calendar days, not trading days\.[^<]*',
        r'\1All reward request intervals are based on calendar days, not trading days. On Demand still has to meet the plan trading-day rule before the first request.',
        html,
        count=1,
    )

    html = strip_element(html, '<div class="rc-combo-wrap" id="rcComboWrap">')
    html = re.sub(
        r"\n        \.rc-combo-wrap \{.*?\n        \}\n",
        "\n",
        html,
        count=1,
        flags=re.S,
    )

    html = html.replace(
        '<span data-i18n="content.span21">Anytime</span>',
        '<span data-i18n="content.span21">Anytime after min days</span>',
        1,
    )

    if 'data-rc-how="1"' not in html:
        weekly_how = """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>"""
        weekly_how_new = """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                        <div class="rc-detail-row" data-rc-days="1" onclick="showModal('first-request')" style="cursor:pointer;"><span>First request after</span><span>3 trading days</span></div>
                        <div class="rc-detail-row" data-rc-how="1"><span>How</span><span>Add-on</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>"""
        if weekly_how not in html:
            raise SystemExit("Weekly card details needle not found")
        html = html.replace(weekly_how, weekly_how_new, 1)
        html = html.replace(
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card rc-featured">""",
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                        <div class="rc-detail-row" data-rc-days="1" onclick="showModal('first-request')" style="cursor:pointer;"><span>First request after</span><span>3 trading days</span></div>
                        <div class="rc-detail-row" data-rc-how="1"><span>How</span><span>Included</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card rc-featured">""",
            1,
        )
        html = html.replace(
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span data-i18n="content.span22">2% and $200</span></div>
                    </div>
                </div>
            </div>""",
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span data-i18n="content.span22">2% and $200</span></div>
                        <div class="rc-detail-row" data-rc-days="1" onclick="showModal('first-request')" style="cursor:pointer;"><span>First request after</span><span>3 trading days</span></div>
                        <div class="rc-detail-row" data-rc-how="1"><span>How</span><span>Add-on</span></div>
                    </div>
                </div>
            </div>""",
            1,
        )
    html = re.sub(
        r'(data-i18n="content.rcBiWeekly">Bi-Weekly</div>.*?Minimum Reward</span><span>\$100</span></div>\n)(\s*<div class="rc-detail-row" data-rc-how="1">)',
        r'\1                        <div class="rc-detail-row" data-rc-days="1" onclick="showModal(\'first-request\')" style="cursor:pointer;"><span>First request after</span><span>3 trading days</span></div>\n\2',
        html,
        count=1,
        flags=re.S,
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
