#!/usr/bin/env python3
"""Shopper add-on catalog: % of list and stickers per challenge SKU."""

from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from write_price_rec_pdf import (
    ANCHORS,
    H,
    MARGIN,
    NAVY,
    REC,
    SIZES,
    W,
    P,
    grid,
    rec_list,
    styles as rec_styles,
    usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Addon_Catalog_2026-08-17.pdf"
OUT_SHOP = RESULTS / "verodus-addon-catalog-2026-08-17.pdf"
MD = RESULTS / "ADDON_CATALOG.md"

PAGE = landscape(A4)

PLAN_LABEL = {
    "Instant": "Instant Funding",
    "1-Step": "One-Step",
    "2-Step Lite": "Two-Step Lite",
    "2-Step Pro": "Two-Step Pro",
}

# News is included (no SKU). Swing is not sold.
# Weekend and Weekly stay on the checkout card. On Demand Instant is 32%
# so year-1 leftover prints; evals 15% match Blue Guardian.
PCT = {
    "weekend": {"Instant": 0.15, "eval": 0.15},
    "weekly": {"Instant": 0.06, "eval": 0.06},
    "od90": {"Instant": 0.32, "eval": 0.15},
}

ADDONS = (
    ("weekend", "Weekend holding"),
    ("weekly", "Weekly 70%"),
    ("od90", "On Demand 90%"),
)


def js_round(x: float) -> int:
    return int(x + 0.5) if x >= 0 else int(x - 0.5)


def sticker(list_px: float, pct: float) -> int:
    return js_round(float(list_px) * float(pct))


def plan_pct(plan: str, key: str) -> float:
    band = "Instant" if plan == "Instant" else "eval"
    return PCT[key][band]


def sku_rows():
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            sale = REC[(plan, sz)]
            list_px = rec_list(sale)
            row = {
                "Plan": PLAN_LABEL[plan],
                "Key": plan,
                "Size": sz,
                "List": list_px,
                "Sale": sale,
            }
            for key, _name in ADDONS:
                row[key] = sticker(list_px, plan_pct(plan, key))
            rows.append(row)
    return rows


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(MARGIN, H - 5.4 * mm, "VERODUS  ·  Add-on catalog  ·  17 Aug 2026")
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Recommended VERO35 card")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Weekend = round(list × 15%). Weekly 70% = round(list × 6%). "
        "On Demand 90% = round(list × 32% Instant / 15% evals). "
        "News included. Swing dropped. Weekly and On Demand may stack.",
    )
    canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Add-on menu", s["cover"]))
    story.append(P(
        "Same percentage on every size in a plan. News is included (not an add-on). "
        "Default reward is Bi-Weekly 80% — not a toggle. Stickers below are before VERO35. "
        "Instant On Demand is 32% so year-1 leftover prints.",
        s["sub"],
    ))

    pheads = ["Add-on", "Instant", "1-Step / Lite / Pro", "What it is"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    menu = (
        ("News trading", "included", "included", "Allowed on eval and funded. No SKU."),
        ("Weekend holding", "15%", "15%", "Friday 22:00 flatten off."),
        ("Weekly Rewards with 70% Reward Split", "6%", "6%", "Withdraw your profit share weekly. Same % on every size."),
        ("On Demand Rewards with 90% Split", "32%", "15%", "Withdraw anytime after that plan’s payout rule. Instant: $100 and Best Day ≤20% of every profitable day; a day meets 0.5% only if profit is at least 0.5% of SOD. 1-Step: $100 and Best Day ≤50%. 2-Step: $100 and 3 trading days. Instant 32% is the year-1 print floor."),
        ("Swing", "not offered", "not offered", "News is already in the fee. Do not sell news+weekend."),
    )
    pspec = {}
    for i, row in enumerate(menu, start=1):
        if row[0] in ("News trading", "Swing"):
            pspec[i] = "live"
        elif "On Demand" in row[0] or "Weekly" in row[0]:
            pspec[i] = "rec"
        pdata.append([P(c, s["tdl"] if j in (0, 3) else s["td"]) for j, c in enumerate(row)])
    story.append(grid(pdata, [58 * mm, 28 * mm, 38 * mm, 88 * mm], pspec))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Coupon <b>VERO35 (35%)</b> applies to challenge list + add-on stickers. "
        "Shopper pays 65% of the sticker. Weekly and On Demand may both be selected. "
        "First-payout refund is the challenge fee only — add-ons are not refunded. "
        "Instant is not refundable at all.",
        s["tiny"],
    ))

    story.append(PageBreak())

    story.append(P("Stickers per challenge", s["cover"]))
    story.append(P(
        f"{len(rows)} SKUs. List = checkout basePrice from the 17 Aug catalog. "
        "Green = Instant. Blue = evals. Weekly 70% is 6% of list. "
        "On Demand 90% is 32% Instant / 15% evals.",
        s["sub"],
    ))

    heads = [
        "Plan", "Size", "List",
        "Weekend", "Weekly 70%", "On Demand 90%",
    ]
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
        "Instant $100k list $675: weekend $101 · weekly $41 · On Demand 90% $216. "
        "Pro $100k list $537: weekend $81 · weekly $32 · On Demand 90% $81. "
        "Green = Instant. Blue = evals.",
        s["tiny"],
    ))

    md = [
        "# Verodus add-on catalog — 17 August 2026\n",
        "Weekend sticker = `round(list × 15%)`. Weekly 70% = `round(list × 6%)`. "
        "On Demand 90% = `round(list × 32%)` Instant / `round(list × 15%)` evals. "
        "VERO35 is 35% off list + stickers. News included. Swing not offered.\n",
        "## Percent of list\n",
        "| Add-on | Instant | 1-Step / Lite / Pro |",
        "|---|---:|---:|",
        "| News trading | included | included |",
        "| Weekend holding | 15% | 15% |",
        "| Weekly Rewards with 70% Reward Split | 6% | 6% |",
        "| On Demand Rewards with 90% Split | 32% | 15% |",
        "| Swing | not offered | not offered |",
        "",
        "## Stickers per challenge\n",
        "| Plan | Size | List | Weekend | Weekly 70% | On Demand 90% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        md.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {usd(r['List'])} | "
            f"{usd(r['weekend'])} | {usd(r['weekly'])} | {usd(r['od90'])} |"
        )
    md.append("")
    md.append(
        "Default is Bi-Weekly 80%. Weekly and On Demand may stack. "
        "PDF: `results/Verodus_Addon_Catalog_2026-08-17.pdf`\n"
    )
    MD.write_text("\n".join(md) + "\n")

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus add-on catalog — 17 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    shutil.copyfile(OUT, OUT_SHOP)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {OUT_SHOP}")
    print(f"Wrote {MD}")


if __name__ == "__main__":
    build()
