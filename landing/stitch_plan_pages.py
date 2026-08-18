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

def _rstep(label: str, body: str) -> str:
    return (
        '                        <li><span class="rules-step-num">&bull;</span>'
        f'<span class="rstep-inline"><strong>{label}:</strong> {body}</span></li>'
    )


# Instant frequencies use live Instant headings.
FREQ_ITEMS_INSTANT = "\n".join(
    [
        '                        <li><span class="rules-step-num">&bull;</span>'
        '<span class="rstep-inline"><strong>Weekly</strong> (Selected Add-on): 70% to trader</span></li>',
        '                        <li><span class="rules-step-num">&bull;</span>'
        '<span class="rstep-inline"><strong>Bi-Weekly</strong> (Default): 80% to trader</span></li>',
        '                        <li><span class="rules-step-num">&bull;</span>'
        '<span class="rstep-inline"><strong>On-Demand</strong> (Selected Add-on): 90% to trader</span></li>',
        '                        <li><span class="rules-step-num">&bull;</span>'
        '<span class="rstep-inline">Weekly and On-Demand are separate add-ons; they cannot both apply at once.</span></li>',
    ]
)

FREQ_ITEMS = "\n".join(
    [
        _rstep(
            "Bi-Weekly (Standard, included)",
            "80% to trader, every 14 calendar days.",
        ),
        _rstep(
            "Weekly Rewards with 70% Reward Split (Add-on)",
            "70% to trader, every 7 calendar days.",
        ),
        _rstep(
            "On Demand Rewards with 90% Split (Add-on)",
            "90% to trader. No 7- or 14-day wait.",
        ),
    ]
)

# Do not repeat Weekly / Bi-Weekly / On-Demand clocks here.
SPLIT_ITEMS = "\n".join(
    [
        _rstep("Default", "80% on the included Bi-Weekly cycle."),
        _rstep(
            "Add-ons",
            "Weekly and On-Demand are separate add-ons; they cannot both apply at once.",
        ),
    ]
)

REWARDS_INSTANT = "\n".join(
    [
        _rstep("Minimum Reward", "$100 (processed within 48 hours)"),
        _rstep(
            "Eligibility",
            "You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.",
        ),
        _rstep(
            "Weekly (Add-on)",
            "7 calendar days and when eligibility requirements are met.",
        ),
        _rstep(
            "Bi-Weekly (Standard)",
            "14 calendar days and when eligibility requirements are met.",
        ),
        _rstep(
            "On-Demand (Add-on)",
            "Available when eligibility requirements are met.",
        ),
        _rstep("Fees", "Instant fees are not refundable."),
    ]
)

REWARDS_1STEP = "\n".join(
    [
        _rstep("Minimum Reward", "$100 (processed within 48 hours)"),
        _rstep(
            "Eligibility",
            "You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.",
        ),
        _rstep(
            "Weekly (Add-on)",
            "7 calendar days and when eligibility requirements are met.",
        ),
        _rstep(
            "Bi-Weekly (Standard)",
            "14 calendar days and when eligibility requirements are met.",
        ),
        _rstep(
            "On-Demand (Add-on)",
            "Available when eligibility requirements are met.",
        ),
        _rstep(
            "Intervals",
            "All reward request intervals are calendar days, not trading days",
        ),
        _rstep(
            "100% Challenge Fee Refund",
            "The original challenge fee is refunded with the first successful performance reward. Add-on fees are not refunded",
        ),
    ]
)

REWARDS_2STEP = "\n".join(
    [
        _rstep("Minimum Reward", "$100 (processed within 48 hours)"),
        _rstep(
            "Eligibility",
            "You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. The first payout and every payout after use this same rule. A trading day is a calendar day with at least one closed trade.",
        ),
        _rstep(
            "Weekly (Add-on)",
            "7 calendar days, and 3 trading days.",
        ),
        _rstep(
            "Bi-Weekly (Standard)",
            "14 calendar days, and 3 trading days.",
        ),
        _rstep(
            "On-Demand (Add-on)",
            "Available when eligibility requirements are met.",
        ),
        _rstep(
            "Intervals",
            "All reward request intervals are calendar days, not trading days",
        ),
        _rstep(
            "100% Challenge Fee Refund",
            "The original challenge fee is refunded with the first successful performance reward. Add-on fees are not refunded",
        ),
    ]
)


