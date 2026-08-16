#!/usr/bin/env python3
"""One complete Verodus operator report: P(pay) audit, BE $, rec, margins."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from write_price_rec_pdf import (
    ANCHORS,
    REC,
    SIZES,
    classic_table,
    family_peers,
    mix_table,
    opex_rows,
    opex_table,
    load,
    plan_be,
    pricing_for,
    rec_be_cell,
    usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Complete_Report_2026-08-16.pdf"
MD = RESULTS / "COMPLETE_REPORT.md"

PAGE = landscape(A4)
W, H = PAGE
MARGIN = 11 * mm

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_V = colors.HexColor("#e8f1ff")
ROW_REC = colors.HexColor("#dcfce7")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Times-Bold",
            fontSize=20, leading=24, textColor=NAVY, alignment=TA_LEFT, spaceAfter=4,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Times-Italic",
            fontSize=10.5, leading=13, textColor=TEAL, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Times-Bold",
            fontSize=12.5, leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=8.3, leading=10.8, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=6.5, leading=8.0, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.5, leading=8.0, alignment=TA_CENTER,
        ),
        "td2": ParagraphStyle(
            "td2", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.5, leading=8.2, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.5, leading=8.0, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.0, leading=9.0, textColor=colors.HexColor("#334155"),
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        MARGIN, H - 5.4 * mm,
        "VERODUS  ·  Complete operator report  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Source of truth. Instant priced on year-1. Evals on first-payout + refund. P(pay) audited.",
    )
    canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def P(text, style):
    return Paragraph(text, style)


def grid(data, col_w, special=None):
    special = special or {}
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 6.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 1.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.5),
    ]
    for i in range(1, len(data)):
        kind = special.get(i)
        if kind == "rec":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_REC))
            sty.append(("FONTNAME", (0, i), (-1, i), "Times-Bold"))
        elif kind == "live":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_V))
            sty.append(("FONTNAME", (0, i), (-1, i), "Times-Bold"))
        elif i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def pct(x, signed=False, digits=1):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    v = 100.0 * float(x)
    return f"{v:+.{digits}f}%" if signed else f"{v:.{digits}f}%"


def m_sale(sale, cost):
    if sale is None or cost is None or sale <= 0:
        return None
    return (sale - cost) / sale


def vero_rows(skus):
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            r = live.iloc[0]
            pr = pricing_for(r)
            rec = REC[(plan, sz)]
            cost = pr["e_used"] if plan == "Instant" else float(r.E_cost)
            rows.append({
                "Plan": plan, "Size": sz, "Basis": pr["basis"],
                "P_pay": pr["p_pay"], "P_yr1": pr["p_yr1"],
                "E_first": pr["e_first"], "E_used": pr["e_used"],
                "BE": pr["be"],
                "px_20": pr["px_20"], "px_40": pr["px_40"], "px_60": pr["px_60"],
                "Live": float(r.Sale), "Rec": rec,
                "List": round(rec / 0.65),
                "Cost": cost,
                "Rec_m": m_sale(rec, cost),
                "Live_m": m_sale(float(r.Sale), cost),
            })
    return rows


def build():
    skus, scored = load()
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    profiles = pd.read_csv(RESULTS / "industry_profiles.csv")
    s = styles()
    story = []
    rows = vero_rows(skus)
    md = []

    story.append(P("Verodus complete operator report", s["cover"]))
    story.append(P(
        "One document. P(pay) audited. Instant priced on year-1. Evals on first-payout "
        "+ refund. Recommended sale, BE $, 20/40/60, peers, and margin % by size and "
        "family. 16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "This replaces the three earlier PDFs for decisions. "
        "<b>Industry report</b> still prices Instant on first-payout 22% (BE $875, "
        "20% = $1,094) — that path is wrong for Instant. "
        "<b>Rank report</b> is difficulty only. "
        "<b>Recommended-prices PDF</b> matches this card. "
        "Ignore <b>verodus_blended.csv</b> (old harsh book: Instant P(pay) 2.8%).",
        s["body"],
    ))
    md.append("# Verodus complete operator report — 16 August 2026\n")
    md.append("One document. Instant priced on year-1. Evals on first-payout + refund.\n")

    # ----- 1. P(pay) verdict -----
    story.append(P("1. Is P(pay) correct?", s["h1"]))
    story.append(P(
        "<b>Yes — if you keep the two Instant numbers apart.</b> "
        "In this book P(pay) is <b>first-payout eligibility</b>: the share of buyers "
        "who collect a first reward of at least $100. It is not “still paying at month 12”. "
        "Year-1 is that later number. Instant must be priced on year-1. Evals stay on "
        "first-payout + fee refund (those already match the shelf).",
        s["body"],
    ))
    story.append(P(
        "Instant has no challenge. The engine treats “phase 1 = funded = paid” as soon as "
        "the trader posts <b>5 valid days at +0.5% of start-of-day</b>, keeps 20% "
        "consistency, and clears the $100 floor at an 80% split. That is a low bar for "
        "a skilled book and an impossible bar for Aggressive / Lottery (45% of buyers), "
        "who blow the 6% trail on day 1. The 22.1% blend is those two facts together — "
        "not “one in five Instant buyers is a year-1 survivor.”",
        s["body"],
    ))

    vheads = ["Plan", "What P(pay) is", "P(pay)", "Year-1", "Use for price?", "Verdict"]
    vdata = [[P(h, s["th"]) for h in vheads]]
    verdicts = [
        ("Instant", "5 valid days + $100 (no eval)", 0.2207, 0.07161,
         "No — use year-1 7.16%", "Correct as first-pay; do not price on it"),
        ("1-Step", "Pass 10% / 4% / 6% hybrid + funded + $100", 0.08808, 0.02921,
         "Yes — first-payout + refund", "Correct. Harder than FTMO 1-Step 13.5%"),
        ("2-Step Lite", "Pass 8/8 then 5/8 + funded 8% DD + $100", 0.10616, 0.03378,
         "Yes — first-payout + refund", "Correct. Near FTMO 12.7% / FN Lite 12.0%"),
        ("2-Step Pro", "Pass 10/10 then 5/10 + funded + $100", 0.11998, 0.04195,
         "Yes — first-payout + refund", "Correct. FTMO 2-step twin is 12.7%"),
    ]
    vspec = {}
    for i, (plan, what, pp, y1, use, verd) in enumerate(verdicts, start=1):
        if plan == "Instant":
            vspec[i] = "rec"
        else:
            vspec[i] = "live"
        vdata.append([
            P(plan, s["tdl"]), P(what, s["tdl"]),
            P(pct(pp), s["td"]), P(pct(y1), s["td"]),
            P(use, s["tdl"]), P(verd, s["tdl"]),
        ])
    story.append(grid(vdata, [
        24*mm, 62*mm, 18*mm, 18*mm, 48*mm, 62*mm,
    ], vspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Check: Instant year-1 = 22.07% × 0.59 × 0.72 × 0.76 = 7.13% (book prints 7.161%). "
        "Post-pay death is PropScorer-class (41% of funded die in month 1). "
        "Track360 sustained Instant is 4–6%; this book is a touch optimistic at 7.2%, "
        "not a different order of magnitude. Pricing Instant on 22% produced the old "
        "$1,094 “20% fee” that sat above every peer.",
        s["body"],
    ))

    md.append("## 1. Is P(pay) correct?\n")
    md.append("| Plan | P(pay) | Year-1 | Price on | Verdict |")
    md.append("|---|---:|---:|---|---|")
    for plan, what, pp, y1, use, verd in verdicts:
        md.append(f"| {plan} | {pct(pp)} | {pct(y1)} | {use} | {verd} |")
    md.append("")

    # ----- 2. P(pay) by profile -----
    story.append(P("2. P(pay) by trader type — why Instant is 22%, not 50%", s["h1"]))
    story.append(P(
        "Book mix is 7% Pro / 22% Semi-skilled / 26% Average / 28% Aggressive / 17% Lottery. "
        "Instant 22.1% = 0.07×76.2% + 0.22×58.7% + 0.26×14.7% + 0.28×0 + 0.17×0. "
        "Almost half the book never collects. That is realistic for a 6% trail that never locks.",
        s["body"],
    ))
    pheads = ["Plan", "Pro 7%", "Semi 22%", "Average 26%", "Aggressive 28%",
              "Lottery 17%", "Blend P(pay)", "Blend year-1"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    pspec = {}
    for i, (plan, product) in enumerate((
        ("Instant", "Verodus Instant"),
        ("1-Step", "Verodus 1-Step"),
        ("2-Step Lite", "Verodus 2-Step Lite"),
        ("2-Step Pro", "Verodus 2-Step Pro"),
    ), start=1):
        sub = profiles[profiles.Product == product]
        by = {r.Profile: float(r.P_pay) for r in sub.itertuples()}
        br = blend[blend.Product == product].iloc[0]
        if plan == "Instant":
            pspec[i] = "rec"
        pdata.append([
            P(plan, s["tdl"]),
            P(pct(by.get("Pro")), s["td"]),
            P(pct(by.get("Semi-skilled")), s["td"]),
            P(pct(by.get("Average")), s["td"]),
            P(pct(by.get("Aggressive")), s["td"]),
            P(pct(by.get("Lottery")), s["td"]),
            P(pct(br.P_pay), s["td"]),
            P(pct(br.P_yr1), s["td"]),
        ])
    story.append(grid(pdata, [
        28*mm, 24*mm, 26*mm, 28*mm, 32*mm, 28*mm, 28*mm, 26*mm,
    ], pspec))
    story.append(Spacer(1, 2*mm))

    # ----- 3. vs published funnel and twins -----
    story.append(P("3. Book vs published funnel and closest twins", s["h1"]))
    story.append(P(
        "The book was calibrated so an FTMO-style 10/5 · 5/10 static 2-step lands near "
        "Track360 / FPFX / FTMO: Phase 1 ~25–30%, funded ~10–12%, ever-paid ~7%, "
        "year-1 ~1–3%. Actual FTMO 2-step in this run: P1 21.8%, funded = P(pay) 12.7%, "
        "year-1 4.2%. Funded equals P(pay) because almost every funded path clears $100. "
        "Track360’s 7% “ever paid” is a bit lower (some funded accounts never request). "
        "Relative ranks still hold. Instant twins with a daily + 6% trail sit at 21–24% "
        "first-pay; no-daily Instant (FXIFY Standard, FN Stellar Instant) sits at ~53%.",
        s["body"],
    ))
    theads = ["Product", "Family", "P1", "Funded", "P(pay)", "Year-1",
              "E[X] first $100k", "Why it sits here"]
    tdata = [[P(h, s["th"]) for h in theads]]
    twins = [
        ("Verodus Instant", "Same 3%/6%/20% as BG; trail never locks", "rec"),
        ("BG Instant", "3% SOD daily + trail locks at +6%", "live"),
        ("IF Instant", "3/6 Instant-class", None),
        ("Goat Instant", "3/6 + 2% risk + 15% cons — harder", None),
        ("Hola Direct", "Instant-class, slightly easier", None),
        ("FXIFY Instant", "8% trail, no daily — much easier", None),
        ("Verodus 1-Step", "4% daily, 6% hybrid, 50% eval cons", "live"),
        ("FTMO 1-Step", "Softer 1-step, 90% split", None),
        ("Verodus 2-Step Lite", "8% static, funded DD 8%", "live"),
        ("FN Stellar Lite", "Closest cheap 2-step twin", None),
        ("Verodus 2-Step Pro", "10/5 · 5/10 static", "live"),
        ("FTMO 2-Step", "Calibration anchor", None),
    ]
    tspec = {}
    for i, (product, why, kind) in enumerate(twins, start=1):
        br = blend[blend.Product == product]
        if br.empty:
            continue
        r = br.iloc[0]
        if kind:
            tspec[i] = kind
        tdata.append([
            P(product, s["tdl"]), P(str(r.Family), s["td"]),
            P(pct(r.Phase1), s["td"]), P(pct(r.Funded), s["td"]),
            P(pct(r.P_pay), s["td"]), P(pct(r.P_yr1), s["td"]),
            P(usd(r.E_payout_100k), s["td"]), P(why, s["tdl"]),
        ])
    story.append(grid(tdata, [
        36*mm, 18*mm, 16*mm, 18*mm, 18*mm, 18*mm, 32*mm, 76*mm,
    ], tspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = Instant (price on year-1). Blue = Verodus evals. "
        "Verodus Instant P(pay) 22.1% matches Blue Guardian 22.1% and Instant Funding 21.4%. "
        "That is the check that 22% is not a bug.",
        s["tiny"],
    ))

    # ----- 4. Rules -----
    story.append(P("4. Live Verodus rules used in the book", s["h1"]))
    rheads = ["Rule", "Instant", "1-Step", "2-Step Lite", "2-Step Pro"]
    rdata = [[P(h, s["th"]) for h in rheads]]
    rules = [
        ("Phases", "0-step (funded on day 1)", "1 eval + funded", "2 eval + funded", "2 eval + funded"),
        ("Profit target", "None — 5 valid days", "10%", "8% then 5%", "10% then 5%"),
        ("Max DD", "6% trailing, never locks", "6% hybrid", "8% static (funded 8%)", "10% static"),
        ("Daily DD", "3% of day’s equity high", "4% SOD", "4% SOD", "5% SOD"),
        ("Consistency", "20% of +days", "50% on eval only", "None", "None"),
        ("Min days / valid", "5 days at +0.5% SOD", "3 funded days", "5+5 eval, 3 funded", "5+5 eval, 3 funded"),
        ("Split / min reward", "80% / $100", "80% / $100", "80% / $100", "80% / $100"),
        ("Fee refund", "None", "First payout", "First payout", "First payout"),
        ("Not in Instant", "No 2% risk cap, no first-reward cap, no $200k", "—", "—", "—"),
    ]
    for row in rules:
        rdata.append([P(c, s["tdl"] if i == 0 else s["td"]) for i, c in enumerate(row)])
    story.append(grid(rdata, [32*mm, 52*mm, 42*mm, 48*mm, 48*mm]))
    story.append(Spacer(1, 2*mm))

    # ----- 5. Cost basis -----
    story.append(P("5. Cost basis and BE $ (the number the card is built on)", s["h1"]))
    story.append(P(
        "<b>Instant</b> E[cost] = E[X]<sub>first</sub> × (P<sub>yr1</sub> / P<sub>pay</sub>) "
        "= $875.25 × (7.161% / 22.07%) = <b>$284 at $100k</b>, no refund, then × size/100k. "
        "<b>Eval</b> BE = E[X] / (1 − P(pay)): 1-Step $108.10 / 0.91192 = <b>$119</b>; "
        "Lite $136.01 / 0.89384 = <b>$152</b>; Pro $132.54 / 0.88002 = <b>$151</b>. "
        "F<sub>m</sub> = BE / (1 − m). Columns are <b>20 / 40 / 60</b> — the industry "
        "layout. Instant rec is the 30% print — greater margin that still sells. "
        "40% and 60% are reference only (too rich versus Goat / Instant Funding).",
        s["body"],
    ))
    bheads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k", "Basis"]
    bdata = [[P(h, s["th"]) for h in bheads]]
    bspec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            if (plan, sz) not in REC:
                cells.append(P("—", s["td"]))
            else:
                cells.append(P(usd(plan_be(skus, plan, sz)), s["td"]))
        cells.append(P("year-1" if plan == "Instant" else "first + refund", s["td"]))
        bdata.append(cells)
        bspec[i] = "rec" if plan == "Instant" else "live"
    story.append(grid(bdata, [
        28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 30*mm, 30*mm, 32*mm,
    ], bspec))
    story.append(Spacer(1, 2*mm))

    # ----- 6. Rec card -----
    story.append(P("6. Recommended VERO35 sale (rec $ over BE $)", s["h1"]))
    story.append(P(
        "Instant sits on the year-1 30% print, with a shop floor on $5k/$10k. "
        "Evals stay live — already the cheapest (or #2) name and fat versus BE.",
        s["body"],
    ))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k",
             "BE $100k", "Live $100k"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        live100 = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == 100000)]
        live_s = float(live100.Sale.iloc[0]) if not live100.empty else None
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            cells.append(rec_be_cell(REC.get((plan, sz)), plan_be(skus, plan, sz), s["td2"]))
        cells.append(P(usd(plan_be(skus, plan, 100000)), s["td"]))
        cells.append(P(usd(live_s), s["td"]))
        data.append(cells)
        special[i] = "rec"
    story.append(grid(data, [
        26*mm, 26*mm, 26*mm, 26*mm, 26*mm, 28*mm, 28*mm, 24*mm, 24*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant rec $59 / $69 / $129 / $229 / $429. $100k $429 is opex floor $422, "
        "0.92× BG $467. Lite $39 / $51 / $89 / $149 / $259 / $479 (solvent floor). "
        "1-Step live. Pro $39 / $49 then live.",
        s["tiny"],
    ))

    # ----- 7. Classic SKU table -----
    story.append(P(
        "7. Plan / Size / List / Sale / E[X] / P(pay) / BE / 20% / 40% / 60% / Sale m",
        s["h1"],
    ))
    story.append(P(
        "<b>Use 20 / 40 / 60</b> as the industry reference. Instant rec is the year-1 "
        "<b>30% print</b> — greater margin that still sells. "
        "40% Instant $100k is $473 (Blue Guardian $467). "
        "60% is $710 (above Goat $559 / Instant Funding $639). Do not aim Instant at 40 or 60. "
        "10 / 20 / 30 was only a reaction when 40/60 looked too rich as Instant targets. "
        "Sale is the recommended VERO35 fee. List = sale ÷ 0.65. "
        "Instant E[X] / BE are year-1; P(pay) is first-payout 22.1%.",
        s["body"],
    ))
    ctab, _crows = classic_table(skus, s)
    story.append(ctab)
    story.append(Spacer(1, 2*mm))

    story.append(P("7b. Wage mix — CAD 10k / month on 310 accounts", s["h1"]))
    story.append(mix_table(skus, s))
    story.append(Spacer(1, 2*mm))

    story.append(P(
        "7c. Opex stack — error 10%, $1 + wage, marketing 20%",
        s["h1"],
    ))
    story.append(P(
        "S<sub>opex</sub> = (BE × 1.10 + $1 + wage) / 0.80. "
        "Wages CAD 10,000 × 0.72 = USD 7,200 / month, weighted across 310 accounts. "
        "Peer low is only usable if Low OK is yes. Alpha Instant and Maven $5k–$25k fail.",
        s["body"],
    ))
    otab, _orows = opex_table(skus, s)
    story.append(otab)
    story.append(Spacer(1, 2*mm))

    # ----- 8. Instant peers -----
    story.append(P("8. Instant $100k peers — first-payout vs year-1", s["h1"]))
    story.append(P(
        "Same-difficulty Instant (daily + ~6% trail) charges $274–$839. "
        "First-payout margins on those stickers are negative. Year-1 margins are +38% to +60%. "
        "That is why the old $1,094 Instant fee was rejected.",
        s["body"],
    ))
    inst = skus[(skus.Family == "instant") & (skus.Size == 100000)].copy().sort_values("Sale")
    pheads = ["Firm", "Plan", "Sale", "P(pay)", "Year-1",
              "E[X] first", "m first", "E[X] yr1", "m yr1"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    pspecial = {}
    for i, r in enumerate(inst.itertuples(), start=1):
        pr = pricing_for(r)
        m_first = (float(r.Sale) - pr["e_first"]) / float(r.Sale) if r.Sale else None
        m_y1 = (float(r.Sale) - pr["e_used"]) / float(r.Sale) if r.Sale else None
        if r.Firm == "Verodus":
            pspecial[i] = "live"
        pdata.append([
            P(str(r.Firm), s["tdl"]), P(str(r.Plan), s["tdl"]),
            P(usd(r.Sale), s["td"]),
            P(pct(r.P_pay), s["td"]), P(pct(r.P_yr1), s["td"]),
            P(usd(pr["e_first"]), s["td"]), P(pct(m_first, signed=True, digits=0), s["td"]),
            P(usd(pr["e_used"]), s["td"]), P(pct(m_y1, signed=True, digits=0), s["td"]),
        ])
    vr = inst[inst.Firm == "Verodus"].iloc[0]
    pr = pricing_for(vr)
    rec = REC[("Instant", 100000)]
    pdata.append([
        P("Verodus rec", s["tdl"]), P("Instant", s["tdl"]),
        P(usd(rec), s["td"]),
        P(pct(vr.P_pay), s["td"]), P(pct(vr.P_yr1), s["td"]),
        P(usd(pr["e_first"]), s["td"]),
        P(pct((rec - pr["e_first"]) / rec, signed=True, digits=0), s["td"]),
        P(usd(pr["e_used"]), s["td"]),
        P(pct((rec - pr["e_used"]) / rec, signed=True, digits=0), s["td"]),
    ])
    pspecial[len(pdata) - 1] = "rec"
    story.append(grid(pdata, [
        32*mm, 28*mm, 18*mm, 16*mm, 16*mm, 24*mm, 18*mm, 22*mm, 16*mm,
    ], pspecial))
    story.append(Spacer(1, 2*mm))

    # ----- 9. Eval peers $100k -----
    story.append(P("9. Eval $100k street — live Verodus vs twins", s["h1"]))
    eheads = ["Family", "Firm", "Plan", "Sale", "P(pay)", "E[X]", "BE $", "Sale m"]
    edata = [[P(h, s["th"]) for h in eheads]]
    espec = {}
    ei = 0
    eval_show = [
        ("1-step", ["Verodus", "FTMO", "FundedNext", "Hola Prime", "Fintokei", "Blue Guardian"]),
        ("2-step", ["Verodus", "FTMO", "Maven", "Goat Funded", "FundedNext", "Ment Funding"]),
    ]
    for fam, firms in eval_show:
        peers = skus[(skus.Family == fam) & (skus.Size == 100000)]
        for firm in firms:
            sub = peers[peers.Firm == firm]
            for r in sub.itertuples():
                ei += 1
                if r.Firm == "Verodus":
                    espec[ei] = "live"
                edata.append([
                    P(fam, s["td"]), P(str(r.Firm), s["tdl"]), P(str(r.Plan), s["tdl"]),
                    P(usd(r.Sale), s["td"]), P(pct(r.P_pay), s["td"]),
                    P(usd(r.E_payout), s["td"]), P(usd(r.BE), s["td"]),
                    P(pct(r.sale_m, signed=True, digits=0), s["td"]),
                ])
    story.append(grid(edata, [
        20*mm, 32*mm, 36*mm, 20*mm, 18*mm, 22*mm, 20*mm, 18*mm,
    ], espec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Blue = live Verodus. 1-Step $335 is the cheapest serious 1-step (Fintokei $399, "
        "Hola $463, FTMO $579). Lite $259 is the cheapest solvent 2-step (under Maven $279). "
        "Pro $296 is #2 after Maven $279.",
        s["tiny"],
    ))

    # ----- 10. Prior PDF audit -----
    story.append(P("10. What the other PDFs still say (do not mix them)", s["h1"]))
    aheads = ["File", "Instant $100k", "Columns", "P(pay) used", "Use it?"]
    adata = [[P(h, s["th"]) for h in aheads]]
    audits = [
        ("This report + Recommended Prices PDF",
         "Rec $429 · BE $284 · +34%",
         "20 / 40 / 60",
         "Year-1 7.16% for Instant; 8.8/10.6/12.0 for evals",
         "Yes — source of truth"),
        ("Verodus_Industry_Report PDF",
         "Proposed $1,094 · first-payout BE $875",
         "20 / 40 / 60",
         "Instant 22.1% as if it were the cost rate",
         "No for Instant price. Rules/research still useful"),
        ("Verodus_BE_Rank_Report PDF",
         "Year-1 BE / 20% / 30% ranks",
         "20 / 30",
         "Year-1 Instant after the last revision",
         "Difficulty only — not the sale card"),
        ("verodus_blended.csv (old engine)",
         "Instant P(pay) 2.8%",
         "—",
         "Harsher pre-industry book",
         "Ignore"),
        ("industry_skus.csv Instant BE column",
         "BE $875 (first-payout)",
         "20 / 40 / 60 first-pay",
         "22.1%",
         "Do not price Instant from this column"),
    ]
    aspec = {1: "rec"}
    for i, row in enumerate(audits, start=1):
        adata.append([P(c, s["tdl"] if j in (0, 3, 4) else s["td"]) for j, c in enumerate(row)])
    story.append(grid(adata, [58*mm, 52*mm, 28*mm, 62*mm, 32*mm], aspec))
    story.append(Spacer(1, 2*mm))

    # ----- 11. Margins by size and family -----
    story.append(P("11. Margin % for every account size and family", s["h1"]))
    story.append(P(
        "Rec m = (rec − E[cost]) / rec. Instant E[cost] is year-1 E[X]. "
        "Eval E[cost] is first-payout E[X] + expected fee refund. "
        "Live m uses the same cost on today’s VERO35 sale. "
        "$5k/$10k Instant look fat because the shop floor ($59 / $69) sits on a $14 / $28 BE — "
        "that is a floor, not a 60% target. $25k+ Instant is the 30–40% print.",
        s["body"],
    ))
    mheads = ["Family / plan", "Size", "Rec $", "BE $", "E[cost]",
              "Rec m", "Live $", "Live m", "vs 20%", "vs 40%"]
    mdata = [[P(h, s["th"]) for h in mheads]]
    mspec = {}
    for i, r in enumerate(rows, start=1):
        mspec[i] = "rec" if r["Plan"] == "Instant" else "live"
        vs20 = (r["Rec"] / r["px_20"] - 1.0) if r["px_20"] else None
        vs40 = (r["Rec"] / r["px_40"] - 1.0) if r["px_40"] else None
        mdata.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["Rec"]), s["td"]), P(usd(r["BE"]), s["td"]),
            P(usd(r["Cost"]), s["td"]),
            P(pct(r["Rec_m"], signed=True, digits=0), s["td"]),
            P(usd(r["Live"]), s["td"]),
            P(pct(r["Live_m"], signed=True, digits=0), s["td"]),
            P(pct(vs20, signed=True, digits=0), s["td"]),
            P(pct(vs40, signed=True, digits=0), s["td"]),
        ])
    story.append(grid(mdata, [
        28*mm, 20*mm, 20*mm, 20*mm, 22*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm,
    ], mspec))
    story.append(Spacer(1, 2.5*mm))

    story.append(P("12. Family roll-up at $100k (the modal size)", s["h1"]))
    fheads = ["Family", "P(pay)", "Year-1", "BE $100k", "Rec $100k",
              "Rec m", "Live $100k", "Live m", "Peer $100k low / med"]
    fdata = [[P(h, s["th"]) for h in fheads]]
    fspec = {}
    for i, (plan, fam) in enumerate(ANCHORS, start=1):
        r = next(x for x in rows if x["Plan"] == plan and x["Size"] == 100000)
        peers = family_peers(skus, fam)
        vals = peers.loc[peers.Size == 100000, "Sale"]
        lo = float(vals.min()) if len(vals) else None
        med = float(vals.median()) if len(vals) else None
        fspec[i] = "rec" if plan == "Instant" else "live"
        fdata.append([
            P(plan, s["tdl"]),
            P(pct(r["P_pay"]), s["td"]), P(pct(r["P_yr1"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["Rec"]), s["td"]),
            P(pct(r["Rec_m"], signed=True, digits=0), s["td"]),
            P(usd(r["Live"]), s["td"]),
            P(pct(r["Live_m"], signed=True, digits=0), s["td"]),
            P(f"{usd(lo)} / {usd(med)}", s["td"]),
        ])
    story.append(grid(fdata, [
        28*mm, 18*mm, 18*mm, 24*mm, 24*mm, 18*mm, 24*mm, 18*mm, 40*mm,
    ], fspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant rec $429 at $100k is the opex floor ($422) plus a small stub. "
        "1-Step +59%, Lite +33%, Pro +43% are leftover live VERO35 — unused pricing power, "
        "not a 40/60 target. Keep them: the evals are already the names shoppers sort cheap.",
        s["body"],
    ))

    md.append("## Plan / Size / List / Sale / E[X] / P(pay) / BE / 20% / 40% / 60% / Sale m\n")
    md.append("| Plan | Size | List | Sale | E[X] | P(pay) | BE | 20% | 40% | 60% | Sale m |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {usd(r['List'])} | {usd(r['Rec'])} | "
            f"{usd(r['E_used'])} | {pct(r['P_pay'])} | {usd(r['BE'])} | "
            f"{usd(r['px_20'])} | {usd(r['px_40'])} | {usd(r['px_60'])} | "
            f"{pct(r['Rec_m'], signed=True, digits=0)} |"
        )
    md.append("")
    md.append("Use 20 / 40 / 60 as the industry reference. Instant rec is opex-checked.\n")
    md.append("## Opex stack — 10% error, $1 + wage, marketing 20%, CAD 10k wages\n")
    md.append(
        "S_opex = (BE × 1.10 + $1 + wage) / 0.80. "
        "Wages CAD 10,000 × 0.72 = USD 7,200 / month on 310 weighted accounts.\n"
    )
    md.append("| Plan | Size | N | Wage | BE | +10% | Loaded | Opex $ | Peer low | Low OK | First OK | Rec | After |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|---:|")
    for r in opex_rows(skus):
        low_s = "—" if r["Low"] is None else f"{usd(r['Low'])} {r['Low_name']}"
        ok_s = "yes" if r["Low_ok"] else "NO"
        first_s = "—" if r["First_ok"] is None else f"{usd(r['First_ok'])} {r['First_ok_name']}"
        md.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {r['N']} | {usd(r['Wage'])} | "
            f"{usd(r['BE'])} | {usd(r['Error'])} | "
            f"{usd(r['Loaded'])} | {usd(r['S_opex'])} | {low_s} | {ok_s} | {first_s} | "
            f"{usd(r['Rec'])} | {usd(r['Rec_left'])} |"
        )
    md.append("")

    # markdown margins
    md.append("## Margin % by size and family\n")
    md.append("| Family | Size | Rec $ | BE $ | E[cost] | Rec m | Live $ | Live m |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {usd(r['Rec'])} | {usd(r['BE'])} | "
            f"{usd(r['Cost'])} | {pct(r['Rec_m'], signed=True, digits=0)} | "
            f"{usd(r['Live'])} | {pct(r['Live_m'], signed=True, digits=0)} |"
        )
    md.append("")
    md.append("## Family roll-up at $100k\n")
    md.append("| Family | P(pay) | Year-1 | BE | Rec | Rec m | Live | Live m |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for plan, _fam in ANCHORS:
        r = next(x for x in rows if x["Plan"] == plan and x["Size"] == 100000)
        md.append(
            f"| {plan} | {pct(r['P_pay'])} | {pct(r['P_yr1'])} | {usd(r['BE'])} | "
            f"{usd(r['Rec'])} | {pct(r['Rec_m'], signed=True, digits=0)} | "
            f"{usd(r['Live'])} | {pct(r['Live_m'], signed=True, digits=0)} |"
        )
    md.append("")
    md.append("PDF: `results/Verodus_Complete_Report_2026-08-16.pdf`\n")

    pd.DataFrame(rows).to_csv(RESULTS / "verodus_complete_margins.csv", index=False)
    MD.write_text("\n".join(md) + "\n")

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus complete operator report — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {MD}")
    print(f"Wrote {RESULTS / 'verodus_complete_margins.csv'}")


if __name__ == "__main__":
    build()
