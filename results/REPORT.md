# Verodus challenge Monte Carlo

Book: 3.5% Disciplined / 14.5% Average / 60% Aggressive / 22% Scalper. 4,000 paths per profile (16,000 per product). Seed 42. Simulated on a $100k account; payouts scale linearly to each SKU.

Rules and sale prices from [verodus.com/faq-plans.html](https://www.verodus.com/faq-plans.html) and live [`index-eval.js`](https://www.verodus.com/index-eval.js) (16 Aug 2026). Instant refund = No on the live eval table; 1-Step / Lite / Pro refund 100% of the fee on the first successful reward.

## Industry pass / fail research

Credible published numbers (not the viral “90% fail” line, which FTMO does not disclose):

| Source | Finding |
|---|---|
| Track360, Jul 2026 | Blended pass 12.3% across tracked programs; range 5–14%. ~7% of all buyers ever paid. ~45% of funded accounts get a first payout. 60–70% of fails are daily or max drawdown. 30–40% of fails repurchase within 90 days. |
| FPFX Technologies / Finance Magnates (300k+ accounts, ~10 firms) | ~14% pass an evaluation; ~45% of funded get a payout → ~7% of buyers ever paid. Average payout ~4% of notional. |
| FundedNext transparency (2023) | Phase 1 ~25–35%; Phase 2 of those ~43%; combined ~10–11%. Daily DD 38–42% of fails, max DD 24–28%, time 18–22%, forbidden 6–10%, abandon 4–8%. 32–38% of funded breach in 30 days; 58–64% in 90 days. |
| FTMO (archived 2023 stats, TradeLens / Arxum summaries) | Stage 1 ~32–37%, Stage 2 of those ~50–60%, combined ~10%. Pass rate falls with size ($10k 12–14% → $200k 7–9%). |
| Topstep 2025 disclosure | 16.8% of Combines completed. |
| The5%ers-style instant | Sustained funding 4–6% — Instant products pay less often than two-step evals. |

Why traders fail, in order: **daily drawdown** (oversizing, floating loss at reset, revenge size), **max drawdown** (no stand-down as the floor trails or the static hole fills), **time / inactivity**, then news / weekend / copy-trading filters. Passing is mostly risk-budget math (≤1% per trade, 0.5–1% good days, skip bad sessions), not a higher win rate.

This book is *stricter* than that funnel: blended P(pay) lands at 1.9–2.8% versus the industry ~7% ever-paid. Almost all payouts come from the 3.5% Disciplined cohort. Average Retail almost never collects; Aggressive and Scalper die on daily DD in 1–4 days. That is conservative for pricing (you will not underprice Lite/Pro the way the older 84/13.5/2.5 book did).

## Blended pass / payout rates

| Product | Phase 1 | Funded | P(pay) | Survives yr 1 | E[payout] on $100k | Avg days |
|---|---:|---:|---:|---:|---:|---:|
| Verodus Instant | 2.80% | 2.80% | 2.80% | 0.89% | $122 | 4 |
| Verodus 1-Step | 2.48% | 1.93% | 1.93% | 0.63% | $27 | 11 |
| Verodus 2-Step Lite | 3.69% | 2.40% | 2.40% | 0.76% | $31 | 7 |
| Verodus 2-Step Pro | 3.68% | 2.64% | 2.64% | 0.83% | $33 | 9 |

Industry anchors: Track360 blended pass 12.3% (range 5–14%); ~7% of buyers ever paid; ~45% of funded accounts receive a first payout. Daily DD 38–42% of fails, max DD 24–28%.

## SKU pricing vs break-even

E[payout] is the expected first performance reward (80% split, $100 minimum). E[cost] at sale = E[payout] + P(pay)×sale when the fee is refunded. Break-even fee solves `fee = E[payout] + P(pay)×fee` on refunding plans, and `fee = E[payout]` on Instant. 20 / 40 / 60 are sale prices that leave that margin after expected cost.

| Plan | Size | List | Sale | P(pay) | E[payout] | E[cost] | BE | 20% | 40% | 60% | Sale m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Instant | $5,000 | $110 | $72 | 2.80% | $6 | $6 | $6 | $8 | $10 | $15 | +92% |
| Instant | $10,000 | $184 | $121 | 2.80% | $12 | $12 | $12 | $15 | $20 | $31 | +90% |
| Instant | $25,000 | $370 | $242 | 2.80% | $31 | $31 | $31 | $38 | $51 | $76 | +87% |
| Instant | $50,000 | $594 | $389 | 2.80% | $61 | $61 | $61 | $76 | $102 | $153 | +84% |
| Instant | $100,000 | $1,032 | $676 | 2.80% | $122 | $122 | $122 | $153 | $204 | $305 | +82% |
| Instant | $200,000 | $2,012 | $1,318 | 2.80% | $244 | $244 | $244 | $305 | $407 | $611 | +81% |
| 1-Step | $5,000 | $55 | $36 | 1.93% | $1 | $2 | $1 | $2 | $2 | $3 | +94% |
| 1-Step | $10,000 | $92 | $60 | 1.93% | $3 | $4 | $3 | $3 | $5 | $7 | +94% |
| 1-Step | $25,000 | $185 | $120 | 1.93% | $7 | $9 | $7 | $8 | $11 | $17 | +93% |
| 1-Step | $50,000 | $297 | $193 | 1.93% | $13 | $17 | $14 | $17 | $23 | $34 | +91% |
| 1-Step | $100,000 | $516 | $335 | 1.93% | $27 | $33 | $27 | $34 | $45 | $68 | +90% |
| 1-Step | $200,000 | $1,006 | $654 | 1.93% | $53 | $66 | $54 | $68 | $90 | $135 | +90% |
| 2-Step Lite | $5,000 | $27 | $18 | 2.40% | $2 | $2 | $2 | $2 | $3 | $4 | +89% |
| 2-Step Lite | $10,000 | $51 | $33 | 2.40% | $3 | $4 | $3 | $4 | $5 | $8 | +88% |
| 2-Step Lite | $25,000 | $101 | $66 | 2.40% | $8 | $9 | $8 | $10 | $13 | $20 | +86% |
| 2-Step Lite | $50,000 | $204 | $133 | 2.40% | $16 | $19 | $16 | $20 | $27 | $40 | +86% |
| 2-Step Lite | $100,000 | $371 | $241 | 2.40% | $31 | $37 | $32 | $40 | $53 | $80 | +85% |
| 2-Step Lite | $200,000 | $734 | $477 | 2.40% | $62 | $74 | $64 | $80 | $106 | $160 | +85% |
| 2-Step Pro | $5,000 | $31 | $20 | 2.64% | $2 | $2 | $2 | $2 | $3 | $4 | +89% |
| 2-Step Pro | $10,000 | $56 | $36 | 2.64% | $3 | $4 | $3 | $4 | $6 | $8 | +88% |
| 2-Step Pro | $25,000 | $131 | $85 | 2.64% | $8 | $10 | $8 | $10 | $14 | $21 | +88% |
| 2-Step Pro | $50,000 | $250 | $163 | 2.64% | $16 | $21 | $17 | $21 | $28 | $42 | +87% |
| 2-Step Pro | $100,000 | $455 | $296 | 2.64% | $33 | $40 | $33 | $42 | $56 | $84 | +86% |
| 2-Step Pro | $200,000 | $887 | $577 | 2.64% | $65 | $80 | $67 | $84 | $111 | $167 | +86% |

## Failure reasons (population-weighted share of all paths)

| Product | Reason | Share of paths |
|---|---|---:|
| Verodus Instant | `daily_dd` | 88.38% |
| Verodus Instant | `max_dd` | 8.27% |
| Verodus Instant | `post_funding_m1` | 1.18% |
| Verodus Instant | `post_funding_m3` | 0.44% |
| Verodus Instant | `time_abandon` | 0.37% |
| Verodus Instant | `post_funding_m12` | 0.29% |
| Verodus Instant | `rule_violation` | 0.19% |
| Verodus 1-Step | `max_dd` | 63.64% |
| Verodus 1-Step | `daily_dd` | 31.51% |
| Verodus 1-Step | `time_abandon` | 1.90% |
| Verodus 1-Step | `post_funding_m1` | 0.78% |
| Verodus 1-Step | `rule_violation` | 0.47% |
| Verodus 1-Step | `post_funding_m3` | 0.32% |
| Verodus 1-Step | `funded_max_dd` | 0.31% |
| Verodus 1-Step | `post_funding_m12` | 0.19% |
| Verodus 2-Step Lite | `daily_dd` | 83.51% |
| Verodus 2-Step Lite | `max_dd` | 12.10% |
| Verodus 2-Step Lite | `post_funding_m1` | 1.00% |
| Verodus 2-Step Lite | `p2_daily_dd` | 0.62% |
| Verodus 2-Step Lite | `time_abandon` | 0.54% |
| Verodus 2-Step Lite | `p2_max_dd` | 0.42% |
| Verodus 2-Step Lite | `post_funding_m3` | 0.38% |
| Verodus 2-Step Lite | `post_funding_m12` | 0.27% |
| Verodus 2-Step Pro | `daily_dd` | 82.73% |
| Verodus 2-Step Pro | `max_dd` | 12.60% |
| Verodus 2-Step Pro | `post_funding_m1` | 1.09% |
| Verodus 2-Step Pro | `time_abandon` | 0.71% |
| Verodus 2-Step Pro | `post_funding_m3` | 0.43% |
| Verodus 2-Step Pro | `p2_max_dd` | 0.42% |
| Verodus 2-Step Pro | `p2_daily_dd` | 0.42% |
| Verodus 2-Step Pro | `post_funding_m12` | 0.29% |

## Profile detail

| Product | Profile | Phase 1 | P(pay) | E[payout] $100k | Avg days |
|---|---|---:|---:|---:|---:|
| Verodus Instant | Disciplined / Pro | 79.95% | 79.95% | $3,490 | 43 |
| Verodus Instant | Average Retail | 0.00% | 0.00% | $0 | 7 |
| Verodus Instant | Aggressive / Over-leveraged | 0.00% | 0.00% | $0 | 1 |
| Verodus Instant | Scalper / High-frequency | 0.00% | 0.00% | $0 | 4 |
| Verodus 1-Step | Disciplined / Pro | 55.50% | 52.30% | $673 | 79 |
| Verodus 1-Step | Average Retail | 2.85% | 0.62% | $19 | 21 |
| Verodus 1-Step | Aggressive / Over-leveraged | 0.10% | 0.00% | $0 | 3 |
| Verodus 1-Step | Scalper / High-frequency | 0.27% | 0.03% | $1 | 17 |
| Verodus 2-Step Lite | Disciplined / Pro | 82.03% | 68.17% | $877 | 89 |
| Verodus 2-Step Lite | Average Retail | 5.03% | 0.12% | $3 | 10 |
| Verodus 2-Step Lite | Aggressive / Over-leveraged | 0.00% | 0.00% | $0 | 1 |
| Verodus 2-Step Lite | Scalper / High-frequency | 0.40% | 0.00% | $0 | 7 |
| Verodus 2-Step Pro | Disciplined / Pro | 85.90% | 75.00% | $910 | 95 |
| Verodus 2-Step Pro | Average Retail | 4.15% | 0.10% | $5 | 14 |
| Verodus 2-Step Pro | Aggressive / Over-leveraged | 0.00% | 0.00% | $0 | 2 |
| Verodus 2-Step Pro | Scalper / High-frequency | 0.33% | 0.00% | $0 | 10 |

## Industry-weighted sensitivity (12% pro)

Same path library, reweighted to 12% Disciplined / 18% Average / 50% Aggressive / 20% Scalper so blended P(pay) sits nearer the published ~7% ever-paid rate. Use this if the 3.5% pro prior is too harsh.

| Product | Phase 1 | Funded | P(pay) | E[payout] $100k |
|---|---:|---:|---:|---:|
| Verodus 1-Step | 7.28% | 6.39% | 6.39% | $84 |
| Verodus 2-Step Lite | 10.83% | 8.20% | 8.20% | $106 |
| Verodus 2-Step Pro | 11.12% | 9.02% | 9.02% | $110 |
| Verodus Instant | 9.59% | 9.59% | 9.59% | $419 |

| Plan | Size | Sale | P(pay) | E[payout] | BE | 40% | Sale m |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1-Step | $5,000 | $36 | 6.39% | $4 | $5 | $8 | +82% |
| 1-Step | $10,000 | $60 | 6.39% | $8 | $9 | $15 | +80% |
| 1-Step | $25,000 | $120 | 6.39% | $21 | $23 | $38 | +76% |
| 1-Step | $50,000 | $193 | 6.39% | $42 | $45 | $75 | +72% |
| 1-Step | $100,000 | $335 | 6.39% | $84 | $90 | $150 | +68% |
| 1-Step | $200,000 | $654 | 6.39% | $169 | $180 | $300 | +68% |
| 2-Step Lite | $5,000 | $18 | 8.20% | $5 | $6 | $10 | +62% |
| 2-Step Lite | $10,000 | $33 | 8.20% | $11 | $12 | $19 | +60% |
| 2-Step Lite | $25,000 | $66 | 8.20% | $26 | $29 | $48 | +52% |
| 2-Step Lite | $50,000 | $133 | 8.20% | $53 | $58 | $96 | +52% |
| 2-Step Lite | $100,000 | $241 | 8.20% | $106 | $115 | $192 | +48% |
| 2-Step Lite | $200,000 | $477 | 8.20% | $212 | $231 | $384 | +47% |
| 2-Step Pro | $5,000 | $20 | 9.02% | $6 | $6 | $10 | +63% |
| 2-Step Pro | $10,000 | $36 | 9.02% | $11 | $12 | $20 | +60% |
| 2-Step Pro | $25,000 | $85 | 9.02% | $28 | $30 | $50 | +59% |
| 2-Step Pro | $50,000 | $163 | 9.02% | $55 | $61 | $101 | +57% |
| 2-Step Pro | $100,000 | $296 | 9.02% | $110 | $121 | $202 | +54% |
| 2-Step Pro | $200,000 | $577 | 9.02% | $220 | $242 | $403 | +53% |
| Instant | $5,000 | $72 | 9.59% | $21 | $21 | $35 | +71% |
| Instant | $10,000 | $121 | 9.59% | $42 | $42 | $70 | +65% |
| Instant | $25,000 | $242 | 9.59% | $105 | $105 | $175 | +57% |
| Instant | $50,000 | $389 | 9.59% | $209 | $209 | $349 | +46% |
| Instant | $100,000 | $676 | 9.59% | $419 | $419 | $698 | +38% |
| Instant | $200,000 | $1,318 | 9.59% | $838 | $838 | $1,396 | +36% |

## Read vs the 15 Aug peer PDFs

Those reports used an 84 / 13.5 / 2.5 book and called Lite/Pro a hole (sale m −32% / −46% at $5k). In *this* Realistic Version the 13.5% “can actually collect” bucket is gone: Average Retail’s Lite P(pay) is 0.12%. VERO35 therefore prints on every SKU. If a fatter skilled tail shows up in live CRM, switch to the 12% pro table above — Instant $5k is still +~70%, Lite $5k still +~70%. The hole only returns if Average Retail starts collecting at a few percent with four-figure first payouts.

First-payout E[X] understates cost for the ~0.8% who survive a year. Two extra cycles on year-1 survivors add roughly 0.6× E[payout] on Instant and less on evals. Instant $5k would still be high-80s margin.

## What is not modeled

- News-window clawback / second-violation hard breach (plans default `newsTradingAllowed=false`).
- Friday flatten without the weekend-holding add-on.
- KYC drop between pass and funded.
- Split scaling to 85/90 and add-on weekly/on-demand cycles.
- Payouts after the first (year-1 survival is a separate overlay, not extra dollars).
- Copy-trading / HFT / pass-your-challenge filters.

