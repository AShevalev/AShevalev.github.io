#!/usr/bin/env python3
"""One report: BE and 40%/60% rank vs like-for-like plans, difficulty-adjusted."""

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
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_V = colors.HexColor("#e8f1ff")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")

# Rule cohorts. Family name is not enough: no-daily Instant is not a 3%/6% Instant.
COHORT = {
    "Verodus Instant": "instant_3_6",
    "BG Instant": "instant_3_6",
    "IF Instant": "instant_3_6",
    "Goat Instant": "instant_3_6",
    "Alpha Instant": "instant_3_6",
    "FP Zero": "instant_3_6",
    "FXIFY Instant Lite": "instant_3_6",
    "Hola Direct": "instant_3_6",
    "FN Stellar Instant": "instant_no_daily",
    "FXIFY Instant": "instant_no_daily",
    "Verodus 1-Step": "onestep_6",
    "Alpha One 10%": "onestep_6",
    "E8 One 6%": "onestep_6",
    "E8 Signature": "onestep_6",
    "Hola 1-Step Prime": "onestep_6",
    "Fintokei SwiftTrader": "onestep_6",
    "TFT Royal": "onestep_6",
    "FN Stellar 1-Step": "onestep_6",
    "FTMO 1-Step": "onestep_10",
    "FP 1-Step Flex": "onestep_12",
    "BG 1-Step": "onestep_8",
    "5ers Hyper Growth": "onestep_other",
    "Verodus 2-Step Lite": "twostep_8",
    "FN Stellar Lite": "twostep_8",
    "ForTraders 2-Step": "twostep_8",
    "Ment 2-Step": "twostep_8",
    "Verodus 2-Step Pro": "twostep_10",
    "FTMO 2-Step": "twostep_10",
    "FN Stellar 2-Step": "twostep_10",
    "FP 2-Step Standard": "twostep_10",
    "Alpha Pro 10%": "twostep_10",
    "Goat 2-Step": "twostep_10",
    "Maven 2-Step": "twostep_10",
    "Hola 2-Step Prime": "twostep_10",
    "TFT Standard": "twostep_10",
    "CTI 2-Step": "twostep_10",
    "FundingTraders 2-Step": "twostep_10",
    "BG 2-Step": "twostep_10",
    "BrightFunded 2-Step": "twostep_10",
    "Fintokei ProTrader": "twostep_10",
    "FXIFY 2-Step": "twostep_10",
    "FP 2-Step Pro": "twostep_6",
    "Alpha Pro 6%": "twostep_6",
    "FP 2-Step Flex": "twostep_12",
    "Maven 3-Step": "threestep",
    "5ers Bootcamp": "threestep",
    "5ers High Stakes": "twostep_10",
}

COHORT_LABEL = {
    "instant_3_6": "Instant 3% daily / ~5–7% trail (like Verodus Instant)",
    "instant_no_daily": "Instant with no daily — not like Verodus (P(pay) ~53%)",
    "onestep_6": "1-step 6% max DD (like Verodus 1-Step hybrid)",
    "onestep_8": "1-step 8% static — looser than Verodus 1-Step",
    "onestep_10": "1-step 10% trail (FTMO) — easier than Verodus 1-Step",
    "onestep_12": "1-step 12% (FP Flex) — not like Verodus 1-Step",
    "onestep_other": "1-step other (50% split / live-from-day-1)",
    "twostep_8": "2-step 8% static (like Verodus Lite)",
    "twostep_10": "2-step 10% / 5% daily (like Verodus Pro / FTMO)",
    "twostep_6": "2-step 6/6 tight — harder than Verodus Pro",
    "twostep_12": "2-step 12% Flex — easier than Verodus Pro",
    "threestep": "3-step — Verodus does not offer this",
}

VERO_PLAN = {
    "instant_3_6": "Instant",
    "onestep_6": "1-Step",
    "twostep_8": "2-Step Lite",
    "twostep_10": "2-Step Pro",
}

