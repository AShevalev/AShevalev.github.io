#!/usr/bin/env python3
"""BE, challenge leftover, and leftover for every legal add-on combination.

Prints? = leftover after 20% ads minus extra E[X] is at least -$1.
Challenge leftover is the opex-stack Rec_left. Addon leftover is
sticker × 0.52 − extra E[X]. Combined = challenge + addon.
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

from write_price_rec_pdf import (
    ANCHORS, MARKETING, REC, SIZES, load, leftover_after_opex, opex_rows, rec_list, usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Addon_BE_Margins_2026-08-17.pdf"

PAGE = landscape(A4)
W, H = PAGE
MARGIN = 10 * mm

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_REC = colors.HexColor("#dcfce7")
ROW_NO = colors.HexColor("#fee2e2")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")

# Extra E[X] vs default 80% biweekly, as a fraction of priced E[X] (BE).
# Instant = year-1; evals = first-payout. News is included in the challenge fee.
EXTRA_F = {
    "Instant": {
        "weekend": 0.08, "weekly": 0.08,
        "od80": 0.12, "split90": 0.125, "od90": 0.41,
    },
    "1-Step": {
        "weekend": 0.04, "weekly": 0.05,
        "od80": 0.05, "split90": 0.125, "od90": 0.125,
    },
}
EXTRA_F["2-Step Lite"] = dict(EXTRA_F["1-Step"])
EXTRA_F["2-Step Pro"] = dict(EXTRA_F["1-Step"])

PCT = {
    "weekend": (0.15, 0.15),
    "weekly": (0.10, 0.10),
    "od80": (0.15, 0.18),
    "split90": (0.15, 0.18),
    "od90": (0.25, 0.35),
}

# Legal shopper carts. Weekly XOR payout upgrades. News is included (no SKU).
COMBOS = [
    ("Challenge only", ()),
    ("Weekend", ("weekend",)),
    ("Weekly 80%", ("weekly",)),
    ("On-demand 80%", ("od80",)),
    ("90% split", ("split90",)),
    ("90% On Demand", ("od90",)),
    ("Weekend + weekly", ("weekend", "weekly")),
    ("Weekend + on-demand 80%", ("weekend", "od80")),
    ("Weekend + 90%", ("weekend", "split90")),
    ("Weekend + 90% On Demand", ("weekend", "od90")),
]


def js_round(x: float) -> int:
    return int(x + 0.5) if x >= 0 else int(x - 0.5)


def sticker(list_px: float, pct: float) -> int:
    return js_round(float(list_px) * float(pct))


def pct_for(plan: str, key: str) -> float:
    ev, inst = PCT[key]
    return inst if plan == "Instant" else ev


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Times-Bold",
            fontSize=16, leading=20, textColor=NAVY, alignment=TA_LEFT, spaceAfter=3,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Times-Italic",
            fontSize=9.5, leading=12, textColor=TEAL, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Times-Bold",
            fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=8.2, leading=10.6, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=6.4, leading=8, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.4, leading=8, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.4, leading=8, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7, leading=9, textColor=colors.HexColor("#334155"),
        ),
    }


def P(text, style):
    return Paragraph(text, style)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        MARGIN, H - 5.4 * mm,
        "VERODUS  ·  Add-on BE / leftover / combinations  ·  17 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.4)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Sticker = round(list × %). After ads = sticker × 0.52 − extra E[X]. Combined = challenge Rec_left + addon leftover.",
    )
    canvas.drawRightString(W - MARGIN, 2.6 * mm, str(doc.page))
    canvas.restoreState()


def grid(data, col_w, special=None):
    special = special or {}
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 2.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        mark = special.get(i)
        if mark == "rec":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_REC))
        elif mark == "no":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_NO))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def flag(left: float) -> str:
    if left >= -1:
        return "yes"
    if left >= -5:
        return "thin"
    return "NO"


def combo_math(plan: str, list_px: float, be: float, keys: tuple[str, ...]):
    extra_f = EXTRA_F[plan]
    stick = 0
    extra = 0.0
    for k in keys:
        stick += sticker(list_px, pct_for(plan, k))
        extra += be * extra_f[k]
    addon_left = stick * 0.65 * (1.0 - MARKETING) - extra
    return stick, extra, addon_left


def sku_index(skus, ox):
    news = pd.read_csv(RESULTS / "verodus_news_included_prices.csv")
    news_ix = {(r.Plan, int(r.Size)): r for r in news.itertuples()}
    out = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if live.empty:
                continue
            oxr = ox.get((plan, sz), {})
            sale = REC[(plan, sz)]
            list_px = rec_list(sale)
            nr = news_ix.get((plan, sz))
            if nr is not None:
                be = float(nr.BE_on)
                chal_left = leftover_after_opex(sale, float(nr.Loaded_on))
            else:
                be = float(oxr.get("BE") or 0.0)
                chal_left = float(oxr.get("Rec_left") or 0.0)
            rec_m = (sale - be) / sale if sale else 0.0
            out.append({
                "Plan": plan, "Size": sz, "Sale": sale, "List": list_px,
                "BE": be, "Rec_m": rec_m, "Chal_left": chal_left,
            })
    return out


def combo_rows(skus_ix, size=100000):
    rows = []
    for sku in skus_ix:
        if sku["Size"] != size:
            continue
        for name, keys in COMBOS:
            stick, extra, addon_left = combo_math(
                sku["Plan"], sku["List"], sku["BE"], keys,
            )
            combined = sku["Chal_left"] + addon_left
            rows.append({
                **sku, "Combo": name, "Keys": keys,
                "Sticker": stick, "Extra": extra,
                "Addon_left": addon_left, "Combined": combined,
            })
    return rows


def build():
    s = styles()
    skus, _sc = load()
    ox = {(r["Plan"], r["Size"]): r for r in opex_rows(skus)}
    ix = sku_index(skus, ox)

    story = []
    story.append(P("Add-on leftover: BE, margins, and every legal combination", s["cover"]))
    story.append(P(
        "News is included on every phase (not an add-on). Remaining add-ons: weekend 15%, "
        "weekly 80% at 10%, on-demand 80% 15%/18% Instant, 90% 15%/18% Instant, "
        "90% On Demand 25%/35% Instant. VERO35 takes 35% off list + stickers. "
        "After ads = 52% of sticker minus extra E[X]. Challenge leftover uses news-on BE.",
        s["sub"],
    ))

    story.append(P("1. Challenge BE and leftover (no add-ons)", s["h1"]))
    story.append(P(
        "BE is year-1 E[X] on Instant and first-payout E[X] / (1 − P(pay)) on evals. "
        "Margin = (rec sale − BE) / rec sale. Leftover is after 10% error, $1, wage share, "
        "and 20% marketing — the opex stack, not BE alone.",
        s["body"],
    ))
    heads = ["Plan", "Size", "BE", "Rec sale", "List", "Margin", "Leftover", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(ix, start=1):
        ok = flag(r["Chal_left"])
        spec[i] = "rec" if ok == "yes" else "no"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["Sale"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(f"{100 * r['Rec_m']:.0f}%", s["td"]),
            P(usd(r["Chal_left"]), s["td"]), P(ok, s["td"]),
        ])
    story.append(grid(data, [
        28*mm, 20*mm, 22*mm, 22*mm, 20*mm, 18*mm, 24*mm, 18*mm,
    ], spec))
    story.append(P("Green = leftover ≥ −$1. Challenge rec prints on every SKU.", s["tiny"]))

    story.append(P("2. Single add-on leftover at $100k", s["h1"]))
    story.append(P(
        "Addon leftover does not include the challenge leftover. Extra E[X] is vs default "
        "80% biweekly. Instant 90% On Demand extra is ~41% of year-1 BE (~$116).",
        s["body"],
    ))
    singles = [c for c in COMBOS if len(c[1]) == 1]
    heads = ["Plan", "Add-on", "% list", "Sticker", "Extra E[X]", "After ads", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 0
    for sku in ix:
        if sku["Size"] != 100000:
            continue
        for name, keys in singles:
            i += 1
            stick, extra, left = combo_math(sku["Plan"], sku["List"], sku["BE"], keys)
            ok = flag(left)
            spec[i] = "rec" if ok == "yes" else ("no" if ok == "NO" else None)
            data.append([
                P(sku["Plan"], s["tdl"]), P(name, s["tdl"]),
                P(f"{round(100 * pct_for(sku['Plan'], keys[0]))}%", s["td"]),
                P(usd(stick), s["td"]), P(usd(extra), s["td"]),
                P(usd(left), s["td"]), P(ok, s["td"]),
            ])
    story.append(grid(data, [
        28*mm, 40*mm, 18*mm, 22*mm, 26*mm, 24*mm, 18*mm,
    ], spec))
    story.append(P(
        "Instant 90% On Demand at 35% leftover ~$11. That is the year-1 floor. "
        "Do not copy Blue Guardian Instant 15% or FundedNext +5% for 90%+anytime.",
        s["tiny"],
    ))

    story.append(P("3. Instant $100k — every legal cart", s["h1"]))
    story.append(P(
        "Weekly cannot mix with on-demand or 90%. On-demand+90% bills as 90% On Demand "
        "(35%), not 18+18. Combined leftover = challenge leftover (~$26) + addon leftover.",
        s["body"],
    ))
    inst_rows = [r for r in combo_rows(ix, 100000) if r["Plan"] == "Instant"]
    heads = ["Cart", "Sticker", "Shopper net", "Extra E[X]", "Addon after",
             "Challenge after", "Combined", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(inst_rows, start=1):
        shopper = r["Sticker"] * 0.65
        ok = flag(r["Combined"])
        spec[i] = "rec" if ok == "yes" else ("no" if ok == "NO" else None)
        data.append([
            P(r["Combo"], s["tdl"]),
            P(usd(r["Sticker"]), s["td"]),
            P(usd(shopper), s["td"]),
            P(usd(r["Extra"]), s["td"]),
            P(usd(r["Addon_left"]), s["td"]),
            P(usd(r["Chal_left"]), s["td"]),
            P(usd(r["Combined"]), s["td"]),
            P(ok, s["td"]),
        ])
    story.append(grid(data, [
        48*mm, 22*mm, 26*mm, 24*mm, 26*mm, 28*mm, 24*mm, 18*mm,
    ], spec))

    story.append(P("4. 2-Step Pro $100k — every legal cart", s["h1"]))
    story.append(P(
        "Eval extra is first-payout only. 90% On Demand at 25% matches Blue Guardian "
        "evals 25% and still prints. Challenge leftover ~$36.",
        s["body"],
    ))
    pro_rows = [r for r in combo_rows(ix, 100000) if r["Plan"] == "2-Step Pro"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(pro_rows, start=1):
        shopper = r["Sticker"] * 0.65
        ok = flag(r["Combined"])
        spec[i] = "rec" if ok == "yes" else ("no" if ok == "NO" else None)
        data.append([
            P(r["Combo"], s["tdl"]),
            P(usd(r["Sticker"]), s["td"]),
            P(usd(shopper), s["td"]),
            P(usd(r["Extra"]), s["td"]),
            P(usd(r["Addon_left"]), s["td"]),
            P(usd(r["Chal_left"]), s["td"]),
            P(usd(r["Combined"]), s["td"]),
            P(ok, s["td"]),
        ])
    story.append(grid(data, [
        48*mm, 22*mm, 26*mm, 24*mm, 26*mm, 28*mm, 24*mm, 18*mm,
    ], spec))

    story.append(P("5. 1-Step and Lite $100k — 90% On Demand and Weekend stacks", s["h1"]))
    focus = {
        "Challenge only", "Weekend", "Weekly 80%", "On-demand 80%", "90% split",
        "90% On Demand", "Weekend + weekly", "Weekend + 90% On Demand",
    }
    heads = ["Plan", "Cart", "Sticker", "Extra E[X]", "Addon after", "Combined", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 0
    for plan in ("1-Step", "2-Step Lite"):
        for r in combo_rows(ix, 100000):
            if r["Plan"] != plan or r["Combo"] not in focus:
                continue
            i += 1
            ok = flag(r["Combined"])
            spec[i] = "rec" if ok == "yes" else ("no" if ok == "NO" else None)
            data.append([
                P(plan, s["tdl"]), P(r["Combo"], s["tdl"]),
                P(usd(r["Sticker"]), s["td"]), P(usd(r["Extra"]), s["td"]),
                P(usd(r["Addon_left"]), s["td"]), P(usd(r["Combined"]), s["td"]),
                P(ok, s["td"]),
            ])
    story.append(grid(data, [
        28*mm, 48*mm, 22*mm, 24*mm, 26*mm, 24*mm, 18*mm,
    ], spec))

    story.append(P("6. Instant $100k — what would not print if copied", s["h1"]))
    inst = next(r for r in ix if r["Plan"] == "Instant" and r["Size"] == 100000)
    holes = [
        ("BG Instant 15% for 90%+anytime", 0.15, 0.41),
        ("FN +5% on-demand with 95%", 0.05, 0.41),
        ("Alpha 10% 90% + our 15% anytime stacked", 0.10 + 0.15, 0.41),
        ("Weekly 70% @ 6% (old decoy)", 0.06, 0.08),
        ("Rec Instant 90% On Demand 35%", 0.35, 0.41),
    ]
    heads = ["If Instant $100k charged…", "Sticker", "Extra E[X]", "After ads", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (name, pct, xf) in enumerate(holes, start=1):
        st = sticker(inst["List"], pct)
        extra = inst["BE"] * xf
        left = st * 0.52 - extra
        ok = flag(left)
        spec[i] = "rec" if "Rec Instant" in name else ("no" if ok == "NO" else None)
        data.append([
            P(name, s["tdl"]), P(usd(st), s["td"]), P(usd(extra), s["td"]),
            P(usd(left), s["td"]), P(ok, s["td"]),
        ])
    story.append(grid(data, [
        90*mm, 24*mm, 28*mm, 26*mm, 22*mm,
    ], spec))
    story.append(P(
        "Qty 1–4 does not change leftover per account: every copy is VERO35, no extra ladder. "
        "Four Instant $100k with 90% On Demand is 4 × the Instant row, not a discount.",
        s["tiny"],
    ))

    RESULTS.mkdir(exist_ok=True)
    pd.DataFrame(combo_rows(ix, 100000)).to_csv(
        RESULTS / "verodus_addon_combos_100k.csv", index=False,
    )
    doc = SimpleDocTemplate(
        str(OUT), pagesize=PAGE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=12 * mm, bottomMargin=11 * mm,
        title="Verodus add-on BE and combinations",
        author="Verodus",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
