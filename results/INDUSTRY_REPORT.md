# Top-20 prop firms — industry-calibrated Monte Carlo

**Read [`RULES.md`](RULES.md) for the Verodus card, [`PRICES.md`](PRICES.md) for every firm’s charge and margin, [`STRATEGY.md`](STRATEGY.md) for actions.**

Book: **7% Pro / 22% Semi-skilled / 26% Average / 28% Aggressive / 17% Lottery**. Calibrated so a standard 10/5 · 5/10 static 2-step (FTMO) lands near the Track360 / FPFX / FTMO funnel. Same path library for every firm; only rules, split, refund, and prices differ. Instant P(pay) is first-payout eligibility; year-1 is the sustained-Instant figure.

Verodus vs live FAQ: Instant is **unchanged** (6% trail never locks; no 2% max-risk; no first-reward % cap). Lite funded max DD **10% → 8%**. 1-Step and Pro unchanged.

## Blended rates by product

| Firm | Plan | Family | P1 | Funded | P(pay) | E[payout] $100k | Days | Refund | Split |
|---|---|---|---:|---:|---:|---:|---:|---|---:|
| Alpha Capital | One 10% | 1-step | 11.2% | 7.0% | 7.0% | $156 | 41 | none | 80% |
| Blue Guardian | 1-Step Standard | 1-step | 20.5% | 15.1% | 15.1% | $186 | 45 | first | 80% |
| E8 Markets | E8 One 6% | 1-step | 13.5% | 8.0% | 8.0% | $186 | 41 | none | 80% |
| E8 Markets | Signature | 1-step | 12.7% | 6.6% | 6.6% | $152 | 28 | none | 80% |
| FTMO | 1-Step | 1-step | 18.6% | 13.5% | 13.5% | $265 | 45 | none | 90% |
| Fintokei | SwiftTrader | 1-step | 18.2% | 12.5% | 12.5% | $148 | 41 | first | 80% |
| FundedNext | Stellar 1-Step | 1-step | 18.7% | 14.3% | 14.3% | $114 | 42 | fourth | 80% |
| FundingPips | 1-Step Flex | 1-step | 20.8% | 17.1% | 17.1% | $141 | 54 | fourth | 85% |
| Hola Prime | 1-Step Prime | 1-step | 18.5% | 13.2% | 13.2% | $148 | 43 | quarter_x4 | 80% |
| The Funded Trader | Royal 1-Step | 1-step | 19.0% | 12.8% | 12.8% | $158 | 45 | none | 80% |
| The5ers | Hyper Growth | 1-step | 19.9% | 15.2% | 15.2% | $85 | 45 | none | 50% |
| Verodus | 1-Step | 1-step | 12.6% | 8.8% | 8.8% | $108 | 41 | first | 80% |
| Alpha Capital | Pro 6% | 2-step | 23.6% | 9.0% | 9.0% | $107 | 45 | none | 80% |
| Alpha Capital | Pro 10% | 2-step | 21.9% | 11.8% | 11.8% | $127 | 55 | none | 80% |
| Blue Guardian | 2-Step Standard | 2-step | 23.2% | 11.6% | 11.6% | $137 | 53 | first | 80% |
| BrightFunded | 2-Step | 2-step | 23.5% | 12.9% | 12.9% | $142 | 54 | first | 80% |
| City Traders Imperium | 2-Step | 2-step | 21.5% | 11.3% | 11.3% | $127 | 56 | first | 80% |
| FTMO | 2-Step | 2-step | 21.8% | 12.7% | 12.7% | $92 | 56 | first | 80% |
| FXIFY | 2-Step | 2-step | 18.4% | 8.9% | 8.9% | $62 | 51 | first | 80% |
| Fintokei | ProTrader | 2-step | 24.7% | 12.6% | 12.6% | $143 | 53 | first | 80% |
| For Traders | 2-Step | 2-step | 22.3% | 10.4% | 10.4% | $122 | 48 | first | 80% |
| FundedNext | Stellar 2-Step | 2-step | 23.8% | 12.9% | 12.9% | $91 | 51 | first | 80% |
| FundedNext | Stellar Lite | 2-step | 21.7% | 12.0% | 12.0% | $90 | 47 | first | 80% |
| Funding Traders | 2-Step | 2-step | 24.3% | 13.0% | 13.0% | $147 | 52 | first | 80% |
| FundingPips | 2-Step Standard | 2-step | 24.2% | 12.6% | 12.6% | $134 | 52 | fourth | 80% |
| FundingPips | 2-Step Flex | 2-step | 24.6% | 14.3% | 14.3% | $104 | 58 | none | 85% |
| FundingPips | 2-Step Pro | 2-step | 26.2% | 9.9% | 9.9% | $107 | 44 | none | 80% |
| Goat Funded | 2-Step Standard | 2-step | 25.0% | 12.9% | 12.9% | $138 | 54 | first | 80% |
| Hola Prime | 2-Step Prime | 2-step | 22.7% | 12.3% | 12.3% | $138 | 53 | quarter_x4 | 80% |
| Maven | 2-Step | 2-step | 24.6% | 12.7% | 12.7% | $136 | 54 | first | 80% |
| Ment Funding | 2-Step | 2-step | 22.1% | 10.5% | 10.5% | $123 | 48 | first | 80% |
| The Funded Trader | Standard | 2-step | 24.5% | 12.9% | 12.9% | $145 | 53 | first | 80% |
| The5ers | High Stakes | 2-step | 22.1% | 11.2% | 11.2% | $230 | 59 | none | 80% |
| Verodus | 2-Step Lite | 2-step | 22.0% | 10.6% | 10.6% | $136 | 50 | first | 80% |
| Verodus | 2-Step Pro | 2-step | 21.6% | 12.0% | 12.0% | $133 | 56 | first | 80% |
| Maven | 3-Step | 3-step | 25.0% | 5.1% | 5.1% | $64 | 52 | first | 80% |
| The5ers | Bootcamp | 3-step | 25.2% | 4.6% | 4.6% | $24 | 51 | none | 50% |
| Alpha Capital | Instant | instant | 13.0% | 13.0% | 13.0% | $690 | 32 | none | 80% |
| Blue Guardian | Instant | instant | 22.1% | 22.1% | 22.1% | $828 | 25 | none | 80% |
| FXIFY | Instant Lite | instant | 15.7% | 15.7% | 15.7% | $680 | 32 | none | 80% |
| FXIFY | Instant Standard | instant | 54.2% | 54.2% | 54.2% | $716 | 9 | none | 80% |
| FundedNext | Stellar Instant | instant | 53.2% | 53.2% | 53.2% | $635 | 9 | first | 80% |
| FundingPips | Zero | instant | 15.3% | 15.3% | 15.3% | $829 | 32 | none | 80% |
| Goat Funded | Instant GOAT | instant | 16.6% | 16.6% | 16.6% | $846 | 31 | none | 80% |
| Hola Prime | Direct | instant | 23.8% | 23.8% | 23.8% | $920 | 28 | quarter_x4 | 80% |
| Instant Funding | Instant | instant | 21.4% | 21.4% | 21.4% | $841 | 27 | none | 80% |
| Verodus | Instant | instant | 22.1% | 22.1% | 22.1% | $875 | 28 | none | 80% |

