#!/usr/bin/env python3
"""Two PDFs on the 17 Aug card: (1) challenge + add-on leftover,
(2) prices, rules, and add-on %."""
from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

from write_addon_pct_pdf import (
    extra_of,
    flag,
    leftover,
    load_skus,
    rec_pct,
    sticker,
)
from write_price_rec_pdf import (
    H,
    MARGIN,
    NAVY,
    W,
    P,
    grid,
    styles as rec_styles,
    usd,
)
from write_book_310 import (
    addon_table,
    compute as book_310,
    family_table,
    pl_table,
    scale_table,
)
from write_simple_catalogs import RULES

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT_MARGINS = RESULTS / "Verodus_Margins_Pricing_Addons_2026-08-17.pdf"
OUT_MARGINS_SHOP = RESULTS / "verodus-margins-pricing-addons-2026-08-17.pdf"
OUT_CATALOG = RESULTS / "Verodus_Catalog_Rules_Addon_Pct_2026-08-17.pdf"
OUT_CATALOG_SHOP = RESULTS / "verodus-catalog-rules-addon-pct-2026-08-17.pdf"

PAGE = landscape(A4)


def money(x: float) -> str:
    if abs(x) < 0.5:
        return "$0"
    sign = "−" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct_s(p: float) -> str:
    return f"{p * 100:.0f}%"


def header(title: str, foot: str):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Bold", 8)
        canvas.drawString(MARGIN, H - 5.4 * mm, title)
        canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "17 Aug 2026")
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Times-Roman", 7.4)
        canvas.drawString(MARGIN, 2.6 * mm, foot)
        canvas.drawRightString(W - MARGIN, 2.6 * mm, str(doc.page))
        canvas.restoreState()
    return _draw


def write_pdf(path: Path, story, title: str, foot: str, shop: Path):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title=title,
        author="Verodus",
    )
    doc.build(story, onFirstPage=header(title, foot), onLaterPages=header(title, foot))
    shutil.copyfile(path, shop)
    print(f"Wrote {path} ({path.stat().st_size:,} bytes)")


def addon_pack(r):
    out = {}
    for key in ("weekend", "weekly", "od90"):
        extra = extra_of(r["Plan"], key, r["BE"])
        pct = rec_pct(r["Plan"], key)
        stick = sticker(r["List"], pct)
        add = leftover(stick, extra)
        out[key] = {
            "pct": pct, "sticker": stick, "extra": extra,
            "left": add, "comb": r["Chal"] + add,
        }
    return out


