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


WEIGHTS = {
    "Pro": 0.07, "Semi-skilled": 0.22, "Average": 0.26,
    "Aggressive": 0.28, "Lottery": 0.17,
}

# Instant sale must print (m > 0). Floor = 20% column; $5k/$10k already above it.
# Attractive (median) card lives in write_price_rec_pdf.py — different objective.
PROPOSED = {
    ("Instant", 5000): 72,
    ("Instant", 10000): 121,
    ("Instant", 25000): 274,
    ("Instant", 50000): 547,
    ("Instant", 100000): 1094,
    ("1-Step", 5000): 49,
    ("1-Step", 10000): 79,
    ("1-Step", 25000): 159,
    ("1-Step", 50000): 249,
    ("1-Step", 100000): 449,
    ("1-Step", 200000): 799,
    ("2-Step Lite", 5000): 27,
    ("2-Step Lite", 10000): 49,
    ("2-Step Lite", 25000): 99,
    ("2-Step Lite", 50000): 179,
    ("2-Step Lite", 100000): 349,
    ("2-Step Lite", 200000): 649,
    ("2-Step Pro", 5000): 36,
    ("2-Step Pro", 10000): 59,
    ("2-Step Pro", 25000): 119,
    ("2-Step Pro", 50000): 229,
    ("2-Step Pro", 100000): 449,
    ("2-Step Pro", 200000): 799,
}

UNIQUE = {
    ("Verodus", "Instant"): "3% peak daily · 6% trail never locks · 20% cons · 5 valid +0.5% · no refund",
    ("Blue Guardian", "Instant"): "3% SOD daily of initial · 6% trail LOCKS at +6% + 1% buffer · 20% cons · BG25",
    ("FundingPips", "Zero"): "3/5 trail locks at +5% · 15% cons · 7 days · HELLO 20% except $100k",
    ("Alpha Capital", "Instant"): "cheap sticker · FUNDED40 · 6% trail class · no refund",
    ("Hola Prime", "Direct"): "2% funded risk · 25%×4 refund · MATCH20",
    ("FundedNext", "Stellar Instant"): "NO daily · size cap $20k · refund on first · P(pay)~53%",
    ("FXIFY", "Instant Lite"): "4% trail locks · 3% peak daily · 20% cons",
    ("FXIFY", "Instant Standard"): "8% trail · NO daily · P(pay)~54%",
    ("Goat Funded", "Instant GOAT"): "3/6 trail · 2% float · 15% cons",
    ("Instant Funding", "Instant"): "3/6 Instant-class · ~20% promo",
    ("Verodus", "1-Step"): "10% · 4% SOD · 6% hybrid · 50% best-day eval · refund",
    ("FTMO", "1-Step"): "10% · 3% daily · 10% trail · 50% cons · 90% split · no refund",
    ("Blue Guardian", "1-Step Standard"): "10/4/8 static · looser than Vero hybrid · refund",
    ("Hola Prime", "1-Step Prime"): "10/3/6 · 2% funded risk · MATCH20 · 25%×4 refund",
    ("FundingPips", "1-Step Flex"): "12% target · 3/12 · refund 4th · HELLO",
    ("Alpha Capital", "One 10%"): "6% trail · 40% cons · ALPHA20 · no refund",
    ("Verodus", "2-Step Lite"): "8/5 · 4/8 static eval+funded · refund · cheapest 2-step",
    ("Verodus", "2-Step Pro"): "10/5 · 5/10 static · FTMO room · refund",
    ("FTMO", "2-Step"): "10/5 · 5/10 · no sale · refund · $626 at $100k",
    ("Blue Guardian", "2-Step Standard"): "8/5 · 4/10 · refund · mid sticker",
    ("FundingPips", "2-Step Standard"): "HELLO · refund 4th · $544 at $100k",
    ("FundingPips", "2-Step Pro"): "6/6 · 3% daily · no refund · tight",
    ("Maven", "2-Step"): "Maven $18 race · 10% funded class",
    ("Hola Prime", "2-Step Prime"): "8/5 · 5/10 · 2% funded risk · MATCH20",
}

