#!/usr/bin/env python3
"""Stitch live Verodus trading-objectives chrome + rec Instant/Lite rules.

Loads styles, images, nav, footer, and markup from www.verodus.com via
<base href>. Rec Instant (no $200k, 5 valid days at +0.5% SOD, 6% trail
never locks) is injected locally. Weekly reward cycle is rec 80% (same
split as Bi-Weekly), not live's 70%. Reward Cycles lists the three legal
combinations (Weekly 80% XOR On Demand 90%; Bi-Weekly 80% is included).
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "landing" / "trading-objectives.html"
REC = ROOT / "landing" / "to-rec.js"
LIVE_URL = "https://www.verodus.com/trading-objectives.html"

COMBO_CSS = """
        .rc-combo-wrap { max-width:1000px; margin:2.2rem auto 0; }
        .rc-combo-title { text-align:center; margin:0 0 0.4rem; font-size:1.05rem; font-weight:700; color:var(--heading-h2); }
        .rc-combo-lead { text-align:center; margin:0 0 1.2rem; font-size:0.82rem; opacity:0.7; }
        .rc-combo-table { display:grid; gap:0.5rem; }
        .rc-combo-head, .rc-combo-row {
            display:grid; grid-template-columns:1.4fr 1fr 1fr; gap:0.5rem; align-items:stretch;
        }
        .rc-combo-head > div {
            font-size:0.68rem; text-transform:uppercase; letter-spacing:0.12em; font-weight:700;
            color:var(--text-on-theme-dim); text-align:center; padding:0.4rem;
        }
        .rc-combo-head > div:first-child { text-align:left; }
        .rc-combo-row > div {
            background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12);
            border-radius:0.85rem; padding:0.9rem 1rem; font-size:0.85rem;
        }
        .rc-combo-row > [role="rowheader"] { color:var(--text-on-dark); font-weight:600; }
        .rc-combo-row > [role="rowheader"] span {
            display:block; font-weight:400; font-size:0.72rem; color:var(--text-on-theme-dim); margin-top:0.25rem;
        }
        .rc-combo-yes, .rc-combo-no {
            text-align:center; display:flex; align-items:center; justify-content:center; font-weight:700;
        }
        .rc-combo-yes { color:#34d399; }
        .rc-combo-no { color:var(--text-on-theme-dim); font-weight:500; opacity:0.75; }
        .rc-combo-row.rc-combo-default > div { border-color:var(--gold-light); }
        @media (max-width:640px) {
            .rc-combo-head { display:none; }
            .rc-combo-head, .rc-combo-row { grid-template-columns:1fr; }
            .rc-combo-yes, .rc-combo-no { display:block; text-align:left; }
            .rc-combo-yes::before, .rc-combo-no::before {
                content: attr(data-label); display:block; font-size:0.65rem; text-transform:uppercase;
                letter-spacing:0.12em; color:var(--text-on-theme-dim); font-weight:600; margin-bottom:0.35rem;
            }
        }
"""

COMBO_HTML = """
            <div class="rc-combo-wrap" id="rcComboWrap">
                <h3 class="rc-combo-title">Possible combinations</h3>
                <p class="rc-combo-lead">Pick one. Weekly and On Demand cannot be combined.</p>
                <div class="rc-combo-table" role="table">
                    <div class="rc-combo-head" role="row">
                        <div role="columnheader">Cycle</div>
                        <div role="columnheader">80% Split</div>
                        <div role="columnheader">90% Split</div>
                    </div>
                    <div class="rc-combo-row" role="row">
                        <div role="rowheader">Weekly<span>every 7 calendar days · min $100</span></div>
                        <div class="rc-combo-yes" data-label="80% Split" role="cell">Add-on</div>
                        <div class="rc-combo-no" data-label="90% Split" role="cell">Not offered</div>
                    </div>
                    <div class="rc-combo-row rc-combo-default" role="row">
                        <div role="rowheader">Bi-Weekly<span>every 14 calendar days · min $100</span></div>
                        <div class="rc-combo-yes" data-label="80% Split" role="cell">Included</div>
                        <div class="rc-combo-no" data-label="90% Split" role="cell">Not offered</div>
                    </div>
                    <div class="rc-combo-row" role="row">
                        <div role="rowheader">On Demand<span>anytime · min 2% and $200</span></div>
                        <div class="rc-combo-no" data-label="80% Split" role="cell">Not offered</div>
                        <div class="rc-combo-yes" data-label="90% Split" role="cell">Add-on</div>
                    </div>
                </div>
            </div>
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
        r'(data-i18n="content.p7">)All reward request intervals are based on calendar days, not trading days\.[^<]*',
        r'\1All reward request intervals are based on calendar days, not trading days. Pick one combination. Weekly and On Demand cannot be combined.',
        html,
        count=1,
    )
    if ".rc-combo-wrap {" not in html:
        if "        .rc-detail-spacer { min-height:1.5em; }\n" in html:
            html = html.replace(
                "        .rc-detail-spacer { min-height:1.5em; }\n",
                "        .rc-detail-spacer { min-height:1.5em; }\n" + COMBO_CSS,
                1,
            )
        else:
            html = html.replace("</style>", COMBO_CSS + "\n    </style>", 1)
    if 'id="rcComboWrap"' not in html:
        m = re.search(
            r'<p style="text-align:center;font-size:0\.75rem;opacity:0\.6;margin-top:1\.8rem;" data-i18n="content\.p7">',
            html,
        )
        if not m:
            raise SystemExit("Reward-cycle footnote not found")
        html = html[:m.start()] + COMBO_HTML + html[m.start():]

    weekly_how = """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>"""
    weekly_how_new = """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                        <div class="rc-detail-row" data-rc-how="1"><span>How</span><span>Add-on</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card">
                    <div class="rc-period" data-i18n="content.rcBiWeekly">Bi-Weekly</div>"""
    if 'data-rc-how="1"' not in html:
        if weekly_how not in html:
            raise SystemExit("Weekly card details needle not found")
        html = html.replace(weekly_how, weekly_how_new, 1)
        html = html.replace(
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
                    </div>
                </div>
                <div class="reward-cycle-card rc-featured">""",
            """                        <div class="rc-detail-row"><span data-i18n="content.span18">Minimum Reward</span><span>$100</span></div>
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
                        <div class="rc-detail-row" data-rc-how="1"><span>How</span><span>Add-on</span></div>
                    </div>
                </div>
            </div>""",
            1,
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
