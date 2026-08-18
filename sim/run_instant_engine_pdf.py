#!/usr/bin/env python3
"""Instant leftover: current catalog vs live trading-engine PDF.

The PDF (evaluateOneStepConsistencyRule) factors every profitable day into
Positive Days' Profit. There is no 0.5% start-of-day filter and no min
valid-day count on consistency. Instant is 20%. 1-Step eval is 50% with
the same function.

Current catalog Instant still gates payout on 5 days at at least 0.5% of
SOD, plus 20% Best Day on every profitable day. This run measures whether
killing that valid-day gate moves leftover.

News on. 1,200 paths per profile. Same Instant seed as run_rule_alignment.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd

from catalog import P, PRODUCTS
from industry_book import PROFILES, simulate_funded_survival
from run_news_included import be_for, blend, run_one
from write_price_rec_pdf import UNITS, leftover_after_opex, opex_stack
from write_reprice_pdf import REC

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
ART = Path("/opt/cursor/artifacts")

N_SIMS = 1200
SEED = 42 + 10007

INSTANT_SALES = {
    5_000: REC[("Instant", 5_000)],
    10_000: REC[("Instant", 10_000)],
    25_000: REC[("Instant", 25_000)],
    50_000: REC[("Instant", 50_000)],
    100_000: REC[("Instant", 100_000)],
}

VARIANTS = {
    "catalog_two_box": {
        "phase": P(
            None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.005, 0.20,
            vdt_op="ge",
        ),
        "note": "5 days ≥0.5% SOD + 20% Best Day on every profitable day",
    },
    "pdf_engine": {
        "phase": P(None, 0.06, "trailing", 0.03, "intraday_peak", 0, 0.0, 0.20),
        "note": "PDF: every profitable day in PDP; no 0.5% valid-day gate; 20% Best Day",
    },
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
        print(f"{label:16s} {profile:12s} P(pay)={paid / n:.3f}")
    blended = blend(pd.DataFrame(rows)).iloc[0]
    sku_rows = []
    family_left = 0.0
    family_sale = 0.0
    for size, sale in INSTANT_SALES.items():
        e, be, _ = be_for(blended, size)
        left = leftover_after_opex(sale, opex_stack(be, "Instant", size)["loaded"])
        cost = e
        sale_m = (sale - cost) / sale
        n_acct = UNITS[("Instant", size)]
        family_left += n_acct * left
        family_sale += n_acct * sale
        sku_rows.append({
            "label": label,
            "Size": size,
            "Sale": sale,
            "P_pay": float(blended.P_pay),
            "P_yr1": float(blended.P_yr1),
            "E": e,
            "BE": be,
            "Left": left,
            "Sale_m": sale_m,
            "Units": n_acct,
            "Avg_days": float(blended.Avg_days),
        })
    return sku_rows, family_left, family_sale, blended


def write_md(df: pd.DataFrame, notes: dict) -> Path:
    body = [
        "# Instant leftover — live engine PDF vs catalog",
        "",
        "PDF `evaluateOneStepConsistencyRule`: every profitable day (including small profitable days) "
        "is in Positive Days’ Profit. No 0.5% start-of-day filter. No min valid "
        "days. Instant 20%. 1-Step eval uses the same function at 50%.",
        "",
        "News on. 1,200 paths per profile. Instant seed matches `run_rule_alignment`.",
        "",
        "| Engine | Size | Sale | P(pay) | BE | Leftover | Sale m |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in df.itertuples():
        body.append(
            f"| {r.label} | ${r.Size:,.0f} | ${r.Sale:,.0f} | "
            f"{100 * r.P_pay:.1f}% | ${r.BE:,.1f} | "
            f"${r.Left:,.1f} | {100 * r.Sale_m:+.0f}% |"
        )
    body.extend(["", "## Instant family (98 accounts)", ""])
    for label, (left, sale) in notes.items():
        body.append(
            f"- **{label}:** leftover **${left:,.0f}** "
            f"({100 * left / sale:.1f}% of ${sale:,.0f} sale)"
        )
    path = RESULTS / "INSTANT_ENGINE_PDF_MARGINS.md"
    path.write_text("\n".join(body) + "\n")
    return path


def main():
    RESULTS.mkdir(exist_ok=True)
    all_rows = []
    notes = {}
    for key, spec in VARIANTS.items():
        print(spec["note"])
        sku_rows, fam_left, fam_sale, _ = run_instant(spec["phase"], key)
        all_rows.extend(sku_rows)
        notes[key] = (fam_left, fam_sale)
        print(
            f"{key}: Instant family leftover ${fam_left:,.0f} "
            f"on ${fam_sale:,.0f} sale"
        )
        print()
    df = pd.DataFrame(all_rows)
    df.to_csv(RESULTS / "verodus_instant_engine_pdf.csv", index=False)
    md = write_md(df, notes)
    if ART.is_dir():
        import shutil
        shutil.copyfile(md, ART / md.name)
        shutil.copyfile(
            RESULTS / "verodus_instant_engine_pdf.csv",
            ART / "verodus_instant_engine_pdf.csv",
        )
    print(df.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    print(f"\nWrote {md}")


if __name__ == "__main__":
    main()
