"""
Top-20 forex/CFD prop-firm catalog (Aug 2026).

Prices are list / sale (shopper pays). Sources noted per firm.
Rules are the binding evaluation + first-payout funded stage used in the MC.
Futures-only firms (Topstep, Apex) are omitted — different product, not a
Verodus SKU competitor.
"""

from __future__ import annotations

# phase helper
def P(target, max_dd, floor, daily, daily_type="sod", min_days=0, vdt=0.0,
      cons=None, trail_lock=None, daily_action="breach", max_risk=None,
      funded_risk=None):
    d = {
        "target": target,
        "max_dd": max_dd,
        "floor_type": floor,
        "daily_dd": daily,
        "daily_dd_type": daily_type,
        "daily_dd_basis": "initial",
        "min_days": min_days,
        "valid_day_threshold": vdt,
        "consistency": cons,
        "daily_dd_action": daily_action,
    }
    if trail_lock is not None:
        d["trail_lock_at"] = trail_lock
    if max_risk is not None:
        d["max_risk_per_trade"] = max_risk
    if funded_risk is not None:
        d["funded_risk_cap"] = funded_risk
    return d


def funded(max_dd, floor, daily, daily_type="sod", min_days=3, vdt=0.0,
           cons=None, trail_lock=None, daily_action="breach", funded_risk=None):
    return P(None, max_dd, floor, daily, daily_type, min_days, vdt, cons,
             trail_lock, daily_action, funded_risk=funded_risk)


def sku(*pairs):
    """pairs of (size, list, sale)."""
    return {int(s): (float(lst), float(sale)) for s, lst, sale in pairs}


PRODUCTS = {}


def add(key, firm, plan, family, phases, funded_rules, skus, refund="first",
        split=0.80, min_reward=100.0, instant=False, source="", discount="",
        first_reward_cap=None):
    PRODUCTS[key] = {
        "firm": firm,
        "plan": plan,
        "family": family,  # instant / 1-step / 2-step / 3-step
        "phases": phases,
        "funded": funded_rules,
        "skus": skus,
        "refund": refund,
        "split": split,
        "min_reward": min_reward,
        "instant": instant,
        "source": source,
        "discount": discount,
        "first_reward_cap": first_reward_cap,
    }


# =============================================================================
# 1. VERODUS — live index-eval.js 16 Aug 2026, VERO35
# =============================================================================
add("Verodus Instant", "Verodus", "Instant", "instant",
    [P(None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.005, 0.20)],
    None, sku((5e3,110,72),(1e4,184,121),(25e3,370,242),(5e4,594,389),(1e5,1032,676)),
    refund="none", split=0.80, instant=True, discount="VERO35",
    source="verodus.com Instant live: 3% daily / 6% trail never locks / 20% cons")

add("Verodus 1-Step", "Verodus", "1-Step", "1-step",
    [P(0.10, 0.06, "hybrid", 0.04, "sod", 0, 0.0, 0.50)],
    funded(0.06, "hybrid", 0.04, min_days=3, cons=None),
    sku((5e3,55,36),(1e4,92,60),(25e3,185,120),(5e4,297,193),(1e5,516,335),(2e5,1006,654)),
    refund="first", discount="VERO35", source="verodus.com/1-step.html")

add("Verodus 2-Step Lite", "Verodus", "2-Step Lite", "2-step",
    [P(0.08, 0.08, "static", 0.04, min_days=5), P(0.05, 0.08, "static", 0.04, min_days=5)],
    funded(0.08, "static", 0.04, min_days=3),
    sku((5e3,27,18),(1e4,51,33),(25e3,101,66),(5e4,204,133),(1e5,371,241),(2e5,734,477)),
    refund="first", discount="VERO35",
    source="verodus Lite + funded max DD 10%→8%")

add("Verodus 2-Step Pro", "Verodus", "2-Step Pro", "2-step",
    [P(0.10, 0.10, "static", 0.05, min_days=5), P(0.05, 0.10, "static", 0.05, min_days=5)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,31,20),(1e4,56,36),(25e3,131,85),(5e4,250,163),(1e5,455,296),(2e5,887,577)),
    refund="first", discount="VERO35", source="verodus.com/2-step-pro.html")

