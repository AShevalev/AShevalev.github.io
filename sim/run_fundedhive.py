#!/usr/bin/env python3
"""FundedHive print / BE analysis on the industry-calibrated book."""

from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from catalog import P, funded, sku
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

# News is allowed on every FundedHive line.
NEWS = True


def run_one(config, profile, rng):
    split = config["split"]
    min_reward = config["min_reward"]
    instant = config["instant"]
    ok, bal, reason, d = run_phase(
        SIM_BALANCE, config["phases"][0], profile, rng,
        is_funded=False,
        min_reward=min_reward if instant else 0.0, split=split,
        news_allowed=NEWS,
    )
    days = d
    if not ok:
        return dict(p1=False, p2=False, eval_pass=False, funded=False, paid=False,
                    payout=0.0, reason=reason or "unknown", stage="p1", days=days)
    p2 = True
    for i, phase in enumerate(config["phases"][1:], start=2):
        ok, bal, reason, d = run_phase(
            SIM_BALANCE, phase, profile, rng, is_funded=False, news_allowed=NEWS,
        )
        days += d
        if not ok:
            return dict(p1=True, p2=False, eval_pass=False, funded=False, paid=False,
                        payout=0.0, reason=reason or "unknown", stage=f"p{i}", days=days)
    eval_pass = True
    if config["funded"] is not None:
        if rng.random() < 0.12:
            return dict(p1=True, p2=p2, eval_pass=True, funded=False, paid=False,
                        payout=0.0, reason="kyc_drop", stage="funded", days=days)
        ok, bal, reason, d = run_phase(
            SIM_BALANCE, config["funded"], profile, rng,
            is_funded=True, min_reward=min_reward, split=split,
            news_allowed=NEWS,
        )
        days += d
        if not ok:
            return dict(p1=True, p2=p2, eval_pass=True, funded=False, paid=False,
                        payout=0.0, reason=reason or "unknown", stage="funded", days=days)
    profit = max(0.0, bal - SIM_BALANCE)
    payout = split * profit
    paid = payout + 1e-12 >= min_reward
    return dict(p1=True, p2=p2, eval_pass=eval_pass, funded=True, paid=paid,
                payout=payout if paid else 0.0,
                reason=None if paid else "min_reward", stage="paid", days=days)


PRODUCTS = {}


def add(key, **kw):
    PRODUCTS[key] = kw


# 3 profitable days, each ≥ 1% of initial (TOS Annex 1.1).
VDT = 0.01
MIN_DAYS = 3

# Classic 2-Step NewBee (70% A-book). List = TheTrustedProp 2026 Classic table.
# Sale = WELCOME25 (25% off, new traders). Hive Coin is not cash — refund none.
add("FH Classic 2-Step",
    firm="FundedHive", plan="Classic 2-Step (NewBee)", family="2-step",
    phases=[
        P(0.08, 0.10, "static", 0.05, "sod", MIN_DAYS, VDT, max_risk=0.03),
        P(0.06, 0.10, "static", 0.05, "sod", MIN_DAYS, VDT, max_risk=0.03),
    ],
    funded=funded(0.10, "static", 0.05, min_days=0, funded_risk=0.03),
    skus=sku((5e3, 29, 22), (1e4, 59, 44), (25e3, 99, 74),
             (5e4, 199, 149), (1e5, 349, 262), (2e5, 599, 449)),
    refund="none", split=0.70, min_reward=100.0, instant=False,
    discount="WELCOME25",
    source="TOS Jan 2026 Annex 1.1; Classic list TheTrustedProp; sale WELCOME25")

# Pay From Profits 2-Step — door is the per-phase access fee (TOS annex table).
add("FH PFP 2-Step",
    firm="FundedHive", plan="Pay From Profits 2-Step", family="2-step",
    phases=[
        P(0.08, 0.10, "static", 0.05, "sod", MIN_DAYS, VDT, max_risk=0.03),
        P(0.06, 0.10, "static", 0.05, "sod", MIN_DAYS, VDT, max_risk=0.03),
    ],
    funded=funded(0.10, "static", 0.05, min_days=0, funded_risk=0.03),
    skus=sku((5e3, 9, 7), (1e4, 19, 14), (25e3, 49, 37),
             (5e4, 75, 56), (1e5, 99, 74), (2e5, 199, 149)),
    refund="none", split=0.80, min_reward=100.0, instant=False,
    discount="WELCOME25",
    source="TOS Annex PayFromProfits 2-Step access fees; funded fee 1–3% of size extra")

