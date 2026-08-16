#!/usr/bin/env python3
"""Verodus BE by account + multi-factor recommended sale card.

Instant BE = year-1 E[X] (first × P_yr1/P_pay). Eval BE = first-payout
E[X] / (1 − P(pay)). Instant rec is the year-1 30% print, then checked
against an opex stack: 10% assumption-error on BE, $1/account, 20%
marketing, CAD 10,000/month wages. Competitor lows are used only if
they still cover that stack.
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
from industry_book import break_even_fee, expected_refund_frac, margin_price

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

# Opex stack (after payout BE). Error first, then cash costs, then marketing.
ASSUMPTION_ERR = 0.10          # 10% of BE — model / year-1 miss
ACCOUNT_COST = 1.0             # $1 per account
MARKETING = 0.20               # 20% of sale
WAGES_CAD = 10000.0            # monthly
CADUSD = 0.72                  # 16 Aug 2026
WAGES_USD = WAGES_CAD * CADUSD  # $7,200 / month

# Expected monthly units (310). Instant-heavy, mid-size modal, few $200k.
# Used only to spread CAD 10k wages — not a sales forecast.
UNITS = {
    ("Instant", 5000): 15,
    ("Instant", 10000): 25,
    ("Instant", 25000): 28,
    ("Instant", 50000): 18,
    ("Instant", 100000): 12,
    ("1-Step", 5000): 8,
    ("1-Step", 10000): 14,
    ("1-Step", 25000): 18,
    ("1-Step", 50000): 14,
    ("1-Step", 100000): 10,
    ("1-Step", 200000): 3,
    ("2-Step Lite", 5000): 10,
    ("2-Step Lite", 10000): 18,
    ("2-Step Lite", 25000): 22,
    ("2-Step Lite", 50000): 16,
    ("2-Step Lite", 100000): 12,
    ("2-Step Lite", 200000): 4,
    ("2-Step Pro", 5000): 6,
    ("2-Step Pro", 10000): 12,
    ("2-Step Pro", 25000): 16,
    ("2-Step Pro", 50000): 14,
    ("2-Step Pro", 100000): 10,
    ("2-Step Pro", 200000): 5,
}

# Support load: Instant lighter (no phases); 2-step heavier; larger size more tickets.
PLAN_WAGE_W = {
    "Instant": 0.85,
    "1-Step": 1.00,
    "2-Step Lite": 1.15,
    "2-Step Pro": 1.10,
}

# Rec = max(prior card, shop-round of fully loaded opex floor).
# Do not match a peer low that fails the stack. Evals stay under Maven
# wherever Maven itself covers. Instant stays under BG.
REC = {
    ("Instant", 5000): 59,
    ("Instant", 10000): 79,
    ("Instant", 25000): 139,
    ("Instant", 50000): 239,
    ("Instant", 100000): 449,
    ("1-Step", 5000): 36,
    ("1-Step", 10000): 60,
    ("1-Step", 25000): 120,
    ("1-Step", 50000): 193,
    ("1-Step", 100000): 335,
    ("1-Step", 200000): 654,
    ("2-Step Lite", 5000): 45,
    ("2-Step Lite", 10000): 59,
    ("2-Step Lite", 25000): 99,
    ("2-Step Lite", 50000): 151,
    ("2-Step Lite", 100000): 269,
    ("2-Step Lite", 200000): 499,
    ("2-Step Pro", 5000): 45,
    ("2-Step Pro", 10000): 59,
    ("2-Step Pro", 25000): 95,
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
        "Stack: year-1 BE, +10% error, +$1, +wage share, then ÷ 0.80 for marketing. "
        "Instant $100k opex floor is $422; Alpha $274 fails it. FXIFY Lite $399 is "
        "close but short. Rec $449 covers with a ~$21 stub and is 0.96× BG $467. "
        "$10k–$50k $79 / $139 / $239 stay under BG $156 / $243. "
        "$5k stays the shop floor. No $200k Instant."
    ),
    "1-Step": (
        "Live already covers the full stack at every size. $335 vs opex floor $200 "
        "at $100k. Fintokei / Alpha / Hola lows all cover. Keep live — leftover "
        "pays most of the wage bill."
    ),
    "2-Step Lite": (
        "Live $18–$241 does not cover wages + 20% marketing on $5k–$100k. "
        "Maven $18 / $35 / $79 also fail. Rec $45 / $59 / $99 / $151 / $269 — "
        "solvent 2-step with a small stub. Maven $151 / $279 cover from $50k."
    ),
    "2-Step Pro": (
        "Live $20 / $36 miss the $5k / $10k floor. Lift those to $45 / $59. "
        "$25k+ live already covers. $296 at $100k is above the $248 floor and "
        "under Goat $399. Maven $18 / $35 / $79 are not usable lows."
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
    skus = skus.merge(blend[["Product", "P_yr1"]], on="Product", how="left")
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
        "td2": ParagraphStyle(
            "td2", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.6, leading=8.4, alignment=TA_CENTER,
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
        "BE + 10% error + $1 + wage share, then ÷ 0.80 marketing. Instant = year-1. Evals = first-payout + refund.",
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
        ("TOPPADDING", (0, 0), (-1, -1), 2.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
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


def plan_be(skus, plan, size):
    row = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == size)]
    if row.empty:
        return None
    return pricing_for(row.iloc[0])["be"]


def rec_be_cell(rec, be, style):
    if rec is None:
        return P("—", style)
    if be is None:
        return P(usd(rec), style)
    return P(
        f"<b>{usd(rec)}</b><br/><font size='6' color='#475569'>BE {usd(be)}</font>",
        style,
    )


def classic_rows(skus):
    """Plan Size List Sale E[X] P(pay) BE 20% 40% 60% Sale m — rec as Sale."""
    out = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            r = live.iloc[0]
            pr = pricing_for(r)
            sale = REC[(plan, sz)]
            cost = pr["e_used"] if plan == "Instant" else (
                pr["e_first"] + float(r.P_pay) * sale
            )
            sm = (sale - cost) / sale if sale else None
            out.append({
                "Plan": plan, "Size": sz, "Basis": pr["basis"],
                "List": round(sale / 0.65), "Sale": sale,
                "E_X": pr["e_used"], "P_pay": pr["p_pay"],
                "P_yr1": pr["p_yr1"], "BE": pr["be"],
                "px_20": pr["px_20"], "px_40": pr["px_40"],
                "px_60": pr["px_60"], "Sale_m": sm, "Cost": cost,
            })
    return out


def classic_table(skus, s):
    """Industry-format grid: Plan Size List Sale E[X] P(pay) BE 20% 40% 60% Sale m."""
    heads = ["Plan", "Size", "List", "Sale", "E[X]", "P(pay)",
             "BE", "20%", "40%", "60%", "Sale m"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    rows = classic_rows(skus)
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(usd(r["Sale"]), s["td"]),
            P(usd(r["E_X"]), s["td"]),
            P(f"{100 * r['P_pay']:.1f}%", s["td"]),
            P(usd(r["BE"]), s["td"]),
            P(usd(r["px_20"]), s["td"]),
            P(usd(r["px_40"]), s["td"]),
            P(usd(r["px_60"]), s["td"]),
            P(margin(r["Sale"], r["Cost"]), s["td"]),
        ])
    return grid(data, [
        26*mm, 18*mm, 16*mm, 16*mm, 18*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm,
    ], spec), rows


def y1_payout(e_first, p_pay, p_yr1):
    """Scale first-payout E[X] down to the year-1 paid share."""
    if p_pay is None or p_pay <= 0 or pd.isna(p_yr1):
        return float(e_first)
    return float(e_first) * float(p_yr1) / float(p_pay)


def pricing_for(r):
    """BE and 10/20/30/40/60 prints. Display columns are 20/40/60."""
    e_first = float(r.E_payout)
    p_pay = float(r.P_pay)
    p_yr1 = float(r.P_yr1) if pd.notna(getattr(r, "P_yr1", None)) else p_pay
    if r.Family == "instant":
        e = y1_payout(e_first, p_pay, p_yr1)
        k = expected_refund_frac(str(r.Refund), p_yr1)
        be = break_even_fee(e, k)
        basis = "year-1"
    else:
        e = e_first
        be = float(r.BE)
        basis = "first"
    return {
        "e_first": e_first,
        "e_used": e,
        "be": be,
        "px_10": margin_price(be, 0.10),
        "px_20": margin_price(be, 0.20),
        "px_30": margin_price(be, 0.30),
        "px_40": margin_price(be, 0.40),
        "px_60": margin_price(be, 0.60),
        "basis": basis,
        "p_pay": p_pay,
        "p_yr1": p_yr1,
    }


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


def size_wage_w(size):
    return 0.65 + 0.35 * (float(size) / 100000.0)


def wage_weight(plan, size):
    return PLAN_WAGE_W[plan] * size_wage_w(size)


def wage_denom():
    return sum(n * wage_weight(plan, sz) for (plan, sz), n in UNITS.items())


def wage_for(plan, size):
    """USD wage allocated to one account of this SKU."""
    return WAGES_USD * wage_weight(plan, size) / wage_denom()


def monthly_units(plan, size):
    return UNITS.get((plan, size), 0)


def opex_stack(be, plan, size):
    """BE → +10% error → +$1 → +wage share → marketing 20% floor."""
    err = float(be) * ASSUMPTION_ERR
    wage = wage_for(plan, size)
    loaded = float(be) + err + ACCOUNT_COST + wage
    return {
        "error": err,
        "account": ACCOUNT_COST,
        "wage": wage,
        "loaded": loaded,
        "s_opex": loaded / (1.0 - MARKETING),
    }


def leftover_after_opex(sale, loaded):
    if sale is None:
        return None
    return float(sale) * (1.0 - MARKETING) - loaded


def n_for_wages(leftover):
    if leftover is None or leftover <= 0.5:
        return None
    return WAGES_USD / leftover


def peer_band(skus, family, size):
    peers = family_peers(skus, family)
    peers = peers[peers.Size == size]
    if peers.empty:
        return None
    ordered = peers.sort_values("Sale")
    lo = ordered.iloc[0]
    return {
        "low_firm": str(lo.Firm),
        "low_plan": str(lo.Plan),
        "low": float(lo.Sale),
        "rows": ordered,
    }


def first_sufficient(band, s_opex):
    if band is None:
        return None
    for r in band["rows"].itertuples():
        if float(r.Sale) + 3 >= s_opex:
            return {"firm": str(r.Firm), "plan": str(r.Plan), "sale": float(r.Sale)}
    return None


def opex_rows(skus):
    """Unit stack + competitor-low test for every rec SKU."""
    out = []
    for plan, fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            r = live.iloc[0]
            pr = pricing_for(r)
            be = pr["be"]
            st = opex_stack(be, plan, sz)
            sale = REC[(plan, sz)]
            band = peer_band(skus, fam, sz)
            ok = first_sufficient(band, st["s_opex"])
            low = band["low"] if band else None
            low_left = leftover_after_opex(low, st["loaded"]) if low is not None else None
            rec_left = leftover_after_opex(sale, st["loaded"])
            n = monthly_units(plan, sz)
            out.append({
                "Plan": plan, "Size": sz, "N": n,
                "BE": be, "Error": st["error"],
                "Wage": st["wage"], "Loaded": st["loaded"],
                "S_opex": st["s_opex"], "Rec": sale,
                "List": round(sale / 0.65),
                "Low": low,
                "Low_name": f"{band['low_firm']}" if band else None,
                "Low_ok": bool(low is not None and low + 3 >= st["s_opex"]),
                "First_ok": ok["sale"] if ok else None,
                "First_ok_name": f"{ok['firm']}" if ok else None,
                "Low_left": low_left,
                "Rec_left": rec_left,
                "Book_pnl": (rec_left or 0.0) * n,
                "Mkt": sale * MARKETING,
            })
    return out


def opex_table(skus, s):
    heads = ["Plan", "Size", "Wage", "BE", "+10%", "$1+w", "Opex $",
             "Peer low", "Low OK?", "First OK $", "Rec", "After"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    rows = opex_rows(skus)
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        low_s = "—" if r["Low"] is None else f"{usd(r['Low'])} {r['Low_name']}"
        ok_s = "yes" if r["Low_ok"] else "NO — hole"
        first_s = "—" if r["First_ok"] is None else f"{usd(r['First_ok'])} {r['First_ok_name']}"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["Wage"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["Error"]), s["td"]),
            P(usd(r["Loaded"]), s["td"]), P(usd(r["S_opex"]), s["td"]),
            P(low_s, s["td"]), P(ok_s, s["td"]), P(first_s, s["td"]),
            P(usd(r["Rec"]), s["td"]),
            P(usd(r["Rec_left"]), s["td"]),
        ])
    return grid(data, [
        24*mm, 16*mm, 14*mm, 16*mm, 14*mm, 16*mm, 16*mm,
        32*mm, 18*mm, 32*mm, 16*mm, 16*mm,
    ], spec), rows


def mix_table(skus, s):
    heads = ["Plan", "Size", "N / mo", "Weight", "Wage $", "Share of wages"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    denom = wage_denom()
    total_n = sum(UNITS.values())
    i = 0
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in UNITS:
                continue
            i += 1
            n = UNITS[(plan, sz)]
            wgt = wage_weight(plan, sz)
            wage = wage_for(plan, sz)
            share = n * wage / WAGES_USD
            spec[i] = "rec" if plan == "Instant" else "live"
            data.append([
                P(plan, s["tdl"]), P(usd(sz), s["td"]),
                P(str(n), s["td"]), P(f"{wgt:.2f}", s["td"]),
                P(usd(wage), s["td"]), P(f"{100 * share:.1f}%", s["td"]),
            ])
    data.append([
        P("Book", s["tdl"]), P("—", s["td"]),
        P(str(total_n), s["td"]), P("1.00 avg", s["td"]),
        P(usd(WAGES_USD / total_n), s["td"]), P("100%", s["td"]),
    ])
    return grid(data, [
        32*mm, 22*mm, 22*mm, 22*mm, 22*mm, 28*mm,
    ], spec)


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


def collect_story():
    skus, scored = load()
    s = styles()
    story = []

    story.append(P("Break-even by account and recommended sale", s["cover"]))
    story.append(P(
        "Every Verodus size has a stated BE. Instant uses year-1 cost. "
        "1-Step / Lite / Pro use first-payout + fee refund. "
        "Recommended sale is multi-factor — not the family median. 16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "<b>Instant BE</b> = E[X]<sub>first</sub> × (P<sub>yr1</sub> / P<sub>pay</sub>) "
        "= $875.25 × (7.161% / 22.07%) = <b>$284 at $100k</b>, then × size/100k. "
        "No refund. <b>Eval BE</b> = E[X] / (1 − P(pay)): 1-Step $108.10 / 0.91192 = "
        "<b>$119</b>; Lite $136.01 / 0.89384 = <b>$152</b>; Pro $132.54 / 0.88002 = "
        "<b>$151</b> at $100k, then × size/100k. F<sub>m</sub> = BE / (1 − m). "
        "List = sale ÷ 0.65. Instant $200k pulled.",
        s["body"],
    ))
    story.append(P(
        "<b>Rec factors:</b> (1) payout BE, then <b>10% assumption error</b>, then "
        "<b>$1 + wage share</b>, then <b>÷ 0.80</b> for 20% marketing; (2) Instant "
        "stays under BG / Goat; (3) do not match a peer low that fails that floor "
        "(Alpha Instant, Maven $5k–$25k, BrightFunded $200k); (4) 1-Step live already "
        "covers — keep it; (5) Lite / small Pro lift to the floor so they are the "
        "cheapest <i>solvent</i> 2-step, not the cheapest hole. "
        "Instant $100k $449 is 0.96× BG $467 (opex floor $422, leftover ~$21).",
        s["body"],
    ))

    story.append(P("1. Recommended Verodus sale (VERO35)", s["h1"]))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k",
             "BE $100k", "Live $100k", "Rec m"]
    data = [[P(h, s["th"]) for h in heads]]
    special = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        live100 = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == 100000)]
        live_s = float(live100.Sale.iloc[0]) if not live100.empty else None
        rec100 = REC.get((plan, 100000))
        be100 = plan_be(skus, plan, 100000)
        live100_r = live100.iloc[0] if not live100.empty else None
        if live100_r is not None and plan == "Instant":
            cost100 = pricing_for(live100_r)["e_used"]
        else:
            cost100 = e_cost(skus, plan, 100000)
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            cells.append(rec_be_cell(REC.get((plan, sz)), plan_be(skus, plan, sz), s["td2"]))
        cells.append(P(usd(be100), s["td"]))
        cells.append(P(usd(live_s), s["td"]))
        cells.append(P(margin(rec100, cost100), s["td"]))
        data.append(cells)
        special[i] = "rec"
    story.append(grid(data, [
        28*mm, 24*mm, 24*mm, 24*mm, 24*mm, 26*mm, 26*mm, 24*mm, 24*mm, 20*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = recommended sale. Each size shows <b>rec $</b> and <b>BE $</b>. "
        "Instant $59 / $79 / $139 / $239 / $449. "
        "Lite $45 / $59 / $99 / $151 / $269 / $499 (small stub; on/under Maven from $50k). "
        "1-Step stays live. Pro $5k–$25k $45 / $59 / $95; $50k+ live.",
        s["body"],
    ))

    story.append(P("1b. Break-even fee ($)", s["h1"]))
    story.append(P(
        "Same sizes as the rec card. Instant = year-1, no refund. "
        "Evals = first-payout + fee refund.",
        s["body"],
    ))
    be_heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k", "Basis"]
    be_card = [[P(h, s["th"]) for h in be_heads]]
    be_spec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            if (plan, sz) not in REC:
                cells.append(P("—", s["td"]))
            else:
                cells.append(P(usd(plan_be(skus, plan, sz)), s["td"]))
        cells.append(P("year-1" if plan == "Instant" else "first + refund", s["td"]))
        be_card.append(cells)
        be_spec[i] = "rec" if plan == "Instant" else "live"
    story.append(grid(be_card, [
        28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 30*mm, 30*mm, 32*mm,
    ], be_spec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $100k BE is <b>$284</b>. 1-Step $119 · Lite $152 · Pro $151. "
        "Then × size/100k.",
        s["tiny"],
    ))

    story.append(P("1c. Plan / Size / List / Sale / E[X] / P(pay) / BE / 20% / 40% / 60% / Sale m", s["h1"]))
    story.append(P(
        "<b>Use 20 / 40 / 60 as the reference columns</b> — that is the industry layout. "
        "Instant <b>target is 30%</b> (greater margin that still sells). "
        "40% Instant $100k is $473 (Blue Guardian $467). "
        "60% is $710 (above Goat $559 / Instant Funding $639). Do not aim Instant at 40 or 60. "
        "Sale is the recommended VERO35 fee. List = sale ÷ 0.65. "
        "Instant E[X] and BE are year-1; P(pay) is first-payout eligibility (22.1%). "
        "Eval E[X] / P(pay) / BE are first-payout + refund. "
        "Sale m = (sale − E[cost]) / sale.",
        s["body"],
    ))
    ctab, _crows = classic_table(skus, s)
    story.append(ctab)
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = Instant (year-1). Blue = evals (first-payout). "
        "Sale is the opex-checked fee. Instant $25k/$50k sit on the fully loaded floor. "
        "Lite is no longer the industry low on $5k–$25k — those lows do not cover wages.",
        s["tiny"],
    ))

    story.append(P(
        "1d. Wage mix — CAD 10,000 / month across 310 accounts",
        s["h1"],
    ))
    story.append(P(
        "CAD 10,000 × 0.72 = <b>USD 7,200 / month</b>. Spread across a 310-account "
        "early book (Instant 98 · 1-Step 67 · Lite 82 · Pro 63). "
        "Weight = plan factor × (0.65 + 0.35 × size/100k). "
        "Instant 0.85 (no phases), 1-Step 1.00, Lite 1.15, Pro 1.10. "
        "Flat average is $23 / account; Instant $5k gets $16, Pro $200k gets $43. "
        "At 150 accounts/month the wage line roughly doubles; at 600 it halves.",
        s["body"],
    ))
    story.append(mix_table(skus, s))
    story.append(Spacer(1, 2*mm))

    story.append(P(
        "1e. Opex stack — error first, then $1 + wage, then marketing 20%",
        s["h1"],
    ))
    story.append(P(
        "Build the fee in order. <b>(1) Payout BE</b> (year-1 Instant; first-payout "
        "+ refund on evals). <b>(2) Assumption error = 10% of BE</b>, taken first. "
        "<b>(3) $1 per account + wage share</b>. "
        "<b>(4) Marketing 20% of sale</b> ⇒ "
        "S<sub>opex</sub> = (BE × 1.10 + $1 + wage) / 0.80. "
        "Peer low is the cheapest same-family street fee. "
        "<b>Low OK</b> means that low already covers S<sub>opex</sub>. "
        "If it does not, <b>First OK</b> is the cheapest peer that does. "
        "Do not match a low that fails the stack.",
        s["body"],
    ))
    otab, _orows = opex_table(skus, s)
    story.append(otab)
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $100k: S<sub>opex</sub> $422. Alpha $274 is a hole. FXIFY Lite $399 "
        "is still short. Rec $449 covers and stays under BG $467. "
        "Instant $25k/$50k Alpha $118 / $154 fail; rec $139 / $239 clear the floor "
        "and stay under BG $156 / $243. "
        "1-Step lows all cover — keep live. "
        "Lite live and Maven $5k–$25k fail; rec is the cheapest solvent 2-step. "
        "Maven $151 / $279 cover Lite $50k / $100k — rec $151 / $269. "
        "Book leftover after the stack at this mix is about +$7,300 / month.",
        s["tiny"],
    ))

    # ----- BE for every account -----
    story.append(P("2. Break-even for every Verodus account", s["h1"]))
    story.append(P(
        "This is the number the rest of the card is built on. Instant also shows "
        "first-payout E[X] so the old $875 / $1,094 path is visible and not used.",
        s["body"],
    ))
    bheads = ["Plan", "Size", "Basis", "E[X] used", "P(pay)", "Year-1",
              "BE $", "20%", "40%", "60%", "Live", "Rec"]
    bdata = [[P(h, s["th"]) for h in bheads]]
    bspec = {}
    bi = 0
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
            bi += 1
            if plan == "Instant":
                bspec[bi] = "rec"
            else:
                bspec[bi] = "live"
            bdata.append([
                P(plan, s["tdl"]),
                P(usd(sz), s["td"]),
                P(pr["basis"], s["td"]),
                P(usd(pr["e_used"]), s["td"]),
                P(f"{100 * pr['p_pay']:.1f}%", s["td"]),
                P(f"{100 * pr['p_yr1']:.1f}%", s["td"]),
                P(usd(pr["be"]), s["td"]),
                P(usd(pr["px_20"]), s["td"]),
                P(usd(pr["px_40"]), s["td"]),
                P(usd(pr["px_60"]), s["td"]),
                P(usd(r.Sale), s["td"]),
                P(usd(rec), s["td"]),
            ])
    story.append(grid(bdata, [
        26*mm, 18*mm, 16*mm, 20*mm, 16*mm, 16*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm,
    ], bspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = Instant (year-1 BE). Blue = evals (first-payout BE). "
        "1-Step $5k BE is $6; sale $36 is leftover live, not a 60% target. "
        "Instant $100k BE is $284, not $875. Columns are 20 / 40 / 60. Instant rec is the 30% print.",
        s["tiny"],
    ))

    story.append(P("3. Why Instant first-payout margins were wrong", s["h1"]))
    story.append(P(
        "Same-difficulty Instant (D 84–94): Blue Guardian, Instant Funding, Goat, Hola, "
        "FP Zero, FXIFY Lite, Alpha. They charge <b>$274–$839</b> at $100k. Our first-payout "
        "book put Verodus Instant E[X] at <b>$875</b> and the 20% fee at <b>$1,094</b> — "
        "above every peer — and painted those peers at −30% to −95%. "
        "A market that keeps selling Instant at Goat / BG / IF prices is not all insolvent. "
        "The industry report already said <b>year-1 (7.2% of buyers) prices Instant</b>, "
        "not first-payout eligibility (22%). First-payout 22% is “hit 5 valid days”; "
        "most of those accounts die in month 1 (PropScorer 41% of funded). "
        "Sustained Instant is 4–6% (Track360) — this book’s year-1 is 7.2%. "
        "<b>Instant E[cost] = E[X]<sub>first</sub> × (P<sub>yr1</sub> / P<sub>pay</sub>)</b>. "
        "Evals stay on first-payout + refund (those margins already matched the shelf).",
        s["body"],
    ))

    # Peer Instant $100k: first-payout m vs year-1 m
    inst = skus[(skus.Family == "instant") & (skus.Size == 100000)].copy()
    pheads = ["Firm", "Plan", "D", "Sale", "P(pay)", "Year-1",
              "E[X] first", "m first", "E[X] yr1", "m yr1"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    pspecial = {}
    inst = inst.sort_values("Sale")
    for i, r in enumerate(inst.itertuples(), start=1):
        pr = pricing_for(r)
        m_first = (float(r.Sale) - pr["e_first"]) / float(r.Sale) if r.Sale else None
        m_y1 = (float(r.Sale) - pr["e_used"]) / float(r.Sale) if r.Sale else None
        if r.Firm == "Verodus":
            pspecial[i] = "live"
        pdata.append([
            P(str(r.Firm), s["tdl"]),
            P(str(r.Plan), s["tdl"]),
            P(f"{float(r.D):.1f}", s["td"]),
            P(usd(r.Sale), s["td"]),
            P(f"{100 * float(r.P_pay):.1f}%", s["td"]),
            P(f"{100 * float(r.P_yr1):.1f}%", s["td"]),
            P(usd(pr["e_first"]), s["td"]),
            P(f"{100 * m_first:+.0f}%", s["td"]),
            P(usd(pr["e_used"]), s["td"]),
            P(f"{100 * m_y1:+.0f}%", s["td"]),
        ])
    # Verodus rec row
    vr = inst[inst.Firm == "Verodus"].iloc[0]
    pr = pricing_for(vr)
    rec = REC[("Instant", 100000)]
    m_y1 = (rec - pr["e_used"]) / rec
    m_first = (rec - pr["e_first"]) / rec
    pdata.append([
        P("Verodus rec", s["tdl"]),
        P("Instant", s["tdl"]),
        P(f"{float(vr.D):.1f}", s["td"]),
        P(usd(rec), s["td"]),
        P(f"{100 * float(vr.P_pay):.1f}%", s["td"]),
        P(f"{100 * float(vr.P_yr1):.1f}%", s["td"]),
        P(usd(pr["e_first"]), s["td"]),
        P(f"{100 * m_first:+.0f}%", s["td"]),
        P(usd(pr["e_used"]), s["td"]),
        P(f"{100 * m_y1:+.0f}%", s["td"]),
    ])
    pspecial[len(pdata) - 1] = "rec"
    story.append(grid(pdata, [
        32*mm, 28*mm, 14*mm, 18*mm, 16*mm, 16*mm, 22*mm, 18*mm, 20*mm, 16*mm,
    ], pspecial))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Blue = live Verodus. Green = rec. On year-1, BG $467 is +38%, Goat $559 is +55%, "
        "IF $639 is +57%, Hola $839 is +60%, rec $449 is +37%. First-payout column is the "
        "old (wrong) Instant basis. 40–60% year-1 takes are what Goat / IF / Hola already "
        "charge — too high for a new name.",
        s["body"],
    ))

    story.append(P("4. Rec vs BE / 20% / 40% / 60% (Instant = year-1)", s["h1"]))
    story.append(P(
        "Instant: <b>BE = E[X]<sub>first</sub> × (P<sub>yr1</sub> / P<sub>pay</sub>)</b>, no refund. "
        "Evals: first-payout E[X] and refund ⇒ <b>BE = E[X] / (1 − P(pay))</b>. "
        "F<sub>m</sub> = BE / (1 − m). Rec is the shopper price.",
        s["body"],
    ))
    heads = ["Plan", "Size", "Rec", "Rec m", "E[X]", "BE $", "20%", "40%", "60%",
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
            pr = pricing_for(r)
            cost = pr["e_used"] if plan == "Instant" else float(r.E_cost)
            rec_m = (rec - cost) / rec if rec else None
            med = med_map.get((plan, sz))
            i += 1
            if rec < pr["be"] - 0.5:
                special[i] = "rec"
            elif abs(rec - float(r.Sale)) < 0.5:
                special[i] = "live"
            data.append([
                P(plan, s["tdl"]),
                P(usd(sz), s["td"]),
                P(usd(rec), s["td"]),
                P(margin(rec, cost), s["td"]),
                P(usd(pr["e_used"]), s["td"]),
                P(usd(pr["be"]), s["td"]),
                P(usd(pr["px_20"]), s["td"]),
                P(usd(pr["px_40"]), s["td"]),
                P(usd(pr["px_60"]), s["td"]),
                P(usd(r.Sale), s["td"]),
                P(usd(med), s["td"]),
            ])
            rows_out.append({
                "Plan": plan, "Size": sz, "Basis": pr["basis"],
                "Rec_sale": rec, "Rec_list": round(rec / 0.65),
                "Rec_m": rec_m, "E_payout": pr["e_used"],
                "E_first": pr["e_first"], "E_cost": cost,
                "P_pay": pr["p_pay"], "P_yr1": pr["p_yr1"],
                "BE": pr["be"], "px_20": pr["px_20"],
                "px_40": pr["px_40"], "px_60": pr["px_60"],
                "Live_sale": float(r.Sale), "Live_m": (float(r.Sale) - cost) / float(r.Sale),
                "Family_median": med,
                "vs_median": vs_pct(rec, med) if med else None,
                "vs_BE": vs_pct(rec, pr["be"]),
                "vs_20": vs_pct(rec, pr["px_20"]),
                "vs_40": vs_pct(rec, pr["px_40"]),
                "vs_60": vs_pct(rec, pr["px_60"]),
            })
    story.append(grid(data, [
        26*mm, 18*mm, 18*mm, 16*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm,
    ], special))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Green = rec is below BE (a hole). Blue = rec equals live and is above BE. "
        "Instant rec sits above the opex floor at $10k+ ($5k is the shop floor). "
        "1-Step / Lite / Pro stay on live VERO35 — those Rec m figures are leftover "
        "pricing power, not a 40/60 target. Green would mean below BE.",
        s["body"],
    ))

    for n, (plan, family) in enumerate(ANCHORS, start=5):
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

    story.append(P("9. Rec vs BE / 20 / 40 / 60 (±%) and list", s["h1"]))
    story.append(P(
        "BE is the dollar fee, then (rec − BE) / BE. Other ±% columns are "
        "(rec − column) / column. Negative = rec is cheaper than that fee. "
        "List = rec ÷ 0.65 so VERO35 still lands on the card.",
        s["body"],
    ))
    heads = ["Plan", "Size", "Rec", "List", "BE $ (±%)", "vs 20%", "vs 40%", "vs 60%",
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
            P(f"{usd(rec_row['BE'])} ({vs_s(rec_row['Rec_sale'], rec_row['BE'])})", s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_20"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_40"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["px_60"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["Live_sale"]), s["td"]),
            P(vs_s(rec_row["Rec_sale"], rec_row["Family_median"]), s["td"]),
        ])
    story.append(grid(data, [
        24*mm, 16*mm, 16*mm, 16*mm, 28*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm,
    ], special))
    story.append(Spacer(1, 2.5*mm))

    story.append(P("10. Rec vs family low / median / average / high (context only)", s["h1"]))
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
        "Median is context only — rec is not set to it. Instant $25k+ sits on the "
        "year-1 30% print, under BG and Goat. Same book 7/22/26/28/17.",
        s["tiny"],
    ))
    return story, skus, rows_out, stats


def build():
    story, skus, rows_out, stats = collect_story()
    pd.DataFrame(classic_rows(skus)).to_csv(RESULTS / "verodus_classic_sku_table.csv", index=False)
    pd.DataFrame(opex_rows(skus)).to_csv(RESULTS / "verodus_opex_stack.csv", index=False)
    pd.DataFrame(rows_out).to_csv(RESULTS / "verodus_recommended_prices.csv", index=False)
    pd.DataFrame(stats).to_csv(RESULTS / "verodus_rec_vs_band.csv", index=False)
    pd.DataFrame([{
        "Plan": r["Plan"], "Size": r["Size"], "Basis": r["Basis"],
        "BE": round(r["BE"], 2), "E_used": round(r["E_payout"], 2),
        "E_first": round(r["E_first"], 2),
        "px_20": round(r["px_20"], 2), "px_40": round(r["px_40"], 2),
        "px_60": round(r["px_60"], 2),
        "Live": r["Live_sale"], "Rec": r["Rec_sale"],
        "Rec_m": round(r["Rec_m"], 4),
    } for r in rows_out]).to_csv(RESULTS / "verodus_be_by_account.csv", index=False)

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
    print(f"Wrote {RESULTS / 'verodus_classic_sku_table.csv'}")
    print(f"Wrote {RESULTS / 'verodus_opex_stack.csv'}")
    print(f"Wrote {RESULTS / 'verodus_recommended_prices.csv'}")
    print(f"Wrote {RESULTS / 'verodus_rec_vs_band.csv'}")
    print(f"Wrote {RESULTS / 'verodus_be_by_account.csv'}")


if __name__ == "__main__":
    build()
