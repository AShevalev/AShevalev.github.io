# Verodus rulebook — one set of rules per category, every size

Every percentage below is of **initial balance** unless stated. A $5k Instant and a $200k Instant use the **same** card. A $5k Lite and a $200k Lite use the **same** card. Do not add size-specific daily, consistency, or payout rules.

The only dollar figure that stays fixed across sizes is the **$100 minimum reward** (industry standard; it binds $5k more than $200k, which is correct).

---

## Shared (all four categories, all sizes)

| Rule | Setting |
|---|---|
| Account sizes | $5,000 · $10,000 · $25,000 · $50,000 · $100,000 · $200,000 |
| Discount | VERO35 (35% off list). Same code on every SKU. |
| Profit split | 80% default. 90% is a **paid add-on**, not the default. |
| Minimum reward | $100 |
| Time limit | None |
| Inactivity | 30 calendar days with no trade → fail / close |
| Daily DD basis | Dollars of **initial** balance (not a % of today’s equity) |
| Platforms / news / EAs / weekend | One policy for the whole firm, not per size |
| Leverage | One number per category, not per size |
| Scaling | After first payout; does not change the first-payout rulebook |

---

## Instant — complete card (every size)

Funded on purchase. No evaluation. No profit target.

| # | Rule | Setting | Why |
|---|---|---|---|
| 1 | Access | Instant funded | Category definition |
| 2 | Profit target | None | |
| 3 | Daily drawdown | **3%** of initial, from the **day’s equity high** (intraday). Breach = fail | Industry Instant standard |
| 4 | Max drawdown | **6% trailing** on HWM. **Never locks** | Live FAQ. Unchanged |
| 5 | Consistency | Best **closed** day ≤ **20%** of the sum of positive days | Stops lottery first payouts |
| 6 | Minimum trading days | **5 valid days** | |
| 7 | Valid day | Closed day PnL ≥ **0.5%** of that day’s start-of-day equity | |
| 8 | Max risk per trade | None | Not added |
| 9 | First reward | **$100 minimum only.** No % cap | Not added |
| 10 | Later rewards | Same 20% consistency | |
| 11 | Fee refund | **No** | Instant P(pay) is high; a refund would tax every sale |
| 12 | Split | 80% | |

Instant is the **live** card. Do not add a +5% trail lock, a 2% max-risk rule, or a first-reward % cap.

---

## 1-Step — complete card (every size)

One evaluation phase, then funded.

### Evaluation

| # | Rule | Setting |
|---|---|---|
| 1 | Profit target | **10%** of initial, all positions closed |
| 2 | Daily drawdown | **4%** of initial, from **start-of-day equity**. Breach = fail |
| 3 | Max drawdown | **6% hybrid**: trails HWM, **locks at initial**. Never above initial |
| 4 | Consistency | Best closed day ≤ **50%** of the sum of positive days |
| 5 | Minimum trading days | **None** (the 50% best-day rule already forces more than one green day) |
| 6 | Time / inactivity | Unlimited / 30 days |

### Funded (after pass)

| # | Rule | Setting |
|---|---|---|
| 7 | Profit target | None |
| 8 | Daily drawdown | **4%** SOD, same as eval |
| 9 | Max drawdown | **6% hybrid**, same as eval |
| 10 | Consistency | **None** |
| 11 | Minimum trading days before first reward | **3** |
| 12 | Valid day (funded) | Any day with a closed trade (no 0.5% hurdle) |
| 13 | Fee refund | **100% of the fee on the first successful reward** |
| 14 | Split | 80% |
| 15 | Min / max first reward | Min $100. **No % cap** (eval already filtered) |

The 6% hybrid is the 1-Step profit engine. Do not widen it to 8% or 10% on large accounts.

---

## 2-Step Lite — complete card (every size)

Cheap 2-step. **Funded max DD matches eval (8%)** — do not keep the old 10% funded hole.

### Phase 1

| # | Rule | Setting |
|---|---|---|
| 1 | Profit target | **8%** |
| 2 | Daily drawdown | **4%** of initial, SOD. Breach = fail |
| 3 | Max drawdown | **8% static** from initial |
| 4 | Minimum trading days | **5** |
| 5 | Consistency | None |
| 6 | Time / inactivity | Unlimited / 30 days |

