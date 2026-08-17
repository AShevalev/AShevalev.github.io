#!/usr/bin/env python3
"""Profitable-but-competitive add-on % on the news-included challenge card.

Addon leftover = round(list × pct) × 0.65 × 0.80 − extra E[X].
Prints if leftover ≥ −$1. Instant extra is year-1 BE; evals are first-payout BE.
"""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate

from write_price_rec_pdf import (
    H,
    MARGIN,
    MARKETING,
    NAVY,
    W,
    P,
    grid,
    styles as rec_styles,
    usd,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Addon_Pct_BE_2026-08-17.pdf"
OUT_SHOP = RESULTS / "verodus-addon-pct-be-2026-08-17.pdf"
MD = RESULTS / "ADDON_PCT_REC.md"

PAGE = landscape(A4)
NET = 0.65 * (1.0 - MARKETING)  # 0.52 after VERO35 and 20% ads

# Extra E[X] vs default Bi-Weekly 80%, as a fraction of priced BE.
# Instant = year-1. Evals = first-payout. Weekly "speed" ignores the 70% vs 80%
# split cut (conservative). Honest weekly credits that 10pp cut (−12.5% of BE).
EXTRA = {
    "Instant": {"weekend": 0.08, "weekly": 0.08, "od90": 0.41},
    "1-Step": {"weekend": 0.04, "weekly": 0.05, "od90": 0.125},
    "2-Step Lite": {"weekend": 0.04, "weekly": 0.05, "od90": 0.125},
    "2-Step Pro": {"weekend": 0.04, "weekly": 0.05, "od90": 0.125},
}
WEEKLY_SPLIT = -0.125  # 70/80 − 1

# Charge this. Instant On Demand cannot match eval 15–20% and still print.
REC_PCT = {
    "weekend": {"Instant": 0.12, "eval": 0.12},
    "weekly": {"Instant": 0.08, "eval": 0.08},
    "od90": {"Instant": 0.32, "eval": 0.15},
}

LIVE_PCT = {"weekend": 0.18, "weekly": 0.06, "od90": 0.20}
NOW_PCT = {"weekend": 0.15, "weekly": 0.06, "od90": 0.20}

SWEEP = (0.06, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.32)


def js_round(x: float) -> int:
    return int(x + 0.5) if x >= 0 else int(x - 0.5)


def sticker(list_px: float, pct: float) -> int:
    return js_round(float(list_px) * float(pct))


def leftover(stick: float, extra: float) -> float:
    return float(stick) * NET - extra


def flag(left: float) -> str:
    if left >= -1:
        return "yes"
    if left >= -5:
        return "thin"
    return "NO"


def be_sticker(extra: float) -> float:
    if extra <= 1:
        return 0.0
    return extra / NET


def load_skus():
    path = RESULTS / "verodus_reprice_news_included.csv"
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            rows.append({
                "Plan": r["Plan"],
                "Size": int(float(r["Size"])),
                "N": int(float(r["N"])),
                "BE": float(r["BE"]),
                "S_opex": float(r["S_opex"]),
                "Sale": float(r["New"]),
                "List": float(r["List"]),
                "Chal": float(r["Left1"]),
            })
    return rows


def extra_of(plan: str, key: str, be: float, honest_weekly: bool = False) -> float:
    frac = EXTRA[plan][key]
    if key == "weekly" and honest_weekly:
        frac = frac + WEEKLY_SPLIT
    return be * frac


def rec_pct(plan: str, key: str) -> float:
    band = "Instant" if plan == "Instant" else "eval"
    return REC_PCT[key][band]


def header(title: str, foot: str):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Bold", 8)
        canvas.drawString(MARGIN, H - 5.4 * mm, title)
        canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Roman", 7.4)
        canvas.drawString(MARGIN, 2.6 * mm, foot)
        canvas.drawRightString(W - MARGIN, 2.6 * mm, str(doc.page))
        canvas.restoreState()
    return _draw


def money(x) -> str:
    if abs(x) < 0.5:
        return "$0"
    sign = "−" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct_s(p: float) -> str:
    return f"{p * 100:.0f}%"


def sku_100k(skus, plan):
    for r in skus:
        if r["Plan"] == plan and r["Size"] == 100000:
            return r
    raise SystemExit(f"missing {plan} $100k")


def build():
    s = rec_styles()
    skus = load_skus()
    inst = sku_100k(skus, "Instant")
    pro = sku_100k(skus, "2-Step Pro")
    one = sku_100k(skus, "1-Step")
    lite = sku_100k(skus, "2-Step Lite")

    story = []
    story.append(P("Add-on % that print and still look like the street", s["cover"]))
    story.append(P(
        "News-included challenge card · VERO35 35% off list + stickers · 20% ads. "
        "Charge the lowest % that covers extra E[X] on Instant $100k. "
        "Do not copy Blue Guardian Instant 15% or FundedNext +5% for 90% + anytime.",
        s["sub"],
    ))

    story.append(P("Charge this", s["h1"]))
    heads = ["Add-on", "Instant", "1-Step / Lite / Pro", "Instant $100k sticker",
             "Addon leftover", "Combined", "Street"]
    data = [[P(h, s["th"]) for h in heads]]
    rec_rows = (
        ("News trading", "included", "included", 0, 0, inst["Chal"],
         "Usually included. Not a SKU."),
        ("Weekend Holding", 0.12, 0.12, None, None, None,
         "FTMO / Alpha Swing ~10–15%. Live 18%."),
        ("Weekly Rewards 70%", 0.08, 0.08, None, None, None,
         "Live 6%. BG 7-day 15% without cutting split."),
        ("On Demand Rewards 90%", 0.32, 0.15, None, None, None,
         "BG 15% · FXIFY / BrightFunded 20%. Instant BE is 32%."),
        ("Bi-Weekly 80%", "included", "included", 0, 0, inst["Chal"],
         "Default. Not a toggle. Min $100."),
    )
    spec = {}
    for i, row in enumerate(rec_rows, start=1):
        name, ip, ep = row[0], row[1], row[2]
        if name in ("Weekend Holding", "Weekly Rewards 70%", "On Demand Rewards 90%"):
            spec[i] = "rec"
            key = {"Weekend Holding": "weekend", "Weekly Rewards 70%": "weekly",
                   "On Demand Rewards 90%": "od90"}[name]
            stick = sticker(inst["List"], ip)
            extra = extra_of("Instant", key, inst["BE"])
            add = leftover(stick, extra)
            comb = inst["Chal"] + add
            ip_s, ep_s = pct_s(ip), pct_s(ep)
            data.append([
                P(name, s["tdl"]), P(ip_s, s["td"]), P(ep_s, s["td"]),
                P(usd(stick), s["td"]), P(money(add), s["td"]),
                P(money(comb), s["td"]), P(row[6], s["tdl"]),
            ])
        else:
            spec[i] = "live"
            data.append([
                P(name, s["tdl"]), P(str(ip), s["td"]), P(str(ep), s["td"]),
                P("—", s["td"]), P("—", s["td"]), P(money(row[5]), s["td"]),
                P(row[6], s["tdl"]),
            ])
    story.append(grid(data, [
        38 * mm, 22 * mm, 32 * mm, 32 * mm, 28 * mm, 24 * mm, 72 * mm,
    ], spec))
    story.append(P(
        "Green = paid add-on rec. Instant On Demand at 32% is the year-1 floor, not a street match. "
        "Evals On Demand at 15% matches Blue Guardian’s 90% add-on and still prints. "
        "Same 20% on Instant $100k leaves about −$15 combined — do not ship that if Instant has to print.",
        s["tiny"],
    ))

    story.append(P("1. Formula", s["h1"]))
    story.append(P(
        "List is checkout <b>basePrice</b> (sale ÷ 0.65). Sticker = round(list × %). "
        "Shopper pays 65% of the sticker after VERO35. Ads take 20% of that cash. "
        "Addon leftover = sticker × 0.52 − extra E[X]. "
        "Prints if leftover ≥ −$1. Combined leftover = challenge leftover + addon leftover. "
        "Challenge leftover already has BE + 10% error + $1/account + wage share, then sale × 0.80 minus that stack. "
        "CAD 10,000/mo wages (~$7,200) sit in the challenge stack, not on the add-on.",
        s["body"],
    ))
    story.append(P(
        "Instant BE is year-1 E[X]. Eval BE is first-payout E[X] / (1 − P(pay)). "
        "Extra E[X] is a fraction of that BE versus default Bi-Weekly 80%. "
        "Weekend Instant 8% · eval 4%. Weekly speed Instant 8% · eval 5% "
        "(conservative: treats Weekly 70% like faster 80%). "
        "On Demand 90% Instant 41% · eval 12.5% (80→90 is +12.5%; Instant anytime is the rest of the 41%).",
        s["body"],
    ))

    story.append(P("2. Challenge BE and leftover (news-included card)", s["h1"]))
    heads = ["Plan", "Size", "BE", "Opex floor", "Sale", "List", "Challenge leftover"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(skus, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["S_opex"]), s["td"]),
            P(usd(r["Sale"]), s["td"]), P(usd(r["List"]), s["td"]),
            P(money(r["Chal"]), s["td"]),
        ])
    story.append(grid(data, [
        32 * mm, 22 * mm, 22 * mm, 28 * mm, 22 * mm, 22 * mm, 36 * mm,
    ], spec))
    story.append(P(
        "Instant $100k leftover ~$26. Lite $5k is about $0 after allocated wages — leftover sits on $25k+. "
        "That $26 does not cover Instant 90% + anytime at 20% of list.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("3. Break-even % of list", s["h1"]))
    story.append(P(
        "BE sticker = extra E[X] ÷ 0.52. BE % = BE sticker ÷ list. "
        "Weekly uses the conservative speed extra (no credit for 70% vs 80%). "
        "Charge above this floor, then stop at the street.",
        s["body"],
    ))
    heads = ["Plan", "Size", "List", "BE $",
             "WE extra", "WE BE%", "Wk extra", "Wk BE%", "OD extra", "OD BE%"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(skus, start=1):
        spec[i] = "rec" if r["Size"] == 100000 else None
        we_x = extra_of(r["Plan"], "weekend", r["BE"])
        wk_x = extra_of(r["Plan"], "weekly", r["BE"])
        od_x = extra_of(r["Plan"], "od90", r["BE"])
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(usd(r["BE"]), s["td"]),
            P(usd(we_x), s["td"]), P(pct_s(be_sticker(we_x) / r["List"]), s["td"]),
            P(usd(wk_x), s["td"]), P(pct_s(be_sticker(wk_x) / r["List"]), s["td"]),
            P(usd(od_x), s["td"]), P(pct_s(be_sticker(od_x) / r["List"]), s["td"]),
        ])
    story.append(grid(data, [
        28 * mm, 20 * mm, 18 * mm, 18 * mm,
        22 * mm, 20 * mm, 22 * mm, 20 * mm, 22 * mm, 20 * mm,
    ], spec))
    story.append(P(
        f"Binding SKU is Instant $100k: Weekend BE {pct_s(be_sticker(extra_of('Instant', 'weekend', inst['BE'])) / inst['List'])}, "
        f"Weekly speed BE {pct_s(be_sticker(extra_of('Instant', 'weekly', inst['BE'])) / inst['List'])}, "
        f"On Demand 90% BE {pct_s(be_sticker(extra_of('Instant', 'od90', inst['BE'])) / inst['List'])}. "
        f"Pro $100k On Demand BE is only {pct_s(be_sticker(extra_of('2-Step Pro', 'od90', pro['BE'])) / pro['List'])} — evals can sit in the 10–20% street band.",
        s["tiny"],
    ))

    story.append(P("4. Instant $100k leftover sweep (binding constraint)", s["h1"]))
    be = inst["BE"]
    lst = inst["List"]
    chal = inst["Chal"]
    heads = ["% of list", "Sticker", "After VERO35+ads",
             "WE extra $22", "WE left", "Wk extra $22", "Wk left",
             "OD extra $112", "OD left", "OD + challenge"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    we_x = extra_of("Instant", "weekend", be)
    wk_x = extra_of("Instant", "weekly", be)
    od_x = extra_of("Instant", "od90", be)
    rec_marks = {0.12: "weekend", 0.08: "weekly", 0.32: "od90"}
    for i, p in enumerate(SWEEP, start=1):
        stick = sticker(lst, p)
        after = stick * NET
        we_l = leftover(stick, we_x)
        wk_l = leftover(stick, wk_x)
        od_l = leftover(stick, od_x)
        if p in rec_marks:
            spec[i] = "rec"
        elif p in (0.06, 0.15, 0.20):
            spec[i] = "live"
        data.append([
            P(pct_s(p), s["td"]), P(usd(stick), s["td"]), P(usd(after), s["td"]),
            P(usd(we_x), s["td"]), P(f"{money(we_l)} {flag(we_l)}", s["td"]),
            P(usd(wk_x), s["td"]), P(f"{money(wk_l)} {flag(wk_l)}", s["td"]),
            P(usd(od_x), s["td"]), P(f"{money(od_l)} {flag(od_l)}", s["td"]),
            P(f"{money(chal + od_l)} {flag(chal + od_l)}", s["td"]),
        ])
    story.append(grid(data, [
        18 * mm, 18 * mm, 28 * mm,
        22 * mm, 22 * mm, 22 * mm, 22 * mm,
        24 * mm, 22 * mm, 30 * mm,
    ], spec))
    story.append(P(
        "Green = rec %. Blue = live / current checkout (Weekly 6%, Weekend 15%, On Demand 20%). "
        "On Demand 20% Instant $100k: addon about −$41, combined about −$15. "
        "On Demand 25% combined is about +$2 (thin). On Demand 32% addon about $0, combined about +$26. "
        "Weekly 6% addon about $0 (thin). Weekly 8% addon about +$6.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("5. Eval $100k leftover at the rec vs street", s["h1"]))
    heads = ["Plan", "Add-on", "BE %", "Rec %", "Sticker", "Extra", "Addon left",
             "Combined", "Live  %", "Live left", "BG 15% left"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 1
    for sku, plan in ((one, "1-Step"), (lite, "2-Step Lite"), (pro, "2-Step Pro")):
        for key, label in (("weekend", "Weekend"), ("weekly", "Weekly 70%"), ("od90", "On Demand 90%")):
            extra = extra_of(plan, key, sku["BE"])
            bp = be_sticker(extra) / sku["List"]
            rp = rec_pct(plan, key)
            st = sticker(sku["List"], rp)
            add = leftover(st, extra)
            live_st = sticker(sku["List"], LIVE_PCT[key])
            live_l = leftover(live_st, extra)
            bg_st = sticker(sku["List"], 0.15)
            bg_l = leftover(bg_st, extra)
            spec[i] = "rec"
            data.append([
                P(plan, s["tdl"]), P(label, s["tdl"]),
                P(pct_s(bp), s["td"]), P(pct_s(rp), s["td"]),
                P(usd(st), s["td"]), P(usd(extra), s["td"]),
                P(money(add), s["td"]), P(money(sku["Chal"] + add), s["td"]),
                P(pct_s(LIVE_PCT[key]), s["td"]), P(money(live_l), s["td"]),
                P(money(bg_l), s["td"]),
            ])
            i += 1
    story.append(grid(data, [
        26 * mm, 28 * mm, 16 * mm, 16 * mm, 18 * mm, 16 * mm, 22 * mm,
        22 * mm, 16 * mm, 20 * mm, 22 * mm,
    ], spec))
    story.append(P(
        "Every eval $100k add-on at the rec prints on its own, and combined is fat. "
        "Evals On Demand at Blue Guardian 15% still prints. Live Weekend 18% is extra leftover you do not need.",
        s["tiny"],
    ))

    story.append(P("6. Instant $100k — rec vs live vs current checkout vs holes", s["h1"]))
    heads = ["Add-on", "Live", "Now in checkout", "Rec", "Sticker rec",
             "Addon left rec", "Combined rec", "If BG 15%", "If FN 5%"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    cases = (
        ("Weekend", "weekend"),
        ("Weekly 70%", "weekly"),
        ("On Demand 90%", "od90"),
    )
    for i, (label, key) in enumerate(cases, start=1):
        spec[i] = "rec"
        extra = extra_of("Instant", key, inst["BE"])
        rp = rec_pct("Instant", key)
        st = sticker(inst["List"], rp)
        add = leftover(st, extra)
        bg = leftover(sticker(inst["List"], 0.15), extra)
        fn = leftover(sticker(inst["List"], 0.05), extra)
        data.append([
            P(label, s["tdl"]),
            P(pct_s(LIVE_PCT[key]), s["td"]),
            P(pct_s(NOW_PCT[key]), s["td"]),
            P(pct_s(rp), s["td"]),
            P(usd(st), s["td"]),
            P(f"{money(add)} {flag(add)}", s["td"]),
            P(f"{money(inst['Chal'] + add)} {flag(inst['Chal'] + add)}", s["td"]),
            P(f"{money(bg)} {flag(bg)}", s["td"]),
            P(f"{money(fn)} {flag(fn)}", s["td"]),
        ])
    story.append(grid(data, [
        32 * mm, 16 * mm, 28 * mm, 16 * mm, 24 * mm, 28 * mm, 28 * mm, 24 * mm, 22 * mm,
    ], spec))
    story.append(P(
        "Blue Guardian Instant 15% on 90% + anytime: about −$64 addon leftover. "
        "FundedNext +5%: about −$99. Those are holes. Weekend at BG-like 15% still prints. "
        "Weekly at live 6% is thin on Instant $100k if you do not credit the 70% split cut.",
        s["tiny"],
    ))

    story.append(P("7. Weekly 70% — why 8%, not 6%", s["h1"]))
    story.append(P(
        "Live charges 6% for Weekly 70%. Faster cadence costs Instant about 8% of year-1 BE (~$22 on $100k). "
        "At 6% the sticker is $41, cash after VERO35 and ads is $21, leftover about −$1 (thin). "
        "At 8% the sticker is $54, leftover about +$6. "
        "If you credit that 70% pays 12.5% less than default 80%, extra E[X] is negative and even 4% prints. "
        "Do not price Instant on that gift — a shopper who withdraws weekly still pulls year-1 cash forward. "
        "8% stays under Blue Guardian’s 15% 7-day add-on, which does not even cut the split.",
        s["body"],
    ))

    story.append(P("8. Combined leftover at the rec (every SKU)", s["h1"]))
    heads = ["Plan", "Size", "Challenge", "WE 12%", "Wk 8%", "OD rec",
             "WE comb", "Wk comb", "OD comb"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(skus, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        we_st = sticker(r["List"], rec_pct(r["Plan"], "weekend"))
        wk_st = sticker(r["List"], rec_pct(r["Plan"], "weekly"))
        od_st = sticker(r["List"], rec_pct(r["Plan"], "od90"))
        we_l = leftover(we_st, extra_of(r["Plan"], "weekend", r["BE"]))
        wk_l = leftover(wk_st, extra_of(r["Plan"], "weekly", r["BE"]))
        od_l = leftover(od_st, extra_of(r["Plan"], "od90", r["BE"]))
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(money(r["Chal"]), s["td"]),
            P(money(we_l), s["td"]), P(money(wk_l), s["td"]), P(money(od_l), s["td"]),
            P(money(r["Chal"] + we_l), s["td"]),
            P(money(r["Chal"] + wk_l), s["td"]),
            P(money(r["Chal"] + od_l), s["td"]),
        ])
    story.append(grid(data, [
        28 * mm, 20 * mm, 22 * mm, 20 * mm, 20 * mm, 20 * mm, 22 * mm, 22 * mm, 22 * mm,
    ], spec))
    story.append(P(
        "OD rec is 32% Instant / 15% evals. No Instant SKU goes red on Weekend 12% or Weekly 8%. "
        "Instant $25k On Demand 32% is fat; Instant $100k On Demand 32% is the floor.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("9. Street (published +% of that firm’s challenge fee)", s["h1"]))
    heads = ["Firm", "90% / higher split", "Faster payout", "Weekend / Swing"]
    street = (
        ("FTMO", "1-Step included; 2-Step scales", "no — biweekly", "Swing SKU ~10–15%"),
        ("FundedNext", "95%: +25–30%", "+5% and includes 95%", "not sold"),
        ("FundingPips", "on-demand cycle = 90%", "included as a cycle", "not sold"),
        ("Alpha Capital", "~10% of on-demand price", "plan variant", "separate plan"),
        ("Maven", "90% ~10% on some plans", "10 business days", "separate plan"),
        ("FXIFY", "+20% of eval fee", "evals first payout on-demand; +5% biweekly", "included on evals"),
        ("Instant Funding", "80→90 about +10%", "weekly after 14-day wait", "bundled with news"),
        ("Blue Guardian", "+15% (evals vs 85%; Instant vs 80%)",
         "Instant included at 80%; evals 7-day +15%", "not sold 12+12"),
        ("BrightFunded", "+20% of base", "no — 30 then biweekly", "holding free; news extra"),
        ("Goat Funded", "futures 90% is +20%", "2-Step add-on", "included on CFD"),
        ("Hola Prime", "monthly 95% / weekly 65%", "cycle at checkout", "not a % add-on"),
        ("Verodus live", "On Demand 90% at 20%", "Weekly 70% at 6%", "Weekend 18%; News 15%"),
        ("Verodus rec", "OD 90%: 32% Instant / 15% evals", "Weekly 70% at 8%",
         "Weekend 12%. News included"),
    )
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(street, start=1):
        spec[i] = "rec" if row[0] == "Verodus rec" else ("live" if row[0] == "Verodus live" else None)
        data.append([P(c, s["tdl"]) for c in row])
    story.append(grid(data, [32 * mm, 70 * mm, 70 * mm, 56 * mm], spec))

    story.append(P("10. What not to do", s["h1"]))
    story.append(P(
        "<b>Do not</b> put Instant 90% + anytime at 15% or 5%. Instant $100k extra E[X] is about $112. "
        "15% brings in $101 × 0.52 = $53. Hole about $64. FundedNext +5% is about −$99. "
        "<b>Do not</b> keep Instant On Demand at 20% if Instant must print — combined leftover is about −$15. "
        "<b>Do not</b> charge Weekend 18% when 12% already prints and the street often includes holding. "
        "<b>Do not</b> keep Weekly at a flat $27 — it overcharges $5k and undercharges Instant $100k. "
        "<b>Do not</b> use one On Demand % for Instant and evals unless you accept Instant $100k as a loss-leader. "
        "If you refuse Instant 32%, the least-bad one-number is <b>25%</b> (Instant combined about +$2, thin).",
        s["body"],
    ))

    story.append(P(
        "Checkout today is Weekend 15% / Weekly 6% / On Demand 20% on every plan. "
        "Move to Weekend 12% / Weekly 8% / On Demand 15% evals and 32% Instant.",
        s["sub"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus add-on % BE",
        author="Verodus",
    )
    doc.build(
        story,
        onFirstPage=header(
            "VERODUS  ·  Add-on %  ·  break-even and leftover  ·  17 Aug 2026",
            "Leftover = sticker × 0.52 − extra E[X]. Prints ≥ −$1. Instant BE = year-1. Eval BE = first payout.",
        ),
        onLaterPages=header(
            "VERODUS  ·  Add-on %  ·  break-even and leftover  ·  17 Aug 2026",
            "Leftover = sticker × 0.52 − extra E[X]. Prints ≥ −$1. Instant BE = year-1. Eval BE = first payout.",
        ),
    )
    shutil.copyfile(OUT, OUT_SHOP)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
    write_md(skus, inst, pro)
    print(f"Wrote {MD}")


def write_md(skus, inst, pro):
    we_x = extra_of("Instant", "weekend", inst["BE"])
    wk_x = extra_of("Instant", "weekly", inst["BE"])
    od_x = extra_of("Instant", "od90", inst["BE"])
    lines = [
        "# Add-on % rec — profitable but competitive",
        "",
        "PDF: `results/Verodus_Addon_Pct_BE_2026-08-17.pdf`. "
        "Leftover = `round(list × pct) × 0.52 − extra E[X]`. Prints if leftover ≥ −$1.",
        "",
        "## Charge this",
        "",
        "| Add-on | Instant | Evals | Instant $100k sticker | Why |",
        "|---|---:|---:|---:|---|",
        "| News | included | included | $0 | Not a SKU |",
        "| Weekend Holding | **12%** | **12%** | "
        f"${sticker(inst['List'], 0.12)} | Street Swing 10–15%. Live 18%. Instant BE 6%. |",
        "| Weekly Rewards 70% | **8%** | **8%** | "
        f"${sticker(inst['List'], 0.08)} | Live 6% is thin on Instant $100k. Under BG 7-day 15%. |",
        "| On Demand Rewards 90% | **32%** | **15%** | "
        f"${sticker(inst['List'], 0.32)} | Instant year-1 BE is 32%. Evals BE ~8%; 15% matches BG. |",
        "| Bi-Weekly 80% | included | included | $0 | Default. Min $100. |",
        "",
        "## Instant $100k math",
        "",
        f"List ${inst['List']:.0f}. Year-1 BE ${inst['BE']:.0f}. Challenge leftover ${inst['Chal']:.0f}.",
        "",
        f"- Weekend extra ${we_x:.0f} → BE {100 * be_sticker(we_x) / inst['List']:.0f}% of list. "
        f"Rec 12% leftover ${leftover(sticker(inst['List'], 0.12), we_x):.0f}.",
        f"- Weekly speed extra ${wk_x:.0f} → BE {100 * be_sticker(wk_x) / inst['List']:.0f}%. "
        f"Rec 8% leftover ${leftover(sticker(inst['List'], 0.08), wk_x):.0f}. "
        f"Live 6% leftover ${leftover(sticker(inst['List'], 0.06), wk_x):.0f}.",
        f"- On Demand 90% extra ${od_x:.0f} → BE {100 * be_sticker(od_x) / inst['List']:.0f}%. "
        f"Rec 32% leftover ${leftover(sticker(inst['List'], 0.32), od_x):.0f}. "
        f"Checkout 20% leftover ${leftover(sticker(inst['List'], 0.20), od_x):.0f} "
        f"(combined ${inst['Chal'] + leftover(sticker(inst['List'], 0.20), od_x):.0f}). "
        f"BG 15% leftover ${leftover(sticker(inst['List'], 0.15), od_x):.0f}.",
        "",
        f"Pro $100k On Demand extra ${extra_of('2-Step Pro', 'od90', pro['BE']):.0f} → "
        f"BE {100 * be_sticker(extra_of('2-Step Pro', 'od90', pro['BE'])) / pro['List']:.0f}% of list. "
        f"Rec 15% leftover ${leftover(sticker(pro['List'], 0.15), extra_of('2-Step Pro', 'od90', pro['BE'])):.0f}.",
        "",
        "Do not copy BG Instant 15% or FundedNext +5% for 90% + anytime. "
        "If Instant and evals must share one On Demand %, 25% is thin on Instant $100k combined.",
        "",
    ]
    MD.write_text("\n".join(lines))


if __name__ == "__main__":
    build()