# =============================================================================
# 2. FTMO — trading-objectives Aug 2026, EUR×1.16, no sitewide sale
# =============================================================================
add("FTMO 1-Step", "FTMO", "1-Step", "1-step",
    [P(0.10, 0.10, "trailing", 0.03, "sod", 0, 0.0, 0.50)],
    funded(0.10, "trailing", 0.03, min_days=0, cons=0.50),
    sku((1e4,92,92),(25e3,231,231),(5e4,370,370),(1e5,579,579),(2e5,1159,1159)),
    refund="none", split=0.90, source="ftmo.com/en/trading-objectives Aug 2026")

add("FTMO 2-Step", "FTMO", "2-Step", "2-step",
    [P(0.10, 0.10, "static", 0.05, min_days=4), P(0.05, 0.10, "static", 0.05, min_days=4)],
    funded(0.10, "static", 0.05, min_days=0),
    sku((1e4,103,103),(25e3,290,290),(5e4,400,400),(1e5,626,626),(2e5,1253,1253)),
    refund="first", split=0.80, source="ftmo.com Aug 2026 EUR×1.16")

# =============================================================================
# 3. FundedNext Stellar — fundednext.com Aug 2026
# =============================================================================
add("FN Stellar 1-Step", "FundedNext", "Stellar 1-Step", "1-step",
    [P(0.10, 0.06, "static", 0.03, min_days=2)],
    funded(0.06, "static", 0.03, min_days=0),
    sku((6e3,66,66),(15e3,130,130),(25e3,220,220),(5e4,330,330),(1e5,570,570),(2e5,1100,1100)),
    refund="fourth", split=0.80, source="fundednext.com/cfds/stellar-1-step")

add("FN Stellar 2-Step", "FundedNext", "Stellar 2-Step", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=5), P(0.05, 0.10, "static", 0.05, min_days=5)],
    funded(0.10, "static", 0.05, min_days=0),
    sku((6e3,66,66),(15e3,130,130),(25e3,220,220),(5e4,330,330),(1e5,550,550),(2e5,1100,1100)),
    refund="first", split=0.80, source="fundednext.com/cfds/stellar-2-step")

add("FN Stellar Lite", "FundedNext", "Stellar Lite", "2-step",
    [P(0.08, 0.08, "static", 0.04, min_days=5), P(0.04, 0.08, "static", 0.04, min_days=5)],
    funded(0.08, "static", 0.04, min_days=0),
    sku((5e3,33,33),(1e4,59,59),(25e3,149,149),(5e4,249,249),(1e5,449,449)),
    refund="first", split=0.80, source="Trader Notion 2026 Stellar Lite $32 $5k")

add("FN Stellar Instant", "FundedNext", "Stellar Instant", "instant",
    [P(None, 0.06, "trailing", None, min_days=0, cons=None)],
    None,
    sku((2e3,59,59),(5e3,99,99),(1e4,199,199),(2e4,599,599)),
    refund="first", split=0.80, instant=True, source="fundednext Stellar Instant cap $20k")

# =============================================================================
# 4. The5ers
# =============================================================================
add("5ers High Stakes", "The5ers", "High Stakes", "2-step",
    [P(0.10, 0.10, "static", 0.05, min_days=3, vdt=0.005),
     P(0.05, 0.10, "static", 0.05, min_days=3, vdt=0.005)],
    funded(0.10, "static", 0.05, min_days=3, vdt=0.005),
    sku((5e3,35,35),(1e4,60,60),(2e4,99,99),(6e4,229,229),(1e5,395,395)),
    refund="none", split=0.80, source="the5ers.com High Stakes 2026 from $19-$35")

add("5ers Hyper Growth", "The5ers", "Hyper Growth", "1-step",
    [P(0.10, 0.06, "static", 0.03, min_days=0, daily_action="pause")],
    funded(0.06, "static", 0.03, min_days=0, daily_action="pause"),
    sku((5e3,260,260),(1e4,450,450),(2e4,850,850)),
    refund="none", split=0.50, source="the5ers Hyper Growth live-from-day-1 50% split")

add("5ers Bootcamp", "The5ers", "Bootcamp", "3-step",
    [P(0.06, 0.05, "static", None, min_days=0),
     P(0.06, 0.05, "static", None, min_days=0),
     P(0.06, 0.05, "static", None, min_days=0)],
    funded(0.04, "static", 0.03, min_days=0, daily_action="pause"),
    sku((2e4,22,22),(1e5,95,95)),
    refund="none", split=0.50, source="the5ers Bootcamp from $22; activation extra not modeled")

