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

ADDON_MENU = (
    ("News trading", "included", "included", "Allowed on eval and funded. No SKU."),
    ("Weekend Holding", "15%", "15%", "Friday 22:00 flatten off."),
    ("Weekly Rewards with 70% Reward Split", "6%", "6%",
     "Every 7 calendar days. Default is Bi-Weekly 80%. Min $100."),
    ("On Demand Rewards with 90% Split", "20%", "20%",
     "Anytime after Instant 5 valid days or eval 3 funded days. Min $100."),
    ("Bi-Weekly 80%", "included", "included",
     "Default. Every 14 calendar days. Min $100."),
    ("Swing", "not offered", "not offered", "News is already in the fee."),
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
        "default Bi-Weekly 80% every 14 calendar days. Weekly 70% (6% of list) and On Demand 90% (20% of list) are paid add-ons.",
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
    heads = ["Add-on", "Instant", "1-Step / Lite / Pro", "What it is"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(ADDON_MENU, start=1):
        if row[0] in ("Weekend Holding", "Weekly Rewards with 70% Reward Split",
                      "On Demand Rewards with 90% Split"):
            spec[i] = "rec"
        elif row[0] in ("News trading", "Swing"):
            spec[i] = "live"
        data.append([P(c, s["tdl"] if j in (0, 3) else s["td"]) for j, c in enumerate(row)])
    return grid(data, [62 * mm, 28 * mm, 38 * mm, 100 * mm], spec)


def build_addons():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Add-on percentages", s["cover"]))
    story.append(P(
        "Percent of list. Sticker = round(list × %). VERO35 takes 35% off list + stickers. "
        "News is included (no SKU). Swing is not sold. Default reward is Bi-Weekly 80%.",
        s["sub"],
    ))
    story.append(addon_pct_table(s))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Checkout card. Weekend 15% · Weekly 70% 6% · On Demand 90% 20%. "
        "Weekly and On Demand may stack. Shopper pays 65% of each sticker after VERO35.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("Stickers per challenge (before VERO35)", s["h1"]))
    heads = ["Plan", "Size", "List", "Weekend 15%", "Weekly 70% 6%", "On Demand 90% 20%"]
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
        "Instant $100k list $675: weekend $101 · weekly $41 · On Demand 90% $135. "
        "Pro $100k list $537: weekend $81 · weekly $32 · On Demand 90% $107.",
        s["tiny"],
    ))
    write_pdf(
        OUT_ADDON, story,
        "VERODUS  ·  Add-on percentages",
        "Weekend 15% · Weekly 70% 6% · On Demand 90% 20%. Sticker = round(list × %). VERO35 35% off.",
        OUT_ADDON_SHOP,
    )


def build():
    RESULTS.mkdir(exist_ok=True)
    build_rules()
    build_prices()
    build_addons()


if __name__ == "__main__":
    build()
