#!/usr/bin/env python3
"""Stitch live Verodus plan-rule pages + rec payout / Instant copy.

Writes landing/instant.html, 1-step.html, 2-step-lite.html, 2-step-pro.html.
Chrome via <base href="https://www.verodus.com/">. Rebuild:
  python3 landing/stitch_plan_pages.py
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "landing"

PAGES = (
    ("instant", "https://www.verodus.com/instant.html"),
    ("1-step", "https://www.verodus.com/1-step.html"),
    ("2-step-lite", "https://www.verodus.com/2-step-lite.html"),
    ("2-step-pro", "https://www.verodus.com/2-step-pro.html"),
)

FREQ_ITEMS = """                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Bi-Weekly</strong> (Standard, included): 80% to trader, every 14 calendar days</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Weekly</strong> (Add-on): 80% to trader, every 7 calendar days. Cannot be combined with On Demand or 90%</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>On Demand</strong> (Add-on): 80% to trader, anytime after first eligibility. Cannot be combined with Weekly</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>90% Bi-Weekly</strong> (Add-on): 90% to trader, every 14 calendar days. Cannot be combined with Weekly</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>90% On Demand</strong> (Both add-ons): 90% to trader, anytime after first eligibility. Cannot be combined with Weekly. 90% Weekly is not offered</span></li>"""

SPLIT_ITEMS = """                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Default:</strong> 80/20 (trader/firm) on the Bi-Weekly cycle</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>90%:</strong> paid add-on. Bi-Weekly unless On Demand is also selected. Cannot be combined with Weekly</span></li>"""

REWARDS_INSTANT = """                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Minimum Reward:</strong> $100 (processed within 48 hours)</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>First eligibility:</strong> 5 valid trading days. A valid day is a calendar day whose closed-trade PnL is at least 0.5% of that day's start-of-day equity. Unrealized PnL does not count. The 20% Best Day rule still applies.</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Weekly (Add-on):</strong> Every 7 calendar days after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Bi-Weekly (Standard):</strong> Every 14 calendar days after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>On Demand (Add-on):</strong> Anytime after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Intervals:</strong> All reward request intervals are calendar days, not trading days</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Refund:</strong> Instant fees are not refundable</span></li>"""

REWARDS_EVAL = """                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Minimum Reward:</strong> $100 (processed within 48 hours)</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>First eligibility:</strong> 3 trading days in the funded (Qualified Performance) phase. A trading day is a calendar day with at least one closed trade</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Weekly (Add-on):</strong> Every 7 calendar days after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Bi-Weekly (Standard):</strong> Every 14 calendar days after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>On Demand (Add-on):</strong> Anytime after first eligibility</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>Intervals:</strong> All reward request intervals are calendar days, not trading days</span></li>
                        <li><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>100% Challenge Fee Refund:</strong> The original challenge fee is refunded with the first successful performance reward. Add-on fees are not refunded</span></li>"""


def fetch(url: str, slug: str) -> str:
    local = Path(f"/tmp/{slug}.html")
    try:
        html = urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "replace")
        local.write_text(html)
        return html
    except Exception:
        if local.exists():
            return local.read_text()
        raise


def _matching_ul_end(html: str, ul_open: int) -> int:
    """Return index of the </ul> that closes the ul that starts at ul_open."""
    pos = html.find(">", ul_open) + 1
    depth = 1
    while depth:
        nxt_open = html.find("<ul", pos)
        nxt_close = html.find("</ul>", pos)
        if nxt_close < 0:
            raise SystemExit("unmatched <ul>")
        if nxt_open >= 0 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 3
        else:
            depth -= 1
            if depth == 0:
                return nxt_close
            pos = nxt_close + 5
    raise SystemExit("unmatched <ul>")


def replace_list_under_title(html: str, title: str, items: str) -> str:
    marker = f"<strong>{title}</strong></p>"
    i = html.find(marker)
    if i < 0:
        raise SystemExit(f"{title!r}: title not found")
    ul_open = html.find('<ul class="rules-step-list">', i)
    if ul_open < 0 or ul_open - i > 200:
        raise SystemExit(f"{title!r}: list not found after title")
    ul_close = _matching_ul_end(html, ul_open)
    return (
        html[:ul_open]
        + '<ul class="rules-step-list">\n'
        + items
        + "\n                    </ul>"
        + html[ul_close + 5 :]
    )


def chrome(html: str) -> str:
    html = html.replace("\r\n", "\n")
    if '<base href="https://www.verodus.com/">' not in html:
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
        r"Last updated: (March|August) 2026",
        "Last updated: August 2026",
        html,
        count=1,
    )
    return html


