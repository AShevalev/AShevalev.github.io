#!/usr/bin/env python3
"""Verodus vs FundedHive print/BE — same content as the FundedHive card, side by side."""
from __future__ import annotations

import csv
import shutil
from collections import defaultdict
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak,
)

NAVY = HexColor("#0f2744")
GOLD = HexColor("#c9a227")
TEAL = HexColor("#0e5c5c")
GREEN = HexColor("#1b7a4a")
RED = HexColor("#b42318")
ROW_A = HexColor("#ffffff")
ROW_B = HexColor("#eef3f8")
MUTED = HexColor("#5a6a7a")
ORANGE = HexColor("#b45309")
V_HEAD = HexColor("#1a3a5c")
H_HEAD = HexColor("#0e5c5c")

PAGE = landscape(A4)
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")
OUT = RESULTS / "Verodus_vs_FundedHive_2026-08-21.pdf"
OUT_SHOP = RESULTS / "verodus-vs-fundedhive.pdf"

BOOK_W = {"Pro": 0.07, "Semi-skilled": 0.22, "Average": 0.26, "Aggressive": 0.28, "Lottery": 0.17}


def P(text, size=9, color=NAVY, align=TA_LEFT, bold=False, leading=None):
    return Paragraph(
        str(text),
        ParagraphStyle(
            "p",
            fontName="Helvetica-Bold" if bold else "Helvetica",
            fontSize=size,
            textColor=color,
            alignment=align,
            leading=leading or (size + 3),
        ),
    )


def usd(n):
    if n is None or n == "":
        return "—"
    return f"${float(n):,.0f}"


def pct_signed(x):
    return f"{100.0 * float(x):+.0f}%"


def pct_plain(x):
    return f"{100.0 * float(x):.1f}%"


def load_csv(name: str) -> list[dict]:
    with (RESULTS / name).open(newline="") as f:
        return list(csv.DictReader(f))


def grid(data, col_w, header=True, font=7.5, header_bg=NAVY, spans=None):
    style = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold" if header else "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font),
        ("TEXTCOLOR", (0, 0), (-1, 0), white if header else NAVY),
        ("BACKGROUND", (0, 0), (-1, 0), header_bg if header else ROW_A),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#c5d0dc")),
    ]
    start = 1 if header else 0
    for i in range(start, len(data)):
        style.append(("BACKGROUND", (0, i), (-1, i), ROW_A if i % 2 else ROW_B))
        style.append(("FONTNAME", (0, i), (-1, i), "Helvetica"))
        style.append(("TEXTCOLOR", (0, i), (-1, i), NAVY))
    if spans:
        for a, b in spans:
            style.append(("SPAN", a, b))
            style.append(("BACKGROUND", a, b, header_bg))
            style.append(("TEXTCOLOR", a, b, white))
            style.append(("FONTNAME", a, b, "Helvetica-Bold"))
            style.append(("ALIGN", a, b, "CENTER"))
    t = Table(data, colWidths=col_w, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style))
    return t


def color_print(yes: bool):
    if yes:
        return P("yes", 7.5, GREEN, TA_CENTER, True)
    return P("NO", 7.5, RED, TA_CENTER, True)


def section(title):
    return KeepTogether([
        Spacer(1, 2 * mm),
        P(title, 11, NAVY, bold=True, leading=14),
        Spacer(1, 1.2 * mm),
    ])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE[0], 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        14 * mm, 4.2 * mm,
        "Verodus vs FundedHive  ·  same CFD book 7/22/26/28/17  ·  VERO35 vs WELCOME25  ·  21 Aug 2026",
    )
    canvas.drawRightString(PAGE[0] - 14 * mm, 4.2 * mm, f"p. {doc.page}")
    canvas.restoreState()


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE[1] - 28 * mm, PAGE[0], 28 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE[1] - 28.8 * mm, PAGE[0], 1.6 * mm, fill=1, stroke=0)
    canvas.restoreState()
    footer(canvas, doc)


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE[1] - 16 * mm, PAGE[0], 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE[1] - 16.8 * mm, PAGE[0], 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(14 * mm, PAGE[1] - 10.5 * mm, "Verodus vs FundedHive  ·  print and breakeven")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        PAGE[0] - 14 * mm, PAGE[1] - 10.5 * mm, "VERO35 35%  ·  WELCOME25 25%  ·  news included",
    )
    canvas.restoreState()
    footer(canvas, doc)


