#!/usr/bin/env python3
"""Family street prices + customer-attractive Verodus sale card.

Pricing ignores difficulty. Rec is what a shopper finds cheap: at or under
the same-family median, and never above live if live is already cheaper.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from difficulty import scores_for_book

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

# Customer-attractive VERO35 sale. Instant cut to the family median
# (shop-round). Evals stay at live — already at or under the family low.
REC = {
    ("Instant", 5000): 63,
    ("Instant", 10000): 99,
    ("Instant", 25000): 175,
    ("Instant", 50000): 279,
    ("Instant", 100000): 499,
    ("1-Step", 5000): 36,
    ("1-Step", 10000): 60,
    ("1-Step", 25000): 120,
    ("1-Step", 50000): 193,
    ("1-Step", 100000): 335,
    ("1-Step", 200000): 654,
    ("2-Step Lite", 5000): 18,
    ("2-Step Lite", 10000): 33,
    ("2-Step Lite", 25000): 66,
    ("2-Step Lite", 50000): 133,
    ("2-Step Lite", 100000): 241,
    ("2-Step Lite", 200000): 477,
    ("2-Step Pro", 5000): 20,
    ("2-Step Pro", 10000): 36,
    ("2-Step Pro", 25000): 85,
    ("2-Step Pro", 50000): 163,
    ("2-Step Pro", 100000): 296,
    ("2-Step Pro", 200000): 577,
}

ANCHORS = (
    ("Instant", "instant"),
    ("1-Step", "1-step"),
    ("2-Step Lite", "2-step"),
    ("2-Step Pro", "2-step"),
)

WHY = {
    "Instant": (
        "Shoppers compare every Instant on the page — Alpha $40, BG $54, Goat $63, "
        "Hola $79 at $5k; Alpha $274, BG $467, Goat $559, Instant Funding $639, "
        "Hola $839 at $100k. Live VERO35 sits above the family median at every size. "
        "Rec cuts to that median (Goat-class, shop-round): $63 / $99 / $175 / $279 / $499. "
        "Under Goat and Instant Funding; above only the loss-leader Alpha / FXIFY Lite holes. "
        "$5k / $10k still print. $25k+ does not — that is the cost of being cheap enough "
        "to click. No $200k Instant."
    ),
    "1-Step": (
        "Live is already the cheapest 1-step on the shelf at every size except $5k "
        "(Fintokei $35). $335 vs FTMO $579 / FN $570 / Hola $463 at $100k. Keep live. "
        "Raising toward Hola would make the card less attractive, not more."
    ),
    "2-Step Lite": (
        "Live is the cheapest 2-step on the shelf (tied with Maven at $5k, under Maven "
        "from $10k). $241 vs Maven $279 / Ment $343 / FN Lite $449 at $100k. Keep live."
    ),
    "2-Step Pro": (
        "Live is #2 cheapest 2-step after Maven. $296 vs Maven $279 / Goat $399 / "
        "FTMO $626 at $100k. Keep live — already cheaper than almost every name a "
        "shopper knows."
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
        "VERODUS  ·  Attractive sale card vs family street  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Rec ≤ family median. BE / 20% / 40% / 60% = F_m = BE/(1−m). VERO35 list = sale ÷ 0.65.",
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


def family_peers(skus, family):
    return skus[(skus.Family == family) & (skus.Firm != "Verodus")]


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


def vs_pct(rec, x):
    if x is None or x <= 0:
        return None
    return 100.0 * (rec / x - 1.0)


def vs_s(rec, x):
    p = vs_pct(rec, x)
    if p is None:
        return "—"
    return f"{p:+.0f}%"


def family_stats(skus):
    rows = []
    for plan, family in ANCHORS:
        peers = family_peers(skus, family)
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            rec = REC[(plan, sz)]
            vals = [float(x) for x in peers.loc[peers.Size == sz, "Sale"].tolist()]
            if not vals:
                continue
            ser = pd.Series(vals)
            lo, med, avg, hi = float(ser.min()), float(ser.median()), float(ser.mean()), float(ser.max())
            field = vals + [rec]
            rank = sum(1 for v in field if v < rec - 1e-9) + 1
            if rec <= lo * 1.02:
                sell = "yes — cheapest / tied low"
            elif rec <= med:
                sell = "yes — at/under median"
            elif rec <= avg:
                sell = "mid — under average"
            elif rec <= hi:
                sell = "premium — under the high"
            else:
                sell = "above every peer"
            rows.append({
                "Plan": plan, "Size": sz, "n": len(vals), "Rec": rec,
                "Live": float(live.Sale.iloc[0]),
                "Low": lo, "Median": med, "Average": avg, "High": hi,
                "vs_low": vs_pct(rec, lo), "vs_med": vs_pct(rec, med),
                "vs_avg": vs_pct(rec, avg), "vs_high": vs_pct(rec, hi),
                "rank": rank, "n_field": len(field), "Sell": sell,
            })
    return rows


def build():
    skus, scored = load()
    s = styles()
    story = []

    story.append(P("Attractive Verodus sale card vs competitor street", s["cover"]))
    story.append(P(
        "Priced for the shopper, not for difficulty. Rec is at or under the same-family "
        "median (what customers see on Instant / 1-step / 2-step pages). "
        "16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "Rule: never recommend a fee above the family median, and never raise a live "
        "fee that is already under that median. 1-Step / Lite / Pro stay at today’s "
        "VERO35 — they are already the cheap names on those shelves. Instant is cut "
        "to the Instant median so we sit with Goat, not above Instant Funding / Hola. "
        "List = sale ÷ 0.65. Instant $200k pulled.",
        s["body"],
    ))

    story.append(P("1. Recommended Verodus sale (VERO35)", s["h1"]))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k",
             "Live $100k", "Rec m $100k", "Why this number"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    why_short = {
        "Instant": "Family median (Goat-class). Under IF / Hola.",
        "1-Step": "Keep live — cheapest 1-step on the shelf.",
        "2-Step Lite": "Keep live — cheapest 2-step on the shelf.",
        "2-Step Pro": "Keep live — #2 after Maven, under Goat / FTMO.",
    }
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        live100 = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == 100000)]
        live_s = float(live100.Sale.iloc[0]) if not live100.empty else None
        rec100 = REC.get((plan, 100000))
        cost100 = e_cost(skus, plan, 100000)
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            cells.append(P(usd(REC.get((plan, sz))), s["td"]))
        cells.append(P(usd(live_s), s["td"]))
        cells.append(P(margin(rec100, cost100), s["td"]))
        cells.append(P(why_short[plan], s["tdl"]))
        data.append(cells)
        special[i] = "rec"
    story.append(grid(data, [
        26*mm, 20*mm, 20*mm, 20*mm, 20*mm, 22*mm, 22*mm, 24*mm, 24*mm, 52*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = recommended sale. Instant is a cut vs live. Evals are unchanged. "
        "Instant $100k rec $499 is −26% vs live $676 and −6% vs Instant Funding $639. "
        "Margin at that size is negative — attractive Instant $25k+ does not print.",
        s["body"],
    ))

    story.append(P("2. Rec vs BE / 20% / 40% / 60%", s["h1"]))
    story.append(P(
        "Same book as the industry report. Instant has no refund ⇒ <b>BE = E[X]</b>. "
        "Evals refund on first payout ⇒ <b>BE = E[X] / (1 − P(pay))</b>. "
        "Fee at margin m: <b>F<sub>m</sub> = BE / (1 − m)</b>. "
        "20% / 40% / 60% are the print / target / fat fees. Rec is the shopper price; "
        "it is not forced up to those columns.",
        s["body"],
    ))
    heads = ["Plan", "Size", "Rec", "Rec m", "E[X]", "BE", "20%", "40%", "60%",
             "Live", "Median"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    stats = family_stats(skus)
    med_map = {(r["Plan"], r["Size"]): r["Median"] for r in stats}
    rows_out = []
    i = 0
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            r = live.iloc[0]
            rec = REC[(plan, sz)]
            cost = float(r.E_cost)
            rec_m = (rec - cost) / rec if rec else None
            med = med_map.get((plan, sz))
            i += 1
            if rec < float(r.BE) - 0.5:
                special[i] = "rec"
            elif abs(rec - float(r.Sale)) < 0.5:
                special[i] = "live"
            data.append([
                P(plan, s["tdl"]),
                P(usd(sz), s["td"]),
                P(usd(rec), s["td"]),
                P(margin(rec, cost), s["td"]),
                P(usd(r.E_payout), s["td"]),
                P(usd(r.BE), s["td"]),
                P(usd(r.px_20), s["td"]),
                P(usd(r.px_40), s["td"]),
                P(usd(r.px_60), s["td"]),
                P(usd(r.Sale), s["td"]),
                P(usd(med), s["td"]),
            ])
            rows_out.append({
                "Plan": plan, "Size": sz,
                "Rec_sale": rec, "Rec_list": round(rec / 0.65),
                "Rec_m": rec_m, "E_payout": float(r.E_payout),
                "E_cost": cost, "P_pay": float(r.P_pay),
                "BE": float(r.BE), "px_20": float(r.px_20),
                "px_40": float(r.px_40), "px_60": float(r.px_60),
                "Live_sale": float(r.Sale), "Live_m": float(r.sale_m),
                "Family_median": med,
                "vs_median": vs_pct(rec, med) if med else None,
                "vs_BE": vs_pct(rec, float(r.BE)),
                "vs_20": vs_pct(rec, float(r.px_20)),
                "vs_40": vs_pct(rec, float(r.px_40)),
                "vs_60": vs_pct(rec, float(r.px_60)),
            })
    story.append(grid(data, [
        26*mm, 18*mm, 18*mm, 16*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = rec is below BE (a hole). Blue = rec equals live and is above BE. "
        "1-Step / Lite / Pro rec sits between the 40% and 60% columns — attractive and "
        "still fat. Instant $5k / $10k sit near 20–40%. Instant $25k+ is under BE.",
        s["body"],
    ))

    for n, (plan, family) in enumerate(ANCHORS, start=3):
        peers = family_peers(skus, family)
        products = peers.drop_duplicates("Product").copy()
        # Sort by $100k street (what a shopper sorts by); missing $100k last.
        px = peers[peers.Size == 100000][["Product", "Sale"]].rename(columns={"Sale": "s100"})
        products = products.merge(px, on="Product", how="left").sort_values(
            ["s100", "Firm"], na_position="last"
        )
        live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan)]
        story.append(P(f"{n}. {plan} — every {family} street fee", s["h1"]))
        story.append(P(WHY[plan], s["body"]))

        heads = ["Firm", "Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
        data = [[P(h, s["th"]) for h in heads]]
        special = {}
        sales = sale_map(peers)
        live_sales = sale_map(live)

        def row_cells(firm, plan_name, sales_lookup):
            cells = [P(firm, s["tdl"]), P(plan_name, s["tdl"])]
            for sz in SIZES:
                cells.append(P(usd(sales_lookup.get((firm, plan_name, sz))), s["td"]))
            return cells

        for r in products.itertuples():
            data.append(row_cells(r.Firm, r.Plan, sales))

        data.append(row_cells("Verodus", plan, live_sales))
        special[len(data) - 1] = "live"
        rec_lookup = {("Verodus rec", plan, sz): REC.get((plan, sz)) for sz in SIZES}
        data.append(row_cells("Verodus rec", plan, rec_lookup))
        special[len(data) - 1] = "rec"

        story.append(grid(data, [
            36*mm, 40*mm, 24*mm, 24*mm, 24*mm, 24*mm, 26*mm, 26*mm,
        ], special))
        story.append(Spacer(1, 2*mm))

    story.append(P("7. Rec vs BE / 20 / 40 / 60 (±%) and list", s["h1"]))
    story.append(P(
        "±% is (rec − column) / column. Negative = rec is cheaper than that fee. "
        "List = rec ÷ 0.65 so VERO35 still lands on the card.",
        s["body"],
    ))
    heads = ["Plan", "Size", "Rec", "List", "vs BE", "vs 20%", "vs 40%", "vs 60%",
             "vs live", "vs median"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    for i, rec_row in enumerate(rows_out, start=1):
        if rec_row["Rec_sale"] < rec_row["BE"] - 0.5:
            special[i] = "rec"
        elif abs(rec_row["Rec_sale"] - rec_row["Live_sale"]) < 0.5:
            special[i] = "live"
        data.append([
            P(rec_row["Plan"], s["tdl"]),
            P(usd(rec_row["Size"]), s["td"]),
            P(usd(rec_row["Rec_sale"]), s["td"]),
            P(usd(rec_row["Rec_list"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["BE"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_20"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_40"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_60"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["Live_sale"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["Family_median"]), s["td"]),
        ])
    story.append(grid(data, [
        26*mm, 18*mm, 18*mm, 18*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 22*mm,
    ], special))
    story.append(Spacer(1, 2.5*mm))

    story.append(P("8. Rec vs family low / median / average / high", s["h1"]))
    story.append(P(
        "% is (rec − stat) / stat. Negative = cheaper than that mark. "
        "Family = every Instant, every 1-step, or every 2-step — the page a customer opens. "
        "5ers Hyper Growth ($260 / $450) pulls 1-step $5k / $10k average up; ignore it.",
        s["body"],
    ))
    heads = ["Plan", "Size", "n", "Rec", "Low", "±%", "Median", "±%",
             "Average", "±%", "High", "±%", "Attractive?"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    for i, r in enumerate(stats, start=1):
        if r["Sell"].startswith("yes"):
            special[i] = "live"
        elif r["Sell"].startswith("above"):
            special[i] = "rec"
        data.append([
            P(r["Plan"], s["tdl"]),
            P(usd(r["Size"]), s["td"]),
            P(str(r["n"]), s["td"]),
            P(usd(r["Rec"]), s["td"]),
            P(usd(r["Low"]), s["td"]),
            P(vs_s(r["Rec"], r["Low"]), s["td"]),
            P(usd(r["Median"]), s["td"]),
            P(vs_s(r["Rec"], r["Median"]), s["td"]),
            P(usd(r["Average"]), s["td"]),
            P(vs_s(r["Rec"], r["Average"]), s["td"]),
            P(usd(r["High"]), s["td"]),
            P(vs_s(r["Rec"], r["High"]), s["td"]),
            P(r["Sell"], s["tdl"]),
        ])
    story.append(grid(data, [
        24*mm, 18*mm, 10*mm, 16*mm, 16*mm, 14*mm, 18*mm, 14*mm,
        18*mm, 14*mm, 16*mm, 14*mm, 48*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Blue = at or under the family median (attractive). Instant rec is at the median, "
        "not above it. Evals are at the low. Same book 7/22/26/28/17.",
        s["tiny"],
    ))

    pd.DataFrame(rows_out).to_csv(RESULTS / "verodus_recommended_prices.csv", index=False)
    pd.DataFrame(stats).to_csv(RESULTS / "verodus_rec_vs_band.csv", index=False)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus attractive sale card — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Wrote {RESULTS / 'verodus_recommended_prices.csv'}")
    print(f"Wrote {RESULTS / 'verodus_rec_vs_band.csv'}")


if __name__ == "__main__":
    build()
