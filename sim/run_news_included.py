#!/usr/bin/env python3
"""Rerun Verodus with news trading allowed on every phase and funded account.

News is not an add-on. The news-window clawback / second-hit breach is off.
High-impact days still have fatter tails (traders may take the event).
Writes results/Verodus_News_Included_2026-08-17.pdf and comparison CSVs.
Does not overwrite the restricted-news industry book CSVs.
"""
from __future__ import annotations

import math
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from catalog import PRODUCTS
from industry_book import (
    PROFILES,
    SIM_BALANCE,
    break_even_fee,
    expected_refund_frac,
    run_phase,
    simulate_funded_survival,
)
from write_addon_combo_pdf import sticker
from write_price_rec_pdf import (
    ANCHORS,
    MARKETING,
    REC,
    SIZES,
    leftover_after_opex,
    opex_stack,
    rec_list,
    usd,
    y1_payout,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "Verodus_News_Included_2026-08-17.pdf"

VERODUS = (
    "Verodus Instant",
    "Verodus 1-Step",
    "Verodus 2-Step Lite",
    "Verodus 2-Step Pro",
)

# Extra E[X] vs default 80% biweekly after news is in the base product.
# News is no longer an add-on. Swing collapses to weekend.
EXTRA_F = {
    "Instant": {
        "weekend": 0.08, "weekly": 0.08,
        "od80": 0.12, "split90": 0.125, "od90": 0.41,
    },
    "1-Step": {
        "weekend": 0.04, "weekly": 0.05,
        "od80": 0.05, "split90": 0.125, "od90": 0.125,
    },
}
EXTRA_F["2-Step Lite"] = dict(EXTRA_F["1-Step"])
EXTRA_F["2-Step Pro"] = dict(EXTRA_F["1-Step"])

LOCKED_ADDON_PCT = {
    "weekend": (0.12, 0.12),
    "weekly": (0.08, 0.08),
    "od80": (0.12, 0.15),
    "split90": (0.12, 0.15),
    "od90": (0.20, 0.32),
}

NAVY = colors.HexColor("#0f2744")
TEAL = colors.HexColor("#1a6b6b")
ROW_ALT = colors.HexColor("#f4f7fb")
ROW_REC = colors.HexColor("#dcfce7")
ROW_NO = colors.HexColor("#fee2e2")
ROW_CHG = colors.HexColor("#fef3c7")
GRID = colors.HexColor("#c5d0dc")
HEAD_BG = colors.HexColor("#0f2744")
PAGE = landscape(A4)
W, H = PAGE
MARGIN = 10 * mm


def run_one(config, profile, rng, news_allowed):
    split = config["split"]
    min_reward = config["min_reward"]
    instant = config["instant"]
    ok, bal, reason, d = run_phase(
        SIM_BALANCE, config["phases"][0], profile, rng,
        is_funded=False,
        min_reward=min_reward if instant else 0.0, split=split,
        news_allowed=news_allowed,
    )
    days = d
    if not ok:
        return dict(p1=False, funded=False, paid=False, payout=0.0,
                    reason=reason or "unknown", stage="p1", days=days)
    for i, phase in enumerate(config["phases"][1:], start=2):
        ok, bal, reason, d = run_phase(
            SIM_BALANCE, phase, profile, rng, is_funded=False,
            news_allowed=news_allowed,
        )
        days += d
        if not ok:
            return dict(p1=True, funded=False, paid=False, payout=0.0,
                        reason=reason or "unknown", stage=f"p{i}", days=days)
    if config["funded"] is not None:
        if rng.random() < 0.12:
            return dict(p1=True, funded=False, paid=False, payout=0.0,
                        reason="kyc_drop", stage="funded", days=days)
        ok, bal, reason, d = run_phase(
            SIM_BALANCE, config["funded"], profile, rng,
            is_funded=True, min_reward=min_reward, split=split,
            news_allowed=news_allowed,
        )
        days += d
        if not ok:
            return dict(p1=True, funded=False, paid=False, payout=0.0,
                        reason=reason or "unknown", stage="funded", days=days)
    profit = max(0.0, bal - SIM_BALANCE)
    payout = split * profit
    cap = config.get("first_reward_cap")
    if cap:
        payout = min(payout, cap * SIM_BALANCE)
    paid = payout + 1e-9 >= min_reward
    return dict(p1=True, funded=True, paid=paid, payout=payout if paid else 0.0,
                reason=None if paid else "min_reward", stage="paid", days=days)


def run_book(n_sims, seed, news_allowed):
    rng = np.random.default_rng(seed)
    total = len(VERODUS) * len(PROFILES) * n_sims
    done = 0
    t0 = time.time()
    rows = []
    fail_rows = []
    label = "news-on" if news_allowed else "restricted"
    print(f"{label}: {len(VERODUS)} products × {len(PROFILES)} × {n_sims} = {total:,}")
    for key in VERODUS:
        cfg = PRODUCTS[key]
        for profile in PROFILES:
            n = p1 = funded = paid = yr1 = 0
            days = []
            payouts = []
            fails = defaultdict(int)
            for _ in range(n_sims):
                res = run_one(cfg, profile, rng, news_allowed)
                n += 1
                days.append(res["days"])
                payouts.append(res["payout"])
                if res["p1"]:
                    p1 += 1
                if res["funded"]:
                    funded += 1
                if res["paid"]:
                    paid += 1
                    survived, m = simulate_funded_survival(rng)
                    if survived:
                        yr1 += 1
                    else:
                        fails[f"post_m{m}"] += 1
                elif res["reason"]:
                    fails[f"{res['stage']}_{res['reason']}"] += 1
                done += 1
                if done % 250 == 0 or done == total:
                    eta = (time.time() - t0) / done * (total - done)
                    sys.stdout.write(
                        f"\r{label:11s} {key[8:22]:14s} {profile:12s} "
                        f"{100 * done / total:5.1f}% ETA {eta:4.0f}s"
                    )
                    sys.stdout.flush()
            rows.append({
                "Product": key,
                "Plan": cfg["plan"],
                "Family": cfg["family"],
                "Profile": profile,
                "Weight": PROFILES[profile]["weight"],
                "Phase1": p1 / n,
                "Funded": funded / n,
                "P_pay": paid / n,
                "P_yr1": yr1 / n,
                "E_payout_100k": float(np.mean(payouts)),
                "E_if_paid": float(np.mean([x for x in payouts if x > 0])) if paid else 0.0,
                "Avg_days": float(np.mean(days)),
                "News": news_allowed,
            })
            for r, c in fails.items():
                fail_rows.append({
                    "Product": key, "Profile": profile, "Reason": r,
                    "Share": c / n, "News": news_allowed,
                })
    print(f"\n{label} done in {time.time() - t0:.1f}s")
    return pd.DataFrame(rows), pd.DataFrame(fail_rows)


def blend(df):
    rows = []
    for product, sub in df.groupby("Product", sort=False):
        w = sub["Weight"].to_numpy()
        cfg = PRODUCTS[product]
        rows.append({
            "Product": product,
            "Plan": cfg["plan"],
            "Family": cfg["family"],
            "Refund": cfg["refund"],
            "Phase1": float(np.dot(w, sub["Phase1"])),
            "Funded": float(np.dot(w, sub["Funded"])),
            "P_pay": float(np.dot(w, sub["P_pay"])),
            "P_yr1": float(np.dot(w, sub["P_yr1"])),
            "E_payout_100k": float(np.dot(w, sub["E_payout_100k"])),
            "Avg_days": float(np.dot(w, sub["Avg_days"])),
            "News": bool(sub["News"].iloc[0]),
        })
    return pd.DataFrame(rows)


def be_for(row, size):
    e_first = float(row.E_payout_100k) * (size / SIM_BALANCE)
    p_pay = float(row.P_pay)
    p_yr1 = float(row.P_yr1)
    if row.Family == "instant":
        e = y1_payout(e_first, p_pay, p_yr1)
        k = expected_refund_frac(str(row.Refund), p_yr1)
        return e, break_even_fee(e, k), "year-1"
    k = expected_refund_frac(str(row.Refund), p_pay)
    return e_first, break_even_fee(e_first, k), "first"


def attractive_up(x: float) -> int:
    n = int(math.ceil(x - 1e-9))
    if n % 10 == 9:
        return n
    return n + (9 - n % 10)


def rec_after(plan, size, be):
    locked = REC[(plan, size)]
    st = opex_stack(be, plan, size)
    left = leftover_after_opex(locked, st["loaded"])
    if left is not None and left >= -1:
        return locked, False, st, left
    need = st["s_opex"]
    bumped = max(locked, attractive_up(need))
    left2 = leftover_after_opex(bumped, st["loaded"])
    return bumped, bumped != locked, st, left2


def price_rows(off, on):
    off_i = {r.Plan: r for r in off.itertuples()}
    on_i = {r.Plan: r for r in on.itertuples()}
    rows = []
    for plan, _fam in ANCHORS:
        for sz in SIZES:
            if (plan, sz) not in REC:
                continue
            a = off_i[plan]
            b = on_i[plan]
            e0, be0, basis = be_for(a, sz)
            e1, be1, _ = be_for(b, sz)
            rec1, changed, st, left = rec_after(plan, sz, be1)
            locked = REC[(plan, sz)]
            st0 = opex_stack(be0, plan, sz)
            left0 = leftover_after_opex(locked, st0["loaded"])
            rows.append({
                "Plan": plan, "Size": sz, "Basis": basis,
                "P_pay_off": float(a.P_pay), "P_pay_on": float(b.P_pay),
                "P_yr1_off": float(a.P_yr1), "P_yr1_on": float(b.P_yr1),
                "E_off": e0, "E_on": e1,
                "BE_off": be0, "BE_on": be1,
                "BE_dlt": be1 - be0,
                "S_opex_off": st0["s_opex"], "S_opex_on": st["s_opex"],
                "Locked": locked, "Rec": rec1, "Changed": changed,
                "List": rec_list(rec1),
                "Left_off": left0, "Left_on": left,
                "Loaded_on": st["loaded"],
            })
    return pd.DataFrame(rows)


def pct_for(plan, key):
    ev, inst = LOCKED_ADDON_PCT[key]
    return inst if plan == "Instant" else ev


def addon_rows(prices):
    names = [
        ("weekend", "Weekend holding"),
        ("weekly", "Weekly 80%"),
        ("od80", "On Demand 80%"),
        ("split90", "90% split"),
        ("od90", "90% On Demand"),
    ]
    rows = []
    for r in prices.itertuples():
        extra_f = EXTRA_F[r.Plan]
        for key, name in names:
            pct = pct_for(r.Plan, key)
            st = sticker(r.List, pct)
            extra = r.BE_on * extra_f[key]
            left = st * 0.65 * (1.0 - MARKETING) - extra
            rows.append({
                "Plan": r.Plan, "Size": r.Size, "Addon": name, "Key": key,
                "Pct": pct, "Sticker": st, "Extra": extra, "Left": left,
                "BE": r.BE_on, "List": r.List, "Sale": r.Rec,
            })
    return pd.DataFrame(rows)


def fail_blend(fails, profiles):
    """Weighted share of buyers by reason family."""
    wmap = {r.Product + "|" + r.Profile: r.Weight for r in profiles.itertuples()}
    out = []
    for news, sub in fails.groupby("News"):
        for product, psub in sub.groupby("Product"):
            bucket = defaultdict(float)
            for r in psub.itertuples():
                w = wmap.get(product + "|" + r.Profile, 0.0)
                fam = "rule" if "rule_violation" in r.Reason else (
                    "daily" if "daily_dd" in r.Reason else (
                        "max" if "max_dd" in r.Reason else "other"
                    )
                )
                bucket[fam] += w * r.Share
            out.append({"Product": product, "News": news, **bucket})
    return pd.DataFrame(out)


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Times-Bold",
            fontSize=16, leading=20, textColor=NAVY, alignment=TA_LEFT, spaceAfter=3,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Times-Italic",
            fontSize=9.5, leading=12, textColor=TEAL, spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Times-Bold",
            fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Times-Roman",
            fontSize=8.2, leading=10.6, alignment=TA_JUSTIFY, spaceAfter=4,
        ),
        "th": ParagraphStyle(
            "th", parent=base["Normal"], fontName="Times-Bold",
            fontSize=6.4, leading=8, textColor=colors.white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.4, leading=8, alignment=TA_CENTER,
        ),
        "tdl": ParagraphStyle(
            "tdl", parent=base["Normal"], fontName="Times-Roman",
            fontSize=6.4, leading=8, alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "tiny", parent=base["Normal"], fontName="Times-Roman",
            fontSize=7, leading=9, textColor=colors.HexColor("#334155"),
        ),
    }