COHORT_ORDER = [
    "instant_3_6", "instant_no_daily",
    "onestep_6", "onestep_8", "onestep_10", "onestep_12", "onestep_other",
    "twostep_8", "twostep_10", "twostep_6", "twostep_12",
    "threestep",
]


def usd(x):
    if pd.isna(x):
        return "—"
    return f"${float(x):,.0f}"


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    skus = skus.loc[~drop].copy()
    skus["Cohort"] = skus.Product.map(COHORT).fillna("other")
    return skus


def rank_in(price, sales):
    sales = [float(x) for x in sales if pd.notna(x)]
    cheaper = sum(1 for s in sales if s < float(price) - 1e-9)
    return cheaper + 1, len(sales)


def hypo_rank(price, peer_sales):
    field = [float(x) for x in peer_sales if pd.notna(x)]
    field.append(float(price))
    return rank_in(price, field)


def diff_label(peer_be, ref_be):
    if ref_be <= 0 or pd.isna(peer_be) or pd.isna(ref_be):
        return "—"
    ratio = float(peer_be) / float(ref_be)
    if ratio > 1.15:
        return "Easier"
    if ratio < 0.85:
        return "Harder"
    return "Similar"


def adj_sale(peer_sale, peer_be, ref_be):
    if peer_be is None or pd.isna(peer_be) or float(peer_be) <= 0:
        return float(peer_sale)
    return float(peer_sale) * (float(ref_be) / float(peer_be))


def ref_be_for(skus, vero_plan, size):
    hit = skus[(skus.Firm == "Verodus") & (skus.Plan == vero_plan) & (skus.Size == size)]
    if hit.empty:
        return None
    return float(hit.BE.iloc[0])


def like_pool(skus, cohort, size):
    return skus[(skus.Cohort == cohort) & (skus.Size == size)]


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
            fontSize=6.5, leading=8.1, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.5, leading=8.1, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.5, leading=8.1, alignment=TA_LEFT,
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
        "VERODUS  ·  Like-for-like BE rank at 40% / 60%  ·  difficulty-adjusted  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Rank 1 = cheapest. Ranks are inside the rule cohort, after scaling street by BE. (k/n) beside the price.",
    )
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
        ("FONTSIZE", (0, 0), (-1, -1), 6.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 1.7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.7),
        ("LEFTPADDING", (0, 0), (-1, -1), 1.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.5),
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


def vero_like_ranks(skus, r):
    """Difficulty-adjusted ranks of Verodus 40%/60% inside the like cohort."""
    pool = like_pool(skus, r.Cohort, r.Size)
    peers = pool[pool.Firm != "Verodus"]
    adj = []
    for p in peers.itertuples():
        adj.append(adj_sale(p.Sale, p.BE, r.BE))
    r40, n40 = hypo_rank(r.px_40, adj)
    r60, n60 = hypo_rank(r.px_60, adj)
    raw_r, raw_n = rank_in(r.Sale, pool["Sale"])
    return raw_r, raw_n, r40, n40, r60, n60, peers


