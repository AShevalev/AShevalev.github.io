#!/usr/bin/env python3
"""News-included rec card with more leftover, still under named peers.

Uses the news-on BE from run_news_included.py. Instant stays pinned under
BG / FundingPips. Evals move up toward Alpha / Fintokei / Maven / Hola.
News is included (not sold). Remaining add-ons step into the 10–25% street band.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from write_price_rec_pdf import (
    ANCHORS, MARKETING, SIZES, UNITS, leftover_after_opex, rec_list, usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Reprice_News_Included_2026-08-17.pdf"

PAGE = landscape(A4)
W, H = PAGE
MARGIN = 10 * mm
NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_REC = colors.HexColor("#dcfce7")
ROW_CHG = colors.HexColor("#fef3c7")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")

OLD_REC = {
    ("Instant", 5000): 49, ("Instant", 10000): 69, ("Instant", 25000): 139,
    ("Instant", 50000): 239, ("Instant", 100000): 439,
    ("1-Step", 5000): 36, ("1-Step", 10000): 60, ("1-Step", 25000): 120,
    ("1-Step", 50000): 193, ("1-Step", 100000): 335, ("1-Step", 200000): 654,
    ("2-Step Lite", 5000): 42, ("2-Step Lite", 10000): 55, ("2-Step Lite", 25000): 94,
    ("2-Step Lite", 50000): 149, ("2-Step Lite", 100000): 269, ("2-Step Lite", 200000): 499,
    ("2-Step Pro", 5000): 45, ("2-Step Pro", 10000): 59, ("2-Step Pro", 25000): 95,
    ("2-Step Pro", 50000): 159, ("2-Step Pro", 100000): 289, ("2-Step Pro", 200000): 577,
}

REC = {
    ("Instant", 5000): 49, ("Instant", 10000): 69, ("Instant", 25000): 149,
    ("Instant", 50000): 239, ("Instant", 100000): 439,
    ("1-Step", 5000): 45, ("1-Step", 10000): 69, ("1-Step", 25000): 129,
    ("1-Step", 50000): 219, ("1-Step", 100000): 379, ("1-Step", 200000): 699,
    ("2-Step Lite", 5000): 49, ("2-Step Lite", 10000): 59, ("2-Step Lite", 25000): 99,
    ("2-Step Lite", 50000): 149, ("2-Step Lite", 100000): 275, ("2-Step Lite", 200000): 549,
    ("2-Step Pro", 5000): 55, ("2-Step Pro", 10000): 69, ("2-Step Pro", 25000): 109,
    ("2-Step Pro", 50000): 169, ("2-Step Pro", 100000): 309, ("2-Step Pro", 200000): 619,
}

BEAT = {
    ("Instant", 5000): "BG $54 / FP $48",
    ("Instant", 10000): "FP $70 / BG $75",
    ("Instant", 25000): "FXIFY Lite $149 / BG $156",
    ("Instant", 50000): "BG $243",
    ("Instant", 100000): "FP $444 / BG $467",
    ("1-Step", 5000): "Hola / BG $47 (Alpha $40)",
    ("1-Step", 10000): "Fintokei / Hola $71",
    ("1-Step", 25000): "Hola $135",
    ("1-Step", 50000): "Fintokei $231",
    ("1-Step", 100000): "Alpha / Fintokei / BG $398–399",
    ("1-Step", 200000): "BG $719",
    ("2-Step Lite", 5000): "stack floor (Maven $18 fails)",
    ("2-Step Lite", 10000): "Alpha 10% $62",
    ("2-Step Lite", 25000): "Ment $119 (Alpha 6% $94)",
    ("2-Step Lite", 50000): "Maven $151",
    ("2-Step Lite", 100000): "Maven $279",
    ("2-Step Lite", 200000): "Alpha 6% $638",
    ("2-Step Pro", 5000): "E8 $59",
    ("2-Step Pro", 10000): "step above Lite",
    ("2-Step Pro", 25000): "Ment $119",
    ("2-Step Pro", 50000): "Alpha 6% $174",
    ("2-Step Pro", 100000): "Alpha 6% $318",
    ("2-Step Pro", 200000): "Alpha 6% $638",
}

OLD_PCT = {
    "weekend": (0.12, 0.12), "weekly": (0.08, 0.08),
    "od80": (0.12, 0.15), "split90": (0.12, 0.15), "od90": (0.20, 0.32),
}
NEW_PCT = {
    "weekend": (0.15, 0.15), "weekly": (0.10, 0.10),
    "od80": (0.15, 0.18), "split90": (0.15, 0.18), "od90": (0.25, 0.35),
}
EXTRA = {
    "Instant": {"weekend": 0.08, "weekly": 0.08, "od80": 0.12, "split90": 0.125, "od90": 0.41},
    "1-Step": {"weekend": 0.04, "weekly": 0.05, "od80": 0.05, "split90": 0.125, "od90": 0.125},
}
EXTRA["2-Step Lite"] = dict(EXTRA["1-Step"])
EXTRA["2-Step Pro"] = dict(EXTRA["1-Step"])
ADDON_NAMES = (
    ("weekend", "Weekend"),
    ("weekly", "Weekly 80%"),
    ("od80", "On Demand 80%"),
    ("split90", "90% split"),
    ("od90", "90% On Demand"),
)


def js_round(x: float) -> int:
    return int(x + 0.5) if x >= 0 else int(x - 0.5)


def sticker(list_px: float, pct: float) -> int:
    return js_round(float(list_px) * float(pct))


def pct_for(plan: str, key: str, table=NEW_PCT) -> float:
    ev, inst = table[key]
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
            fontSize=6.3, leading=8, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.3, leading=8, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.3, leading=8, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7, leading=9, textColor=colors.HexColor("#334155"),
        ),
    }


def P(text, style):
    return Paragraph(str(text), style)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        MARGIN, H - 5.4 * mm,
        "VERODUS  ·  Reprice after news-included  ·  17 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.4)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "News included. Instant pinned under BG/FP. Evals step up under Alpha / Fintokei / Maven / Hola. VERO35 still 35% off list.",
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
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 1.8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.8),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        mark = special.get(i)
        if mark == "rec":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_REC))
        elif mark == "chg":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_CHG))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def load_news():
    px = pd.read_csv(RESULTS / "verodus_news_included_prices.csv")
    return {(r.Plan, int(r.Size)): r for r in px.itertuples()}


def build():
    s = styles()
    news = load_news()
    rows = []
    old_pnl = new_pnl = old_rev = new_rev = 0.0
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            k = (plan, sz)
            if k not in REC:
                continue
            r = news[k]
            n = UNITS[k]
            loaded = float(r.Loaded_on)
            old_s, new_s = OLD_REC[k], REC[k]
            left0 = leftover_after_opex(old_s, loaded)
            left1 = leftover_after_opex(new_s, loaded)
            old_pnl += left0 * n
            new_pnl += left1 * n
            old_rev += old_s * n
            new_rev += new_s * n
            rows.append({
                "Plan": plan, "Size": sz, "N": n, "BE": float(r.BE_on),
                "S_opex": float(r.S_opex_on), "Old": old_s, "New": new_s,
                "List": rec_list(new_s), "Left0": left0, "Left1": left1,
                "Beat": BEAT[k], "Changed": new_s != old_s,
            })

    story = []
    story.append(P("Reprice: more leftover, still under the named peer", s["cover"]))
    story.append(P(
        "News is included on every phase and funded account — not an add-on. "
        f"Book leftover after opex + 20% ads ${old_pnl:,.0f}/mo → ${new_pnl:,.0f}/mo "
        f"(+${new_pnl - old_pnl:,.0f}). Sale ${old_rev:,.0f} → ${new_rev:,.0f}. "
        f"Leftover / sale {100 * old_pnl / old_rev:.1f}% → {100 * new_pnl / new_rev:.1f}%. "
        "Instant barely moves: $5k–$10k / $50k–$100k are already $1–$5 under FundingPips or Blue Guardian.",
        s["sub"],
    ))

    story.append(P("1. Rule", s["h1"]))
    story.append(P(
        "Use the news-on BE. Keep leftover ≥ ~$7 on small SKUs. Do not match a peer that fails "
        "the opex stack (Maven $5k–$25k, Alpha Instant, BrightFunded $200k). Instant stays under "
        "Blue Guardian and FundingPips Zero. 1-Step sits under the Alpha / Fintokei / BG $398–399 "
        "cluster and under Hola at $25k. Lite stays $2–$4 under Maven where Maven covers "
        "($50k / $100k). Pro stays a step above Lite and under Alpha Pro 6% from $50k. "
        "List = round(sale / 0.65). VERO35 still 35% off list.",
        s["body"],
    ))

    story.append(P("2. Challenge rec — old vs new", s["h1"]))
    heads = ["Plan", "Size", "BE", "Opex", "Was", "Now", "List", "Left was", "Left now", "Beat"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "chg" if r["Changed"] else "rec"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["S_opex"]), s["td"]),
            P(usd(r["Old"]), s["td"]), P(usd(r["New"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(usd(r["Left0"]), s["td"]),
            P(usd(r["Left1"]), s["td"]), P(r["Beat"], s["tdl"]),
        ])
    story.append(grid(data, [
        24*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm, 18*mm, 18*mm, 52*mm,
    ], spec))
    story.append(P(
        "Yellow = sale moved. Green = Instant pinned to the street ceiling. "
        "1-Step $5k $45 is $5 over Alpha One $40 and $2 under Hola/BG $47 — Alpha is the "
        "closest peer; take the leftover rather than sit at $1 after news-on BE.",
        s["tiny"],
    ))

    story.append(P("3. Sale card (VERO35)", s["h1"]))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        spec[i] = "rec"
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            k = (plan, sz)
            if k not in REC:
                cells.append(P("—", s["td"]))
                continue
            old, new = OLD_REC[k], REC[k]
            cells.append(P(usd(new) if old == new else f"{usd(old)} → <b>{usd(new)}</b>", s["td"]))
        data.append(cells)
    story.append(grid(data, [
        28*mm, 32*mm, 32*mm, 32*mm, 32*mm, 32*mm, 32*mm,
    ], spec))

    story.append(P("4. Add-on rec — news dropped, percents into the street band", s["h1"]))
    story.append(P(
        "News is included, so the 12% News SKU and the 20% Swing bundle are gone. "
        "Weekend 12→15% (live was 18%). Weekly 8→10% (BG 7-day is 15% on evals). "
        "On Demand 80% 12/15→15/18 Instant. 90% 12/15→15/18 Instant (BG Instant 90% is 15%; "
        "evals match BG 15%). 90% On Demand 20/32→25/35 Instant. Evals 25% matches BG’s "
        "90%+7-day both-25%. Instant 35% is the year-1 floor with a ~$11 cushion; do not "
        "copy BG Instant 15%.",
        s["body"],
    ))
    heads = ["Add-on", "Was evals / Instant", "Now evals / Instant", "Street"]
    menu = [
        ("News", "12% / 12%", "included", "often free on evals"),
        ("Weekend", "12% / 12%", "15% / 15%", "live 18%; Swing SKUs 10–20%"),
        ("Swing", "20% / 20%", "drop", "news already in the fee"),
        ("Weekly 80%", "8% / 8%", "10% / 10%", "BG 7-day 15% evals"),
        ("On Demand 80%", "12% / 15%", "15% / 18%", "BG Instant includes OD at 80%"),
        ("90% split", "12% / 15%", "15% / 18%", "Alpha 10, BG 15, FXIFY 20"),
        ("90% On Demand", "20% / 32%", "25% / 35%", "BG evals both 25%; Instant 15% is a hole"),
    ]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(menu, start=1):
        spec[i] = "chg" if "included" in row[2] or "drop" in row[2] else "rec"
        data.append([P(c, s["tdl"] if j == 0 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [40*mm, 40*mm, 45*mm, 70*mm], spec))

    story.append(P("5. Remaining add-on leftover at $100k (new list × new %)", s["h1"]))
    heads = ["Plan", "Add-on", "%", "Sticker", "Extra E[X]", "After ads"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 0
    for plan, _fam in ANCHORS:
        k = (plan, 100000)
        r = news[k]
        lst = rec_list(REC[k])
        be = float(r.BE_on)
        for key, name in ADDON_NAMES:
            i += 1
            spec[i] = "rec"
            pct = pct_for(plan, key)
            st = sticker(lst, pct)
            extra = be * EXTRA[plan][key]
            left = st * 0.65 * (1.0 - MARKETING) - extra
            data.append([
                P(plan, s["tdl"]), P(name, s["tdl"]),
                P(f"{round(100 * pct)}%", s["td"]),
                P(usd(st), s["td"]), P(usd(extra), s["td"]), P(usd(left), s["td"]),
            ])
    story.append(grid(data, [
        28*mm, 36*mm, 16*mm, 22*mm, 26*mm, 24*mm,
    ], spec))
    story.append(P(
        "After ads = sticker × 0.52 − extra E[X]. Instant 90% On Demand at 35% leftover ~$11 "
        "(was ~$1 at 32%). Do not cut it to BG’s 15%.",
        s["tiny"],
    ))

    story.append(P("6. $100k stickers after the move", s["h1"]))
    heads = ["Plan", "Sale", "List", "Weekend 15%", "Weekly 10%", "OD 80%", "90%", "90% OD"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        spec[i] = "rec"
        k = (plan, 100000)
        lst = rec_list(REC[k])
        data.append([
            P(plan, s["tdl"]), P(usd(REC[k]), s["td"]), P(usd(lst), s["td"]),
            P(usd(sticker(lst, pct_for(plan, "weekend"))), s["td"]),
            P(usd(sticker(lst, pct_for(plan, "weekly"))), s["td"]),
            P(usd(sticker(lst, pct_for(plan, "od80"))), s["td"]),
            P(usd(sticker(lst, pct_for(plan, "split90"))), s["td"]),
            P(usd(sticker(lst, pct_for(plan, "od90"))), s["td"]),
        ])
    story.append(grid(data, [
        28*mm, 20*mm, 18*mm, 28*mm, 26*mm, 24*mm, 22*mm, 24*mm,
    ], spec))

    story.append(P("7. What not to do", s["h1"]))
    story.append(P(
        "Do not raise Instant $5k / $10k / $50k / $100k — each is already $1–$5 under "
        "FundingPips or Blue Guardian. Do not copy Maven $18 / $35 / $79 (opex hole). "
        "Do not copy Alpha Instant $274 at $100k. Do not put News back on checkout. "
        "Do not sell Swing at 20%. Door headline stays Instant from $49; 1-Step from $45; "
        "Lite from $49; Pro from $55.",
        s["body"],
    ))

    RESULTS.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(RESULTS / "verodus_reprice_news_included.csv", index=False)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=PAGE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=12 * mm, bottomMargin=11 * mm,
        title="Verodus reprice after news-included",
        author="Verodus",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUT, rows, old_pnl, new_pnl


if __name__ == "__main__":
    path, rows, old_pnl, new_pnl = build()
    print(f"Wrote {path}")
    print(f"Book leftover ${old_pnl:,.0f} → ${new_pnl:,.0f}")
