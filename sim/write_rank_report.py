#!/usr/bin/env python3
"""One report: every Verodus and peer plan, break-even, 40%/60% rank."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_BE_Rank_Report_2026-08-16.pdf"

PAGE = landscape(A4)
W, H = PAGE
MARGIN = 11 * mm

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
RED = colors.HexColor("#9b1c1c")
GREEN = colors.HexColor("#14532d")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_V = colors.HexColor("#e8f1ff")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")


def usd(x):
    if pd.isna(x):
        return "—"
    return f"${float(x):,.0f}"


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    return skus.loc[~drop].copy()


def street_pool(skus, family, size):
    return skus[(skus.Family == family) & (skus.Size == size)]


def rank_in(price, sales):
    """Rank 1 = cheapest. Ties share the lower rank. n is the field size."""
    sales = [float(x) for x in sales if pd.notna(x)]
    cheaper = sum(1 for s in sales if s < float(price) - 1e-9)
    return cheaper + 1, len(sales)


def hypo_rank(price, peer_sales):
    """Where `price` would sit among peer street sales + itself."""
    field = [float(x) for x in peer_sales if pd.notna(x)]
    field.append(float(price))
    return rank_in(price, field)


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
            fontSize=13, leading=16, textColor=NAVY, spaceBefore=8, spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Times-Bold",
            fontSize=11, leading=13, textColor=TEAL, spaceBefore=6, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=8.5, leading=11, alignment=TA_JUSTIFY, spaceAfter=4,
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
            fontSize=7.2, leading=9.2, textColor=colors.HexColor("#334155"),
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(MARGIN, H - 5.4 * mm,
                      "VERODUS  ·  Break-even & 40% / 60% rank vs every peer plan  ·  16 Aug 2026")
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(MARGIN, 2.6 * mm,
                      "Rank 1 = cheapest. Rank is among the same family and size. (k/n) beside the price.")
    canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def P(text, style):
    return Paragraph(text, style)


def grid(data, col_w, verodus_rows=None):
    verodus_rows = verodus_rows or set()
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
        if i in verodus_rows:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_V))
            sty.append(("FONTNAME", (0, i), (-1, i), "Times-Bold"))
        elif i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def priced(price, rank, n):
    return f"{usd(price)} ({rank}/{n})"


def build():
    skus = load()
    s = styles()
    story = []

    story.append(P("Break-even and rank at 40% / 60% pricing", s["cover"]))
    story.append(P(
        "Every Verodus plan and every competitor plan in the 20-firm book. "
        "Same family, same size. Rank 1 = cheapest street price. 16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "Break-even (BE) is the fee that sets expected contribution to zero after payouts "
        "and refunds on this book. <b>40%</b> and <b>60%</b> are the fees that deliver those "
        "contribution margins: fee = BE / (1 − m). Street is what the shopper pays today "
        "(VERO35, BG25, HELLO, MATCH20, FUNDED40, or the typical ~20% promo). "
        "Rank in parentheses is among all products in that <b>family + size</b> "
        "(Instant vs Instant $100k, not Instant vs a 2-step). "
        "For Verodus @40% and @60%, the rank is where that fee would sit against "
        "everyone else’s <b>current street sale</b> plus that fee. "
        "Instant $200k is not offered.",
        s["body"],
    ))

    # ----- 1. Verodus scoreboard -----
    story.append(P("1. Verodus — if we price at 40% and at 60%", s["h1"]))
    story.append(P(
        "This is the decision table. Street (rk) is today’s VERO35 rank. "
        "@40% (rk) and @60% (rk) are the hypothetical ranks if we moved to those fees "
        "and every peer kept today’s sale.",
        s["body"],
    ))
    score_h = [P(x, s["th"]) for x in [
        "Plan", "Size", "BE", "Street (rk)", "@40% (rk)", "@60% (rk)",
        "Peers n", "Peer cheapest", "Peer median", "Peer dearest",
    ]]
    score = [score_h]
    vset = set()
    fam_ord = {"instant": 0, "1-step": 1, "2-step": 2, "3-step": 3}
    plan_ord = {"Instant": 0, "1-Step": 1, "2-Step Lite": 2, "2-Step Pro": 3}
    v = skus[skus.Firm == "Verodus"].copy()
    v["_fo"] = v.Family.map(fam_ord)
    v["_po"] = v.Plan.map(plan_ord)
    v = v.sort_values(["_fo", "_po", "Size"])
    for i, r in enumerate(v.itertuples(), start=1):
        pool = street_pool(skus, r.Family, r.Size)
        peer_sales = pool.loc[pool.Firm != "Verodus", "Sale"]
        all_sales = pool["Sale"]
        sr, sn = rank_in(r.Sale, all_sales)
        r40, n40 = hypo_rank(r.px_40, peer_sales)
        r60, n60 = hypo_rank(r.px_60, peer_sales)
        vset.add(i)
        score.append([
            P(str(r.Plan), s["tdl"]),
            P(usd(r.Size), s["td"]),
            P(usd(r.BE), s["td"]),
            P(priced(r.Sale, sr, sn), s["td"]),
            P(priced(r.px_40, r40, n40), s["td"]),
            P(priced(r.px_60, r60, n60), s["td"]),
            P(str(len(peer_sales)), s["td"]),
            P(usd(peer_sales.min()) if len(peer_sales) else "—", s["td"]),
            P(usd(peer_sales.median()) if len(peer_sales) else "—", s["td"]),
            P(usd(peer_sales.max()) if len(peer_sales) else "—", s["td"]),
        ])
    story.append(grid(score, [
        28*mm, 18*mm, 18*mm, 28*mm, 28*mm, 28*mm, 16*mm, 26*mm, 24*mm, 24*mm,
    ], verodus_rows=vset))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Read the parenthesis as “cheapest-to-dearest place in this family and size.” "
        "Instant @40% is mid-to-dear because a solvent Instant fee sits above the "
        "loss-leading street (BG $54/$467, FP Zero $48/$444, Alpha $40/$274). "
        "1-Step and both 2-steps @40% stay near the cheap end — unused pricing power. "
        "@60% on Instant is the top of the field at $25k+; @60% on 1-Step / Lite / Pro "
        "is still inside the pack.",
        s["body"],
    ))

    # ----- 2–5. Full field by family -----
    fams = [
        ("instant", "2. Instant / straight-to-funded — every plan"),
        ("1-step", "3. One-step — every plan"),
        ("2-step", "4. Two-step — every plan"),
        ("3-step", "5. Three-step — every plan"),
    ]
    for fam, title in fams:
        story.append(P(title, s["h1"]))
        story.append(P(
            "Every SKU in this family. BE is that product’s own break-even. "
            "Street (rk) is today’s shopper price and its rank in this size. "
            "@40% (rk) and @60% (rk) on a Verodus row are our hypothetical fees. "
            "On a peer row those two columns are that peer’s own 40% / 60% fees "
            "from the same book (no rank — the rank question is ours).",
            s["body"],
        ))
        sub = skus[skus.Family == fam].sort_values(["Size", "Sale", "Firm", "Plan"])
        data = [[P(x, s["th"]) for x in [
            "Firm", "Plan", "Size", "BE", "Street (rk)",
            "Verodus @40% (rk)  /  peer 40%",
            "Verodus @60% (rk)  /  peer 60%",
            "P(pay)",
        ]]]
        vrows = set()
        for i, r in enumerate(sub.itertuples(), start=1):
            pool = street_pool(skus, r.Family, r.Size)
            sr, sn = rank_in(r.Sale, pool["Sale"])
            if r.Firm == "Verodus":
                peer_sales = pool.loc[pool.Firm != "Verodus", "Sale"]
                r40, n40 = hypo_rank(r.px_40, peer_sales)
                r60, n60 = hypo_rank(r.px_60, peer_sales)
                c40 = priced(r.px_40, r40, n40)
                c60 = priced(r.px_60, r60, n60)
                vrows.add(i)
            else:
                c40 = usd(r.px_40)
                c60 = usd(r.px_60)
            data.append([
                P(str(r.Firm), s["tdl"]),
                P(str(r.Plan), s["tdl"]),
                P(usd(r.Size), s["td"]),
                P(usd(r.BE), s["td"]),
                P(priced(r.Sale, sr, sn), s["td"]),
                P(c40, s["td"]),
                P(c60, s["td"]),
                P(f"{100 * float(r.P_pay):.1f}%", s["td"]),
            ])
        story.append(grid(data, [
            32*mm, 36*mm, 18*mm, 20*mm, 32*mm, 48*mm, 48*mm, 16*mm,
        ], verodus_rows=vrows))
        story.append(Spacer(1, 3*mm))

    story.append(P("6. How to use the ranks", s["h1"]))
    story.append(P(
        "A cheap rank at @40% (1-Step, Lite, Pro) means we can raise toward 40% and still "
        "look inexpensive next to FTMO / FundedNext / Hola. A dear rank at @40% on Instant "
        "means a solvent Instant fee will not win a price war — and should not try. "
        "Peers whose street is far below their own BE (red Instant $25k–$100k at BG, "
        "FundingPips Zero, Alpha) are not a rank to chase. "
        "Same book for every row: 7% Pro / 22% Semi-skilled / 26% Average / 28% Aggressive / "
        "17% Lottery. Sources and rule cards live in the industry Monte Carlo notes; "
        "this report is only BE, street, and rank.",
        s["body"],
    ))
    story.append(P(
        "Book: results/industry_skus.csv · Engine: sim/industry_book.py · "
        "Catalog: sim/catalog.py · Instant $200k removed · Lite funded DD 8% · "
        "Blue Guardian Instant = live BG25.",
        s["tiny"],
    ))

    # also write a CSV the operator can sort
    rows = []
    for r in skus.sort_values(["Family", "Size", "Sale", "Firm"]).itertuples():
        pool = street_pool(skus, r.Family, r.Size)
        sr, sn = rank_in(r.Sale, pool["Sale"])
        rec = {
            "Family": r.Family,
            "Firm": r.Firm,
            "Plan": r.Plan,
            "Size": int(r.Size),
            "BE": round(float(r.BE), 2),
            "Street": float(r.Sale),
            "Street_rank": sr,
            "Street_n": sn,
            "px_40": round(float(r.px_40), 2),
            "px_60": round(float(r.px_60), 2),
            "P_pay": float(r.P_pay),
        }
        if r.Firm == "Verodus":
            peer_sales = pool.loc[pool.Firm != "Verodus", "Sale"]
            rec["rank_at_40"], rec["n_at_40"] = hypo_rank(r.px_40, peer_sales)
            rec["rank_at_60"], rec["n_at_60"] = hypo_rank(r.px_60, peer_sales)
        else:
            rec["rank_at_40"] = rec["n_at_40"] = rec["rank_at_60"] = rec["n_at_60"] = None
        rows.append(rec)
    pd.DataFrame(rows).to_csv(RESULTS / "verodus_be_ranks.csv", index=False)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus break-even and 40%/60% rank vs every peer — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {RESULTS / 'verodus_be_ranks.csv'}")


if __name__ == "__main__":
    build()
