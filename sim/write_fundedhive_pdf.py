#!/usr/bin/env python3
"""FundedHive print + BE report as a downloadable landscape PDF."""
from __future__ import annotations

import csv
import shutil
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
GREEN = HexColor("#1b7a4a")
RED = HexColor("#b42318")
ROW_A = HexColor("#ffffff")
ROW_B = HexColor("#eef3f8")
MUTED = HexColor("#5a6a7a")
ORANGE = HexColor("#b45309")

PAGE = landscape(A4)
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")
OUT = RESULTS / "FundedHive_Print_BE_2026-08-21.pdf"
OUT_SHOP = RESULTS / "fundedhive-print-be.pdf"


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
    return f"${float(n):,.0f}"


def pct_signed(x):
    return f"{100.0 * float(x):+.0f}%"


def pct_plain(x):
    return f"{100.0 * float(x):.1f}%"


def load_csv(name: str) -> list[dict]:
    with (RESULTS / name).open(newline="") as f:
        return list(csv.DictReader(f))


def grid(data, col_w, header=True, font=7.5):
    style = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold" if header else "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font),
        ("TEXTCOLOR", (0, 0), (-1, 0), white if header else NAVY),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY if header else ROW_A),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#c5d0dc")),
    ]
    for i in range(1, len(data)):
        style.append(("BACKGROUND", (0, i), (-1, i), ROW_A if i % 2 else ROW_B))
        style.append(("FONTNAME", (0, i), (-1, i), "Helvetica"))
        style.append(("TEXTCOLOR", (0, i), (-1, i), NAVY))
    t = Table(data, colWidths=col_w, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE[0], 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        14 * mm, 4.2 * mm,
        "FundedHive print + BE  ·  TOS Jan 2026  ·  CFD book 7/22/26/28/17  ·  700 sims × 5 profiles",
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
    canvas.drawString(14 * mm, PAGE[1] - 10.5 * mm, "FundedHive  ·  print and breakeven")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        PAGE[0] - 14 * mm, PAGE[1] - 10.5 * mm, "WELCOME25  ·  Hive Coin is not cash",
    )
    canvas.restoreState()
    footer(canvas, doc)


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


def sku_short(plan: str, size: float) -> str:
    size_s = usd(size)
    if plan.startswith("Classic"):
        return f"Classic {size_s}"
    if "2-Step" in plan:
        return f"PFP 2-Step {size_s}"
    if "1-Step" in plan:
        return f"PFP 1-Step {size_s}"
    return f"Instant {size_s}"


