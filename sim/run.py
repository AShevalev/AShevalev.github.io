#!/usr/bin/env python3
"""Run the Verodus Monte Carlo and write CSV + markdown results."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from verodus_mc import assert_floor_examples, run_monte_carlo

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def _pct(x) -> str:
    if pd.isna(x):
        return "—"
    return f"{100 * float(x):.2f}%"


def _usd(x) -> str:
    return f"${float(x):,.0f}"


def write_report(df_profiles, df_blend, df_skus, df_fails, n_sims: int, seed: int) -> str:
    lines = []
    lines.append("# Verodus challenge Monte Carlo")
    lines.append("")
    lines.append(f"Book: 3.5% Disciplined / 14.5% Average / 60% Aggressive / 22% Scalper. "
                 f"{n_sims:,} paths per profile ({n_sims * 4:,} per product). Seed {seed}. "
                 f"Simulated on a $100k account; payouts scale linearly to each SKU.")
    lines.append("")
    lines.append("Rules and sale prices from [verodus.com/faq-plans.html](https://www.verodus.com/faq-plans.html) "
                 "and live [`index-eval.js`](https://www.verodus.com/index-eval.js) (16 Aug 2026). "
                 "Instant refund = No on the live eval table; 1-Step / Lite / Pro refund 100% of the fee "
                 "on the first successful reward.")
    lines.append("")
    lines.append("## Blended pass / payout rates")
    lines.append("")
    lines.append("| Product | Phase 1 | Funded | P(pay) | Survives yr 1 | E[payout] on $100k | Avg days |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for _, r in df_blend.iterrows():
        lines.append(
            f"| {r['Product']} | {_pct(r['Phase1'])} | {_pct(r['Funded'])} | "
            f"{_pct(r['P_pay'])} | {_pct(r['P_yr1'])} | {_usd(r['E_payout_100k'])} | {r['Avg_days']:.0f} |"
        )
    lines.append("")
    lines.append("Industry anchors: Track360 blended pass 12.3% (range 5–14%); ~7% of buyers ever paid; "
                 "~45% of funded accounts receive a first payout. Daily DD 38–42% of fails, max DD 24–28%.")
    lines.append("")
    lines.append("## SKU pricing vs break-even")
    lines.append("")
    lines.append("E[payout] is the expected first performance reward (80% split, $100 minimum). "
                 "E[cost] at sale = E[payout] + P(pay)×sale when the fee is refunded. "
                 "Break-even fee solves `fee = E[payout] + P(pay)×fee` on refunding plans, "
                 "and `fee = E[payout]` on Instant. 20 / 40 / 60 are sale prices that leave that margin "
                 "after expected cost.")
    lines.append("")
    lines.append("| Plan | Size | List | Sale | P(pay) | E[payout] | E[cost] | BE | 20% | 40% | 60% | Sale m |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in df_skus.iterrows():
        lines.append(
            f"| {r['Product'].replace('Verodus ', '')} | {_usd(r['Size'])} | {_usd(r['List'])} | "
            f"{_usd(r['Sale'])} | {_pct(r['P_pay'])} | {_usd(r['E_payout'])} | {_usd(r['E_cost_at_sale'])} | "
            f"{_usd(r['BE'])} | {_usd(r['px_20'])} | {_usd(r['px_40'])} | {_usd(r['px_60'])} | "
            f"{100 * r['sale_m']:+.0f}% |"
        )
    lines.append("")
    lines.append("## Failure reasons (population-weighted share of all paths)")
    lines.append("")
    weights = {
        "Disciplined / Pro": 0.035,
        "Average Retail": 0.145,
        "Aggressive / Over-leveraged": 0.600,
        "Scalper / High-frequency": 0.220,
    }
    if not df_fails.empty:
        rows = []
        for product in df_fails["Product"].unique():
            sub = df_fails[df_fails.Product == product]
            reasons = {}
            for _, r in sub.iterrows():
                reasons[r["Reason"]] = reasons.get(r["Reason"], 0.0) + weights[r["Profile"]] * r["Share_of_profile"]
            for reason, share in sorted(reasons.items(), key=lambda kv: -kv[1])[:8]:
                rows.append((product, reason, share))
        lines.append("| Product | Reason | Share of paths |")
        lines.append("|---|---|---:|")
        for product, reason, share in rows:
            lines.append(f"| {product} | `{reason}` | {_pct(share)} |")
        lines.append("")
    lines.append("## Profile detail")
    lines.append("")
    lines.append("| Product | Profile | Phase 1 | P(pay) | E[payout] $100k | Avg days |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for _, r in df_profiles.iterrows():
        lines.append(
            f"| {r['Product']} | {r['Profile']} | {_pct(r['Phase1'])} | {_pct(r['P_pay'])} | "
            f"{_usd(r['E_payout_100k'])} | {r['Avg_days']:.0f} |"
        )
    lines.append("")
    lines.append("## What is not modeled")
    lines.append("")
    lines.append("- News-window clawback / second-violation hard breach (plans default `newsTradingAllowed=false`).")
    lines.append("- Friday flatten without the weekend-holding add-on.")
    lines.append("- KYC drop between pass and funded.")
    lines.append("- Split scaling to 85/90 and add-on weekly/on-demand cycles.")
    lines.append("- Payouts after the first (year-1 survival is a separate overlay, not extra dollars).")
    lines.append("- Copy-trading / HFT / pass-your-challenge filters.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-sims", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    assert_floor_examples()
    RESULTS.mkdir(parents=True, exist_ok=True)
    df_profiles, df_blend, df_skus, df_fails = run_monte_carlo(
        n_sims=args.n_sims, seed=args.seed
    )
    df_profiles.to_csv(RESULTS / "verodus_profiles.csv", index=False)
    df_blend.to_csv(RESULTS / "verodus_blended.csv", index=False)
    df_skus.to_csv(RESULTS / "verodus_skus.csv", index=False)
    df_fails.to_csv(RESULTS / "verodus_failures.csv", index=False)
    report = write_report(df_profiles, df_blend, df_skus, df_fails, args.n_sims, args.seed)
    (RESULTS / "REPORT.md").write_text(report)
    print(report)
    print(f"Wrote {RESULTS}")


if __name__ == "__main__":
    main()