def rewards_for(slug: str) -> str:
    if slug == "instant":
        return REWARDS_INSTANT
    if slug == "1-step":
        return REWARDS_1STEP
    return REWARDS_2STEP


def fetch(url: str, slug: str) -> str:
    local = Path(f"/tmp/{slug}.html")
    landing = OUT_DIR / f"{slug}.html"
    try:
        html = urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "replace")
        local.write_text(html)
        return html
    except Exception:
        if local.exists():
            return local.read_text()
        if landing.exists():
            return landing.read_text()
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


def replace_list_under_title(html: str, title: str, items: str, *, required: bool = True) -> str:
    marker = f"<strong>{title}</strong></p>"
    i = html.find(marker)
    if i < 0:
        if required:
            raise SystemExit(f"{title!r}: title not found")
        return html
    ul_open = html.find('<ul class="rules-step-list">', i)
    if ul_open < 0 or ul_open - i > 200:
        if required:
            raise SystemExit(f"{title!r}: list not found after title")
        return html
    ul_close = _matching_ul_end(html, ul_open)
    return (
        html[:ul_open]
        + '<ul class="rules-step-list">\n'
        + items
        + "\n                    </ul>"
        + html[ul_close + 5 :]
    )


def drop_card_under_title(html: str, title: str) -> str:
    marker = f"<strong>{title}</strong></p>"
    i = html.find(marker)
    if i < 0:
        return html
    card_open = html.rfind('<div class="rules-card"', 0, i)
    if card_open < 0:
        return html
    ul_open = html.find('<ul class="rules-step-list">', i)
    if ul_open < 0:
        return html
    ul_close = _matching_ul_end(html, ul_open)
    card_end = html.find("</div>", ul_close)
    if card_end < 0:
        return html
    card_end += len("</div>")
    return html[:card_open].rstrip() + html[card_end:]


def drop_every_payout_card(html: str) -> str:
    return re.sub(
        r'\s*<div class="rules-card"[^>]*>\s*<ul class="rules-step-list">\s*'
        r'<li[^>]*>\s*<span class="rules-step-num">&bull;</span>'
        r'<div><strong>Every Payout:</strong>.*?</ul>\s*</div>',
        "",
        html,
        count=1,
        flags=re.S,
    )


def ensure_split_card(html: str) -> str:
    if "<strong>Performance Reward Split</strong></p>" in html:
        return html
    marker = "<strong>Payout Frequencies &amp; Trader Profit Share</strong></p>"
    i = html.find(marker)
    if i < 0:
        raise SystemExit("Payout Frequencies title not found; cannot insert split card")
    ul_open = html.find('<ul class="rules-step-list">', i)
    if ul_open < 0:
        raise SystemExit("Payout Frequencies list not found")
    ul_close = _matching_ul_end(html, ul_open)
    card_end = html.find("</div>", ul_close)
    if card_end < 0:
        raise SystemExit("Payout Frequencies card end not found")
    card_end += len("</div>")
    split_card = (
        '\n                <div class="rules-card" style="margin-top:1.25rem;">\n'
        '                    <p data-i18n-html="content.p10" style="margin-bottom:1.25rem;">'
        "<strong>Performance Reward Split</strong></p>\n"
        '                    <ul class="rules-step-list">\n'
        + SPLIT_ITEMS
        + "\n                    </ul>\n"
        "                </div>"
    )
    return html[:card_end] + split_card + html[card_end:]


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


