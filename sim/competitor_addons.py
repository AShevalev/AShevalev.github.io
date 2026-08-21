"""Street checkout add-ons for the 19 peer firms + Verodus rec.

Percents are of the firm's own challenge fee (list or sale as they bill).
Sources: official help/checkout, Aug 2026. CFD book only (Goat futures 90%
+20% is noted, not mixed into the CFD rec).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Verodus locked rec (of list). VERO35 then takes 35% off list + stickers.
# Attractiveness pass: weekly is 80% (not a 70% decoy) at 8%; Instant 90%
# solo matches Blue Guardian Instant 90% at 15%. 90%+anytime Instant stays 32%.
VERO = {
    "news": 0.12,
    "weekend": 0.12,
    "swing": 0.20,
    "weekly": 0.08,
    "od80_eval": 0.12,
    "od80_instant": 0.15,
    "split90_eval": 0.12,
    "split90_instant": 0.15,
    "od90_eval": 0.20,
    "od90_instant": 0.32,
    "qty": "1–4 at VERO35, no extra ladder",
}

# One row per firm. pct = fraction of challenge fee, or None if not sold.
# how: addon | included | sku | cycle | config | none | restricted
FIRMS = [
    {
        "firm": "FTMO",
        "news": "restricted funded (2-min); Swing SKU removes it",
        "weekend": "flatten Friday; Swing SKU holds",
        "swing": "separate 2-Step SKU, ~10–15% premium, 1:30 lev",
        "split90": "1-Step included; 2-Step scales — no checkout 90%",
        "ondemand": "no — biweekly",
        "weekly": "no",
        "bundle": "Swing is the news+weekend SKU",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": 0.12,
        "note": "No add-on menu. Swing is a product, not +% toggles.",
    },
    {
        "firm": "FundedNext",
        "news": "funded 5-min window, profits cut to 40%",
        "weekend": "not on master",
        "swing": "not sold",
        "split90": "Lifetime 95%: +25% 1-Step / +30% 2-Step & Lite",
        "ondemand": "+5% and includes 95% + 40% consistency",
        "weekly": "Bi-weekly: +25% 2-Step / +15% Lite (small sizes)",
        "bundle": "addons stack (no save). Double Up +40% = 2nd account 60% off after pass",
        "qty": "Double Up +40% (2nd after funded), not a 4-pack",
        "split90_pct": 0.30,
        "od_pct": 0.05,
        "weekly_pct": 0.25,
        "swing_pct": None,
        "note": "On-demand +5% with 95% is a loss-leader. Do not match.",
    },
    {
        "firm": "The5ers",
        "news": "allowed (program rules)",
        "weekend": "included, all programs",
        "swing": "included — no SKU",
        "split90": "program ladder (50–100%), not checkout",
        "ondemand": "no — 14-day then biweekly",
        "weekly": "no",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": 0.0,
        "note": "Holding is free. Split is the product, not an add-on.",
    },
    {
        "firm": "FundingPips",
        "news": "funded 5-min restriction",
        "weekend": "master flatten Friday (verify live)",
        "swing": "not sold",
        "split90": "on-demand cycle = 90%; monthly = 100%; weekly = 60%",
        "ondemand": "included as a cycle (consistency)",
        "weekly": "included as a cycle at 60% split",
        "bundle": "cycle IS the split — not two addons",
        "qty": "none published",
        "split90_pct": 0.0,
        "od_pct": 0.0,
        "weekly_pct": 0.0,
        "swing_pct": None,
        "note": "No % add-on menu. Shopper picks a cycle. Weekly is a worse split.",
    },
    {
        "firm": "E8 Markets",
        "news": "eval free; funded 5-min ban",
        "weekend": "E8 One allowed; Signature daily flatten",
        "swing": "not a toggle",
        "split90": "80/90/100 chosen at config; baked into fee",
        "ondemand": "after 14 days + profitable days",
        "weekly": "no",
        "bundle": "config, not a 5% save bundle",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "Higher split raises the sticker; % not a separate line.",
    },
    {
        "firm": "Alpha Capital",
        "news": "Swing plan; standard restricted",
        "weekend": "Swing plan holds",
        "swing": "separate plan (like FTMO)",
        "split90": "+~10% of on-demand price (e.g. $18 on $177)",
        "ondemand": "plan variant (On-Demand Pro), not +%",
        "weekly": "no — biweekly vs on-demand XOR at qualification",
        "bundle": "90% is on the on-demand price, not stacked with speed",
        "qty": "none published",
        "split90_pct": 0.10,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "Cheapest published 90% (10%). Speed is a SKU, not 15%.",
    },
    {
        "firm": "Goat Funded",
        "news": "CFD allowed (funded profit cap near news on some models)",
        "weekend": "CFD allowed",
        "swing": "included on CFD",
        "split90": "100% checkout add-on (CFD % unpublished; futures 90% is +20%)",
        "ondemand": "2-Step Standard/Pro add-on; GOAT first payout 40% split",
        "weekly": "no — biweekly default; Instant 10-day",
        "bundle": "100% and on-demand are separate toggles",
        "qty": "none published",
        "split90_pct": 0.20,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": 0.0,
        "note": "Use +20% as the CFD 100% proxy (futures 90% is +20%). Holding free.",
    },
    {
        "firm": "Maven",
        "news": "program-dependent",
        "weekend": "program-dependent; Swing plan exists",
        "swing": "separate plan",
        "split90": "core forex 80%; 90% ~10% on some plans (not all)",
        "ondemand": "10-business-day default",
        "weekly": "no",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": 0.10,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "Cheap sticker, 80% default. Do not lead Verodus with 90%.",
    },
    {
        "firm": "Hola Prime",
        "news": "program-dependent",
        "weekend": "program-dependent",
        "swing": "not a % addon",
        "split90": "cycle: weekly 65% / biweekly 80% / monthly 95%",
        "ondemand": "available on some plans (chosen at checkout)",
        "weekly": "cycle at 65% split",
        "bundle": "cycle IS the split",
        "qty": "none published",
        "split90_pct": 0.0,
        "od_pct": None,
        "weekly_pct": 0.0,
        "swing_pct": None,
        "note": "Same idea as FundingPips. Faster cycle = worse split.",
    },
    {
        "firm": "FXIFY",
        "news": "included on evals; Instant restricted",
        "weekend": "included on evals; Instant flatten Friday",
        "swing": "included on evals",
        "split90": "+20% of evaluation fee",
        "ondemand": "evals first-payout on-demand; Instant 14-day",
        "weekly": "biweekly +5% (default monthly)",
        "bundle": "stack, no save (90%+20 and biweekly+5 = +25%)",
        "qty": "none published",
        "split90_pct": 0.20,
        "od_pct": None,
        "weekly_pct": 0.05,
        "swing_pct": 0.0,
        "note": "Evals: holding free, 90% is +20%. Instant 90% included.",
    },
    {
        "firm": "Instant Funding",
        "news": "addon: Allow major news + weekend holding (one SKU)",
        "weekend": "same addon as news (funded)",
        "swing": "that bundled addon",
        "split90": "Add 10% to profit split (80→90); fee % not on homepage",
        "ondemand": "weekly after 14-day wait on core Instant",
        "weekly": "included on Instant",
        "bundle": "news+weekend are one add-on (like Verodus Swing)",
        "qty": "PlusPoints 10% back, up to 50% next order — not a 4-pack",
        "split90_pct": 0.10,
        "od_pct": None,
        "weekly_pct": 0.0,
        "swing_pct": None,
        "note": "Swing is one toggle. 90% addon named +10pp split; treat fee as ~10%.",
    },
    {
        "firm": "Fintokei",
        "news": "allowed",
        "weekend": "included; ProTrader Swing is a SKU",
        "swing": "separate ProTrader Swing SKU (swap-free)",
        "split90": "SwiftTrader 90% included; ProTrader 80%",
        "ondemand": "instant payout processing (not a +%)",
        "weekly": "no",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": 0.0,
        "od_pct": 0.0,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "90% and holding are the product. No checkout % menu.",
    },
    {
        "firm": "For Traders",
        "news": "eval free; funded 5-min ban",
        "weekend": "included, all programs",
        "swing": "included",
        "split90": "customizer at checkout (higher split = higher fee)",
        "ondemand": "Instant scales 10pp per payout to 90%",
        "weekly": "no",
        "bundle": "BOGO promos (not a % ladder)",
        "qty": "BOGO / NEW20 / TRADE15 — not 4-pack 30/35/40",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": 0.0,
        "note": "Holding free. Split is a config slider.",
    },
    {
        "firm": "The Funded Trader",
        "news": "program-dependent",
        "weekend": "program-dependent",
        "swing": "not a standard % addon",
        "split90": "up to 95% on some SKUs, not a clean +% line",
        "ondemand": "Knight Pro anytime",
        "weekly": "every 7 days on some SKUs",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "SKU mix, not a Verodus-style toggle menu.",
    },
    {
        "firm": "City Traders Imperium",
        "news": "program-dependent",
        "weekend": "program-dependent",
        "swing": "not published as +%",
        "split90": "80% typical; no 90% add-on on core 2-Step",
        "ondemand": "included on core",
        "weekly": "no",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": 0.0,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "On-demand at 80% is the product.",
    },
    {
        "firm": "Funding Traders",
        "news": "not a published checkout addon",
        "weekend": "not a published checkout addon",
        "swing": "none",
        "split90": "none published",
        "ondemand": "none published",
        "weekly": "none published",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "No public add-on menu in the 20-firm CFD set.",
    },
    {
        "firm": "Blue Guardian",
        "news": "not a separate toggle",
        "weekend": "not a separate toggle on Instant (on-demand included)",
        "swing": "not sold as 12+12",
        "split90": "+15% (evals vs 85%; Instant vs 80%)",
        "ondemand": "Instant included at 80%; evals 7-day +15%",
        "weekly": "7-day +15%",
        "bundle": "90% + 7-day = +25% (save 5pp vs 30%)",
        "qty": "1st site code 25%, 2nd 30%, 3rd 35%, 4th 40%; 5th-free on some futures",
        "split90_pct": 0.15,
        "od_pct": 0.15,
        "weekly_pct": 0.15,
        "swing_pct": None,
        "note": "Template for Verodus evals. Instant 15% for 90%+OD is insolvent here.",
    },
    {
        "firm": "BrightFunded",
        "news": "restricted funded; paid news addon (fee variable)",
        "weekend": "included",
        "swing": "holding free; news is extra",
        "split90": "+20% of base (e.g. EUR 99 on Saturn 100k EUR 495)",
        "ondemand": "no — first payout 30 days then biweekly",
        "weekly": "+25% of fee (or EUR 25–50 in one guide)",
        "bundle": "stack, no save; fee-refund addon +10%",
        "qty": "none published (codes EARLY25 / BF10)",
        "split90_pct": 0.20,
        "od_pct": None,
        "weekly_pct": 0.25,
        "swing_pct": 0.0,
        "note": "90% +20% matches FXIFY. Weekly is expensive vs Verodus 8%.",
    },
    {
        "firm": "Ment Funding",
        "news": "not a published +%",
        "weekend": "not a published +%",
        "swing": "none",
        "split90": "Forex 75% default, 90% paid addon (fee % unpublished)",
        "ondemand": "14-day cycle",
        "weekly": "no",
        "bundle": "n/a",
        "qty": "none published",
        "split90_pct": None,
        "od_pct": None,
        "weekly_pct": None,
        "swing_pct": None,
        "note": "90% exists; % not on the public CFD help we could pin.",
    },
]


def pct_s(x):
    if x is None:
        return "—"
    if x == 0:
        return "incl."
    return f"{round(100 * x)}%"


def write_csv():
    import csv
    path = RESULTS / "competitor_addons.csv"
    fields = [
        "Firm", "News", "Weekend", "Swing", "Split90", "OnDemand", "Weekly",
        "Bundle", "Qty", "Split90_pct", "OD_pct", "Weekly_pct", "Swing_pct", "Note",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in FIRMS:
            w.writerow({
                "Firm": r["firm"],
                "News": r["news"],
                "Weekend": r["weekend"],
                "Swing": r["swing"],
                "Split90": r["split90"],
                "OnDemand": r["ondemand"],
                "Weekly": r["weekly"],
                "Bundle": r["bundle"],
                "Qty": r["qty"],
                "Split90_pct": r["split90_pct"] if r["split90_pct"] is not None else "",
                "OD_pct": r["od_pct"] if r["od_pct"] is not None else "",
                "Weekly_pct": r["weekly_pct"] if r["weekly_pct"] is not None else "",
                "Swing_pct": r["swing_pct"] if r["swing_pct"] is not None else "",
                "Note": r["note"],
            })
    return path


def leftover(list_px, pct, extra):
    """After VERO35 and 20% ads, minus extra E[X]."""
    sticker = int(round(list_px * pct))
    return sticker * 0.65 * 0.80 - extra, sticker


def write_md():
    path = RESULTS / "COMPETITOR_ADDONS.md"
    lines = []
    a = lines.append
    a("# Competitor checkout add-ons (19 peers + Verodus rec)")
    a("")
    a("CFD book, Aug 2026. Percents are of **that firm’s challenge fee**. Verodus stickers are of **list**, then VERO35 takes 35% off list + stickers.")
    a("")
    a("## Street menu")
    a("")
    a("| Firm | 90% / higher split | Faster payout | News / weekend | Qty bundle |")
    a("|---|---|---|---|---|")
    for r in FIRMS:
        a(f"| {r['firm']} | {r['split90']} | {r['ondemand'] if r['ondemand'] != 'no' else r['weekly']} | {r['swing']} | {r['qty']} |")
    a("")
    a("## Published +% (where pinned)")
    a("")
    a("| Firm | 90%/100% | On-demand / 7-day | Weekly | Swing / holding |")
    a("|---|---:|---:|---:|---:|")
    for r in FIRMS:
        a(f"| {r['firm']} | {pct_s(r['split90_pct'])} | {pct_s(r['od_pct'])} | {pct_s(r['weekly_pct'])} | {pct_s(r['swing_pct'])} |")
    a("")
    a("incl. = in the base product (0% extra). — = not sold as a % line.")
    a("")
    a("## What the street is doing")
    a("")
    a("- **Holding:** The5ers, Fintokei, For Traders, Goat CFD, FXIFY evals include weekend. FTMO / Alpha / Maven / Instant Funding sell Swing as a **SKU or one toggle**. Charging 12%+12% and bundling at 20% is in-family with Instant Funding’s news+weekend addon and FTMO Swing (~10–15% SKU premium + lower leverage).")
    a("- **90%:** Published fees cluster **10–20%** of the challenge (Alpha ~10%, BG 15%, FXIFY / BrightFunded 20%, Goat futures 90% 20%, FN 95% **25–30%**). FundedNext on-demand **+5% with 95%** is an outlier — do not match.")
    a("- **Speed:** BG eval 7-day **+15%**. FXIFY biweekly **+5%**. BrightFunded weekly **+25%**. FN biweekly **+15–25%**. FundingPips / Hola make faster cycles a **worse split**, not a fee.")
    a("- **90% + speed bundle:** Only BG publishes a real save (15+15 → **25%**). FXIFY stacks 20+5 with no save. FN’s +5% on-demand already includes 95%.")
    a("- **Qty:** Only BG has a shopper-facing 4-pack ladder (25/30/35/40). FN Double Up is +40% now for a 2nd account later. For Traders uses BOGO. Instant Funding uses points on the next order.")
    a("")
    a("## Verodus rec vs that street")
    a("")
    a("| Add-on | Verodus rec | Street | Keep? |")
    a("|---|---|---|---|")
    a("| News | 12% of list | Usually included on eval, restricted funded, or inside Swing | **Keep** — below live 15% |")
    a("| Weekend | 12% of list | Often included; else Swing SKU ~10–15% | **Keep** — below live 18% |")
    a("| Swing (both) | **20%** | FTMO Swing ~10–15% SKU; Instant Funding one toggle; BG does not sell this pair | **Keep** — 4pp save vs 24% |")
    a("| Weekly 80% | **8%** | 5–25% for faster cadence **without** cutting split (FP weekly is 60%) | **Change** — was 70% @ 6% (gotcha vs default 80%). 8% still prints |")
    a("| On-demand 80% | 12% eval / **15% Instant** | BG Instant includes it; BG eval 7-day 15%; FN +5% is a hole | **Keep** — match BG 7-day, not FN +5% |")
    a("| 90% split | 12% eval / **15% Instant** | Alpha 10%, BG 15%, FXIFY/BrightFunded 20% | **Change Instant** — 20% → 15% to match BG Instant 90% solo. Eval stays 12% |")
    a("| 90% On Demand | **20% eval / 32% Instant** | BG evals 25%; BG Instant 15% (OD included); FN +5% | **Keep** — eval cheaper than BG 25%; Instant 32% is the year-1 floor, not a street match |")
    a("| Qty 1–4 | VERO35 on every copy, no extra ladder | BG 30/35/40 on copies; 5th-free futures | **Keep** — Instant/Lite leftover cannot fund extra %; VERO35 already 35% vs BG 25% |")
    a("")
    a("## Leftover check (Instant / Pro $100k)")
    a("")
    a("After ads = sticker × 0.52 − extra E[X]. Instant extra: speed ~0.12 × BE $284; 90% ~0.125 × BE; both 0.41 × BE. Pro extra: first-payout 0.125 × BE $151.")
    a("")
    inst_list, pro_list = 675, 445
    inst_be, pro_be = 283.99, 150.61
    rows = [
        ("Instant weekly 80% @ 8%", inst_list, 0.08, 0.08 * inst_be),
        ("Instant 80% OD 15%", inst_list, 0.15, 0.12 * inst_be),
        ("Instant 90% solo 15%", inst_list, 0.15, 0.125 * inst_be),
        ("Instant 90% solo 20% (old)", inst_list, 0.20, 0.125 * inst_be),
        ("Instant 90% OD 32%", inst_list, 0.32, 0.41 * inst_be),
        ("Instant 90% OD at BG 15%", inst_list, 0.15, 0.41 * inst_be),
        ("Instant 90% OD at FN 5%", inst_list, 0.05, 0.41 * inst_be),
        ("Pro weekly 80% @ 8%", pro_list, 0.08, 0.05 * pro_be),
        ("Pro 80% OD 12%", pro_list, 0.12, 0.05 * pro_be),
        ("Pro 90% 12%", pro_list, 0.12, 0.125 * pro_be),
        ("Pro 90% OD 20%", pro_list, 0.20, 0.125 * pro_be),
        ("Pro 90% OD at BG 25%", pro_list, 0.25, 0.125 * pro_be),
        ("Pro Swing 20%", pro_list, 0.20, 0.06 * pro_be),
        ("Instant Swing 20%", inst_list, 0.20, 0.13 * inst_be),
    ]
    a("| SKU | Sticker | Extra E[X] | After ads |")
    a("|---|---:|---:|---:|")
    for name, lst, pct, extra in rows:
        left, sticker = leftover(lst, pct, extra)
        if left >= -1:
            flag = "yes"
        elif left >= -5:
            flag = "thin"
        else:
            flag = "NO"
        a(f"| {name} | ${sticker} | ${extra:.0f} | ${left:.0f} {flag} |")
    a("")
    a("Matching BG Instant 15% or FN +5% for **90%+anytime** on Instant $100k is a hole (**−$64** / **−$99**). Instant **90% solo** at 15% still prints (~+$17) because extra E[X] is the split only. The 32% bundle is the year-1 floor. Evals at 20% still print vs BG’s 25%.")
    a("")
    a("## Attractiveness changes (locked)")
    a("")
    a("1. **Weekly 70% @ 6% → Weekly 80% @ 8%.** Shoppers compare to the default 80% biweekly. FundingPips/Hola make faster cycles a worse split; that reads as a trap. 8% of list undercuts BG 7-day 15% and BrightFunded weekly 25%. Instant leftover ~+$5; Pro leftover ~+$11.")
    a("2. **Instant 90% solo 20% → 15%.** Matches Blue Guardian’s Instant 90% add-on. Solo leftover ~+$17. Do **not** drop the 90%+anytime bundle below 32%.")
    a("")
    a("Do not cheapen Swing 20%, eval 90% On Demand 20%, Instant 90% On Demand 32%, or add a 4-pack extra-% ladder. Do not match FundedNext +5%.")
    a("")
    a("## Bundling rec")
    a("")
    a("1. **Swing** news+weekend → 20% (street: Instant Funding one toggle; FTMO Swing SKU).")
    a("2. **90% On Demand** speed+90% → 20% eval / 32% Instant (street: BG evals 25%; Instant cannot copy 15% for both).")
    a("3. **Weekly XOR** both payout upgrades.")
    a("4. **Qty 1–4** at VERO35, same add-ons, no 30/35/40 ladder, no 5th free.")
    a("")
    a("Challenge rec fees do not move.")
    a("")
    path.write_text("\n".join(lines) + "\n")
    return path


def main():
    RESULTS.mkdir(exist_ok=True)
    c = write_csv()
    m = write_md()
    print(f"Wrote {c}")
    print(f"Wrote {m}")
    inst_list, inst_be = 675, 283.99
    for name, pct, extra in [
        ("BG Instant 15% 90%+OD", 0.15, 0.41 * inst_be),
        ("Verodus Instant 32%", 0.32, 0.41 * inst_be),
        ("FN 5%", 0.05, 0.41 * inst_be),
    ]:
        left, st = leftover(inst_list, pct, extra)
        print(f"  {name}: sticker ${st} leftover ${left:.1f}")


if __name__ == "__main__":
    main()