## Margins at shopper price (all SKUs)

| Firm | Plan | Size | List | Sale | Off | P(pay) | E[payout] | E[cost] | BE | 40% | Sale m |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Alpha Capital | One 10% | $5,000 | $50 | $40 | 20.0% | 7.0% | $8 | $8 | $8 | $13 | +81% |
| Alpha Capital | One 10% | $10,000 | $97 | $78 | 19.6% | 7.0% | $16 | $16 | $16 | $26 | +80% |
| Alpha Capital | One 10% | $25,000 | $197 | $158 | 19.8% | 7.0% | $39 | $39 | $39 | $65 | +75% |
| Alpha Capital | One 10% | $50,000 | $297 | $238 | 19.9% | 7.0% | $78 | $78 | $78 | $130 | +67% |
| Alpha Capital | One 10% | $100,000 | $497 | $398 | 19.9% | 7.0% | $156 | $156 | $156 | $260 | +61% |
| Alpha Capital | One 10% | $200,000 | $997 | $798 | 20.0% | 7.0% | $312 | $312 | $312 | $519 | +61% |
| Blue Guardian | 1-Step Standard | $5,000 | $59 | $47 | 20.3% | 15.1% | $9 | $16 | $11 | $18 | +65% |
| Blue Guardian | 1-Step Standard | $10,000 | $99 | $79 | 20.2% | 15.1% | $19 | $31 | $22 | $36 | +61% |
| Blue Guardian | 1-Step Standard | $25,000 | $189 | $151 | 20.1% | 15.1% | $46 | $69 | $55 | $91 | +54% |
| Blue Guardian | 1-Step Standard | $50,000 | $299 | $239 | 20.1% | 15.1% | $93 | $129 | $109 | $182 | +46% |
| Blue Guardian | 1-Step Standard | $100,000 | $499 | $399 | 20.0% | 15.1% | $186 | $246 | $219 | $365 | +38% |
| Blue Guardian | 1-Step Standard | $200,000 | $899 | $719 | 20.0% | 15.1% | $372 | $480 | $438 | $730 | +33% |
| E8 Markets | E8 One 6% | $5,000 | $59 | $59 | 0.0% | 8.0% | $9 | $9 | $9 | $16 | +84% |
| E8 Markets | E8 One 6% | $10,000 | $138 | $138 | 0.0% | 8.0% | $19 | $19 | $19 | $31 | +86% |
| E8 Markets | E8 One 6% | $25,000 | $228 | $228 | 0.0% | 8.0% | $47 | $47 | $47 | $78 | +80% |
| E8 Markets | E8 One 6% | $50,000 | $338 | $338 | 0.0% | 8.0% | $93 | $93 | $93 | $155 | +72% |
| E8 Markets | E8 One 6% | $100,000 | $538 | $538 | 0.0% | 8.0% | $186 | $186 | $186 | $311 | +65% |
| E8 Markets | E8 One 6% | $200,000 | $988 | $988 | 0.0% | 8.0% | $373 | $373 | $373 | $621 | +62% |
| E8 Markets | Signature | $25,000 | $198 | $198 | 0.0% | 6.6% | $38 | $38 | $38 | $63 | +81% |
| E8 Markets | Signature | $50,000 | $298 | $298 | 0.0% | 6.6% | $76 | $76 | $76 | $126 | +75% |
| E8 Markets | Signature | $100,000 | $498 | $498 | 0.0% | 6.6% | $152 | $152 | $152 | $253 | +70% |
| FTMO | 1-Step | $10,000 | $92 | $92 | 0.0% | 13.5% | $26 | $26 | $26 | $44 | +71% |
| FTMO | 1-Step | $25,000 | $231 | $231 | 0.0% | 13.5% | $66 | $66 | $66 | $110 | +71% |
| FTMO | 1-Step | $50,000 | $370 | $370 | 0.0% | 13.5% | $132 | $132 | $132 | $221 | +64% |
| FTMO | 1-Step | $100,000 | $579 | $579 | 0.0% | 13.5% | $265 | $265 | $265 | $442 | +54% |
| FTMO | 1-Step | $200,000 | $1,159 | $1,159 | 0.0% | 13.5% | $530 | $530 | $530 | $883 | +54% |
| Fintokei | SwiftTrader | $5,000 | $44 | $35 | 20.5% | 12.5% | $7 | $12 | $8 | $14 | +66% |
| Fintokei | SwiftTrader | $10,000 | $89 | $71 | 20.2% | 12.5% | $15 | $24 | $17 | $28 | +67% |
| Fintokei | SwiftTrader | $25,000 | $179 | $143 | 20.1% | 12.5% | $37 | $55 | $42 | $71 | +62% |
| Fintokei | SwiftTrader | $50,000 | $289 | $231 | 20.1% | 12.5% | $74 | $103 | $85 | $141 | +55% |
| Fintokei | SwiftTrader | $100,000 | $499 | $399 | 20.0% | 12.5% | $148 | $198 | $169 | $282 | +50% |
| FundedNext | Stellar 1-Step | $6,000 | $66 | $66 | 0.0% | 14.3% | $7 | $10 | $7 | $12 | +85% |
| FundedNext | Stellar 1-Step | $15,000 | $130 | $130 | 0.0% | 14.3% | $17 | $24 | $18 | $30 | +82% |
| FundedNext | Stellar 1-Step | $25,000 | $220 | $220 | 0.0% | 14.3% | $28 | $39 | $30 | $50 | +82% |
| FundedNext | Stellar 1-Step | $50,000 | $330 | $330 | 0.0% | 14.3% | $57 | $73 | $60 | $100 | +78% |
| FundedNext | Stellar 1-Step | $100,000 | $570 | $570 | 0.0% | 14.3% | $114 | $142 | $120 | $199 | +75% |
| FundedNext | Stellar 1-Step | $200,000 | $1,100 | $1,100 | 0.0% | 14.3% | $227 | $282 | $239 | $398 | +74% |
| FundingPips | 1-Step Flex | $5,000 | $66 | $53 | 19.7% | 17.1% | $7 | $10 | $7 | $12 | +81% |
| FundingPips | 1-Step Flex | $10,000 | $99 | $79 | 20.2% | 17.1% | $14 | $19 | $15 | $25 | +76% |
| FundingPips | 1-Step Flex | $25,000 | $211 | $169 | 19.9% | 17.1% | $35 | $45 | $37 | $62 | +73% |
| FundingPips | 1-Step Flex | $50,000 | $313 | $250 | 20.1% | 17.1% | $70 | $85 | $75 | $125 | +66% |
| FundingPips | 1-Step Flex | $100,000 | $569 | $569 | 0.0% | 17.1% | $141 | $175 | $150 | $250 | +69% |
| Hola Prime | 1-Step Prime | $5,000 | $59 | $47 | 20.3% | 13.2% | $7 | $11 | $8 | $13 | +77% |
| Hola Prime | 1-Step Prime | $10,000 | $89 | $71 | 20.2% | 13.2% | $15 | $20 | $16 | $27 | +72% |
| Hola Prime | 1-Step Prime | $25,000 | $169 | $135 | 20.1% | 13.2% | $37 | $46 | $40 | $66 | +66% |
| Hola Prime | 1-Step Prime | $50,000 | $329 | $263 | 20.1% | 13.2% | $74 | $92 | $80 | $133 | +65% |
| Hola Prime | 1-Step Prime | $100,000 | $579 | $463 | 20.0% | 13.2% | $148 | $180 | $159 | $265 | +61% |
| Hola Prime | 1-Step Prime | $200,000 | $1,049 | $839 | 20.0% | 13.2% | $296 | $355 | $318 | $530 | +58% |
| The Funded Trader | Royal 1-Step | $5,000 | $79 | $63 | 20.3% | 12.8% | $8 | $8 | $8 | $13 | +87% |
| The Funded Trader | Royal 1-Step | $10,000 | $129 | $103 | 20.2% | 12.8% | $16 | $16 | $16 | $26 | +85% |
| The Funded Trader | Royal 1-Step | $25,000 | $249 | $199 | 20.1% | 12.8% | $40 | $40 | $40 | $66 | +80% |
| The Funded Trader | Royal 1-Step | $50,000 | $379 | $303 | 20.1% | 12.8% | $79 | $79 | $79 | $132 | +74% |
| The Funded Trader | Royal 1-Step | $100,000 | $599 | $479 | 20.0% | 12.8% | $158 | $158 | $158 | $264 | +67% |
| The5ers | Hyper Growth | $5,000 | $260 | $260 | 0.0% | 15.2% | $4 | $4 | $4 | $7 | +98% |
| The5ers | Hyper Growth | $10,000 | $450 | $450 | 0.0% | 15.2% | $8 | $8 | $8 | $14 | +98% |
| The5ers | Hyper Growth | $20,000 | $850 | $850 | 0.0% | 15.2% | $17 | $17 | $17 | $28 | +98% |
| Verodus | 1-Step | $5,000 | $55 | $36 | 34.5% | 8.8% | $5 | $9 | $6 | $10 | +76% |
| Verodus | 1-Step | $10,000 | $92 | $60 | 34.8% | 8.8% | $11 | $16 | $12 | $20 | +73% |
| Verodus | 1-Step | $25,000 | $185 | $120 | 35.1% | 8.8% | $27 | $38 | $30 | $49 | +69% |
| Verodus | 1-Step | $50,000 | $297 | $193 | 35.0% | 8.8% | $54 | $71 | $59 | $99 | +63% |
| Verodus | 1-Step | $100,000 | $516 | $335 | 35.1% | 8.8% | $108 | $138 | $119 | $198 | +59% |
| Verodus | 1-Step | $200,000 | $1,006 | $654 | 35.0% | 8.8% | $216 | $274 | $237 | $395 | +58% |
| Alpha Capital | Pro 10% | $5,000 | $33 | $26 | 21.2% | 11.8% | $6 | $6 | $6 | $11 | +76% |
| Alpha Capital | Pro 10% | $10,000 | $77 | $62 | 19.5% | 11.8% | $13 | $13 | $13 | $21 | +80% |
| Alpha Capital | Pro 10% | $25,000 | $177 | $142 | 19.8% | 11.8% | $32 | $32 | $32 | $53 | +78% |
| Alpha Capital | Pro 10% | $50,000 | $267 | $214 | 19.9% | 11.8% | $64 | $64 | $64 | $106 | +70% |
| Alpha Capital | Pro 10% | $100,000 | $447 | $358 | 19.9% | 11.8% | $127 | $127 | $127 | $212 | +65% |
| Alpha Capital | Pro 10% | $200,000 | $897 | $718 | 20.0% | 11.8% | $254 | $254 | $254 | $423 | +65% |
| Alpha Capital | Pro 6% | $5,000 | $27 | $22 | 18.5% | 9.0% | $5 | $5 | $5 | $9 | +76% |
| Alpha Capital | Pro 6% | $10,000 | $47 | $38 | 19.1% | 9.0% | $11 | $11 | $11 | $18 | +72% |
| Alpha Capital | Pro 6% | $25,000 | $117 | $94 | 19.7% | 9.0% | $27 | $27 | $27 | $44 | +72% |
| Alpha Capital | Pro 6% | $50,000 | $217 | $174 | 19.8% | 9.0% | $53 | $53 | $53 | $89 | +69% |
| Alpha Capital | Pro 6% | $100,000 | $397 | $318 | 19.9% | 9.0% | $107 | $107 | $107 | $178 | +66% |
| Alpha Capital | Pro 6% | $200,000 | $797 | $638 | 19.9% | 9.0% | $213 | $213 | $213 | $355 | +67% |
| Blue Guardian | 2-Step Standard | $5,000 | $55 | $44 | 20.0% | 11.6% | $7 | $12 | $8 | $13 | +73% |
| Blue Guardian | 2-Step Standard | $10,000 | $97 | $78 | 19.6% | 11.6% | $14 | $23 | $15 | $26 | +71% |
| Blue Guardian | 2-Step Standard | $25,000 | $187 | $150 | 19.8% | 11.6% | $34 | $52 | $39 | $64 | +66% |
| Blue Guardian | 2-Step Standard | $50,000 | $287 | $230 | 19.9% | 11.6% | $68 | $95 | $77 | $129 | +59% |
| Blue Guardian | 2-Step Standard | $100,000 | $497 | $398 | 19.9% | 11.6% | $137 | $183 | $154 | $257 | +54% |
| BrightFunded | 2-Step | $5,000 | $55 | $44 | 20.0% | 12.9% | $7 | $13 | $8 | $14 | +71% |
| BrightFunded | 2-Step | $10,000 | $99 | $79 | 20.2% | 12.9% | $14 | $24 | $16 | $27 | +69% |
| BrightFunded | 2-Step | $25,000 | $189 | $151 | 20.1% | 12.9% | $35 | $55 | $41 | $68 | +64% |
| BrightFunded | 2-Step | $50,000 | $289 | $231 | 20.1% | 12.9% | $71 | $101 | $81 | $136 | +56% |
| BrightFunded | 2-Step | $100,000 | $399 | $319 | 20.1% | 12.9% | $142 | $183 | $163 | $271 | +43% |
| BrightFunded | 2-Step | $200,000 | $297 | $238 | 19.9% | 12.9% | $283 | $314 | $326 | $543 | -32% |
| City Traders Imperium | 2-Step | $10,000 | $99 | $79 | 20.2% | 11.3% | $13 | $22 | $14 | $24 | +73% |
| City Traders Imperium | 2-Step | $25,000 | $199 | $159 | 20.1% | 11.3% | $32 | $50 | $36 | $60 | +69% |
| City Traders Imperium | 2-Step | $50,000 | $349 | $279 | 20.1% | 11.3% | $63 | $95 | $72 | $119 | +66% |
| City Traders Imperium | 2-Step | $100,000 | $549 | $439 | 20.0% | 11.3% | $127 | $176 | $143 | $238 | +60% |
| FTMO | 2-Step | $10,000 | $103 | $103 | 0.0% | 12.7% | $9 | $22 | $11 | $18 | +78% |
| FTMO | 2-Step | $25,000 | $290 | $290 | 0.0% | 12.7% | $23 | $60 | $26 | $44 | +79% |
| FTMO | 2-Step | $50,000 | $400 | $400 | 0.0% | 12.7% | $46 | $97 | $53 | $88 | +76% |
| FTMO | 2-Step | $100,000 | $626 | $626 | 0.0% | 12.7% | $92 | $172 | $105 | $175 | +73% |
| FTMO | 2-Step | $200,000 | $1,253 | $1,253 | 0.0% | 12.7% | $183 | $343 | $210 | $350 | +73% |
| FXIFY | 2-Step | $5,000 | $59 | $47 | 20.3% | 8.9% | $3 | $7 | $3 | $6 | +84% |
| FXIFY | 2-Step | $10,000 | $89 | $71 | 20.2% | 8.9% | $6 | $13 | $7 | $11 | +82% |
| FXIFY | 2-Step | $25,000 | $189 | $151 | 20.1% | 8.9% | $16 | $29 | $17 | $28 | +81% |
| FXIFY | 2-Step | $50,000 | $379 | $303 | 20.1% | 8.9% | $31 | $58 | $34 | $57 | +81% |
| FXIFY | 2-Step | $100,000 | $499 | $399 | 20.0% | 8.9% | $62 | $98 | $68 | $114 | +76% |
| FXIFY | 2-Step | $200,000 | $999 | $799 | 20.0% | 8.9% | $124 | $195 | $136 | $227 | +76% |
| Fintokei | ProTrader | $5,000 | $44 | $35 | 20.5% | 12.6% | $7 | $12 | $8 | $14 | +67% |
| Fintokei | ProTrader | $10,000 | $99 | $79 | 20.2% | 12.6% | $14 | $24 | $16 | $27 | +69% |
| Fintokei | ProTrader | $25,000 | $199 | $159 | 20.1% | 12.6% | $36 | $56 | $41 | $68 | +65% |
| Fintokei | ProTrader | $50,000 | $299 | $239 | 20.1% | 12.6% | $71 | $102 | $82 | $136 | +58% |
| Fintokei | ProTrader | $100,000 | $529 | $423 | 20.0% | 12.6% | $143 | $196 | $164 | $273 | +54% |
| Fintokei | ProTrader | $200,000 | $999 | $799 | 20.0% | 12.6% | $286 | $386 | $327 | $545 | +52% |
| For Traders | 2-Step | $5,000 | $49 | $39 | 20.4% | 10.4% | $6 | $10 | $7 | $11 | +74% |
| For Traders | 2-Step | $10,000 | $89 | $71 | 20.2% | 10.4% | $12 | $20 | $14 | $23 | +72% |
| For Traders | 2-Step | $25,000 | $179 | $143 | 20.1% | 10.4% | $31 | $45 | $34 | $57 | +68% |
| For Traders | 2-Step | $50,000 | $289 | $231 | 20.1% | 10.4% | $61 | $85 | $68 | $114 | +63% |
| For Traders | 2-Step | $100,000 | $489 | $391 | 20.0% | 10.4% | $122 | $163 | $136 | $227 | +58% |
| FundedNext | Stellar 2-Step | $6,000 | $66 | $66 | 0.0% | 12.9% | $5 | $14 | $6 | $10 | +79% |
| FundedNext | Stellar 2-Step | $15,000 | $130 | $130 | 0.0% | 12.9% | $14 | $30 | $16 | $26 | +77% |
| FundedNext | Stellar 2-Step | $25,000 | $220 | $220 | 0.0% | 12.9% | $23 | $51 | $26 | $43 | +77% |
| FundedNext | Stellar 2-Step | $50,000 | $330 | $330 | 0.0% | 12.9% | $45 | $88 | $52 | $87 | +73% |
| FundedNext | Stellar 2-Step | $100,000 | $550 | $550 | 0.0% | 12.9% | $91 | $161 | $104 | $173 | +71% |
| FundedNext | Stellar 2-Step | $200,000 | $1,100 | $1,100 | 0.0% | 12.9% | $181 | $323 | $208 | $346 | +71% |
| FundedNext | Stellar Lite | $5,000 | $33 | $33 | 0.0% | 12.0% | $4 | $8 | $5 | $8 | +74% |
| FundedNext | Stellar Lite | $10,000 | $59 | $59 | 0.0% | 12.0% | $9 | $16 | $10 | $17 | +73% |
| FundedNext | Stellar Lite | $25,000 | $149 | $149 | 0.0% | 12.0% | $22 | $40 | $25 | $42 | +73% |
| FundedNext | Stellar Lite | $50,000 | $249 | $249 | 0.0% | 12.0% | $45 | $75 | $51 | $85 | +70% |
| FundedNext | Stellar Lite | $100,000 | $449 | $449 | 0.0% | 12.0% | $90 | $143 | $102 | $170 | +68% |
| Funding Traders | 2-Step | $5,000 | $36 | $29 | 19.4% | 13.0% | $7 | $11 | $8 | $14 | +62% |
| Funding Traders | 2-Step | $10,000 | $66 | $53 | 19.7% | 13.0% | $15 | $22 | $17 | $28 | +59% |
| Funding Traders | 2-Step | $25,000 | $156 | $125 | 19.9% | 13.0% | $37 | $53 | $42 | $70 | +58% |
| Funding Traders | 2-Step | $50,000 | $266 | $213 | 19.9% | 13.0% | $73 | $101 | $84 | $141 | +53% |
| Funding Traders | 2-Step | $100,000 | $499 | $399 | 20.0% | 13.0% | $147 | $199 | $169 | $281 | +50% |
| FundingPips | 2-Step Flex | $5,000 | $32 | $26 | 18.8% | 14.3% | $5 | $5 | $5 | $9 | +80% |
| FundingPips | 2-Step Flex | $10,000 | $59 | $47 | 20.3% | 14.3% | $10 | $10 | $10 | $17 | +78% |
| FundingPips | 2-Step Flex | $25,000 | $159 | $127 | 20.1% | 14.3% | $26 | $26 | $26 | $43 | +80% |
| FundingPips | 2-Step Flex | $50,000 | $269 | $215 | 20.1% | 14.3% | $52 | $52 | $52 | $86 | +76% |
| FundingPips | 2-Step Flex | $100,000 | $555 | $555 | 0.0% | 14.3% | $104 | $104 | $104 | $173 | +81% |
| FundingPips | 2-Step Pro | $5,000 | $29 | $23 | 20.7% | 9.9% | $5 | $5 | $5 | $9 | +77% |
| FundingPips | 2-Step Pro | $10,000 | $55 | $44 | 20.0% | 9.9% | $11 | $11 | $11 | $18 | +76% |
| FundingPips | 2-Step Pro | $25,000 | $134 | $107 | 20.1% | 9.9% | $27 | $27 | $27 | $45 | +75% |
| FundingPips | 2-Step Pro | $50,000 | $224 | $179 | 20.1% | 9.9% | $54 | $54 | $54 | $89 | +70% |
| FundingPips | 2-Step Pro | $100,000 | $422 | $422 | 0.0% | 9.9% | $107 | $107 | $107 | $179 | +75% |
| FundingPips | 2-Step Pro | $200,000 | $844 | $675 | 20.0% | 9.9% | $215 | $215 | $215 | $358 | +68% |
| FundingPips | 2-Step Standard | $5,000 | $34 | $27 | 20.6% | 12.6% | $7 | $8 | $7 | $12 | +71% |
| FundingPips | 2-Step Standard | $10,000 | $63 | $50 | 20.6% | 12.6% | $13 | $16 | $14 | $23 | +69% |
| FundingPips | 2-Step Standard | $25,000 | $168 | $134 | 20.2% | 12.6% | $34 | $39 | $35 | $59 | +71% |
| FundingPips | 2-Step Standard | $50,000 | $285 | $228 | 20.0% | 12.6% | $67 | $77 | $70 | $117 | +66% |
| FundingPips | 2-Step Standard | $100,000 | $544 | $544 | 0.0% | 12.6% | $134 | $158 | $140 | $234 | +71% |
| Goat Funded | 2-Step Standard | $5,000 | $36 | $29 | 19.4% | 12.9% | $7 | $11 | $8 | $13 | +63% |
| Goat Funded | 2-Step Standard | $10,000 | $66 | $53 | 19.7% | 12.9% | $14 | $21 | $16 | $26 | +61% |
| Goat Funded | 2-Step Standard | $25,000 | $156 | $125 | 19.9% | 12.9% | $34 | $51 | $39 | $66 | +60% |
| Goat Funded | 2-Step Standard | $50,000 | $266 | $213 | 19.9% | 12.9% | $69 | $96 | $79 | $132 | +55% |
| Goat Funded | 2-Step Standard | $100,000 | $499 | $399 | 20.0% | 12.9% | $138 | $189 | $158 | $263 | +53% |
| Hola Prime | 2-Step Prime | $5,000 | $47 | $38 | 19.1% | 12.3% | $7 | $9 | $7 | $12 | +75% |
| Hola Prime | 2-Step Prime | $10,000 | $69 | $55 | 20.3% | 12.3% | $14 | $17 | $15 | $25 | +68% |
| Hola Prime | 2-Step Prime | $25,000 | $159 | $127 | 20.1% | 12.3% | $34 | $43 | $37 | $61 | +66% |
| Hola Prime | 2-Step Prime | $50,000 | $319 | $255 | 20.1% | 12.3% | $69 | $86 | $74 | $123 | +66% |
| Hola Prime | 2-Step Prime | $100,000 | $569 | $455 | 20.0% | 12.3% | $138 | $168 | $147 | $246 | +63% |
| Hola Prime | 2-Step Prime | $200,000 | $939 | $751 | 20.0% | 12.3% | $276 | $325 | $295 | $492 | +57% |
| Maven | 2-Step | $5,000 | $22 | $18 | 18.2% | 12.7% | $7 | $9 | $8 | $13 | +49% |
| Maven | 2-Step | $10,000 | $44 | $35 | 20.5% | 12.7% | $14 | $18 | $16 | $26 | +48% |
| Maven | 2-Step | $25,000 | $99 | $79 | 20.2% | 12.7% | $34 | $44 | $39 | $65 | +44% |
| Maven | 2-Step | $50,000 | $189 | $151 | 20.1% | 12.7% | $68 | $87 | $78 | $130 | +42% |
| Maven | 2-Step | $100,000 | $349 | $279 | 20.1% | 12.7% | $136 | $172 | $156 | $260 | +38% |
| Ment Funding | 2-Step | $5,000 | $39 | $31 | 20.5% | 10.5% | $6 | $9 | $7 | $11 | +70% |
| Ment Funding | 2-Step | $10,000 | $69 | $55 | 20.3% | 10.5% | $12 | $18 | $14 | $23 | +67% |
| Ment Funding | 2-Step | $25,000 | $149 | $119 | 20.1% | 10.5% | $31 | $43 | $34 | $57 | +64% |
| Ment Funding | 2-Step | $50,000 | $249 | $199 | 20.1% | 10.5% | $61 | $82 | $68 | $114 | +59% |
| Ment Funding | 2-Step | $100,000 | $429 | $343 | 20.0% | 10.5% | $123 | $159 | $137 | $228 | +54% |
| The Funded Trader | Standard | $5,000 | $49 | $39 | 20.4% | 12.9% | $7 | $12 | $8 | $14 | +68% |
| The Funded Trader | Standard | $10,000 | $99 | $79 | 20.2% | 12.9% | $15 | $25 | $17 | $28 | +69% |
| The Funded Trader | Standard | $25,000 | $189 | $151 | 20.1% | 12.9% | $36 | $56 | $42 | $70 | +63% |
| The Funded Trader | Standard | $50,000 | $289 | $231 | 20.1% | 12.9% | $73 | $103 | $83 | $139 | +56% |
| The Funded Trader | Standard | $100,000 | $499 | $399 | 20.0% | 12.9% | $145 | $197 | $167 | $278 | +51% |
| The Funded Trader | Standard | $200,000 | $939 | $751 | 20.0% | 12.9% | $290 | $388 | $334 | $556 | +48% |
| The5ers | High Stakes | $5,000 | $35 | $35 | 0.0% | 11.2% | $11 | $11 | $11 | $19 | +67% |
| The5ers | High Stakes | $10,000 | $60 | $60 | 0.0% | 11.2% | $23 | $23 | $23 | $38 | +62% |
| The5ers | High Stakes | $20,000 | $99 | $99 | 0.0% | 11.2% | $46 | $46 | $46 | $77 | +54% |
| The5ers | High Stakes | $60,000 | $229 | $229 | 0.0% | 11.2% | $138 | $138 | $138 | $230 | +40% |
| The5ers | High Stakes | $100,000 | $395 | $395 | 0.0% | 11.2% | $230 | $230 | $230 | $383 | +42% |
| Verodus | 2-Step Lite | $5,000 | $27 | $18 | 33.3% | 10.6% | $7 | $9 | $8 | $13 | +52% |
| Verodus | 2-Step Lite | $10,000 | $51 | $33 | 35.3% | 10.6% | $14 | $17 | $15 | $25 | +48% |
| Verodus | 2-Step Lite | $25,000 | $101 | $66 | 34.7% | 10.6% | $34 | $41 | $38 | $63 | +38% |
| Verodus | 2-Step Lite | $50,000 | $204 | $133 | 34.8% | 10.6% | $68 | $82 | $76 | $127 | +38% |
| Verodus | 2-Step Lite | $100,000 | $371 | $241 | 35.0% | 10.6% | $136 | $162 | $152 | $254 | +33% |
| Verodus | 2-Step Lite | $200,000 | $734 | $477 | 35.0% | 10.6% | $272 | $323 | $304 | $507 | +32% |
| Verodus | 2-Step Pro | $5,000 | $31 | $20 | 35.5% | 12.0% | $7 | $9 | $8 | $13 | +55% |
| Verodus | 2-Step Pro | $10,000 | $56 | $36 | 35.7% | 12.0% | $13 | $18 | $15 | $25 | +51% |
| Verodus | 2-Step Pro | $25,000 | $131 | $85 | 35.1% | 12.0% | $33 | $43 | $38 | $63 | +49% |
| Verodus | 2-Step Pro | $50,000 | $250 | $163 | 34.8% | 12.0% | $66 | $86 | $75 | $126 | +47% |
| Verodus | 2-Step Pro | $100,000 | $455 | $296 | 34.9% | 12.0% | $133 | $168 | $151 | $251 | +43% |
| Verodus | 2-Step Pro | $200,000 | $887 | $577 | 34.9% | 12.0% | $265 | $334 | $301 | $502 | +42% |
| Maven | 3-Step | $5,000 | $17 | $14 | 17.6% | 5.1% | $3 | $4 | $3 | $6 | +72% |
| Maven | 3-Step | $10,000 | $32 | $26 | 18.8% | 5.1% | $6 | $8 | $7 | $11 | +70% |
| Maven | 3-Step | $25,000 | $69 | $55 | 20.3% | 5.1% | $16 | $19 | $17 | $28 | +66% |
| Maven | 3-Step | $50,000 | $129 | $103 | 20.2% | 5.1% | $32 | $37 | $33 | $56 | +64% |
| Maven | 3-Step | $100,000 | $249 | $199 | 20.1% | 5.1% | $64 | $74 | $67 | $112 | +63% |
| The5ers | Bootcamp | $20,000 | $22 | $22 | 0.0% | 4.6% | $5 | $5 | $5 | $8 | +78% |
| The5ers | Bootcamp | $100,000 | $95 | $95 | 0.0% | 4.6% | $24 | $24 | $24 | $41 | +74% |
| Alpha Capital | Instant | $5,000 | $67 | $40 | 40.3% | 13.0% | $35 | $35 | $35 | $58 | +14% |
| Alpha Capital | Instant | $10,000 | $97 | $58 | 40.2% | 13.0% | $69 | $69 | $69 | $115 | -19% |
| Alpha Capital | Instant | $25,000 | $197 | $118 | 40.1% | 13.0% | $173 | $173 | $173 | $288 | -46% |
| Alpha Capital | Instant | $50,000 | $257 | $154 | 40.1% | 13.0% | $345 | $345 | $345 | $575 | -124% |
| Alpha Capital | Instant | $100,000 | $457 | $274 | 40.0% | 13.0% | $690 | $690 | $690 | $1,150 | -152% |
| Alpha Capital | Instant | $200,000 | $897 | $538 | 40.0% | 13.0% | $1,380 | $1,380 | $1,380 | $2,300 | -157% |
| Blue Guardian | Instant | $5,000 | $89 | $71 | 20.2% | 22.1% | $41 | $41 | $41 | $69 | +42% |
| Blue Guardian | Instant | $10,000 | $149 | $119 | 20.1% | 22.1% | $83 | $83 | $83 | $138 | +30% |
| Blue Guardian | Instant | $25,000 | $279 | $223 | 20.1% | 22.1% | $207 | $207 | $207 | $345 | +7% |
| Blue Guardian | Instant | $50,000 | $429 | $343 | 20.0% | 22.1% | $414 | $414 | $414 | $690 | -21% |
| Blue Guardian | Instant | $100,000 | $699 | $559 | 20.0% | 22.1% | $828 | $828 | $828 | $1,380 | -48% |
| FXIFY | Instant Lite | $2,500 | $19 | $19 | 0.0% | 15.7% | $17 | $17 | $17 | $28 | +11% |
| FXIFY | Instant Lite | $5,000 | $39 | $39 | 0.0% | 15.7% | $34 | $34 | $34 | $57 | +13% |
| FXIFY | Instant Lite | $10,000 | $79 | $79 | 0.0% | 15.7% | $68 | $68 | $68 | $113 | +14% |
| FXIFY | Instant Lite | $25,000 | $149 | $149 | 0.0% | 15.7% | $170 | $170 | $170 | $283 | -14% |
| FXIFY | Instant Lite | $50,000 | $249 | $249 | 0.0% | 15.7% | $340 | $340 | $340 | $566 | -36% |
| FXIFY | Instant Lite | $100,000 | $399 | $399 | 0.0% | 15.7% | $680 | $680 | $680 | $1,133 | -70% |
| FXIFY | Instant Standard | $5,000 | $109 | $87 | 20.2% | 54.2% | $36 | $36 | $36 | $60 | +59% |
| FXIFY | Instant Standard | $10,000 | $179 | $143 | 20.1% | 54.2% | $72 | $72 | $72 | $119 | +50% |
| FXIFY | Instant Standard | $25,000 | $329 | $263 | 20.1% | 54.2% | $179 | $179 | $179 | $298 | +32% |
| FXIFY | Instant Standard | $50,000 | $529 | $423 | 20.0% | 54.2% | $358 | $358 | $358 | $596 | +15% |
| FXIFY | Instant Standard | $100,000 | $799 | $639 | 20.0% | 54.2% | $716 | $716 | $716 | $1,193 | -12% |
| FundedNext | Stellar Instant | $2,000 | $59 | $59 | 0.0% | 53.2% | $13 | $44 | $27 | $45 | +25% |
| FundedNext | Stellar Instant | $5,000 | $99 | $99 | 0.0% | 53.2% | $32 | $84 | $68 | $113 | +15% |
| FundedNext | Stellar Instant | $10,000 | $199 | $199 | 0.0% | 53.2% | $64 | $169 | $136 | $226 | +15% |
| FundedNext | Stellar Instant | $20,000 | $599 | $599 | 0.0% | 53.2% | $127 | $445 | $271 | $452 | +26% |
| FundingPips | Zero | $5,000 | $60 | $48 | 20.0% | 15.3% | $41 | $41 | $41 | $69 | +14% |
| FundingPips | Zero | $10,000 | $88 | $70 | 20.5% | 15.3% | $83 | $83 | $83 | $138 | -18% |
| FundingPips | Zero | $25,000 | $188 | $150 | 20.2% | 15.3% | $207 | $207 | $207 | $345 | -38% |
| FundingPips | Zero | $50,000 | $244 | $195 | 20.1% | 15.3% | $415 | $415 | $415 | $691 | -113% |
| FundingPips | Zero | $100,000 | $444 | $444 | 0.0% | 15.3% | $829 | $829 | $829 | $1,382 | -87% |
| FundingPips | Zero | $200,000 | $888 | $710 | 20.0% | 15.3% | $1,658 | $1,658 | $1,658 | $2,763 | -134% |
| Goat Funded | Instant GOAT | $5,000 | $79 | $63 | 20.3% | 16.6% | $42 | $42 | $42 | $70 | +33% |
| Goat Funded | Instant GOAT | $10,000 | $129 | $103 | 20.2% | 16.6% | $85 | $85 | $85 | $141 | +18% |
| Goat Funded | Instant GOAT | $25,000 | $249 | $199 | 20.1% | 16.6% | $211 | $211 | $211 | $352 | -6% |
| Goat Funded | Instant GOAT | $50,000 | $399 | $319 | 20.1% | 16.6% | $423 | $423 | $423 | $705 | -33% |
| Goat Funded | Instant GOAT | $100,000 | $699 | $559 | 20.0% | 16.6% | $846 | $846 | $846 | $1,410 | -51% |
| Hola Prime | Direct | $5,000 | $99 | $79 | 20.2% | 23.8% | $46 | $56 | $53 | $88 | +29% |
| Hola Prime | Direct | $10,000 | $132 | $106 | 19.7% | 23.8% | $92 | $105 | $105 | $176 | +1% |
| Hola Prime | Direct | $25,000 | $369 | $295 | 20.1% | 23.8% | $230 | $267 | $263 | $439 | +9% |
| Hola Prime | Direct | $50,000 | $689 | $551 | 20.0% | 23.8% | $460 | $530 | $527 | $878 | +4% |
| Hola Prime | Direct | $100,000 | $1,049 | $839 | 20.0% | 23.8% | $920 | $1,026 | $1,053 | $1,755 | -22% |
| Instant Funding | Instant | $5,000 | $109 | $87 | 20.2% | 21.4% | $42 | $42 | $42 | $70 | +52% |
| Instant Funding | Instant | $10,000 | $179 | $143 | 20.1% | 21.4% | $84 | $84 | $84 | $140 | +41% |
| Instant Funding | Instant | $25,000 | $329 | $263 | 20.1% | 21.4% | $210 | $210 | $210 | $350 | +20% |
| Instant Funding | Instant | $50,000 | $529 | $423 | 20.0% | 21.4% | $421 | $421 | $421 | $701 | +1% |
| Instant Funding | Instant | $100,000 | $799 | $639 | 20.0% | 21.4% | $841 | $841 | $841 | $1,402 | -32% |
| Verodus | Instant | $5,000 | $110 | $72 | 34.5% | 22.1% | $44 | $44 | $44 | $73 | +39% |
| Verodus | Instant | $10,000 | $184 | $121 | 34.2% | 22.1% | $88 | $88 | $88 | $146 | +28% |
| Verodus | Instant | $25,000 | $370 | $242 | 34.6% | 22.1% | $219 | $219 | $219 | $365 | +10% |
| Verodus | Instant | $50,000 | $594 | $389 | 34.5% | 22.1% | $438 | $438 | $438 | $729 | -13% |
| Verodus | Instant | $100,000 | $1,032 | $676 | 34.5% | 22.1% | $875 | $875 | $875 | $1,459 | -29% |
| Verodus | Instant | $200,000 | $2,012 | $1,318 | 34.5% | 22.1% | $1,751 | $1,751 | $1,751 | $2,918 | -33% |

