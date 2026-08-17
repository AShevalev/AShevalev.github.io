#!/usr/bin/env python3
"""310-account monthly P&L on the news-included rec card.

CAD 10,000 wages (~$7,200) are a fixed monthly cost, spread across the
Instant-heavy 310 mix in write_price_rec_pdf.UNITS. Challenge leftover is
sale × 0.80 − (BE × 1.10 + $1 + wage share). Add-on leftover is
sticker × 0.52 − extra E[X], then attach-weighted.
"""
from __future__ import annotations

import csv
import shutil
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

from write_addon_pct_pdf import (
    NOW_PCT,
    REC_PCT,
    extra_of,
    leftover as addon_leftover,
    sticker,
)
from write_price_rec_pdf import (
    ACCOUNT_COST,
    ANCHORS,
    ASSUMPTION_ERR,
    ATTACH,
    H,
    MARGIN,
    MARKETING,
    NAVY,
    SIZES,
    UNITS,
    W,
    WAGES_USD,
    P,
    grid,
    leftover_after_opex,
    opex_stack,
    rec_list,
    styles as rec_styles,
    usd,
    wage_for,
)
from write_reprice_pdf import REC

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT_PDF = RESULTS / "Verodus_Book_310_2026-08-17.pdf"
OUT_SHOP = RESULTS / "verodus-book-310-2026-08-17.pdf"
OUT_CSV = RESULTS / "verodus_book_310.csv"
OUT_MD = RESULTS / "BOOK_310.md"
PAGE = landscape(A4)
N_BOOK = sum(UNITS.values())
SCALE_N = (150, 310, 600)

# News is included. Keep weekend / weekly / on-demand attach from the early book.
ATTACH_310 = {
    plan: {"weekend": a["weekend"], "weekly": a["weekly"], "od90": a["ondemand"]}
    for plan, a in ATTACH.items()
}

CHECKOUT_PCT = {
    "weekend": {"Instant": NOW_PCT["weekend"], "eval": NOW_PCT["weekend"]},
    "weekly": {"Instant": NOW_PCT["weekly"], "eval": NOW_PCT["weekly"]},
    "od90": {"Instant": NOW_PCT["od90"], "eval": NOW_PCT["od90"]},
}


def money(x: float) -> str:
    if abs(x) < 0.5:
        return "$0"
    sign = "−" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct_s(p: float) -> str:
    if p is None:
        return "—"
    sign = "−" if p < 0 else ""
    return f"{sign}{abs(p) * 100:.1f}%"


def js_round_sale_m(sale: float, cost: float) -> float:
    if sale <= 0:
        return 0.0
    return (sale - cost) / sale


def load_be():
    path = RESULTS / "verodus_news_included_prices.csv"
    out = {}
    with path.open() as f:
        for r in csv.DictReader(f):
            out[(r["Plan"], int(float(r["Size"])))] = {
                "be": float(r["BE_on"]),
                "e": float(r["E_on"]),
                "p_pay": float(r["P_pay_on"]),
                "p_yr1": float(r["P_yr1_on"]),
                "basis": r["Basis"],
            }
    return out


def sku_rows():
    be_map = load_be()
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            k = (plan, sz)
            if k not in UNITS:
                continue
            meta = be_map[k]
            sale = float(REC[k])
            n = int(UNITS[k])
            be = meta["be"]
            ox = opex_stack(be, plan, sz)
            left = leftover_after_opex(sale, ox["loaded"])
            if plan == "Instant":
                e_cost = meta["e"]
            else:
                e_cost = meta["e"] + meta["p_pay"] * sale
            rows.append({
                "Plan": plan,
                "Size": sz,
                "N": n,
                "Sale": sale,
                "List": rec_list(sale),
                "BE": be,
                "E": meta["e"],
                "P_pay": meta["p_pay"],
                "P_yr1": meta["p_yr1"],
                "Basis": meta["basis"],
                "Wage": ox["wage"],
                "Loaded": ox["loaded"],
                "S_opex": ox["s_opex"],
                "Left": left,
                "Book_left": n * left,
                "Rev": n * sale,
                "BE_cost": n * be,
                "Error": n * be * ASSUMPTION_ERR,
                "Acct": n * ACCOUNT_COST,
                "Wage_book": n * ox["wage"],
                "Ads": n * sale * MARKETING,
                "E_cost": e_cost,
                "Sale_m": js_round_sale_m(sale, e_cost),
                "Prints": left >= -1.0,
            })
    return rows


