#!/usr/bin/env python3
"""Shopper catalog: recommended VERO35 sale + list, Lite funded DD 8%."""

from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

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
OUT = RESULTS / "Verodus_Challenge_Catalog_2026-08-17.pdf"
OUT_SHOP = RESULTS / "verodus-challenge-catalog-2026-08-17.pdf"
MD = RESULTS / "CHALLENGE_CATALOG.md"

PAGE = landscape(A4)

PLAN_LABEL = {
    "Instant": "Instant Funding",
    "1-Step": "One-Step",
    "2-Step Lite": "Two-Step Lite",
    "2-Step Pro": "Two-Step Pro",
}


def discount(list_px, sale):
    if not list_px:
        return "—"
    return f"{round(100.0 * (1.0 - sale / list_px))}%"


def sku_rows():
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            sale = REC[(plan, sz)]
            list_px = rec_list(sale)
            rows.append({
                "Plan": PLAN_LABEL[plan],
                "Key": plan,
                "Size": sz,
                "List": list_px,
                "Sale": sale,
                "Off": discount(list_px, sale),
            })
    return rows


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(MARGIN, H - 5.4 * mm, "VERODUS  ·  Challenge catalog  ·  17 Aug 2026")
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Recommended VERO35 card")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "List = sale ÷ 0.65. Sale = recommended VERO35. Instant $200k pulled. "
        "News included. Lite funded max DD 8%. Street doors on Lite/Pro $5k–$10k.",
    )
    canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    s = rec_styles()
    story = []
    rows = sku_rows()

    story.append(P("Current Verodus challenges", s["cover"]))
    story.append(P(
        f"{len(rows)} SKUs. List = checkout basePrice. Sale = recommended VERO35 "
        "(what shoppers pay). Instant $200k is not offered. News is included "
        "(not an add-on). Lite/Pro $5k–$10k follow the 2-step street door.",
        s["sub"],
    ))

    heads = ["Plan", "Size", "List", "Sale (VERO35)", "Discount", "Account"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Key"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]),
            P(f"${r['Size'] // 1000}k", s["td"]),
            P(usd(r["List"]), s["td"]),
            P(usd(r["Sale"]), s["td"]),
            P(r["Off"], s["td"]),
            P(usd(r["Size"]), s["td"]),
        ])
    story.append(grid(data, [48*mm, 28*mm, 32*mm, 40*mm, 28*mm, 36*mm], spec))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Coupon default: <b>VERO35 (35%)</b>. List = sale ÷ 0.65 so the code still lands. "
        "Green = Instant. Blue = evals. Door: Instant from $49 · 1-Step from $45 · "
        "Lite from $39 · Pro from $45. Source: street-door rec 17 Aug 2026.",
        s["tiny"],
    ))

    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(P("Pass + drawdown rules", s["cover"]))
    story.append(P(
        "Same percentage rules on every size in a plan. "
        "News is included on every eval phase and funded account. "
        "Lite funded max DD is 8%. Instant 6% trail never locks.",
        s["sub"],
    ))

    rheads = ["Plan", "Stage", "Target", "Min days", "Consistency",
              "Daily DD", "Max DD", "Max basis"]
    rdata = [[P(h, s["th"]) for h in rheads]]
    rules = (
        ("Instant Funding", "Funded (day 1)", "None (payout unlock)",
         "None", "20% best day (all profitable days)", "3%", "6%", "Trailing HWM (never locks)"),
        ("One-Step", "Evaluation", "10%", "0", "50% best day",
         "4%", "6%", "Hybrid trail, lock at initial"),
        ("One-Step", "Funded", "None", "0", "50% best day",
         "4%", "6%", "Hybrid trail, lock at initial"),
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
    rspec = {}
    for i, row in enumerate(rules, start=1):
        if row[0] == "Two-Step Lite" and row[1] == "Funded":
            rspec[i] = "rec"
        elif row[0].startswith("Two-Step Lite"):
            rspec[i] = "live"
        rdata.append([P(c, s["tdl"] if j < 2 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(rdata, [
        32*mm, 32*mm, 36*mm, 22*mm, 28*mm, 20*mm, 18*mm, 44*mm,
    ], rspec))
    story.append(Spacer(1, 3*mm))

    story.append(P("Notes", s["h1"]))
    story.append(P(
        "<b>Instant:</b> no eval. Daily 3% of start from the day’s equity high. "
        "Max 6% trails peak and never locks. One payout rule: 20% Best Day "
        "(every profitable day is factored; a day meets 0.5% only if profit is at least 0.5% of SOD), $100 min. "
        "The 20% cap implies at least five counted days — do not list a 5-day checkbox. "
        "<b>No fee refund.</b> Split 80/20, biweekly. No 2% risk cap, no first-reward cap, no $200k.",
        s["body"],
    ))
    story.append(P(
        "<b>One-Step:</b> 10% target, 50% best-day, 4% daily (SOD), 6% hybrid max "
        "(locks at initial). Same DD on funded. 50% Best Day (two equal days can pass; "
        "that split is rare, so the clock is usually three days). Do not list a 3-day min. "
        "Fee refunded on first payout (challenge fee only — add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Lite:</b> P1 8% / P2 5%, 5 days each, 4% daily, "
        "<b>8% static max on eval and funded</b> (funded was 10% — now the same 8% floor). "
        "Fee refunded on first payout (challenge fee only — add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>Two-Step Pro:</b> P1 10% / P2 5%, 5 days each, 5% daily, 10% static max "
        "eval and funded. Fee refunded on first payout (challenge fee only — add-ons are not refunded).",
        s["body"],
    ))
    story.append(P(
        "<b>News</b> is included on every plan (eval and funded). Weekend holding is a paid add-on. "
        "Shared: VERO35 · 30-day inactivity · unlimited time · $100 min reward on every cycle.",
        s["tiny"],
    ))

    md = [
        "# Verodus challenge catalog — 17 August 2026\n",
        "Recommended VERO35 sale. List = sale ÷ 0.65. Instant $200k pulled. "
        "News included. Lite funded max DD 8%. Street doors: Instant $49 · 1-Step $45 · "
        "Lite $39 · Pro $45.\n",
        "## Prices\n",
        "| Plan | Size | List | Sale (VERO35) | Discount |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        md.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {usd(r['List'])} | "
            f"{usd(r['Sale'])} | {r['Off']} |"
        )
    md.append("")
    md.append("## Rules\n")
    md.append("| Plan | Stage | Target | Min days | Consistency | Daily DD | Max DD |")
    md.append("|---|---|---|---|---|---|---|")
    for row in rules:
        md.append("| " + " | ".join(row[:7]) + " |")
    md.append("")
    md.append(
        "News is **included** (not an add-on). Lite funded max DD is **8%**. "
        "Instant has no fee refund. Evals refund the challenge fee only on first payout. "
        "PDF: `results/Verodus_Challenge_Catalog_2026-08-17.pdf`\n"
    )
    MD.write_text("\n".join(md) + "\n")

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus challenge catalog — 17 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    shutil.copyfile(OUT, OUT_SHOP)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {OUT_SHOP}")
    print(f"Wrote {MD}")


if __name__ == "__main__":
    build()
