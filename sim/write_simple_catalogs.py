#!/usr/bin/env python3
"""Simple PDFs: plans+rules, pricing catalogue, add-on percentages."""

from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

from write_addon_catalog import PLAN_LABEL, sku_rows
from write_price_rec_pdf import (
    ANCHORS,
    H,
    MARGIN,
    NAVY,
    SIZES,
    W,
    P,
    grid,
    styles as rec_styles,
    usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")
OUT_RULES = RESULTS / "Verodus_Plans_and_Rules_2026-08-17.pdf"
OUT_RULES_SHOP = RESULTS / "verodus-plans-and-rules-2026-08-17.pdf"
OUT_PRICES = RESULTS / "Verodus_Prices_and_Addons_2026-08-17.pdf"
OUT_PRICES_SHOP = RESULTS / "verodus-prices-and-addons-2026-08-17.pdf"
OUT_CAT = RESULTS / "Verodus_Pricing_Catalogue_2026-08-17.pdf"
OUT_CAT_SHOP = RESULTS / "verodus-pricing-catalogue-2026-08-17.pdf"
OUT_ADDON = RESULTS / "Verodus_Addon_Percentages_2026-08-17.pdf"
OUT_ADDON_SHOP = RESULTS / "verodus-addon-percentages-2026-08-17.pdf"

PAGE = landscape(A4)

RULES = (
    ("Instant Funding", "Funded (day 1)", "None",
     "None", "20% best day (all green days)", "3%", "6%", "Trailing HWM (never locks)"),
    ("One-Step", "Evaluation", "10%", "0", "50% best day",
     "4%", "6%", "Hybrid trail, locks at initial"),
    ("One-Step", "Funded", "None", "0", "50% best day",
     "4%", "6%", "Hybrid trail, locks at initial"),
    ("Two-Step Lite", "Phase 1", "8%", "5", "None",
     "4%", "8%", "Static vs initial"),
    ("Two-Step Lite", "Phase 2", "5%", "5", "None",
     "4%", "8%", "Static vs initial"),
    ("Two-Step Lite", "Funded", "None", "3", "None",
     "4%", "8%", "Static vs initial"),
    ("Two-Step Pro", "Phase 1", "10%", "5", "None",
     "5%", "10%", "Static vs initial"),
    ("Two-Step Pro", "Phase 2", "5%", "5", "None",
     "5%", "10%", "Static vs initial"),
    ("Two-Step Pro", "Funded", "None", "3", "None",
     "5%", "10%", "Static vs initial"),
)

# Checkout row copy (desc) and ⓘ tooltip body. Modal title is the add-on name.
# Weekly / On Demand tooltips split Instant vs eval min-day lines.
ADDON_MENU = (
    (
        "News trading", "included", "included",
        "Not a checkout row. Included on every account.",
        "Not shown. News trading is permitted on evaluation and funded accounts.",
    ),
    (
        "Weekend Holding", "15%", "15%",
        "Hold positions over the weekend with zero restrictions.",
        "Exempts all open positions from the 22:00 UTC Friday liquidation rule so you may hold through the weekend on evaluation and funded accounts. Perfect for swing traders, position traders, and multi-day strategies.",
    ),
    (
        "Weekly Rewards with 70% Reward Split", "6%", "6%",
        "Withdraw your profit share weekly",
        "Receive your 70% reward share every week. Default is Bi-Weekly 80%. Minimum reward $100. Instant: Best Day ≤20% of every green day; a day meets the 0.5% parameter only if profit is more than 0.5% of start-of-day equity. 1-Step: no min trading days; Best Day ≤50%. 2-Step: 3 trading days.",
    ),
    (
        "On Demand Rewards with 90% Split", "32%", "15%",
        "Withdraw your profit share anytime — no waiting for fixed cycles",
        "Request your 90% reward share anytime after you meet that plan’s payout rule — no waiting for a 7- or 14-day cycle. Minimum reward $100. Instant: $100 and Best Day ≤20% of every green day; a day meets 0.5% only if profit is more than 0.5% of start-of-day equity. 1-Step: $100 and Best Day ≤50%; no min trading days. 2-Step: $100 and 3 trading days.",
    ),
    (
        "Bi-Weekly 80%", "included", "included",
        "Not a checkout add-on. Default reward cycle.",
        "Not shown as an add-on. Bi-Weekly 80% every 14 calendar days, min $100, is the default.",
    ),
    (
        "Swing", "not offered", "not offered",
        "Not a checkout row. Not offered.",
        "Not shown. News is already included. Do not sell a news+weekend bundle.",
    ),
)


def header(title: str, foot: str):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Bold", 8)
        canvas.drawString(MARGIN, H - 5.4 * mm, title)
        canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "17 Aug 2026")
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Roman", 7.5)
        canvas.drawString(MARGIN, 2.6 * mm, foot)
        canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
        canvas.restoreState()
    return _draw