def P(text, style):
    return Paragraph(text, style)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 8 * mm, W, 8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        MARGIN, H - 5.4 * mm,
        "VERODUS  ·  News included (not an add-on)  ·  17 Aug 2026",
    )
    canvas.drawRightString(W - MARGIN, H - 5.4 * mm, "Confidential — operator")
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 7.4)
    canvas.drawString(
        MARGIN, 2.6 * mm,
        "Same 7/22/26/28/17 book. News allowed on every phase and funded account. VERO35 still 35% off list.",
    )
    canvas.drawRightString(W - MARGIN, 2.6 * mm, str(doc.page))
    canvas.restoreState()


def grid(data, col_w, special=None):
    special = special or {}
    sty = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.25, GRID),
        ("TOPPADDING", (0, 0), (-1, -1), 2.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.0),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        mark = special.get(i)
        if mark == "rec":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_REC))
        elif mark == "no":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_NO))
        elif mark == "chg":
            sty.append(("BACKGROUND", (0, i), (-1, i), ROW_CHG))
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(sty))
    return t


def flag(left):
    if left is None:
        return "—"
    if left >= -1:
        return "yes"
    if left >= -5:
        return "thin"
    return "NO"


def build_pdf(off, on, prices, addons):
    s = styles()
    story = []
    n_chg = int(prices.Changed.sum())
    be_dlt_100k = prices[prices.Size == 100000][["Plan", "BE_off", "BE_on", "BE_dlt", "P_pay_off", "P_pay_on"]]

    story.append(P("News trading included — rec prices and remaining add-ons", s["cover"]))
    story.append(P(
        "Monte Carlo rerun with news allowed on every evaluation phase and every funded "
        "account. News is not sold. The ±2-minute window / News Addon is off. Weekend holding, "
        "Weekly, On Demand, and 90% stay paid add-ons. Swing (news+weekend) is dropped — news "
        "is already in the base, so the holding SKU is Weekend at 12%.",
        s["sub"],
    ))

    story.append(P("1. What changed in the engine", s["h1"]))
    story.append(P(
        "Restricted book: a per-day rule-violation draw is a hard fail (news window plus "
        "HFT / arb / copy). News-on: 65% of those draws are treated as the news window and "
        "are skipped; the other 35% still fail. About 12% of active days are high-impact; "
        "on those days session vol ×1.40, shock probability ×2.20, and winning RRR ×1.15. "
        "Instant, 1-Step, Lite, and Pro all use the same news-on switch. Same seed 42, "
        "same 7/22/26/28/17 mix, 1,200 paths per profile.",
        s["body"],
    ))

    story.append(P("2. Blended funnel — restricted vs news included", s["h1"]))
    heads = ["Plan", "P(pay) off", "P(pay) on", "Year-1 off", "Year-1 on",
             "E[X] $100k off", "E[X] $100k on", "Δ E[X]"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    off_i = {r.Plan: r for r in off.itertuples()}
    for i, r in enumerate(on.itertuples(), start=1):
        a = off_i[r.Plan]
        e0 = float(a.E_payout_100k)
        e1 = float(r.E_payout_100k)
        spec[i] = "rec" if abs(e1 - e0) / max(e0, 1) < 0.03 else "chg"
        data.append([
            P(r.Plan, s["tdl"]),
            P(f"{100 * a.P_pay:.1f}%", s["td"]),
            P(f"{100 * r.P_pay:.1f}%", s["td"]),
            P(f"{100 * a.P_yr1:.1f}%", s["td"]),
            P(f"{100 * r.P_yr1:.1f}%", s["td"]),
            P(usd(e0), s["td"]),
            P(usd(e1), s["td"]),
            P(usd(e1 - e0), s["td"]),
        ])
    story.append(grid(data, [
        28*mm, 24*mm, 24*mm, 24*mm, 24*mm, 28*mm, 28*mm, 22*mm,
    ], spec))
    story.append(P(
        "E[X] $100k is first-payout mean over all buyers. Instant rec prices use year-1 "
        "(first × P_yr1 / P_pay). Green = move under 3%. Yellow = larger move.",
        s["tiny"],
    ))

    story.append(P("3. Challenge rec — locked VERO35 vs news-on opex floor", s["h1"]))
    story.append(P(
        "Locked rec stays if leftover after 10% error, $1, wage share, and 20% ads is still "
        "at least −$1. Otherwise the sale is bumped to the next attractive 9 that covers "
        f"the new opex floor. {n_chg} of {len(prices)} SKUs need a bump."
        if n_chg else
        "Locked rec leftover still prints on every SKU after baking news into the base. "
        "Challenge fees do not change.",
        s["body"],
    ))
    heads = ["Plan", "Size", "BE off", "BE on", "Δ BE", "Opex on",
             "Locked", "Rec now", "Left off", "Left on", "Fee?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(prices.itertuples(), start=1):
        spec[i] = "chg" if r.Changed else "rec"
        data.append([
            P(r.Plan, s["tdl"]), P(usd(r.Size), s["td"]),
            P(usd(r.BE_off), s["td"]), P(usd(r.BE_on), s["td"]),
            P(usd(r.BE_dlt), s["td"]),
            P(usd(r.S_opex_on), s["td"]),
            P(usd(r.Locked), s["td"]),
            P(usd(r.Rec), s["td"]),
            P(usd(r.Left_off), s["td"]),
            P(usd(r.Left_on), s["td"]),
            P("bump" if r.Changed else "same", s["td"]),
        ])
    story.append(grid(data, [
        24*mm, 16*mm, 18*mm, 18*mm, 16*mm, 18*mm,
        18*mm, 18*mm, 18*mm, 18*mm, 16*mm,
    ], spec))
    story.append(P(
        "Green = locked fee kept. Yellow = sale bumped. List is still round(sale / 0.65). "
        "Instant BE is year-1; evals are first-payout including the fee-refund circularity.",
        s["tiny"],
    ))

    story.append(P("4. Rec sale card after news-included", s["h1"]))
    heads = ["Plan", "$5k", "$10k", "$25k", "$50k", "$100k", "$200k"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, (plan, _fam) in enumerate(ANCHORS, start=1):
        cells = [P(plan, s["tdl"])]
        any_chg = False
        for sz in SIZES:
            sub = prices[(prices.Plan == plan) & (prices.Size == sz)]
            if sub.empty:
                cells.append(P("—", s["td"]))
                continue
            r = sub.iloc[0]
            any_chg = any_chg or bool(r.Changed)
            mark = " → " + usd(r.Rec) if r.Changed else ""
            cells.append(P(f"{usd(r.Locked)}{mark}", s["td"]))
        spec[i] = "chg" if any_chg else "rec"
        data.append(cells)
    story.append(grid(data, [
        28*mm, 32*mm, 32*mm, 32*mm, 32*mm, 32*mm, 32*mm,
    ], spec))

    story.append(P("5. Add-on rec — news removed", s["h1"]))
    story.append(P(
        "News is included in the challenge fee, so the 12% News SKU is gone and Swing at 20% "
        "is gone. Weekend holding stays 12% (Friday 22:00 flatten still on unless paid). "
        "Payout add-ons keep the locked percents: Weekly 8%, On Demand 80% 12%/15% Instant, "
        "90% 12%/15% Instant, 90% On Demand 20%/32% Instant. Stickers are still "
        "round(list × %). Extra E[X] for news is now inside challenge BE, not an add-on cost.",
        s["body"],
    ))
    heads = ["Add-on", "Evals %", "Instant %", "Was", "Now"]
    menu = [
        ("News trading", "12%", "12%", "paid SKU", "included — drop"),
        ("Weekend holding", "12%", "12%", "paid SKU", "unchanged"),
        ("Swing (news+weekend)", "20%", "20%", "bundle", "drop (news included)"),
        ("Weekly 80%", "8%", "8%", "paid SKU", "unchanged"),
        ("On Demand 80%", "12%", "15%", "paid SKU", "unchanged"),
        ("90% split", "12%", "15%", "paid SKU", "unchanged"),
        ("90% On Demand", "20%", "32%", "bundle", "unchanged"),
    ]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, row in enumerate(menu, start=1):
        spec[i] = "chg" if "drop" in row[4] or "included" in row[4] else "rec"
        data.append([P(c, s["tdl"] if j == 0 else s["td"]) for j, c in enumerate(row)])
    story.append(grid(data, [
        50*mm, 24*mm, 26*mm, 32*mm, 50*mm,
    ], spec))

    story.append(P("6. Remaining add-on leftover at $100k (news-on BE)", s["h1"]))
    a100 = addons[addons.Size == 100000]
    heads = ["Plan", "Add-on", "% list", "Sticker", "Extra E[X]", "After ads", "Prints?"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(a100.itertuples(), start=1):
        ok = flag(r.Left)
        spec[i] = "rec" if ok == "yes" else ("no" if ok == "NO" else None)
        data.append([
            P(r.Plan, s["tdl"]), P(r.Addon, s["tdl"]),
            P(f"{round(100 * r.Pct)}%", s["td"]),
            P(usd(r.Sticker), s["td"]),
            P(usd(r.Extra), s["td"]),
            P(usd(r.Left), s["td"]),
            P(ok, s["td"]),
        ])
    story.append(grid(data, [
        28*mm, 36*mm, 18*mm, 22*mm, 26*mm, 24*mm, 18*mm,
    ], spec))
    story.append(P(
        "After ads = sticker × 0.52 − extra E[X]. Instant 90% On Demand at 32% was already "
        "the year-1 floor. Challenge leftover is now after news is in the base, so combined "
        "carts are slightly tighter than the restricted-news book.",
        s["tiny"],
    ))

    story.append(P("7. Instant and Pro $100k — stickers after the drop", s["h1"]))
    focus = prices[(prices.Size == 100000) & (prices.Plan.isin(["Instant", "2-Step Pro"]))]
    heads = ["Plan", "Rec sale", "List", "Weekend", "Weekly", "OD 80%", "90%", "90% OD"]
    data = [[P(h, s["th"]) for h in heads]]
    spec = {}
    for i, r in enumerate(focus.itertuples(), start=1):
        spec[i] = "rec"
        lst = r.List
        data.append([
            P(r.Plan, s["tdl"]),
            P(usd(r.Rec), s["td"]),
            P(usd(lst), s["td"]),
            P(usd(sticker(lst, pct_for(r.Plan, "weekend"))), s["td"]),
            P(usd(sticker(lst, pct_for(r.Plan, "weekly"))), s["td"]),
            P(usd(sticker(lst, pct_for(r.Plan, "od80"))), s["td"]),
            P(usd(sticker(lst, pct_for(r.Plan, "split90"))), s["td"]),
            P(usd(sticker(lst, pct_for(r.Plan, "od90"))), s["td"]),
        ])
    story.append(grid(data, [
        28*mm, 22*mm, 18*mm, 24*mm, 22*mm, 24*mm, 22*mm, 24*mm,
    ], spec))
    story.append(P(
        "News sticker is $0. Do not keep a 12% News toggle on checkout. Do not keep Swing "
        "at 20% — that would charge again for news that is already in the fee.",
        s["tiny"],
    ))

    story.append(P("8. Read", s["h1"]))
    dlt = "; ".join(
        f"{r.Plan} BE {usd(r.BE_off)} → {usd(r.BE_on)} ({usd(r.BE_dlt)})"
        for r in prices[prices.Size == 100000].itertuples()
    )
    if n_chg == 0:
        verdict = (
            "Include news. Do not raise challenge fees. Drop the News add-on and the Swing "
            "bundle. Leave weekend and payout add-on percents as locked."
        )
    else:
        verdict = (
            f"Include news and bump the {n_chg} SKU(s) in yellow so the opex stack still prints. "
            "Drop the News add-on and the Swing bundle. Leave weekend and payout add-on percents."
        )
    story.append(P(
        f"$100k BE move: {dlt}. {verdict} First-payout refund is still challenge fee only "
        "(Instant is not refundable). News on evals and funded is the same rule — one policy.",
        s["body"],
    ))

    RESULTS.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=PAGE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=12 * mm, bottomMargin=11 * mm,
        title="Verodus news included — rec prices and add-ons",
        author="Verodus",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUT


def main():
    n_sims = 1200
    seed = 42
    if len(sys.argv) > 1:
        n_sims = int(sys.argv[1])
    off_p, off_f = run_book(n_sims, seed, news_allowed=False)
    on_p, on_f = run_book(n_sims, seed, news_allowed=True)
    off_b = blend(off_p)
    on_b = blend(on_p)
    prices = price_rows(off_b, on_b)
    addons = addon_rows(prices)
    RESULTS.mkdir(exist_ok=True)
    off_b.assign(News=False).to_csv(RESULTS / "verodus_news_restricted_blended.csv", index=False)
    on_b.assign(News=True).to_csv(RESULTS / "verodus_news_included_blended.csv", index=False)
    pd.concat([off_f, on_f], ignore_index=True).to_csv(
        RESULTS / "verodus_news_included_failures.csv", index=False,
    )
    prices.to_csv(RESULTS / "verodus_news_included_prices.csv", index=False)
    addons.to_csv(RESULTS / "verodus_news_included_addons.csv", index=False)
    path = build_pdf(off_b, on_b, prices, addons)
    print(on_b.to_string(index=False))
    print()
    print(prices[["Plan", "Size", "BE_off", "BE_on", "Locked", "Rec", "Changed", "Left_on"]].to_string(index=False))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