def book_from_rows(rows):
    n = sum(r["N"] for r in rows)
    rev = sum(r["Rev"] for r in rows)
    ads = sum(r["Ads"] for r in rows)
    be = sum(r["BE_cost"] for r in rows)
    err = sum(r["Error"] for r in rows)
    acct = sum(r["Acct"] for r in rows)
    wage = sum(r["Wage_book"] for r in rows)
    left = sum(r["Book_left"] for r in rows)
    contrib = left + wage  # after ads, BE, error, $1 — before wages
    return {
        "N": n,
        "Rev": rev,
        "Ads": ads,
        "BE": be,
        "Error": err,
        "Acct": acct,
        "Wage": wage,
        "Contrib": contrib,
        "Left": left,
        "Left_pct": left / rev if rev else 0.0,
        "Contrib_pct": contrib / rev if rev else 0.0,
        "Sale_m": 1.0 - (sum(r["N"] * r["E_cost"] for r in rows) / rev),
    }


def family_rows(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["Plan"]].append(r)
    out = []
    for plan, _fam in ANCHORS:
        grp = by[plan]
        b = book_from_rows(grp)
        b["Plan"] = plan
        out.append(b)
    return out


def scale_row(rows, n_book: int):
    """Same mix, wages stay CAD 10k. Units scale with n_book / 310."""
    k = n_book / float(N_BOOK)
    scaled = []
    for r in rows:
        n = r["N"] * k
        sale = r["Sale"]
        be = r["BE"]
        loaded_var = be * (1.0 + ASSUMPTION_ERR) + ACCOUNT_COST
        left_unit = sale * (1.0 - MARKETING) - loaded_var
        scaled.append({
            "N": n,
            "Rev": n * sale,
            "Ads": n * sale * MARKETING,
            "BE_cost": n * be,
            "Error": n * be * ASSUMPTION_ERR,
            "Acct": n * ACCOUNT_COST,
            "Book_left": n * left_unit,
            "E_cost": r["E_cost"],
            "Sale": sale,
        })
    b = {
        "N": n_book,
        "Rev": sum(r["Rev"] for r in scaled),
        "Ads": sum(r["Ads"] for r in scaled),
        "BE": sum(r["BE_cost"] for r in scaled),
        "Error": sum(r["Error"] for r in scaled),
        "Acct": sum(r["Acct"] for r in scaled),
        "Wage": WAGES_USD,
        "Contrib": sum(r["Book_left"] for r in scaled),
        "Left": sum(r["Book_left"] for r in scaled) - WAGES_USD,
    }
    b["Left_pct"] = b["Left"] / b["Rev"] if b["Rev"] else 0.0
    b["Contrib_pct"] = b["Contrib"] / b["Rev"] if b["Rev"] else 0.0
    return b


def addon_unit(r, key: str, table):
    band = "Instant" if r["Plan"] == "Instant" else "eval"
    pct = table[key][band]
    stick = sticker(r["List"], pct)
    extra = extra_of(r["Plan"], key, r["BE"])
    left = addon_leftover(stick, extra)
    attach = ATTACH_310[r["Plan"]][key]
    return {
        "pct": pct,
        "sticker": stick,
        "extra": extra,
        "left": left,
        "attach": attach,
        "e_left": attach * left,
        "book": r["N"] * attach * left,
        "e_rev": attach * stick * 0.65,
        "book_rev": r["N"] * attach * stick * 0.65,
    }


