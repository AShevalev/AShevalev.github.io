#!/usr/bin/env python3
"""Run the industry-calibrated book across the top-20 catalog and write reports."""

from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from catalog import PRODUCTS
from industry_book import (
    PROFILES,
    SIM_BALANCE,
    break_even_fee,
    expected_refund_frac,
    margin_price,
    run_phase,
    simulate_funded_survival,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def run_one(config, profile, rng):
    split = config["split"]
    min_reward = config["min_reward"]
    instant = config["instant"]
    ok, bal, reason, d = run_phase(
        SIM_BALANCE, config["phases"][0], profile, rng,
        is_funded=False,
        min_reward=min_reward if instant else 0.0, split=split,
    )
    days = d
    if not ok:
        return dict(p1=False, funded=False, paid=False, payout=0.0,
                    reason=reason or "unknown", stage="p1", days=days)
    for i, phase in enumerate(config["phases"][1:], start=2):
        ok, bal, reason, d = run_phase(SIM_BALANCE, phase, profile, rng, is_funded=False)
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
        )
        days += d
        if not ok:
            return dict(p1=True, funded=False, paid=False, payout=0.0,
                        reason=reason or "unknown", stage="funded", days=days)
    profit = max(0.0, bal - SIM_BALANCE)
    payout = split * profit
    paid = payout + 1e-9 >= min_reward
    return dict(p1=True, funded=True, paid=paid, payout=payout if paid else 0.0,
                reason=None if paid else "min_reward", stage="paid", days=days)


def run_all(n_sims=1200, seed=42, only=None):
    rng = np.random.default_rng(seed)
    keys = [k for k in PRODUCTS if only is None or k in only]
    total = len(keys) * len(PROFILES) * n_sims
    done = 0
    t0 = time.time()
    rows = []
    fail_rows = []
    print(f"{len(keys)} products × {len(PROFILES)} profiles × {n_sims} = {total:,} paths\n")

    for key in keys:
        cfg = PRODUCTS[key]
        for profile in PROFILES:
            n = p1 = funded = paid = yr1 = 0
            days = []
            payouts = []
            fails = defaultdict(int)
            for _ in range(n_sims):
                res = run_one(cfg, profile, rng)
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
                if done % 200 == 0 or done == total:
                    eta = (time.time() - t0) / done * (total - done)
                    pct = 100 * done / total
                    sys.stdout.write(f"\r{key[:22]:22s} {profile:12s} {pct:5.1f}% ETA {eta:5.0f}s")
                    sys.stdout.flush()
            rows.append({
                "Product": key,
                "Firm": cfg["firm"],
                "Plan": cfg["plan"],
                "Family": cfg["family"],
                "Profile": profile,
                "Weight": PROFILES[profile]["weight"],
                "Phase1": p1 / n,
                "Funded": funded / n,
                "P_pay": paid / n,
                "P_yr1": yr1 / n,
                "E_payout_100k": float(np.mean(payouts)),
                "E_payout_if_paid": float(np.mean([x for x in payouts if x > 0])) if paid else 0.0,
                "Avg_days": float(np.mean(days)),
            })
            for r, c in fails.items():
                fail_rows.append({
                    "Product": key, "Profile": profile, "Reason": r,
                    "Share": c / n,
                })
    print(f"\nDone in {time.time() - t0:.1f}s")
    return pd.DataFrame(rows), pd.DataFrame(fail_rows)


def blend(df_profiles):
    rows = []
    for product, sub in df_profiles.groupby("Product", sort=False):
        w = sub["Weight"].to_numpy()
        cfg = PRODUCTS[product]
        rows.append({
            "Product": product,
            "Firm": cfg["firm"],
            "Plan": cfg["plan"],
            "Family": cfg["family"],
            "Discount": cfg["discount"],
            "Refund": cfg["refund"],
            "Split": cfg["split"],
            "Phase1": float(np.dot(w, sub["Phase1"])),
            "Funded": float(np.dot(w, sub["Funded"])),
            "P_pay": float(np.dot(w, sub["P_pay"])),
            "P_yr1": float(np.dot(w, sub["P_yr1"])),
            "E_payout_100k": float(np.dot(w, sub["E_payout_100k"])),
            "Avg_days": float(np.dot(w, sub["Avg_days"])),
        })
    return pd.DataFrame(rows)


