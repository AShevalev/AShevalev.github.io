"""
Industry-calibrated prop-firm Monte Carlo.

Sensitivities are set so a standard FTMO-style 2-step
(10%/5% targets, 5% daily, 10% static, 4 min days) lands near the
published funnel:

  Phase 1  ~25-30%
  Funded   ~10-12%
  P(pay)   ~7%
  Year-1   ~1-3%

Sources: Track360 2026 (12.3% blended pass, ~7% ever paid),
FPFX 300k accounts, FundedNext/FTMO stage tables, Topstep 16.8% Combine.
Failure mix target: daily DD 38-42%, max DD 24-28%, time/abandon 15-22%,
rule/news 6-10%.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

FRICTION_BASE = 0.00032
TILT_SPIKE = 0.14
TILT_DECAY = 0.80
INACTIVITY_LIMIT = 30
SAFETY_MAX_DAYS = 280
SIM_BALANCE = 100_000.0

# wr, rrr, trades/day, (risk_lo, risk_hi), violation/day
PROFILES = {
    "Pro": {
        "sens": (0.52, 1.50, 2, (0.0036, 0.0068), 0.00007),
        "awareness": 0.94,
        "weight": 0.07,
    },
    "Semi-skilled": {
        "sens": (0.51, 1.38, 2, (0.0044, 0.0078), 0.00012),
        "awareness": 0.86,
        "weight": 0.22,
    },
    "Average": {
        "sens": (0.49, 1.22, 3, (0.0052, 0.0095), 0.00018),
        "awareness": 0.72,
        "weight": 0.26,
    },
    "Aggressive": {
        "sens": (0.43, 0.96, 6, (0.0150, 0.0260), 0.00038),
        "awareness": 0.18,
        "weight": 0.28,
    },
    "Lottery": {
        "sens": (0.40, 0.84, 8, (0.0240, 0.0420), 0.00065),
        "awareness": 0.05,
        "weight": 0.17,
    },
}

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
SESSIONS = [(0.80, 0.18), (1.05, 0.32), (1.22, 0.38), (0.93, 0.12)]
SESSION_P = np.array([s[1] for s in SESSIONS], dtype=float)


def get_floor(hwm, start, max_dd, floor_type, trail_lock_at=None):
    if floor_type == "static":
        return start * (1.0 - max_dd)
    if floor_type == "trailing":
        floor = hwm * (1.0 - max_dd)
        if trail_lock_at is not None and hwm >= start * (1.0 + trail_lock_at):
            return start
        return floor
    trailing = hwm * (1.0 - max_dd)
    locked = start * (1.0 - max_dd)
    return min(max(trailing, locked), start)


def daily_floor(rules, start, sod, day_peak):
    dd = rules["daily_dd"]
    if dd is None or dd <= 0:
        return -1e18
    basis = rules.get("daily_dd_basis", "initial")
    dollars = start * dd if basis == "initial" else sod * dd
    if rules.get("daily_dd_type") == "intraday_peak":
        return day_peak - dollars
    return sod - dollars


# Share of per-day rule_violation draws that are the funded/eval news window
# (clawback → second-hit hard breach). Remainder is HFT / arb / copy / EA.
NEWS_SHARE_OF_RULE = 0.65
# High-impact event days (NFP / CPI / FOMC / similar), when news is allowed.
NEWS_DAY_P = 0.12
NEWS_VOL_MULT = 1.40
NEWS_SHOCK_MULT = 2.20
NEWS_WIN_RRR_MULT = 1.15


def simulate_trade(wr, rrr, risk_amt, regime, tilt, vol, rng, news_day=False):
    friction = (risk_amt / 0.01) * FRICTION_BASE * REGIME_FRIC[regime]
    friction *= (1.0 + 0.42 * tilt) * vol
    shock_p = REGIME_SHOCK[regime] * (1.0 + 0.38 * tilt)
    if news_day:
        shock_p = min(0.55, shock_p * NEWS_SHOCK_MULT)
    if rng.random() < shock_p:
        return -risk_amt * rng.uniform(1.5, 2.6) - friction
    adj_wr = np.clip(wr * REGIME_WR[regime] * (1.0 - 0.16 * tilt), 0.21, 0.70)
    if rng.random() < adj_wr:
        actual_rrr = rrr * REGIME_RRR[regime] * rng.uniform(0.78, 1.20)
        actual_rrr *= 1.0 - 0.11 * tilt
        if news_day:
            actual_rrr *= NEWS_WIN_RRR_MULT
        return risk_amt * actual_rrr - friction
    slip = 1.0 + 0.20 * tilt
    return -risk_amt * min(slip, 2.1) - friction


def _consistency_ok(positive_pnls, cons):
    if cons is None or not positive_pnls:
        return True
    return max(positive_pnls) <= sum(positive_pnls) * cons + 1e-12


def run_phase(start_balance, rules, profile_name, rng, is_funded=False,
              min_reward=0.0, split=0.80, news_allowed=False):
    p = PROFILES[profile_name]
    wr, rrr, tpd, risk_range, violation_hazard = p["sens"]
    room_awareness = p["awareness"]

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
    trail_lock_at = rules.get("trail_lock_at")
    daily_action = rules.get("daily_dd_action", "breach")
    max_risk_hard = rules.get("max_risk_per_trade")
    funded_risk_cap = rules.get("funded_risk_cap") if is_funded else None

    while days < SAFETY_MAX_DAYS:
        days += 1
        if consecutive_inactive >= INACTIVITY_LIMIT:
            return False, balance, "inactivity", days
        if rng.random() < violation_hazard:
            # Default: every rule draw is a fail (news window + other forbidden).
            # news_allowed: skip the news-window share; HFT/arb/copy still fail.
            if not news_allowed or rng.random() >= NEWS_SHARE_OF_RULE:
                return False, balance, "rule_violation", days

        news_day = bool(news_allowed and rng.random() < NEWS_DAY_P)

        regime = int(rng.choice(4, p=REGIME_P[regime]))
        activity = 0.71 + 0.16 * (1.0 - tilt)
        if is_funded:
            activity *= 0.92
            if days == 1 and tilt < 0.20:
                tilt = 0.20
        if rng.random() > activity:
            consecutive_inactive += 1
            tilt *= TILT_DECAY
            continue

        consecutive_inactive = 0
        sod = balance
        day_peak = balance
        day_pnl = 0.0
        traded = False
        paused = False
        n_trades = max(1, int(np.clip(tpd * (1.0 + 0.42 * tilt), 1, tpd * 1.9)))

        for _ in range(n_trades):
            if paused:
                break
            vol = SESSIONS[int(rng.choice(len(SESSIONS), p=SESSION_P))][0]
            if news_day:
                vol *= NEWS_VOL_MULT
            floor = get_floor(hwm, start, rules["max_dd"], rules["floor_type"], trail_lock_at)
            d_floor = daily_floor(rules, start, sod, day_peak)
            room = min(balance - floor, balance - d_floor)
            stand_down = balance * 0.0015 * (0.2 + 0.8 * room_awareness)
            if room < stand_down:
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
                risk_pct *= 1.05
            if funded_risk_cap is not None:
                risk_pct = min(risk_pct, funded_risk_cap)
            risk_amt = balance * risk_pct

            if max_risk_hard is not None and risk_pct > max_risk_hard + 1e-12:
                return False, balance, "max_risk", days

            if room_awareness > 0.15:
                clamp_divisor = 1.2 + 2.3 * room_awareness
                if room < clamp_divisor * risk_amt:
                    risk_amt = room / clamp_divisor
                live_min = balance * risk_range[0] * 1.25
                risk_amt = max(risk_amt, min(live_min, max(room, 0.0)))
            if risk_amt <= 0:
                break

            pnl = simulate_trade(
                wr, rrr, risk_amt, regime, tilt, vol, rng, news_day=news_day
            )
            balance += pnl
            day_pnl += pnl
            traded = True
            hwm = max(hwm, balance)
            day_peak = max(day_peak, balance)

            floor = get_floor(hwm, start, rules["max_dd"], rules["floor_type"], trail_lock_at)
            d_floor = daily_floor(rules, start, sod, day_peak)
            if balance <= floor:
                return False, balance, "max_dd", days
            if balance <= d_floor:
                if daily_action == "pause":
                    paused = True
                    break
                return False, balance, "daily_dd", days

            if pnl > 0:
                consecutive_losses = 0
                tilt *= TILT_DECAY * 0.89
                has_profitable_trade = True
            else:
                consecutive_losses += 1
                severity = min(1.0, abs(pnl) / (balance * 0.01 + 1e-9))
                spike = TILT_SPIKE * (1.0 - 0.55 * room_awareness)
                tilt = min(0.90, tilt * TILT_DECAY + spike + 0.18 * severity)

        if not traded:
            consecutive_inactive += 1
            continue
        if day_pnl > 0:
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
            if balance >= start * (1.0 + target) and valid_days >= rules.get("min_days", 0):
                passed = _consistency_ok(positive_pnls, rules.get("consistency"))
        else:
            extra_ok = True if vdt > 0 else has_profitable_trade
            if valid_days >= rules.get("min_days", 0) and extra_ok:
                passed = _consistency_ok(positive_pnls, rules.get("consistency"))
            if passed and min_reward > 0:
                if split * max(0.0, balance - start) + 1e-9 < min_reward:
                    passed = False
        if passed:
            return True, balance, None, days
        tilt *= TILT_DECAY

    return False, balance, "time_abandon", days


def simulate_funded_survival(rng):
    for month, survive in ((1, 0.59), (3, 0.72), (12, 0.76)):
        if rng.random() > survive:
            return False, month
    return True, 12


def expected_refund_frac(mode: str, p_pay: float, p_fourth: float = 0.35) -> float:
    """Expected refund as a fraction of fee, given first-payout probability."""
    if mode == "none":
        return 0.0
    if mode == "first":
        return p_pay
    if mode == "fourth":
        return p_pay * p_fourth
    if mode == "quarter_x4":
        # 25% of fee on each of first 4 payouts; ~1-3% load in prior Hola work
        return p_pay * (0.25 * (1.0 + 0.55 + 0.35 + 0.22))
    return p_pay


def break_even_fee(e_payout: float, refund_frac_per_fee: float) -> float:
    """fee = E[payout] + refund_frac * fee  =>  fee = E[payout] / (1 - k).

    For refund_mode first, k = P(pay). For none, k = 0.
    """
    k = min(max(refund_frac_per_fee, 0.0), 0.95)
    return e_payout / (1.0 - k)


def margin_price(be: float, margin: float) -> float:
    return be / (1.0 - margin) if margin < 1 else float("inf")