add("FH PFP 1-Step",
    firm="FundedHive", plan="Pay From Profits 1-Step", family="1-step",
    phases=[P(0.10, 0.10, "static", 0.05, "sod", MIN_DAYS, VDT, max_risk=0.03)],
    funded=funded(0.10, "static", 0.05, min_days=0, funded_risk=0.03),
    skus=sku((5e3, 19, 14), (1e4, 39, 29), (25e3, 99, 74),
             (5e4, 149, 112), (1e5, 249, 187), (2e5, 399, 299)),
    refund="none", split=0.80, min_reward=100.0, instant=False,
    discount="WELCOME25",
    source="TOS Annex PayFromProfits 1-Step access fees; 10% target")

# Instant Growth Level 1. On-chain transparency Jun 2026: $10k @ $299.
# TOS: 6% static, no daily, 2% max/trade, 80% A-book, start $10k, scale by doubling.
add("FH Instant Growth",
    firm="FundedHive", plan="Instant Growth L1", family="instant",
    phases=[P(None, 0.06, "static", None, min_days=0, vdt=0.0, max_risk=0.02)],
    funded=None,
    skus=sku((1e4, 299, 299)),
    refund="none", split=0.80, min_reward=100.0, instant=True,
    discount="—",
    source="TOS Annex 1.4 + 2.1; $10k fee from fundedhive.com/transparency Jun 2026")


# Profile → PFP risk group (funded fee % of size, share payable from profits).
PFP_GROUP = {
    "Pro": ("Low", 0.01, 1.00),
    "Semi-skilled": ("Low", 0.01, 1.00),
    "Average": ("Moderate", 0.02, 1.00),
    "Aggressive": ("Medium", 0.025, 0.50),
    "Lottery": ("High", 0.03, 0.50),
}


def run_all(n_sims=700, seed=42):
    rng = np.random.default_rng(seed)
    keys = list(PRODUCTS)
    total = len(keys) * len(PROFILES) * n_sims
    done = 0
    t0 = time.time()
    rows = []
    fail_rows = []
    print(f"{len(keys)} products × {len(PROFILES)} × {n_sims} = {total:,}\n")
    for key in keys:
        cfg = PRODUCTS[key]
        for profile in PROFILES:
            n = p1 = p2 = ev = funded_n = paid = yr1 = 0
            days, payouts = [], []
            fails = defaultdict(int)
            for _ in range(n_sims):
                res = run_one(cfg, profile, rng)
                n += 1
                days.append(res["days"])
                payouts.append(res["payout"])
                if res["p1"]:
                    p1 += 1
                if res["p2"]:
                    p2 += 1
                if res["eval_pass"]:
                    ev += 1
                if res["funded"]:
                    funded_n += 1
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
                    sys.stdout.write(
                        f"\r{key[:22]:22s} {profile:12s} {100*done/total:5.1f}% ETA {eta:5.0f}s"
                    )
                    sys.stdout.flush()
            rows.append({
                "Product": key,
                "Firm": cfg["firm"],
                "Plan": cfg["plan"],
                "Family": cfg["family"],
                "Profile": profile,
                "Weight": PROFILES[profile]["weight"],
                "Phase1": p1 / n,
                "Phase2": p2 / n,
                "EvalPass": ev / n,
                "Funded": funded_n / n,
                "P_pay": paid / n,
                "P_yr1": yr1 / n,
                "E_payout_100k": float(np.mean(payouts)),
                "Avg_days": float(np.mean(days)),
            })
            for r, c in fails.items():
                fail_rows.append({
                    "Product": key, "Profile": profile, "Reason": r, "Share": c / n,
                })
    print(f"\nDone in {time.time() - t0:.1f}s")
    return pd.DataFrame(rows), pd.DataFrame(fail_rows)


def blend(df):
    rows = []
    for product, sub in df.groupby("Product", sort=False):
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
            "Phase2": float(np.dot(w, sub["Phase2"])),
            "EvalPass": float(np.dot(w, sub["EvalPass"])),
            "Funded": float(np.dot(w, sub["Funded"])),
            "P_pay": float(np.dot(w, sub["P_pay"])),
            "P_yr1": float(np.dot(w, sub["P_yr1"])),
            "E_payout_100k": float(np.dot(w, sub["E_payout_100k"])),
            "Avg_days": float(np.dot(w, sub["Avg_days"])),
        })
    return pd.DataFrame(rows)


