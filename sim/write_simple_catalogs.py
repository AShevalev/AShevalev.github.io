#!/usr/bin/env python3
"""Two simple PDFs: plans+rules, and prices+add-on costs."""

from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from write_addon_catalog import sku_rows
from write_price_rec_pdf import (
    H,
    MARGIN,
    NAVY,
    W,
    P,
    grid,
    styles as rec_styles,
    usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT_RULES = RESULTS / "Verodus_Plans_and_Rules_2026-08-17.pdf"
OUT_RULES_SHOP = RESULTS / "verodus-plans-and-rules-2026-08-17.pdf"
OUT_PRICES = RESULTS / "Verodus_Prices_and_Addons_2026-08-17.pdf"
OUT_PRICES_SHOP = RESULTS / "verodus-prices-and-addons-2026-08-17.pdf"

PAGE = landscape(A4)

RULES = (
    ("Instant Funding", "Funded (day 1)", "None",
     "5 valid", "20% best day", "3%", "6%", "Trailing HWM (never locks)"),
    ("One-Step", "Evaluation", "10%", "0", "50% best day",
     "4%", "6%", "Hybrid trail, locks at initial"),
    ("One-Step", "Funded", "None", "3", "None",
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


def write_pdf(path: Path, story, title: str, foot: str, shop: Path):
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
        "equity high. Max 6% trails the peak and never locks. First payout after 5 valid days "
        "(+0.5% of that day’s start-of-day equity), 20% best-day, $100 minimum. "
        "No fee refund. Default split 80% bi-weekly.",
        s["body"],
    ))
    story.append(P(
        "<b>One-Step.</b> One evaluation: 10% target, no min days, 50% best-day. "
        "4% daily, 6% hybrid max (locks at initial). Same drawdown on funded. "
        "First payout after 3 funded trading days. Challenge fee refunded on first payout "
        "(add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Lite.</b> Phase 1 8% / Phase 2 5%, 5 days each. 4% daily, "
        "8% static max on evaluation and funded. First payout after 3 funded trading days. "
        "Challenge fee refunded on first payout (add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Pro.</b> Phase 1 10% / Phase 2 5%, 5 days each. 5% daily, "
        "10% static max on evaluation and funded. First payout after 3 funded trading days. "
        "Challenge fee refunded on first payout (add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "Shared: unlimited time · 30-day inactivity · $100 minimum reward on every cycle · "
        "default Bi-Weekly 80% every 14 calendar days. Weekly 70% (+$27) and On Demand 90% (20% of list) are paid add-ons.",
        s["tiny"],
    ))
    write_pdf(
        OUT_RULES, story,
        "VERODUS  ·  Plans and rules",
        "News trading is permitted. Weekend holding is paid. Instant is not refundable.",
        OUT_RULES_SHOP,
    )


def build_prices():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Challenge prices", s["cover"]))
    story.append(P(
        "List = checkout basePrice. Sale = what the shopper pays with VERO35 (35% off). "
        "Instant $200k is not offered.",
        s["sub"],
    ))

    heads = ["Plan", "Size", "List", "Sale (VERO35)", "Discount"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Key"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]),
            P(f"${r['Size'] // 1000}k", s["td"]),
            P(usd(r["List"]), s["td"]),
            P(usd(r["Sale"]), s["td"]),
            P("35%", s["td"]),
        ])
    story.append(grid(data, [48 * mm, 28 * mm, 36 * mm, 40 * mm, 28 * mm], spec))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Door: Instant from $49 · 1-Step from $45 · Lite from $39 · Pro from $45. "
        "Green = Instant. Blue = evaluations.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("Add-on cost", s["cover"]))
    story.append(P(
        "Sticker = round(list × %). VERO35 takes 35% off list + stickers. "
        "News is permitted (no SKU). Swing is not sold.",
        s["sub"],
    ))

    pheads = ["Add-on", "Instant", "1-Step / Lite / Pro"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    menu = (
        ("News trading", "permitted", "permitted"),
        ("Weekend holding", "15%", "15%"),
        ("Weekly Rewards with 70% Reward Split", "+$27", "+$27"),
        ("On Demand Rewards with 90% Split", "20%", "20%"),
        ("Swing", "not offered", "not offered"),
    )
    pspec = {}
    for i, row in enumerate(menu, start=1):
        pspec[i] = "rec" if "Weekly" in row[0] or "On Demand" in row[0] else (
            "live" if row[0] in ("News trading", "Swing") else None
        )
        pdata.append([P(c, s["tdl"] if j == 0 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(pdata, [90 * mm, 45 * mm, 45 * mm], pspec))
    story.append(Spacer(1, 4 * mm))

    story.append(P("Stickers per challenge (before VERO35)", s["h1"]))
    heads = ["Plan", "Size", "List", "Weekend", "Weekly 70%", "On Demand 90%"]
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
        48 * mm, 22 * mm, 28 * mm, 32 * mm, 34 * mm, 38 * mm,
    ], spec))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Default is Bi-Weekly 80%. Weekly is +$27 on every size. On Demand 90% is 20% of list. "
        "Weekly and On Demand may stack. Shopper pays 65% of each sticker after VERO35.",
        s["tiny"],
    ))
    write_pdf(
        OUT_PRICES, story,
        "VERODUS  ·  Prices and add-on cost",
        "List = checkout basePrice. Sale = VERO35. Sticker = round(list × %).",
        OUT_PRICES_SHOP,
    )


def build():
    RESULTS.mkdir(exist_ok=True)
    build_rules()
    build_prices()


if __name__ == "__main__":
    build()