def patch_shared(html: str, slug: str) -> str:
    freq = FREQ_ITEMS_INSTANT if slug == "instant" else FREQ_ITEMS
    html = replace_list_under_title(
        html, "Payout Frequencies &amp; Trader Profit Share", freq
    )
    if slug == "instant":
        html = drop_card_under_title(html, "Performance Reward Split")
    else:
        html = ensure_split_card(html)
        html = replace_list_under_title(html, "Performance Reward Split", SPLIT_ITEMS)
    html = replace_list_under_title(html, "Rewards &amp; Payouts", rewards_for(slug))
    html = html.replace("Allowed in Evaluation:", "Allowed:")
    html = html.replace("48 business hours", "48 hours")
    for old, new in (
        ("every green day", "every profitable day"),
        ("Every green day", "Every profitable day"),
        ("small green days", "small profitable days"),
        ("green days", "profitable days"),
        ("green day", "profitable day"),
    ):
        html = html.replace(old, new)
    html = html.replace(
        "cannot exceed 50% of Positive Days' Profit from every profitable day.",
        "cannot exceed 50% of your total Positive Days' Profit.",
    )
    html = html.replace(
        " of Positive Days' Profit from every profitable day",
        " of Positive Days' Profit",
    )
    html = html.replace(" from every profitable day", "")
    html = html.replace(" of every profitable day", " of Positive Days' Profit")
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
    html = patch_news(html)
    return html


def patch_news(html: str) -> str:
    """News is included on every phase and funded account. Not an add-on."""
    html = re.sub(
        r'(<strong>News Trading:</strong><span>)Full details on News Trading restrictions.*?</span>',
        r'\1News trading is permitted. There is no News Trading add-on and no restricted news window.</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        "Full news trading (subject to restrictions), Expert Advisors",
        "News trading is permitted. Expert Advisors",
    )
    html = html.replace(
        "Full news trading, Expert Advisors",
        "News trading is permitted. Expert Advisors",
    )
    html = re.sub(
        r'\s*<li[^>]*>\s*<strong>News Trading Addon:</strong>.*?</li>',
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'\s*<li[^>]*>\s*<strong>News Trading \(Tiered Breach Model.*?</ul>\s*</li>',
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        "Removal of conflicting trades and profits from your history (standard for first News Trading violation)",
        "Removal of conflicting trades and profits from your history",
    )
    html = html.replace(
        "Complete termination of your Qualified Performance account (standard for second News Trading violation or System Exploitation)",
        "Complete termination of your Qualified Performance account (standard for System Exploitation)",
    )
    return html