def sku_rows(df_blend):
    rows = []
    for _, b in df_blend.iterrows():
        cfg = PRODUCTS[b["Product"]]
        k = expected_refund_frac(cfg["refund"], b["P_pay"])
        for size, (lst, sale) in cfg["skus"].items():
            e_x = b["E_payout_100k"] * (size / SIM_BALANCE)
            e_cost = e_x + k * sale
            be = break_even_fee(e_x, k)
            rows.append({
                "Product": b["Product"],
                "Plan": cfg["plan"],
                "Family": cfg["family"],
                "Size": int(size),
                "List": lst,
                "Sale": sale,
                "P_pay": b["P_pay"],
                "E_payout": e_x,
                "E_cost": e_cost,
                "BE": be,
                "px_20": margin_price(be, 0.20),
                "px_40": margin_price(be, 0.40),
                "px_60": margin_price(be, 0.60),
                "sale_m": (sale - e_cost) / sale if sale else np.nan,
                "prints": (sale - e_cost) >= -1.0,
            })
    return pd.DataFrame(rows)


def pfp_funnel(df_profiles, product, phases=2):
    """Expected $ the firm keeps vs pays, per starter, by size."""
    sub = df_profiles[df_profiles.Product == product]
    cfg = PRODUCTS[product]
    rows = []
    for size, (lst, sale) in cfg["skus"].items():
        e_pay = e_rev = e_access = e_funded = 0.0
        for _, r in sub.iterrows():
            w = r["Weight"]
            name, fee_pct, from_profits = PFP_GROUP[r["Profile"]]
            p1 = r["Phase1"]
            ev = r["EvalPass"]
            p_pay = r["P_pay"]
            e_x = r["E_payout_100k"] * (size / SIM_BALANCE)
            # Everyone pays one access fee. 2-step passers of P1 pay a second.
            access = sale * (1.0 + (p1 if phases == 2 else 0.0))
            funded_fee = fee_pct * size
            upfront = funded_fee * (1.0 - from_profits)
            from_p = funded_fee * from_profits
            # Upfront funded fee only if they pass eval (and Medium/High).
            # From-profits portion only if they actually get paid.
            funded_rev = ev * upfront + p_pay * from_p
            e_access += w * access
            e_funded += w * funded_rev
            e_rev += w * (access + funded_rev)
            e_pay += w * e_x
        left = e_rev - e_pay
        rows.append({
            "Size": int(size),
            "Access_sale": sale,
            "E_access": e_access,
            "E_funded_fee": e_funded,
            "E_revenue": e_rev,
            "E_payout": e_pay,
            "Leftover": left,
            "prints": left >= -1.0,
            "m": left / e_rev if e_rev else np.nan,
        })
    return pd.DataFrame(rows)


def usd(x):
    return f"${float(x):,.0f}"


def pct(x):
    return f"{100 * float(x):.1f}%"