## $5k / $10k / $100k snapshot (sale margin)

### $5,000

| Firm | Plan | Sale | P(pay) | E[cost] | Sale m | vs Verodus peer |
|---|---|---:|---:|---:|---:|---|
| FXIFY | Instant Lite | $39 | 15.7% | $34 | +13% | instant |
| FundingPips | Zero | $48 | 15.3% | $41 | +14% | instant |
| Alpha Capital | Instant | $40 | 13.0% | $35 | +14% | instant |
| FundedNext | Stellar Instant | $99 | 53.2% | $84 | +15% | instant |
| Hola Prime | Direct | $79 | 23.8% | $56 | +29% | instant |
| Goat Funded | Instant GOAT | $63 | 16.6% | $42 | +33% | instant |
| Verodus | Instant | $72 | 22.1% | $44 | +39% | instant |
| Blue Guardian | Instant | $71 | 22.1% | $41 | +42% | instant |
| Maven | 2-Step | $18 | 12.7% | $9 | +49% | 2-step |
| Verodus | 2-Step Lite | $18 | 10.6% | $9 | +52% | 2-step |
| Instant Funding | Instant | $87 | 21.4% | $42 | +52% | instant |
| Verodus | 2-Step Pro | $20 | 12.0% | $9 | +55% | 2-step |
| FXIFY | Instant Standard | $87 | 54.2% | $36 | +59% | instant |
| Funding Traders | 2-Step | $29 | 13.0% | $11 | +62% | 2-step |
| Goat Funded | 2-Step Standard | $29 | 12.9% | $11 | +63% | 2-step |
| Blue Guardian | 1-Step Standard | $47 | 15.1% | $16 | +65% | 1-step |
| Fintokei | SwiftTrader | $35 | 12.5% | $12 | +66% | 1-step |
| Fintokei | ProTrader | $35 | 12.6% | $12 | +67% | 2-step |
| The5ers | High Stakes | $35 | 11.2% | $11 | +67% | 2-step |
| The Funded Trader | Standard | $39 | 12.9% | $12 | +68% | 2-step |
| Ment Funding | 2-Step | $31 | 10.5% | $9 | +70% | 2-step |
| FundingPips | 2-Step Standard | $27 | 12.6% | $8 | +71% | 2-step |
| BrightFunded | 2-Step | $44 | 12.9% | $13 | +71% | 2-step |
| Maven | 3-Step | $14 | 5.1% | $4 | +72% | 3-step |
| Blue Guardian | 2-Step Standard | $44 | 11.6% | $12 | +73% | 2-step |
| For Traders | 2-Step | $39 | 10.4% | $10 | +74% | 2-step |
| FundedNext | Stellar Lite | $33 | 12.0% | $8 | +74% | 2-step |
| Hola Prime | 2-Step Prime | $38 | 12.3% | $9 | +75% | 2-step |
| Alpha Capital | Pro 10% | $26 | 11.8% | $6 | +76% | 2-step |
| Alpha Capital | Pro 6% | $22 | 9.0% | $5 | +76% | 2-step |
| Verodus | 1-Step | $36 | 8.8% | $9 | +76% | 1-step |
| FundingPips | 2-Step Pro | $23 | 9.9% | $5 | +77% | 2-step |
| Hola Prime | 1-Step Prime | $47 | 13.2% | $11 | +77% | 1-step |
| FundingPips | 2-Step Flex | $26 | 14.3% | $5 | +80% | 2-step |
| Alpha Capital | One 10% | $40 | 7.0% | $8 | +81% | 1-step |
| FundingPips | 1-Step Flex | $53 | 17.1% | $10 | +81% | 1-step |
| E8 Markets | E8 One 6% | $59 | 8.0% | $9 | +84% | 1-step |
| FXIFY | 2-Step | $47 | 8.9% | $7 | +84% | 2-step |
| The Funded Trader | Royal 1-Step | $63 | 12.8% | $8 | +87% | 1-step |
| The5ers | Hyper Growth | $260 | 15.2% | $4 | +98% | 1-step |