def patch_instant(html: str) -> str:
    html = drop_every_payout_card(html)
    html = html.replace(
        "20% Best Day rule, and 5 minimum valid trading days (each requiring at least 0.5% net profit).",
        "20% Best Day rule. Instant has no minimum trading days.",
    )
    html = html.replace(
        "It includes a <strong>20% Best Day consistency rule</strong> and requires a <strong>minimum of 5 valid trading days</strong>, where each day must achieve at least <strong>0.5% net profit</strong> to count.",
        "It includes a <strong>20% Best Day consistency rule</strong>. Instant has <strong>no minimum trading days</strong>.",
    )
    html = html.replace(
        '<div><div class="phase-stat-lbl">Minimum Trading Days</div><div class="phase-stat-val">5</div></div>',
        '<div><div class="phase-stat-lbl">Minimum Trading Days</div><div class="phase-stat-val">None</div></div>',
    )
    html = html.replace(
        "Valid Day Threshold: <strong>&ge;0.5% net profit</strong>",
        "Payout rule: <strong>$100 + 20% Best Day</strong>",
    )
    html = html.replace(
        "Valid Day Threshold: <strong>&ge;0.5% of that day's start-of-day equity</strong>",
        "Payout rule: <strong>$100 + 20% Best Day</strong>",
    )
    html = html.replace(
        '<li data-i18n-html="content.li4"><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>5</strong> Minimum valid trading days (each with closed-trade PnL of at least 0.5% of that day\'s start-of-day equity)</span></li>',
        '<li data-i18n-html="content.li4"><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>No minimum trading days</strong></span></li>',
    )
    html = html.replace(
        '<li data-i18n-html="content.li4"><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>5</strong> Minimum valid trading days (each with at least 0.5% net profit)</span></li>',
        '<li data-i18n-html="content.li4"><span class="rules-step-num">&bull;</span><span class="rstep-inline"><strong>No minimum trading days</strong></span></li>',
    )
    html = html.replace(
        "as soon as you meet the minimum activity requirements.",
        "as soon as you meet that payout's qualifying parameters.",
    )
    html = html.replace(
        '<li data-i18n-html="content.li9"><span class="rules-step-num">&bull;</span><div><strong>Valid Trading Day Definition:</strong><span>A trading day only counts if closed-trade PnL is at least <strong>0.5%</strong> of that day\'s start-of-day equity (after commissions, swaps, spreads, and platform fees). Unrealized PnL does not count. Days below +0.5% of that day\'s start-of-day equity do not count toward the minimum trading day requirement.</span></div></li>',
        '<li data-i18n-html="content.li9"><span class="rules-step-num">&bull;</span><div><strong>No Minimum Trading Days:</strong><span>Instant has no minimum trading days. Every payout needs $100, Best Day ≤20% of Positive Days\' Profit, and the selected cycle.</span></div></li>',
    )
    html = html.replace(
        '<li data-i18n-html="content.li9"><span class="rules-step-num">&bull;</span><div><strong>Valid Trading Day Definition:</strong><span>A trading day only counts if you close the day with a minimum net profit of <strong>0.5%</strong> of that day\'s start-of-day equity (after commissions, swaps, spreads, and platform fees). Unrealized PnL does not count. Days with less than +0.5% net profit do not count toward the minimum trading day requirement.</span></div></li>',
        '<li data-i18n-html="content.li9"><span class="rules-step-num">&bull;</span><div><strong>No Minimum Trading Days:</strong><span>Instant has no minimum trading days. Every payout needs $100, Best Day ≤20% of Positive Days\' Profit, and the selected cycle.</span></div></li>',
    )
    html = html.replace(
        "You must complete a minimum of <strong>5 valid trading days</strong> (each with closed-trade PnL of at least 0.5% of that day's start-of-day equity) before you become eligible for your first performance reward.",
        "Instant has no minimum trading days. The first payout and every payout after use the same rule: $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle.",
    )
    html = html.replace(
        "You must complete a minimum of <strong>5 valid trading days</strong> (each achieving at least +0.5% net profit) before you become eligible for your first performance reward.",
        "Instant has no minimum trading days. The first payout and every payout after use the same rule: $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle.",
    )
    html = html.replace(
        '<strong>0.5% Minimum Profit to Count as a Trading Day:</strong><span>Only days where you achieve a net closed-trade profit of at least <strong>0.5%</strong> of that day\'s start-of-day equity are counted as valid trading days toward the minimum requirement of 5 days.</span>',
        "<strong>No Minimum Trading Days:</strong><span>Instant has no minimum trading days. Every payout needs $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle.</span>",
    )
    html = html.replace(
        '<div><div class="phase-stat-lbl">Minimum Trading Days</div><div class="phase-stat-val">N/A</div></div>',
        '<div><div class="phase-stat-lbl">Minimum Trading Days</div><div class="phase-stat-val">None</div></div>',
    )
    html = html.replace(
        "Minimum Trading Days: <strong>N/A</strong>",
        "Minimum Trading Days: <strong>None</strong>",
    )
    html = html.replace(
        '<span data-i18n-html="content.span3">Minimum Trading Days: <strong>None</strong></span>',
        "",
    )
    html = re.sub(
        r'\s*<li[^>]*>\s*<span class="rules-step-num">&bull;</span><div><strong>Minimum Trading Days:</strong><span>No minimum trading days\.</span></div></li>',
        "",
        html,
        count=1,
    )
    html = html.replace(
        " of Positive Days' Profit from every profitable day",
        " of Positive Days' Profit",
    )
    html = html.replace(" from every profitable day", "")
    html = html.replace(" of every profitable day", " of Positive Days' Profit")
    # Instant Best Day = live 1-Step wording, Instant-applicable only (20%; payout request).
    html = html.replace(
        "Your single best qualifying profit day cannot account for more than 20% of Positive Days’ Profit at the time you request a payout. A day counts only when closed profit is at least 0.5% of that day’s start-of-day equity. Smaller green days do not count toward Best Day or Positive Days’ Profit.",
        "Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.",
    )
    html = html.replace(
        "Your single best qualifying profit day cannot account for more than 20% of Positive Days’ Profit at the time you request a payout. A day counts only when closed profit is at least 0.5% of that day’s start-of-day equity. Smaller profitable days do not count toward Best Day or Positive Days’ Profit.",
        "Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.",
    )
    html = html.replace(
        "Your Best Day (highest profit calendar day) must not exceed 20% of Positive Days' Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days' Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 20% is not a breach — continue trading until Best Day is ≤20%.",
        "Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.",
    )
    html = html.replace(
        "Best Day must be ≤20% of Positive Days' Profit (qualifying days only).",
        "No single trading day can contribute more than 20% of your total Positive Days' Profit at the time you request a payout.",
    )
    html = html.replace(
        "Best Day must be ≤20% of Positive Days' Profit. All Positive Days count.",
        "No single trading day can contribute more than 20% of your total Positive Days' Profit at the time you request a payout.",
    )
    html = html.replace(
        "Exceeding 20% on a single day does not immediately terminate your account — you must continue trading to grow your total Positive Days' Profit until the best day drops to 20% or below.",
        "Exceeding 20% on a single day does not immediately fail your account — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤20%.",
    )
    html = html.replace(
        "<strong>Not a Breach:</strong><span>Exceeding 20% is not a breach — continue trading until Best Day is ≤20%.</span>",
        "<strong>Not a Breach:</strong><span>Exceeding 20% on a single day does not immediately fail your account — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤20%.</span>",
    )
    html = html.replace(
        "Closed trades only, at 00:00 UTC. Losing days do not count. Days under the 0.5% start-of-day equity floor do not count. Example ($100,000 start-of-day equity): the floor for that day is $500 closed profit. +$400 does not qualify. +$600 does. If the largest qualifying day is $10,000, Positive Days’ Profit must be at least $50,000 before you can request a payout.",
        "Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.",
    )
    html = html.replace(
        "<strong>Calculation:</strong><span>Profits are calculated from closed trades at 00:00 UTC. Losing days do not count toward Positive Days' Profit.</span>",
        "<strong>Calculation:</strong><span>Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.</span>",
    )
    html = html.replace(
        '<strong>Every Payout:</strong><span>Minimum $100, Best Day ≤20% of every green day, and the selected cycle. Instant has no minimum trading days. The first payout and every payout after use this same rule. Processed within 48 hours.</span>',
        "<strong>Every Payout:</strong><span>Minimum $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle. No minimum trading days required. The same rule applies to every payout. Processed within 48 hours.</span>",
    )
    html = html.replace(
        '<strong>Every Payout:</strong><span>Minimum $100, Best Day ≤20% of every green day, and the selected cycle. Instant has no minimum trading days. The first payout and every payout after use this same rule. Processed within 48 business hours.</span>',
        "<strong>Every Payout:</strong><span>Minimum $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle. No minimum trading days required. The same rule applies to every payout. Processed within 48 hours.</span>",
    )
    for old, new in (
        ("every green day", "every profitable day"),
        ("Every green day", "Every profitable day"),
        ("small green days", "small profitable days"),
        ("green days", "profitable days"),
        ("green day", "profitable day"),
    ):
        html = html.replace(old, new)
    html = html.replace(
        "A day meets the 0.5% parameter only if it closes at least 0.5% profit of account balance. ",
        "",
    )
    html = html.replace(
        "A day meets the 0.5% parameter only if it closes at least 0.5% profit of account balance.",
        "",
    )
    LIVE_1STEP_INSTANT_MODAL = (
        'does not exceed <strong class="hl">20%</strong> of your Positive Days\' Profit on the account. '
        "Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). "
        "Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit."
    )
    html = html.replace(
        "does not exceed <strong class=\"hl\">20%</strong> of your Positive Days' Profit at the time you request a payout. Every profitable day is factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit.",
        LIVE_1STEP_INSTANT_MODAL,
    )
    html = html.replace(
        "does not exceed <strong class=\"hl\">20%</strong> of your Positive Days' Profit at the time you request a payout. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit.",
        LIVE_1STEP_INSTANT_MODAL,
    )
    html = html.replace(
        "does not exceed <strong class=\"hl\">20%</strong> of Positive Days' Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days' Profit. Losing days do not count toward Positive Days' Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 20% is not a breach — continue trading until Best Day is ≤20%.",
        LIVE_1STEP_INSTANT_MODAL,
    )
    html = html.replace(
        "Small profitable days still count toward Positive Days' Profit. Small profitable days still count toward Positive Days' Profit.",
        "Small profitable days still count toward Positive Days' Profit.",
    )
    # Live Instant modal still has the 0.5% qualifying-day filter.
    html = re.sub(
        r'The Best Day Rule requires that your most profitable <strong>qualifying</strong> day \(&quot;Best Day&quot;\) does not exceed <strong class="hl">20%</strong>.*?(?=</p>)',
        "The Best Day Rule requires that your most profitable day (&quot;Best Day&quot;) "
        + LIVE_1STEP_INSTANT_MODAL,
        html,
        count=1,
        flags=re.S,
    )
    if "never locks" not in html:
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
    html = html.replace(
        "A Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). Valid Day is not a minimum trading-day count and does not remove small Positive Days from Positive Days' Profit. ",
        "",
    )
    html = html.replace(
        "A Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). ",
        "",
    )
    html = html.replace(
        "Every profitable day is factored in, including small chip days.",
        "Profitable days are factored into Positive Days' Profit.",
    )
    html = html.replace(
        "20% Best Day of qualifying days (closed profit ≥ 0.5% of that day’s start-of-day equity). No minimum trading days.",
        "20% Best Day rule, and no minimum trading days.",
    )
    html = html.replace(
        "20% Best Day of qualifying days (closed profit ≥ 0.5% of that day's start-of-day equity). No minimum trading days.",
        "20% Best Day rule, and no minimum trading days.",
    )
    return html