# =============================================================================
# 5. FundingPips — CryptoSlate 14 Aug 2026 + HELLO 20% except $100k
# =============================================================================
add("FP Zero", "FundingPips", "Zero", "instant",
    [P(None, 0.05, "trailing", 0.03, "intraday_peak", 7, 0.0025, 0.15, trail_lock=0.05)],
    None,
    sku((5e3,60,48),(1e4,88,70),(25e3,188,150),(5e4,244,195),(1e5,444,444),(2e5,888,710)),
    refund="none", split=0.80, instant=True, discount="HELLO 20% (not $100k)",
    source="fundingpips.com + CryptoSlate 14 Aug 2026")

add("FP 1-Step Flex", "FundingPips", "1-Step Flex", "1-step",
    [P(0.12, 0.12, "static", 0.03, min_days=0)],
    funded(0.12, "static", 0.03, min_days=0),
    sku((5e3,66,53),(1e4,99,79),(25e3,211,169),(5e4,313,250),(1e5,569,569)),
    refund="fourth", split=0.85, discount="HELLO 20% (not $100k)",
    source="fundingpips 1-Step Flex 12/3/12")

add("FP 2-Step Standard", "FundingPips", "2-Step Standard", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,34,27),(1e4,63,50),(25e3,168,134),(5e4,285,228),(1e5,544,544)),
    refund="fourth", split=0.80, discount="HELLO 20% (not $100k)",
    source="fundingpips 2-Step Standard 8/5 5/10")

add("FP 2-Step Flex", "FundingPips", "2-Step Flex", "2-step",
    [P(0.08, 0.12, "static", 0.04, min_days=3), P(0.05, 0.12, "static", 0.04, min_days=3)],
    funded(0.12, "static", 0.04, min_days=0),
    sku((5e3,32,26),(1e4,59,47),(25e3,159,127),(5e4,269,215),(1e5,555,555)),
    refund="none", split=0.85, discount="HELLO 20% (not $100k)",
    source="fundingpips 2-Step Flex 4/12")

add("FP 2-Step Pro", "FundingPips", "2-Step Pro", "2-step",
    [P(0.06, 0.06, "static", 0.03, min_days=1), P(0.06, 0.06, "static", 0.03, min_days=1)],
    funded(0.06, "static", 0.03, min_days=3),
    sku((5e3,29,23),(1e4,55,44),(25e3,134,107),(5e4,224,179),(1e5,422,422),(2e5,844,675)),
    refund="none", split=0.80, discount="HELLO 20% (not $100k)",
    source="fundingpips 2-Step Pro 6/6 3% daily")

# =============================================================================
# 6. E8 Markets
# =============================================================================
add("E8 One 6%", "E8 Markets", "E8 One 6%", "1-step",
    [P(0.09, 0.06, "trailing", 0.03, min_days=0, cons=0.40)],
    funded(0.06, "trailing", 0.03, min_days=0, cons=0.40),
    sku((5e3,59,59),(1e4,138,138),(25e3,228,228),(5e4,338,338),(1e5,538,538),(2e5,988,988)),
    refund="none", split=0.80, source="E8 One default ~6% trail / 9% target / 40% best day")

add("E8 Signature", "E8 Markets", "Signature", "1-step",
    [P(0.06, 0.04, "trailing", 0.02, min_days=3, vdt=0.003, cons=0.35)],
    funded(0.04, "trailing", 0.02, min_days=3, vdt=0.003, cons=0.35),
    sku((25e3,198,198),(5e4,298,298),(1e5,498,498)),
    refund="none", split=0.80, source="E8 Signature EOD trail + 35% best day")

# =============================================================================
# 7. Alpha Capital — 23 Jul 2026 + FUNDED40 / ALPHA20
# =============================================================================
add("Alpha Instant", "Alpha Capital", "Instant", "instant",
    [P(None, 0.05, "trailing", 0.03, "intraday_peak", 5, 0.003, 0.15)],
    None,
    sku((5e3,67,40),(1e4,97,58),(25e3,197,118),(5e4,257,154),(1e5,457,274),(2e5,897,538)),
    refund="none", split=0.80, instant=True, discount="FUNDED40",
    source="alphacapitalgroup.uk Instant Funding post")

