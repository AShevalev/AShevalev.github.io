#!/usr/bin/env python3
"""One report: difficulty score on every plan; 20%/30% rank only inside the band."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from difficulty import DELTA, comparable, scores_for_book
from write_price_rec_pdf import pricing_for

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


def usd(x):
    if pd.isna(x):
        return "—"
    return f"${float(x):,.0f}"


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    skus = skus.loc[~drop].copy()
    pp = dict(zip(blend.Product, blend.P_pay))
    sc = scores_for_book(pp)
    sdf = pd.DataFrame(sc.values())
    skus = skus.merge(sdf[["Product", "D", "D_rules", "D_book"]], on="Product", how="left")
    skus = skus.merge(blend[["Product", "P_yr1"]], on="Product", how="left")
    return skus, sdf.sort_values("D")


def rank_in(price, sales):
    sales = [float(x) for x in sales if pd.notna(x)]
    cheaper = sum(1 for s in sales if s < float(price) - 1e-9)
    return cheaper + 1, len(sales)


def hypo_rank(price, peer_sales):
    field = [float(x) for x in peer_sales if pd.notna(x)]
    field.append(float(price))
    return rank_in(price, field)


def band(skus, r):
    """Same family, same size, |D − D_vero| <= DELTA."""
    return skus[
        (skus.Family == r.Family)
        & (skus.Size == r.Size)
        & (skus.D.notna())
        & ((skus.D - r.D).abs() <= DELTA)
    ]


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
        f"VERODUS  ·  Difficulty score + 20%/30% rank  ·  band ±{DELTA:.0f}  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        f"D is 0–100 (higher = harder). Rank only if same family, same size, |ΔD| ≤ {DELTA:.0f}. Rank 1 = cheapest.",
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


def vero_ranks(skus, r):
    pool = band(skus, r)
    peers = pool[pool.Firm != "Verodus"]
    raw_r, raw_n = rank_in(r.Sale, pool["Sale"])
    pr = pricing_for(r)
    r20, n20 = hypo_rank(pr["px_20"], peers["Sale"])
    r30, n30 = hypo_rank(pr["px_30"], peers["Sale"])
    return raw_r, raw_n, r20, n20, r30, n30, peers, pr


def collect_story():
    skus, scored = load()
    s = styles()
    story = []

    story.append(P("Difficulty score and 20% / 30% rank", s["cover"]))
    story.append(P(
        f"Every plan gets a difficulty D (0–100). We only rank a peer if it is the "
        f"same family, the same size, and |D − D_Verodus| ≤ {DELTA:.0f}. "
        "16 August 2026.",
        s["sub"],
    ))
    v_d = {
        "Instant": float(scored.loc[scored.Product == "Verodus Instant", "D"].iloc[0]),
        "1-Step": float(scored.loc[scored.Product == "Verodus 1-Step", "D"].iloc[0]),
        "Lite": float(scored.loc[scored.Product == "Verodus 2-Step Lite", "D"].iloc[0]),
        "Pro": float(scored.loc[scored.Product == "Verodus 2-Step Pro", "D"].iloc[0]),
    }
    story.append(P(
        f"<b>D = 0.55 × rules + 0.45 × book.</b> Rules use the catalog card: daily DD "
        f"(none / 5% / 4% / 3% / 2%), day’s-high vs SOD, max DD, static vs hybrid vs "
        f"trail, trail lock (−4), consistency, target ÷ max DD, min days, 2% risk caps, "
        f"extra eval phases. Book is 100 × (1 − P(pay)) on this Monte Carlo. "
        f"Higher D = harder to get paid. "
        f"<b>Band ±{DELTA:.0f}</b> is about one daily-DD step after the 0.55 rule weight — "
        f"tight enough that no-daily Instant cannot sit next to Verodus Instant "
        f"(D {v_d['Instant']:.1f}), and Lite (D {v_d['Lite']:.1f}) cannot sit next to "
        f"Pro (D {v_d['Pro']:.1f}).",
        s["body"],
    ))

    # ----- 1. every plan's D -----
    story.append(P("1. Difficulty score — every plan", s["h1"]))
    story.append(P(
        "One row per product (D does not change with account size). "
        "Verodus rows highlighted. Sorted easiest → hardest.",
        s["body"],
    ))
    dtab = [[P(x, s["th"]) for x in [
        "Firm", "Plan", "Family", "D", "Rules", "Book", "P(pay)",
        "Δ vs Instant", "Δ vs 1-Step", "Δ vs Lite", "Δ vs Pro", "In a Vero band?",
    ]]]
    vset = set()
    for i, r in enumerate(scored.itertuples(), start=1):
        gaps = {k: abs(float(r.D) - v) for k, v in v_d.items()}
        in_band = []
        if r.Family == "instant" and gaps["Instant"] <= DELTA:
            in_band.append("Instant")
        if r.Family == "1-step" and gaps["1-Step"] <= DELTA:
            in_band.append("1-Step")
        if r.Family == "2-step" and gaps["Lite"] <= DELTA:
            in_band.append("Lite")
        if r.Family == "2-step" and gaps["Pro"] <= DELTA:
            in_band.append("Pro")
        if r.Firm == "Verodus":
            vset.add(i)
        dtab.append([
            P(str(r.Firm), s["tdl"]),
            P(str(r.Plan), s["tdl"]),
            P(str(r.Family), s["td"]),
            P(f"{float(r.D):.1f}", s["td"]),
            P(f"{float(r.D_rules):.0f}", s["td"]),
            P(f"{float(r.D_book):.0f}", s["td"]),
            P(f"{100 * float(r.P_pay):.1f}%", s["td"]),
            P(f"{gaps['Instant']:.1f}", s["td"]),
            P(f"{gaps['1-Step']:.1f}", s["td"]),
            P(f"{gaps['Lite']:.1f}", s["td"]),
            P(f"{gaps['Pro']:.1f}", s["td"]),
            P(", ".join(in_band) if in_band else "no", s["td"]),
        ])
    story.append(grid(dtab, [
        32*mm, 34*mm, 18*mm, 14*mm, 14*mm, 14*mm, 16*mm, 22*mm, 22*mm, 18*mm, 18*mm, 28*mm,
    ], verodus_rows=vset))
    story.append(Spacer(1, 3*mm))

    # ----- 2. Verodus 20/30 inside the band -----
    story.append(P(f"2. Verodus @20% / @30% — ranked only inside |ΔD| ≤ {DELTA:.0f}", s["h1"]))
    story.append(P(
        "Street (rk) is today’s VERO35 rank among the band. "
        "@20% (rk) and @30% (rk) are where those fees would sit if every in-band peer "
        "kept today’s sale. Instant BE / 20 / 30 use year-1 cost. "
        "40% and 60% were dropped — too rich versus the Instant shelf. "
        "Out-of-band peers are ignored.",
        s["body"],
    ))
    score = [[P(x, s["th"]) for x in [
        "Plan", "D", "Size", "BE", "Street (rk)",
        "@20% (rk)", "@30% (rk)", "In-band n", "In-band peers",
    ]]]
    vset = set()
    plan_ord = {"Instant": 0, "1-Step": 1, "2-Step Lite": 2, "2-Step Pro": 3}
    v = skus[skus.Firm == "Verodus"].copy()
    v["_po"] = v.Plan.map(plan_ord)
    v = v.sort_values(["_po", "Size"])
    for i, r in enumerate(v.itertuples(), start=1):
        raw_r, raw_n, r20, n20, r30, n30, peers, pr = vero_ranks(skus, r)
        names = ", ".join(f"{p.Firm} {p.Plan}" for p in peers.drop_duplicates("Product").itertuples())
        if len(names) > 90:
            names = names[:87] + "…"
        vset.add(i)
        score.append([
            P(str(r.Plan), s["tdl"]),
            P(f"{float(r.D):.1f}", s["td"]),
            P(usd(r.Size), s["td"]),
            P(usd(pr["be"]), s["td"]),
            P(priced(r.Sale, raw_r, raw_n), s["td"]),
            P(priced(pr["px_20"], r20, n20), s["td"]),
            P(priced(pr["px_30"], r30, n30), s["td"]),
            P(str(len(peers)), s["td"]),
            P(names or "—", s["tdl"]),
        ])
    story.append(grid(score, [
        24*mm, 14*mm, 16*mm, 16*mm, 28*mm, 28*mm, 28*mm, 18*mm, 78*mm,
    ], verodus_rows=vset))
    story.append(Spacer(1, 3*mm))

    # ----- 3–6 family SKU grids -----
    fams = [
        ("instant", "3. Instant SKUs — D and in-band vs Verodus Instant"),
        ("1-step", "4. One-step SKUs — D and in-band vs Verodus 1-Step"),
        ("2-step", "5. Two-step SKUs — D and in-band vs Lite / Pro"),
        ("3-step", "6. Three-step SKUs — no Verodus twin (shown for D only)"),
    ]
    vero_by_fam = {
        "instant": ["Instant"],
        "1-step": ["1-Step"],
        "2-step": ["2-Step Lite", "2-Step Pro"],
        "3-step": [],
    }
    for fam, title in fams:
        story.append(P(title, s["h1"]))
        sub = skus[skus.Family == fam].sort_values(["Size", "D", "Sale", "Firm"])
        heads = ["Firm", "Plan", "Size", "D", "ΔD", "In band", "BE", "Street",
                 "Vero @20% (rk) / peer 20%", "Vero @30% (rk) / peer 30%"]
        data = [[P(x, s["th"]) for x in heads]]
        vrows = set()
        anchors = {
            p: float(skus[(skus.Firm == "Verodus") & (skus.Plan == p)].D.iloc[0])
            for p in vero_by_fam[fam]
            if not skus[(skus.Firm == "Verodus") & (skus.Plan == p)].empty
        }
        for i, r in enumerate(sub.itertuples(), start=1):
            if anchors:
                gaps = {p: abs(float(r.D) - d) for p, d in anchors.items()}
                best = min(gaps, key=gaps.get)
                dlt = gaps[best]
                inb = "yes" if dlt <= DELTA else "no"
                dlt_s = f"{dlt:.1f} vs {best.replace('2-Step ', '')}"
            else:
                inb, dlt_s = "—", "—"
            pr = pricing_for(r)
            if r.Firm == "Verodus":
                raw_r, raw_n, r20, n20, r30, n30, _, _ = vero_ranks(skus, r)
                c20 = priced(pr["px_20"], r20, n20)
                c30 = priced(pr["px_30"], r30, n30)
                vrows.add(i)
                street = priced(r.Sale, raw_r, raw_n)
            else:
                c20, c30 = usd(pr["px_20"]), usd(pr["px_30"])
                street = usd(r.Sale)
            data.append([
                P(str(r.Firm), s["tdl"]),
                P(str(r.Plan), s["tdl"]),
                P(usd(r.Size), s["td"]),
                P(f"{float(r.D):.1f}", s["td"]),
                P(dlt_s, s["td"]),
                P(inb, s["td"]),
                P(usd(pr["be"]), s["td"]),
                P(street, s["td"]),
                P(c20, s["td"]),
                P(c30, s["td"]),
            ])
        story.append(grid(data, [
            30*mm, 32*mm, 16*mm, 14*mm, 28*mm, 16*mm, 16*mm, 28*mm, 40*mm, 40*mm,
        ], verodus_rows=vrows))
        story.append(Spacer(1, 2.5*mm))

    def _d(product):
        return float(scored.loc[scored.Product == product, "D"].iloc[0])

    bg_d, fn_i, fx_i = _d("BG Instant"), _d("FN Stellar Instant"), _d("FXIFY Instant")
    ftmo2, fn_lite = _d("FTMO 2-Step"), _d("FN Stellar Lite")
    story.append(P("7. What the band does", s["h1"]))
    story.append(P(
        f"FundedNext Instant (D {fn_i:.1f}) and FXIFY Standard (D {fx_i:.1f}) are 40+ "
        f"points below Verodus Instant (D {v_d['Instant']:.1f}) — no daily, P(pay) ~53%. "
        f"They never enter the Instant rank. "
        f"Blue Guardian Instant is D {bg_d:.1f} (SOD daily + trail lock), "
        f"ΔD {abs(bg_d - v_d['Instant']):.1f} vs us — inside the ±{DELTA:.0f} band, "
        f"the closest Instant twin. Instant Funding, Hola Direct, Goat, FP Zero, "
        f"FXIFY Lite and Alpha Instant are also in-band. "
        f"Lite (D {v_d['Lite']:.1f}) ranks against FN Lite (D {fn_lite:.1f}) / For Traders / Ment, "
        f"not against FTMO 2-Step (D {ftmo2:.1f}). "
        f"Pro (D {v_d['Pro']:.1f}) ranks against the FTMO-class 10%/5% set. "
        f"Same book: 7/22/26/28/17. Instant $200k removed.",
        s["body"],
    ))
    story.append(P(
        f"D formula: sim/difficulty.py · band ±{DELTA:.0f} · "
        "SKUs: results/industry_skus.csv · scores: results/difficulty_scores.csv.",
        s["tiny"],
    ))
    return story, skus, scored


def build():
    story, skus, scored = collect_story()
    scored.to_csv(RESULTS / "difficulty_scores.csv", index=False)
    rows = []
    for r in skus.sort_values(["Family", "Size", "D", "Sale"]).itertuples():
        pr = pricing_for(r)
        rec = {
            "Family": r.Family, "Firm": r.Firm, "Plan": r.Plan, "Product": r.Product,
            "Size": int(r.Size), "D": float(r.D), "BE": round(pr["be"], 2),
            "Street": float(r.Sale), "px_20": round(pr["px_20"], 2),
            "px_30": round(pr["px_30"], 2), "P_pay": float(r.P_pay),
        }
        if r.Firm == "Verodus":
            raw_r, raw_n, r20, n20, r30, n30, peers, _ = vero_ranks(skus, r)
            rec.update(
                street_rank=raw_r, street_n=raw_n,
                rank_at_20=r20, n_at_20=n20, rank_at_30=r30, n_at_30=n30,
                band_peers="; ".join(peers.Product.unique()),
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
        title="Verodus difficulty score and 20%/30% rank — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {RESULTS / 'difficulty_scores.csv'}")
    print(f"Wrote {RESULTS / 'verodus_be_ranks.csv'}")


if __name__ == "__main__":
    build()