### $10,000

| Firm | Plan | Sale | P(pay) | E[cost] | Sale m | vs Verodus peer |
|---|---|---:|---:|---:|---:|---|
| Alpha Capital | Instant | $58 | 13.0% | $69 | -19% | instant |
| FundingPips | Zero | $70 | 15.3% | $83 | -18% | instant |
| Hola Prime | Direct | $106 | 23.8% | $105 | +1% | instant |
| FXIFY | Instant Lite | $79 | 15.7% | $68 | +14% | instant |
| FundedNext | Stellar Instant | $199 | 53.2% | $169 | +15% | instant |
| Goat Funded | Instant GOAT | $103 | 16.6% | $85 | +18% | instant |
| Verodus | Instant | $121 | 22.1% | $88 | +28% | instant |
| Blue Guardian | Instant | $119 | 22.1% | $83 | +30% | instant |
| Instant Funding | Instant | $143 | 21.4% | $84 | +41% | instant |
| Verodus | 2-Step Lite | $33 | 10.6% | $17 | +48% | 2-step |
| Maven | 2-Step | $35 | 12.7% | $18 | +48% | 2-step |
| FXIFY | Instant Standard | $143 | 54.2% | $72 | +50% | instant |
| Verodus | 2-Step Pro | $36 | 12.0% | $18 | +51% | 2-step |
| Funding Traders | 2-Step | $53 | 13.0% | $22 | +59% | 2-step |
| Goat Funded | 2-Step Standard | $53 | 12.9% | $21 | +61% | 2-step |
| Blue Guardian | 1-Step Standard | $79 | 15.1% | $31 | +61% | 1-step |
| The5ers | High Stakes | $60 | 11.2% | $23 | +62% | 2-step |
| Fintokei | SwiftTrader | $71 | 12.5% | $24 | +67% | 1-step |
| Ment Funding | 2-Step | $55 | 10.5% | $18 | +67% | 2-step |
| Hola Prime | 2-Step Prime | $55 | 12.3% | $17 | +68% | 2-step |
| The Funded Trader | Standard | $79 | 12.9% | $25 | +69% | 2-step |
| FundingPips | 2-Step Standard | $50 | 12.6% | $16 | +69% | 2-step |
| BrightFunded | 2-Step | $79 | 12.9% | $24 | +69% | 2-step |
| Fintokei | ProTrader | $79 | 12.6% | $24 | +69% | 2-step |
| Maven | 3-Step | $26 | 5.1% | $8 | +70% | 3-step |
| Blue Guardian | 2-Step Standard | $78 | 11.6% | $23 | +71% | 2-step |
| FTMO | 1-Step | $92 | 13.5% | $26 | +71% | 1-step |
| Alpha Capital | Pro 6% | $38 | 9.0% | $11 | +72% | 2-step |
| Hola Prime | 1-Step Prime | $71 | 13.2% | $20 | +72% | 1-step |
| For Traders | 2-Step | $71 | 10.4% | $20 | +72% | 2-step |
| City Traders Imperium | 2-Step | $79 | 11.3% | $22 | +73% | 2-step |
| FundedNext | Stellar Lite | $59 | 12.0% | $16 | +73% | 2-step |
| Verodus | 1-Step | $60 | 8.8% | $16 | +73% | 1-step |
| FundingPips | 2-Step Pro | $44 | 9.9% | $11 | +76% | 2-step |
| FundingPips | 1-Step Flex | $79 | 17.1% | $19 | +76% | 1-step |
| FundingPips | 2-Step Flex | $47 | 14.3% | $10 | +78% | 2-step |
| FTMO | 2-Step | $103 | 12.7% | $22 | +78% | 2-step |
| Alpha Capital | Pro 10% | $62 | 11.8% | $13 | +80% | 2-step |
| Alpha Capital | One 10% | $78 | 7.0% | $16 | +80% | 1-step |
| FXIFY | 2-Step | $71 | 8.9% | $13 | +82% | 2-step |
| The Funded Trader | Royal 1-Step | $103 | 12.8% | $16 | +85% | 1-step |
| E8 Markets | E8 One 6% | $138 | 8.0% | $19 | +86% | 1-step |
| The5ers | Hyper Growth | $450 | 15.2% | $8 | +98% | 1-step |

