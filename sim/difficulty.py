"""Numeric difficulty for every catalog plan.

Higher = harder for the trader (tighter daily / max DD, trail, consistency,
more phases). Score is 0–100. Compare two plans only when
|D_a − D_b| <= DELTA.

D = 0.55 × rule score + 0.45 × book score.
Rule score is built from the catalog card. Book score is 100 × (1 − P(pay)),
so the Monte Carlo pass rate can pull two similar cards together or apart.
"""

from __future__ import annotations

from catalog import PRODUCTS

# Half-width of the comparison band. ±6 is about one daily-DD step after
# the 0.55 rule weight — enough for Blue Guardian Instant (SOD + trail lock)
# to sit with Verodus Instant (peak + never-lock), not enough to pull in
# no-daily Instant or to mix Lite with Pro.
DELTA = 6.0


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _phase_score(p: dict) -> float:
    """Hardness of one phase. ~0–70 before extras."""
    s = 0.0
    daily = p.get("daily_dd")
    if daily is None or daily <= 0:
        s += 4.0
    elif daily >= 0.05:
        s += 16.0
    elif daily >= 0.04:
        s += 26.0
    elif daily >= 0.03:
        s += 38.0
    else:
        s += 48.0
    # Peak vs SOD is a real extra, but the book already prices it — keep
    # this small so 3%/6% Instant twins stay in one band.
    if p.get("daily_dd_type") == "intraday_peak" and daily:
        s += 3.0
    if p.get("daily_dd_action") == "pause":
        s -= 4.0

    mx = p.get("max_dd") or 0.10
    if mx >= 0.12:
        s += 6.0
    elif mx >= 0.10:
        s += 12.0
    elif mx >= 0.08:
        s += 20.0
    elif mx >= 0.06:
        s += 30.0
    elif mx >= 0.05:
        s += 36.0
    else:
        s += 44.0

    floor = p.get("floor_type")
    if floor == "trailing":
        s += 12.0
    elif floor == "hybrid":
        s += 7.0
    if p.get("trail_lock_at") is not None:
        s -= 4.0

    cons = p.get("consistency")
    if cons:
        s += _clip((0.55 - cons) * 40.0, 0.0, 16.0)

    tgt = p.get("target")
    if tgt and mx:
        s += _clip((tgt / mx - 0.70) * 14.0, 0.0, 12.0)

    if (p.get("valid_day_threshold") or 0) >= 0.005:
        s += 3.0
    if (p.get("consistency_floor") or 0) >= 0.005:
        s += 3.0
    if (p.get("min_days") or 0) >= 5:
        s += 2.0
    if p.get("max_risk_per_trade"):
        s += 5.0
    if p.get("funded_risk_cap"):
        s += 7.0
    return s


def rule_score(cfg: dict) -> float:
    """0–100 from the rule card only."""
    phases = list(cfg["phases"])
    funded = cfg.get("funded")
    binding = funded if funded is not None else phases[0]
    s = _phase_score(binding)
    # Extra eval phases add a smaller load (another chance to fail).
    extra = phases if funded is not None else phases[1:]
    for ph in extra:
        s += 0.22 * _phase_score(ph)
    if cfg.get("instant"):
        s += 5.0
    n = len(phases) + (0 if funded is None else 1)
    if n >= 3:
        s += 6.0
    if cfg.get("split", 0.80) <= 0.55:
        s -= 4.0  # 50% split is a different product, slightly less "hard to get paid"
    # Leave headroom so Instant cards do not all pin at 100.
    return float(_clip(s * 0.92, 0.0, 100.0))


def book_score(p_pay: float) -> float:
    return float(_clip(100.0 * (1.0 - p_pay), 0.0, 100.0))


def difficulty(cfg: dict, p_pay: float) -> float:
    return round(0.55 * rule_score(cfg) + 0.45 * book_score(p_pay), 1)


def scores_for_book(p_pay_by_product: dict) -> dict:
    out = {}
    for key, cfg in PRODUCTS.items():
        p = float(p_pay_by_product.get(key, 0.10))
        out[key] = {
            "Product": key,
            "Firm": cfg["firm"],
            "Plan": cfg["plan"],
            "Family": cfg["family"],
            "D": difficulty(cfg, p),
            "D_rules": round(rule_score(cfg), 1),
            "D_book": round(book_score(p), 1),
            "P_pay": p,
        }
    return out


def comparable(d_a: float, d_b: float, delta: float = DELTA) -> bool:
    return abs(float(d_a) - float(d_b)) <= float(delta)