def build():
    skus = load()
    s = styles()
    story = []

    story.append(P("Like-for-like break-even rank at 40% / 60%", s["cover"]))
    story.append(P(
        "Family name is not enough. Ranks below are only against plans with comparable "
        "rules, then street is scaled by break-even so an easier plan does not look cheap. "
        "16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "<b>They were not all comparable.</b> The first rank report put every Instant in "
        "one pool — including FundedNext / FXIFY Standard, which have <b>no daily</b> and "
        "P(pay) ~53% versus Verodus Instant 22%. It also mixed Verodus Lite (8% static) "
        "with FTMO / FP Pro (10% or 6/6). Those are different products. "
        "This revision groups by the binding rules, then difficulty-adjusts.",
        s["body"],
    ))
    story.append(P(
        "<b>Difficulty adjustment.</b> Adj street = peer sale × (Verodus BE / peer BE) "
        "at the same size. A peer with a higher BE (easier / richer payouts / refund) "
        "has its sticker scaled down — they are cheaper than they look for the risk they "
        "take. A harder peer (lower BE) has its sticker scaled up. "
        "Easier / Similar / Harder is peer BE vs Verodus BE: &gt;1.15× easier, "
        "&lt;0.85× harder. "
        "Verodus @40% and @60% ranks are against those <b>adjusted</b> like-for-like "
        "street prices. Rank 1 = cheapest. Instant $200k is not offered.",
        s["body"],
    ))

    # ----- 1. Verodus scoreboard -----
    story.append(P("1. Verodus — 40% / 60% rank vs like-for-like only", s["h1"]))
    story.append(P(
        "Parentheses are the difficulty-adjusted rank inside the rule cohort. "
        "Street (rk) is raw rank among those same like plans (no adjustment).",
        s["body"],
    ))
    score = [[P(x, s["th"]) for x in [
        "Plan", "Like cohort", "Size", "BE", "Street (raw rk)",
        "@40% vs like (rk)", "@60% vs like (rk)", "Like n",
        "Like cheapest adj", "Like dearest adj",
    ]]]
    vset = set()
    plan_ord = {"Instant": 0, "1-Step": 1, "2-Step Lite": 2, "2-Step Pro": 3}
    v = skus[skus.Firm == "Verodus"].copy()
    v["_po"] = v.Plan.map(plan_ord)
    v = v.sort_values(["_po", "Size"])
    for i, r in enumerate(v.itertuples(), start=1):
        raw_r, raw_n, r40, n40, r60, n60, peers = vero_like_ranks(skus, r)
        adjs = [adj_sale(p.Sale, p.BE, r.BE) for p in peers.itertuples()]
        vset.add(i)
        score.append([
            P(str(r.Plan), s["tdl"]),
            P(COHORT_LABEL.get(r.Cohort, r.Cohort).split(" (")[0], s["tdl"]),
            P(usd(r.Size), s["td"]),
            P(usd(r.BE), s["td"]),
            P(priced(r.Sale, raw_r, raw_n), s["td"]),
            P(priced(r.px_40, r40, n40), s["td"]),
            P(priced(r.px_60, r60, n60), s["td"]),
            P(str(len(peers)), s["td"]),
            P(usd(min(adjs)) if adjs else "—", s["td"]),
            P(usd(max(adjs)) if adjs else "—", s["td"]),
        ])
    story.append(grid(score, [
        24*mm, 48*mm, 16*mm, 16*mm, 28*mm, 32*mm, 32*mm, 16*mm, 28*mm, 28*mm,
    ], verodus_rows=vset))
    story.append(Spacer(1, 3*mm))

    # ----- cohort tables -----
    n = 2
    for cohort in COHORT_ORDER:
        sub = skus[skus.Cohort == cohort]
        if sub.empty:
            continue
        vero_plan = VERO_PLAN.get(cohort)
        like = "like Verodus" if vero_plan else "not a Verodus twin — shown, not used in our rank"
        story.append(P(f"{n}. {COHORT_LABEL[cohort]}", s["h1"]))
        n += 1
        story.append(P(
            f"{like}. Adj $ puts the peer’s street into Verodus-BE dollars at that size. "
            "Verodus @40% / @60% ranks use those Adj $ figures."
            if vero_plan else
            "No Verodus product sits in this cohort. Listed so the book is complete. "
            "Do not use these stickers as a Verodus price signal.",
            s["body"],
        ))
        data = [[P(x, s["th"]) for x in [
            "Firm", "Plan", "Size", "BE", "P(pay)", "Diff vs Vero",
            "Street", "Adj $", "Vero @40% (rk) / peer 40%",
            "Vero @60% (rk) / peer 60%",
        ]]]
        vrows = set()
        sub = sub.sort_values(["Size", "Sale", "Firm"])
        for i, r in enumerate(sub.itertuples(), start=1):
            ref = ref_be_for(skus, vero_plan, r.Size) if vero_plan else None
            if ref:
                dlab = "—" if r.Firm == "Verodus" else diff_label(r.BE, ref)
                adj = float(r.Sale) if r.Firm == "Verodus" else adj_sale(r.Sale, r.BE, ref)
            else:
                dlab, adj = "—", float(r.Sale)
            if r.Firm == "Verodus":
                _, _, r40, n40, r60, n60, _ = vero_like_ranks(skus, r)
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
                P(f"{100 * float(r.P_pay):.1f}%", s["td"]),
                P(dlab, s["td"]),
                P(usd(r.Sale), s["td"]),
                P(usd(adj), s["td"]),
                P(c40, s["td"]),
                P(c60, s["td"]),
            ])
        story.append(grid(data, [
            30*mm, 32*mm, 16*mm, 16*mm, 14*mm, 22*mm, 18*mm, 18*mm, 42*mm, 42*mm,
        ], verodus_rows=vrows))
        story.append(Spacer(1, 2.5*mm))

    story.append(P(f"{n}. How to read difficulty", s["h1"]))
    story.append(P(
        "Blue Guardian Instant is the only Instant that is both the same card "
        "(3% / 6% / 20%) and Similar on BE ($911 vs our $875 at $100k). Their trail "
        "locks and daily is SOD, so they are a touch easier — Adj $ at $100k is $448 "
        "versus street $467. Ranking us against them is fair. "
        "FundingPips Zero and Alpha Instant are the same 3%-daily class but slightly "
        "harder on this book (lower P(pay)); Adj $ rises versus raw street, and they "
        "are still a hole. "
        "FundedNext Instant and FXIFY Standard stay in their own table: no daily is "
        "not our Instant. "
        "1-Step: rank against the 6% max-DD set (Hola, Alpha One, E8, FN, Fintokei, TFT), "
        "not against FTMO’s 10% trail or FP Flex 12%. "
        "Lite: only the 8% static 2-steps. Pro: the 10%/5% FTMO-class set, not FP Pro 6/6.",
        s["body"],
    ))
    story.append(P(
        "Book: results/industry_skus.csv · Cohorts: sim/write_rank_report.py · "
        "Adj $ = street × (Verodus BE / peer BE) · Instant $200k removed · Lite funded 8% · "
        "BG Instant = live BG25.",
        s["tiny"],
    ))

    rows = []
    for r in skus.sort_values(["Cohort", "Size", "Sale"]).itertuples():
        vero_plan = VERO_PLAN.get(r.Cohort)
        ref = ref_be_for(skus, vero_plan, r.Size) if vero_plan else None
        rec = {
            "Cohort": r.Cohort,
            "Firm": r.Firm,
            "Plan": r.Plan,
            "Size": int(r.Size),
            "BE": round(float(r.BE), 2),
            "Street": float(r.Sale),
            "P_pay": float(r.P_pay),
            "Diff": diff_label(r.BE, ref) if ref and r.Firm != "Verodus" else "—",
            "Adj_street": round(adj_sale(r.Sale, r.BE, ref), 2) if ref else None,
            "px_40": round(float(r.px_40), 2),
            "px_60": round(float(r.px_60), 2),
        }
        if r.Firm == "Verodus":
            raw_r, raw_n, r40, n40, r60, n60, _ = vero_like_ranks(skus, r)
            rec.update(
                street_rank=raw_r, street_n=raw_n,
                rank_at_40=r40, n_at_40=n40, rank_at_60=r60, n_at_60=n60,
            )
        rows.append(rec)
    pd.DataFrame(rows).to_csv(RESULTS / "verodus_be_ranks.csv", index=False)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus like-for-like BE rank at 40%/60% — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {RESULTS / 'verodus_be_ranks.csv'}")


if __name__ == "__main__":
    build()
