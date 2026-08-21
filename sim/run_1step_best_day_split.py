#!/usr/bin/env python3
"""Split 1-Step leftover: 3 any days vs 50% Best Day.

Same seed as the 1-Step slice of run_rule_alignment (seed + 2*10007).
News on. 1,200 paths per profile. Eval stays 10% / 50% Best Day / 0 min days.
"""
from __future__ import annotations

from copy import deepcopy

import numpy as np
import pandas as pd

from catalog import PRODUCTS, funded
from industry_book import PROFILES, simulate_funded_survival
from run_news_included import be_for, blend, run_one
from write_price_rec_pdf import leftover_after_opex, opex_stack

SALE = 379
SIZE = 100_000
N_SIMS = 1200
SEED = 42 + 2 * 10007

VARIANTS = {
    "old_3_any_days": funded(0.06, "hybrid", 0.04, min_days=3, cons=None),
    "best_day_50_no_min": funded(0.06, "hybrid", 0.04, min_days=0, cons=0.50),
    "best_day_50_and_3": funded(0.06, "hybrid", 0.04, min_days=3, cons=0.50),
}


def run_one_step(funded_rules, label):
    cfg = deepcopy(PRODUCTS["Verodus 1-Step"])
    cfg["funded"] = funded_rules
    rng = np.random.default_rng(SEED)
    rows = []
    for profile in PROFILES:
        n = paid = yr1 = 0
        payouts = []
        days = []
        for _ in range(N_SIMS):
            res = run_one(cfg, profile, rng, news_allowed=True)
            n += 1
            days.append(res["days"])
            payouts.append(res["payout"])
            if res["paid"]:
                paid += 1
                survived, _m = simulate_funded_survival(rng)
                if survived:
                    yr1 += 1
        rows.append({
            "Product": "Verodus 1-Step",
            "Plan": "1-Step",
            "Family": "1-step",
            "Refund": "first",
            "Profile": profile,
            "Weight": PROFILES[profile]["weight"],
            "Phase1": paid / n,
            "Funded": paid / n,
            "P_pay": paid / n,
            "P_yr1": yr1 / n,
            "E_payout_100k": float(np.mean(payouts)),
            "Avg_days": float(np.mean(days)),
            "News": True,
        })
        print(f"{label:22s} {profile:12s} P(pay)={paid / n:.3f}")
    blended = blend(pd.DataFrame(rows)).iloc[0]
    e, be, _ = be_for(blended, SIZE)
    left = leftover_after_opex(SALE, opex_stack(be, "1-Step", SIZE)["loaded"])
    return {
        "label": label,
        "P_pay": float(blended.P_pay),
        "E_first": float(blended.E_payout_100k),
        "BE": be,
        "Left_100k": left,
        "Avg_days": float(blended.Avg_days),
    }


def main():
    out = [run_one_step(rules, key) for key, rules in VARIANTS.items()]
    df = pd.DataFrame(out)
    print()
    print(df.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    base = df.iloc[0]
    for r in df.itertuples():
        if r.label == base.label:
            continue
        print(
            f"{r.label}: leftover {r.Left_100k - base.Left_100k:+.1f} vs 3 any days, "
            f"P(pay) {100 * (r.P_pay - base.P_pay):+.1f} pp, "
            f"BE {r.BE - base.BE:+.1f}"
        )


if __name__ == "__main__":
    main()