def patch_1step(html: str) -> str:
    # Keep live 1-Step Best Day / Eligibility wording. Drop Instant from 1-Step.
    html = html.replace(" (Instant uses 20%)", "")
    html = html.replace(
        "plus the 50% Best Day consistency rule unique to 1-Step.",
        "plus the 50% Best Day rule.",
    )
    html = html.replace(
        "See Section 3. Instant also trails, but Instant never locks.",
        "Unique to this plan; see Section 3.",
    )
    html = html.replace(
        "<strong>50% Best Day Rule (Instant uses 20%)",
        "<strong>50% Best Day Rule",
    )
    html = html.replace(
        "<strong>50% Best Day Rule — unique to 1-Step",
        "<strong>50% Best Day Rule",
    )
    html = html.replace(
        "50% Best Day rule (Instant uses 20%) — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.",
        "50% Best Day rule — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.",
    )
    html = html.replace(
        "Unique to 1-Step — your single best profit day cannot exceed 50% of your total Positive Days' Profit. See Section 3 for full details.",
        "50% Best Day rule — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.",
    )
    html = html.replace(
        "Best Day must be ≤50% of Positive Days' Profit. All Positive Days count. See Section 3 for full details.",
        "50% Best Day rule — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.",
    )
    html = html.replace(
        "Your Best Day (highest profit calendar day) must not exceed 50% of Positive Days' Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days' Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 50% is not a breach — continue trading until Best Day is ≤50%.",
        "Your single best profit day cannot account for more than 50% of your Positive Days' Profit at the time of passing the evaluation. This is not an immediate breach — you must continue trading until the condition is met.",
    )
    html = html.replace(
        "Best Day must be ≤50% of Positive Days' Profit. All Positive Days count.",
        "No single trading day can contribute more than 50% of your total Positive Days' Profit at the point you hit the 10% target.",
    )
    html = html.replace(
        "<strong>Not a Breach:</strong><span>Exceeding 50% is not a breach — continue trading until Best Day is ≤50%.</span>",
        "<strong>Not a Breach:</strong><span>Exceeding 50% on a single day does not immediately fail your evaluation — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤50%.</span>",
    )
    html = html.replace(
        "<strong>Calculation:</strong><span>Profits are calculated from closed trades at 00:00 UTC. Losing days do not count toward Positive Days' Profit.</span>",
        "<strong>Calculation:</strong><span>Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.</span>",
    )
    html = html.replace(
        "does not exceed <strong class=\"hl\">50%</strong> of Positive Days' Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days' Profit. Losing days do not count toward Positive Days' Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 50% is not a breach — continue trading until Best Day is ≤50%.",
        "does not exceed <strong class=\"hl\">50%</strong> of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤50% of total Positive Days' Profit.",
    )
    return html


