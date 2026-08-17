# Verodus 310-account book — 17 Aug 2026

Same mix already in `write_price_rec_pdf.UNITS`. Instant-heavy, mid-size modal, few $200k. CAD 10,000/mo wages (~$7,200) are a **fixed** cost, not a per-SKU hurdle. News is included. Default reward is Bi-Weekly 80%, min $100. 8(h) is off.

Mix: Instant 98 · 1-Step 67 · Lite 82 · Pro 63 · **310**.

## Book P&L (challenge only, VERO35 sale)

| Line | $/mo |
|---|---:|
| Challenge revenue | $54,270 |
| Ads 20% | −$10,854 |
| Payout BE (Instant year-1 / eval first-payout + refund) | −$24,744 |
| 10% assumption error on BE | −$2,474 |
| $1 per account | −$310 |
| Wages CAD 10,000 × 0.72 | −$7,200 |
| **Leftover after opex** | **$8,687** |

Leftover is **16.0%** of challenge revenue. Contribution before wages is $15,887 (29.3%). Payout-only sale margin (ignores ads/wages/$1/error) is 50.0% — do not run the desk on that number.

## Family roll-up at 310

| Plan | N | Revenue | Leftover | of revenue |
|---|---:|---:|---:|---:|
| Instant | 98 | $16,202 | $512 | 3.2% |
| 1-Step | 67 | $12,601 | $3,172 | 25.2% |
| 2-Step Lite | 82 | $12,718 | $2,138 | 16.8% |
| 2-Step Pro | 63 | $12,749 | $2,866 | 22.5% |
| **Book** | **310** | **$54,270** | **$8,687** | **16.0%** |

## Same mix at 150 / 310 / 600

Wages stay $7,200. Per-account wage falls as volume rises.

| Accounts | Revenue | Leftover | of revenue |
|---:|---:|---:|---:|
| 150 | $26,260 | $487 | 1.9% |
| 310 ← this book | $54,270 | $8,687 | 16.0% |
| 600 | $105,039 | $23,550 | 22.4% |

## Per SKU at 310

Leftover = sale × 0.80 − (BE × 1.10 + $1 + wage share). Sale m is payout-only (sale − E[cost]) / sale.

| Plan | Size | N | Sale | List | BE | Opex floor | Sale m | Left / unit | Book left |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Instant | $5,000 | 15 | $49 | $75 | $15 | $43 | 68.7% | $5 | $76 |
| Instant | $10,000 | 25 | $69 | $106 | $31 | $64 | 55.6% | $4 | $94 |
| Instant | $25,000 | 28 | $149 | $229 | $77 | $129 | 48.6% | $16 | $447 |
| Instant | $50,000 | 18 | $239 | $368 | $153 | $237 | 35.9% | $2 | $29 |
| Instant | $100,000 | 12 | $439 | $675 | $306 | $453 | 30.2% | −$11 | −$134 |
| 1-Step | $5,000 | 8 | $45 | $69 | $8 | $37 | 75.1% | $7 | $54 |
| 1-Step | $10,000 | 14 | $69 | $106 | $16 | $48 | 70.0% | $16 | $230 |
| 1-Step | $25,000 | 18 | $129 | $198 | $41 | $84 | 62.6% | $36 | $645 |
| 1-Step | $50,000 | 14 | $219 | $337 | $82 | $144 | 57.4% | $60 | $842 |
| 1-Step | $100,000 | 10 | $379 | $583 | $164 | $263 | 52.0% | $93 | $927 |
| 1-Step | $200,000 | 3 | $699 | $1,075 | $329 | $502 | 48.7% | $158 | $474 |
| 2-Step Lite | $5,000 | 10 | $39 | $60 | $7 | $39 | 72.4% | $0 | $1 |
| 2-Step Lite | $10,000 | 18 | $55 | $85 | $15 | $50 | 65.4% | $4 | $76 |
| 2-Step Lite | $25,000 | 22 | $115 | $177 | $37 | $82 | 60.7% | $26 | $578 |
| 2-Step Lite | $50,000 | 16 | $169 | $260 | $73 | $136 | 50.5% | $26 | $420 |
| 2-Step Lite | $100,000 | 12 | $309 | $475 | $147 | $244 | 46.8% | $52 | $621 |
| 2-Step Lite | $200,000 | 4 | $599 | $922 | $293 | $461 | 45.5% | $111 | $443 |
| 2-Step Pro | $5,000 | 6 | $45 | $69 | $8 | $38 | 72.2% | $5 | $32 |
| 2-Step Pro | $10,000 | 12 | $59 | $91 | $16 | $50 | 64.2% | $7 | $87 |
| 2-Step Pro | $25,000 | 16 | $125 | $192 | $39 | $84 | 60.0% | $32 | $520 |
| 2-Step Pro | $50,000 | 14 | $199 | $306 | $79 | $142 | 53.0% | $46 | $640 |
| 2-Step Pro | $100,000 | 10 | $349 | $537 | $157 | $257 | 48.1% | $74 | $738 |
| 2-Step Pro | $200,000 | 5 | $699 | $1,075 | $314 | $487 | 48.2% | $170 | $849 |
| **Book** | — | **310** | — | — | $24,744 | — | 50.0% | — | **$8,687** |

Does not print (leftover < −$1): Instant $100,000 −$11.
Thin (under $2 leftover): Instant $50,000 $2, 2-Step Lite $5,000 $0. Leave the street doors; the book still prints.

## Add-ons on the 310 mix (attach-weighted)

News attach is 0 (included). Weekend / Weekly / On Demand attach is the early-book mix (Instant 10% / 8% / 18%, 1-Step 16% / 10% / 12%, Lite 12% / 7% / 8%, Pro 20% / 12% / 16%). Not a sales forecast.

| Card | Weekend | Weekly 70% | On Demand 90% | Extra leftover | Extra net $ |
|---|---:|---:|---:|---:|---:|
| Rec 12% / 8% / 15–32% | $565 | $182 | $363 | **$1,110** | $2,939 |
| Checkout 15% / 6% / 20% | $753 | $105 | $263 | **$1,121** | $2,953 |

Challenge leftover $8,687 plus rec add-on leftover $1,110 = **$9,798**/mo blended. Checkout 15/6/20 blended **$9,809**/mo. Instant $100k On Demand at checkout 20% still does not print on that SKU; attach-weighted book leftover can stay positive because smaller Instant doors do.

PDF: `results/Verodus_Book_310_2026-08-17.pdf`