STREET = [
    ("Verodus", "VERO35", "35%", "Sitewide on every SKU"),
    ("Blue Guardian", "BG25", "25%", "Live 16 Aug 2026 — all CFD & futures. Instant $5k $54 / $100k $467"),
    ("FundingPips", "HELLO", "20%", "First challenge; excludes $100k. Affiliate FP/2C14A034 also 20–25%"),
    ("FTMO", "none / €101 off $10k", "0–42%", "No sitewide sale. Occasional $10k-only cut if no active 10k"),
    ("FundedNext", "HOLY15 / 5BESTOFF / FNF30", "5–30%", "Rotating; 30% is first-challenge seasonal"),
    ("Alpha Capital", "FUNDED40 / ALPHA20–30", "20–40%", "Instant 40%; evals 20–30%"),
    ("Hola Prime", "MATCH20", "20%", "Prop Firm Match affiliate code, still live"),
    ("FXIFY", "HOT20 / NEW30", "20–30%", "HOT20 summer to 1 Sep 2026 excl. Instant Lite; NEW30 2-phase Pro"),
    ("The5ers", "PROPFXD", "25%", "Aggregator listing Aug 2026"),
    ("Goat Funded", "promo 20–40%", "20–40%", "Stacking promos; do not treat 40% as list"),
    ("Maven", "INVEST", "15–20%", "Street is still the $18 $5k 2-step"),
    ("E8 Markets", "SAVE2TRADE / ELLIOTE8", "5–10%", "Rarely deep-discounts; stickers already high"),
    ("Instant Funding", "~20% typical", "20%", "Same band as FXIFY Instant"),
    ("Fintokei", "20% listed", "20%", "On-site 20% off"),
    ("The Funded Trader", "~20% typical", "20%", "Standard mid-tier"),
    ("City Traders Imperium", "APR30-class", "20–30%", "Seasonal 30% still cycles"),
    ("Funding Traders", "~20% typical", "20%", "Mid-tier 2-step"),
    ("For Traders", "~20% typical", "20%", "Mid-tier 2-step"),
    ("BrightFunded", "~20% typical", "20%", "$200k list is an anomaly — ignore"),
    ("Ment Funding", "~20% typical", "20%", "Seacrest-class mid-tier"),
]


def load():
    skus = pd.read_csv(RESULTS / "industry_skus.csv")
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    fails = pd.read_csv(RESULTS / "industry_failures.csv")
    drop = (skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == 200000)
    skus = skus.loc[~drop].copy()
    return skus, blend, fails


def sale_margin(sale, e_payout, k):
    e_cost = e_payout + k * sale
    return (sale - e_cost) / sale if sale else float("nan")


def proposed_sale(plan, size, live_sale, px20):
    key = (plan, int(size))
    if key in PROPOSED:
        return float(PROPOSED[key])
    # Instant floor: never below 20% column
    if plan == "Instant":
        return max(float(live_sale), float(px20))
    return float(live_sale)


def fail_bucket(reason):
    r = str(reason)
    if "daily_dd" in r:
        return "Daily DD"
    if "max_dd" in r:
        return "Max DD"
    if "time_abandon" in r or "inactivity" in r:
        return "Time / abandon"
    if "rule_violation" in r or "max_risk" in r:
        return "Rule / news"
    if "kyc" in r:
        return "KYC drop"
    if r.startswith("post_m"):
        return "Post-payout attrition"
    if "min_reward" in r:
        return "Min reward"
    return "Other"