def addon_book(rows, table):
    keys = ("weekend", "weekly", "od90")
    by_key = {k: {"left": 0.0, "rev": 0.0} for k in keys}
    sku = []
    for r in rows:
        pack = {k: addon_unit(r, k, table) for k in keys}
        sku.append((r, pack))
        for k in keys:
            by_key[k]["left"] += pack[k]["book"]
            by_key[k]["rev"] += pack[k]["book_rev"]
    tot_left = sum(v["left"] for v in by_key.values())
    tot_rev = sum(v["rev"] for v in by_key.values())
    return sku, by_key, tot_left, tot_rev


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


def write_csv(rows, book, families, scales, rec_add, chk_add):
    with OUT_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "Plan", "Size", "N", "Sale", "List", "BE", "P_pay", "E_cost",
            "Sale_m", "Wage", "S_opex", "Left", "Book_left", "Prints",
        ])
        for r in rows:
            w.writerow([
                r["Plan"], r["Size"], r["N"], f"{r['Sale']:.0f}", f"{r['List']:.0f}",
                f"{r['BE']:.6f}", f"{r['P_pay']:.6f}", f"{r['E_cost']:.6f}",
                f"{r['Sale_m']:.6f}", f"{r['Wage']:.6f}", f"{r['S_opex']:.6f}",
                f"{r['Left']:.6f}", f"{r['Book_left']:.6f}", int(r["Prints"]),
            ])
        w.writerow([])
        w.writerow(["Book", "N", "Rev", "Ads", "BE", "Error", "Acct", "Wage",
                    "Contrib", "Left", "Left_pct"])
        w.writerow([
            "challenge", book["N"], f"{book['Rev']:.2f}", f"{book['Ads']:.2f}",
            f"{book['BE']:.2f}", f"{book['Error']:.2f}", f"{book['Acct']:.2f}",
            f"{book['Wage']:.2f}", f"{book['Contrib']:.2f}", f"{book['Left']:.2f}",
            f"{book['Left_pct']:.6f}",
        ])
        w.writerow([])
        w.writerow(["Family", "N", "Rev", "Left", "Left_pct"])
        for fam in families:
            w.writerow([
                fam["Plan"], fam["N"], f"{fam['Rev']:.2f}",
                f"{fam['Left']:.2f}", f"{fam['Left_pct']:.6f}",
            ])
        w.writerow([])
        w.writerow(["Scale_N", "Rev", "Wage", "Left", "Left_pct"])
        for sc in scales:
            w.writerow([
                sc["N"], f"{sc['Rev']:.2f}", f"{sc['Wage']:.2f}",
                f"{sc['Left']:.2f}", f"{sc['Left_pct']:.6f}",
            ])
        w.writerow([])
        w.writerow(["Addon_card", "Weekend_left", "Weekly_left", "OD_left", "Total_left"])
        for name, _sku, by_key, tot, _rev in (
            ("rec_12_8_15-32",) + rec_add,
            ("checkout_15_6_20",) + chk_add,
        ):
            w.writerow([
                name,
                f"{by_key['weekend']['left']:.2f}",
                f"{by_key['weekly']['left']:.2f}",
                f"{by_key['od90']['left']:.2f}",
                f"{tot:.2f}",
            ])


