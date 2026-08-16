# Verodus complete operator report — 16 August 2026

One document. Instant priced on year-1. Evals on first-payout + refund.

## 1. Is P(pay) correct?

| Plan | P(pay) | Year-1 | Price on | Verdict |
|---|---:|---:|---|---|
| Instant | 22.1% | 7.2% | No — use year-1 7.16% | Correct as first-pay; do not price on it |
| 1-Step | 8.8% | 2.9% | Yes — first-payout + refund | Correct. Harder than FTMO 1-Step 13.5% |
| 2-Step Lite | 10.6% | 3.4% | Yes — first-payout + refund | Correct. Near FTMO 12.7% / FN Lite 12.0% |
| 2-Step Pro | 12.0% | 4.2% | Yes — first-payout + refund | Correct. FTMO 2-step twin is 12.7% |

## Margin % by size and family

| Family | Size | Rec $ | BE $ | E[cost] | Rec m | Live $ | Live m |
|---|---:|---:|---:|---:|---:|---:|---:|
| Instant | $5,000 | $59 | $14 | $14 | +76% | $72 | +80% |
| Instant | $10,000 | $69 | $28 | $28 | +59% | $121 | +77% |
| Instant | $25,000 | $99 | $71 | $71 | +28% | $242 | +71% |
| Instant | $50,000 | $189 | $142 | $142 | +25% | $389 | +63% |
| Instant | $100,000 | $359 | $284 | $284 | +21% | $676 | +58% |
| 1-Step | $5,000 | $36 | $6 | $9 | +76% | $36 | +76% |
| 1-Step | $10,000 | $60 | $12 | $16 | +73% | $60 | +73% |
| 1-Step | $25,000 | $120 | $30 | $38 | +69% | $120 | +69% |
| 1-Step | $50,000 | $193 | $59 | $71 | +63% | $193 | +63% |
| 1-Step | $100,000 | $335 | $119 | $138 | +59% | $335 | +59% |
| 1-Step | $200,000 | $654 | $237 | $274 | +58% | $654 | +58% |
| 2-Step Lite | $5,000 | $18 | $8 | $9 | +52% | $18 | +52% |
| 2-Step Lite | $10,000 | $33 | $15 | $17 | +48% | $33 | +48% |
| 2-Step Lite | $25,000 | $66 | $38 | $41 | +38% | $66 | +38% |
| 2-Step Lite | $50,000 | $133 | $76 | $82 | +38% | $133 | +38% |
| 2-Step Lite | $100,000 | $241 | $152 | $162 | +33% | $241 | +33% |
| 2-Step Lite | $200,000 | $477 | $304 | $323 | +32% | $477 | +32% |
| 2-Step Pro | $5,000 | $20 | $8 | $9 | +55% | $20 | +55% |
| 2-Step Pro | $10,000 | $36 | $15 | $18 | +51% | $36 | +51% |
| 2-Step Pro | $25,000 | $85 | $38 | $43 | +49% | $85 | +49% |
| 2-Step Pro | $50,000 | $163 | $75 | $86 | +47% | $163 | +47% |
| 2-Step Pro | $100,000 | $296 | $151 | $168 | +43% | $296 | +43% |
| 2-Step Pro | $200,000 | $577 | $301 | $334 | +42% | $577 | +42% |

## Family roll-up at $100k

| Family | P(pay) | Year-1 | BE | Rec | Rec m | Live | Live m |
|---|---:|---:|---:|---:|---:|---:|---:|
| Instant | 22.1% | 7.2% | $284 | $359 | +21% | $676 | +58% |
| 1-Step | 8.8% | 2.9% | $119 | $335 | +59% | $335 | +59% |
| 2-Step Lite | 10.6% | 3.4% | $152 | $241 | +33% | $241 | +33% |
| 2-Step Pro | 12.0% | 4.2% | $151 | $296 | +43% | $296 | +43% |

PDF: `results/Verodus_Complete_Report_2026-08-16.pdf`