### $100,000

| Firm | Plan | Sale | P(pay) | E[cost] | Sale m | vs Verodus peer |
|---|---|---:|---:|---:|---:|---|
| Alpha Capital | Instant | $274 | 13.0% | $690 | -152% | instant |
| FundingPips | Zero | $444 | 15.3% | $829 | -87% | instant |
| FXIFY | Instant Lite | $399 | 15.7% | $680 | -70% | instant |
| Goat Funded | Instant GOAT | $559 | 16.6% | $846 | -51% | instant |
| Blue Guardian | Instant | $559 | 22.1% | $828 | -48% | instant |
| Instant Funding | Instant | $639 | 21.4% | $841 | -32% | instant |
| Verodus | Instant | $676 | 22.1% | $875 | -29% | instant |
| Hola Prime | Direct | $839 | 23.8% | $1,026 | -22% | instant |
| FXIFY | Instant Standard | $639 | 54.2% | $716 | -12% | instant |
| Verodus | 2-Step Lite | $241 | 10.6% | $162 | +33% | 2-step |
| Blue Guardian | 1-Step Standard | $399 | 15.1% | $246 | +38% | 1-step |
| Maven | 2-Step | $279 | 12.7% | $172 | +38% | 2-step |
| The5ers | High Stakes | $395 | 11.2% | $230 | +42% | 2-step |
| BrightFunded | 2-Step | $319 | 12.9% | $183 | +43% | 2-step |
| Verodus | 2-Step Pro | $296 | 12.0% | $168 | +43% | 2-step |
| Funding Traders | 2-Step | $399 | 13.0% | $199 | +50% | 2-step |
| Fintokei | SwiftTrader | $399 | 12.5% | $198 | +50% | 1-step |
| The Funded Trader | Standard | $399 | 12.9% | $197 | +51% | 2-step |
| Goat Funded | 2-Step Standard | $399 | 12.9% | $189 | +53% | 2-step |
| Fintokei | ProTrader | $423 | 12.6% | $196 | +54% | 2-step |
| Ment Funding | 2-Step | $343 | 10.5% | $159 | +54% | 2-step |
| Blue Guardian | 2-Step Standard | $398 | 11.6% | $183 | +54% | 2-step |
| FTMO | 1-Step | $579 | 13.5% | $265 | +54% | 1-step |
| For Traders | 2-Step | $391 | 10.4% | $163 | +58% | 2-step |
| Verodus | 1-Step | $335 | 8.8% | $138 | +59% | 1-step |
| City Traders Imperium | 2-Step | $439 | 11.3% | $176 | +60% | 2-step |
| Alpha Capital | One 10% | $398 | 7.0% | $156 | +61% | 1-step |
| Hola Prime | 1-Step Prime | $463 | 13.2% | $180 | +61% | 1-step |
| Maven | 3-Step | $199 | 5.1% | $74 | +63% | 3-step |
| Hola Prime | 2-Step Prime | $455 | 12.3% | $168 | +63% | 2-step |
| Alpha Capital | Pro 10% | $358 | 11.8% | $127 | +65% | 2-step |
| E8 Markets | E8 One 6% | $538 | 8.0% | $186 | +65% | 1-step |
| Alpha Capital | Pro 6% | $318 | 9.0% | $107 | +66% | 2-step |
| The Funded Trader | Royal 1-Step | $479 | 12.8% | $158 | +67% | 1-step |
| FundedNext | Stellar Lite | $449 | 12.0% | $143 | +68% | 2-step |
| FundingPips | 1-Step Flex | $569 | 17.1% | $175 | +69% | 1-step |
| E8 Markets | Signature | $498 | 6.6% | $152 | +70% | 1-step |
| FundedNext | Stellar 2-Step | $550 | 12.9% | $161 | +71% | 2-step |
| FundingPips | 2-Step Standard | $544 | 12.6% | $158 | +71% | 2-step |
| FTMO | 2-Step | $626 | 12.7% | $172 | +73% | 2-step |
| The5ers | Bootcamp | $95 | 4.6% | $24 | +74% | 3-step |
| FundingPips | 2-Step Pro | $422 | 9.9% | $107 | +75% | 2-step |
| FundedNext | Stellar 1-Step | $570 | 14.3% | $142 | +75% | 1-step |
| FXIFY | 2-Step | $399 | 8.9% | $98 | +76% | 2-step |
| FundingPips | 2-Step Flex | $555 | 14.3% | $104 | +81% | 2-step |