def write_md(rows, book, families, scales, rec_add, chk_add):
    mix = (
        ("Instant", sum(r["N"] for r in rows if r["Plan"] == "Instant")),
        ("1-Step", sum(r["N"] for r in rows if r["Plan"] == "1-Step")),
        ("2-Step Lite", sum(r["N"] for r in rows if r["Plan"] == "2-Step Lite")),
        ("2-Step Pro", sum(r["N"] for r in rows if r["Plan"] == "2-Step Pro")),
    )
    thin = [r for r in rows if r["Left"] < -1]
    near = [r for r in rows if -1 <= r["Left"] < 2]
    _sku, rec_by, rec_tot, rec_rev = rec_add
    _sku2, chk_by, chk_tot, chk_rev = chk_add
    lines = [
        "# Verodus 310-account book — 17 Aug 2026",
        "",
        "Same mix already in `write_price_rec_pdf.UNITS`. Instant-heavy, mid-size modal, few $200k. "
        "CAD 10,000/mo wages (~$7,200) are a **fixed** cost, not a per-SKU hurdle. "
        "News is included. Default reward is Bi-Weekly 80%, min $100. 8(h) is off.",
        "",
        f"Mix: Instant {mix[0][1]} · 1-Step {mix[1][1]} · Lite {mix[2][1]} · Pro {mix[3][1]} · **{N_BOOK}**.",
        "",
        "## Book P&L (challenge only, VERO35 sale)",
        "",
        "| Line | $/mo |",
        "|---|---:|",
        f"| Challenge revenue | {money(book['Rev'])} |",
        f"| Ads 20% | {money(-book['Ads'])} |",
        f"| Payout BE (Instant year-1 / eval first-payout + refund) | {money(-book['BE'])} |",
        f"| 10% assumption error on BE | {money(-book['Error'])} |",
        f"| $1 per account | {money(-book['Acct'])} |",
        f"| Wages CAD 10,000 × 0.72 | {money(-book['Wage'])} |",
        f"| **Leftover after opex** | **{money(book['Left'])}** |",
        "",
        f"Leftover is **{pct_s(book['Left_pct'])}** of challenge revenue. "
        f"Contribution before wages is {money(book['Contrib'])} ({pct_s(book['Contrib_pct'])}). "
        f"Payout-only sale margin (ignores ads/wages/$1/error) is {pct_s(book['Sale_m'])} — do not run the desk on that number.",
        "",
        "## Family roll-up at 310",
        "",
        "| Plan | N | Revenue | Leftover | of revenue |",
        "|---|---:|---:|---:|---:|",
    ]
    for fam in families:
        lines.append(
            f"| {fam['Plan']} | {fam['N']} | {money(fam['Rev'])} | "
            f"{money(fam['Left'])} | {pct_s(fam['Left_pct'])} |"
        )
    lines += [
        f"| **Book** | **{book['N']}** | **{money(book['Rev'])}** | "
        f"**{money(book['Left'])}** | **{pct_s(book['Left_pct'])}** |",
        "",
        "## Same mix at 150 / 310 / 600",
        "",
        "Wages stay $7,200. Per-account wage falls as volume rises.",
        "",
        "| Accounts | Revenue | Leftover | of revenue |",
        "|---:|---:|---:|---:|",
    ]
    for sc in scales:
        mark = " ← this book" if sc["N"] == N_BOOK else ""
        lines.append(
            f"| {sc['N']}{mark} | {money(sc['Rev'])} | {money(sc['Left'])} | {pct_s(sc['Left_pct'])} |"
        )
    lines += [
        "",
        "## Per SKU at 310",
        "",
        "Leftover = sale × 0.80 − (BE × 1.10 + $1 + wage share). "
        "Sale m is payout-only (sale − E[cost]) / sale.",
        "",
        "| Plan | Size | N | Sale | List | BE | Opex floor | Sale m | Left / unit | Book left |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['Plan']} | {usd(r['Size'])} | {r['N']} | {usd(r['Sale'])} | "
            f"{usd(r['List'])} | {usd(r['BE'])} | {usd(r['S_opex'])} | "
            f"{pct_s(r['Sale_m'])} | {money(r['Left'])} | {money(r['Book_left'])} |"
        )
    lines.append(
        f"| **Book** | — | **{book['N']}** | — | — | {usd(book['BE'])} | — | "
        f"{pct_s(book['Sale_m'])} | — | **{money(book['Left'])}** |"
    )
    if thin:
        bits = ", ".join(f"{r['Plan']} {usd(r['Size'])} {money(r['Left'])}" for r in thin)
        lines += ["", f"Does not print (leftover < −$1): {bits}."]
    else:
        lines += ["", "No SKU is more than $1 under the opex floor."]
    if near:
        bits = ", ".join(f"{r['Plan']} {usd(r['Size'])} {money(r['Left'])}" for r in near)
        lines += [f"Thin (under $2 leftover): {bits}. Leave the street doors; the book still prints."]
    lines += [
        "",
        "## Add-ons on the 310 mix (attach-weighted)",
        "",
        "News attach is 0 (included). Weekend / Weekly / On Demand attach is the early-book mix "
        "(Instant 10% / 8% / 18%, 1-Step 16% / 10% / 12%, Lite 12% / 7% / 8%, Pro 20% / 12% / 16%). "
        "Not a sales forecast.",
        "",
        "| Card | Weekend | Weekly 70% | On Demand 90% | Extra leftover | Extra net $ |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Rec 12% / 8% / 15–32% | {money(rec_by['weekend']['left'])} | "
        f"{money(rec_by['weekly']['left'])} | {money(rec_by['od90']['left'])} | "
        f"**{money(rec_tot)}** | {money(rec_rev)} |",
        f"| Checkout 15% / 6% / 20% | {money(chk_by['weekend']['left'])} | "
        f"{money(chk_by['weekly']['left'])} | {money(chk_by['od90']['left'])} | "
        f"**{money(chk_tot)}** | {money(chk_rev)} |",
        "",
        f"Challenge leftover {money(book['Left'])} plus rec add-on leftover {money(rec_tot)} "
        f"= **{money(book['Left'] + rec_tot)}**/mo blended. "
        f"Checkout 15/6/20 blended **{money(book['Left'] + chk_tot)}**/mo. "
        "Instant $100k On Demand at checkout 20% still does not print on that SKU; "
        "attach-weighted book leftover can stay positive because smaller Instant doors do.",
        "",
        "PDF: `results/Verodus_Book_310_2026-08-17.pdf`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def pl_table(book, s):
    heads = ["Line", "$ / month"]
    data = [[P(h, s["th"]) for h in heads]]
    rows = (
        ("Challenge revenue (VERO35 sale)", book["Rev"], False),
        ("Ads 20%", -book["Ads"], False),
        ("Payout BE", -book["BE"], False),
        ("10% error on BE", -book["Error"], False),
        ("$1 per account", -book["Acct"], False),
        ("Wages CAD 10,000 × 0.72", -book["Wage"], False),
        ("Leftover after opex", book["Left"], True),
    )
    spec = {}
    for i, (lab, val, rec) in enumerate(rows, start=1):
        if rec:
            spec[i] = "rec"
        data.append([P(lab, s["tdl"]), P(money(val), s["td"])])
    return grid(data, [90 * mm, 40 * mm], spec)


def family_table(families, book, s):
    heads = ["Plan", "N", "Revenue", "Leftover", "of revenue"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, fam in enumerate(families, start=1):
        spec[i] = "rec" if fam["Plan"] == "Instant" else "live"
        data.append([
            P(fam["Plan"], s["tdl"]), P(str(fam["N"]), s["td"]),
            P(money(fam["Rev"]), s["td"]), P(money(fam["Left"]), s["td"]),
            P(pct_s(fam["Left_pct"]), s["td"]),
        ])
    data.append([
        P("Book", s["tdl"]), P(str(book["N"]), s["td"]),
        P(money(book["Rev"]), s["td"]), P(money(book["Left"]), s["td"]),
        P(pct_s(book["Left_pct"]), s["td"]),
    ])
    return grid(data, [36 * mm, 18 * mm, 32 * mm, 32 * mm, 28 * mm], spec)


def scale_table(scales, s):
    heads = ["Accounts / mo", "Revenue", "Wages", "Leftover", "of revenue"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, sc in enumerate(scales, start=1):
        spec[i] = "rec" if sc["N"] == N_BOOK else "live"
        data.append([
            P(str(sc["N"]), s["td"]), P(money(sc["Rev"]), s["td"]),
            P(money(sc["Wage"]), s["td"]), P(money(sc["Left"]), s["td"]),
            P(pct_s(sc["Left_pct"]), s["td"]),
        ])
    return grid(data, [36 * mm, 32 * mm, 28 * mm, 32 * mm, 28 * mm], spec)


def sku_table(rows, book, s):
    heads = ["Plan", "Size", "N", "Sale", "BE", "Opex floor",
             "Sale m", "Left / unit", "Book left"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Plan"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(str(r["N"]), s["td"]), P(usd(r["Sale"]), s["td"]),
            P(usd(r["BE"]), s["td"]), P(usd(r["S_opex"]), s["td"]),
            P(pct_s(r["Sale_m"]), s["td"]),
            P(money(r["Left"]), s["td"]), P(money(r["Book_left"]), s["td"]),
        ])
    data.append([
        P("Book", s["tdl"]), P("—", s["td"]), P(str(book["N"]), s["td"]),
        P("—", s["td"]), P(usd(book["BE"]), s["td"]), P("—", s["td"]),
        P(pct_s(book["Sale_m"]), s["td"]), P("—", s["td"]),
        P(money(book["Left"]), s["td"]),
    ])
    return grid(data, [
        28 * mm, 18 * mm, 12 * mm, 16 * mm, 16 * mm, 22 * mm, 18 * mm, 22 * mm, 24 * mm,
    ], spec)


def addon_table(rec_add, chk_add, s):
    heads = ["Card", "Weekend", "Weekly 70%", "On Demand 90%", "Extra leftover"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {1: "rec", 2: "live"}
    labels = (
        ("Rec 12% / 8% / 15–32%", rec_add[1], rec_add[2]),
        ("Checkout 15% / 6% / 20%", chk_add[1], chk_add[2]),
    )
    for lab, by_key, tot in labels:
        data.append([
            P(lab, s["tdl"]),
            P(money(by_key["weekend"]["left"]), s["td"]),
            P(money(by_key["weekly"]["left"]), s["td"]),
            P(money(by_key["od90"]["left"]), s["td"]),
            P(money(tot), s["td"]),
        ])
    return grid(data, [50 * mm, 28 * mm, 32 * mm, 36 * mm, 32 * mm], spec)


def build_story(rows, book, families, scales, rec_add, chk_add):
    s = rec_styles()
    story = []
    story.append(P("310-account book — leftover after opex", s["cover"]))
    story.append(P(
        f"Instant {sum(r['N'] for r in rows if r['Plan']=='Instant')} · "
        f"1-Step {sum(r['N'] for r in rows if r['Plan']=='1-Step')} · "
        f"Lite {sum(r['N'] for r in rows if r['Plan']=='2-Step Lite')} · "
        f"Pro {sum(r['N'] for r in rows if r['Plan']=='2-Step Pro')} · "
        f"{N_BOOK} accounts. CAD 10,000 wages (~$7,200) are fixed. "
        f"Day rules: Instant 20% Best Day on a green day of at least 0.5% of SOD "
        f"(five counted days implied, not listed); "
        f"1-Step QPP no min days + 50% Best Day; 2-Step 5 eval / 3 QPP. "
        f"Challenge leftover {money(book['Left'])}/mo "
        f"({pct_s(book['Left_pct'])} of {money(book['Rev'])} sale revenue).",
        s["sub"],
    ))
    story.append(P("1. Monthly P&L at 310", s["h1"]))
    story.append(P(
        "Leftover = sale × 0.80 − (BE × 1.10 + $1 + wage). Instant BE is year-1 E[X]. "
        "Eval BE is first-payout E[X] / (1 − P(pay)), so the fee refund sits in BE. "
        "Sale m in the SKU table ignores ads, wages, $1, and the 10% error — do not run on it.",
        s["body"],
    ))
    story.append(pl_table(book, s))
    story.append(Spacer(1, 3 * mm))
    story.append(family_table(families, book, s))
    step_p = next(r["P_pay"] for r in rows if r["Plan"] == "1-Step")
    inst_100 = next(
        r for r in rows if r["Plan"] == "Instant" and r["Size"] == 100000
    )
    story.append(P(
        f"1-Step still carries most leftover (P(pay) {100 * step_p:.1f}%) and the "
        f"$25k–$100k doors sit above the opex floor. Instant leftover is thinner: "
        f"year-1 BE is the whole fee job. Instant $100k leftover is "
        f"{money(inst_100['Left'])} after the Best Day day-count change. "
        f"Lite $5k is about $0 after allocated wages — keep the Hola/TFT street door.",
        s["tiny"],
    ))

    story.append(P("2. Volume — wages do not scale", s["h1"]))
    story.append(P(
        "Same mix. Wages stay $7,200. At 150 accounts leftover compresses; at 600 it fattens. "
        "Do not price as if 310 is a forecast — it is the wage-allocation book.",
        s["body"],
    ))
    story.append(scale_table(scales, s))

    story.append(PageBreak())
    story.append(P("3. Per SKU at 310", s["h1"]))
    story.append(sku_table(rows, book, s))
    under = [
        f"{r['Plan']} ${r['Size'] // 1000}k {money(r['Left'])}"
        for r in rows if r["Left"] is not None and r["Left"] < -1
    ]
    under_s = (
        "Does not print: " + "; ".join(under) + "."
        if under else
        "No row is more than $1 under the floor."
    )
    story.append(P(
        f"Green = Instant. Blue = evals. {under_s} "
        "Lite $5k leftover is about $0; Pro $5k/$10k and Instant $5k/$10k are the next thinnest.",
        s["tiny"],
    ))

    story.append(P("4. Add-ons, attach-weighted", s["h1"]))
    story.append(P(
        "News attach = 0. Weekend / Weekly / On Demand attach is the early-book mix "
        "(not 100% of N). Rec card is Weekend 12%, Weekly 70% 8%, On Demand 90% 15% evals / 32% Instant. "
        "Checkout still bills 15% / 6% / 20%.",
        s["body"],
    ))
    story.append(addon_table(rec_add, chk_add, s))
    rec_tot = rec_add[2]
    chk_tot = chk_add[2]
    story.append(P(
        f"Blended leftover at rec add-on %: {money(book['Left'] + rec_tot)}/mo. "
        f"At checkout 15/6/20: {money(book['Left'] + chk_tot)}/mo. "
        "Instant $100k On Demand at 20% still does not print as a unit; the mix can.",
        s["tiny"],
    ))
    return story


def write_pdf(story):
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus 310-account book",
        author="Verodus",
    )
    foot = "310 mix. Leftover = sale×0.80 − (BE×1.10 + $1 + wage). Wages CAD 10k × 0.72."
    doc.build(
        story,
        onFirstPage=header("VERODUS  ·  310-account book  ·  leftover after opex", foot),
        onLaterPages=header("VERODUS  ·  310-account book  ·  leftover after opex", foot),
    )
    shutil.copyfile(OUT_PDF, OUT_SHOP)
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size:,} bytes)")


def compute():
    rows = sku_rows()
    book = book_from_rows(rows)
    wage_sum = sum(r["Wage_book"] for r in rows)
    if abs(wage_sum - WAGES_USD) > 0.05:
        raise SystemExit(f"wage book {wage_sum} != {WAGES_USD}")
    families = family_rows(rows)
    scales = [scale_row(rows, n) for n in SCALE_N]
    rec_add = addon_book(rows, REC_PCT)
    chk_add = addon_book(rows, CHECKOUT_PCT)
    return rows, book, families, scales, rec_add, chk_add


def main():
    RESULTS.mkdir(exist_ok=True)
    rows, book, families, scales, rec_add, chk_add = compute()
    assert book["N"] == N_BOOK == 310, (book["N"], N_BOOK)
    write_csv(rows, book, families, scales, rec_add, chk_add)
    write_md(rows, book, families, scales, rec_add, chk_add)
    write_pdf(build_story(rows, book, families, scales, rec_add, chk_add))
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(
        f"Book {book['N']} rev {book['Rev']:.0f} leftover {book['Left']:.0f} "
        f"({100 * book['Left_pct']:.1f}%)"
    )


if __name__ == "__main__":
    main()