def build_margins():
    s = rec_styles()
    skus = load_skus()
    story = []

    book_chal = sum(r["N"] * r["Chal"] for r in skus)
    book_we = book_wk = book_od = 0.0
    packs = []
    for r in skus:
        p = addon_pack(r)
        packs.append((r, p))
        book_we += r["N"] * p["weekend"]["left"]
        book_wk += r["N"] * p["weekly"]["left"]
        book_od += r["N"] * p["od90"]["left"]

    _rows310, book, families, scales, rec_add, chk_add = book_310()

    story.append(P("Margins — 310-account book + add-on leftover", s["cover"]))
    story.append(P(
        f"{book['N']} accounts/mo on the Instant-heavy mix. "
        f"Challenge leftover {money(book['Left'])}/mo "
        f"({book['Left_pct'] * 100:.1f}% of {money(book['Rev'])} sale revenue) "
        "after payouts, 10% error, $1/account, CAD 10k wages, and 20% ads. "
        "Lite/Pro $25k+ sit under Ment / Alpha 6% and Hola / Alpha 10%. Doors unchanged.",
        s["sub"],
    ))

    story.append(P("1. Monthly P&L at 310", s["h1"]))
    story.append(P(
        "CAD 10,000 wages (~$7,200) are a fixed monthly cost, spread across 310 weighted accounts. "
        "They do not scale down if volume is 150. Instant BE is year-1. Eval BE includes the first-payout refund.",
        s["body"],
    ))
    story.append(pl_table(book, s))
    story.append(Spacer(1, 3 * mm))
    story.append(family_table(families, book, s))
    story.append(P(
        "1-Step carries most leftover. Instant is thinner because year-1 BE is the whole fee job. "
        "Lite $5k is about $0 after allocated wages — keep the Hola/TFT street door.",
        s["tiny"],
    ))
    story.append(P("1b. Same mix at 150 / 310 / 600", s["h1"]))
    story.append(scale_table(scales, s))

    story.append(PageBreak())
    story.append(P("2. Challenge leftover by SKU", s["h1"]))
    story.append(P(
        "Leftover = sale × 0.80 − (BE + 10% error + $1 + wage share). "
        "Instant BE is year-1 E[X]. Eval BE is first-payout E[X] / (1 − P(pay)). "
        "CAD 10,000/mo wages (~$7,200) sit in this stack, not on the add-on.",
        s["body"],
    ))
    heads = ["Plan", "Size", "N/mo", "BE", "Opex floor", "Sale", "List",
             "Challenge leftover", "Book leftover"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(skus, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(str(r["N"]), s["td"]), P(usd(r["BE"]), s["td"]),
            P(usd(r["S_opex"]), s["td"]), P(usd(r["Sale"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(money(r["Chal"]), s["td"]),
            P(money(r["N"] * r["Chal"]), s["td"]),
        ])
    story.append(grid(data, [
        28 * mm, 18 * mm, 14 * mm, 18 * mm, 22 * mm, 18 * mm, 18 * mm, 32 * mm, 28 * mm,
    ], spec))
    lite100 = next(r["Chal"] for r in skus if r["Plan"] == "2-Step Lite" and r["Size"] == 100000)
    pro100 = next(r["Chal"] for r in skus if r["Plan"] == "2-Step Pro" and r["Size"] == 100000)
    story.append(P(
        f"Book challenge leftover {money(book_chal)}/mo. Lite $5k is about $0 after allocated wages. "
        f"Lite $100k leftover {money(lite100)} (was $15). Pro $100k leftover {money(pro100)} (was $36).",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("3. Add-on leftover at the rec % (per buyer, not attach)", s["h1"]))
    story.append(P(
        "Addon leftover = round(list × %) × 0.52 − extra E[X]. Prints if leftover ≥ −$1. "
        "Weekend Instant extra 8% of BE · eval 4%. Weekly speed Instant 8% · eval 5%. "
        "On Demand 90% Instant 41% · eval 12.5%. Combined = challenge leftover + addon leftover.",
        s["body"],
    ))
    heads = ["Plan", "Size", "Chal",
             "WE 12% $", "WE left", "WE comb",
             "Wk 8% $", "Wk left", "Wk comb",
             "OD %", "OD $", "OD left", "OD comb"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (r, p) in enumerate(packs, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        we, wk, od = p["weekend"], p["weekly"], p["od90"]
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(money(r["Chal"]), s["td"]),
            P(usd(we["sticker"]), s["td"]), P(money(we["left"]), s["td"]),
            P(money(we["comb"]), s["td"]),
            P(usd(wk["sticker"]), s["td"]), P(money(wk["left"]), s["td"]),
            P(money(wk["comb"]), s["td"]),
            P(pct_s(od["pct"]), s["td"]), P(usd(od["sticker"]), s["td"]),
            P(f"{money(od['left'])} {flag(od['left'])}", s["td"]),
            P(f"{money(od['comb'])} {flag(od['comb'])}", s["td"]),
        ])
    story.append(grid(data, [
        24 * mm, 16 * mm, 16 * mm,
        16 * mm, 16 * mm, 18 * mm,
        16 * mm, 16 * mm, 18 * mm,
        14 * mm, 16 * mm, 22 * mm, 20 * mm,
    ], spec))
    story.append(P(
        f"If every account bought Weekend, extra leftover {money(book_we)}/mo. "
        f"Weekly {money(book_wk)}/mo. On Demand {money(book_od)}/mo. "
        "Those are not attach-weighted — they are unit leftover × monthly N. "
        "Instant On Demand 32% is the year-1 floor. 20% Instant $100k still does not print.",
        s["tiny"],
    ))

    story.append(P("3b. Add-ons attach-weighted on the 310 mix", s["h1"]))
    story.append(P(
        "News attach = 0. Weekend / Weekly / On Demand attach is the early-book mix, not 100% of N. "
        "Rec card 12% / 8% / 15–32% vs checkout 15% / 6% / 20%.",
        s["body"],
    ))
    story.append(addon_table(rec_add, chk_add, s))
    story.append(P(
        f"Blended leftover at rec add-on %: {money(book['Left'] + rec_add[2])}/mo. "
        f"At checkout 15/6/20: {money(book['Left'] + chk_add[2])}/mo.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("4. $100k unit snapshot", s["h1"]))
    heads = ["Plan", "Sale", "Chal left", "WE left", "Wk left", "OD left",
             "WE comb", "Wk comb", "OD comb"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 1
    for r, p in packs:
        if r["Size"] != 100000:
            continue
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Sale"]), s["td"]),
            P(money(r["Chal"]), s["td"]),
            P(money(p["weekend"]["left"]), s["td"]),
            P(money(p["weekly"]["left"]), s["td"]),
            P(money(p["od90"]["left"]), s["td"]),
            P(money(p["weekend"]["comb"]), s["td"]),
            P(money(p["weekly"]["comb"]), s["td"]),
            P(money(p["od90"]["comb"]), s["td"]),
        ])
        i += 1
    story.append(grid(data, [
        32 * mm, 20 * mm, 22 * mm, 20 * mm, 20 * mm, 20 * mm, 22 * mm, 22 * mm, 22 * mm,
    ], spec))
    story.append(P(
        "Green = Instant. Blue = evals. Every $100k add-on at the rec % prints on its own "
        "and combined stays green. Lite/Pro leftover stepped up with the $25k+ reprice.",
        s["tiny"],
    ))

    write_pdf(
        OUT_MARGINS, story,
        "VERODUS  ·  Margins  ·  new prices + add-ons",
        "Challenge leftover = sale×0.80 − opex stack. Addon leftover = sticker×0.52 − extra E[X].",
        OUT_MARGINS_SHOP,
    )


def build_catalog():
    s = rec_styles()
    skus = load_skus()
    story = []

    story.append(P("Catalog — prices, rules, add-on %", s["cover"]))
    story.append(P(
        "VERO35 sale and list in separate rows. Same percentage rules on every size in a plan. "
        "News trading is included. Default reward is Bi-Weekly 80%, min $100.",
        s["sub"],
    ))

    story.append(P("1. Challenge prices", s["h1"]))
    heads = ["Plan", "Price", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    sizes = (5000, 10000, 25000, 50000, 100000, 200000)
    by = {}
    for r in skus:
        by[(r["Plan"], r["Size"])] = r
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    i = 0
    for plan in ("Instant", "1-Step", "2-Step Lite", "2-Step Pro"):
        for kind, field in (("Sale", "Sale"), ("List", "List")):
            i += 1
            spec[i] = "rec" if plan == "Instant" else "live"
            cells = [P(plan, s["tdl"]), P(kind, s["td"])]
            for sz in sizes:
                r = by.get((plan, sz))
                if r is None:
                    cells.append(P("—", s["td"]))
                else:
                    cells.append(P(usd(r[field]), s["td"]))
            data.append(cells)
    story.append(grid(data, [
        32 * mm, 18 * mm, 28 * mm, 28 * mm, 28 * mm, 28 * mm, 30 * mm, 30 * mm,
    ], spec))
    story.append(P(
        "Door: Instant from $49 · 1-Step from $45 · Lite from $39 · Pro from $45. "
        "Lite $25k+ under Ment / Alpha 6%. Pro $25k+ under Hola / Alpha 10% / BG. "
        "Shopper pays the sale. List is checkout basePrice.",
        s["tiny"],
    ))

    story.append(P("2. Rules", s["h1"]))
    heads = ["Plan", "Stage", "Target", "Min days", "Consistency",
             "Daily DD", "Max DD", "Max drawdown basis"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(RULES, start=1):
        spec[i] = "rec" if row[0] == "Instant Funding" else "live"
        data.append([P(c, s["tdl"] if j < 2 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [
        32 * mm, 30 * mm, 28 * mm, 22 * mm, 28 * mm, 20 * mm, 20 * mm, 48 * mm,
    ], spec))
    story.append(P(
        "News trading is permitted on every phase and funded account. Instant trail never locks. "
        "Instant is not refundable. Evals refund the challenge fee only on first payout "
        "(add-ons are not refunded). Weekend flatten Friday 22:00 UTC unless Weekend is paid.",
        s["tiny"],
    ))

    story.append(PageBreak())
    story.append(P("3. Add-on % to charge", s["h1"]))
    heads = ["Add-on", "Instant", "1-Step / Lite / Pro", "What it is"]
    data = [[P(h, s["th"]) for h in heads]]
    menu = (
        ("News trading", "included", "included", "Allowed on eval and funded. No SKU."),
        ("Weekend Holding", "12%", "12%", "Friday 22:00 flatten off."),
        ("Weekly Rewards with 70% Reward Split", "8%", "8%",
         "Every 7 calendar days. Default is Bi-Weekly 80%. Min $100."),
        ("On Demand Rewards with 90% Split", "32%", "15%",
         "Anytime after Instant 5 valid days or eval 3 funded days. Min $100."),
        ("Bi-Weekly 80%", "included", "included", "Default. Every 14 calendar days. Min $100."),
        ("Swing", "not offered", "not offered", "News is already in the fee."),
    )
    spec = {}
    for i, row in enumerate(menu, start=1):
        if row[0] in ("Weekend Holding", "Weekly Rewards with 70% Reward Split",
                      "On Demand Rewards with 90% Split"):
            spec[i] = "rec"
        elif row[0] in ("News trading", "Swing"):
            spec[i] = "live"
        data.append([P(c, s["tdl"] if j in (0, 3) else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [62 * mm, 28 * mm, 38 * mm, 100 * mm], spec))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Sticker = round(list × %). VERO35 takes 35% off list + stickers. "
        "Instant On Demand 32% is the year-1 print floor. Evals 15% matches Blue Guardian’s 90% add-on. "
        "Do not copy BG Instant 15% or FundedNext +5% for 90% + anytime.",
        s["tiny"],
    ))

    story.append(P("4. Stickers per challenge (before VERO35)", s["h1"]))
    heads = ["Plan", "Size", "List", "Weekend 12%", "Weekly 8%", "On Demand"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(skus, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        we = sticker(r["List"], rec_pct(r["Plan"], "weekend"))
        wk = sticker(r["List"], rec_pct(r["Plan"], "weekly"))
        od = sticker(r["List"], rec_pct(r["Plan"], "od90"))
        od_lab = f"{usd(od)} ({pct_s(rec_pct(r['Plan'], 'od90'))})"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["List"]), s["td"]),
            P(usd(we), s["td"]), P(usd(wk), s["td"]), P(od_lab, s["td"]),
        ])
    story.append(grid(data, [
        32 * mm, 22 * mm, 22 * mm, 32 * mm, 32 * mm, 40 * mm,
    ], spec))
    story.append(P(
        "Instant $100k list $675: weekend $81 · weekly $54 · On Demand 90% $216. "
        "Pro $100k list $537: weekend $64 · weekly $43 · On Demand 90% $81. "
        "Shopper pays 65% of each sticker after VERO35.",
        s["tiny"],
    ))

    write_pdf(
        OUT_CATALOG, story,
        "VERODUS  ·  Catalog  ·  prices, rules, add-on %",
        "Sale and list in separate rows. News included. Weekend 12% · Weekly 70% 8% · On Demand 90% 15% evals / 32% Instant.",
        OUT_CATALOG_SHOP,
    )


def main():
    RESULTS.mkdir(exist_ok=True)
    from write_book_310 import main as write_book
    write_book()
    build_margins()
    build_catalog()


if __name__ == "__main__":
    main()