def weighted_fail_mix(fails, product=None):
    df = fails.copy()
    if product:
        df = df[df.Product == product]
    if df.empty:
        return {}
    df["w"] = df.Profile.map(WEIGHTS).fillna(0.0)
    df["ws"] = df.Share * df.w
    if product is None:
        n_prod = df.Product.nunique()
        df["ws"] = df["ws"] / max(n_prod, 1)
    out = df.groupby(df.Reason.map(fail_bucket))["ws"].sum().to_dict()
    return out


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
    canvas.drawString(MARGIN, 2.6 * mm, "Same book. Instant $200k removed. Instant proposed ≥20% margin. BG Instant = live BG25 + SOD daily + trail lock.")
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
    skus, blend, fails = load()
    s = styles()
    story = []
    usable = W - 2 * MARGIN

    # ----- cover -----
    story.append(P("Verodus challenge economics", s["cover"]))
    story.append(P(
        "Industry-calibrated Monte Carlo · 20 forex/CFD peers · Blue Guardian Instant · "
        "street sales · failure metrics · proposed prices that print · 16 August 2026",
        s["sub"],
    ))
    story.append(P(
        "This is the single operator book. It replaces the 15 August peer PDFs and the earlier "
        "16 August draft. Instant $200k is removed. The only Verodus <b>rule</b> change versus "
        "the live FAQ is Lite funded max drawdown 10% → 8%. Instant stays live: 6% trailing "
        "<b>never locks</b>, no 2% max-risk, no first-reward % cap. Instant <b>prices</b> on "
        "$25k / $50k / $100k are raised so every Instant SKU prints (sale margin ≥ +20%). "
        "Blue Guardian Instant is the closest rule twin and is priced off the live BG25 shop.",
        s["body"],
    ))
    story.append(P(
        "<b>Read this as an operator document.</b> Sale is what the shopper pays after the "
        "named discount (VERO35, BG25, HELLO, FUNDED40, ALPHA20, MATCH20, HOT20, or a typical "
        "~20% promo). E[X] is expected first-payout dollars. BE is the fee that sets expected "
        "profit to zero after refunds. 20% / 40% / 60% are the fees that deliver those "
        "contribution margins before affiliate CPA.",
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
    story.append(P("1.1 August 2026 failure-rate literature (operator reading)", s["h2"]))
    story.append(P(
        "Nine trader-facing write-ups were read against this book. They do <b>not</b> move the "
        "calibration. They confirm the same funnel and they add a firm-side reading of why "
        "accounts die. The 99.72% “never earn a split” figure (Power Trading Group / Medium) "
        "is treated as an outlier — it is closer to “make a living” than to first-payout "
        "eligibility, and it conflicts with Track360 / FPFX. QuantVPS’s “7% of funded get "
        "paid” is the same collision: Track360’s 7% is of <b>all buyers</b>, not of funded. "
        "We keep the book.",
        s["body"],
    ))
    story.append(P(
        "• <b>TradersYard:</b> 90–95% fail first attempt; &lt;7–10% ever funded; 6–7% of funded "
        "paid. Trailing DD and tight daily raise failure; static DD and one-step lower it. "
        "~80% of fails blamed on risk; half of fails were in profit at some point.<br/>"
        "• <b>ThePropFirmGuide:</b> 5–10% pass; most fails in week 1 on daily loss, not a missed "
        "target. Daily 45–55% of fails; trailing 20–30%; consistency 10–15%; time 5–10%. "
        "2–4 attempts before first fund. ~60% of 2020–23 firms gone. $100k is the modal size. "
        "Industry fee pool cited $2–4B (wider than Track360’s $850M forex/CFD slice).<br/>"
        "• <b>JP Trading Capital:</b> 80% fail in 30 days. Daily 45% / max DD 28% / consistency "
        "17% / overnight 10%. First-attempt pass 18–22% by size (optimistic vs census). "
        "3–5 attempts to first pass. EA users 2.3× pass rate — a filter, not a price input.<br/>"
        "• <b>Pipcy:</b> 80–95% fail; FPFX 300k → 7% of passers ever paid; TFT 5% pass; "
        "PickMyTrade 94% fail. Funnel: 100 pay → 10–15 funded → 2–4 paid → 1 career. "
        "Fails cluster days 1–7 and near the target.<br/>"
        "• <b>Velotrade:</b> Pass &lt;10%. Revenge trading, misunderstood trail vs static, "
        "time pressure, oversize, strategy/rule mismatch. Tick trail harder than EOD trail. "
        "Profitable personal-account traders still fail on short-window variance.<br/>"
        "• <b>Power Trading Group (Medium):</b> 0.28% “earn a profit split”; $180k fees per "
        "paid trader. Use as a marketing-psychology warning, not a pricing input.<br/>"
        "• <b>Axcera (retention):</b> 94% fail the challenge; 7% ever paid; 98% of funded gone "
        "in 6 months (TradingView survey). Typical user spends $600–800 across retries. "
        "Future P&amp;L is retention and LTV, not a cheaper Instant sticker.<br/>"
        "• <b>PropScorer (50k funded accounts):</b> 41% of funded die in month 1; +28% by month 3; "
        "+24% by month 12; <b>7% of funded survive year 1</b>. Causes among funded: size creep "
        "31%, strategy drift 24%, revenge 19%, news 12%, no cash buffer 8%, platform 5%. "
        "This is why Instant year-1 (7.2% of buyers) is the number that must price Instant, "
        "not first-payout 22%.<br/>"
        "• <b>QuantVPS:</b> 5–10% pass; 7% of funded paid (we reject that as a buyer-level "
        "rate). Futures pass rates (Apex 15–20%) are a different product.",
        s["bullet"],
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
        "Live Instant $5k sale $72 sits on the 40% column ($73). Live Instant $25k is +10% "
        "(below 20%). Live Instant $50k/$100k are below break-even. "
        "<b>Proposed Instant</b> (section 5) lifts $25k / $50k / $100k to the 20% column so "
        "every Instant SKU prints without adding trail-lock, 2% risk, or a first-reward cap. "
        "1-Step $5k 40% is $10 — you could charge $49 and still print. "
        "Lite $100k 40% is $254 versus sale $241 (just under). Pro $100k 40% is $251 versus sale $296 (clears 40%).",
        s["body"],
    ))

    # ----- 5 proposed Verodus (Instant prints) -----
    story.append(P("5. Proposed Verodus prices — Instant in the positive", s["h1"]))
    story.append(P(
        "Rules stay the live FAQ (Instant never locks). Only the <b>sticker</b> moves. "
        "Instant proposed sale = max(live VERO35, 20% column). That is the lowest fee at which "
        "every Instant size has a positive contribution after E[X]. $5k and $10k already clear "
        "20% and are left alone. $25k / $50k / $100k rise. Evals keep the earlier raise toward "
        "Hola / FTMO / FP Standard — they already print; the raise is unused pricing power, "
        "not a rescue. List stays VERO35 (sale ÷ 0.65, rounded).",
        s["body"],
    ))
    prop_h = [P(x, s["th"]) for x in [
        "Plan", "Size", "Live list", "Live sale", "Live m", "E[X]", "BE", "20%",
        "Proposed sale", "Proposed list", "Proposed m", "Action",
    ]]
    prop = [prop_h]
    v = skus[skus.Firm == "Verodus"].sort_values(["Family", "Plan", "Size"])
    for r in v.itertuples():
        live = float(r.Sale)
        ps = proposed_sale(r.Plan, r.Size, live, r.px_20)
        k = 0.0 if r.Refund == "none" else float(r.P_pay) * (
            1.0 if r.Refund == "first" else 0.35 if r.Refund == "fourth" else 0.53
        )
        if r.Refund == "first":
            k = float(r.P_pay)
        elif r.Refund == "none":
            k = 0.0
        pm = sale_margin(ps, float(r.E_payout), k)
        pl = round(ps / 0.65) if ps else 0
        if abs(ps - live) < 0.5:
            act = "Keep"
        elif ps > live:
            act = "Raise"
        else:
            act = "Cut"
        prop.append([
            P(str(r.Plan), s["tdl"]),
            P(usd(r.Size), s["td"]),
            P(usd(r.List), s["td"]),
            P(usd(live), s["td"]),
            P(pct(r.sale_m, True).replace("-", "−"), s["td"]),
            P(usd(r.E_payout), s["td"]),
            P(usd(r.BE), s["td"]),
            P(usd(r.px_20), s["td"]),
            P(usd(ps), s["td"]),
            P(usd(pl), s["td"]),
            P(pct(pm, True).replace("-", "−"), s["td"]),
            P(act, s["td"]),
        ])
    story.append(grid(prop, [
        28*mm, 16*mm, 18*mm, 18*mm, 16*mm, 16*mm, 16*mm, 16*mm, 24*mm, 22*mm, 20*mm, 16*mm,
    ], neg_cols={4, 10}))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Instant $100k proposed $1,094 is 1.62× the live $676 and 2.34× Blue Guardian’s live "
        "$467. That is the point. BG Instant, FP Zero, and Alpha Instant are selling $100k "
        "below their own E[X]. Matching them is how Instant becomes a hole. $5k Instant stays "
        "$72 — already the 40% column, already next to (not under) BG’s $54.",
        s["body"],
    ))

    # ----- 6 relative -----
    story.append(P("6. Relative price analysis — live Verodus vs the 20-firm set", s["h1"]))
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
        "• <b>Instant $5k</b> is mid-pack (above Alpha $40 / FP $48 / live BG $54, next to Hola $79). Margin +39% — you are not the cheap Instant, and you should not become it. "
        "BG Instant $5k is now $54 with BG25 and still only +16%; their $10k+ is red.<br/>"
        "• <b>Live Instant $50k/$100k</b> are cheaper than a 40% peer fee and below your own BE. Relative “value” here is a hole. Proposed $547 / $1,094 fixes it without touching rules.<br/>"
        "• <b>1-Step</b> is at or under the peer floor at every size (0.6–0.8× median) with +58–76% margins. That is unused pricing power, not a competitive need.<br/>"
        "• <b>Lite</b> is the cheapest or second-cheapest 2-step (tied with Maven $18 at $5k). $100k $241 is ~0.6× peer median (~$400–550). Margin +33% is the thinnest 2-step in the set.<br/>"
        "• <b>Pro</b> is FTMO’s rulebook at ~0.5× FTMO’s $100k fee ($296 vs $626) and ~0.7× peer median. Room to raise toward $449 and still undercut FTMO.",
        s["bullet"],
    ))

    # ----- 6 all peers 20/40/60 by family -----
    story.append(P("7. All 20 firms — price vs break-even / 20 / 40 / 60", s["h1"]))
    story.append(P(
        "Same columns as the 15 August FundingPips / FTMO / Alpha / Hola PDFs. Values are this book, not the 15 August 84/13.5/2.5 book. "
        "Verodus rows are highlighted. Negative sale margins in red.",
        s["body"],
    ))

    fam_titles = [
        ("instant", "7.1 Instant / straight-to-funded"),
        ("1-step", "7.2 One-step evaluations"),
        ("2-step", "7.3 Two-step evaluations"),
        ("3-step", "7.4 Three-step evaluations"),
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
    story.append(P("8. Peer read vs the 15 August PDFs", s["h1"]))
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

    # ----- 9 Blue Guardian Instant -----
    story.append(P("9. Blue Guardian Instant — the closest twin", s["h1"]))
    story.append(P(
        "Blue Guardian Instant is the product shoppers will put next to Verodus Instant. "
        "Both are 0-step, 3% daily, 6% trailing, 20% consistency, 80% split, $5k–$100k, "
        "no time limit. The differences that move money are small on the FAQ and large on "
        "the P&amp;L.",
        s["body"],
    ))
    bg_rules = [
        [P(x, s["th"]) for x in ["Rule", "Verodus Instant (live FAQ)", "Blue Guardian Instant (help + shop 16 Aug 2026)"]],
        [P("Daily DD", s["tdl"]),
         P("3% of initial from the <b>day’s equity high</b> (tightens on a winning day)", s["tdl"]),
         P("3% of initial from the <b>day’s starting balance</b> (SOD; does not tighten intraday)", s["tdl"])],
        [P("Max DD", s["tdl"]),
         P("6% trailing HWM, <b>never locks</b>", s["tdl"]),
         P("6% trailing HWM, <b>locks at initial once +6%</b>, then a 1% withdrawal buffer", s["tdl"])],
        [P("Valid days", s["tdl"]),
         P("5 days with closed day ≥ 0.5% of SOD", s["tdl"]),
         P("5 days; any traded day counts", s["tdl"])],
        [P("Consistency", s["tdl"]),
         P("20% best day of positive days (blocks payout, does not breach)", s["tdl"]),
         P("Same 20% payout gate", s["tdl"])],
        [P("Refund / split", s["tdl"]),
         P("No refund · 80% (90% add-on)", s["tdl"]),
         P("No refund · 80% (90% add-on)", s["tdl"])],
        [P("Street sale", s["tdl"]),
         P("VERO35: $72 / $121 / $242 / $389 / $676", s["tdl"]),
         P("BG25 25% off: $54 / $75 / $156 / $243 / $467", s["tdl"])],
        [P("This book P(pay) / E[X] $100k / year-1", s["tdl"]),
         P("22.1% · $875 · 7.2%", s["tdl"]),
         P("22.1% · $911 · 7.1%  (lock + SOD daily raise extractable profit)", s["tdl"])],
    ]
    story.append(grid(bg_rules, [32*mm, 90*mm, 110*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "The lock is the one rule Verodus was told not to copy. It is also why BG Instant "
        "costs <b>more</b> to operate ($911 vs $875 at $100k) while they charge <b>less</b> "
        "($467 vs live $676, vs proposed $1,094). Once the trail locks at start, a winner "
        "can withdraw down to the 1% buffer. Verodus’s never-lock floor keeps rising with "
        "HWM, so the same winner leaves more on the table — and still we must not match "
        "their $467. BG Instant $5k at $54 still prints (+16%). From $10k they are already "
        "red (−22% / −46% / −88% / −95%). Their Instant is a customer-acquisition SKU, "
        "not a unit-economic SKU. Do not follow them down.",
        s["body"],
    ))
    bg_cmp = [ [P(x, s["th"]) for x in [
        "Size", "Vero live", "Vero live m", "Vero proposed", "Vero prop. m",
        "BG sale BG25", "BG m", "BG 20%", "Vero prop. vs BG",
    ]] ]
    for sz in (5000, 10000, 25000, 50000, 100000):
        vr = skus[(skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == sz)]
        bg = skus[(skus.Firm == "Blue Guardian") & (skus.Plan == "Instant") & (skus.Size == sz)]
        if vr.empty or bg.empty:
            continue
        v, b = vr.iloc[0], bg.iloc[0]
        ps = proposed_sale("Instant", sz, v.Sale, v.px_20)
        pm = sale_margin(ps, float(v.E_payout), 0.0)
        bg_cmp.append([
            P(usd(sz), s["td"]),
            P(usd(v.Sale), s["td"]),
            P(pct(v.sale_m, True).replace("-", "−"), s["td"]),
            P(usd(ps), s["td"]),
            P(pct(pm, True).replace("-", "−"), s["td"]),
            P(usd(b.Sale), s["td"]),
            P(pct(b.sale_m, True).replace("-", "−"), s["td"]),
            P(usd(b.px_20), s["td"]),
            P(f"{ps / b.Sale:.2f}×", s["td"]),
        ])
    story.append(grid(bg_cmp, [20*mm, 22*mm, 22*mm, 26*mm, 24*mm, 26*mm, 18*mm, 20*mm, 28*mm],
                      neg_cols={2, 4, 6}))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Read the last column as “how much more we must charge than BG to stay solvent,” "
        "not as a conversion problem. At $100k the solvent Instant is 2.3× BG’s sale because "
        "BG is 0.41× their own 20% fee ($1,139). Copying BG Instant’s <b>rules</b> (lock, "
        "SOD daily, drop the 0.5% valid-day) would raise our E[X] toward $911 and force "
        "an even higher sticker. Keep the harder Instant card and price it.",
        s["body"],
    ))

    # ----- 10 street sales / PFM -----
    story.append(P("10. Street sales — Prop Firm Match and the August 2026 promo book", s["h1"]))
    story.append(P(
        "The live Prop Firm Match FX+crypto challenge table "
        "(propfirmmatch.com/prop-firm-challenges, assets = fx + crypto) is Cloudflare-gated "
        "from this environment. The <b>offers</b> index and the firm shops were used instead, "
        "cross-checked on 16 August 2026 against Opinatron’s August promo list, PropFirmMap’s "
        "discount-war note, PropFirmDiscountFinder, and each peer’s checkout banner. "
        "Sale prices already in section 7 are these street prices, not list. "
        "Blue Guardian Instant was refreshed to the live BG25 ladder in this revision.",
        s["body"],
    ))
    street_t = [[P(x, s["th"]) for x in ["Firm", "Live code", "Off", "What the shopper actually pays"]]]
    for firm, code, off, note in STREET:
        street_t.append([
            P(firm, s["tdl"]), P(code, s["td"]), P(off, s["td"]), P(note, s["tdl"]),
        ])
    story.append(grid(street_t, [36*mm, 48*mm, 18*mm, 130*mm],
                      verodus_rows={1}))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Industry pattern: 20% is the default first-order cut (HELLO, MATCH20, HOT20, "
        "typical mid-tier). 25–35% is the aggressive band (BG25, VERO35, The5ers 25%, "
        "Goat 40% stacks). FTMO and E8 barely discount. Instant is where the deep cuts "
        "destroy unit economics — FUNDED40, BG25, HELLO on Zero. VERO35 is already in "
        "the aggressive band; the answer is a higher <b>list</b> on Instant $25k+, not "
        "a deeper code. Do not add a second Instant-only discount.",
        s["body"],
    ))

    # ----- 11 failure metrics (prop firm) -----
    story.append(P("11. Failure metrics — for the prop firm, not the trader", s["h1"]))
    story.append(P(
        "Trader blogs count “how do I pass.” This section counts “what dies on our book, "
        "and what that does to contribution.” Same 235k-path library. Weights are the "
        "industry mix. Instant failures are labelled p1_* in the engine because Instant "
        "is modelled as a single funded-from-purchase phase.",
        s["body"],
    ))

    def mix_row(label, mix):
        tot = sum(mix.values()) or 1.0
        def g(name):
            return pct(mix.get(name, 0.0) / tot) if tot else "—"
        return [
            P(label, s["tdl"]),
            P(g("Daily DD"), s["td"]),
            P(g("Max DD"), s["td"]),
            P(g("Time / abandon"), s["td"]),
            P(g("Rule / news"), s["td"]),
            P(g("KYC drop"), s["td"]),
            P(g("Post-payout attrition"), s["td"]),
        ]

    fail_t = [[P(x, s["th"]) for x in [
        "Book (share of ending reasons)", "Daily DD", "Max DD", "Time / abandon",
        "Rule / news", "KYC", "Post-payout",
    ]]]
    fail_t.append(mix_row("Whole 20-firm book", weighted_fail_mix(fails)))
    for prod, lab in (
        ("Verodus Instant", "Verodus Instant"),
        ("BG Instant", "Blue Guardian Instant"),
        ("Verodus 1-Step", "Verodus 1-Step"),
        ("Verodus 2-Step Lite", "Verodus Lite"),
        ("Verodus 2-Step Pro", "Verodus Pro"),
        ("FTMO 2-Step", "FTMO 2-Step (calibration)"),
    ):
        fail_t.append(mix_row(lab, weighted_fail_mix(fails, prod)))
    story.append(grid(fail_t, [48*mm, 22*mm, 22*mm, 28*mm, 24*mm, 18*mm, 28*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "Literature vs this book. Published fail mix (PropFirmGuide / JPTC / Pipcy): "
        "daily 45–55%, max DD 20–30%, consistency/time 10–20%, rules 6–10%. "
        "Our Instant mix is <b>daily-heavy</b> because 45% of the population is Aggressive + "
        "Lottery and Instant’s 3% daily is the first wall they hit — that is the product "
        "working. Eval mixes shift toward max DD (the 6–10% floor) and time/abandon. "
        "Post-payout attrition is the PropScorer month-1/3/12 curve (41% / 28% / 24% of "
        "<b>funded</b>), applied after first payout; it is not a challenge fail.",
        s["body"],
    ))

    # 100-account operator P&L
    story.append(P("11.1 One hundred accounts — operator P&amp;L", s["h2"]))
    story.append(P(
        "For each Verodus plan at $5k and $100k: 100 independent purchases, live sale vs "
        "proposed sale. Contribution = 100 × sale − 100 × E[cost]. Instant has no refund, "
        "so E[cost] = E[X]. This is the number that must stay positive.",
        s["body"],
    ))
    hun = [[P(x, s["th"]) for x in [
        "Plan", "Size", "P(pay)", "Year-1", "Fail before pay",
        "Live sale ×100", "Live payouts", "Live contrib.",
        "Prop. sale ×100", "Prop. contrib.",
    ]]]
    for plan in ("Instant", "1-Step", "2-Step Lite", "2-Step Pro"):
        for sz in (5000, 100000):
            vr = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if vr.empty:
                continue
            r = vr.iloc[0]
            k = 0.0 if r.Refund == "none" else float(r.P_pay)
            ps = proposed_sale(plan, sz, r.Sale, r.px_20)
            live_in = 100 * float(r.Sale)
            live_out = 100 * float(r.E_cost)
            prop_in = 100 * ps
            prop_out = 100 * (float(r.E_payout) + k * ps)
            br = blend[blend.Product == r.Product]
            yr1 = float(br.P_yr1.iloc[0]) if not br.empty else float("nan")
            hun.append([
                P(plan, s["tdl"]),
                P(usd(sz), s["td"]),
                P(pct(r.P_pay), s["td"]),
                P(pct(yr1), s["td"]),
                P(pct(1 - float(r.P_pay)), s["td"]),
                P(usd(live_in), s["td"]),
                P(usd(live_out), s["td"]),
                P(usd(live_in - live_out), s["td"]),
                P(usd(prop_in), s["td"]),
                P(usd(prop_in - prop_out), s["td"]),
            ])
    story.append(grid(hun, [28*mm, 18*mm, 16*mm, 16*mm, 24*mm, 26*mm, 24*mm, 24*mm, 26*mm, 24*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $100k live: 100 × $676 = $67,600 in, $87,525 out, <b>−$19,925</b>. "
        "Proposed: 100 × $1,094 = $109,400 in, $87,525 out, <b>+$21,875</b> (~20%). "
        "That is the whole Instant decision. Evals already contribute at live prices; "
        "the proposed raise is extra, not a rescue. Year-1 Instant ~7 of 100 buyers "
        "matches PropScorer’s 7% funded-year-1 and Track360’s 4–6% sustained Instant. "
        "Axcera’s LTV point stands: the second and third Instant purchases from the same "
        "human are extra fee with a similar E[X] — do not spend that option by underpricing "
        "the first.",
        s["body"],
    ))
    story.append(P(
        "Retries (industry 2–4 attempts, ThePropFirmGuide / JPTC) raise fee LTV and raise "
        "payout LTV only for the subset who eventually pass. We price the single challenge. "
        "A 12% CPA on the proposed Instant $100k is ~$131 — still inside the 20% if "
        "affiliates are held to that. A 25% CPA on Instant $100k eats the whole margin; "
        "cap Instant affiliate at 10–12%.",
        s["body"],
    ))

    # ----- 12 proposed vs each competitor -----
    story.append(P("12. Proposed Verodus vs each competitor (difficulty + unique rules)", s["h1"]))
    story.append(P(
        "Proposed Verodus sale against the peer’s street sale at the same size. "
        "<b>Difficulty</b> is this book: higher P(pay) or higher E[X] = easier / more "
        "expensive to operate. A peer who is easier and cheaper is a hole we do not match. "
        "A peer who is harder and dearer is unused room. Instant rows use proposed Verodus "
        "prices (all positive). Eval rows use the proposed raise.",
        s["body"],
    ))

    def difficulty(peer_p, peer_x, vero_p, vero_x):
        if peer_p > vero_p * 1.20 or peer_x > vero_x * 1.20:
            return "Easier"
        if peer_p < vero_p * 0.80 and peer_x < vero_x * 0.80:
            return "Harder"
        return "Similar"

    def add_vs_table(title, vplan, fam, sizes):
        story.append(P(title, s["h2"]))
        head = [P(x, s["th"]) for x in [
            "Firm / plan", "Unique rules", "Diff.", "Size", "Peer sale", "Peer m",
            "Vero proposed", "Vero m", "Vero / peer",
        ]]
        rows = [head]
        vset = set()
        i = 0
        peers = skus[(skus.Family == fam) & (skus.Size.isin(sizes))].sort_values(
            ["Firm", "Plan", "Size"]
        )
        for r in peers.itertuples():
            if r.Firm == "Verodus" and r.Plan != vplan:
                continue
            vr = skus[(skus.Firm == "Verodus") & (skus.Plan == vplan) & (skus.Size == r.Size)]
            if vr.empty:
                continue
            v = vr.iloc[0]
            ps = proposed_sale(vplan, r.Size, v.Sale, v.px_20)
            vk = 0.0 if v.Refund == "none" else float(v.P_pay)
            vm = sale_margin(ps, float(v.E_payout), vk)
            rules = UNIQUE.get((r.Firm, r.Plan), r.Discount)
            diff = "—" if r.Firm == "Verodus" else difficulty(
                float(r.P_pay), float(r.E_payout), float(v.P_pay), float(v.E_payout)
            )
            i += 1
            if r.Firm == "Verodus":
                vset.add(i)
            rows.append([
                P(f"{r.Firm} {r.Plan}", s["tdl"]),
                P(str(rules), s["tdl"]),
                P(diff, s["td"]),
                P(usd(r.Size), s["td"]),
                P(usd(r.Sale) if r.Firm != "Verodus" else usd(ps), s["td"]),
                P(pct(r.sale_m if r.Firm != "Verodus" else vm, True).replace("-", "−"), s["td"]),
                P(usd(ps), s["td"]),
                P(pct(vm, True).replace("-", "−"), s["td"]),
                P("1.00×" if r.Firm == "Verodus" else f"{ps / r.Sale:.2f}×", s["td"]),
            ])
        story.append(grid(rows, [
            36*mm, 62*mm, 16*mm, 16*mm, 18*mm, 16*mm, 24*mm, 16*mm, 18*mm,
        ], verodus_rows=vset, neg_cols={5, 7}))
        story.append(Spacer(1, 2*mm))

    add_vs_table("12.1 Instant $5k and $100k", "Instant", "instant", [5000, 100000])
    add_vs_table("12.2 One-step $5k and $100k", "1-Step", "1-step", [5000, 100000])
    add_vs_table("12.3 Two-step $5k and $100k (Lite vs cheap peers, Pro vs FTMO-class)",
                 "2-Step Pro", "2-step", [5000, 100000])
    story.append(P(
        "Two-step proposed column is <b>Pro</b> ($36 / $449). Lite proposed is $27 / $349 — "
        "still the cheap 2-step, still above Maven $18 / $279, still under FP Standard $27 / $544. "
        "Do not put Lite on the Pro sticker.",
        s["body"],
    ))
    # Lite vs cheap 2-steps only
    story.append(P("12.4 Lite vs the cheap 2-step street ($5k / $100k)", s["h2"]))
    lite_firms = {
        "Verodus", "Maven", "FundingPips", "Blue Guardian", "FundedNext",
        "BrightFunded", "Ment Funding", "Goat Funded",
    }
    lite_h = [P(x, s["th"]) for x in [
        "Firm / plan", "Size", "Peer sale", "Peer m", "Lite proposed", "Lite m", "Lite / peer",
    ]]
    lite_rows = [lite_h]
    lvset = set()
    li = 0
    sub = skus[(skus.Family == "2-step") & (skus.Size.isin([5000, 100000]))
               & (skus.Firm.isin(lite_firms))].sort_values(["Size", "Firm", "Plan"])
    for r in sub.itertuples():
        vr = skus[(skus.Firm == "Verodus") & (skus.Plan == "2-Step Lite") & (skus.Size == r.Size)]
        if vr.empty:
            continue
        v = vr.iloc[0]
        ps = proposed_sale("2-Step Lite", r.Size, v.Sale, v.px_20)
        vm = sale_margin(ps, float(v.E_payout), float(v.P_pay))
        li += 1
        if r.Firm == "Verodus" and r.Plan == "2-Step Lite":
            lvset.add(li)
        lite_rows.append([
            P(f"{r.Firm} {r.Plan}", s["tdl"]),
            P(usd(r.Size), s["td"]),
            P(usd(r.Sale), s["td"]),
            P(pct(r.sale_m, True).replace("-", "−"), s["td"]),
            P(usd(ps), s["td"]),
            P(pct(vm, True).replace("-", "−"), s["td"]),
            P("1.00×" if r.Firm == "Verodus" and r.Plan == "2-Step Lite"
              else f"{ps / r.Sale:.2f}×", s["td"]),
        ])
    story.append(grid(lite_rows, [50*mm, 20*mm, 22*mm, 18*mm, 28*mm, 18*mm, 22*mm],
                      verodus_rows=lvset, neg_cols={3, 5}))
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "How to use section 12. If Vero/peer &gt; 1.3× and the peer is red, we are priced "
        "to live and they are not — keep the gap. If Vero/peer &lt; 0.7× and we still print "
        "40%+ (1-Step, Pro), raise. If a peer is easier (no daily, trail lock, 10% funded DD) "
        "their cheap sticker is not a comparable. Blue Guardian Instant is the only Instant "
        "that is <b>similar</b> on difficulty and still cheaper — and they are red from $10k. "
        "That is the proof that “similar Instant, cheaper price” is not a strategy.",
        s["body"],
    ))

    # ----- 13 recommendations -----
    story.append(P("13. What to do", s["h1"]))
    rec = [
        [P(x, s["th"]) for x in ["Plan", "Rules", "Live $5k / $100k", "Do this", "Proposed $5k / $100k"]],
        [P("Instant", s["tdl"]), P("Keep live FAQ. No $200k. No trail lock.", s["td"]),
         P("$72 +39% / $676 −29%", s["td"]),
         P("Keep $5k/$10k. Raise $25k to $274. Raise $50k to $547 and $100k to $1,094 so Instant prints. Do not match BG25 $54/$467.", s["td"]),
         P("$72 +39% / $1,094 +20%", s["td"])],
        [P("1-Step", s["tdl"]), P("Keep 6% hybrid + 50% best-day + refund.", s["td"]),
         P("$36 +76% / $335 +59%", s["td"]),
         P("Raise toward Hola, still under FTMO. Unused pricing power.", s["td"]),
         P("$49 / $449", s["td"])],
        [P("Lite", s["tdl"]), P("Funded DD 10% → 8%. Rest live.", s["td"]),
         P("$18 +52% / $241 +33%", s["td"]),
         P("Ship the 8% floor. Raise off Maven $18 toward FP Standard $27.", s["td"]),
         P("$27 / $349", s["td"])],
        [P("Pro", s["tdl"]), P("Keep 10/5 · 5/10.", s["td"]),
         P("$20 +55% / $296 +43%", s["td"]),
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

    story.append(P("14. Sources", s["h1"]))
    story.append(P(
        "Track360 2026 · FPFX / Finance Magnates 300k · FTMO trading-objectives Aug 2026 · "
        "FundedNext Stellar · FundingPips + CryptoSlate 14 Aug 2026 · Alpha FUNDED40 / ALPHA20 · "
        "Hola Prime FXEmpire 27 Jul 2026 (MATCH20) · The5ers, E8, Goat, Maven, FXIFY, Instant Funding, "
        "Fintokei, For Traders, TFT, CTI, Funding Traders, BrightFunded, Ment · "
        "<b>Blue Guardian</b> Instant Standard help (articles 14061082, 10686064) + blueguardian.com shop "
        "16 Aug 2026 (BG25: $54 / $75 / $156 / $243 / $467) · "
        "Prop Firm Match offers index + FX/crypto challenge table (Cloudflare-blocked here; street sales "
        "from firm shops, Opinatron Aug 2026, PropFirmMap, PropFirmDiscountFinder) · "
        "TradersYard “How many people fail” · ThePropFirmGuide statistics · JP Trading Capital failure-rate "
        "statistics · Pipcy most-traders-fail · Velotrade why traders fail · Power Trading Group / Medium "
        "99.72% · Axcera retention · PropScorer 50k-account data analysis · QuantVPS prop-firm statistics · "
        "Verodus FAQ / index-eval.js 16 Aug 2026 (VERO35). "
        "Engine: sim/industry_book.py · catalog: sim/catalog.py · SKUs: results/industry_skus.csv.",
        s["tiny"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus Industry Monte Carlo, Blue Guardian Instant & Proposed Prices — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