def write_md(df_b, df_s, df_p, df_f, pfp2, pfp1):
    lines = []
    a = lines.append
    a("# FundedHive — print / BE analysis")
    a("")
    a("Industry-calibrated CFD book (7/22/26/28/17), **21 Aug 2026**. "
      "News allowed on every path. Same engine as the Verodus industry catalog. "
      "E[X] is **first-payout dollars per buyer** (zeros included). "
      "BE = E[X] / (1 − k). Hive Coin is **not cash**, so k = 0 on every line.")
    a("")
    a("Sources: [fundedhive.com](https://fundedhive.com/) homepage + "
      "[TOS PDF](https://fundedhive.com/static/assets/download/terms-and-conditions.pdf) "
      "(effective Jan 2026); Instant $10k fee from on-chain transparency (Jun 2026); "
      "Classic list from TheTrustedProp’s Classic table; **WELCOME25** = 25% off new-trader access fees.")
    a("")
    a("## Verdict")
    a("")
    a("- **Classic 2-Step prints on every size** at WELCOME25 ($22–$449). $100k sale **$262** vs first-payout E[X] **$89** (BE $89; 20/40/60 = $111 / $148 / $222). Sale m **+66%**. The 3% max-per-trade rule is doing most of the work.")
    a("- **PFP 2-Step access alone is a hole from $100k up** ($74 sale vs $91 E[X]). **With the 1–3% funded fee, the funnel prints everywhere** (~**+60%** at $100k, leftover **~$135** per starter).")
    a("- **PFP 1-Step access already prints** (even $200k is +6%). Funnel leftover at $100k ~**$256**.")
    a("- **Instant Growth $10k @ $299 prints fat on first payout** (E[X] **$38**, m **+87%**). 46% of buyers take a small payout; 2% max/trade stops lottery blow-ups. Residual risk is the **tower** (account doubles each 6%).")
    a("- Hive Coin (200%, cap 50% of the next fee) and A-book clawbacks are extra firm protection not in these leftovers.")
    a("")
    a("## How the firm is built")
    a("")
    a("| Line | What the shopper buys | Split (A-book) | Eval | Funded / Instant |")
    a("|---|---|---|---|---|")
    a("| Classic 2-Step (NewBee / WorkerBee / QueenBee) | Full challenge fee up front | 70 / 80 / 90% | 8% then 6%; 5%/4%/3% daily EOD; 10% static; 3% max/trade; 3 days at ≥1% of initial | Same 10% static, no min days, weekend **not** allowed |")
    a("| Pay From Profits 2-Step | Cheap access fee **per phase**; funded fee 1–3% of size after pass | 80% | Same 8/6 · 5/10 · 3% max/trade · 3×1% days | Funded fee from first profits if Low/Moderate; 50% upfront if Medium/High |")
    a("| Pay From Profits 1-Step | Access fee once; 10% target | 80% | 10% · 5/10 · 3×1% days | Same funded-fee ladder |")
    a("| Instant Growth (Golden Tower) | Level-1 demo from **$10,000** | 80% | None | 6% static, **no daily**, 2% max/trade, 6% scale-to-double, L2+ A-book, $2k/day payout cap after 6% |")
    a("")
    a("- **No consistency rule.** Drawdowns are **balance-based static** (floor does not trail).")
    a("- **News allowed** on every line. Challenge weekend holding yes; **funded weekend holding no**.")
    a("- **Hive Coin:** 200% of the access/challenge fee on pass, spendable on later challenges, **max 50% of the next price**. Not a cash refund — ignored in BE.")
    a("- **A-book / B-book:** 80/70/90% applies only to A-book PnL. A risk-parameter breach moves the account to B-book; those profits are not withdrawable. This book does **not** haircut E[X] for that switch, so leftover here is a **lower bound** for the firm.")
    a("- Payouts: advertised **<60s** USDC via smart contract. Instant Growth daily cap **$2,000** after the 6% target (TOS). Reviews also cite a **$1,000**/day cap on other lines.")
    a("- 80% of challenge fees locked in the contract as payout liquidity (their FAQ).")
    a("")
    a("## Blended funnel")
    a("")
    a("| Plan | P1 | P2 / eval | Funded | P(pay) | P(yr1) | E[X] $100k | Days | Split |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in df_b.iterrows():
        a(f"| {r['Plan']} | {pct(r['Phase1'])} | {pct(r['EvalPass'])} | "
          f"{pct(r['Funded'])} | {pct(r['P_pay'])} | {pct(r['P_yr1'])} | "
          f"{usd(r['E_payout_100k'])} | {r['Avg_days']:.0f} | {int(r['Split']*100)}% |")
    a("")
    a("## Access / challenge fee vs first-payout E[X] (does the **sticker** print?)")
    a("")
    a("Sale m = (sale − E[X]) / sale. Prints if leftover ≥ −$1. "
      "**PFP stickers are access fees only** — they are not supposed to cover E[X]; see the funnel below.")
    a("")
    a("| Plan | Size | List | Sale | E[X] | BE | 20% | 40% | 60% | Sale m | Prints? |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for _, r in df_s.sort_values(["Family", "Plan", "Size"]).iterrows():
        a(f"| {r['Plan']} | {usd(r['Size'])} | {usd(r['List'])} | {usd(r['Sale'])} | "
          f"{usd(r['E_payout'])} | {usd(r['BE'])} | {usd(r['px_20'])} | {usd(r['px_40'])} | "
          f"{usd(r['px_60'])} | {100*r['sale_m']:+.0f}% | "
          f"{'yes' if r['prints'] else 'NO'} |")
    a("")
    a("## Pay From Profits — full-funnel leftover (this is the real P&L)")
    a("")
    a("Shopper pays access per phase (WELCOME25). If they pass, the firm also collects a **funded fee** = 1% / 2% / 2.5% / 3% of size for Low / Moderate / Medium / High. "
      "This book maps Pro+Semi → Low, Average → Moderate, Aggressive → Medium, Lottery → High.")
    a("")
    a("### PFP 2-Step")
    a("")
    a("| Size | Access sale | E[access] | E[funded fee] | E[revenue] | E[X] | Leftover | Funnel m | Prints? |")
    a("|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for _, r in pfp2.iterrows():
        a(f"| {usd(r['Size'])} | {usd(r['Access_sale'])} | {usd(r['E_access'])} | "
          f"{usd(r['E_funded_fee'])} | {usd(r['E_revenue'])} | {usd(r['E_payout'])} | "
          f"{usd(r['Leftover'])} | {100*r['m']:+.0f}% | {'yes' if r['prints'] else 'NO'} |")
    a("")
    a("### PFP 1-Step")
    a("")
    a("| Size | Access sale | E[access] | E[funded fee] | E[revenue] | E[X] | Leftover | Funnel m | Prints? |")
    a("|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for _, r in pfp1.iterrows():
        a(f"| {usd(r['Size'])} | {usd(r['Access_sale'])} | {usd(r['E_access'])} | "
          f"{usd(r['E_funded_fee'])} | {usd(r['E_revenue'])} | {usd(r['E_payout'])} | "
          f"{usd(r['Leftover'])} | {100*r['m']:+.0f}% | {'yes' if r['prints'] else 'NO'} |")
    a("")
    a("## Read")
    a("")
    a("1. **Classic 2-Step at TheTrustedProp stickers + WELCOME25** is a cheap 8/6 · 5/10 2-step with a 1% valid-day gate and 3% max/trade. "
      "70% split (NewBee) cuts E[X] vs an 80% peer. Hive Coin is extra cost only if passers rebuy.")
    a("2. **PFP access fees do not print on their own** — that is the product. The firm is selling a lottery ticket at $7–$74 and collecting **1–3% of notional** from the people who pass. Funnel leftover is the number that matters.")
    a("3. **Instant Growth $10k @ $299** is a 6% static corridor with **no daily** and a **2% max/trade**. "
      "Level 1 is B-book; they let you cash out **once**, then you must scale. Upgrade to the next size is **~2% of the new balance from profits**. "
      "If WELCOME25 does not apply (on-chain prints $299), judge it at $299.")
    a("4. Instant first-payout E[X] **understates** year-1 if anyone scales the tower (account doubles each 6%). "
      "The 6% DD on a doubling book is the firm’s main protection.")
    a("")
    a("## Failure mix (share of all paths)")
    a("")
    if df_f is not None and not df_f.empty:
        # Weight each profile's fail share by book mix.
        wmap = {name: p["weight"] for name, p in PROFILES.items()}
        df_f = df_f.copy()
        df_f["WShare"] = df_f["Profile"].map(wmap) * df_f["Share"]
        mix = df_f.groupby(["Product", "Reason"])["WShare"].sum().reset_index()
        a("| Product | Reason | Share of all buyers |")
        a("|---|---|---:|")
        for _, r in mix.sort_values(["Product", "WShare"], ascending=[True, False]).iterrows():
            if r["WShare"] < 0.02:
                continue
            a(f"| {r['Product']} | {r['Reason']} | {pct(r['WShare'])} |")
    a("")
    a("## Caveats")
    a("")
    a("- Classic **list** is from a review table, not a scraped checkout (Cloudflare blocked later live fetches). PFP and Instant Growth fees are from the TOS / on-chain feed.")
    a("- WorkerBee (80%, 4% daily) and QueenBee (90%, 3% daily) are not priced separately here; NewBee 70% is the Classic default.")
    a("- $100 minimum reward is assumed (not published). Instant may effectively need the 6% scale target before a full withdrawal.")
    a("- A-book clawback is **not** in E[X]; real leftover is higher for the firm.")
    a("")
    return "\n".join(lines) + "\n"


def main():
    n = 700
    df_p, df_f = run_all(n_sims=n, seed=42)
    df_b = blend(df_p)
    df_s = sku_rows(df_b)
    pfp2 = pfp_funnel(df_p, "FH PFP 2-Step", phases=2)
    pfp1 = pfp_funnel(df_p, "FH PFP 1-Step", phases=1)
    RESULTS.mkdir(parents=True, exist_ok=True)
    df_p.to_csv(RESULTS / "fundedhive_profiles.csv", index=False)
    df_b.to_csv(RESULTS / "fundedhive_blended.csv", index=False)
    df_s.to_csv(RESULTS / "fundedhive_skus.csv", index=False)
    pfp2.to_csv(RESULTS / "fundedhive_pfp2_funnel.csv", index=False)
    pfp1.to_csv(RESULTS / "fundedhive_pfp1_funnel.csv", index=False)
    md = write_md(df_b, df_s, df_p, df_f, pfp2, pfp1)
    path = RESULTS / "FUNDEDHIVE.md"
    path.write_text(md)
    print(df_b.to_string(index=False))
    print()
    print(df_s.to_string(index=False))
    print()
    print("PFP2 funnel")
    print(pfp2.to_string(index=False))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
