#!/usr/bin/env python3
"""In-band competitor street prices + recommended Verodus sale card."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from difficulty import DELTA, scores_for_book

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Recommended_Prices_2026-08-16.pdf"

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

SIZES = (5000, 10000, 25000, 50000, 100000, 200000)

# Difficulty-banded recommendation (VERO35 sale). Instant $25k+ is the
# 20% print floor. Evals match the cheap same-D peer (Hola / Ment / Goat).
REC = {
    ("Instant", 5000): 72,
    ("Instant", 10000): 121,
    ("Instant", 25000): 274,
    ("Instant", 50000): 547,
    ("Instant", 100000): 1094,
    ("1-Step", 5000): 47,
    ("1-Step", 10000): 71,
    ("1-Step", 25000): 149,
    ("1-Step", 50000): 249,
    ("1-Step", 100000): 449,
    ("1-Step", 200000): 829,
    ("2-Step Lite", 5000): 31,
    ("2-Step Lite", 10000): 55,
    ("2-Step Lite", 25000): 119,
    ("2-Step Lite", 50000): 199,
    ("2-Step Lite", 100000): 343,
    ("2-Step Lite", 200000): 549,
    ("2-Step Pro", 5000): 29,
    ("2-Step Pro", 10000): 53,
    ("2-Step Pro", 25000): 125,
    ("2-Step Pro", 50000): 213,
    ("2-Step Pro", 100000): 399,
    ("2-Step Pro", 200000): 749,
}

ANCHORS = (
    ("Instant", "instant", "Instant Funding, Hola Direct, Goat, FP Zero, FXIFY Lite, Alpha Instant, Blue Guardian. Out: FN Instant, FXIFY Standard (no daily)."),
    ("1-Step", "1-step", "Hola 1-Step, FundedNext 1-Step, FTMO 1-Step, 5ers Hyper Growth. Out: FP Flex, Alpha One, E8."),
    ("2-Step Lite", "2-step", "FundedNext Lite, Ment, For Traders, FXIFY 2-Step. Out: FTMO-class / Pro (D ~63)."),
    ("2-Step Pro", "2-step", "FTMO, FN, Maven, FP Standard/Flex, Alpha Pro 10%, Goat, Hola, TFT, BrightFunded, CTI, Fintokei, Funding Traders, 5ers High Stakes. Out: Lite-class, Alpha Pro 6%."),
)

WHY = {
    "Instant": (
        "D 89.2 — hardest Verodus line. Same 22% P(pay) as Blue Guardian, but five points "
        "harder (peak daily, trail never locks). $5k / $10k already print and sit between "
        "Goat and Hola. From $25k, live is +10% / −13% / −29%. The 20% floor lands on Hola "
        "at $25k–$50k. At $100k, Hola $839 and Instant Funding $639 lose money; matching "
        "BG $467 is a −95% product. Charge like Hola, not like BG. No $200k Instant."
    ),
    "1-Step": (
        "D 81.5 — same as FundedNext 1-Step (81.9), slightly harder than FTMO (78.9), "
        "slightly easier than Hola (85.9). Live already prints +58–76% and is the cheapest "
        "in the band. We are not an easier product than FTMO, so $335 vs $579 is a gift. "
        "Price to Hola; stay well under FN / FTMO."
    ),
    "2-Step Lite": (
        "D 77.7 — same as FundedNext Lite (77.1), Ment (77.3), For Traders (77.4). Live is "
        "the cheapest in the band by a wide gap. $241 vs Ment $343 / FN $449 underprices "
        "the same product. Match Ment (cheap same-D peer); stay under FN Lite."
    ),
    "2-Step Pro": (
        "D 64.0 — same as FTMO 2-Step (63.2) and FN 2-Step (63.2). Live is #2 cheapest "
        "after Maven. We do not have FTMO’s brand, so do not go to $626. Price like Goat / "
        "Funding Traders (D 62.7–62.8): mid-cheap in the FTMO class, still $227 under FTMO "
        "at $100k. Skip Maven’s race to the bottom."
    ),
}


def usd(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    return f"${float(x):,.0f}"


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    skus = skus.loc[~drop].copy()
    pp = dict(zip(blend.Product, blend.P_pay))
    sc = pd.DataFrame(scores_for_book(pp).values())
    skus = skus.merge(sc[["Product", "D"]], on="Product", how="left")
    return skus, sc


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
            fontSize=8.4, leading=11, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=6.6, leading=8.2, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.6, leading=8.2, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.6, leading=8.2, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.1, leading=9.1, textColor=colors.HexColor("#334155"),
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
        f"VERODUS  ·  In-band street + recommended sale  ·  band ±{DELTA:.0f}  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        f"Compare only same family + size and |ΔD| ≤ {DELTA:.0f}. Rec sale is VERO35 (list = sale ÷ 0.65).",
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
        ("FONTSIZE", (0, 0), (-1, -1), 6.6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 1.6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.6),
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


def vero_d(scored, plan):
    key = {
        "Instant": "Verodus Instant",
        "1-Step": "Verodus 1-Step",
        "2-Step Lite": "Verodus 2-Step Lite",
        "2-Step Pro": "Verodus 2-Step Pro",
    }[plan]
    return float(scored.loc[scored.Product == key, "D"].iloc[0])


def in_band(skus, plan, family, d0):
    return skus[
        (skus.Family == family)
        & (skus.Firm != "Verodus")
        & (skus.D.notna())
        & ((skus.D - d0).abs() <= DELTA)
    ]


def sale_map(frame):
    out = {}
    for r in frame.itertuples():
        out[(r.Firm, r.Plan, int(r.Size))] = float(r.Sale)
    return out


def e_cost(skus, plan, size):
    row = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == size)]
    if row.empty:
        return None
    return float(row.E_cost.iloc[0])


def margin(sale, cost):
    if sale is None or cost is None or sale <= 0:
        return "—"
    return f"{100.0 * (sale - cost) / sale:+.0f}%"


def build():
    skus, scored = load()
    s = styles()
    story = []

    story.append(P("In-band competitor prices and recommended Verodus card", s["cover"]))
    story.append(P(
        f"Street fees only for plans with |D − D_Verodus| ≤ {DELTA:.0f} (same family). "
        "Recommended sale factors difficulty: harder in-band plans can charge more; "
        "easier holes are ignored. 16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        f"<b>D = 0.55 × rules + 0.45 × book.</b> Band ±{DELTA:.0f} is about one daily-DD "
        "step. Instant $25k+ must print (20% column). 1-Step / Lite / Pro already print "
        "at live VERO35; those raises take unused power so we stop selling a same-D "
        "product cheaper than Hola / Ment / Goat. List = sale ÷ 0.65. Instant $200k pulled.",
        s["body"],
    ))

    # ----- 1. recommended card -----
    story.append(P("1. Recommended Verodus sale (VERO35)", s["h1"]))
    heads = ["Plan", "D", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k",
             "Live $100k", "Rec m $100k", "Anchor"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    anchors_why = {
        "Instant": "20% print floor; Hola-class, not BG",
        "1-Step": "Hola street; under FN / FTMO",
        "2-Step Lite": "Ment street; under FN Lite",
        "2-Step Pro": "Goat / Funding Traders; under FTMO",
    }
    for i, (plan, _fam, _peers) in enumerate(ANCHORS, start=1):
        d0 = vero_d(scored, plan)
        live100 = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == 100000)]
        live_s = float(live100.Sale.iloc[0]) if not live100.empty else None
        rec100 = REC.get((plan, 100000))
        cost100 = e_cost(skus, plan, 100000)
        cells = [P(plan, s["tdl"]), P(f"{d0:.1f}", s["td"])]
        for sz in SIZES:
            cells.append(P(usd(REC.get((plan, sz))), s["td"]))
        cells.append(P(usd(live_s), s["td"]))
        cells.append(P(margin(rec100, cost100), s["td"]))
        cells.append(P(anchors_why[plan], s["tdl"]))
        data.append(cells)
        special[i] = "rec"
    story.append(grid(data, [
        26*mm, 12*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm, 20*mm, 22*mm, 22*mm, 56*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = recommended sale. Instant $5k / $10k stay at live (already above the "
        "print floor). Every other Instant size moves up. Eval raises are optional power — "
        "live still prints if you hold today’s card.",
        s["body"],
    ))

    # ----- 2–5. in-band street per plan -----
    for n, (plan, family, peer_txt) in enumerate(ANCHORS, start=2):
        d0 = vero_d(scored, plan)
        peers = in_band(skus, plan, family, d0)
        products = (
            peers.drop_duplicates("Product")
            .sort_values(["D", "Firm"])
        )
        live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan)]
        story.append(P(f"{n}. {plan} — in-band street (D {d0:.1f})", s["h1"]))
        story.append(P(WHY[plan], s["body"]))
        story.append(P(f"<i>In band:</i> {peer_txt}", s["tiny"]))

        heads = ["Firm", "Plan", "D", "ΔD", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
        data = [[P(h, s["th"]) for h in heads]]
        special = {}
        sales = sale_map(peers)
        live_sales = sale_map(live)

        def row_cells(firm, plan_name, d, sales_lookup, tag=None):
            cells = [
                P(firm, s["tdl"]),
                P(plan_name, s["tdl"]),
                P(f"{d:.1f}", s["td"]),
                P(f"{abs(d - d0):.1f}", s["td"]),
            ]
            for sz in SIZES:
                cells.append(P(usd(sales_lookup.get((firm, plan_name, sz))), s["td"]))
            return cells

        for r in products.itertuples():
            data.append(row_cells(r.Firm, r.Plan, float(r.D), sales))

        live_d = d0
        live_plan = plan
        data.append(row_cells("Verodus", live_plan, live_d, live_sales))
        special[len(data) - 1] = "live"

        rec_cells = [
            P("Verodus rec", s["tdl"]),
            P(plan, s["tdl"]),
            P(f"{d0:.1f}", s["td"]),
            P("0.0", s["td"]),
        ]
        for sz in SIZES:
            rec_cells.append(P(usd(REC.get((plan, sz))), s["td"]))
        data.append(rec_cells)
        special[len(data) - 1] = "rec"

        story.append(grid(data, [
            32*mm, 36*mm, 14*mm, 14*mm, 20*mm, 20*mm, 20*mm, 20*mm, 22*mm, 22*mm,
        ], special))
        story.append(Spacer(1, 2*mm))

    # ----- 6. list prices + live vs rec -----
    story.append(P("6. List (VERO35) and live vs recommended", s["h1"]))
    story.append(P(
        "Shopper pays sale. List = sale ÷ 0.65 so VERO35 still lands on the card. "
        "Margin uses this book’s E[cost] (payout + expected refund).",
        s["body"],
    ))
    heads = ["Plan", "Size", "Live sale", "Live m", "Rec sale", "Rec list", "Rec m",
             "Δ sale", "20% floor", "Must move?"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    rows_out = []
    i = 0
    for plan, _fam, _ in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            r = live.iloc[0]
            rec = REC[(plan, sz)]
            cost = float(r.E_cost)
            floor20 = float(r.px_20)
            must = "yes — print" if (plan == "Instant" and rec > float(r.Sale) + 0.5) else "no"
            i += 1
            if rec > float(r.Sale) + 0.5:
                special[i] = "rec"
            elif abs(rec - float(r.Sale)) < 0.5:
                special[i] = "live"
            data.append([
                P(plan, s["tdl"]),
                P(usd(sz), s["td"]),
                P(usd(r.Sale), s["td"]),
                P(f"{100 * float(r.sale_m):+.0f}%", s["td"]),
                P(usd(rec), s["td"]),
                P(usd(round(rec / 0.65)), s["td"]),
                P(margin(rec, cost), s["td"]),
                P(usd(rec - float(r.Sale)), s["td"]),
                P(usd(floor20), s["td"]),
                P(must, s["td"]),
            ])
            rows_out.append({
                "Plan": plan, "Size": sz, "D": vero_d(scored, plan),
                "Live_sale": float(r.Sale), "Live_m": float(r.sale_m),
                "Rec_sale": rec, "Rec_list": round(rec / 0.65),
                "Rec_m": (rec - cost) / rec, "E_cost": cost,
                "px_20": floor20, "Must_move": must,
            })
    story.append(grid(data, [
        26*mm, 18*mm, 22*mm, 18*mm, 22*mm, 20*mm, 18*mm, 20*mm, 22*mm, 24*mm,
    ], special))
    story.append(Spacer(1, 2.5*mm))
    story.append(P(
        "Blue = live already equals rec. Green = raise. Instant $25k / $50k / $100k are "
        "the only must-moves. Out of band and ignored: FundedNext Instant, FXIFY Instant "
        "Standard, FP 1-Step Flex, Alpha One, E8, Lite vs FTMO/Pro, Alpha Pro 6%. "
        "Same book 7/22/26/28/17. Formula: sim/difficulty.py.",
        s["tiny"],
    ))

    pd.DataFrame(rows_out).to_csv(RESULTS / "verodus_recommended_prices.csv", index=False)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus in-band prices and recommended card — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {RESULTS / 'verodus_recommended_prices.csv'}")


if __name__ == "__main__":
    build()
