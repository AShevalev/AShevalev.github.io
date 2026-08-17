#!/usr/bin/env python3
"""Split Instant leftover: 5-day floor vs which days sit in Best Day.

Same seed as the Instant slice of run_rule_alignment (seed + 10007).
News on. 1,200 paths per profile.
"""
from __future__ import annotations

from copy import deepcopy

import numpy as np
import pandas as pd

from catalog import P, PRODUCTS
from industry_book import PROFILES, simulate_funded_survival
from run_news_included import be_for, blend, run_one
from write_price_rec_pdf import leftover_after_opex, opex_stack

SALE = 439
SIZE = 100_000
N_SIMS = 1200
SEED = 42 + 10007

VARIANTS = {
    "prior_two_boxes": P(
        None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.005, 0.20
    ),
    "best_day_on_valid_only": P(
        None, 0.06, "trailing", 0.03, "intraday_peak", 0, 0.0, 0.20,
        cons_floor=0.005, cons_basis="sod", cons_op="ge",
    ),
    "aligned": P(
        None, 0.06, "trailing", 0.03, "intraday_peak", 0, 0.0, 0.20,
        cons_floor=0.005, cons_basis="sod", cons_op="ge",
    ),
}


def run_instant(phase, label):
    cfg = deepcopy(PRODUCTS["Verodus Instant"])
    cfg["phases"] = [phase]
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
            "Product": "Verodus Instant",
            "Plan": "Instant",
            "Family": "instant",
            "Refund": "none",
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
        print(f"{label:24s} {profile:12s} P(pay)={paid / n:.3f}")
    blended = blend(pd.DataFrame(rows)).iloc[0]
    e, be, _ = be_for(blended, SIZE)
    left = leftover_after_opex(SALE, opex_stack(be, "Instant", SIZE)["loaded"])
    return {
        "label": label,
        "P_pay": float(blended.P_pay),
        "P_yr1": float(blended.P_yr1),
        "E_first": float(blended.E_payout_100k),
        "E_y1": e,
        "BE": be,
        "Left_100k": left,
        "Avg_days": float(blended.Avg_days),
    }


def main():
    out = []
    for key, phase in VARIANTS.items():
        out.append(run_instant(phase, key))
    df = pd.DataFrame(out)
    print()
    print(df.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    base = df.iloc[0]
    for r in df.itertuples():
        if r.label == base.label:
            continue
        print(
            f"{r.label}: leftover {r.Left_100k - base.Left_100k:+.1f} vs prior, "
            f"P(pay) {100 * (r.P_pay - base.P_pay):+.1f} pp, "
            f"BE {r.BE - base.BE:+.1f}"
        )


if __name__ == "__main__":
    main()
