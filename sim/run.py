#!/usr/bin/env python3
"""Run the Verodus Monte Carlo and write CSV + markdown results."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from verodus_mc import (
    PRODUCTS,
    SIZES,
    SKUS,
    assert_floor_examples,
    break_even_fee,
    margin_price,
    run_monte_carlo,
    scale_payout,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def _pct(x) -> str:
    if pd.isna(x):
        return "—"
    return f"{100 * float(x):.2f}%"


def _usd(x) -> str:
    return f"${float(x):,.0f}"


INDUSTRY_WEIGHTS = {
    "Disciplined / Pro": 0.12,
    "Average Retail": 0.18,
    "Aggressive / Over-leveraged": 0.50,
    "Scalper / High-frequency": 0.20,
}

DEFAULT_WEIGHTS = {
    "Disciplined / Pro": 0.035,
    "Average Retail": 0.145,
    "Aggressive / Over-leveraged": 0.600,
    "Scalper / High-frequency": 0.220,
}


def _reweight(df_profiles: pd.DataFrame, weights: dict) -> pd.DataFrame:
    rows = []
    for product, sub in df_profiles.groupby("Product"):
        w = sub["Profile"].map(weights).to_numpy()
        rows.append(
            {
                "Product": product,
                "Phase1": float((w * sub["Phase1"]).sum()),
                "Funded": float((w * sub["Funded"]).sum()),
                "P_pay": float((w * sub["P_pay"]).sum()),
                "P_yr1": float((w * sub["P_yr1"]).sum()),
                "E_payout_100k": float((w * sub["E_payout_100k"]).sum()),
            }
        )
    return pd.DataFrame(rows)


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
    lines.append("## Industry pass / fail research")
    lines.append("")
    lines.append("Credible published numbers (not the viral “90% fail” line, which FTMO does not disclose):")
    lines.append("")
    lines.append("| Source | Finding |")
    lines.append("|---|---|")
    lines.append("| Track360, Jul 2026 | Blended pass 12.3% across tracked programs; range 5–14%. ~7% of all buyers ever paid. ~45% of funded accounts get a first payout. 60–70% of fails are daily or max drawdown. 30–40% of fails repurchase within 90 days. |")
    lines.append("| FPFX Technologies / Finance Magnates (300k+ accounts, ~10 firms) | ~14% pass an evaluation; ~45% of funded get a payout → ~7% of buyers ever paid. Average payout ~4% of notional. |")
    lines.append("| FundedNext transparency (2023) | Phase 1 ~25–35%; Phase 2 of those ~43%; combined ~10–11%. Daily DD 38–42% of fails, max DD 24–28%, time 18–22%, forbidden 6–10%, abandon 4–8%. 32–38% of funded breach in 30 days; 58–64% in 90 days. |")
    lines.append("| FTMO (archived 2023 stats, TradeLens / Arxum summaries) | Stage 1 ~32–37%, Stage 2 of those ~50–60%, combined ~10%. Pass rate falls with size ($10k 12–14% → $200k 7–9%). |")
    lines.append("| Topstep 2025 disclosure | 16.8% of Combines completed. |")
    lines.append("| The5%ers-style instant | Sustained funding 4–6% — Instant products pay less often than two-step evals. |")
    lines.append("")
    lines.append("Why traders fail, in order: **daily drawdown** (oversizing, floating loss at reset, revenge size), **max drawdown** (no stand-down as the floor trails or the static hole fills), **time / inactivity**, then news / weekend / copy-trading filters. Passing is mostly risk-budget math (≤1% per trade, 0.5–1% good days, skip bad sessions), not a higher win rate.")
    lines.append("")
    lines.append("This book is *stricter* than that funnel: blended P(pay) lands at 1.9–2.8% versus the industry ~7% ever-paid. Almost all payouts come from the 3.5% Disciplined cohort. Average Retail almost never collects; Aggressive and Scalper die on daily DD in 1–4 days. That is conservative for pricing (you will not underprice Lite/Pro the way the older 84/13.5/2.5 book did).")
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
    lines.append("## Industry-weighted sensitivity (12% pro)")
    lines.append("")
    lines.append("Same path library, reweighted to 12% Disciplined / 18% Average / 50% Aggressive / 20% Scalper "
                 "so blended P(pay) sits nearer the published ~7% ever-paid rate. "
                 "Use this if the 3.5% pro prior is too harsh.")
    lines.append("")
    ind = _reweight(df_profiles, INDUSTRY_WEIGHTS)
    lines.append("| Product | Phase 1 | Funded | P(pay) | E[payout] $100k |")
    lines.append("|---|---:|---:|---:|---:|")
    for _, r in ind.iterrows():
        lines.append(
            f"| {r['Product']} | {_pct(r['Phase1'])} | {_pct(r['Funded'])} | "
            f"{_pct(r['P_pay'])} | {_usd(r['E_payout_100k'])} |"
        )
    lines.append("")
    lines.append("| Plan | Size | Sale | P(pay) | E[payout] | BE | 40% | Sale m |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for _, brow in ind.iterrows():
        product = brow["Product"]
        p_pay = brow["P_pay"]
        refund = PRODUCTS[product]["refund_on_first_payout"]
        for size in SIZES:
            list_px, sale_px = SKUS[product][size]
            e_payout = scale_payout(brow["E_payout_100k"], size)
            e_refund = p_pay * sale_px if refund else 0.0
            e_cost = e_payout + e_refund
            be = break_even_fee(e_payout, p_pay, refund)
            lines.append(
                f"| {product.replace('Verodus ', '')} | {_usd(size)} | {_usd(sale_px)} | "
                f"{_pct(p_pay)} | {_usd(e_payout)} | {_usd(be)} | {_usd(margin_price(be, 0.40))} | "
                f"{100 * (sale_px - e_cost) / sale_px:+.0f}% |"
            )
    lines.append("")
    lines.append("## Read vs the 15 Aug peer PDFs")
    lines.append("")
    lines.append("Those reports used an 84 / 13.5 / 2.5 book and called Lite/Pro a hole "
                 "(sale m −32% / −46% at $5k). In *this* Realistic Version the 13.5% “can actually collect” "
                 "bucket is gone: Average Retail’s Lite P(pay) is 0.12%. VERO35 therefore prints on every SKU. "
                 "If a fatter skilled tail shows up in live CRM, switch to the 12% pro table above — "
                 "Instant $5k is still +~70%, Lite $5k still +~70%. The hole only returns if Average Retail "
                 "starts collecting at a few percent with four-figure first payouts.")
    lines.append("")
    lines.append("First-payout E[X] understates cost for the ~0.8% who survive a year. "
                 "Two extra cycles on year-1 survivors add roughly 0.6× E[payout] on Instant "
                 "and less on evals. Instant $5k would still be high-80s margin.")
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
    ind = _reweight(df_profiles, INDUSTRY_WEIGHTS)
    ind["Product"] = pd.Categorical(ind["Product"], list(PRODUCTS))
    ind = ind.sort_values("Product")
    ind.to_csv(RESULTS / "verodus_blended_industry12.csv", index=False)
    ind_skus = []
    for _, brow in ind.iterrows():
        product = brow["Product"]
        p_pay = brow["P_pay"]
        refund = PRODUCTS[product]["refund_on_first_payout"]
        for size in SIZES:
            list_px, sale_px = SKUS[product][size]
            e_payout = scale_payout(brow["E_payout_100k"], size)
            e_refund = p_pay * sale_px if refund else 0.0
            e_cost = e_payout + e_refund
            be = break_even_fee(e_payout, p_pay, refund)
            ind_skus.append(
                {
                    "Product": product,
                    "Size": size,
                    "List": list_px,
                    "Sale": sale_px,
                    "P_pay": p_pay,
                    "E_payout": e_payout,
                    "E_cost_at_sale": e_cost,
                    "BE": be,
                    "px_40": margin_price(be, 0.40),
                    "sale_m": (sale_px - e_cost) / sale_px,
                }
            )
    pd.DataFrame(ind_skus).to_csv(RESULTS / "verodus_skus_industry12.csv", index=False)
    report = write_report(df_profiles, df_blend, df_skus, df_fails, args.n_sims, args.seed)
    (RESULTS / "REPORT.md").write_text(report)
    print(report)
    print(f"Wrote {RESULTS}")


if __name__ == "__main__":
    main()
