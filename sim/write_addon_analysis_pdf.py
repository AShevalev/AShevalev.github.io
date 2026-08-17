#!/usr/bin/env python3
"""Standalone PDF: 19-peer checkout add-ons vs the Verodus rec.

Why each Verodus add-on exists, what to change to stay attractive, and
what not to copy. Challenge fees are locked and are not reopened here.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from competitor_addons import FIRMS, leftover, pct_s

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Addon_Competitor_Analysis_2026-08-17.pdf"

PAGE = A4
W, H = PAGE
MARGIN = 14 * mm

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_REC = colors.HexColor("#dcfce7")
ROW_NO = colors.HexColor("#fee2e2")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")

INST_LIST, PRO_LIST = 675, 445
INST_BE, PRO_BE = 283.99, 150.61


def usd(n):
    n = float(n)
    if abs(n - round(n)) < 0.05:
        return f"${int(round(n)):,}"
    return f"${n:,.0f}"


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Times-Bold",
            fontSize=18, leading=22, textColor=NAVY, alignment=TA_LEFT, spaceAfter=4,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Times-Italic",
            fontSize=10, leading=13, textColor=TEAL, spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Times-Bold",
            fontSize=12, leading=15, textColor=NAVY, spaceBefore=9, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=9, leading=12, alignment=TA_JUSTIFY, spaceAfter=5,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=7.2, leading=9, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.2, leading=9, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7.2, leading=9, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=8, leading=10.2, textColor=colors.HexColor("#334155"),
            spaceAfter=4,
        ),
    }


def P(text, style):
    return Paragraph(text, style)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 9 * mm, W, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        MARGIN, H - 5.6 * mm,
        "VERODUS  ·  Checkout add-ons vs 19 peers  ·  17 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.6 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        MARGIN, 3 * mm,
        "Stickers = % of list. Shopper pays 65% after VERO35. After ads = sticker × 0.52 − extra E[X].",
    )
    canvas.drawRightString(W - MARGIN, 3 * mm, str(doc.page))
    canvas.restoreState()


def grid(data, col_w, special=None):
    special = special or {}
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
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


def leftover_rows():
    return [
        ("Instant weekly 80% @ 8%", INST_LIST, 0.08, 0.08 * INST_BE, "rec"),
        ("Instant 80% on-demand @ 15%", INST_LIST, 0.15, 0.12 * INST_BE, "rec"),
        ("Instant 90% solo @ 15% (new)", INST_LIST, 0.15, 0.125 * INST_BE, "rec"),
        ("Instant 90% solo @ 20% (old)", INST_LIST, 0.20, 0.125 * INST_BE, None),
        ("Instant 90% On Demand @ 32%", INST_LIST, 0.32, 0.41 * INST_BE, "rec"),
        ("Instant 90%+anytime at BG 15%", INST_LIST, 0.15, 0.41 * INST_BE, "no"),
        ("Instant 90%+anytime at FN 5%", INST_LIST, 0.05, 0.41 * INST_BE, "no"),
        ("Pro weekly 80% @ 8%", PRO_LIST, 0.08, 0.05 * PRO_BE, "rec"),
        ("Pro 80% on-demand @ 12%", PRO_LIST, 0.12, 0.05 * PRO_BE, "rec"),
        ("Pro 90% @ 12%", PRO_LIST, 0.12, 0.125 * PRO_BE, "rec"),
        ("Pro 90% On Demand @ 20%", PRO_LIST, 0.20, 0.125 * PRO_BE, "rec"),
        ("Pro 90%+7-day at BG 25%", PRO_LIST, 0.25, 0.125 * PRO_BE, None),
        ("Pro Swing @ 20%", PRO_LIST, 0.20, 0.06 * PRO_BE, "rec"),
        ("Instant Swing @ 20%", INST_LIST, 0.20, 0.13 * INST_BE, "rec"),
    ]


def build():
    s = styles()
    story = []
    story.append(P("Verodus checkout add-ons: competitor analysis", s["cover"]))
    story.append(P(
        "19-peer CFD street, August 2026. Challenge fees stay locked. "
        "This card answers whether the add-on menu should change to stay attractive, "
        "and why each Verodus line is priced as it is.",
        s["sub"],
    ))

    story.append(P("1. Verdict — change two lines, keep the rest", s["h1"]))
    story.append(P(
        "Yes. Two product changes make the menu look like the street without "
        "reopening Instant 90%+anytime (the year-1 floor) or copying loss-leaders.",
        s["body"],
    ))
    story.append(P(
        "<b>1. Weekly Rewards: 70% split at 6% of list → 80% split at 8% of list.</b> "
        "Default is already 80% biweekly. A 70% weekly SKU reads as a FundingPips / "
        "Hola trap (faster cycle, worse split). Shoppers who want weekly cash flow "
        "should keep the same 80%. 8% of list undercuts Blue Guardian’s 7-day +15% "
        "and BrightFunded weekly +25%. Instant $100k leftover after ads is about "
        "<b>+$5</b>; Pro $100k about <b>+$11</b>.",
        s["body"],
    ))
    story.append(P(
        "<b>2. Instant 90% solo: 20% → 15% of list.</b> Blue Guardian Instant 90% "
        "is +15%. Alpha is ~10%; FXIFY / BrightFunded are 20%. Matching BG on the "
        "solo 90% line is the shopper comparison. Extra E[X] on Instant 90% <i>alone</i> "
        "is the split (~12.5% of year-1 BE, ~$35), not the 41% anytime stack. "
        "15% of $675 stickers $101; after VERO35 and 20% ads leftover is about "
        "<b>+$17</b>. Do <b>not</b> drop the 90% + on-demand <i>bundle</i> below 32%.",
        s["body"],
    ))
    story.append(P(
        "Do not cheapen Swing 20%, eval 90% On Demand 20%, Instant 90% On Demand 32%, "
        "or add Blue Guardian’s 30/35/40 copy ladder. Do not match FundedNext on-demand "
        "+5% with 95%. Challenge rec sales stay: Instant $49/$69/$139/$239/$439; "
        "1-Step $36/$60/$120/$193/$335/$654; Lite $42/$55/$94/$149/$269/$499; "
        "Pro $45/$59/$95/$159/$289/$577. Coupon VERO35 = 35% off list + stickers.",
        s["body"],
    ))

    story.append(P("2. Locked Verodus menu after the attractiveness pass", s["h1"]))
    heads = ["Add-on", "Evals", "Instant", "What it does", "Why this %"]
    data = [[P(h, s["th"]) for h in heads]]
    rec_rows = [
        ("News trading", "12%", "12%",
         "Turns the funded high-impact news window off.",
         "Live is 15%. Street often includes eval news or buries it in Swing. 12% is below live and still insurance."),
        ("Weekend holding", "12%", "12%",
         "Turns Friday 22:00 UTC flatten off.",
         "Live is 18%. The5ers / FXIFY evals / Goat CFD include it. 12% is the paid SKU, not a 18% premium."),
        ("Swing (both)", "20%", "20%",
         "News + weekend as one add-on. Second row shows Incl.",
         "FTMO Swing is a SKU (~10–15% + 1:30 lev). Instant Funding is one toggle. 20% saves 4pp vs 12+12."),
        ("Weekly Rewards", "8%", "8%",
         "Every 7 days at the default 80% split. XOR with on-demand and 90%.",
         "Was 70% @ 6% (gotcha). 8% still prints. BG 7-day is 15%; BrightFunded weekly is 25%."),
        ("On Demand 80%", "12%", "15%",
         "Anytime withdrawal, keep 80%. XOR with weekly.",
         "BG Instant includes this (their default is on-demand). Verodus default is biweekly, so speed is paid. Instant 15% matches BG’s 7-day fee, not FN +5%."),
        ("90% Reward Split", "12%", "15%",
         "Keep 90% on the default biweekly cycle. XOR with weekly.",
         "Street 10–20%. Eval 12% undercuts BG 15%. Instant 15% matches BG Instant 90% solo. Alpha 10% is too thin on Instant leftover if bundled with speed."),
        ("90% On Demand", "20%", "32%",
         "Both on-demand and 90% on. 90% row Incl. Not 12+12 / 15+15.",
         "Only BG publishes a real bundle save (15+15→25%). Eval 20% undercuts that 25%. Instant 32% is year-1 extra E[X] (~$116) after ads. BG Instant 15% for 90%+OD is −$64 here."),
        ("Accounts 1–4", "VERO35 each", "VERO35 each",
         "Same add-ons on every copy. No extra % off copies. No 5th free.",
         "Only BG has a shopper 4-pack (25/30/35/40). Instant leftover ~$13 cannot fund a visible extra cut. VERO35 already 35% vs BG 25% on copy 1."),
    ]
    spec = {}
    for i, row in enumerate(rec_rows, start=1):
        spec[i] = "rec"
        data.append([P(c, s["tdl"] if j in (0, 3, 4) else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [32*mm, 22*mm, 26*mm, 52*mm, 56*mm], spec))
    story.append(P(
        "Green = locked rec. Sticker = round(list × %). First-payout refund is the challenge fee only — add-ons stay.",
        s["tiny"],
    ))

    story.append(P("3. What the 19-peer street is actually selling", s["h1"]))
    story.append(P(
        "Most firms do <b>not</b> have a five-toggle menu. Split and speed are often "
        "the product (FundingPips, Hola, E8, Fintokei). Holding is often free on "
        "evals (The5ers, For Traders, Goat CFD, FXIFY). The shops that look like "
        "Verodus — Blue Guardian, FundedNext, FXIFY, BrightFunded, Instant Funding — "
        "are the ones the % rec has to beat on a screenshot.",
        s["body"],
    ))
    heads = ["Firm", "90% / higher", "Faster payout", "Weekly", "Swing / hold"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    highlight = {"Blue Guardian", "FXIFY", "Alpha Capital", "FundedNext", "BrightFunded", "Instant Funding"}
    for i, r in enumerate(FIRMS, start=1):
        if r["firm"] in highlight:
            spec[i] = "rec"
        data.append([
            P(r["firm"], s["tdl"]),
            P(pct_s(r["split90_pct"]), s["td"]),
            P(pct_s(r["od_pct"]), s["td"]),
            P(pct_s(r["weekly_pct"]), s["td"]),
            P(pct_s(r["swing_pct"]), s["td"]),
        ])
    story.append(grid(data, [38*mm, 32*mm, 38*mm, 28*mm, 32*mm], spec))
    story.append(P(
        "incl. = in the base product (0% extra). — = not sold as a percent of fee. "
        "Green = firms whose published +% set the screenshot comparison.",
        s["tiny"],
    ))

    story.append(P("4. How each street cluster prices the same idea", s["h1"]))
    story.append(P(
        "<b>90% / 95% / 100%.</b> Published fees cluster 10–20% of the challenge: "
        "Alpha ~10%, Instant Funding ~10% for +10pp split, Blue Guardian 15%, "
        "FXIFY and BrightFunded 20%, Goat futures 90% 20% (CFD 100% unpublished). "
        "FundedNext Lifetime 95% is 25–30% — a different product. "
        "Verodus eval 12% sits under BG. Instant 90% solo at 15% sits on BG, under FXIFY.",
        s["body"],
    ))
    story.append(P(
        "<b>Speed.</b> Blue Guardian eval 7-day +15%. FXIFY biweekly +5% off a monthly default. "
        "BrightFunded weekly +25%. FundedNext biweekly +15–25%. "
        "FundingPips and Hola do not charge a fee: weekly is a worse split (60% / 65%). "
        "That is the model Verodus is leaving. BG Instant Standard includes on-demand at 80%; "
        "Verodus Instant does not, so on-demand 80% at 15% Instant is the paid equivalent of what BG gives away.",
        s["body"],
    ))
    story.append(P(
        "<b>90% + speed as a bundle.</b> Only Blue Guardian publishes a real save: 15+15 → 25%. "
        "FXIFY stacks 20+5 with no save. FundedNext +5% on-demand already includes 95% — "
        "that is a loss-leader (Instant $100k leftover about −$99 if copied). "
        "Verodus evals: 12+12 → 20% (save 4pp, cheaper than BG 25%). "
        "Instant: 15+15 would be 30% and still a hole; 32% is the floor that almost clears year-1 extra E[X] (−$4).",
        s["body"],
    ))
    story.append(P(
        "<b>Holding.</b> The5ers, Fintokei, For Traders, Goat CFD, and FXIFY evals include weekend. "
        "FTMO, Alpha, Maven, and Instant Funding sell Swing as a SKU or one toggle. "
        "FTMO Swing is roughly a 10–15% SKU premium plus 1:30 leverage. "
        "Charging 12%+12% and bundling at 20% is in-family with Instant Funding’s news+weekend add-on. "
        "Blue Guardian does not sell this pair.",
        s["body"],
    ))
    story.append(P(
        "<b>Quantity.</b> Only Blue Guardian has a shopper-facing 4-pack ladder (site code 25%, "
        "then 30/35/40, 5th-free on some futures). FundedNext Double Up is +40% now for a second "
        "account after you pass. For Traders uses BOGO. Instant Funding uses points on the next order. "
        "VERO35 is already 35% off every copy — better than BG’s 25% on the first and about even with "
        "BG’s ~32.5% average on a 4-pack. Extra cuts on copies 2–4 do not print on Instant (~$13 leftover) "
        "or Lite (~$14). A 10% extra on Instant $100k copy 2 is about −$22 after ads.",
        s["body"],
    ))

    story.append(P("5. Leftover check — why 32% Instant and why not 15%", s["h1"]))
    story.append(P(
        "After ads = sticker × 0.65 × 0.80 − extra E[X] = sticker × 0.52 − extra. "
        "Instant extra: weekly speed ~8% of year-1 BE $284; 80% on-demand ~12%; "
        "90% solo ~12.5%; 90%+anytime ~41% (~$116). Eval extra is first-payout only "
        "(Pro BE $151). Weekend gap tail is not in extra E[X] — keep Swing at 20%.",
        s["body"],
    ))
    heads = ["SKU", "Sticker", "Extra E[X]", "After ads", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (name, lst, pct, extra, mark) in enumerate(leftover_rows(), start=1):
        left, sticker = leftover(lst, pct, extra)
        if left >= -1:
            flag = "yes"
        elif left >= -5:
            flag = "thin — keep"
        else:
            flag = "NO — hole"
        spec[i] = mark or ("no" if flag.startswith("NO") else None)
        data.append([
            P(name, s["tdl"]),
            P(usd(sticker), s["td"]),
            P(usd(extra), s["td"]),
            P(usd(left), s["td"]),
            P(flag, s["td"]),
        ])
    story.append(grid(data, [58*mm, 24*mm, 28*mm, 26*mm, 32*mm], spec))
    story.append(P(
        "Green = rec. Red = do not copy. Instant 90% On Demand at 32% is −$4 — the floor, not a cut. "
        "BG Instant 15% and FN +5% for 90%+anytime are holes of −$64 and −$99 on Instant $100k.",
        s["tiny"],
    ))

    story.append(P("6. Why not match the cheapest published line", s["h1"]))
    story.append(P(
        "<b>Alpha 10% 90%.</b> Fine as a solo eval sticker. Instant $100k at 10% stickers $68; "
        "after ads ~$35 versus 90% extra ~$35 — breakeven solo, insolvent the moment the buyer "
        "also wants anytime. Verodus sells those as a bundle at 32%, not as 10%+15%.",
        s["body"],
    ))
    story.append(P(
        "<b>FundedNext +5% on-demand with 95%.</b> Screenshot-cheap. Extra E[X] on Instant is "
        "the 90%+anytime stack. 5% of $675 is $34; after ads $18 versus $116 cost. Ignore it. "
        "FN’s 95% Lifetime add-on is 25–30% of fee — that is the real 95% price.",
        s["body"],
    ))
    story.append(P(
        "<b>Blue Guardian Instant 15% for 90%.</b> Their Instant Standard already includes "
        "on-demand at 80%. The 15% only buys the extra 10pp of split. Verodus Instant default "
        "is biweekly 80%, so the same 15% would buy 90% <i>and</i> anytime if copied as one SKU. "
        "That is a different product. Copy 15% for 90% <i>solo</i>. Keep 32% when anytime is on.",
        s["body"],
    ))
    story.append(P(
        "<b>Weekly 70% at 6%.</b> It printed, and it was the cheapest speed SKU on the street. "
        "It also taught shoppers that faster = worse split, which is FundingPips’ trick. "
        "Default 80% weekly at 8% is the attractive read and still prints.",
        s["body"],
    ))

    story.append(P("7. Firm-by-firm notes (why they do not set the rec)", s["h1"]))
    heads = ["Firm", "Note"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(FIRMS, start=1):
        if r["firm"] in highlight:
            spec[i] = "rec"
        data.append([P(r["firm"], s["tdl"]), P(r["note"], s["tdl"])])
    story.append(grid(data, [40*mm, 138*mm], spec))
    story.append(Spacer(1, 2 * mm))

    story.append(P("8. Checkout logic that must ship with these prices", s["h1"]))
    story.append(P(
        "Sticker = round(list × %). VERO35 is 35% off (list + stickers), capped at 35%. "
        "Cart = (list + stickers − coupon) × quantity. Quantity 1–4; same add-ons on every copy. "
        "News + weekend = Swing at 20% (weekend row Incl.). On-demand + 90% = 90% On Demand "
        "at 20% eval / 32% Instant (90% row Incl.). Weekly XOR both payout upgrades. "
        "On-demand and 90% may both be on — that is the bundle, not a stack of 12+12 or 15+15. "
        "Tooltips are product/rules only — never “X% of list”. 80% / 90% in copy is the split, not the fee. "
        "First-payout refund is the challenge fee only. Complete HTML with this logic: "
        "landing/checkout.html. Drop-in for live checkout.css: landing/checkout-addons.html.",
        s["body"],
    ))
    story.append(P(
        "Challenge rec fees do not move. Add-on cash is extra AOV. Do not cut Instant $439 / "
        "Pro $289 / Lite $269 / 1-Step $335 because some buyers add Swing.",
        s["body"],
    ))

    RESULTS.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=PAGE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14 * mm, bottomMargin=12 * mm,
        title="Verodus checkout add-ons vs 19 peers",
        author="Verodus",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
