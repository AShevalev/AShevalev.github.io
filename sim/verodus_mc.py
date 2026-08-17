"""
Verodus challenge Monte Carlo — revised from the Realistic Version.

Rule sources (16 Aug 2026):
  - https://www.verodus.com/faq-plans.html
  - https://www.verodus.com/instant.html
  - https://www.verodus.com/1-step.html
  - https://www.verodus.com/2-step-lite.html
  - https://www.verodus.com/2-step-pro.html
  - https://www.verodus.com/index-eval.js  (live SKU list/sale prices)
  - Catalog PDF 13 Aug 2026 (runtime plans table; same SKUs)

Revisions vs the attached Realistic Version
------------------------------------------
1. Daily SOD drawdown is a fixed dollar of *initial* balance measured from
   start-of-day equity (`sod - start * daily_dd`), not `sod * (1 - daily_dd)`.
   Instant stays `day_peak - start * 0.03` (official: 3% of start from the
   day's equity high). Pricing table quotes dollars of initial ($200 = 4%
   on $5k 1-Step).
2. Instant fee refund is **No** on the live eval table. 1-Step / Lite / Pro
   refund 100% of the fee on the first successful reward.
3. Instant default split is 80%. Eval default split is 80%, scales later
   (not modeled). $100 minimum reward is enforced before a path counts as paid.
4. First-payout profit is taken from the simulated funded (or Instant) balance
   so E[X] is in dollars, then scaled linearly across SKU sizes.
5. Eval / first-payout horizon capped at 400 days (officially unlimited, but
   30-day inactivity already kills idle paths; 2500-day walks were wasted).
6. Hybrid floor matches the published $100k example (trails, locks at initial).
7. Pricing layer: break-even fee accounts for the refund circularity on evals.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

# =============================================================================
# 1. TRADER PROFILES (unchanged mix; documented vs industry)
# =============================================================================
# Industry funnel (Track360 2026, FPFX 300k accounts, FundedNext/FTMO 2023-25):
#   purchase → Phase 1 25-35% → funded 5-14% (blended 12.3%) → ever paid ~7%
#   of buyers. ~45% of funded get a first payout (Track360); FundedNext 26-32%.
#   Failures: daily DD 38-42%, max DD 24-28%, time 18-22%, forbidden 6-10%,
#   abandon 4-8%. 60-70% of fails are a drawdown breach.
# This book is 3.5% pro / 14.5% average / 60% aggressive / 22% scalper —
# heavier on over-leverage than a 5-14% pass-rate book, which is the point
# for pricing (most buyers are not the FPFX-average passer).

SENSITIVITIES = {
    "Disciplined / Pro": (0.53, 1.65, 2, (0.0040, 0.0080), 0.00012),
    "Average Retail": (0.47, 1.10, 4, (0.0100, 0.0180), 0.00030),
    "Aggressive / Over-leveraged": (0.41, 0.90, 6, (0.0200, 0.0350), 0.00050),
    "Scalper / High-frequency": (0.54, 0.75, 9, (0.0060, 0.0120), 0.00070),
}

ROOM_AWARENESS = {
    "Disciplined / Pro": 0.95,
    "Average Retail": 0.55,
    "Aggressive / Over-leveraged": 0.10,
    "Scalper / High-frequency": 0.30,
}

PRODUCT_POPULATION_WEIGHTS = {
    "default": {
        "Disciplined / Pro": 0.035,
        "Average Retail": 0.145,
        "Aggressive / Over-leveraged": 0.600,
        "Scalper / High-frequency": 0.220,
    }
}

# =============================================================================
# 2. MARKET PARAMETERS
# =============================================================================
FRICTION_BASE = 0.00032
TILT_SPIKE = 0.14
TILT_DECAY = 0.80
INACTIVITY_LIMIT = 30
SAFETY_MAX_DAYS = 400

REGIME_P = np.array(
    [
        [0.86, 0.12, 0.02, 0.00],
        [0.09, 0.78, 0.12, 0.01],
        [0.03, 0.18, 0.68, 0.11],
        [0.01, 0.07, 0.24, 0.68],
    ]
)
REGIME_WR = [1.03, 1.00, 0.89, 0.76]
REGIME_RRR = [0.94, 1.00, 1.18, 1.42]
REGIME_FRIC = [0.92, 1.00, 1.32, 2.05]
REGIME_SHOCK = [0.0017, 0.0042, 0.013, 0.032]

SESSIONS = [
    (0.80, 0.18),
    (1.05, 0.32),
    (1.22, 0.38),
    (0.93, 0.12),
]
SESSION_P = np.array([s[1] for s in SESSIONS], dtype=float)

# =============================================================================
# 3. VERODUS PRODUCTS — FAQ / live rules
# =============================================================================
# Instant: funded day 1. 6% trailing HWM (never locks). Daily 3% of start from
#   day's equity high. No min trading days. 20% Best Day of Positive Days'
#   Profit; a day counts only if it closes more than 0.5% of EOD balance.
#   $100 min. Split 80%. No refund.
# 1-Step: 10% target, no min days, 50% Best Day of Positive Days' Profit,
#   4% daily from SOD equity (fixed $ of initial), 6% hybrid (lock at initial).
#   Funded: same DD, no min days, 50% Best Day. 100% fee refund on first reward.
# Lite: P1 8% / P2 5%, 5 days each, 4% daily, 8% static eval and funded.
# Pro:  P1 10% / P2 5%, 5 days each, 5% daily, 10% static eval and funded.

PRODUCTS = {
    "Verodus Instant": {
        "phases": [
            {
                "target": None,
                "max_dd": 0.06,
                "floor_type": "trailing",
                "daily_dd": 0.03,
                "daily_dd_type": "intraday_peak",
                "min_days": 0,
                "valid_day_threshold": 0.0,
                "consistency": 0.20,
                "consistency_floor": 0.005,
                "consistency_basis": "eod",
            }
        ],
        "funded": None,
        "instant": True,
        "refund_on_first_payout": False,
        "split": 0.80,
        "min_reward": 100.0,
    },
    "Verodus 1-Step": {
        "phases": [
            {
                "target": 0.10,
                "max_dd": 0.06,
                "floor_type": "hybrid",
                "daily_dd": 0.04,
                "daily_dd_type": "sod",
                "min_days": 0,
                "valid_day_threshold": 0.0,
                "consistency": 0.50,
            }
        ],
        "funded": {
            "target": None,
            "max_dd": 0.06,
            "floor_type": "hybrid",
            "daily_dd": 0.04,
            "daily_dd_type": "sod",
            "min_days": 0,
            "valid_day_threshold": 0.0,
            "consistency": 0.50,
        },
        "instant": False,
        "refund_on_first_payout": True,
        "split": 0.80,
        "min_reward": 100.0,
    },
    "Verodus 2-Step Lite": {
        "phases": [
            {
                "target": 0.08,
                "max_dd": 0.08,
                "floor_type": "static",
                "daily_dd": 0.04,
                "daily_dd_type": "sod",
                "min_days": 5,
                "valid_day_threshold": 0.0,
                "consistency": None,
            },
            {
                "target": 0.05,
                "max_dd": 0.08,
                "floor_type": "static",
                "daily_dd": 0.04,
                "daily_dd_type": "sod",
                "min_days": 5,
                "valid_day_threshold": 0.0,
                "consistency": None,
            },
        ],
        "funded": {
            "target": None,
            "max_dd": 0.08,
            "floor_type": "static",
            "daily_dd": 0.04,
            "daily_dd_type": "sod",
            "min_days": 3,
            "valid_day_threshold": 0.0,
            "consistency": None,
        },
        "instant": False,
        "refund_on_first_payout": True,
        "split": 0.80,
        "min_reward": 100.0,
    },
    "Verodus 2-Step Pro": {
        "phases": [
            {
                "target": 0.10,
                "max_dd": 0.10,
                "floor_type": "static",
                "daily_dd": 0.05,
                "daily_dd_type": "sod",
                "min_days": 5,
                "valid_day_threshold": 0.0,
                "consistency": None,
            },
            {
                "target": 0.05,
                "max_dd": 0.10,
                "floor_type": "static",
                "daily_dd": 0.05,
                "daily_dd_type": "sod",
                "min_days": 5,
                "valid_day_threshold": 0.0,
                "consistency": None,
            },
        ],
        "funded": {
            "target": None,
            "max_dd": 0.10,
            "floor_type": "static",
            "daily_dd": 0.05,
            "daily_dd_type": "sod",
            "min_days": 3,
            "valid_day_threshold": 0.0,
            "consistency": None,
        },
        "instant": False,
        "refund_on_first_payout": True,
        "split": 0.80,
        "min_reward": 100.0,
    },
}

# Recommended VERO35 card (16 Aug 2026) — sale = shopper price, list = sale ÷ 0.65.
SKUS = {
    "Verodus Instant": {
        5_000: (75, 49),
        10_000: (106, 69),
        25_000: (214, 139),
        50_000: (368, 239),
        100_000: (675, 439),
    },
    "Verodus 1-Step": {
        5_000: (55, 36),
        10_000: (92, 60),
        25_000: (185, 120),
        50_000: (297, 193),
        100_000: (515, 335),
        200_000: (1006, 654),
    },
    "Verodus 2-Step Lite": {
        5_000: (65, 42),
        10_000: (85, 55),
        25_000: (145, 94),
        50_000: (229, 149),
        100_000: (414, 269),
        200_000: (768, 499),
    },
    "Verodus 2-Step Pro": {
        5_000: (69, 45),
        10_000: (91, 59),
        25_000: (146, 95),
        50_000: (245, 159),
        100_000: (445, 289),
        200_000: (888, 577),
    },
}

SIZES = (5_000, 10_000, 25_000, 50_000, 100_000, 200_000)
SIM_BALANCE = 100_000.0


# =============================================================================
# 4. ENGINE
# =============================================================================
def get_floor(hwm: float, start: float, max_dd: float, floor_type: str) -> float:
    if floor_type == "static":
        return start * (1.0 - max_dd)
    if floor_type == "trailing":
        return hwm * (1.0 - max_dd)
    trailing = hwm * (1.0 - max_dd)
    locked = start * (1.0 - max_dd)
    return min(max(trailing, locked), start)


def daily_floor(rules: dict, start: float, sod: float, day_peak: float) -> float:
    dd = rules["daily_dd"]
    if rules["daily_dd_type"] == "intraday_peak":
        return day_peak - start * dd
    return sod - start * dd


def simulate_trade(wr, rrr, risk_amt, regime, tilt, vol, rng):
    friction = (risk_amt / 0.01) * FRICTION_BASE * REGIME_FRIC[regime]
    friction *= (1.0 + 0.42 * tilt) * vol

    shock_p = REGIME_SHOCK[regime] * (1.0 + 0.38 * tilt)
    if rng.random() < shock_p:
        return -risk_amt * rng.uniform(1.5, 2.6) - friction

    adj_wr = np.clip(wr * REGIME_WR[regime] * (1.0 - 0.16 * tilt), 0.21, 0.70)
    if rng.random() < adj_wr:
        actual_rrr = rrr * REGIME_RRR[regime] * rng.uniform(0.78, 1.20)
        actual_rrr *= 1.0 - 0.11 * tilt
        return risk_amt * actual_rrr - friction
    slip = 1.0 + 0.20 * tilt
    return -risk_amt * min(slip, 2.1) - friction


def _consistency_ok(positive_pnls: list[float], cons: Optional[float]) -> bool:
    if cons is None:
        return True
    if not positive_pnls:
        return False
    best = max(positive_pnls)
    total = sum(positive_pnls)
    return best <= total * cons + 1e-12


def _counts_for_best_day(day_pnl, sod, eod, start, rules) -> bool:
    floor = rules.get("consistency_floor")
    if floor is None:
        return day_pnl > 0
    basis = rules.get("consistency_basis", "eod")
    if basis == "sod":
        denom = sod
    elif basis == "initial":
        denom = start
    else:
        denom = eod
    return denom > 0 and day_pnl > denom * floor


def run_phase(start_balance, rules, sens, profile_name, rng, is_funded=False,
              min_reward=0.0, split=0.80):
    wr, rrr, tpd, risk_range, violation_hazard = sens
    room_awareness = ROOM_AWARENESS[profile_name]

    balance = start_balance
    hwm = start_balance
    start = start_balance

    days = 0
    valid_days = 0
    consecutive_inactive = 0
    positive_pnls: list[float] = []
    has_profitable_trade = False

    tilt = 0.0
    regime = 1
    consecutive_losses = 0

    while days < SAFETY_MAX_DAYS:
        days += 1

        if consecutive_inactive >= INACTIVITY_LIMIT:
            return False, balance, "inactivity", days

        if rng.random() < violation_hazard:
            return False, balance, "rule_violation", days

        regime = int(rng.choice(4, p=REGIME_P[regime]))

        activity = 0.71 + 0.16 * (1.0 - tilt)
        if is_funded:
            activity *= 0.90

        if rng.random() > activity:
            consecutive_inactive += 1
            tilt *= TILT_DECAY
            continue

        consecutive_inactive = 0
        sod = balance
        day_peak = balance
        day_pnl = 0.0
        traded = False

        n_trades = max(1, int(np.clip(tpd * (1.0 + 0.42 * tilt), 1, tpd * 1.9)))

        for _ in range(n_trades):
            vol = SESSIONS[int(rng.choice(len(SESSIONS), p=SESSION_P))][0]

            floor = get_floor(hwm, start, rules["max_dd"], rules["floor_type"])
            d_floor = daily_floor(rules, start, sod, day_peak)

            room = min(balance - floor, balance - d_floor)
            stand_down_threshold = balance * 0.0015 * (0.2 + 0.8 * room_awareness)
            if room < stand_down_threshold:
                break

            base_risk = rng.uniform(*risk_range)
            tilt_mult = 1.0 + 0.95 * tilt
            if consecutive_losses >= 2:
                tilt_mult *= 1.0 + 0.10 * min(consecutive_losses, 4)

            room_ratio = room / (balance + 1e-9)
            adaptive = 1.0
            if room_ratio < 0.04:
                adaptive = max(0.45, room_ratio / 0.04)
            elif room_ratio < 0.08:
                adaptive = 0.68 + 0.32 * (room_ratio - 0.04) / 0.04
            adaptive = 1.0 - room_awareness * (1.0 - adaptive)

            risk_pct = min(base_risk * tilt_mult * adaptive, risk_range[1] * 1.35)
            if is_funded:
                risk_pct *= 0.75
            risk_amt = balance * risk_pct

            if room_awareness > 0.15:
                clamp_divisor = 1.2 + 2.3 * room_awareness
                if room < clamp_divisor * risk_amt:
                    risk_amt = room / clamp_divisor
                live_min_risk_floor = balance * risk_range[0] * 1.25
                risk_amt = max(risk_amt, min(live_min_risk_floor, max(room, 0.0)))

            if risk_amt <= 0:
                break

            pnl = simulate_trade(wr, rrr, risk_amt, regime, tilt, vol, rng)
            balance += pnl
            day_pnl += pnl
            traded = True

            hwm = max(hwm, balance)
            day_peak = max(day_peak, balance)

            floor = get_floor(hwm, start, rules["max_dd"], rules["floor_type"])
            d_floor = daily_floor(rules, start, sod, day_peak)

            if balance <= floor:
                return False, balance, "max_dd", days
            if balance <= d_floor:
                return False, balance, "daily_dd", days

            if pnl > 0:
                consecutive_losses = 0
                tilt *= TILT_DECAY * 0.89
                has_profitable_trade = True
            else:
                consecutive_losses += 1
                severity = min(1.0, abs(pnl) / (balance * 0.01 + 1e-9))
                tilt = min(0.90, tilt * TILT_DECAY + TILT_SPIKE + 0.18 * severity)

        if not traded:
            consecutive_inactive += 1
            continue

        if _counts_for_best_day(day_pnl, sod, balance, start, rules):
            positive_pnls.append(day_pnl)

        vdt = rules.get("valid_day_threshold", 0.0)
        if vdt > 0:
            if day_pnl >= sod * vdt:
                valid_days += 1
        else:
            valid_days += 1

        target = rules.get("target")
        passed = False
        if target is not None:
            if balance >= start * (1.0 + target) and valid_days >= rules["min_days"]:
                passed = _consistency_ok(positive_pnls, rules.get("consistency"))
        else:
            extra_ok = True if vdt > 0 else has_profitable_trade
            if valid_days >= rules["min_days"] and extra_ok:
                passed = _consistency_ok(positive_pnls, rules.get("consistency"))
            if passed and min_reward > 0:
                reward = split * max(0.0, balance - start)
                if reward + 1e-9 < min_reward:
                    passed = False

        if passed:
            return True, balance, None, days

        tilt *= TILT_DECAY

    return False, balance, "time_abandon", days


def simulate_funded_survival(rng, months=12):
    checkpoints = [(1, 1 - 0.41), (3, 1 - 0.28), (12, 1 - 0.24)]
    for month_label, survive_frac in checkpoints:
        if rng.random() > survive_frac:
            return False, month_label
    return True, months


# =============================================================================
# 5. PRICING MATH
# =============================================================================
def break_even_fee(e_payout: float, p_pay: float, refund: bool) -> float:
    """Fee at which E[revenue] = E[payout + refund]."""
    p_pay = min(max(p_pay, 0.0), 0.999)
    if refund:
        return e_payout / (1.0 - p_pay) if p_pay < 1 else float("inf")
    return e_payout


def margin_price(be: float, margin: float) -> float:
    return be / (1.0 - margin) if margin < 1 else float("inf")


def scale_payout(payout_at_sim: float, size: int) -> float:
    return payout_at_sim * (size / SIM_BALANCE)


# =============================================================================
# 6. RUNNER
# =============================================================================
@dataclass
class PathAgg:
    n: int = 0
    p1: int = 0
    p2: int = 0
    funded: int = 0
    paid: int = 0
    yr1: int = 0
    days: list = field(default_factory=list)
    payouts: list = field(default_factory=list)
    fails: dict = field(default_factory=lambda: defaultdict(int))


def print_progress(current, total, prefix="", bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    sys.stdout.write(f"\r{prefix} |{bar}| {percent * 100:5.1f}% ({current}/{total})")
    sys.stdout.flush()
    if current == total:
        sys.stdout.write("\n")


def run_one_path(config, sens, profile, rng):
    split = config["split"]
    min_reward = config["min_reward"]
    instant = config.get("instant", False)

    ok, bal, reason, d = run_phase(
        SIM_BALANCE,
        config["phases"][0],
        sens,
        profile,
        rng,
        is_funded=instant,
        min_reward=min_reward if instant else 0.0,
        split=split,
    )
    total_days = d
    stage = "p1"
    if not ok:
        return {
            "ok_p1": False,
            "ok_p2": False,
            "ok_funded": False,
            "paid": False,
            "payout": 0.0,
            "reason": reason or "unknown",
            "stage": stage,
            "days": total_days,
        }

    if len(config["phases"]) > 1:
        ok2, bal, reason2, d2 = run_phase(
            SIM_BALANCE, config["phases"][1], sens, profile, rng, is_funded=False
        )
        total_days += d2
        if not ok2:
            return {
                "ok_p1": True,
                "ok_p2": False,
                "ok_funded": False,
                "paid": False,
                "payout": 0.0,
                "reason": reason2 or "unknown",
                "stage": "p2",
                "days": total_days,
            }
        ok_p2 = True
    else:
        ok_p2 = True

    if config["funded"] is not None:
        okf, balf, reasonf, df_ = run_phase(
            SIM_BALANCE,
            config["funded"],
            sens,
            profile,
            rng,
            is_funded=True,
            min_reward=min_reward,
            split=split,
        )
        total_days += df_
        if not okf:
            return {
                "ok_p1": True,
                "ok_p2": ok_p2,
                "ok_funded": False,
                "paid": False,
                "payout": 0.0,
                "reason": reasonf or "unknown",
                "stage": "funded",
                "days": total_days,
            }
        profit = max(0.0, balf - SIM_BALANCE)
        payout = split * profit
        paid = payout + 1e-9 >= min_reward
        return {
            "ok_p1": True,
            "ok_p2": ok_p2,
            "ok_funded": True,
            "paid": paid,
            "payout": payout if paid else 0.0,
            "reason": None if paid else "min_reward",
            "stage": "funded",
            "days": total_days,
        }

    profit = max(0.0, bal - SIM_BALANCE)
    payout = split * profit
    paid = payout + 1e-9 >= min_reward
    return {
        "ok_p1": True,
        "ok_p2": True,
        "ok_funded": True,
        "paid": paid,
        "payout": payout if paid else 0.0,
        "reason": None if paid else "min_reward",
        "stage": "instant",
        "days": total_days,
    }


def run_monte_carlo(n_sims=4000, seed=42, model_post_funding_survival=True):
    rng = np.random.default_rng(seed)
    weights = PRODUCT_POPULATION_WEIGHTS["default"]
    aggs = {p: {pr: PathAgg() for pr in SENSITIVITIES} for p in PRODUCTS}

    total_paths = len(PRODUCTS) * len(SENSITIVITIES) * n_sims
    done = 0
    t0 = time.time()
    print(
        f"Running {len(PRODUCTS)} Verodus products × {len(SENSITIVITIES)} "
        f"profiles × {n_sims} sims = {total_paths:,} paths\n"
    )

    for product, config in PRODUCTS.items():
        for profile, sens in SENSITIVITIES.items():
            agg = aggs[product][profile]
            for _ in range(n_sims):
                res = run_one_path(config, sens, profile, rng)
                agg.n += 1
                agg.days.append(res["days"])
                agg.payouts.append(res["payout"])
                if res["ok_p1"]:
                    agg.p1 += 1
                if res["ok_p2"] and len(config["phases"]) > 1:
                    agg.p2 += 1
                if res["ok_funded"]:
                    agg.funded += 1
                if res["paid"]:
                    agg.paid += 1
                    if model_post_funding_survival:
                        survived, fail_month = simulate_funded_survival(rng)
                        if survived:
                            agg.yr1 += 1
                        else:
                            agg.fails[f"post_funding_m{fail_month}"] += 1
                elif res["reason"]:
                    key = res["reason"] if res["stage"] in ("p1", "instant") else f"{res['stage']}_{res['reason']}"
                    agg.fails[key] += 1

                done += 1
                if done % 80 == 0 or done == total_paths:
                    elapsed = time.time() - t0
                    eta = (elapsed / done) * (total_paths - done)
                    print_progress(
                        done,
                        total_paths,
                        prefix=f"{product[:18]:18s} {profile[:16]:16s} ETA {eta:5.0f}s",
                    )

    profile_rows = []
    fail_rows = []
    for product, by_prof in aggs.items():
        for profile, agg in by_prof.items():
            n = agg.n
            profile_rows.append(
                {
                    "Product": product,
                    "Profile": profile,
                    "Weight": weights[profile],
                    "N": n,
                    "Phase1": agg.p1 / n,
                    "Phase2": (agg.p2 / agg.p1) if agg.p1 and len(PRODUCTS[product]["phases"]) > 1 else np.nan,
                    "Funded": agg.funded / n,
                    "P_pay": agg.paid / n,
                    "P_yr1": agg.yr1 / n,
                    "E_payout_100k": float(np.mean(agg.payouts)),
                    "E_payout_if_paid_100k": float(np.mean([x for x in agg.payouts if x > 0])) if agg.paid else 0.0,
                    "Avg_days": float(np.mean(agg.days)),
                }
            )
            for reason, count in agg.fails.items():
                fail_rows.append(
                    {
                        "Product": product,
                        "Profile": profile,
                        "Reason": reason,
                        "Count": count,
                        "Share_of_profile": count / n,
                    }
                )

    df_profiles = pd.DataFrame(profile_rows)
    df_fails = pd.DataFrame(fail_rows)

    blend_rows = []
    for product in PRODUCTS:
        sub = df_profiles[df_profiles.Product == product]
        w = sub["Weight"].to_numpy()
        blend_rows.append(
            {
                "Product": product,
                "Phase1": float(np.dot(w, sub["Phase1"])),
                "Phase2_of_P1": float(np.nanmean(sub["Phase2"])) if sub["Phase2"].notna().any() else np.nan,
                "Funded": float(np.dot(w, sub["Funded"])),
                "P_pay": float(np.dot(w, sub["P_pay"])),
                "P_yr1": float(np.dot(w, sub["P_yr1"])),
                "E_payout_100k": float(np.dot(w, sub["E_payout_100k"])),
                "Avg_days": float(np.dot(w, sub["Avg_days"])),
                "refund": PRODUCTS[product]["refund_on_first_payout"],
                "split": PRODUCTS[product]["split"],
            }
        )
    df_blend = pd.DataFrame(blend_rows)

    sku_rows = []
    for _, brow in df_blend.iterrows():
        product = brow["Product"]
        p_pay = brow["P_pay"]
        refund = bool(brow["refund"])
        for size in SIZES:
            if size not in SKUS[product]:
                continue
            list_px, sale_px = SKUS[product][size]
            e_payout = scale_payout(brow["E_payout_100k"], size)
            if size == 5_000 and product == "Verodus Instant":
                # $100 min already applied at $100k scale (min $100 is tiny there).
                # Re-apply at $5k: 80% * 2.5% * $5k = $100 on a bare Instant qualify.
                e_payout = max(e_payout, 0.0)
            e_refund = p_pay * sale_px if refund else 0.0
            e_cost = e_payout + e_refund
            be = break_even_fee(e_payout, p_pay, refund)
            sku_rows.append(
                {
                    "Product": product,
                    "Size": size,
                    "List": list_px,
                    "Sale": sale_px,
                    "P_pay": p_pay,
                    "E_payout": e_payout,
                    "E_refund_at_sale": e_refund,
                    "E_cost_at_sale": e_cost,
                    "BE": be,
                    "px_20": margin_price(be, 0.20),
                    "px_40": margin_price(be, 0.40),
                    "px_60": margin_price(be, 0.60),
                    "sale_m": (sale_px - e_cost) / sale_px if sale_px else np.nan,
                    "list_m": (list_px - (e_payout + (p_pay * list_px if refund else 0.0))) / list_px,
                    "refund": refund,
                }
            )
    df_skus = pd.DataFrame(sku_rows)

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.1f} seconds")
    return df_profiles, df_blend, df_skus, df_fails


def assert_floor_examples():
    start = 100_000.0
    assert abs(get_floor(start, start, 0.06, "hybrid") - 94_000) < 1e-6
    assert abs(get_floor(105_000, start, 0.06, "hybrid") - 98_700) < 1e-6
    assert abs(get_floor(106_383, start, 0.06, "hybrid") - 100_000) < 0.02
    assert abs(get_floor(110_000, start, 0.06, "hybrid") - 100_000) < 1e-6
    assert abs(get_floor(110_000, start, 0.06, "trailing") - 103_400) < 1e-6
    assert abs(get_floor(start, start, 0.08, "static") - 92_000) < 1e-6
    assert PRODUCTS["Verodus 2-Step Lite"]["funded"]["max_dd"] == 0.08
    d = daily_floor({"daily_dd": 0.03, "daily_dd_type": "intraday_peak"}, start, start, 102_000)
    assert abs(d - (102_000 - 3_000)) < 1e-6
    d = daily_floor({"daily_dd": 0.04, "daily_dd_type": "sod"}, start, 105_000, 105_000)
    assert abs(d - 101_000) < 1e-6


if __name__ == "__main__":
    assert_floor_examples()
    df_profiles, df_blend, df_skus, df_fails = run_monte_carlo(n_sims=4000, seed=42)
    print("\nBLENDED")
    print(df_blend.to_string(index=False))
    print("\nSKUS")
    print(df_skus.to_string(index=False))