def sku_table(df_blend):
    rows = []
    for _, b in df_blend.iterrows():
        cfg = PRODUCTS[b["Product"]]
        p_pay = b["P_pay"]
        k = expected_refund_frac(cfg["refund"], p_pay)
        for size, (lst, sale) in cfg["skus"].items():
            e_payout = b["E_payout_100k"] * (size / SIM_BALANCE)
            e_refund = k * sale
            e_cost = e_payout + e_refund
            be = break_even_fee(e_payout, k)
            rows.append({
                "Firm": cfg["firm"],
                "Plan": cfg["plan"],
                "Family": cfg["family"],
                "Size": int(size),
                "List": lst,
                "Sale": sale,
                "Discount": cfg["discount"] or "—",
                "Off": (1 - sale / lst) if lst else 0.0,
                "P_pay": p_pay,
                "E_payout": e_payout,
                "E_cost": e_cost,
                "BE": be,
                "px_20": margin_price(be, 0.20),
                "px_40": margin_price(be, 0.40),
                "px_60": margin_price(be, 0.60),
                "sale_m": (sale - e_cost) / sale if sale else np.nan,
                "list_m": (lst - (e_payout + k * lst)) / lst if lst else np.nan,
                "Refund": cfg["refund"],
                "Product": b["Product"],
            })
    return pd.DataFrame(rows)


def _pct(x):
    return "—" if pd.isna(x) else f"{100 * float(x):.1f}%"


def _usd(x):
    return f"${float(x):,.0f}"


def write_report(df_blend, df_skus, df_profiles, df_fails):
    lines = []
    lines.append("# Top-20 prop firms — industry-calibrated Monte Carlo")
    lines.append("")
    lines.append("**Read [`STRATEGY.md`](STRATEGY.md) first** — Verodus actions by plan and size.")
    lines.append("")
    lines.append("Book: **7% Pro / 22% Semi-skilled / 26% Average / 28% Aggressive / 17% Lottery**. "
                 "Calibrated so a standard 10/5 · 5/10 static 2-step (FTMO) lands near the "
                 "Track360 / FPFX / FTMO funnel. Same path library for every firm; only rules, "
                 "split, refund, and prices differ. Instant P(pay) is first-payout eligibility; "
                 "year-1 is the sustained-Instant figure.")
    lines.append("")
    lines.append("## Blended rates by product")
    lines.append("")
    lines.append("| Firm | Plan | Family | P1 | Funded | P(pay) | E[payout] $100k | Days | Refund | Split |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---|---:|")
    for _, r in df_blend.sort_values(["Family", "Firm"]).iterrows():
        lines.append(
            f"| {r['Firm']} | {r['Plan']} | {r['Family']} | {_pct(r['Phase1'])} | "
            f"{_pct(r['Funded'])} | {_pct(r['P_pay'])} | {_usd(r['E_payout_100k'])} | "
            f"{r['Avg_days']:.0f} | {r['Refund']} | {int(r['Split']*100)}% |"
        )
    lines.append("")
    lines.append("## Margins at shopper price (all SKUs)")
    lines.append("")
    lines.append("| Firm | Plan | Size | List | Sale | Off | P(pay) | E[payout] | E[cost] | BE | 40% | Sale m |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    show = df_skus.sort_values(["Family", "Firm", "Plan", "Size"])
    for _, r in show.iterrows():
        lines.append(
            f"| {r['Firm']} | {r['Plan']} | {_usd(r['Size'])} | {_usd(r['List'])} | "
            f"{_usd(r['Sale'])} | {_pct(r['Off'])} | {_pct(r['P_pay'])} | {_usd(r['E_payout'])} | "
            f"{_usd(r['E_cost'])} | {_usd(r['BE'])} | {_usd(r['px_40'])} | {100*r['sale_m']:+.0f}% |"
        )
    lines.append("")
    lines.append("## $5k / $10k / $100k snapshot (sale margin)")
    lines.append("")
    for size in (5000, 10000, 100000):
        sub = df_skus[df_skus.Size == size].sort_values("sale_m")
        if sub.empty:
            continue
        lines.append(f"### { _usd(size) }")
        lines.append("")
        lines.append("| Firm | Plan | Sale | P(pay) | E[cost] | Sale m | vs Verodus peer |")
        lines.append("|---|---|---:|---:|---:|---:|---|")
        for _, r in sub.iterrows():
            lines.append(
                f"| {r['Firm']} | {r['Plan']} | {_usd(r['Sale'])} | {_pct(r['P_pay'])} | "
                f"{_usd(r['E_cost'])} | {100*r['sale_m']:+.0f}% | {r['Family']} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-sims", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    df_p, df_f = run_all(n_sims=args.n_sims, seed=args.seed, only=args.only)
    df_b = blend(df_p)
    df_s = sku_table(df_b)
    df_p.to_csv(RESULTS / "industry_profiles.csv", index=False)
    df_b.to_csv(RESULTS / "industry_blended.csv", index=False)
    df_s.to_csv(RESULTS / "industry_skus.csv", index=False)
    df_f.to_csv(RESULTS / "industry_failures.csv", index=False)
    report = write_report(df_b, df_s, df_p, df_f)
    (RESULTS / "INDUSTRY_REPORT.md").write_text(report)
    print(df_b.to_string(index=False))
    print(f"\nWrote {RESULTS}")


if __name__ == "__main__":
    main()
