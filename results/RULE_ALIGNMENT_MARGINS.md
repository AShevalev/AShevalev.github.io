# Rule-alignment Monte Carlo — leftover vs prior day rules

**Margins did not increase on any account.** Instant leftover is down on every size. 1-Step leftover is down on every size. 2-Step Lite and Pro are unchanged (same paths). Instant $100k leftover at the current $439 sale is now **−$10** and no longer prints after opex. Prices were not raised.

News included. 1200 paths per profile, same 7/22/26/28/17 mix, paired per-product seeds. Sale card is unchanged (current rec).

Prior Instant: two checkboxes — 5 days at ≥0.5% of start-of-day equity **and** 20% Best Day on every green day. Aligned Instant: one rule — 20% Best Day, and a day counts only if it closes **more than 0.5% of EOD account balance**. The 20% cap still forces at least five counted days (`1 ÷ n` of PDP). The 5 is implied, not a second checkbox.

Prior 1-Step QPP: 3 min days, no Best Day. Aligned 1-Step QPP: no min days, 50% Best Day (no 0.5% floor). 2-Step Lite/Pro unchanged (5 eval / 3 QPP).

Leftover = sale × 0.80 − (BE × 1.10 + $1 + wage share). Sale m is the ads-line margin (Instant year-1 E[X]; evals include fee refund).

| Plan | Size | Sale | P(pay) old → new | BE old → new | Leftover old → new | Sale m old → new | Leftover up? |
|---|---:|---:|---|---|---|---|:---:|
| Instant | $5,000 | $49 | 21.3% → 19.3% | $13.9 → $15.3 | $6.6 → $5.1 (-1.5) | +72% → +69% | no |
| Instant | $10,000 | $69 | 21.3% → 19.3% | $27.8 → $30.5 | $6.9 → $3.9 (-3.0) | +60% → +56% | no |
| Instant | $25,000 | $149 | 21.3% → 19.3% | $69.5 → $76.3 | $23.7 → $16.2 (-7.5) | +53% → +49% | no |
| Instant | $50,000 | $239 | 21.3% → 19.3% | $139.0 → $152.6 | $17.2 → $2.2 (-15.0) | +42% → +36% | no |
| Instant | $100,000 | $439 | 21.3% → 19.3% | $278.0 → $305.2 | $20.0 → $-10.0 (-30.0) | +37% → +30% | no |
| 1-Step | $5,000 | $45 | 9.1% → 8.2% | $6.5 → $8.2 | $8.7 → $6.8 (-1.9) | +78% → +75% | no |
| 1-Step | $10,000 | $69 | 9.1% → 8.2% | $13.0 → $16.4 | $20.3 → $16.4 (-3.8) | +74% → +70% | no |
| 1-Step | $25,000 | $129 | 9.1% → 8.2% | $32.4 → $41.1 | $45.4 → $35.8 (-9.6) | +68% → +63% | no |
| 1-Step | $50,000 | $219 | 9.1% → 8.2% | $64.8 → $82.2 | $79.3 → $60.1 (-19.1) | +64% → +57% | no |
| 1-Step | $100,000 | $379 | 9.1% → 8.2% | $129.5 → $164.3 | $131.0 → $92.7 (-38.3) | +60% → +52% | no |
| 1-Step | $200,000 | $699 | 9.1% → 8.2% | $259.0 → $328.6 | $234.5 → $157.9 (-76.6) | +57% → +49% | no |
| 2-Step Lite | $5,000 | $39 | 10.8% → 10.8% | $7.3 → $7.3 | $0.1 → $0.1 (+0.0) | +72% → +72% | flat |
| 2-Step Lite | $10,000 | $55 | 10.8% → 10.8% | $14.7 → $14.7 | $4.2 → $4.2 (+0.0) | +65% → +65% | flat |
| 2-Step Lite | $25,000 | $115 | 10.8% → 10.8% | $36.7 → $36.7 | $26.3 → $26.3 (+0.0) | +61% → +61% | flat |
| 2-Step Lite | $50,000 | $169 | 10.8% → 10.8% | $73.4 → $73.4 | $26.2 → $26.2 (+0.0) | +50% → +50% | flat |
| 2-Step Lite | $100,000 | $309 | 10.8% → 10.8% | $146.7 → $146.7 | $51.7 → $51.7 (+0.0) | +47% → +47% | flat |
| 2-Step Lite | $200,000 | $599 | 10.8% → 10.8% | $293.5 → $293.5 | $110.8 → $110.8 (+0.0) | +45% → +45% | flat |
| 2-Step Pro | $5,000 | $45 | 12.5% → 12.5% | $7.9 → $7.9 | $5.3 → $5.3 (+0.0) | +72% → +72% | flat |
| 2-Step Pro | $10,000 | $59 | 12.5% → 12.5% | $15.7 → $15.7 | $7.3 → $7.3 (+0.0) | +64% → +64% | flat |
| 2-Step Pro | $25,000 | $125 | 12.5% → 12.5% | $39.3 → $39.3 | $32.5 → $32.5 (+0.0) | +60% → +60% | flat |
| 2-Step Pro | $50,000 | $199 | 12.5% → 12.5% | $78.5 → $78.5 | $45.7 → $45.7 (+0.0) | +53% → +53% | flat |
| 2-Step Pro | $100,000 | $349 | 12.5% → 12.5% | $157.1 → $157.1 | $73.8 → $73.8 (+0.0) | +48% → +48% | flat |
| 2-Step Pro | $200,000 | $699 | 12.5% → 12.5% | $314.2 → $314.2 | $169.9 → $169.9 (+0.0) | +48% → +48% | flat |

**0 SKUs leftover up · 11 down · 12 flat** (±$0.05).

2-Step rows are bit-identical — those payout day rules did not change.

## Why Instant and 1-Step leftover fell

- Instant: the payout floor that matters is the same. Four equal counted days = 25% Best Day; five equal counted days = 20%. You still cannot get paid with fewer than five days that closed more than 0.5% of account balance. Leftover fell on the **small differences**, not from dropping a 5-day min: tiny greens (+0.1%, +0.4%) no longer sit in Positive Days’ Profit (old Best Day used every green day, which made 20% easier); exactly 0.5% no longer counts (old copy was often **at least** 0.5% of SOD). P(pay) fell 21.3% → 19.3%. Paths that still get paid stay longer and pay more (first-payout E[X] $100k $825 → $881), so year-1 BE rose $278 → $305.
- 1-Step: 50% Best Day on Qualified Performance is tighter than “3 any trading days.” P(pay) fell 9.1% → 8.2%. Paid paths keep trading to flatten Best Day, so first-payout E[X] $100k $118 → $151 and BE $130 → $164.
- Sale card was not raised. Instant $100k at $439 is the only challenge SKU that fails the opex stack (leftover −$10). Instant $50k is thin (+$2).

## 310-account book

Challenge leftover **$10,219 (18.8%) → $8,723 (16.1%)** of $54,270. Instant family leftover $1,684 → $548. 1-Step $4,048 → $3,172. Lite and Pro unchanged.

## Instant $100k add-ons (same extra-E[X] fractions)

| Add-on | Sticker | Extra E[X] | Leftover after ads |
|---|---:|---:|---:|
| Weekend 15% | $101 | $24 | +$28 |
| Weekly 70% 6% | $41 | $24 | **−$3** |
| On Demand 90% 32% | $216 | $125 | **−$13** |

Weekly and On Demand on Instant $100k no longer print at the locked percents because challenge BE rose. 1-Step $100k add-ons still print.

