#!/usr/bin/env python3
"""Verodus DCF — 25 August 2026. Internal. Do not send to Joe.

Reproducible unlevered DCF of the three operating affiliates
(Verodus Capital Inc., Verodus L.L.C.-FZ, 1591011 B.C. Ltd.).
Cash-free / debt-free going concern. Joe's TradeMap volume is a
separate case, not the standing value.

Run: python3 11-dcf-model.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from math import prod

VALUATION_DATE = "2026-08-25"

# --- Year-0 normalised run-rate (USD) ---
# Live book: ~$70k receipts, ~$11k payouts, CAD $20k opex ex-ads.
RECEIPTS_0 = 70_000 * 12  # 840,000
PAYOUTS_0 = 11_000 * 12  # 132,000
ADS_RATE = 0.20
OPEX_0 = 14_500 * 12  # 174,000
INTERN_0 = 3_000 * 12  # 36,000
DAVID_0 = 1_500 * 12  # 18,000  (part-time; stated as assumption)
OPEX_LOADED_0 = OPEX_0 + INTERN_0 + DAVID_0
ADS_0 = RECEIPTS_0 * ADS_RATE  # 168,000
PRETAX_0 = RECEIPTS_0 - PAYOUTS_0 - ADS_0 - OPEX_LOADED_0  # 312,000
PAYOUT_RATE_0 = PAYOUTS_0 / RECEIPTS_0  # 0.15714...

TAX_BASE = 0.15  # blended; CCPC SBD ~11% if it applies, 27% if not
TAX_HIGH = 0.27
MAINT_CAPEX_0 = 10_000  # software/hardware refresh; hosting sits in opex
NWC_PCT_OF_INCREMENTAL_REV = 0.02  # processor reserves as receipts grow
OPEX_INFLATION = 0.03
G_TERMINAL = 0.025
R_BASE = 0.25
YEARS = 5
EXIT_MULT_BASE = 3.5  # SDE multiple on year-5 pretax leftover


def round_k(x: float) -> int:
    return int(round(x))


def pv_factor(r: float, t: float, mid_year: bool = True) -> float:
    """Discount factor for cash in year t (t=1..n). Mid-year → t-0.5."""
    when = t - 0.5 if mid_year else t
    return 1.0 / ((1.0 + r) ** when)


@dataclass
class Year:
    n: int
    receipts: float
    payouts: float
    ads: float
    opex_loaded: float
    pretax: float
    nopat: float
    capex: float
    dnwc: float
    fcff: float


def project(
    receipts_path: list[float],
    payout_rate_path: list[float],
    ads_rate: float = ADS_RATE,
    tax: float = TAX_BASE,
    opex0: float = OPEX_LOADED_0,
    capex0: float = MAINT_CAPEX_0,
) -> list[Year]:
    years: list[Year] = []
    prev_r = RECEIPTS_0
    opex = opex0
    capex = capex0
    for i, (rec, pr) in enumerate(zip(receipts_path, payout_rate_path), start=1):
        opex = opex * (1 + OPEX_INFLATION)
        capex = capex * (1 + OPEX_INFLATION)
        ads = rec * ads_rate
        payouts = rec * pr
        pretax = rec - payouts - ads - opex
        nopat = pretax * (1 - tax) if pretax > 0 else pretax
        dnwc = max(0.0, rec - prev_r) * NWC_PCT_OF_INCREMENTAL_REV
        fcff = nopat - capex - dnwc
        years.append(
            Year(i, rec, payouts, ads, opex, pretax, nopat, capex, dnwc, fcff)
        )
        prev_r = rec
    return years


def value_path(
    years: list[Year],
    r: float,
    exit_mult: float = EXIT_MULT_BASE,
    g: float = G_TERMINAL,
    mid_year: bool = True,
) -> dict:
    pv_fcff = sum(y.fcff * pv_factor(r, y.n, mid_year) for y in years)
    y5 = years[-1]
    tv_exit = exit_mult * y5.pretax  # equity-like SDE exit, cash-free
    # Gordon on FCFF: next year grows at g from a fading explicit period
    fcff_6 = y5.fcff * (1 + g)
    tv_gordon = fcff_6 / (r - g) if r > g else float("nan")
    # Terminal cash at end of year 5 (exit at year-end, not mid-year)
    df_end = 1.0 / ((1.0 + r) ** YEARS)
    pv_exit = tv_exit * df_end
    pv_gordon = tv_gordon * df_end
    # Blend: 50/50 exit multiple and Gordon, both standard for a private book
    pv_tv_blend = 0.5 * pv_exit + 0.5 * pv_gordon
    equity_exit = pv_fcff + pv_exit
    equity_gordon = pv_fcff + pv_gordon
    equity_blend = pv_fcff + pv_tv_blend
    return {
        "pv_explicit_fcff": pv_fcff,
        "tv_exit": tv_exit,
        "tv_gordon": tv_gordon,
        "pv_exit": pv_exit,
        "pv_gordon": pv_gordon,
        "equity_exit": equity_exit,
        "equity_gordon": equity_gordon,
        "equity_blend": equity_blend,
        "year5_pretax": y5.pretax,
        "year5_fcff": y5.fcff,
        "implied_exit_mult_on_y5_pretax_from_gordon": (
            tv_gordon / y5.pretax if y5.pretax else None
        ),
    }


def receipts_from_cagrs(y1: float, cagrs: list[float]) -> list[float]:
    """y1 is year-1 receipts; cagrs[i] grows year i+1 from previous."""
    out = [y1]
    rec = y1
    for c in cagrs:
        rec = rec * (1 + c)
        out.append(rec)
    return out


def lerp(start: float, end: float, n: int) -> list[float]:
    if n == 1:
        return [end]
    return [start + (end - start) * i / (n - 1) for i in range(n)]


# --- Scenarios (5 years) ---
# Year-1 receipts stay at the $840k normalised run-rate unless named.
Y1 = RECEIPTS_0

SCENARIOS = {
    "base": {
        "label": "Base — strict book holds, modest organic",
        "weight": 0.45,
        "receipts": receipts_from_cagrs(Y1, [0.08, 0.06, 0.05, 0.04]),
        "payout_rates": [PAYOUT_RATE_0] * 5,
        "note": "Ads on at 20%. Payouts stay at the live 15.7%. Receipts +8/6/5/4% after a flat year 1. No TradeMap volume.",
    },
    "reversion": {
        "label": "Conservative — payouts drift toward industry",
        "weight": 0.25,
        "receipts": receipts_from_cagrs(Y1, [0.05, 0.04, 0.03, 0.02]),
        "payout_rates": lerp(PAYOUT_RATE_0, 0.28, 5),
        "note": "Ever-paid mean-reverts. Payouts go 15.7% → 28% of receipts by year 5 (still below a 7% ever-paid disaster). Receipts grow slowly.",
    },
    "downside": {
        "label": "Downside — receipts decay, book softens",
        "weight": 0.15,
        "receipts": receipts_from_cagrs(Y1 * 0.75, [-0.05, -0.03, 0.00, 0.02]),
        "payout_rates": lerp(PAYOUT_RATE_0, 0.32, 5),
        "note": "Year 1 receipts at $630k (ads restart does not hold $70k/month). Payouts to 32%. Still a going concern, not a shutdown.",
    },
    "upside": {
        "label": "Upside organic — no Joe",
        "weight": 0.15,
        "receipts": receipts_from_cagrs(Y1, [0.15, 0.12, 0.10, 0.08]),
        "payout_rates": lerp(PAYOUT_RATE_0, 0.20, 5),
        "note": "Content/affiliates work. Mild payout drift to 20%. Not TradeMap.",
    },
    "joe": {
        "label": "Joe volume (not standing value)",
        "weight": 0.0,
        "receipts": [Y1, Y1 * 1.4, Y1 * 2.0, Y1 * 2.3, Y1 * 2.5],
        "payout_rates": lerp(PAYOUT_RATE_0, 0.22, 5),
        "note": "Illustrative only. Receipts 2.5× by year 5. Do not use as the $1.2m. This is the freeze he is buying.",
    },
}


def run_scenario(key: str, tax: float = TAX_BASE, r: float = R_BASE) -> dict:
    s = SCENARIOS[key]
    years = project(s["receipts"], s["payout_rates"], tax=tax)
    v = value_path(years, r=r)
    return {
        "key": key,
        "label": s["label"],
        "weight": s["weight"],
        "note": s["note"],
        "years": [asdict(y) for y in years],
        **v,
    }


def wacc_build() -> dict:
    rf = 0.035
    erp = 0.05
    beta = 1.50
    size = 0.06
    specific = 0.08
    # 3.5 + 7.5 + 6 + 8 = 25.0
    return {
        "risk_free_cad": rf,
        "equity_risk_premium": erp,
        "unlevered_beta": beta,
        "beta_times_erp": beta * erp,
        "size_micro": size,
        "company_specific": specific,
        "wacc": rf + beta * erp + size + specific,
        "company_specific_split": {
            "four_month_history": 0.03,
            "prop_firm_mortality": 0.025,
            "key_person_kim": 0.015,
            "processor_and_enforcement": 0.01,
        },
    }


def fmt(x: float) -> str:
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.2f}m"
    if abs(x) >= 1000:
        return f"${x:,.0f}"
    return f"${x:,.0f}"


def main() -> None:
    wacc = wacc_build()
    assert abs(wacc["wacc"] - 0.25) < 1e-9

    results = {k: run_scenario(k) for k in SCENARIOS}
    weighted = sum(
        results[k]["equity_blend"] * SCENARIOS[k]["weight"]
        for k in ("base", "reversion", "downside", "upside")
    )

    # Discount-rate / tax / exit-multiple sensitivities on BASE
    r_grid = [0.20, 0.225, 0.25, 0.275, 0.30]
    tax_grid = [0.11, 0.15, 0.27]
    mult_grid = [2.5, 3.0, 3.5, 4.0, 4.5]

    base_r_sens = {
        str(r): run_scenario("base", r=r)["equity_blend"] for r in r_grid
    }
    base_tax_sens = {
        str(t): run_scenario("base", tax=t)["equity_blend"] for t in tax_grid
    }
    base_mult_sens = {}
    s = SCENARIOS["base"]
    years = project(s["receipts"], s["payout_rates"])
    for m in mult_grid:
        v = value_path(years, R_BASE, exit_mult=m)
        base_mult_sens[str(m)] = v["equity_blend"]

    # r vs g matrix on base Gordon-only (cleaner tornado)
    g_grid = [0.00, 0.015, 0.025, 0.035]
    gordon_matrix = {}
    for r in r_grid:
        gordon_matrix[str(r)] = {}
        for g in g_grid:
            if r <= g:
                gordon_matrix[str(r)][str(g)] = None
                continue
            gordon_matrix[str(r)][str(g)] = value_path(
                years, r=r, g=g
            )["equity_gordon"]

    # Implied 60%
    standing = results["base"]["equity_blend"]
    expected = weighted

    out = {
        "valuation_date": VALUATION_DATE,
        "year0": {
            "receipts": RECEIPTS_0,
            "payouts": PAYOUTS_0,
            "payout_rate": PAYOUT_RATE_0,
            "ads": ADS_0,
            "opex_ex_ads": OPEX_0,
            "intern": INTERN_0,
            "david": DAVID_0,
            "opex_loaded": OPEX_LOADED_0,
            "pretax": PRETAX_0,
            "nopat_15": PRETAX_0 * (1 - TAX_BASE),
            "fcff_steady": PRETAX_0 * (1 - TAX_BASE) - MAINT_CAPEX_0,
        },
        "wacc": wacc,
        "scenarios": results,
        "probability_weighted": expected,
        "sensitivities": {
            "discount_rate_on_base_blend": base_r_sens,
            "tax_on_base_blend": base_tax_sens,
            "exit_mult_on_base_blend": base_mult_sens,
            "gordon_r_vs_g": gordon_matrix,
        },
        "sixty_percent": {
            "of_base_blend": standing * 0.60,
            "of_expected": expected * 0.60,
            "ask": 900_000,
            "take": 750_000,
            "floor": 660_000,
        },
    }

    # Pretty print
    print("=" * 72)
    print("YEAR 0 NORMALISED")
    print(f"  Receipts        {fmt(RECEIPTS_0)}")
    print(f"  Payouts         {fmt(PAYOUTS_0)}  ({PAYOUT_RATE_0*100:.2f}%)")
    print(f"  Ads 20%         {fmt(ADS_0)}")
    print(f"  Opex loaded     {fmt(OPEX_LOADED_0)}")
    print(f"  Pretax leftover {fmt(PRETAX_0)}")
    print(f"  NOPAT @ 15%     {fmt(PRETAX_0*(1-TAX_BASE))}")
    print(f"  Steady FCFF     {fmt(PRETAX_0*(1-TAX_BASE)-MAINT_CAPEX_0)}")
    print()
    print("WACC BUILD-UP")
    print(f"  {wacc['wacc']*100:.1f}%  =  {wacc['risk_free_cad']*100:.1f}% rf  +  {wacc['beta_times_erp']*100:.1f}% beta*ERP  +  {wacc['size_micro']*100:.1f}% size  +  {wacc['company_specific']*100:.1f}% specific")
    print()
    for k, res in results.items():
        print("-" * 72)
        print(f"{res['label']}  (weight {res['weight']*100:.0f}%)")
        print(f"  {res['note']}")
        print(
            f"  {'Yr':>3} {'Receipts':>10} {'Payout%':>8} {'Pretax':>10} {'FCFF':>10}"
        )
        src = SCENARIOS[k]
        for y, pr in zip(res["years"], src["payout_rates"]):
            print(
                f"  {y['n']:3d} {fmt(y['receipts']):>10} {pr*100:7.1f}% {fmt(y['pretax']):>10} {fmt(y['fcff']):>10}"
            )
        print(f"  PV of 5yr FCFF     {fmt(res['pv_explicit_fcff'])}")
        print(f"  TV exit 3.5x       {fmt(res['tv_exit'])}   PV {fmt(res['pv_exit'])}")
        print(f"  TV Gordon          {fmt(res['tv_gordon'])}   PV {fmt(res['pv_gordon'])}")
        print(f"  Equity (exit)      {fmt(res['equity_exit'])}")
        print(f"  Equity (Gordon)    {fmt(res['equity_gordon'])}")
        print(f"  Equity BLEND       {fmt(res['equity_blend'])}")
        print(f"  60% of blend       {fmt(res['equity_blend']*0.6)}")
    print("=" * 72)
    print(f"PROBABILITY-WEIGHTED (ex-Joe)  {fmt(expected)}")
    print(f"60% of expected                {fmt(expected*0.6)}")
    print(f"BASE blend                     {fmt(standing)}")
    print(f"60% of base                    {fmt(standing*0.6)}")
    print()
    print("SENSITIVITY r on base blend")
    for r, v in base_r_sens.items():
        print(f"  r={float(r)*100:.1f}%  {fmt(v)}")
    print("SENSITIVITY tax on base blend")
    for t, v in base_tax_sens.items():
        print(f"  tax={float(t)*100:.0f}%  {fmt(v)}")
    print("SENSITIVITY exit multiple on base blend")
    for m, v in base_mult_sens.items():
        print(f"  {m}x  {fmt(v)}")

    json_path = "/workspace/internal/2026-08-25-joe-wong/11-dcf-output.json"
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {json_path}")


if __name__ == "__main__":
    main()