add("Alpha One 10%", "Alpha Capital", "One 10%", "1-step",
    [P(0.10, 0.06, "trailing", 0.04, min_days=1, cons=0.40)],
    funded(0.06, "trailing", 0.04, min_days=0, cons=0.40),
    sku((5e3,50,40),(1e4,97,78),(25e3,197,158),(5e4,297,238),(1e5,497,398),(2e5,997,798)),
    refund="none", split=0.80, discount="ALPHA20",
    source="Alpha One 10% 6% trail lock 40% cons")

add("Alpha Pro 6%", "Alpha Capital", "Pro 6%", "2-step",
    [P(0.06, 0.06, "static", 0.03, min_days=3), P(0.06, 0.06, "static", 0.03, min_days=3)],
    funded(0.06, "static", 0.03, min_days=3),
    sku((5e3,27,22),(1e4,47,38),(25e3,117,94),(5e4,217,174),(1e5,397,318),(2e5,797,638)),
    refund="none", split=0.80, discount="ALPHA20",
    source="Alpha Pro 6/6 3% daily")

add("Alpha Pro 10%", "Alpha Capital", "Pro 10%", "2-step",
    [P(0.10, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,33,26),(1e4,77,62),(25e3,177,142),(5e4,267,214),(1e5,447,358),(2e5,897,718)),
    refund="none", split=0.80, discount="ALPHA20",
    source="Alpha Pro 10/5 5/10 — Lite-class hole")

# =============================================================================
# 8. Goat Funded Trader
# =============================================================================
add("Goat Instant", "Goat Funded", "Instant GOAT", "instant",
    [P(None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.005, 0.15, max_risk=0.02)],
    None,
    sku((5e3,79,63),(1e4,129,103),(25e3,249,199),(5e4,399,319),(1e5,699,559)),
    refund="none", split=0.80, instant=True, discount="~20% promo",
    source="help.goatfundedtrader.com Instant GOAT 3/6 trail + 2% float + 15% cons")

add("Goat 2-Step", "Goat Funded", "2-Step Standard", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.06, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,36,29),(1e4,66,53),(25e3,156,125),(5e4,266,213),(1e5,499,399)),
    refund="first", split=0.80, discount="~20% promo",
    source="goatfundedtrader 2-Step from $36 $5k")

# =============================================================================
# 9. Maven Trading
# =============================================================================
add("Maven 2-Step", "Maven", "2-Step", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,22,18),(1e4,44,35),(25e3,99,79),(5e4,189,151),(1e5,349,279)),
    refund="first", split=0.80, discount="~20% promo",
    source="cheapest-challenge 2026 Maven 2-step from $22")

add("Maven 3-Step", "Maven", "3-Step", "3-step",
    [P(0.06, 0.06, "static", 0.04, min_days=2),
     P(0.06, 0.06, "static", 0.04, min_days=2),
     P(0.06, 0.06, "static", 0.04, min_days=2)],
    funded(0.06, "static", 0.04, min_days=3),
    sku((5e3,17,14),(1e4,32,26),(25e3,69,55),(5e4,129,103),(1e5,249,199)),
    refund="first", split=0.80, discount="~20% promo",
    source="Maven 3-step from $17 $5k")

# =============================================================================
# 10. Hola Prime — MATCH20, FXEmpire 27 Jul 2026
# =============================================================================
add("Hola Direct", "Hola Prime", "Direct", "instant",
    [P(None, 0.07, "trailing", 0.03, "sod", 5, 0.005, 0.20, funded_risk=0.02)],
    None,
    sku((5e3,99,79),(1e4,132,106),(25e3,369,295),(5e4,689,551),(1e5,1049,839)),
    refund="quarter_x4", split=0.80, instant=True, discount="MATCH20",
    source="holaprime Direct 7% EOD trail 20% cons 2% funded risk")

add("Hola 1-Step Prime", "Hola Prime", "1-Step Prime", "1-step",
    [P(0.10, 0.06, "static", 0.03, min_days=2)],
    funded(0.06, "static", 0.03, min_days=3, funded_risk=0.02),
    sku((5e3,59,47),(1e4,89,71),(25e3,169,135),(5e4,329,263),(1e5,579,463),(2e5,1049,839)),
    refund="quarter_x4", split=0.80, discount="MATCH20",
    source="holaprime 1-Step 10/3/6 + 2% funded risk")