def by_key(rows, *keys):
    out = {}
    for r in rows:
        out[tuple(r[k] if k in r else r.get(k) for k in keys)] = r
    return out


def fnum(r, *names):
    for n in names:
        if n in r and r[n] not in (None, ""):
            return float(r[n])
    raise KeyError(names)


def weighted_fails(path: Path, product: str, news: str | None = "true") -> list[tuple[str, float]]:
    by = defaultdict(float)
    with path.open(newline="") as f:
        for r in csv.DictReader(f):
            if r.get("Product") != product:
                continue
            if news is not None and r.get("News", "true").lower() != news:
                continue
            w = BOOK_W.get(r["Profile"])
            if w is None:
                continue
            by[r["Reason"]] += w * float(r["Share"])
    return sorted(by.items(), key=lambda x: -x[1])[:6]


def fh_sku_map(rows):
    out = {}
    for r in rows:
        out[(r["Plan"], int(float(r["Size"])))] = r
    return out


def build(path: Path | None = None) -> Path:
    path = Path(path) if path else OUT
    v_px = [r for r in load_csv("verodus_be_20_40_60_margins.csv") if r["Kind"] == "challenge"]
    v_blend = load_csv("verodus_news_included_blended.csv")
    fh_skus = load_csv("fundedhive_skus.csv")
    fh_blend = load_csv("fundedhive_blended.csv")
    pfp1 = load_csv("fundedhive_pfp1_funnel.csv")
    pfp2 = load_csv("fundedhive_pfp2_funnel.csv")
    v_by = {(r["Plan"], int(float(r["Size"]))): r for r in v_px}
    fh_by = fh_sku_map(fh_skus)
    v_b = {r["Plan"]: r for r in v_blend}
    fh_b = {r["Plan"]: r for r in fh_blend}
    pfp1_by = {int(float(r["Size"])): r for r in pfp1}
    pfp2_by = {int(float(r["Size"])): r for r in pfp2}

    v_inst_first_100k = fnum(v_b["Instant"], "E_payout_100k")
    fh_classic = fh_b["Classic 2-Step (NewBee)"]
    fh_pfp2 = fh_b["Pay From Profits 2-Step"]
    fh_pfp1 = fh_b["Pay From Profits 1-Step"]
    fh_inst = fh_b["Instant Growth L1"]

    story = []
    usable = PAGE[0] - 28 * mm

    story.append(Spacer(1, 12 * mm))
    story.append(KeepTogether([
        Table(
            [[P("Verodus vs FundedHive — print and breakeven", 16, white, TA_LEFT, True, 20)],
             [P(
                 "Same CFD book 7/22/26/28/17  ·  Verodus locked rec + news-included  ·  FundedHive TOS Jan 2026 + WELCOME25  ·  21 Aug 2026",
                 8.5, HexColor("#d4c4a8"), TA_LEFT, False, 12,
             )]],
            colWidths=[usable],
        )
    ]))
    story.append(Spacer(1, 7 * mm))

    story.append(P(
        "Verdict. On the shopper door Verodus is cheaper on Instant and 1-Step; FundedHive Classic is cheaper than Verodus Pro and close to Lite. "
        "On operator leftover, FundedHive Classic $100k keeps <b>$173</b> vs Verodus Lite <b>$145</b> / Pro <b>$168</b>. "
        "FundedHive Instant $10k @ $299 keeps <b>$261</b> on first payout (m +87%); Verodus Instant $10k @ $69 keeps <b>$41</b> on the year-1 card (m +60%). "
        "PFP 2-Step access is a hole from $100k until the 1–3% funded fee — Verodus has no PFP analog (fee is up front). "
        "Hive Coin is not cash (k = 0). Verodus evals refund the challenge fee on first reward (k = P(pay)). Instant is not refundable on either firm.",
        9, NAVY, leading=12.5,
    ))

    story.append(section("Product map"))
    story.append(grid(
        [
            ["Family", "Verodus (VERO35)", "FundedHive (WELCOME25)", "What to compare"],
            ["Instant", "Instant $5k–$100k, no $200k", "Instant Growth L1 $10k only", "$10k door + first-payout vs year-1 leftover"],
            ["1-Step", "1-Step $5k–$200k, fee up front, first-reward refund", "PFP 1-Step access + 1–3% funded fee", "Sticker vs full funnel"],
            ["2-Step", "Lite 8/5 · 4/8  and  Pro 10/5 · 5/10", "Classic NewBee 8/6 · 5/10, 70% split", "Lite/Pro vs Classic leftover"],
            ["2-Step cheap door", "None — challenge fee up front", "PFP 2-Step access + funded fee", "PFP is a different unit; funnel leftover is the P&L"],
        ],
        [32 * mm, 72 * mm, 72 * mm, usable - 176 * mm],
        font=8,
    ))

    story.append(section("$100k leftover scoreboard  ·  operator $ per starter"))
    v100_lite = v_by[("2-Step Lite", 100000)]
    v100_pro = v_by[("2-Step Pro", 100000)]
    v100_1s = v_by[("1-Step", 100000)]
    v100_in = v_by[("Instant", 100000)]
    fh100_c = fh_by[("Classic 2-Step (NewBee)", 100000)]
    fh100_p2 = fh_by[("Pay From Profits 2-Step", 100000)]
    fh100_p1 = fh_by[("Pay From Profits 1-Step", 100000)]
    story.append(grid(
        [
            ["Match", "Verodus sale", "Verodus leftover", "m", "FundedHive sale", "FH leftover", "m", "Fatter leftover"],
            ["Instant $100k (V year-1)", usd(v100_in["Sale"]), usd(float(v100_in["Sale"]) - float(v100_in["E"])),
             pct_signed(v100_in["Sale_m"]), "— (no $100k Instant)", "—", "—",
             P("Verodus only", 7.5, V_HEAD, TA_CENTER, True)],
            ["1-Step vs PFP 1-Step sticker", usd(v100_1s["Sale"]), usd(float(v100_1s["Sale"]) - float(v100_1s["Cost"])),
             pct_signed(v100_1s["Sale_m"]), usd(fh100_p1["Sale"]),
             usd(float(fh100_p1["Sale"]) - float(fh100_p1["E_payout"])),
             pct_signed(fh100_p1["sale_m"]),
             P("Verodus sticker", 7.5, GREEN, TA_CENTER, True)],
            ["1-Step vs PFP 1-Step funnel", usd(v100_1s["Sale"]), usd(float(v100_1s["Sale"]) - float(v100_1s["Cost"])),
             pct_signed(v100_1s["Sale_m"]),
             usd(pfp1_by[100000]["E_revenue"]), usd(pfp1_by[100000]["Leftover"]),
             pct_signed(pfp1_by[100000]["m"]),
             P("FH funnel", 7.5, TEAL, TA_CENTER, True)],
            ["Lite vs Classic", usd(v100_lite["Sale"]), usd(float(v100_lite["Sale"]) - float(v100_lite["Cost"])),
             pct_signed(v100_lite["Sale_m"]), usd(fh100_c["Sale"]),
             usd(float(fh100_c["Sale"]) - float(fh100_c["E_payout"])),
             pct_signed(fh100_c["sale_m"]),
             P("FH Classic", 7.5, TEAL, TA_CENTER, True)],
            ["Pro vs Classic", usd(v100_pro["Sale"]), usd(float(v100_pro["Sale"]) - float(v100_pro["Cost"])),
             pct_signed(v100_pro["Sale_m"]), usd(fh100_c["Sale"]),
             usd(float(fh100_c["Sale"]) - float(fh100_c["E_payout"])),
             pct_signed(fh100_c["sale_m"]),
             P("about even", 7.5, ORANGE, TA_CENTER, True)],
            ["PFP 2-Step funnel (no V analog)", "—", "—", "—",
             usd(pfp2_by[100000]["E_revenue"]), usd(pfp2_by[100000]["Leftover"]),
             pct_signed(pfp2_by[100000]["m"]),
             P("FH only", 7.5, TEAL, TA_CENTER, True)],
        ],
        [48 * mm] + [(usable - 48 * mm) / 7] * 7,
        font=7.5,
    ))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Verodus leftover on evals = sale − E[X] − P(pay)×sale (first-fee refund). Instant leftover on the operator card = sale − year-1 E[X] (no refund). "
        "FundedHive leftover = sale − first-payout E[X] (Hive Coin k = 0). PFP funnel leftover = E[access + funded fee] − E[X].",
        8, MUTED, leading=11,
    ))

    story.append(PageBreak())
    story.append(Spacer(1, 6 * mm))
    story.append(section("How each firm is built  ·  Instant"))
    story.append(grid(
        [
            ["Rule", "Verodus Instant", "FundedHive Instant Growth L1"],
            ["Door", "$5k–$100k. Rec $49–$439 VERO35. No $200k.", "$10k only. On-chain $299. WELCOME25 not on this print."],
            ["Daily DD", "3% from that day’s equity high (intraday).", "None."],
            ["Max DD", "6% trailing HWM. Never locks.", "6% static vs initial."],
            ["Best Day / consistency", "20% of Positive Days’ Profit at payout request. Every profitable day counts. No min days.", "None."],
            ["Max / trade", "None.", "2% of initial."],
            ["Split / refund", "80% default. Instant not refundable.", "80%. Hive Coin 200% coupon, not cash. k = 0."],
            ["Scale / residual", "After first payout. First-payout E[X] overstates year-1.", "Double at +6% to $1M. L1 B-book one cash-out; L2+ A-book. Residual = tower."],
            ["News / weekend", "News included. Weekend is a paid add-on (15% of list).", "News allowed. Weekend eval yes, funded no."],
            ["What prints?", "$10k sale $69 vs year-1 E[X] $28, leftover $41, m +60%. First-payout E[X] $82 — sticker does not cover the first check.", "$10k sale $299 vs first-payout E[X] $38, leftover $261, m +87%."],
        ],
        [38 * mm, (usable - 38 * mm) / 2, (usable - 38 * mm) / 2],
        font=7.5,
    ))

    story.append(section("1-Step"))
    story.append(grid(
        [
            ["Rule", "Verodus 1-Step", "FundedHive PFP 1-Step"],
            ["Door", "Challenge fee up front. $45–$699 VERO35.", "Access fee once ($14–$299 WELCOME25). Funded fee 1–3% of size at pass."],
            ["Target / DD", "10%. Daily 4% SOD. Max 6% hybrid, locks at initial.", "10%. Daily 5% EOD. Max 10% static. 3% max/trade. 3 days ≥1%."],
            ["Best Day", "50% to pass and to get paid. Do not put Instant 20% here.", "None."],
            ["Refund / split", "100% of challenge fee on first successful reward. 80%.", "No cash refund. 80% A-book. Hive Coin coupon."],
            ["What prints?", "Every size. $100k sale $379 vs E[X] $151, leftover after refund $197, m +52%.", "Access prints (even $200k +6%). Funnel leftover ~$256 at $100k."],
        ],
        [38 * mm, (usable - 38 * mm) / 2, (usable - 38 * mm) / 2],
        font=7.5,
    ))

    story.append(section("2-Step"))
    story.append(grid(
        [
            ["Rule", "Verodus Lite", "Verodus Pro", "FH Classic NewBee", "FH PFP 2-Step"],
            ["Targets", "8% then 5%", "10% then 5%", "8% then 6%", "Same 8/6 as Classic"],
            ["Daily / max", "4% / 8% static (funded 8%)", "5% / 10% static", "5% EOD / 10% static", "Same 5/10"],
            ["Extra gates", "5 min days / phase; QPP 3", "5 min days / phase; QPP 3", "3 days ≥1%; 3% max/trade", "Same + access per phase"],
            ["Split", "80%", "80%", "NewBee 70% (Worker 80 / Queen 90)", "80% A-book"],
            ["Refund", "First-reward fee refund", "First-reward fee refund", "None (Hive Coin coupon)", "None; funded fee 1–3% of size"],
            ["$100k leftover", "$145, m +47%", "$168, m +48%", "$173, m +66%", "Access −$17; funnel +$135, m +60%"],
        ],
        [32 * mm] + [(usable - 32 * mm) / 4] * 4,
        font=7.5,
    ))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Shared Verodus: $100 min every cycle. Default Bi-Weekly 80%. Weekly 6% and On Demand 90% (32% Instant / 15% evals) cannot stack. Weekend 15% is a separate paid add-on. "
        "FundedHive payouts USDC &lt;60s. A-book clawback (split only on A-book PnL) is not in E[X] — FH leftover is a floor.",
        8, MUTED, leading=11,
    ))

    story.append(section("Blended funnel  ·  first-payout E[X] per buyer at $100k scale"))

    def blend_row(firm, plan, r, split, refund, e100=None):
        e = e100 if e100 is not None else fnum(r, "E_payout_100k")
        p1 = fnum(r, "Phase1")
        ev = fnum(r, "Funded") if "Funded" in r else fnum(r, "EvalPass")
        return [
            firm, plan, pct_plain(p1), pct_plain(r["P_pay"]), pct_plain(r["P_yr1"]),
            usd(e), f"{float(r['Avg_days']):.0f}", split, refund,
        ]

    blend_data = [
        ["Firm", "Plan", "P1 / start", "P(pay)", "P(yr1)", "E[X] $100k", "Days", "Split", "Refund k"],
        blend_row("Verodus", "Instant", v_b["Instant"], "80%", "none", v_inst_first_100k),
        blend_row("FundedHive", "Instant L1", fh_inst, "80%", "none"),
        blend_row("Verodus", "1-Step", v_b["1-Step"], "80%", "first = P(pay)"),
        blend_row("FundedHive", "PFP 1-Step", fh_pfp1, "80%", "none"),
        blend_row("Verodus", "2-Step Lite", v_b["2-Step Lite"], "80%", "first = P(pay)"),
        blend_row("Verodus", "2-Step Pro", v_b["2-Step Pro"], "80%", "first = P(pay)"),
        blend_row("FundedHive", "Classic 2-Step", fh_classic, "70%", "none"),
        blend_row("FundedHive", "PFP 2-Step", fh_pfp2, "80%", "none"),
    ]
    story.append(grid(blend_data, [28 * mm, 36 * mm] + [(usable - 64 * mm) / 7] * 7, font=8))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Instant E[X] $100k here is first-payout scaled (Verodus $825, FH $377). Verodus Instant year-1 E[X] at $100k is $278 — that is the operator BE. "
        "FH Instant live SKU is $10k only; $377 is the $10k path × 10. 20/40/60 = BE / (1 − m).",
        8, MUTED, leading=11,
    ))

    story.append(section("Instant sticker  ·  Verodus year-1 leftover vs FH first-payout leftover"))
    story.append(P(
        "Verodus Instant Prints? uses year-1 E[X] (operator card). First-payout E[X] is shown so it matches the FundedHive card. "
        "FH Instant is $10k only.",
        8, MUTED, leading=11,
    ))
    story.append(Spacer(1, 1 * mm))
    inst_head = ["Size", "V list", "V sale", "V E yr1", "V left", "V m", "V prints",
                 "V E 1st", "FH sale", "FH E 1st", "FH left", "FH m", "FH prints"]
    inst_data = [inst_head]
    for sz in (5000, 10000, 25000, 50000, 100000):
        v = v_by[("Instant", sz)]
        e_yr1 = float(v["E"])
        e_1st = v_inst_first_100k * (sz / 100000.0)
        sale = float(v["Sale"])
        fh = fh_by.get(("Instant Growth L1", sz))
        if fh:
            fh_e = float(fh["E_payout"])
            fh_s = float(fh["Sale"])
            fh_row = [usd(fh_s), usd(fh_e), usd(fh_s - fh_e), pct_signed(fh["sale_m"]),
                      color_print(fh["prints"].lower() == "true")]
        else:
            fh_row = ["—", "—", "—", "—", "—"]
        inst_data.append([
            usd(sz), usd(v["List"]), usd(sale), usd(e_yr1), usd(sale - e_yr1),
            pct_signed(v["Sale_m"]), color_print(float(v["Sale_m"]) >= 0),
            usd(e_1st), *fh_row,
        ])
    w0 = 22 * mm
    rest = (usable - w0) / 12
    story.append(grid(inst_data, [w0] + [rest] * 12, font=6.5))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Read the Instant $10k line: Verodus door $69 vs FH $299. Operator leftover $41 vs $261. "
        "Verodus first-payout E[X] $82 is above the $69 sale — the 3% daily and 20% Best Day cut P(pay) to 21% (FH 46%) but the first check is larger. "
        "Year-1 is the right Verodus Instant BE because Instant is funded on day 1.",
        8, MUTED, leading=11,
    ))

    story.append(section("1-Step sticker vs PFP 1-Step  ·  leftover after each firm’s true cost"))
    s1_head = ["Size", "V sale", "V E[X]", "V leftover", "V m", "V prints",
               "FH access", "FH E[X]", "FH stick left", "FH stick m", "FH funnel in", "FH funnel left", "FH funnel m"]
    s1_data = [s1_head]
    for sz in (5000, 10000, 25000, 50000, 100000, 200000):
        v = v_by[("1-Step", sz)]
        fh = fh_by[("Pay From Profits 1-Step", sz)]
        fun = pfp1_by[sz]
        vs, ve, vc = float(v["Sale"]), float(v["E"]), float(v["Cost"])
        fs, fe = float(fh["Sale"]), float(fh["E_payout"])
        s1_data.append([
            usd(sz), usd(vs), usd(ve), usd(vs - vc), pct_signed(v["Sale_m"]),
            color_print(float(v["Sale_m"]) >= 0),
            usd(fs), usd(fe), usd(fs - fe), pct_signed(fh["sale_m"]),
            usd(fun["E_revenue"]), usd(fun["Leftover"]), pct_signed(fun["m"]),
        ])
    story.append(grid(s1_data, [20 * mm] + [(usable - 20 * mm) / 12] * 12, font=6.5))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "PFP access is not supposed to cover E[X] alone. At $100k Verodus leftover $197 vs PFP sticker $46 vs PFP funnel $256. "
        "The funded fee is the PFP print engine. Verodus has no 1–3% of notional after pass.",
        8, MUTED, leading=11,
    ))

    story.append(PageBreak())
    story.append(Spacer(1, 6 * mm))
    story.append(section("2-Step sticker  ·  Lite / Pro vs Classic  ·  PFP 2-Step access vs funnel"))
    s2_head = ["Size", "Lite sale", "Lite left", "Lite m", "Pro sale", "Pro left", "Pro m",
               "Classic sale", "Classic left", "Classic m", "PFP2 access", "PFP2 stick", "PFP2 funnel"]
    s2_data = [s2_head]
    for sz in (5000, 10000, 25000, 50000, 100000, 200000):
        lite = v_by[("2-Step Lite", sz)]
        pro = v_by[("2-Step Pro", sz)]
        cl = fh_by[("Classic 2-Step (NewBee)", sz)]
        p2s = fh_by[("Pay From Profits 2-Step", sz)]
        fun = pfp2_by[sz]
        s2_data.append([
            usd(sz),
            usd(lite["Sale"]), usd(float(lite["Sale"]) - float(lite["Cost"])), pct_signed(lite["Sale_m"]),
            usd(pro["Sale"]), usd(float(pro["Sale"]) - float(pro["Cost"])), pct_signed(pro["Sale_m"]),
            usd(cl["Sale"]), usd(float(cl["Sale"]) - float(cl["E_payout"])), pct_signed(cl["sale_m"]),
            usd(p2s["Sale"]),
            P("NO" if p2s["prints"].lower() != "true" else "yes", 7,
              RED if p2s["prints"].lower() != "true" else GREEN, TA_CENTER, True),
            usd(fun["Leftover"]),
        ])
    story.append(grid(s2_data, [20 * mm] + [(usable - 20 * mm) / 12] * 12, font=6.5))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Classic prints on every size at WELCOME25. PFP 2-Step $100k and $200k access stickers are the only FundedHive NO — until the funded fee. "
        "Verodus Lite/Pro leftover already includes the first-fee refund; Classic does not refund cash.",
        8, MUTED, leading=11,
    ))

    story.append(section("PFP full funnel  ·  no Verodus analog  ·  access + funded fee − E[X]"))
    story.append(P(
        "Risk map: Pro+Semi → Low 1% of size, 100% from profits. Average → Moderate 2%, 100% from profits. "
        "Aggressive → Medium 2.5%, 50% upfront. Lottery → High 3%, 50% upfront.",
        8, MUTED, leading=11,
    ))
    story.append(Spacer(1, 1 * mm))
    funnel_head = ["Size", "PFP2 access", "PFP2 E[fee]", "PFP2 in", "PFP2 E[X]", "PFP2 left", "m",
                   "PFP1 access", "PFP1 E[fee]", "PFP1 in", "PFP1 E[X]", "PFP1 left", "m"]
    funnel_data = [funnel_head]
    for sz in (5000, 10000, 25000, 50000, 100000, 200000):
        a, b = pfp2_by[sz], pfp1_by[sz]
        funnel_data.append([
            usd(sz),
            usd(a["Access_sale"]), usd(a["E_funded_fee"]), usd(a["E_revenue"]), usd(a["E_payout"]),
            usd(a["Leftover"]), pct_signed(a["m"]),
            usd(b["Access_sale"]), usd(b["E_funded_fee"]), usd(b["E_revenue"]), usd(b["E_payout"]),
            usd(b["Leftover"]), pct_signed(b["m"]),
        ])
    story.append(grid(funnel_data, [20 * mm] + [(usable - 20 * mm) / 12] * 12, font=6.5))

    def floors(label, sale, be, m):
        return [label, usd(sale), usd(be), usd(float(be) / 0.8), usd(float(be) / 0.6), usd(float(be) / 0.4), m]
    fl = [
        ["Plan", "Sale", "BE", "20%", "40%", "60%", "Sale m"],
        floors("Verodus Instant (year-1 BE)", v100_in["Sale"], v100_in["BE"], pct_signed(v100_in["Sale_m"])),
        floors("Verodus 1-Step", v100_1s["Sale"], v100_1s["BE"], pct_signed(v100_1s["Sale_m"])),
        floors("Verodus Lite", v100_lite["Sale"], v100_lite["BE"], pct_signed(v100_lite["Sale_m"])),
        floors("Verodus Pro", v100_pro["Sale"], v100_pro["BE"], pct_signed(v100_pro["Sale_m"])),
        floors("FH Classic", fh100_c["Sale"], fh100_c["BE"], pct_signed(fh100_c["sale_m"])),
        floors("FH PFP 2-Step access", fh100_p2["Sale"], fh100_p2["BE"], pct_signed(fh100_p2["sale_m"])),
        floors("FH PFP 1-Step access", fh100_p1["Sale"], fh100_p1["BE"], pct_signed(fh100_p1["sale_m"])),
        floors("FH Instant $10k (not $100k)", fh_by[("Instant Growth L1", 10000)]["Sale"],
               fh_by[("Instant Growth L1", 10000)]["BE"],
               pct_signed(fh_by[("Instant Growth L1", 10000)]["sale_m"])),
    ]
    story.append(KeepTogether([
        section("BE / 20% / 40% / 60% at $100k  ·  charge-this floors"),
        grid(fl, [58 * mm] + [(usable - 58 * mm) / 6] * 6, font=8),
        Spacer(1, 1.2 * mm),
        P(
            "PFP 2-Step $100k sale $74 sits below BE $91 — that is the access hole. Instant $10k FH sale $299 is well above its $38 BE. "
            "Verodus Instant $100k sale $439 is above year-1 BE $278 and below the 60% floor $695.",
            8, MUTED, leading=11,
        ),
    ]))

    story.append(section("How to read this"))
    bullets = [
        "<b>Side-by-side only these two firms.</b> Same industry book. Verodus prices are the locked VERO35 rec card. FundedHive Classic list is TheTrustedProp; Instant $299 is on-chain Jun 2026.",
        "<b>Prints?</b> leftover ≥ −$1 after that firm’s true cost. Verodus evals include the first-fee refund. Verodus Instant uses year-1 E[X]. FundedHive uses first-payout E[X], k = 0.",
        "<b>BE = E[X] / (1 − k).</b> Hive Coin is a coupon (k = 0). Verodus Instant k = 0. Verodus evals k = P(pay). 20/40/60 = BE / (1 − m).",
        "<b>Instant Best Day</b> on Verodus is 20% of Positive Days’ Profit at payout request. No min days. 1-Step Best Day stays 50% to pass and to get paid.",
        "<b>Instant $10k @ $299</b> (FH) is B-book L1, one cash-out, 6% static, no daily, 2% max/trade. Residual risk is the doubling tower. Verodus Instant residual is year-1 survival after the 3% daily / 6% trail / 20% Best Day.",
        "<b>A-book clawback</b> on FundedHive is not in E[X]. Leftover there is a floor. Verodus has no published A/B switch.",
        "<b>News is included</b> on every Verodus phase and funded account, and allowed on FundedHive. Weekend holding is a Verodus paid add-on; FH eval yes / funded no.",
    ]
    for b in bullets:
        story.append(P("•  " + b, 8, NAVY, leading=11))
        story.append(Spacer(1, 0.45 * mm))

    v_fail_i = weighted_fails(RESULTS / "verodus_news_included_failures.csv", "Verodus Instant")
    v_fail_1 = weighted_fails(RESULTS / "verodus_news_included_failures.csv", "Verodus 1-Step")
    v_fail_l = weighted_fails(RESULTS / "verodus_news_included_failures.csv", "Verodus 2-Step Lite")
    v_fail_p = weighted_fails(RESULTS / "verodus_news_included_failures.csv", "Verodus 2-Step Pro")

    def fail_cell(items, *keys):
        d = dict(items)
        parts = []
        for k in keys:
            if k in d:
                parts.append(f"{k.replace('p1_', '').replace('p2_', 'p2 ')} {100*d[k]:.0f}%")
        return " · ".join(parts) if parts else "—"

    fail = [
        ["Product", "Main kill", "Second", "Rest"],
        ["Verodus Instant", "daily DD 43%", "max DD 29%", fail_cell(v_fail_i, "post_m1", "p1_time_abandon", "post_m3")],
        ["FH Instant L1", "max/trade 45%", "post M1 19%", "max DD 8% · post M3 7%"],
        ["Verodus 1-Step", "max DD 57%", "daily DD 20%", fail_cell(v_fail_1, "p1_time_abandon", "post_m1", "funded_kyc_drop")],
        ["FH PFP 1-Step", "max/trade 41%", "max DD 26%", "abandon 7% · daily 4% · KYC 3%"],
        ["Verodus Lite", "daily DD 39%", "max DD 30%", fail_cell(v_fail_l, "p2_max_dd", "p1_time_abandon", "post_m1")],
        ["Verodus Pro", "daily DD 43%", "max DD 28%", fail_cell(v_fail_p, "p1_time_abandon", "post_m1", "p2_max_dd")],
        ["FH Classic / PFP 2", "max/trade ~40%", "max DD ~24%", "p2 max DD ~7% · abandon ~5%"],
    ]
    story.append(section("Failure mix  ·  share of all buyers  ·  top reasons"))
    story.append(grid(fail, [40 * mm, 40 * mm, 36 * mm, usable - 116 * mm], font=7.5))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "Verodus Instant/Lite/Pro print engine is the daily DD (3/4/5%). FundedHive print engine is the 3% (evals) / 2% (Instant) max-per-trade cap. "
        "That is why FH Lottery almost never pays and Classic leftover is fat at a cheaper door.",
        8, MUTED, leading=11,
    ))

    story.append(section("Caveats"))
    caveats = [
        "FundedHive Classic list is from TheTrustedProp, not a scraped checkout (Cloudflare blocked later live fetches). Re-check stickers on fundedhive.com before using leftover $ as live P&amp;L.",
        "Verodus numbers are the locked rec card + news-included aligned book. WorkerBee / QueenBee are not priced separately; NewBee 70% is the Classic default.",
        "PFP funded-fee mix uses this book’s 7/22/26/28/17, not FundedHive’s unpublished Low/Mod/Med/High mix. E[X] is first cash-out except the Verodus Instant year-1 column.",
        "$100 minimum reward is assumed on both. Instant on FH may need the 6% scale target before a full withdrawal. Do not change performance-reward.html. 1-Step Best Day stays 50%. Instant Best Day stays 20% at payout request.",
    ]
    for c in caveats:
        story.append(P("•  " + c, 8, NAVY, leading=11))
        story.append(Spacer(1, 0.4 * mm))
    story.append(section("Sources"))
    story.append(P(
        "Verodus: locked rec card, news-included CSVs. FundedHive: TOS Jan 2026, on-chain Instant Jun 2026, TheTrustedProp Classic, WELCOME25, results/FUNDEDHIVE.md + fundedhive_*.csv. "
        "Same engine as the industry catalog. Not investment advice.",
        8, MUTED, leading=11,
    ))

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=PAGE,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=20 * mm,
        bottomMargin=16 * mm,
        title="Verodus vs FundedHive print and breakeven",
        author="Verodus research",
    )
    doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
    return path


def copy_outputs(src: Path) -> None:
    shutil.copy2(src, OUT_SHOP)
    if ART.is_dir():
        shutil.copy2(src, ART / src.name)
        shutil.copy2(OUT_SHOP, ART / OUT_SHOP.name)
        print(f"copied to {ART}")


def main():
    out = build(OUT)
    copy_outputs(out)
    print(out)
    print(OUT_SHOP)


if __name__ == "__main__":
    main()