FORBIDDEN = (
    "can scale according to performance plan",
    "Scales to 85/15",
    "Scales to 90/10",
    "Net profit &gt; $200",
    "Net profit &gt; 2% of your account balance",
    "up to 90% of performance rewards",
    "up to 90% profit split",
    "48 business hours",
    "News Trading Addon",
    "Tiered Breach Model",
    "2-minute restricted",
    "may be purchased together",
)

INSTANT_FORBIDDEN = (
    "of the account balance are counted as valid trading days",
    "of the account balance (after commissions",
    "each with at least 0.5% net profit",
    "At least 3 trading days have passed",
    "non-refundable</strong> once trading activity has commenced",
    "Challenge fees are refunded only with the first successful",
    "5 valid trading days",
    "5 valid days",
    "minimum of 5 valid",
    "Minimum Trading Days:</strong><span>No minimum trading days",
    "green day",
    "0.5% parameter",
    "Valid Day",
    "at least 0.5% profit",
    "qualifying days only",
    "qualifying days",
    "Days below this floor",
    "Every Payout:",
    "4. Qualified Performance Phase",
    "Performance Reward Split",
    "<strong>Intervals:</strong>",
    "<strong>Refund:</strong>",
)

SHARED_FORBIDDEN = (
    "first eligibility",
    "does not skip the trading-day",
    "for that evaluation",
    "green day",
)


