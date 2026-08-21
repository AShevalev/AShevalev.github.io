#!/usr/bin/env python3
"""Classic BE / 20% / 40% / 60% / Sale m on the new rec prices and add-on %."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

from industry_book import margin_price
from write_addon_catalog import PLAN_LABEL, plan_pct, sticker
from write_addon_pct_pdf import extra_of
from write_price_rec_pdf import (
    ANCHORS,
    H,
    MARGIN,
    NAVY,
    SIZES,
    W,
    P,
    grid,
    rec_list,
    styles as rec_styles,
    usd,
)
from write_reprice_pdf import REC as SALE

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")
OUT = RESULTS / "Verodus_BE_20_40_60_Margins_2026-08-17.pdf"
OUT_SHOP = RESULTS / "verodus-be-20-40-60-margins-2026-08-17.pdf"
OUT_CSV = RESULTS / "verodus_be_20_40_60_margins.csv"
MD = RESULTS / "BE_20_40_60_MARGINS.md"
PAGE = landscape(A4)

ADDONS = (
    ("weekend", "Weekend Holding"),
    ("weekly", "Weekly 70%"),
    ("od90", "On Demand 90%"),
)


def money_m(sale: float, cost: float) -> str:
    if sale is None or sale <= 0:
        return "—"
    return f"{100.0 * (sale - cost) / sale:+.0f}%"


def load_be():
    out = {}
    with (RESULTS / "verodus_news_included_prices.csv").open() as f:
        for r in csv.DictReader(f):
            out[(r["Plan"], int(float(r["Size"])))] = {
                "be": float(r["BE_on"]),
                "e": float(r["E_on"]),
                "p_pay": float(r["P_pay_on"]),
                "basis": r["Basis"],
            }
    return out


def challenge_rows():
    be_map = load_be()
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            k = (plan, sz)
            if k not in SALE:
                continue
            meta = be_map[k]
            sale = float(SALE[k])
            be = meta["be"]
            if plan == "Instant":
                cost = meta["e"]
            else:
                cost = meta["e"] + meta["p_pay"] * sale
            rows.append({
                "kind": "challenge",
                "Plan": plan,
                "Label": PLAN_LABEL[plan],
                "Size": sz,
                "Addon": "Challenge",
                "Pct": "",
                "Sticker": sale,
                "List": rec_list(sale),
                "Sale": sale,
                "E": meta["e"],
                "P_pay": meta["p_pay"],
                "BE": be,
                "px_20": margin_price(be, 0.20),
                "px_40": margin_price(be, 0.40),
                "px_60": margin_price(be, 0.60),
                "Cost": cost,
                "Sale_m": (sale - cost) / sale,
            })
    return rows


def addon_rows():
    be_map = load_be()
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            k = (plan, sz)
            if k not in SALE:
                continue
            sale = float(SALE[k])
            list_px = rec_list(sale)
            be_chal = be_map[k]["be"]
            for key, name in ADDONS:
                pct = plan_pct(plan, key)
                stick = sticker(list_px, pct)
                net = stick * 0.65
                extra = extra_of(plan, key, be_chal)
                be = extra
                rows.append({
                    "kind": "addon",
                    "Plan": plan,
                    "Label": PLAN_LABEL[plan],
                    "Size": sz,
                    "Addon": name,
                    "Pct": pct,
                    "Sticker": stick,
                    "List": list_px,
                    "Sale": net,
                    "E": extra,
                    "P_pay": 0.0,
                    "BE": be,
                    "px_20": margin_price(be, 0.20),
                    "px_40": margin_price(be, 0.40),
                    "px_60": margin_price(be, 0.60),
                    "Cost": extra,
                    "Sale_m": (net - extra) / net if net else 0.0,
                })
    return rows


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


def write_pdf(story):
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus BE 20 40 60 margins",
        author="Verodus",
    )
    foot = (
        "Challenge: Instant year-1 · eval first-payout + refund in Sale m. "
        "Addon: BE = extra E[X], no refund. 20/40/60 = BE ÷ (1 − m). Sale m = (sale − cost) / sale."
    )
    doc.build(
        story,
        onFirstPage=header("VERODUS  ·  BE  ·  20%  ·  40%  ·  60%  ·  Sale m", foot),
        onLaterPages=header("VERODUS  ·  BE  ·  20%  ·  40%  ·  60%  ·  Sale m", foot),
    )
    shutil.copyfile(OUT, OUT_SHOP)
    if ART.is_dir():
        shutil.copyfile(OUT, ART / OUT.name)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


def challenge_table(rows, s):
    heads = ["Plan", "Size", "List", "Sale", "E[X]", "P(pay)",
             "BE", "20%", "40%", "60%", "Sale m"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Label"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(usd(r["List"]), s["td"]), P(usd(r["Sale"]), s["td"]),
            P(usd(r["E"]), s["td"]),
            P(f"{100 * r['P_pay']:.1f}%", s["td"]),
            P(usd(r["BE"]), s["td"]),
            P(usd(r["px_20"]), s["td"]),
            P(usd(r["px_40"]), s["td"]),
            P(usd(r["px_60"]), s["td"]),
            P(money_m(r["Sale"], r["Cost"]), s["td"]),
        ])
    return grid(data, [
        28 * mm, 18 * mm, 16 * mm, 16 * mm, 16 * mm, 16 * mm,
        16 * mm, 16 * mm, 16 * mm, 16 * mm, 16 * mm,
    ], spec)


def addon_table(rows, s):
    heads = ["Plan", "Size", "Add-on", "%", "Sticker", "Sale",
             "BE", "20%", "40%", "60%", "Sale m"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(rows, start=1):
        spec[i] = "rec" if r["Plan"] == "Instant" else "live"
        data.append([
            P(r["Label"], s["tdl"]), P(usd(r["Size"]), s["td"]),
            P(r["Addon"], s["tdl"]),
            P(f"{100 * r['Pct']:.0f}%", s["td"]),
            P(usd(r["Sticker"]), s["td"]),
            P(usd(r["Sale"]), s["td"]),
            P(usd(r["BE"]), s["td"]),
            P(usd(r["px_20"]), s["td"]),
            P(usd(r["px_40"]), s["td"]),
            P(usd(r["px_60"]), s["td"]),
            P(money_m(r["Sale"], r["Cost"]), s["td"]),
        ])
    return grid(data, [
        26 * mm, 16 * mm, 32 * mm, 12 * mm, 16 * mm, 16 * mm,
        16 * mm, 16 * mm, 16 * mm, 16 * mm, 16 * mm,
    ], spec)


def write_csv(chal, addons):
    with OUT_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "Kind", "Plan", "Size", "Addon", "Pct", "List", "Sticker", "Sale",
            "E", "P_pay", "BE", "px_20", "px_40", "px_60", "Cost", "Sale_m",
        ])
        for r in chal + addons:
            w.writerow([
                r["kind"], r["Plan"], r["Size"], r["Addon"],
                "" if r["Pct"] == "" else f"{r['Pct']:.4f}",
                f"{r['List']:.0f}", f"{r['Sticker']:.2f}", f"{r['Sale']:.4f}",
                f"{r['E']:.6f}", f"{r['P_pay']:.6f}", f"{r['BE']:.6f}",
                f"{r['px_20']:.6f}", f"{r['px_40']:.6f}", f"{r['px_60']:.6f}",
                f"{r['Cost']:.6f}", f"{r['Sale_m']:.6f}",
            ])


def write_md(chal, addons):
    lines = [
        "# BE, 20%, 40%, 60%, Sale m — 17 Aug 2026",
        "",
        "New rec sale card. News included. Instant BE is year-1. Eval BE is first-payout. "
        "Eval Sale m uses E[X] + P(pay)×sale (fee refund). "
        "Add-on BE is extra E[X] vs Bi-Weekly 80%. Add-ons are not refunded. "
        "Sale on add-ons is sticker × 0.65 (VERO35). "
        "20/40/60 = BE ÷ (1 − 0.20/0.40/0.60). Sale m = (sale − cost) / sale.",
        "",
        "On Demand 90% is **32% Instant / 15% evals**. Weekend 15%. Weekly 70% 6%.",
        "",
        "## Challenges",
        "",
        "| Plan | Size | List | Sale | E[X] | P(pay) | BE | 20% | 40% | 60% | Sale m |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in chal:
        lines.append(
            f"| {r['Label']} | {usd(r['Size'])} | {usd(r['List'])} | {usd(r['Sale'])} | "
            f"{usd(r['E'])} | {100 * r['P_pay']:.1f}% | {usd(r['BE'])} | "
            f"{usd(r['px_20'])} | {usd(r['px_40'])} | {usd(r['px_60'])} | "
            f"{money_m(r['Sale'], r['Cost'])} |"
        )
    lines += [
        "",
        "## Add-ons",
        "",
        "| Plan | Size | Add-on | % | Sticker | Sale | BE | 20% | 40% | 60% | Sale m |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in addons:
        lines.append(
            f"| {r['Label']} | {usd(r['Size'])} | {r['Addon']} | {100 * r['Pct']:.0f}% | "
            f"{usd(r['Sticker'])} | {usd(r['Sale'])} | {usd(r['BE'])} | "
            f"{usd(r['px_20'])} | {usd(r['px_40'])} | {usd(r['px_60'])} | "
            f"{money_m(r['Sale'], r['Cost'])} |"
        )
    lines += [
        "",
        "PDF: `results/Verodus_BE_20_40_60_Margins_2026-08-17.pdf`",
        "",
    ]
    MD.write_text("\n".join(lines), encoding="utf-8")


def build():
    RESULTS.mkdir(exist_ok=True)
    s = rec_styles()
    chal = challenge_rows()
    addons = addon_rows()
    by_key = {key: [r for r in addons if r["Addon"] == name] for key, name in ADDONS}

    story = []
    story.append(P("Challenges — BE, 20%, 40%, 60%, Sale m", s["cover"]))
    story.append(P(
        "Sale is VERO35. List is checkout basePrice. Instant E[X] and BE are year-1. "
        "Eval BE is first-payout E[X] / (1 − P(pay)). Eval Sale m includes the fee refund. "
        "20/40/60 are sale prices that print that payout margin on BE.",
        s["sub"],
    ))
    story.append(challenge_table(chal, s))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Green = Instant. Blue = evals. Sale m is payout-only — it ignores ads, wages, and $1. "
        "Door: Instant from $49 · One-Step from $45 · Lite from $39 · Pro from $45.",
        s["tiny"],
    ))

    for i, (key, name) in enumerate(ADDONS):
        story.append(PageBreak())
        story.append(P(f"{name} — BE, 20%, 40%, 60%, Sale m", s["cover"]))
        story.append(P(
            "Sticker = round(list × %). Sale = sticker × 0.65 (VERO35). "
            "BE = extra E[X] vs Bi-Weekly 80%. Add-ons are not refunded. "
            "20/40/60 = BE ÷ (1 − m). Sale m = (sale − cost) / sale.",
            s["sub"],
        ))
        story.append(addon_table(by_key[key], s))
        story.append(Spacer(1, 2 * mm))
        if key == "od90":
            inst100 = next(
                r for r in addons
                if r["Plan"] == "Instant" and r["Size"] == 100000 and r["Addon"] == name
            )
            pro100 = next(
                r for r in addons
                if r["Plan"] == "2-Step Pro" and r["Size"] == 100000 and r["Addon"] == name
            )
            story.append(P(
                f"Instant $100k On Demand: sticker {usd(inst100['Sticker'])} · sale {usd(inst100['Sale'])} · "
                f"BE {usd(inst100['BE'])} · 20% {usd(inst100['px_20'])} · "
                f"Sale m {money_m(inst100['Sale'], inst100['Cost'])}. "
                f"Pro $100k On Demand: sticker {usd(pro100['Sticker'])} · sale {usd(pro100['Sale'])} · "
                f"BE {usd(pro100['BE'])} · Sale m {money_m(pro100['Sale'], pro100['Cost'])}.",
                s["tiny"],
            ))
        else:
            story.append(P(
                "Green = Instant. Blue = evals. Instant extra: weekend 8% of year-1 BE, weekly 8%. "
                "Eval extra: weekend 4%, weekly 5%. On Demand extra: Instant 41%, evals 12.5%.",
                s["tiny"],
            ))

    write_csv(chal, addons)
    write_md(chal, addons)
    write_pdf(story)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {MD}")


if __name__ == "__main__":
    build()
