#!/usr/bin/env python3
"""One confirmed PDF: summary, then rank tables, industry tables, rec tables.

All Instant money numbers use year-1. Columns are 20 / 40 / 60. Instant rec is the 30% print.
Recommended sale is the current card, not the old $1,094 Instant path.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

from write_comprehensive_pdf import STREET, UNIQUE, weighted_fail_mix
from write_price_rec_pdf import (
    ANCHORS,
    H,
    MARGIN as REC_MARGIN,
    NAVY,
    REC,
    SIZES,
    W,
    P,
    classic_table,
    collect_story as rec_collect,
    opex_table,
    family_peers,
    grid,
    plan_be,
    pricing_for,
    rec_be_cell,
    styles,
    usd,
)
from write_rank_report import collect_story as rank_collect

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_Confirmed_Book_2026-08-16.pdf"

PAGE = landscape(A4)
MARGIN = 11 * mm


def pct(x, signed=False, digits=1):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    v = 100.0 * float(x)
    return f"{v:+.{digits}f}%" if signed else f"{v:.{digits}f}%"


def sale_m(sale, cost):
    if not sale:
        return None
    return (sale - cost) / sale


def industry_tables(story, s, skus, blend, profiles, fails):
    story.append(P("Part B — Industry report (calculation tables, reconfirmed)", s["cover"]))
    story.append(P(
        "Same Monte Carlo as the industry PDF. Instant BE / 20 / 40 / 60 / sale m "
        "are year-1. Instant rec is the 30% print — 40/60 are reference only. "
        "The old industry PDF’s Instant $1,094 is not a recommendation.",
        s["sub"],
    ))

    story.append(P("B1. Book mix (same on every firm)", s["h1"]))
    pop = [[P(h, s["th"]) for h in [
        "Profile", "Weight", "Win rate", "R:R", "Trades/day", "Risk / trade",
        "Room awareness", "Violation / day",
    ]]]
    for row in (
        ("Pro", "7%", "52%", "1.50", "2", "0.36–0.68%", "0.94", "0.007%"),
        ("Semi-skilled", "22%", "51%", "1.38", "2", "0.44–0.78%", "0.86", "0.012%"),
        ("Average", "26%", "49%", "1.22", "3", "0.52–0.95%", "0.72", "0.018%"),
        ("Aggressive", "28%", "43%", "0.96", "6", "1.50–2.60%", "0.18", "0.038%"),
        ("Lottery", "17%", "40%", "0.84", "8", "2.40–4.20%", "0.05", "0.065%"),
    ):
        pop.append([P(row[0], s["tdl"])] + [P(c, s["td"]) for c in row[1:]])
    story.append(grid(pop, [28*mm, 18*mm, 20*mm, 16*mm, 22*mm, 28*mm, 28*mm, 28*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "1,000 paths × 5 profiles × 47 products. Seed 42. Dollars scale × size/100k. "
        "Year-1 after first pay: 59% × 72% × 76%. $100 min reward.",
        s["tiny"],
    ))

    story.append(P("B2. Blended rates — every product", s["h1"]))
    heads = ["Firm", "Plan", "Family", "P1", "Funded", "P(pay)", "Year-1",
             "E[X] first $100k", "Days", "Refund"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    blend_s = blend.sort_values(["Family", "Firm", "Plan"])
    for i, r in enumerate(blend_s.itertuples(), start=1):
        if r.Firm == "Verodus":
            spec[i] = "rec" if r.Family == "instant" else "live"
        data.append([
            P(str(r.Firm), s["tdl"]), P(str(r.Plan), s["tdl"]), P(str(r.Family), s["td"]),
            P(pct(r.Phase1), s["td"]), P(pct(r.Funded), s["td"]),
            P(pct(r.P_pay), s["td"]), P(pct(r.P_yr1), s["td"]),
            P(usd(r.E_payout_100k), s["td"]),
            P(f"{float(r.Avg_days):.0f}", s["td"]), P(str(r.Refund), s["td"]),
        ])
    story.append(grid(data, [
        30*mm, 36*mm, 18*mm, 16*mm, 16*mm, 16*mm, 16*mm, 32*mm, 14*mm, 20*mm,
    ], spec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant P(pay) = first-payout eligibility. Verodus Instant 22.1% matches "
        "BG Instant 22.1% and Instant Funding 21.4%. Price Instant on year-1 7.16%.",
        s["tiny"],
    ))

    story.append(P("B3. Verodus P(pay) by trader type", s["h1"]))
    pheads = ["Plan", "Pro 7%", "Semi 22%", "Average 26%", "Aggressive 28%",
              "Lottery 17%", "Blend P(pay)", "Blend year-1"]
    pdata = [[P(h, s["th"]) for h in pheads]]
    pspec = {}
    for i, (plan, product) in enumerate((
        ("Instant", "Verodus Instant"),
        ("1-Step", "Verodus 1-Step"),
        ("2-Step Lite", "Verodus 2-Step Lite"),
        ("2-Step Pro", "Verodus 2-Step Pro"),
    ), start=1):
        sub = profiles[profiles.Product == product]
        by = {r.Profile: float(r.P_pay) for r in sub.itertuples()}
        br = blend[blend.Product == product].iloc[0]
        if plan == "Instant":
            pspec[i] = "rec"
        pdata.append([
            P(plan, s["tdl"]),
            P(pct(by.get("Pro")), s["td"]),
            P(pct(by.get("Semi-skilled")), s["td"]),
            P(pct(by.get("Average")), s["td"]),
            P(pct(by.get("Aggressive")), s["td"]),
            P(pct(by.get("Lottery")), s["td"]),
            P(pct(br.P_pay), s["td"]),
            P(pct(br.P_yr1), s["td"]),
        ])
    story.append(grid(pdata, [
        28*mm, 24*mm, 26*mm, 28*mm, 32*mm, 28*mm, 28*mm, 26*mm,
    ], pspec))
    story.append(Spacer(1, 2*mm))

    story.append(P("B4. Live Verodus rules", s["h1"]))
    rdata = [[P(h, s["th"]) for h in ["Rule", "Instant", "1-Step", "Lite", "Pro"]]]
    for row in (
        ("Phases", "0-step", "1 + funded", "2 + funded", "2 + funded"),
        ("Target", "5 valid days", "10%", "8% then 5%", "10% then 5%"),
        ("Max DD", "6% trail, never locks", "6% hybrid", "8% static (funded 8%)", "10% static"),
        ("Daily DD", "3% day’s equity high", "4% SOD", "4% SOD", "5% SOD"),
        ("Consistency", "20% of +days", "50% eval only", "None", "None"),
        ("Min days", "5 at +0.5% SOD", "3 funded", "5+5 / 3", "5+5 / 3"),
        ("Refund / split", "None / 80%", "First / 80%", "First / 80%", "First / 80%"),
        ("Min reward", "$100", "$100", "$100", "$100"),
        ("vs live FAQ", "None", "None", "Funded DD 10%→8%", "None"),
    ):
        rdata.append([P(row[0], s["tdl"])] + [P(c, s["td"]) for c in row[1:]])
    story.append(grid(rdata, [32*mm, 48*mm, 42*mm, 50*mm, 40*mm]))
    story.append(Spacer(1, 2*mm))

    story.append(P("B5. Every industry SKU — street / E[X] / BE $ / 20 / 40 / 60 / m", s["h1"]))
    story.append(P(
        "Instant rows use year-1 E[X] and year-1 BE. Eval rows use first-payout E[X] "
        "and BE = E[X] / (1 − k). Sale m is (sale − E[cost]) / sale on that basis. "
        "This replaces the industry PDF’s first-payout Instant 20/40/60 grid.",
        s["body"],
    ))
    for fam, title in (
        ("instant", "B5.1 Instant"),
        ("1-step", "B5.2 One-step"),
        ("2-step", "B5.3 Two-step"),
        ("3-step", "B5.4 Three-step"),
    ):
        story.append(P(title, s["h1"]))
        sub = skus[skus.Family == fam].sort_values(["Firm", "Plan", "Size"])
        heads = ["Firm", "Plan", "Size", "Sale", "P(pay)", "Year-1",
                 "E[X] used", "BE $", "20%", "40%", "60%", "Sale m"]
        data = [[P(h, s["th"]) for h in heads]]
        spec = {}
        for i, r in enumerate(sub.itertuples(), start=1):
            pr = pricing_for(r)
            cost = pr["e_used"] if r.Family == "instant" else float(r.E_cost)
            if r.Firm == "Verodus":
                spec[i] = "rec" if r.Family == "instant" else "live"
            data.append([
                P(str(r.Firm), s["tdl"]), P(str(r.Plan), s["tdl"]),
                P(usd(r.Size), s["td"]), P(usd(r.Sale), s["td"]),
                P(pct(pr["p_pay"]), s["td"]), P(pct(pr["p_yr1"]), s["td"]),
                P(usd(pr["e_used"]), s["td"]), P(usd(pr["be"]), s["td"]),
                P(usd(pr["px_20"]), s["td"]), P(usd(pr["px_40"]), s["td"]),
                P(usd(pr["px_60"]), s["td"]),
                P(pct(sale_m(float(r.Sale), cost), signed=True, digits=0), s["td"]),
            ])
        story.append(grid(data, [
            28*mm, 32*mm, 16*mm, 16*mm, 14*mm, 14*mm, 20*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm,
        ], spec))
        story.append(Spacer(1, 2*mm))

    story.append(P("B6. Live Verodus vs family street (reconfirmed m)", s["h1"]))
    rel = [[P(h, s["th"]) for h in [
        "Plan", "Size", "Live $", "Live m", "n", "Peer min", "Peer med", "Peer max",
        "vs med", "Rank cheap",
    ]]]
    for plan, fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            vr = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if vr.empty:
                continue
            r = vr.iloc[0]
            pr = pricing_for(r)
            cost = pr["e_used"] if plan == "Instant" else float(r.E_cost)
            peers = family_peers(skus, fam)
            peers = peers[peers.Size == sz]
            if peers.empty:
                continue
            vsale = float(r.Sale)
            pmin, pmed, pmax = float(peers.Sale.min()), float(peers.Sale.median()), float(peers.Sale.max())
            rank = int((peers.Sale < vsale).sum()) + 1
            rel.append([
                P(plan, s["tdl"]), P(usd(sz), s["td"]), P(usd(vsale), s["td"]),
                P(pct(sale_m(vsale, cost), signed=True, digits=0), s["td"]),
                P(str(len(peers)), s["td"]),
                P(usd(pmin), s["td"]), P(usd(pmed), s["td"]), P(usd(pmax), s["td"]),
                P(f"{vsale / pmed:.2f}×", s["td"]),
                P(f"{rank} / {len(peers)+1}", s["td"]),
            ])
    story.append(grid(rel, [
        26*mm, 18*mm, 18*mm, 16*mm, 12*mm, 20*mm, 20*mm, 20*mm, 16*mm, 20*mm,
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "On year-1, live Instant $50k/$100k print (+63% / +58%). They were holes only "
        "on the rejected first-payout $875 cost.",
        s["tiny"],
    ))

    story.append(P("B7. Blue Guardian Instant vs Verodus (year-1)", s["h1"]))
    bg = [[P(h, s["th"]) for h in [
        "Size", "Vero live", "Vero live m", "Vero rec", "Vero rec m",
        "BG sale", "BG m yr1", "Rec / BG",
    ]]]
    for sz in (5000, 10000, 25000, 50000, 100000):
        vr = skus[(skus.Firm == "Verodus") & (skus.Plan == "Instant") & (skus.Size == sz)]
        br = skus[(skus.Firm == "Blue Guardian") & (skus.Plan == "Instant") & (skus.Size == sz)]
        if vr.empty or br.empty:
            continue
        v, b = vr.iloc[0], br.iloc[0]
        pv, pb = pricing_for(v), pricing_for(b)
        rec = REC[("Instant", sz)]
        bg.append([
            P(usd(sz), s["td"]),
            P(usd(v.Sale), s["td"]),
            P(pct(sale_m(float(v.Sale), pv["e_used"]), signed=True, digits=0), s["td"]),
            P(usd(rec), s["td"]),
            P(pct(sale_m(rec, pv["e_used"]), signed=True, digits=0), s["td"]),
            P(usd(b.Sale), s["td"]),
            P(pct(sale_m(float(b.Sale), pb["e_used"]), signed=True, digits=0), s["td"]),
            P(f"{rec / float(b.Sale):.2f}×", s["td"]),
        ])
    story.append(grid(bg, [
        20*mm, 24*mm, 24*mm, 22*mm, 24*mm, 22*mm, 22*mm, 20*mm,
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "BG $100k $467 is +38% on their year-1 cost. Rec $429 is +34% on ours and 0.92× BG. "
        "Do not copy their lock. Do not match Alpha $274.",
        s["tiny"],
    ))

    story.append(P("B8. One hundred accounts — operator P&L (year-1 Instant)", s["h1"]))
    hun = [[P(h, s["th"]) for h in [
        "Plan", "Size", "P(pay)", "Year-1", "Fail before pay",
        "Live ×100", "E[cost]×100", "Live contrib.",
        "Rec ×100", "Rec contrib.",
    ]]]
    hspec = {}
    hi = 0
    for plan, _fam in ANCHORS:
        for sz in (5000, 100000):
            if (plan, sz) not in REC:
                continue
            vr = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)]
            if vr.empty:
                continue
            r = vr.iloc[0]
            pr = pricing_for(r)
            rec = REC[(plan, sz)]
            if plan == "Instant":
                live_cost = 100 * pr["e_used"]
                rec_cost = 100 * pr["e_used"]
            else:
                live_cost = 100 * float(r.E_cost)
                k = float(r.P_pay)
                rec_cost = 100 * (pr["e_first"] + k * rec)
            live_in = 100 * float(r.Sale)
            rec_in = 100 * rec
            hi += 1
            if plan == "Instant":
                hspec[hi] = "rec"
            hun.append([
                P(plan, s["tdl"]), P(usd(sz), s["td"]),
                P(pct(pr["p_pay"]), s["td"]), P(pct(pr["p_yr1"]), s["td"]),
                P(pct(1 - pr["p_pay"]), s["td"]),
                P(usd(live_in), s["td"]), P(usd(live_cost), s["td"]),
                P(usd(live_in - live_cost), s["td"]),
                P(usd(rec_in), s["td"]), P(usd(rec_in - rec_cost), s["td"]),
            ])
    story.append(grid(hun, [
        26*mm, 18*mm, 16*mm, 16*mm, 24*mm, 22*mm, 24*mm, 24*mm, 22*mm, 24*mm,
    ], hspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $100k live: 100 × $676 − 100 × $284 = <b>+$39,200</b> on year-1. "
        "Rec: 100 × $429 − 100 × $284 = <b>+$14,500</b> (~34%). "
        "The industry PDF’s −$19,925 / +$21,875 used first-payout $875 — not used here.",
        s["body"],
    ))

    story.append(P("B9. Failure mix (share of ending reasons)", s["h1"]))
    fail_t = [[P(h, s["th"]) for h in [
        "Book", "Daily DD", "Max DD", "Time / abandon", "Rule / news", "KYC", "Post-payout",
    ]]]

    def mix_row(label, mix):
        tot = sum(mix.values()) or 1.0

        def g(name):
            return pct(mix.get(name, 0.0) / tot) if tot else "—"

        return [
            P(label, s["tdl"]),
            P(g("Daily DD"), s["td"]), P(g("Max DD"), s["td"]),
            P(g("Time / abandon"), s["td"]), P(g("Rule / news"), s["td"]),
            P(g("KYC drop"), s["td"]), P(g("Post-payout attrition"), s["td"]),
        ]

    fail_t.append(mix_row("Whole 20-firm book", weighted_fail_mix(fails)))
    for prod, lab in (
        ("Verodus Instant", "Verodus Instant"),
        ("BG Instant", "Blue Guardian Instant"),
        ("Verodus 1-Step", "Verodus 1-Step"),
        ("Verodus 2-Step Lite", "Verodus Lite"),
        ("Verodus 2-Step Pro", "Verodus Pro"),
        ("FTMO 2-Step", "FTMO 2-Step"),
    ):
        fail_t.append(mix_row(lab, weighted_fail_mix(fails, prod)))
    story.append(grid(fail_t, [48*mm, 22*mm, 22*mm, 28*mm, 24*mm, 18*mm, 28*mm]))
    story.append(Spacer(1, 2*mm))

    story.append(P("B10. Street codes (August 2026)", s["h1"]))
    st = [[P(h, s["th"]) for h in ["Firm", "Live code", "Off", "What the shopper pays"]]]
    for i, (firm, code, off, note) in enumerate(STREET, start=1):
        st.append([P(firm, s["tdl"]), P(code, s["td"]), P(off, s["td"]), P(note, s["tdl"])])
    story.append(grid(st, [36*mm, 48*mm, 18*mm, 130*mm], {1: "live"}))
    story.append(Spacer(1, 2*mm))

    story.append(P("B11. Unique rules (catalog card used in D)", s["h1"]))
    ur = [[P(h, s["th"]) for h in ["Firm", "Plan", "Rules"]]]
    for (firm, plan), text in UNIQUE.items():
        ur.append([P(firm, s["tdl"]), P(plan, s["tdl"]), P(text, s["tdl"])])
    story.append(grid(ur, [36*mm, 40*mm, 156*mm]))
    story.append(Spacer(1, 2*mm))


def summary(story, s, skus):
    story.append(P("Verodus confirmed book — one PDF", s["cover"]))
    story.append(P(
        "Summary first. Then every calculation table from the BE rank report, "
        "the industry report (recomputed), and the recommended-prices report. "
        "16 August 2026.",
        s["sub"],
    ))
    story.append(P(
        "<b>Reconfirmed.</b> Instant P(pay) 22.1% is first-payout eligibility — correct, "
        "do not price on it. Instant year-1 7.16% is the cost rate. "
        "Eval P(pay) 8.8% / 10.6% / 12.0% is the eval cost rate. "
        "Columns are 20 / 40 / 60. Instant rec sits on the year-1 30% print. "
        "Evals stay live. Ignore the industry PDF’s Instant $1,094 and "
        "industry_skus Instant BE $875.",
        s["body"],
    ))

    story.append(P("Confirmed P(pay)", s["h1"]))
    v = [[P(h, s["th"]) for h in [
        "Plan", "P(pay)", "Year-1", "Price on", "BE $100k", "Rec $100k", "Rec m",
    ]]]
    vspec = {}
    for i, (plan, use) in enumerate((
        ("Instant", "Year-1 7.16%"),
        ("1-Step", "First-payout + refund"),
        ("2-Step Lite", "First-payout + refund"),
        ("2-Step Pro", "First-payout + refund"),
    ), start=1):
        live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == 100000)].iloc[0]
        pr = pricing_for(live)
        rec = REC[(plan, 100000)]
        cost = pr["e_used"] if plan == "Instant" else float(live.E_cost)
        vspec[i] = "rec" if plan == "Instant" else "live"
        v.append([
            P(plan, s["tdl"]), P(pct(pr["p_pay"]), s["td"]), P(pct(pr["p_yr1"]), s["td"]),
            P(use, s["tdl"]), P(usd(pr["be"]), s["td"]), P(usd(rec), s["td"]),
            P(pct(sale_m(rec, cost), signed=True, digits=0), s["td"]),
        ])
    story.append(grid(v, [28*mm, 18*mm, 18*mm, 44*mm, 24*mm, 24*mm, 18*mm], vspec))
    story.append(Spacer(1, 2*mm))

    story.append(P(
        "Confirmed SKU table — Plan / Size / List / Sale / E[X] / P(pay) / BE / 20% / 40% / 60% / Sale m",
        s["h1"],
    ))
    story.append(P(
        "<b>Use 20 / 40 / 60</b> as the industry reference columns. Instant rec is the "
        "year-1 <b>30% print</b> — greater margin that still sells. "
        "40% Instant $100k ($473) is Blue Guardian $467. "
        "60% ($710) sits above Goat $559 / Instant Funding $639 — do not aim Instant there. "
        "10 / 20 / 30 was only a reaction when 40/60 looked too rich as Instant targets. "
        "Sale is the recommended VERO35 fee. List = sale ÷ 0.65.",
        s["body"],
    ))
    ctab, _crows = classic_table(skus, s)
    story.append(ctab)
    story.append(Spacer(1, 2*mm))

    story.append(P(
        "Opex stack — 10% error, $1/account, marketing 20%, CAD 10k wages",
        s["h1"],
    ))
    story.append(P(
        "S<sub>opex</sub> = (BE × 1.10 + $1) / 0.80. Wages CAD 10,000 × 0.72 = "
        "USD 7,200 / month. N wages = $7,200 / leftover at rec if that SKU carried "
        "the whole wage bill. Do not match a peer low that fails Low OK.",
        s["body"],
    ))
    otab, _orows = opex_table(skus, s)
    story.append(otab)
    story.append(Spacer(1, 2*mm))

    story.append(P("Confirmed rec $ and BE $", s["h1"]))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            cells.append(rec_be_cell(REC.get((plan, sz)), plan_be(skus, plan, sz), s["td2"]))
        data.append(cells)
        spec[i] = "rec"
    story.append(grid(data, [26*mm, 30*mm, 30*mm, 30*mm, 30*mm, 32*mm, 32*mm], spec))
    story.append(Spacer(1, 2*mm))

    story.append(P("Confirmed margin % by size and family", s["h1"]))
    mheads = ["Family", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    mdata = [[P(h, s["th"]) for h in mheads]]
    mspec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        cells = [P(plan, s["tdl"])]
        for sz in SIZES:
            if (plan, sz) not in REC:
                cells.append(P("—", s["td"]))
                continue
            live = skus[(skus.Firm == "Verodus") & (skus.Plan == plan) & (skus.Size == sz)].iloc[0]
            pr = pricing_for(live)
            cost = pr["e_used"] if plan == "Instant" else float(live.E_cost)
            cells.append(P(pct(sale_m(REC[(plan, sz)], cost), signed=True, digits=0), s["td"]))
        mdata.append(cells)
        mspec[i] = "rec" if plan == "Instant" else "live"
    story.append(grid(mdata, [28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 30*mm, 30*mm], mspec))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Instant $5k/$10k are a shop floor on a $14/$28 BE. $25k+ Instant is the 30–40% print. "
        "Eval margins are leftover live VERO35. Part A = rank tables. Part B = industry "
        "tables on this basis. Part C = recommended-price tables.",
        s["body"],
    ))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        REC_MARGIN, H - 5.4 * mm,
        "VERODUS  ·  Confirmed book — rank + industry + rec tables  ·  16 Aug 2026",
    )
    canvas.drawRightString(W - REC_MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(
        REC_MARGIN, 2.6 * mm,
        "Reconfirmed. Instant = year-1. Evals = first-payout + refund. Columns 20/40/60. Instant rec = 30% print.",
    )
    canvas.drawRightString(W - REC_MARGIN, 2.6 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    rec_story, skus, _rows, _stats = rec_collect()
    rank_story, _skus2, _scored = rank_collect()
    blend = pd.read_csv(RESULTS / "industry_blended.csv")
    profiles = pd.read_csv(RESULTS / "industry_profiles.csv")
    fails = pd.read_csv(RESULTS / "industry_failures.csv")

    story = []
    summary(story, s, skus)
    story.append(PageBreak())
    story.append(P("Part A — BE rank report (reconfirmed)", s["cover"]))
    story.append(P(
        "Difficulty D and in-band 20% / 30% ranks. Instant BE is year-1. "
        "Tables reprinted from the rank report on the confirmed basis.",
        s["sub"],
    ))
    story.extend(rank_story)
    story.append(PageBreak())
    industry_tables(story, s, skus, blend, profiles, fails)
    story.append(PageBreak())
    story.append(P("Part C — Recommended prices (reconfirmed)", s["cover"]))
    story.append(P(
        "VERO35 rec card, BE $ by size, 20/40/60, Instant peer year-1 margins, "
        "every family street fee, rec vs BE $. Tables reprinted from the "
        "recommended-prices report.",
        s["sub"],
    ))
    story.extend(rec_story)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        title="Verodus confirmed book — 16 Aug 2026",
        author="Verodus operator research",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