def verify(slug: str, html: str) -> None:
    misses = []
    shared = [
        "News trading is permitted",
        "Minimum Reward:</strong> $100",
    ]
    if slug != "instant":
        shared += [
            "Weekly Rewards with 70% Reward Split",
            "On Demand Rewards with 90% Split",
            "calendar days, not trading days",
        ]
    for needle in shared:
        if needle not in html:
            misses.append(needle)
    leftover = [s for s in FORBIDDEN if s in html]
    leftover += [s for s in SHARED_FORBIDDEN if s in html]
    on_demand_cycle = html.count("On-Demand (Add-on)")
    if on_demand_cycle != 1:
        leftover.append(f"On-Demand (Add-on) count={on_demand_cycle}")
    if slug == "instant":
        leftover += [s for s in INSTANT_FORBIDDEN if s in html]
        for needle in (
            "never locks",
            "not refundable",
            "Instant has no minimum trading days",
            "your Best Day is ≤20% of Positive Days",
            "Your single best profit day cannot account for more than 20%",
            "Profitable days are factored into Positive Days' Profit",
            "at the time you request a payout",
            "4. Payouts and risk limits",
            "<strong>Weekly</strong> (Selected Add-on)",
            "<strong>Fees:</strong>",
            "7 calendar days and when eligibility requirements are met",
            "14 calendar days and when eligibility requirements are met",
            "Available when eligibility requirements are met",
        ):
            if needle not in html:
                misses.append(needle)
    elif slug == "1-step":
        leftover += [
            s
            for s in (
                "3 trading days in the funded",
                "0.5% profit",
                "5 valid",
                "Instant uses 20%",
                "Instant also trails",
            )
            if s in html
        ]
        for needle in (
            "Add-on fees are not refunded",
            "1-Step has no minimum trading days",
            "Your single best profit day cannot account for more than 50%",
            "Profitable days are factored into Positive Days' Profit",
            "at the time of passing the evaluation",
            "7 calendar days and when eligibility requirements are met",
            "14 calendar days and when eligibility requirements are met",
            "Available when eligibility requirements are met",
        ):
            if needle not in html:
                misses.append(needle)
    else:
        leftover += [
            s
            for s in (
                "Best Day ≤20%",
                "0.5% profit",
                "no minimum trading days",
            )
            if s in html
        ]
        for needle in (
            "Add-on fees are not refunded",
            "Available when eligibility requirements are met",
            "7 calendar days, and 3 trading days",
            "14 calendar days, and 3 trading days",
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
        html = patch_shared(html, slug)
        if slug == "instant":
            html = patch_instant(html)
        elif slug == "1-step":
            html = patch_1step(html)
        verify(slug, html)
        out = OUT_DIR / f"{slug}.html"
        out.write_text(html)
        print(f"Wrote {out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