def write_pdf(path: Path, story, title: str, foot: str, shop: Path, aliases=()):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title=title,
        author="Verodus",
    )
    doc.build(story, onFirstPage=header(title, foot), onLaterPages=header(title, foot))
    shutil.copyfile(path, shop)
    for dest in aliases:
        shutil.copyfile(path, dest)
    if ART.is_dir():
        shutil.copyfile(path, ART / path.name)
    print(f"Wrote {path} ({path.stat().st_size:,} bytes)")


def build_rules():
    s = rec_styles()
    story = []
    story.append(P("Plans and rules", s["cover"]))
    story.append(P(
        "Same percentage rules on every size in a plan. Instant has no $200k. "
        "News trading is permitted. Weekend holding is a paid add-on.",
        s["sub"],
    ))

    heads = ["Plan", "Stage", "Target", "Min days", "Consistency",
             "Daily DD", "Max DD", "Max drawdown basis"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(RULES, start=1):
        spec[i] = "rec" if row[0] == "Instant Funding" else "live"
        data.append([P(c, s["tdl"] if j < 2 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [
        32 * mm, 30 * mm, 28 * mm, 22 * mm, 28 * mm, 20 * mm, 20 * mm, 48 * mm,
    ], spec))
    story.append(Spacer(1, 4 * mm))

    story.append(P("What each plan is", s["h1"]))
    story.append(P(
        "<b>Instant Funding.</b> No evaluation. Funded on day one. Daily 3% from the day’s "
        "equity high. Max 6% trails the peak and never locks. One payout rule: $100 and "
        "Best Day ≤20% of every green day. A day meets the 0.5% parameter only if profit is more than 0.5% of that day’s start-of-day equity. "
        "The 20% cap cannot clear with fewer than five counted days — implied, not a second "
        "checkbox. Do not list “5 valid days.” No fee refund. Default split 80% bi-weekly.",
        s["body"],
    ))
    story.append(P(
        "<b>One-Step.</b> One evaluation: 10% target, no min days, 50% best-day. "
        "4% daily, 6% hybrid max (locks at initial). Same drawdown on funded. "
        "Qualified Performance: $100 and Best Day ≤50% (no 0.5% floor). Two equal green days "
        "can pass; that split is rare, so the clock is usually three days. Do not list a 3-day min. "
        "Challenge fee refunded on first payout (add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Lite.</b> Phase 1 8% / Phase 2 5%, 5 days each. 4% daily, "
        "8% static max on evaluation and funded. Every Qualified Performance payout needs 3 trading days. "
        "Challenge fee refunded on first payout (add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Pro.</b> Phase 1 10% / Phase 2 5%, 5 days each. 5% daily, "
        "10% static max on evaluation and funded. Every Qualified Performance payout needs 3 trading days. "
        "Challenge fee refunded on first payout (add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "Shared: unlimited time · 30-day inactivity · $100 minimum reward on every cycle · "
        "default Bi-Weekly 80% every 14 calendar days. Weekly 70% (6% of list) and On Demand 90% (32% Instant / 15% evals) are paid add-ons.",
        s["tiny"],
    ))
    write_pdf(
        OUT_RULES, story,
        "VERODUS  ·  Plans and rules",
        "News trading is permitted. Weekend holding is paid. Instant is not refundable.",
        OUT_RULES_SHOP,
    )


def price_grid(rows, s):
    heads = ["Plan", "Price", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    by = {(r["Key"], r["Size"]): r for r in rows}
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 0
    for plan, _fam in ANCHORS:
        for kind, field in (("Sale", "Sale"), ("List", "List")):
            i += 1
            spec[i] = "rec" if plan == "Instant" else "live"
            cells = [P(PLAN_LABEL[plan], s["tdl"]), P(kind, s["td"])]
            for sz in SIZES:
                r = by.get((plan, sz))
                if r is None:
                    cells.append(P("—", s["td"]))
                else:
                    cells.append(P(usd(r[field]), s["td"]))
            data.append(cells)
    return grid(data, [
        36 * mm, 18 * mm, 28 * mm, 28 * mm, 28 * mm, 28 * mm, 30 * mm, 30 * mm,
    ], spec)


def build_prices():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Pricing catalogue", s["cover"]))
    story.append(P(
        "Sale is what the shopper pays with VERO35 (35% off list). "
        "List is checkout basePrice. Instant has no $200k.",
        s["sub"],
    ))
    story.append(price_grid(rows, s))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Door: Instant from $49 · One-Step from $45 · Lite from $39 · Pro from $45. "
        "Green = Instant. Blue = evaluations. Coupon default VERO35.",
        s["tiny"],
    ))
    write_pdf(
        OUT_PRICES, story,
        "VERODUS  ·  Pricing catalogue",
        "Sale and list in separate rows. VERO35 35% off list. Instant has no $200k.",
        OUT_PRICES_SHOP,
        aliases=(OUT_CAT, OUT_CAT_SHOP),
    )


def addon_pct_table(s):
    heads = ["Add-on", "Instant", "1-Step / Lite / Pro", "Description", "Tooltip"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(ADDON_MENU, start=1):
        if row[0] in ("Weekend Holding", "Weekly Rewards with 70% Reward Split",
                      "On Demand Rewards with 90% Split"):
            spec[i] = "rec"
        elif row[0] in ("News trading", "Swing"):
            spec[i] = "live"
        data.append([
            P(row[0], s["tdl"]),
            P(row[1], s["td"]),
            P(row[2], s["td"]),
            P(row[3], s["tdl"]),
            P(row[4], s["tdl"]),
        ])
    return grid(data, [
        38 * mm, 18 * mm, 28 * mm, 52 * mm, 92 * mm,
    ], spec)


def build_addons():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Add-on percentages", s["cover"]))
    story.append(P(
        "Percent of list. Description is the checkout row. Tooltip is the ⓘ modal body "
        "(title is the add-on name). News and Bi-Weekly are not checkout add-on rows. "
        "Sticker = round(list × %). VERO35 takes 35% off list + stickers.",
        s["sub"],
    ))
    story.append(addon_pct_table(s))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Checkout Weekend 15% · Weekly 70% 6%. On Demand 90% is 32% Instant / 15% evals "
        "so Instant year-1 leftover prints. Weekly and On Demand may stack. "
        "Shopper pays 65% of each sticker after VERO35.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("Stickers per challenge (before VERO35)", s["h1"]))
    heads = ["Plan", "Size", "List", "Weekend 15%", "Weekly 70% 6%", "On Demand 90%"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Key"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]),
            P(f"${r['Size'] // 1000}k", s["td"]),
            P(usd(r["List"]), s["td"]),
            P(usd(r["weekend"]), s["td"]),
            P(usd(r["weekly"]), s["td"]),
            P(usd(r["od90"]), s["td"]),
        ])
    story.append(grid(data, [
        48 * mm, 22 * mm, 28 * mm, 32 * mm, 38 * mm, 42 * mm,
    ], spec))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Instant $100k list $675: weekend $101 · weekly $41 · On Demand 90% $216 (32%). "
        "Pro $100k list $537: weekend $81 · weekly $32 · On Demand 90% $81 (15%).",
        s["tiny"],
    ))
    write_pdf(
        OUT_ADDON, story,
        "VERODUS  ·  Add-on percentages",
        "Weekend 15% · Weekly 70% 6% · On Demand 90% 32% Instant / 15% evals. Sticker = round(list × %). VERO35 35% off.",
        OUT_ADDON_SHOP,
    )


def build():
    RESULTS.mkdir(exist_ok=True)
    build_rules()
    build_prices()
    build_addons()
    from write_be_margin_card import build as build_be
    build_be()


if __name__ == "__main__":
    build()
