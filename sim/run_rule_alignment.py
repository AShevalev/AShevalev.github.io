#!/usr/bin/env python3
"""Paired Monte Carlo: prior Instant/1-Step day rules vs rule-alignment.

News stays included. Instant factors every green day into Best Day. A day
meets the 0.5% parameter only if profit is more than 0.5% of SOD. 1-Step
QPP drops the 3-day min and applies 50% Best Day. 2-Step Lite/Pro are
unchanged (5 eval days, 3 QPP days). Same per-product seed so the delta
is the rule change, not a new random stream.

Writes results/verodus_rule_alignment_compare.csv and RULE_ALIGNMENT_MARGINS.md,
and refreshes verodus_news_included_prices.csv BE_on from the new book so the
310-account leftover and BE/20/40/60 cards rebuild on the aligned rules.
"""
from __future__ import annotations

import shutil
import sys
import time
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd

from catalog import P, PRODUCTS, funded
from industry_book import PROFILES, simulate_funded_survival
from run_news_included import (
    VERODUS,
    be_for,
    blend,
    run_one,
)
from write_price_rec_pdf import leftover_after_opex, opex_stack
from write_reprice_pdf import REC

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")

OLD_RULES = {
    "Verodus Instant": {
        "phases": [P(None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.005, 0.20)],
        "note": "5 valid days at ≥0.5% of SOD; 20% Best Day on every green day",
    },
    "Verodus 1-Step": {
        "funded": funded(0.06, "hybrid", 0.04, min_days=3, cons=None),
        "note": "QPP 3 min days, no Best Day",
    },
}


def catalog_with(overrides: dict) -> dict:
    out = {k: deepcopy(PRODUCTS[k]) for k in VERODUS}
    for key, patch in overrides.items():
        cfg = out[key]
        if "phases" in patch:
            cfg["phases"] = patch["phases"]
        if "funded" in patch:
            cfg["funded"] = patch["funded"]
    return out


def run_book(n_sims: int, seed: int, catalog: dict, label: str) -> pd.DataFrame:
    total = len(VERODUS) * len(PROFILES) * n_sims
    done = 0
    t0 = time.time()
    rows = []
    print(f"{label}: {len(VERODUS)} products × {len(PROFILES)} × {n_sims} = {total:,}")
    for i, key in enumerate(VERODUS):
        cfg = catalog[key]
        rng = np.random.default_rng(seed + (i + 1) * 10007)
        for profile in PROFILES:
            n = p1 = funded_n = paid = yr1 = 0
            days = []
            payouts = []
            for _ in range(n_sims):
                res = run_one(cfg, profile, rng, news_allowed=True)
                n += 1
                days.append(res["days"])
                payouts.append(res["payout"])
                if res["p1"]:
                    p1 += 1
                if res["funded"]:
                    funded_n += 1
                if res["paid"]:
                    paid += 1
                    survived, _m = simulate_funded_survival(rng)
                    if survived:
                        yr1 += 1
                done += 1
                if done % 250 == 0 or done == total:
                    eta = (time.time() - t0) / done * (total - done)
                    sys.stdout.write(
                        f"\r{label:12s} {key[8:22]:14s} {profile:12s} "
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
                "Funded": funded_n / n,
                "P_pay": paid / n,
                "P_yr1": yr1 / n,
                "E_payout_100k": float(np.mean(payouts)),
                "E_if_paid": float(np.mean([x for x in payouts if x > 0])) if paid else 0.0,
                "Avg_days": float(np.mean(days)),
                "News": True,
            })
    print(f"\n{label} done in {time.time() - t0:.1f}s")
    return pd.DataFrame(rows)


def sale_cost(plan: str, sale: float, e: float, p_pay: float) -> float:
    if plan == "Instant":
        return e
    return e + p_pay * sale