def patch_shared(html: str, instant: bool) -> str:
    html = replace_list_under_title(
        html, "Payout Frequencies &amp; Trader Profit Share", FREQ_ITEMS
    )
    html = replace_list_under_title(html, "Performance Reward Split", SPLIT_ITEMS)
    html = replace_list_under_title(
        html, "Rewards &amp; Payouts", REWARDS_INSTANT if instant else REWARDS_EVAL
    )
    html = html.replace(
        "keep up to 90% of performance rewards under our sustainable trading rules.",
        "keep 80% of performance rewards (90% is a paid add-on) under our sustainable trading rules.",
        1,
    )
    html = html.replace(
        "earn performance rewards (up to 90% profit split) as soon as you meet the minimum activity requirements.",
        "earn performance rewards at an 80% split (90% is a paid add-on) as soon as you meet the minimum activity requirements.",
        1,
    )
    html = html.replace(
        "You receive a full refund of your original challenge fee with your first successful performance reward.",
        "The original challenge fee is refunded with the first successful performance reward. Add-on fees are not refunded.",
    )
    html = html.replace(
        "Challenge fees are non-refundable once trading activity has commenced. Serious violations may result in permanent blacklist and reporting to relevant authorities.",
        "Challenge fees are refunded only with the first successful performance reward (add-on fees are not refunded). Otherwise, fees are non-refundable once trading activity has commenced. Serious violations may result in permanent blacklist and reporting to relevant authorities.",
    )
    return html


def patch_instant(html: str) -> str:
    html = html.replace(
        "of the account balance (after commissions, swaps, spreads, and platform fees)",
        "of that day's start-of-day equity (after commissions, swaps, spreads, and platform fees)",
    )
    html = html.replace(
        "A trading day only counts if you close the day with a minimum net profit of <strong>0.5%</strong> of that day's start-of-day equity (after commissions, swaps, spreads, and platform fees).",
        "A trading day only counts if closed-trade PnL is at least <strong>0.5%</strong> of that day's start-of-day equity (after commissions, swaps, spreads, and platform fees).",
    )
    html = html.replace(
        "of at least <strong>0.5%</strong> of the account balance are counted as valid trading days",
        "of at least <strong>0.5%</strong> of that day's start-of-day equity are counted as valid trading days",
    )
    html = html.replace(
        "each with at least 0.5% net profit",
        "each with closed-trade PnL of at least 0.5% of that day's start-of-day equity",
    )
    html = html.replace(
        "each achieving at least +0.5% net profit",
        "each with closed-trade PnL of at least 0.5% of that day's start-of-day equity",
    )
    html = html.replace(
        "Valid Day Threshold: <strong>&ge;0.5% net profit</strong>",
        "Valid Day Threshold: <strong>&ge;0.5% of that day's start-of-day equity</strong>",
    )
    html = html.replace(
        "Days with less than +0.5% net profit do not count toward the minimum trading day requirement.",
        "Unrealized PnL does not count. Days below +0.5% of that day's start-of-day equity do not count toward the minimum trading day requirement.",
    )
    html = html.replace(
        "The limit trails upward as new equity highs are achieved.",
        "The limit trails upward as new equity highs are achieved. It never locks.",
    )
    html = html.replace(
        "The limit follows your highest equity peak and trails upward with new highs.",
        "The limit follows your highest equity peak and trails upward with new highs. It never locks.",
    )
    html = html.replace(
        "The <strong><span data-pct=\"6\">6%</span></strong> maximum drawdown is trailing from your account equity high water mark.",
        "The <strong><span data-pct=\"6\">6%</span></strong> maximum drawdown is trailing from your account equity high water mark and never locks.",
    )
    html = html.replace(
        "Instant Funding fees are <strong>non-refundable</strong> once trading activity has commenced.",
        "Instant Funding fees are <strong>not refundable</strong>.",
    )
    return html


FORBIDDEN = (
    "70% to trader",
    "can scale according to performance plan",
    "Scales to 85/15",
    "Scales to 90/10",
    "Net profit &gt; $200",
    "Net profit &gt; 2% of your account balance",
    "up to 90% of performance rewards",
    "up to 90% profit split",
    "48 business hours",
)

INSTANT_FORBIDDEN = (
    "of the account balance are counted as valid trading days",
    "of the account balance (after commissions",
    "each with at least 0.5% net profit",
    "At least 3 trading days have passed",
    "non-refundable</strong> once trading activity has commenced",
    "Challenge fees are refunded only with the first successful",
)


def verify(slug: str, html: str) -> None:
    misses = []
    for needle in (
        "90% Bi-Weekly",
        "90% On Demand",
        "Cannot be combined with Weekly",
        "paid add-on",
        "calendar days, not trading days",
    ):
        if needle not in html:
            misses.append(needle)
    leftover = [s for s in FORBIDDEN if s in html]
    if slug == "instant":
        leftover += [s for s in INSTANT_FORBIDDEN if s in html]
        for needle in (
            "never locks",
            "start-of-day equity",
            "not refundable",
            "5 valid trading days",
        ):
            if needle not in html:
                misses.append(needle)
    else:
        for needle in (
            "Add-on fees are not refunded",
            "3 trading days in the funded",
        ):
            if needle not in html:
                misses.append(needle)
    if misses or leftover:
        raise SystemExit(
            f"{slug}: missing {misses or '—'}; leftover {leftover or '—'}"
        )


def main() -> None:
    for slug, url in PAGES:
        html = chrome(fetch(url, slug))
        html = patch_shared(html, instant=(slug == "instant"))
        if slug == "instant":
            html = patch_instant(html)
        verify(slug, html)
        out = OUT_DIR / f"{slug}.html"
        out.write_text(html)
        print(f"Wrote {out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