def build(path: Path | None = None) -> Path:
    path = Path(path) if path else OUT
    skus = load_csv("fundedhive_skus.csv")
    blended = load_csv("fundedhive_blended.csv")
    pfp2 = load_csv("fundedhive_pfp2_funnel.csv")
    pfp1 = load_csv("fundedhive_pfp1_funnel.csv")

    story = []
    usable = PAGE[0] - 28 * mm

    story.append(Spacer(1, 12 * mm))
    story.append(KeepTogether([
        Table(
            [[P("FundedHive — does it print, and what is BE?", 16, white, TA_LEFT, True, 20)],
             [P(
                 "fundedhive.com  ·  TOS 1 Jan 2026  ·  sale WELCOME25 = 25% off new-trader access  ·  21 Aug 2026",
                 8.5, HexColor("#d4c4a8"), TA_LEFT, False, 12,
             )]],
            colWidths=[usable],
        )
    ]))
    story.append(Spacer(1, 8 * mm))

    story.append(P(
        "Verdict. Classic 2-Step prints on every size at WELCOME25. Instant Growth $10k @ $299 prints fat on the first cash-out "
        "(m +87%) — residual risk is the doubling tower, not L1. PFP 2-Step access is the hole from $100k (−23% vs first-payout E[X]), "
        "but the funded-account fee (1–3% of size, paid at pass) puts the full funnel back in the black (~+60% leftover at $100k). "
        "Hive Coin is a coupon, not cash, so it is not in E[X] and not in BE. News is allowed. CFD book. "
        "A-book clawback is not in E[X] — leftover is a floor for the firm.",
        9, NAVY, leading=13,
    ))

    story.append(section("How the firm is built"))
    story.append(grid(
        [
            [P("Plan", 7.5, white, bold=True), P("Phases / DD", 7.5, white, TA_CENTER, True),
             P("Funded split / extra", 7.5, white, TA_CENTER, True), P("What prints?", 7.5, white, TA_CENTER, True)],
            [P("<b>Classic 2-Step</b>", 8, NAVY),
             P("8% then 6%. 5% EOD daily (NewBee) / 10% static. 3% max/trade. 3 days ≥1% of initial. No consistency. Weekend eval yes, funded no.", 7.5, NAVY, leading=10),
             P("NewBee 70% · WorkerBee 80% 4% daily · QueenBee 90% 3% daily. Hive Coin 200% of fee on pass, max 50% of next price (coupon, not cash).", 7.5, NAVY, leading=10),
             P("Every size at WELCOME25. $100k sale $262 vs E[X] $89, leftover $173, m +66%.", 7.5, GREEN, leading=10)],
            [P("<b>PFP 2-Step</b>", 8, NAVY),
             P("Same 8/6 · 5/10. Access fee per phase. Funded fee 1 / 2 / 2.5 / 3% of size (Low / Mod / Med / High).", 7.5, NAVY, leading=10),
             P("Low/Mod 100% from first profits. Med/High 50% of funded fee upfront, rest from profits. Split only on A-book PnL.", 7.5, NAVY, leading=10),
             P("Access-only hole from $100k. With funded fee, funnel leftover ~$135 at $100k, m ~+60%.", 7.5, ORANGE, leading=10)],
            [P("<b>PFP 1-Step</b>", 8, NAVY),
             P("10% target, same 5/10. Access fee once. Same funded-fee ladder.", 7.5, NAVY, leading=10),
             P("Same 100% vs 50% upfront as PFP 2-Step. News allowed. Payouts USDC &lt;60s.", 7.5, NAVY, leading=10),
             P("Access prints (even $200k +6%). Funnel leftover ~$256 at $100k.", 7.5, GREEN, leading=10)],
            [P("<b>Instant Growth</b>", 8, NAVY),
             P("Start $10k. 6% static, no daily. 2% max/trade. Scale 6% doubles to $1M. L1 B-book (one cash-out); L2+ A-book.", 7.5, NAVY, leading=10),
             P("80% split. Next-level ~2% of new balance from profits. $2k/day cap after 6%.", 7.5, NAVY, leading=10),
             P("$10k @ $299 vs E[X] $38, leftover $261, m +87%. Residual = tower, not L1.", 7.5, GREEN, leading=10)],
        ],
        [32 * mm, 78 * mm, 78 * mm, usable - 188 * mm],
        font=7.5,
    ))

    story.append(section("Blended funnel  ·  first-payout E[X] per buyer  ·  Hive Coin k = 0"))
    blend_header = ["Plan", "P1", "P2 / eval", "Funded", "P(pay)", "P(yr1)", "E[X] $100k", "Days", "Split"]
    blend_rows = [blend_header]
    for r in blended:
        blend_rows.append([
            r["Plan"],
            pct_plain(r["Phase1"]),
            pct_plain(r["EvalPass"]),
            pct_plain(r["Funded"]),
            pct_plain(r["P_pay"]),
            pct_plain(r["P_yr1"]),
            usd(r["E_payout_100k"]),
            f"{float(r['Avg_days']):.0f}",
            f"{int(float(r['Split']) * 100)}%",
        ])
    story.append(grid(blend_rows, [52 * mm] + [(usable - 52 * mm) / 8] * 8, font=8))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "BE = E[X] because Hive Coin is not cash. Firm leftover = sale − E[X], k = 0. "
        "20 / 40 / 60 are the fees that deliver those margins: F<sub>m</sub> = BE / (1 − m). They are charge-this floors, not leftover haircuts. "
        "Instant E[X] $100k ($377) is the $10k path scaled to $100k for the catalog; live Instant is $10k only, E[X] $38.",
        8, MUTED, leading=11,
    ))

    story.append(PageBreak())
    story.append(Spacer(1, 6 * mm))
    story.append(section("Sticker vs first-payout E[X]  ·  WELCOME25  ·  Prints? = sale ≥ E[X]"))
    story.append(P(
        "Sale m = (sale − E[X]) / sale. PFP stickers are access fees only — they are not supposed to cover E[X] on their own. "
        "See the full-funnel tables below. Instant list = sale $299 (WELCOME25 not applied on the on-chain print).",
        8, MUTED, leading=11,
    ))
    story.append(Spacer(1, 1.2 * mm))

    sku_header = ["SKU", "List", "Sale", "E[X]", "BE", "20%", "40%", "60%", "Leftover", "m", "Prints?"]
    sku_data = [sku_header]
    order = [
        "Classic 2-Step (NewBee)",
        "Pay From Profits 2-Step",
        "Pay From Profits 1-Step",
        "Instant Growth L1",
    ]
    by_plan = {p: [] for p in order}
    for r in skus:
        by_plan.setdefault(r["Plan"], []).append(r)
    for plan in order:
        for r in sorted(by_plan.get(plan, []), key=lambda x: float(x["Size"])):
            sale = float(r["Sale"])
            e = float(r["E_payout"])
            sku_data.append([
                sku_short(r["Plan"], float(r["Size"])),
                usd(r["List"]),
                usd(sale),
                usd(e),
                usd(r["BE"]),
                usd(r["px_20"]),
                usd(r["px_40"]),
                usd(r["px_60"]),
                usd(sale - e),
                pct_signed(r["sale_m"]),
                color_print(r["prints"].lower() == "true"),
            ])
    n_cols = 11
    first_w = 40 * mm
    last_w = 20 * mm
    mid = (usable - first_w - last_w) / (n_cols - 2)
    story.append(grid(sku_data, [first_w] + [mid] * (n_cols - 2) + [last_w], font=7))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "PFP 2-Step $100k and $200k are the only stickers that do not cover first-payout E[X]. "
        "The next tables add the funded-account fee — that is the real PFP unit.",
        8, MUTED, leading=11,
    ))

    pfp2_data = [["Size", "Access sale", "E[access]", "E[funded fee]", "Funnel in", "E[X]", "Leftover", "m", "Prints?"]]
    for r in pfp2:
        pfp2_data.append([
            usd(r["Size"]),
            usd(r["Access_sale"]),
            usd(r["E_access"]),
            usd(r["E_funded_fee"]),
            usd(r["E_revenue"]),
            usd(r["E_payout"]),
            usd(r["Leftover"]),
            pct_signed(r["m"]),
            color_print(r["prints"].lower() == "true"),
        ])
    pfp1_data = [["Size", "Access sale", "E[access]", "E[funded fee]", "Funnel in", "E[X]", "Leftover", "m", "Prints?"]]
    for r in pfp1:
        pfp1_data.append([
            usd(r["Size"]),
            usd(r["Access_sale"]),
            usd(r["E_access"]),
            usd(r["E_funded_fee"]),
            usd(r["E_revenue"]),
            usd(r["E_payout"]),
            usd(r["Leftover"]),
            pct_signed(r["m"]),
            color_print(r["prints"].lower() == "true"),
        ])
    story.append(KeepTogether([
        section("PFP 2-Step full funnel  ·  access + funded fee − E[X]"),
        P(
            "Risk map: Pro+Semi → Low 1% of size, 100% from profits. Average → Moderate 2%, 100% from profits. "
            "Aggressive → Medium 2.5%, 50% upfront. Lottery → High 3%, 50% upfront. Weighted P(reach funded) ≈ 12.8%. "
            "E[access] is two WELCOME25 access fees × P(reach that phase).",
            8, MUTED, leading=11,
        ),
        Spacer(1, 1 * mm),
        grid(pfp2_data, [24 * mm] + [(usable - 24 * mm) / 8] * 8, font=8),
    ]))
    story.append(section("PFP 1-Step full funnel  ·  access + funded fee − E[X]"))
    story.append(P(
        "Weighted P(reach funded) ≈ 18.4%. Same funded-fee ladder as PFP 2-Step. Access is paid once.",
        8, MUTED, leading=11,
    ))
    story.append(Spacer(1, 1 * mm))
    story.append(grid(pfp1_data, [24 * mm] + [(usable - 24 * mm) / 8] * 8, font=8))

    story.append(section("How to read this"))
    bullets = [
        "<b>Prints?</b> on the SKU table is sticker-only: sale ≥ first-payout E[X]. Classic, Instant, and PFP 1-Step all yes. PFP 2-Step $100k/$200k no — until you add the funded fee.",
        "<b>BE = E[X]</b> here. Hive Coin (200% of fee on pass, max 50% of next challenge) is a coupon for the next buy, not a cash rebate, so k = 0.",
        "<b>20 / 40 / 60</b> are the fees that deliver those margins: F<sub>m</sub> = BE / (1 − m). Example Classic $100k: BE $89 → 20% = $111, 40% = $148, 60% = $222. They are not “sale minus a haircut.”",
        "<b>Instant $10k @ $299</b> is the on-chain Jun 2026 price. L1 is B-book, one cash-out, 80% split, 6% static, no daily. Residual risk is scaling (double at 6%, L2+ A-book, next-level ~2% of new balance from profits).",
        "<b>A-book clawback</b> (TOS: split only on A-book PnL) is not in E[X]. Leftover in these tables is a floor for the firm, not a ceiling.",
        "<b>News is allowed.</b> Weekend holding: eval yes on Classic, funded no. Payouts USDC &lt;60s. 80% of challenge fees locked in the contract as payout liquidity (their FAQ).",
        "<b>Book:</b> industry-calibrated CFD 7 / 22 / 26 / 28 / 17 (Pro / Semi / Average / Aggressive / Lottery). 700 Monte Carlo paths per profile per SKU.",
    ]
    for b in bullets:
        story.append(P("•  " + b, 8.5, NAVY, leading=11.5))
        story.append(Spacer(1, 0.8 * mm))

    story.append(section("Failure mix  ·  share of all buyers  ·  top reasons"))
    fail = [
        ["Product", "p1 max/trade", "p1 max DD", "p2 max DD", "post M1", "time / daily / KYC"],
        ["Classic 2-Step", "40.7%", "23.8%", "6.6%", "5.9%", "abandon 5.4% · daily 4.3% · KYC 2.0%"],
        ["PFP 2-Step", "40.3%", "24.9%", "6.4%", "4.9%", "abandon 5.3% · daily 5.0% · KYC ~2%"],
        ["PFP 1-Step", "41.0%", "25.6%", "—", "7.4%", "abandon 6.5% · daily 4.2% · KYC 2.6%"],
        ["Instant L1", "45.0%", "7.6%", "—", "19.3%", "post M3 7.1% · post M12 4.4%"],
    ]
    story.append(grid(fail, [36 * mm, 28 * mm, 26 * mm, 26 * mm, 24 * mm, usable - 140 * mm], font=8))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "The 3% max/trade (Classic/PFP) and 2% max/trade (Instant) TOS caps are why Lottery and Aggressive almost never pay. That is the print engine.",
        8, MUTED, leading=11,
    ))

    story.append(section("Caveats"))
    caveats = [
        "Classic <b>list</b> is from TheTrustedProp, not a scraped checkout (Cloudflare blocked later live fetches). PFP and Instant fees are from the TOS / on-chain feed. Re-check stickers on fundedhive.com before using leftover $ as a live P&amp;L.",
        "WorkerBee (80%, 4% daily) and QueenBee (90%, 3% daily) are not priced separately here; NewBee 70% is the Classic default.",
        "PFP funded-fee expectation uses this book’s risk mix, not FundedHive’s unpublished mix of Low/Mod/Med/High. If the book is more Lottery than 17%, funded-fee income rises and leftover rises.",
        "E[X] is first cash-out only. Instant tower, Classic scale, and A-book after first payout are not in the leftover number.",
        "$100 minimum reward is assumed (not published). Instant may effectively need the 6% scale target before a full withdrawal.",
        "A-book clawback is not in E[X]; real leftover is higher for the firm.",
    ]
    for c in caveats:
        story.append(P("•  " + c, 8.5, NAVY, leading=11.5))
        story.append(Spacer(1, 0.6 * mm))
    story.append(section("Sources"))
    story.append(P(
        "fundedhive.com homepage  ·  TOS PDF https://fundedhive.com/static/assets/download/terms-and-conditions.pdf (Jan 2026)  ·  "
        "on-chain Instant pricing Jun 2026  ·  TheTrustedProp Classic list  ·  coupon WELCOME25  ·  "
        "runner sim/run_fundedhive.py  ·  markdown results/FUNDEDHIVE.md  ·  CSVs results/fundedhive_*.csv",
        8, MUTED, leading=11,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(P("Not investment advice. Internal print/BE card for Verodus research.", 8, MUTED, TA_CENTER))

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=PAGE,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=20 * mm,
        bottomMargin=16 * mm,
        title="FundedHive print and breakeven",
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