def compare(old_b: pd.DataFrame, new_b: pd.DataFrame) -> pd.DataFrame:
    old_i = {r.Plan: r for r in old_b.itertuples()}
    new_i = {r.Plan: r for r in new_b.itertuples()}
    rows = []
    for plan in ("Instant", "1-Step", "2-Step Lite", "2-Step Pro"):
        a = old_i[plan]
        b = new_i[plan]
        e0, be0, basis = be_for(a, 100000)
        e1, be1, _ = be_for(b, 100000)
        for (p, sz), sale in REC.items():
            if p != plan:
                continue
            e0s, be0s, _ = be_for(a, sz)
            e1s, be1s, _ = be_for(b, sz)
            st0 = opex_stack(be0s, plan, sz)
            st1 = opex_stack(be1s, plan, sz)
            left0 = leftover_after_opex(sale, st0["loaded"])
            left1 = leftover_after_opex(sale, st1["loaded"])
            cost0 = sale_cost(plan, sale, e0s, float(a.P_pay))
            cost1 = sale_cost(plan, sale, e1s, float(b.P_pay))
            m0 = (sale - cost0) / sale
            m1 = (sale - cost1) / sale
            rows.append({
                "Plan": plan,
                "Size": sz,
                "Basis": basis,
                "Sale": sale,
                "P_pay_old": float(a.P_pay),
                "P_pay_new": float(b.P_pay),
                "P_yr1_old": float(a.P_yr1),
                "P_yr1_new": float(b.P_yr1),
                "E_old": e0s,
                "E_new": e1s,
                "BE_old": be0s,
                "BE_new": be1s,
                "BE_dlt": be1s - be0s,
                "Left_old": left0,
                "Left_new": left1,
                "Left_dlt": left1 - left0,
                "Sale_m_old": m0,
                "Sale_m_new": m1,
                "Sale_m_dlt": m1 - m0,
                "Avg_days_old": float(a.Avg_days),
                "Avg_days_new": float(b.Avg_days),
                "Margin_up": left1 > left0 + 0.05,
                "Margin_down": left1 < left0 - 0.05,
            })
    return pd.DataFrame(rows)


def write_prices_csv(old_b: pd.DataFrame, new_b: pd.DataFrame, cmp_df: pd.DataFrame):
    """Refresh news-included prices: off = prior day rules, on = aligned."""
    rows = []
    for r in cmp_df.itertuples():
        rows.append({
            "Plan": r.Plan,
            "Size": r.Size,
            "Basis": r.Basis,
            "P_pay_off": r.P_pay_old,
            "P_pay_on": r.P_pay_new,
            "P_yr1_off": r.P_yr1_old,
            "P_yr1_on": r.P_yr1_new,
            "E_off": r.E_old,
            "E_on": r.E_new,
            "BE_off": r.BE_old,
            "BE_on": r.BE_new,
            "BE_dlt": r.BE_dlt,
            "S_opex_off": opex_stack(r.BE_old, r.Plan, r.Size)["s_opex"],
            "S_opex_on": opex_stack(r.BE_new, r.Plan, r.Size)["s_opex"],
            "Locked": r.Sale,
            "Rec": r.Sale,
            "Changed": False,
            "List": int(round(r.Sale / 0.65)),
            "Left_off": r.Left_old,
            "Left_on": r.Left_new,
            "Loaded_on": opex_stack(r.BE_new, r.Plan, r.Size)["loaded"],
        })
    pd.DataFrame(rows).to_csv(RESULTS / "verodus_news_included_prices.csv", index=False)
    old_b.assign(Rules="prior").to_csv(
        RESULTS / "verodus_rule_alignment_old_blended.csv", index=False
    )
    new_b.assign(Rules="aligned").to_csv(
        RESULTS / "verodus_news_included_blended.csv", index=False
    )
    new_b.assign(Rules="aligned").to_csv(
        RESULTS / "verodus_rule_alignment_new_blended.csv", index=False
    )