add("Hola 2-Step Prime", "Hola Prime", "2-Step Prime", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3, funded_risk=0.02),
    sku((5e3,47,38),(1e4,69,55),(25e3,159,127),(5e4,319,255),(1e5,569,455),(2e5,939,751)),
    refund="quarter_x4", split=0.80, discount="MATCH20",
    source="holaprime 2-Step Prime 8/5 5/10 + 2% funded risk")

# =============================================================================
# 11. FXIFY
# =============================================================================
add("FXIFY 2-Step", "FXIFY", "2-Step", "2-step",
    [P(0.10, 0.10, "trailing", 0.04, min_days=0), P(0.05, 0.10, "trailing", 0.04, min_days=0)],
    funded(0.10, "trailing", 0.04, min_days=0),
    sku((5e3,59,47),(1e4,89,71),(25e3,189,151),(5e4,379,303),(1e5,499,399),(2e5,999,799)),
    refund="first", split=0.80, discount="~20% typical",
    source="forexpropreviews FXIFY 2-step Feb 2026")

add("FXIFY Instant Lite", "FXIFY", "Instant Lite", "instant",
    [P(None, 0.04, "trailing", 0.03, "intraday_peak", 5, 0.0, 0.20, trail_lock=0.04)],
    None,
    sku((25e2,19,19),(5e3,39,39),(1e4,79,79),(25e3,149,149),(5e4,249,249),(1e5,399,399)),
    refund="none", split=0.80, instant=True,
    source="fxify.com Instant Funding Lite Feb 2026")

add("FXIFY Instant", "FXIFY", "Instant Standard", "instant",
    [P(None, 0.08, "trailing", None, min_days=0, trail_lock=0.08)],
    None,
    sku((5e3,109,87),(1e4,179,143),(25e3,329,263),(5e4,529,423),(1e5,799,639)),
    refund="none", split=0.80, instant=True, discount="~20% typical",
    source="fxify Instant Standard 8% trail no daily")

# =============================================================================
# 12. Instant Funding (the firm)
# =============================================================================
add("IF Instant", "Instant Funding", "Instant", "instant",
    [P(None, 0.06, "trailing", 0.03, "intraday_peak", 5, 0.0, 0.20)],
    None,
    sku((5e3,109,87),(1e4,179,143),(25e3,329,263),(5e4,529,423),(1e5,799,639)),
    refund="none", split=0.80, instant=True, discount="~20% typical",
    source="fxify comparison table Instant Funding 3/6")

# =============================================================================
# 13. Fintokei
# =============================================================================
add("Fintokei ProTrader", "Fintokei", "ProTrader", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,44,35),(1e4,99,79),(25e3,199,159),(5e4,299,239),(1e5,529,423),(2e5,999,799)),
    refund="first", split=0.80, discount="20% OFF listed",
    source="fintokei.com + propvator $529 $100k 2-step")

add("Fintokei SwiftTrader", "Fintokei", "SwiftTrader", "1-step",
    [P(0.10, 0.06, "static", 0.04, min_days=2)],
    funded(0.06, "static", 0.04, min_days=3),
    sku((5e3,44,35),(1e4,89,71),(25e3,179,143),(5e4,289,231),(1e5,499,399)),
    refund="first", split=0.80, discount="20% OFF listed",
    source="fintokei SwiftTrader 1-step from $44")

# =============================================================================
# 14. For Traders
# =============================================================================
add("ForTraders 2-Step", "For Traders", "2-Step", "2-step",
    [P(0.08, 0.08, "static", 0.04, min_days=3), P(0.05, 0.08, "static", 0.04, min_days=3)],
    funded(0.08, "static", 0.04, min_days=3),
    sku((5e3,49,39),(1e4,89,71),(25e3,179,143),(5e4,289,231),(1e5,489,391)),
    refund="first", split=0.80, discount="~20% typical",
    source="typical For Traders 2-step 8/5 4/8 2026 reviews")

# =============================================================================
# 15. The Funded Trader
# =============================================================================
add("TFT Standard", "The Funded Trader", "Standard", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,49,39),(1e4,99,79),(25e3,189,151),(5e4,289,231),(1e5,499,399),(2e5,939,751)),
    refund="first", split=0.80, discount="~20% typical",
    source="TFT Standard from ~$49 $5k")