### Phase 2

| # | Rule | Setting |
|---|---|---|
| 7 | Profit target | **5%** |
| 8 | Daily / max / min days | **Same as Phase 1** (4% / 8% static / 5 days) |

### Funded

| # | Rule | Setting |
|---|---|---|
| 9 | Profit target | None |
| 10 | Daily drawdown | **4%** SOD |
| 11 | Max drawdown | **8% static** (same as eval — this is the change) |
| 12 | Consistency | None |
| 13 | Min days before first reward | **3** |
| 14 | Fee refund | **100% on first successful reward** |
| 15 | Split | 80% |
| 16 | Min reward | $100 |

---

## 2-Step Pro — complete card (every size)

Wide-room 2-step. FTMO’s 10/5 · 5/10, same at every size.

### Phase 1

| # | Rule | Setting |
|---|---|---|
| 1 | Profit target | **10%** |
| 2 | Daily drawdown | **5%** of initial, SOD. Breach = fail |
| 3 | Max drawdown | **10% static** from initial |
| 4 | Minimum trading days | **5** |
| 5 | Consistency | None |
| 6 | Time / inactivity | Unlimited / 30 days |

### Phase 2

| # | Rule | Setting |
|---|---|---|
| 7 | Profit target | **5%** |
| 8 | Daily / max / min days | **Same as Phase 1** (5% / 10% static / 5 days) |

### Funded

| # | Rule | Setting |
|---|---|---|
| 9 | Profit target | None |
| 10 | Daily drawdown | **5%** SOD |
| 11 | Max drawdown | **10% static** |
| 12 | Consistency | None |
| 13 | Min days before first reward | **3** |
| 14 | Fee refund | **100% on first successful reward** |
| 15 | Split | 80% |
| 16 | Min reward | $100 |

---

## Side-by-side (the four cards)

| | Instant | 1-Step | Lite | Pro |
|---|---|---|---|---|
| Phases | 0 (funded day 1) | 1 | 2 | 2 |
| Target | — | 10% | 8% then 5% | 10% then 5% |
| Daily | 3% from day’s high | 4% SOD | 4% SOD | 5% SOD |
| Max DD | 6% trail, **never locks** | 6% hybrid | 8% static | 10% static |
| Consistency | 20% best day | 50% on eval only | None | None |
| Min days | 5 valid (0.5%) | 0 eval / 3 funded | 5 + 5 / 3 funded | 5 + 5 / 3 funded |
| Max risk / trade | — | — | — | — |
| First reward cap | — ($100 min only) | — | — | — |
| Fee refund | No | Yes, first reward | Yes, first reward | Yes, first reward |
| Split | 80% | 80% | 80% | 80% |

---

## Price card (VERO35, same rules at every size)

Shopper pays **sale**. List = sale / 0.65.

| Plan | $5k | $10k | $25k | $50k | $100k | $200k |
|---|---:|---:|---:|---:|---:|---:|
| Instant | $72 | $129 | $299 | $499 | $649 | $999 |
| 1-Step | $49 | $79 | $149 | $249 | $449 | $799 |
| Lite | $27 | $45 | $99 | $179 | $349 | $549 |
| Pro | $36 | $59 | $129 | $229 | $449 | $799 |

Instant prices above are a **raise on $25k+** only. Instant rules stay live (6% trail never locks, no 2% risk cap, no first-reward % cap), so large Instant still has a high E[payout]. Do not cut Instant sale below today’s VERO35; $50k+ stays a hole unless you raise the fee.

Evals already print at today’s VERO35. The eval sale column is a raise toward Hola / FundingPips, still under FTMO. The only **rule** change vs live FAQ is Lite funded max DD 10% → 8%.

---

## What not to put on the card

- Different daily or max DD on $100k vs $5k
- Consistency only on Instant $50k+ (Blue Guardian does this — do not copy)
- A 3-step
- 90% split as the default
- Instant fee refund
- News-trading bans as a margin tool