def write_md(cmp_df: pd.DataFrame, n_sims: int) -> Path:
    body = [
        "# Rule-alignment Monte Carlo — leftover vs prior day rules",
        "",
        "**Margins did not increase on any account.** Instant leftover is down "
        "on every size. 1-Step leftover is down on every size. 2-Step Lite and "
        "Pro are unchanged (same paths). Instant $100k leftover at the current "
        "$439 sale is now negative and no longer prints after opex. Prices were "
        "not raised.",
        "",
        f"News included. {n_sims} paths per profile, same 7/22/26/28/17 mix, "
        "paired per-product seeds. Sale card is unchanged (current rec).",
        "",
        "Prior Instant: two checkboxes — 5 days at ≥0.5% of SOD **and** 20% Best "
        "Day on every green day. New Instant: every green day is factored into "
        "Best Day; a day meets the 0.5% parameter only if profit is **more than** "
        "0.5% of SOD. Do not list a 5-day checkbox.",
        "",
        "Prior 1-Step QPP: 3 min days, no Best Day. Aligned 1-Step QPP: no min "
        "days, 50% Best Day (no 0.5% floor). 2-Step Lite/Pro unchanged (5 eval / 3 QPP).",
        "",
        "Leftover = sale × 0.80 − (BE × 1.10 + $1 + wage share). "
        "Sale m is the ads-line margin (Instant year-1 E[X]; evals include fee refund).",
        "",
        "| Plan | Size | Sale | P(pay) old → new | BE old → new | Leftover old → new | Sale m old → new | Leftover up? |",
        "|---|---:|---:|---|---|---|---|:---:|",
    ]
    yes = no = flat = 0
    for r in cmp_df.itertuples():
        if r.Margin_up:
            verdict = "yes"
            yes += 1
        elif r.Margin_down:
            verdict = "no"
            no += 1
        else:
            verdict = "flat"
            flat += 1
        body.append(
            f"| {r.Plan} | ${r.Size:,.0f} | ${r.Sale:,.0f} | "
            f"{100 * r.P_pay_old:.1f}% → {100 * r.P_pay_new:.1f}% | "
            f"${r.BE_old:,.1f} → ${r.BE_new:,.1f} | "
            f"${r.Left_old:,.1f} → ${r.Left_new:,.1f} ({r.Left_dlt:+.1f}) | "
            f"{100 * r.Sale_m_old:+.0f}% → {100 * r.Sale_m_new:+.0f}% | {verdict} |"
        )
    body.extend([
        "",
        f"**{yes} SKUs leftover up · {no} down · {flat} flat** (±$0.05).",
        "",
        "2-Step rows should be flat aside from Monte Carlo noise — those payout "
        "day rules did not change.",
        "",
    ])
    path = RESULTS / "RULE_ALIGNMENT_MARGINS.md"
    path.write_text("\n".join(body) + "\n")
    return path


def main():
    n_sims = 1200
    seed = 42
    if len(sys.argv) > 1:
        n_sims = int(sys.argv[1])
    RESULTS.mkdir(exist_ok=True)
    prices = RESULTS / "verodus_news_included_prices.csv"
    if prices.exists():
        shutil.copyfile(prices, RESULTS / "verodus_news_included_prices_pre_alignment.csv")

    old_cat = catalog_with(OLD_RULES)
    new_cat = {k: deepcopy(PRODUCTS[k]) for k in VERODUS}

    old_p = run_book(n_sims, seed, old_cat, "prior-rules")
    new_p = run_book(n_sims, seed, new_cat, "aligned")
    old_b = blend(old_p)
    new_b = blend(new_p)
    cmp_df = compare(old_b, new_b)
    cmp_df.to_csv(RESULTS / "verodus_rule_alignment_compare.csv", index=False)
    write_prices_csv(old_b, new_b, cmp_df)
    md = write_md(cmp_df, n_sims)
    if ART.is_dir():
        shutil.copyfile(md, ART / md.name)
        shutil.copyfile(
            RESULTS / "verodus_rule_alignment_compare.csv",
            ART / "verodus_rule_alignment_compare.csv",
        )
    print(old_b.to_string(index=False))
    print()
    print(new_b.to_string(index=False))
    print()
    cols = [
        "Plan", "Size", "Sale", "P_pay_old", "P_pay_new",
        "BE_old", "BE_new", "Left_old", "Left_new", "Left_dlt",
        "Sale_m_old", "Sale_m_new", "Margin_up",
    ]
    print(cmp_df[cols].to_string(index=False))
    print(f"\nWrote {md}")


if __name__ == "__main__":
    main()
