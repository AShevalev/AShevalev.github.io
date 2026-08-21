# Instant leftover — live engine PDF vs catalog

PDF `evaluateOneStepConsistencyRule` is **correct** for Instant Best Day:

- Every profitable day (including small profitable days) is in Positive Days’ Profit and can be Best Day.
- Red days and flats are ignored. Open trades ignored.
- Instant pass iff Best Day ≤ 20% of Positive Days’ Profit. Not a breach.
- Same function at 50% for 1-Step evaluation. Instant itself is 20%, not 50%.
- The +$0.01 epsilon is rounding, not a chip exploit.
- Worked examples in the PDF all check out (`Positive ≥ Best / 0.20` for Instant).

The PDF also says the retired Instant **+0.5% valid-day counter is dead** and was never wired into consistency. Our leftover catalog still gates Instant payouts on **5 days at at least 0.5% of SOD** plus 20% Best Day. That extra gate is **not** in the live function.

News on. 1,200 paths per profile. Instant seed matches `run_rule_alignment`. Prices were not raised.

| Engine | Size | Sale | P(pay) | BE | Leftover | Sale m |
|---|---:|---:|---:|---:|---:|---:|
| catalog (5 days >0.5% SOD + 20% all profitable days) | $5,000 | $49 | 21.3% | $13.9 | $6.6 | +72% |
| catalog | $10,000 | $69 | 21.3% | $27.8 | $6.9 | +60% |
| catalog | $25,000 | $149 | 21.3% | $69.5 | $23.7 | +53% |
| catalog | $50,000 | $239 | 21.3% | $139.0 | $17.2 | +42% |
| catalog | $100,000 | $439 | 21.3% | $278.0 | $20.0 | +37% |
| PDF engine (no valid-day gate, 20% all profitable days) | $5,000 | $49 | 21.4% | $13.7 | $6.8 | +72% |
| PDF engine | $10,000 | $69 | 21.4% | $27.4 | $7.4 | +60% |
| PDF engine | $25,000 | $149 | 21.4% | $68.4 | $25.0 | +54% |
| PDF engine | $50,000 | $239 | 21.4% | $136.8 | $19.6 | +43% |
| PDF engine | $100,000 | $439 | 21.4% | $273.6 | $24.8 | +38% |

## Instant family (98 accounts)

- **Catalog two-box:** leftover **$1,486** (9.2% of $16,202 sale)
- **PDF engine:** leftover **$1,636** (10.1% of $16,202 sale)

Killing the 0.5% valid-day gate **raises** Instant leftover (Instant $100k **+$20 → +$25**). P(pay) is almost flat (21.3% → 21.4%). Year-1 E[X] is a little lower because a few more paths print a small first reward without five 0.5% days. Rec prices stay.

1-Step and 2-Step were not changed. Adding ~$150 Instant family leftover to the current 310 book would put the book near **$9,811/mo** instead of $9,661.

## Copy implication

Do not write that only days above 0.5% count toward Positive Days’ Profit. The live function never did that. The 0.5% “meets the parameter” line is also **not** in this engine. Instant copy is: every profitable day, 20% Best Day, no listed min trading days.