add("TFT Royal", "The Funded Trader", "Royal 1-Step", "1-step",
    [P(0.10, 0.06, "static", 0.04, min_days=0)],
    funded(0.06, "static", 0.04, min_days=3),
    sku((5e3,79,63),(1e4,129,103),(25e3,249,199),(5e4,379,303),(1e5,599,479)),
    refund="none", split=0.80, discount="~20% typical",
    source="TFT Royal-class 1-step")

# =============================================================================
# 16. City Traders Imperium
# =============================================================================
add("CTI 2-Step", "City Traders Imperium", "2-Step", "2-step",
    [P(0.10, 0.10, "static", 0.05, min_days=4), P(0.05, 0.10, "static", 0.05, min_days=4)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((1e4,99,79),(25e3,199,159),(5e4,349,279),(1e5,549,439)),
    refund="first", split=0.80, discount="~20% typical",
    source="CTI classic 10/5 5/10")

# =============================================================================
# 17. Funding Traders
# =============================================================================
add("FundingTraders 2-Step", "Funding Traders", "2-Step", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=3), P(0.05, 0.10, "static", 0.05, min_days=3)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,36,29),(1e4,66,53),(25e3,156,125),(5e4,266,213),(1e5,499,399)),
    refund="first", split=0.80, discount="~20% typical",
    source="Funding Traders mid-tier 2-step")

# =============================================================================
# 18. Blue Guardian
# =============================================================================
add("BG Instant", "Blue Guardian", "Instant", "instant",
    [P(None, 0.06, "trailing", 0.03, "sod", 5, 0.0, 0.20, trail_lock=0.06)],
    None,
    sku((5e3,72,54),(1e4,100,75),(25e3,208,156),(5e4,324,243),(1e5,623,467)),
    refund="none", split=0.80, instant=True, discount="BG25",
    source="blueguardian.com Instant 16 Aug 2026: 3% daily of initial from SOD, "
           "6% trail locks at +6% + 1% buffer, 20% cons, BG25 25% off")

add("BG 1-Step", "Blue Guardian", "1-Step Standard", "1-step",
    [P(0.10, 0.08, "static", 0.04, min_days=0)],
    funded(0.08, "static", 0.04, min_days=3),
    sku((5e3,59,47),(1e4,99,79),(25e3,189,151),(5e4,299,239),(1e5,499,399),(2e5,899,719)),
    refund="first", split=0.80, discount="~20% typical",
    source="thetrustedprop BG 1-step 10/4/8")

add("BG 2-Step", "Blue Guardian", "2-Step Standard", "2-step",
    [P(0.08, 0.10, "static", 0.04, min_days=3), P(0.05, 0.10, "static", 0.04, min_days=3)],
    funded(0.10, "static", 0.04, min_days=3),
    sku((5e3,55,44),(1e4,97,78),(25e3,187,150),(5e4,287,230),(1e5,497,398)),
    refund="first", split=0.80, discount="~20% typical",
    source="blueguardian 2-step standard")

# =============================================================================
# 19. BrightFunded
# =============================================================================
add("BrightFunded 2-Step", "BrightFunded", "2-Step", "2-step",
    [P(0.08, 0.10, "static", 0.05, min_days=5), P(0.05, 0.10, "static", 0.05, min_days=5)],
    funded(0.10, "static", 0.05, min_days=3),
    sku((5e3,55,44),(1e4,99,79),(25e3,189,151),(5e4,289,231),(1e5,399,319),(2e5,297,238)),
    refund="first", split=0.80, discount="~20% typical",
    source="brightfunded 8/5 5/10 from $55; $200k listed $297 review")

# =============================================================================
# 20. Ment Funding (Seacrest-class mid-tier)
# =============================================================================
add("Ment 2-Step", "Ment Funding", "2-Step", "2-step",
    [P(0.08, 0.08, "static", 0.04, min_days=3), P(0.05, 0.08, "static", 0.04, min_days=3)],
    funded(0.08, "static", 0.04, min_days=3),
    sku((5e3,39,31),(1e4,69,55),(25e3,149,119),(5e4,249,199),(1e5,429,343)),
    refund="first", split=0.80, discount="~20% typical",
    source="Ment/Seacrest-class 8/5 4/8 mid-tier 2026")

FIRMS = sorted({p["firm"] for p in PRODUCTS.values()})
