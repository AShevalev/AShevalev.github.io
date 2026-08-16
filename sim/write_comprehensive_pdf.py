#!/usr/bin/env python3
"""One comprehensive Verodus industry PDF: research, math, rules, 20/40/60 grids."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Industry_Report_2026-08-16.pdf"

PAGE = landscape(A4)
W, H = PAGE
MARGIN = 12 * mm

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
RED = colors.HexColor("#9b1c1c")
GREEN = colors.HexColor("#14532d")
GOLD = colors.HexColor("#b45309")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_V = colors.HexColor("#e8f1ff")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")


def usd(x):
    if pd.isna(x):
        return "—"
    return f"${float(x):,.0f}"


def pct(x, signed=False):
    if pd.isna(x):
        return "—"
    v = 100 * float(x)
    return f"{v:+.0f}%" if signed else f"{v:.1f}%"


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    # drop Instant $200k
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    skus = skus.loc[~drop].copy()
    return skus, blend


def styles():
    base = getSampleStyleSheet()
    s = {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Times-Bold",
            fontSize=22, leading=26, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Times-Italic",
            fontSize=11, leading=14, textColor=TEAL, spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Times-Bold",
            fontSize=14, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Times-Bold",
            fontSize=11.5, leading=14, textColor=TEAL, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=9, leading=12, alignment=TA_JUSTIFY, spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"], fontName="Times-Roman",
            fontSize=9, leading=12, leftIndent=12, spaceAfter=2,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.5, leading=9.5, textColor=colors.HexColor("#334155"),
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=7, leading=9, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7, leading=9, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7, leading=9, alignment=TA_LEFT,
        ),
        "foot": ParagraphStyle(
            "foot", parent=base["Normal"], fontName="Times-Italic",
            fontSize=7.5, leading=9, textColor=colors.HexColor("#64748b"),
        ),
    }
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(MARGIN, H - 5.4 * mm, "VERODUS  ·  Industry Monte Carlo & Peer Pricing  ·  16 Aug 2026")
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(MARGIN, 2.6 * mm, "Same book for every firm. Instant $200k removed. Lite funded DD 8%. Instant rules = live FAQ.")
    canvas.drawRightString(W - MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def P(text, style):
    return Paragraph(text, style)


def grid(data, col_w, verodus_rows=None, neg_cols=None):
    verodus_rows = verodus_rows or set()
    neg_cols = neg_cols or set()
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]
    for i in range(1, len(data)):
        if i in verodus_rows:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_V))
            sty.append(("FONTNAME", (0, i), (-1, i), "Times-Bold"))
        elif i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        for c in neg_cols:
            cell = data[i][c]
            if isinstance(cell, str) and cell.startswith("−") or (isinstance(cell, str) and cell.startswith("-") and "%" in cell):
                sty.append(("TEXTCOLOR", (c, i), (c, i), RED))
            elif isinstance(cell, str) and cell.startswith("+"):
                sty.append(("TEXTCOLOR", (c, i), (c, i), GREEN))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def sku_row(r, s, with_firm=True):
    m = pct(r.sale_m, signed=True).replace("-", "−")
    cells = []
    if with_firm:
        cells.append(P(str(r.Firm), s["tdl"]))
    cells += [
        P(str(r.Plan), s["tdl"]),
        P(usd(r.Size).replace("$", "$"), s["td"]),
        P(usd(r.List), s["td"]),
        P(usd(r.Sale), s["td"]),
        P(usd(r.E_payout), s["td"]),
        P(pct(r.P_pay), s["td"]),
        P(usd(r.BE), s["td"]),
        P(usd(r.px_20), s["td"]),
        P(usd(r.px_40), s["td"]),
        P(usd(r.px_60), s["td"]),
        P(m, s["td"]),
    ]
    return cells


def sku_header(s, with_firm=True):
    labels = (["Firm"] if with_firm else []) + [
        "Plan", "Size", "List", "Sale", "E[X]", "P(pay)", "BE", "20%", "40%", "60%", "Sale m",
    ]
    return [P(x, s["th"]) for x in labels]


def build():
    skus, blend = load()
    s = styles()
    story = []
    usable = W - 2 * MARGIN

    # ----- cover -----
    story.append(P("Verodus challenge economics", s["cover"]))
    story.append(P(
        "Industry-calibrated Monte Carlo · 20 forex/CFD peers · every account size · "
        "break-even / 20% / 40% / 60% · 16 August 2026",
        s["sub"],
    ))
    story.append(P(
        "This report replaces the 15 August peer PDFs (FundingPips, FTMO, Alpha Capital, "
        "Hola Prime) with one book, one set of sensitivities, and every SKU those firms "
        "and sixteen other peers sell. Instant $200k is removed. The only Verodus "
        "<b>rule</b> change versus the live FAQ is Lite funded max drawdown 10% → 8%. "
        "Instant stays live: 6% trailing never locks, no 2% max-risk, no first-reward % cap.",
        s["body"],
    ))
    story.append(P(
        "<b>Read this as an operator document.</b> Sale is what the shopper pays after the "
        "named discount (VERO35, HELLO, FUNDED40, ALPHA20, MATCH20, or a typical ~20% promo). "
        "E[X] is expected first-payout dollars. BE is the fee that sets expected profit to zero "
        "after refunds. 20% / 40% / 60% are the fees that deliver those contribution margins "
        "before affiliate CPA.",
        s["body"],
    ))

    # ----- 1 research -----
    story.append(P("1. Industry research (2025–2026)", s["h1"]))
    story.append(P(
        "Retail prop is an estimated <b>$850M</b> fee market in 2026 (Track360), ~2.1M active "
        "traders, ~12M challenge purchases at ~$250 average fee. Five firms — FTMO, FundedNext, "
        "The5ers, Apex, Topstep — take ~62% of acquisition. This study is forex/CFD only "
        "(Verodus’s set). Futures (Topstep, Apex) are a different product and are omitted.",
        s["body"],
    ))
    story.append(P("Published funnel (the calibration target)", s["h2"]))
    story.append(P(
        "• <b>Phase 1:</b> 25–35% (FTMO/FundedNext community stage tables; traderssecondbrain 2026).<br/>"
        "• <b>Funded (both phases):</b> 5–14% of purchases. Track360 blended pass across tracked programs: <b>12.3%</b>. "
        "FTMO historically ~9–12% combined. FPFX Technology / Finance Magnates, 300k+ accounts, ~10 firms: <b>~14%</b> reach funded.<br/>"
        "• <b>Ever paid:</b> ~<b>7%</b> of all buyers (Track360; FPFX). ~45% of funded accounts receive a first payout in the Track360 summary; "
        "FundedNext has disclosed 26–32% of funded reaching payout in earlier windows.<br/>"
        "• <b>Long-term:</b> 1–3% of buyers become consistently paid.<br/>"
        "• <b>Instant / straight-to-funded sustained:</b> 4–6% (Track360 Instant / The5ers-class).<br/>"
        "• <b>Failures:</b> 60–70% of fails are a drawdown breach. Daily DD ~38–42%, max DD ~24–28%, time/abandon ~15–22%, forbidden/news ~6–10%.<br/>"
        "• <b>Topstep 2025 (futures, not in the catalog):</b> Combine pass 16.8% account-level; 33.3% of funded-level participants paid. "
        "Used only as a one-phase sanity check.",
        s["bullet"],
    ))
    story.append(P(
        "This book’s FTMO 2-step lands at <b>P1 22% / funded 13% / P(pay) 13% / year-1 4%</b> — inside the published band, "
        "slightly rich on first-payout versus the 7% ever-paid census (we count first-payout eligibility, not unique humans across retries). "
        "Instant P(pay) 22% is first-payout eligibility; Instant year-1 7.2% is the figure that matches 4–6% sustained Instant.",
        s["body"],
    ))

    # ----- 2 math -----
    story.append(P("2. Calculations and assumptions", s["h1"]))
    story.append(P("2.1 Population (the book)", s["h2"]))
    story.append(P(
        "Five profiles, weights sum to 1. Same mix on every firm and every SKU. "
        "That is the point of a peer table: only rules, split, refund, and price differ.",
        s["body"],
    ))
    pop = [
        [P(x, s["th"]) for x in ["Profile", "Weight", "Win rate", "R:R", "Trades/day", "Risk / trade", "Room awareness", "Violation / day"]],
        [P("Pro", s["tdl"]), P("7%", s["td"]), P("52%", s["td"]), P("1.50", s["td"]), P("2", s["td"]), P("0.36–0.68%", s["td"]), P("0.94", s["td"]), P("0.007%", s["td"])],
        [P("Semi-skilled", s["tdl"]), P("22%", s["td"]), P("51%", s["td"]), P("1.38", s["td"]), P("2", s["td"]), P("0.44–0.78%", s["td"]), P("0.86", s["td"]), P("0.012%", s["td"])],
        [P("Average", s["tdl"]), P("26%", s["td"]), P("49%", s["td"]), P("1.22", s["td"]), P("3", s["td"]), P("0.52–0.95%", s["td"]), P("0.72", s["td"]), P("0.018%", s["td"])],
        [P("Aggressive", s["tdl"]), P("28%", s["td"]), P("43%", s["td"]), P("0.96", s["td"]), P("6", s["td"]), P("1.50–2.60%", s["td"]), P("0.18", s["td"]), P("0.038%", s["td"])],
        [P("Lottery", s["tdl"]), P("17%", s["td"]), P("40%", s["td"]), P("0.84", s["td"]), P("8", s["td"]), P("2.40–4.20%", s["td"]), P("0.05", s["td"]), P("0.065%", s["td"])],
    ]
    story.append(grid(pop, [28*mm, 18*mm, 20*mm, 16*mm, 22*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 4*mm))
    story.append(P("2.2 Path engine", s["h2"]))
    story.append(P(
        "• Simulated on a <b>$100,000</b> notional. Dollars scale linearly with account size: "
        "E[X]<sub>size</sub> = E[X]<sub>$100k</sub> × (size / 100,000). Rules are percentages of initial, so the scale is exact inside this model.<br/>"
        "• <b>1,000 paths × 5 profiles × 47 products = 235,000</b> accounts. Seed 42.<br/>"
        "• Four market regimes (quiet / normal / volatile / chaotic) with a Markov matrix; session vol multipliers; "
        "per-trade friction 3.2 bp × (risk/1%) × regime; shock tails; tilt after losses (damped by room awareness).<br/>"
        "• Daily DD is dollars of <b>initial</b> from start-of-day equity, except Instant-class products that use the day’s equity high.<br/>"
        "• Floors: static = start×(1−dd); trailing = HWM×(1−dd); hybrid = max(trailing, start×(1−dd)), capped at start.<br/>"
        "• Horizon 280 days; 30-day inactivity kills the path. Eval passers take a <b>12% KYC / never-start</b> drop before funded. "
        "Funded paths start with tilt 0.20 and 1.05× risk (overconfidence).<br/>"
        "• Year-1 survival after first payout: 59% month 1, then 72% to month 3, then 76% to month 12 (independent of firm).<br/>"
        "• $100 minimum reward. Split as published (usually 80%; FTMO 1-Step 90%; The5ers Hyper/Bootcamp 50%; FP Flex 85%).",
        s["bullet"],
    ))
    story.append(P("2.3 Pricing identities (the 20 / 40 / 60 columns)", s["h2"]))
    story.append(P(
        "Let <i>p</i> = P(first payout), <i>X</i> = first-payout dollars (0 if unpaid), "
        "<i>F</i> = fee the shopper pays (Sale), <i>k</i> = expected refund as a fraction of the fee.",
        s["body"],
    ))
    story.append(P(
        "• <b>Refund fraction k</b><br/>"
        "&nbsp;&nbsp;none → k = 0<br/>"
        "&nbsp;&nbsp;first payout (Verodus evals, FTMO 2-Step, most 2-steps) → k = p<br/>"
        "&nbsp;&nbsp;fourth payout (FundingPips Standard / 1-Step, FundedNext 1-Step) → k = p × 0.35<br/>"
        "&nbsp;&nbsp;25% × first four (Hola) → k = p × 0.25 × (1 + 0.55 + 0.35 + 0.22)<br/>"
        "• <b>E[cost] = E[X] + k × F</b> &nbsp;&nbsp;(payouts plus expected refund at the fee actually charged)<br/>"
        "• <b>Break-even fee:</b> F = E[X] + k(F)×F &nbsp;⇒&nbsp; <b>BE = E[X] / (1 − k)</b> &nbsp;(k capped at 0.95)<br/>"
        "&nbsp;&nbsp;For Instant with no refund, BE = E[X]. For a first-payout refund, BE = E[X] / (1 − p).<br/>"
        "• <b>Fee at margin m:</b> F<sub>m</sub> = BE / (1 − m). The 20% / 40% / 60% columns are F<sub>0.20</sub>, F<sub>0.40</sub>, F<sub>0.60</sub>.<br/>"
        "• <b>Sale margin:</b> (F − E[cost]) / F. This is contribution before affiliate CPA (~10–15% of fee in this vertical). "
        "A 40% sale margin leaves ~25–30% after a 12% CPA.<br/>"
        "• <b>List margin</b> uses the same E[X] but refunds k × list (not used in the grids below).",
        s["bullet"],
    ))
    story.append(P(
        "<b>Worked Verodus Instant $5k:</b> E[X]<sub>$100k</sub> = $875.25 ⇒ E[X]<sub>$5k</sub> = 875.25 × 0.05 = <b>$43.76</b>. "
        "Refund none ⇒ k = 0 ⇒ BE = $43.76. 20% = 43.76/0.80 = <b>$55</b>. 40% = 43.76/0.60 = <b>$73</b>. "
        "60% = 43.76/0.40 = <b>$109</b>. Sale $72 ⇒ sale m = (72 − 43.76)/72 = <b>+39%</b>.",
        s["body"],
    ))
    story.append(P(
        "<b>Worked Verodus 1-Step $5k:</b> E[X]<sub>$5k</sub> = 108.10 × 0.05 = <b>$5.41</b>. "
        "Refund on first payout, p = 8.808% ⇒ k = 0.08808 ⇒ BE = 5.41 / (1 − 0.08808) = <b>$5.93</b>. "
        "E[cost] at $36 sale = 5.41 + 0.08808×36 = <b>$8.58</b>. Sale m = (36 − 8.58)/36 = <b>+76%</b>. "
        "40% fee = 5.93 / 0.60 = <b>$9.88</b> — the current $36 sale is far above a 40% target; that is unused pricing power.",
        s["body"],
    ))
    story.append(P("2.4 What is not modeled", s["h2"]))
    story.append(P(
        "Affiliate CPA, payment fees, chargebacks, KYC cost, desk/support, broker rebate, scaling after first payout, "
        "90% split add-ons, news-window clawbacks, copy-trade / EA bans as a filter, weekend flatten, striking systems, "
        "multi-account correlation, and retry purchase (the 7% ever-paid census is unique-human; our p is per challenge). "
        "E[X] is first payout only — a year-1 paid tail exists (1–3% of buyers) and is the main model risk on Instant $50k+.",
        s["body"],
    ))

    # ----- 3 rules -----
    story.append(P("3. Recommended Verodus rules (one card per category, every size)", s["h1"]))
    story.append(P(
        "Percentages are of <b>initial balance</b>. A $5k and a $100k Instant use the same card. "
        "Instant $200k is not offered. The only FAQ edit versus live is Lite funded max DD.",
        s["body"],
    ))
    rules = [
        [P(x, s["th"]) for x in ["", "Instant (live)", "1-Step (live)", "Lite (CHANGE)", "Pro (live)"]],
        [P("Phases", s["tdl"]), P("0 — funded day 1", s["td"]), P("1", s["td"]), P("2", s["td"]), P("2", s["td"])],
        [P("Target", s["tdl"]), P("None", s["td"]), P("10%", s["td"]), P("8% then 5%", s["td"]), P("10% then 5%", s["td"])],
        [P("Daily DD", s["tdl"]), P("3% from day’s equity high", s["td"]), P("4% SOD", s["td"]), P("4% SOD", s["td"]), P("5% SOD", s["td"])],
        [P("Max DD", s["tdl"]), P("6% trail, never locks", s["td"]), P("6% hybrid (locks at initial)", s["td"]), P("8% static eval + funded", s["td"]), P("10% static", s["td"])],
        [P("Consistency", s["tdl"]), P("20% best day of +days", s["td"]), P("50% best day on eval", s["td"]), P("None", s["td"]), P("None", s["td"])],
        [P("Min days", s["tdl"]), P("5 valid at +0.5% SOD", s["td"]), P("0 eval / 3 funded", s["td"]), P("5+5 / 3 funded", s["td"]), P("5+5 / 3 funded", s["td"])],
        [P("Fee refund", s["tdl"]), P("No", s["td"]), P("100% on first reward", s["td"]), P("100% on first reward", s["td"]), P("100% on first reward", s["td"])],
        [P("Split", s["tdl"]), P("80%", s["td"]), P("80%", s["td"]), P("80%", s["td"]), P("80%", s["td"])],
        [P("Min reward", s["tdl"]), P("$100", s["td"]), P("$100", s["td"]), P("$100", s["td"]), P("$100", s["td"])],
        [P("Sizes", s["tdl"]), P("$5k–$100k (no $200k)", s["td"]), P("$5k–$200k", s["td"]), P("$5k–$200k", s["td"]), P("$5k–$200k", s["td"])],
        [P("Change vs live FAQ", s["tdl"]), P("None. No trail lock, no 2% risk, no first-reward cap.", s["td"]), P("None", s["td"]), P("Funded max DD 10% → 8%", s["td"]), P("None", s["td"])],
    ]
    story.append(grid(rules, [32*mm, 52*mm, 48*mm, 48*mm, 42*mm], verodus_rows=set()))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Shared: VERO35 on every SKU · 30-day inactivity · unlimited time · daily DD in dollars of initial · "
        "one news/EA/weekend/leverage policy for the firm. Do not vary daily, consistency, or payout rules by size.",
        s["body"],
    ))

    # ----- 4 Verodus 20/40/60 -----
    story.append(P("4. Verodus — list / sale / E[X] / BE / 20 / 40 / 60", s["h1"]))
    story.append(P(
        "Live VERO35 prices. Instant $200k removed. Lite uses funded 8%. "
        "Sale m uses E[cost] at the current sale (includes expected refund on evals).",
        s["body"],
    ))
    v = skus[skus.Firm == "Verodus"].sort_values(["Family", "Plan", "Size"])
    data = [sku_header(s, with_firm=False)]
    v_rows = set()
    for i, r in enumerate(v.itertuples(), start=1):
        data.append(sku_row(r, s, with_firm=False))
        v_rows.add(i)
    colw = [38*mm, 18*mm, 18*mm, 18*mm, 20*mm, 16*mm, 18*mm, 18*mm, 18*mm, 18*mm, 16*mm]
    story.append(grid(data, colw, verodus_rows=v_rows, neg_cols={10}))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $5k sale $72 sits on the 40% column ($73). Instant $25k is already below 20%. "
        "Instant $50k/$100k are below break-even. 1-Step $5k 40% is $10 — you could charge $49 and still print. "
        "Lite $100k 40% is $254 versus sale $241 (just under). Pro $100k 40% is $251 versus sale $296 (clears 40%).",
        s["body"],
    ))

    # ----- 5 relative -----
    story.append(P("5. Relative price analysis — Verodus vs the 20-firm set", s["h1"]))
    story.append(P(
        "For each family and size, Verodus sale versus the peer distribution (same family, same size, Verodus excluded). "
        "Rank 1 = cheapest. “vs med” is Verodus sale / peer median. "
        "A cheap rank with a high sale margin is unused pricing power. A cheap rank with a negative margin is a hole.",
        s["body"],
    ))

    rel_header = [P(x, s["th"]) for x in [
        "Family", "Size", "Vero sale", "Vero m", "Peers n", "Peer min", "Peer median", "Peer max",
        "vs med", "Rank cheap", "Peer 40% med", "Vero vs 40% med",
    ]]
    rel = [rel_header]
    pairs = [
        ("instant", "Instant"),
        ("1-step", "1-Step"),
        ("2-step", "2-Step Lite"),
        ("2-step", "2-Step Pro"),
    ]
    sizes = [5000, 10000, 25000, 50000, 100000, 200000]
    for fam, plan in pairs:
        for sz in sizes:
            if fam == "instant" and sz == 200000:
                continue
            vr = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if vr.empty:
                continue
            peers = skus[(skus.Family == fam) & (skus.Size == sz) & (skus.Firm != "Verodus")]
            if peers.empty:
                continue
            vsale = float(vr.Sale.iloc[0])
            vm = float(vr.sale_m.iloc[0])
            pmin, pmed, pmax = peers.Sale.min(), peers.Sale.median(), peers.Sale.max()
            p40 = peers.px_40.median()
            cheaper = int((peers.Sale < vsale).sum())
            rank = cheaper + 1
            n = len(peers)
            rel.append([
                P(fam, s["td"]),
                P(usd(sz), s["td"]),
                P(usd(vsale), s["td"]),
                P(pct(vm, True).replace("-", "−"), s["td"]),
                P(str(n), s["td"]),
                P(usd(pmin), s["td"]),
                P(usd(pmed), s["td"]),
                P(usd(pmax), s["td"]),
                P(f"{vsale / pmed:.2f}×", s["td"]),
                P(f"{rank} / {n+1}", s["td"]),
                P(usd(p40), s["td"]),
                P(f"{vsale / p40:.2f}×" if p40 else "—", s["td"]),
            ])
    story.append(grid(rel, [22*mm, 18*mm, 20*mm, 16*mm, 16*mm, 20*mm, 22*mm, 20*mm, 16*mm, 20*mm, 24*mm, 24*mm], neg_cols={3}))
    story.append(Spacer(1, 3*mm))
    story.append(P("How to read the ranks", s["h2"]))
    story.append(P(
        "• <b>Instant $5k</b> is mid-pack (above Alpha $40 / FP $48, next to BG $71 / Hola $79). Margin +39% — you are not the cheap Instant, and you should not become it. "
        "Those cheaper Instant $5k SKUs are already red by $25k–$100k.<br/>"
        "• <b>Instant $50k/$100k</b> are cheaper than a 40% peer fee and below your own BE. Relative “value” here is a hole, not a feature.<br/>"
        "• <b>1-Step</b> is at or under the peer floor at every size (0.6–0.8× median) with +58–76% margins. That is unused pricing power, not a competitive need.<br/>"
        "• <b>Lite</b> is the cheapest or second-cheapest 2-step (tied with Maven $18 at $5k). $100k $241 is ~0.6× peer median (~$400–550). Margin +33% is the thinnest 2-step in the set.<br/>"
        "• <b>Pro</b> is FTMO’s rulebook at ~0.5× FTMO’s $100k fee ($296 vs $626) and ~0.7× peer median. Room to raise toward $449 and still undercut FTMO.",
        s["bullet"],
    ))

    # ----- 6 all peers 20/40/60 by family -----
    story.append(P("6. All 20 firms — price vs break-even / 20 / 40 / 60", s["h1"]))
    story.append(P(
        "Same columns as the 15 August FundingPips / FTMO / Alpha / Hola PDFs. Values are this book, not the 15 August 84/13.5/2.5 book. "
        "Verodus rows are highlighted. Negative sale margins in red.",
        s["body"],
    ))

    fam_titles = [
        ("instant", "6.1 Instant / straight-to-funded"),
        ("1-step", "6.2 One-step evaluations"),
        ("2-step", "6.3 Two-step evaluations"),
        ("3-step", "6.4 Three-step evaluations"),
    ]
    for fam, title in fam_titles:
        story.append(P(title, s["h2"]))
        sub = skus[skus.Family == fam].sort_values(["Firm", "Plan", "Size"])
        data = [sku_header(s, with_firm=True)]
        vset = set()
        for i, r in enumerate(sub.itertuples(), start=1):
            data.append(sku_row(r, s, with_firm=True))
            if r.Firm == "Verodus":
                vset.add(i)
        cw = [28*mm, 32*mm, 16*mm, 16*mm, 16*mm, 18*mm, 14*mm, 16*mm, 16*mm, 16*mm, 16*mm, 14*mm]
        story.append(grid(data, cw, verodus_rows=vset, neg_cols={11}))
        story.append(Spacer(1, 3*mm))

    # ----- 7 peer takeaways -----
    story.append(P("7. Peer read vs the 15 August PDFs", s["h1"]))
    story.append(P(
        "Those PDFs used a harsher book (3.5% pro / 14.5% average / 60% aggressive / 22% scalper). "
        "P(pay) was 1–4%. This book is calibrated to the industry funnel, so E[X] and BE are higher and sale margins are lower. "
        "Direction is the same: Instant $5k prints, Instant $50k+ does not; cheap 2-steps with 10% funded DD are the thin SKUs; "
        "tight 1-steps and 6/6 Pros print.",
        s["body"],
    ))
    story.append(P("FundingPips", s["h2"]))
    story.append(P(
        "Zero (their Instant) still prints at $5k (+14%) and is a hole from $10k (−18% to −87%). HELLO 20% except $100k. "
        "1-Step Flex remains their best unit (+69–81%) — 12% target, 3/12, refund on 4th. "
        "2-Step Standard is no longer the −EV Lite-class hole of the 15 August book; under this funnel it prints (+71% at $5k, +71% at $100k) "
        "because they charge $27–$544 versus Verodus Lite $18–$241. "
        "2-Step Pro (6/6, 3% daily, no refund) still prints (+75–77%). "
        "<b>Steal the Pro tightness, not the Standard sticker.</b> Do not copy Zero’s $48 $5k.",
        s["body"],
    ))
    story.append(P("FTMO", s["h2"]))
    story.append(P(
        "No sitewide sale (EUR×1.16). 1-Step: 10% target, 3% daily, 10% trail, 50% best-day, 90% split, no refund. "
        "Sale $92–$1,159, margins +54–71%. 2-Step: 10/5, 5/10 static, refund, $103–$1,253, +73–79%. "
        "Verodus 1-Step is cheaper and tighter (6% hybrid vs 10% trail) — keep the hybrid, raise toward $49/$79/$449. "
        "Verodus Pro is the same 10/5 · 5/10 at one-third the $100k fee. Raise Pro; do not tighten it to look like FP Pro.",
        s["body"],
    ))
    story.append(P("Alpha Capital", s["h2"]))
    story.append(P(
        "FUNDED40 Instant / ALPHA20 evals. Instant $40 $5k is +14% and $100k $274 is −152% — the poster child for cheap Instant. "
        "One 10% (6% trail, 40% cons, no refund) prints +61–81%. Pro 6% is the FP-Pro twin and prints. "
        "Pro 10% is Lite-class room at a higher sticker than Verodus Lite, so it still prints. "
        "Do not match Instant $40.",
        s["body"],
    ))
    story.append(P("Hola Prime", s["h2"]))
    story.append(P(
        "MATCH20. Direct Instant has 2% funded risk and a 25%×4 refund; $5k +29%, $100k −22%. "
        "1-Step Prime 10/3/6 + 2% funded risk, $47–$839, +58–77%. "
        "2-Step Prime 8/5 5/10 + 2% funded risk, $38–$751, +57–75%. "
        "Closest rule-for-rule peer. Beat them on 1-Step with refund + 4% daily (they have 3%) at a $49 $5k, not $36.",
        s["body"],
    ))
    story.append(P("The rest of the twenty", s["h2"]))
    story.append(P(
        "FundedNext Stellar Instant and FXIFY Instant Standard show P(pay) ~53% because they have <b>no daily</b> — only works if you also cap size (FN Instant max $20k) or charge more. "
        "Do not copy. Maven $18 2-step is the race Verodus Lite is in; Maven $100k +38% versus Lite +33%. "
        "The5ers Bootcamp / Maven 3-step print on ~5% P(pay) and a $14–$22 fee — skip the 3-step. "
        "E8 One / Signature are tight 1-steps (6% or 4% trail + 35–40% best-day) and print at FTMO-like stickers. "
        "BrightFunded’s $200k $238 is a listed anomaly and goes red (−32%) — ignore as a price signal.",
        s["body"],
    ))

    # ----- 8 recommendations -----
    story.append(P("8. What to do", s["h1"]))
    rec = [
        [P(x, s["th"]) for x in ["Plan", "Rules", "Today $5k / $100k", "Do this", "Target $5k / $100k"]],
        [P("Instant", s["tdl"]), P("Keep live. No $200k.", s["td"]), P("$72 +39% / $676 −29%", s["td"]),
         P("Keep $5k/$10k. Raise $25k. Raise or pull $50k+. Do not add trail lock, 2% risk, or a first-reward cap.", s["td"]),
         P("$72 / pull or $1,100+", s["td"])],
        [P("1-Step", s["tdl"]), P("Keep 6% hybrid + 50% best-day + refund.", s["td"]), P("$36 +76% / $335 +59%", s["td"]),
         P("Raise toward Hola, still under FTMO. Unused pricing power.", s["td"]),
         P("$49 / $449", s["td"])],
        [P("Lite", s["tdl"]), P("Funded DD 10% → 8%. Rest live.", s["td"]), P("$18 +52% / $241 +33%", s["td"]),
         P("Ship the 8% floor. Raise off Maven $18 toward FP Standard $27.", s["td"]),
         P("$27 / $349", s["td"])],
        [P("Pro", s["tdl"]), P("Keep 10/5 · 5/10.", s["td"]), P("$20 +55% / $296 +43%", s["td"]),
         P("Keep FTMO room. Price as the grown-up 2-step.", s["td"]),
         P("$36 / $449", s["td"])],
    ]
    story.append(grid(rec, [22*mm, 48*mm, 42*mm, 78*mm, 32*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Do not launch a 3-step. Do not default 90% split (offer as a paid add-on). Do not add an Instant fee refund. "
        "Do not vary rules by account size. Do not match Alpha Instant $40 or Maven 2-step $18. "
        "VERO35 stays — it is the shopper language; raise list if you need a higher sale.",
        s["body"],
    ))

    story.append(P("9. Sources", s["h1"]))
    story.append(P(
        "Track360 2026 industry statistics and rankings · FPFX Technology / Finance Magnates 300k-account sample · "
        "FTMO trading-objectives (1-Step / 2-Step, Aug 2026) · FundedNext Stellar pages · FundingPips trading-objectives + CryptoSlate 14 Aug 2026 · "
        "Alpha Capital Instant / One / Pro posts (FUNDED40 / ALPHA20) · Hola Prime FXEmpire 27 Jul 2026 (MATCH20) · "
        "The5ers program pages · E8, Goat, Maven, FXIFY, Instant Funding, Fintokei, For Traders, TFT, CTI, Funding Traders, "
        "Blue Guardian, BrightFunded, Ment public 2026 reviews · Verodus FAQ / index-eval.js 16 Aug 2026 (VERO35). "
        "Engine: sim/industry_book.py, catalog: sim/catalog.py, SKUs: results/industry_skus.csv.",
        s["tiny"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus Industry Monte Carlo & Peer Pricing — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
