# Verodus — final live-site changes

**This is the paste list.** Use it on live `www.verodus.com` and matching locale JSON.

**How to use:** paste HTML, then the same string in `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`.

**Fresh live scan: 18 Aug 2026 (re-fetched `www.verodus.com`, 44 HTML pages).** Locked FAQ four cards, Instant Best Day / Eligibility / JSON-LD, 1-Step Instant-name strip, home Instant blurb, FAQ Evaluation `p5`, Trading Objectives Instant modal, FAQ Qualified Trader 90/10 ladder, and TOS min-days / Instant-not-refundable **already match live**. Do not re-paste those unless a locale is still stale.

**Still leftover on live**
- Instant section still titled **Additional Qualified Performance Rules** (news body is Instant-correct). Prefer an Instant heading that does not say Qualified Performance.
- `refund-policy.html` is still blanket non-refundable (no eval first-reward / Instant split). TOS already has the split.
- `performance-reward.html` — **do not change** (still sells scale-to-90/10; leave as live).

**Contents**
1. [FAQ → Plans — four cards locked](#1-faq--plans-faq-planshtml--four-cards-locked)
2. [Instant page](#2-instant-page-instanthtml)
3. [1-Step page](#3-1-step-page-1-stephtml)
4. [2-Step Lite / Pro](#4-2-step-lite--pro-2-step-litehtml-2-step-prohtml)
5. [Trading Objectives](#5-trading-objectives-trading-objectiveshtml)
6. [Home](#6-home-indexhtml)
7. [FAQ → Evaluation](#7-faq--evaluation-faq-evaluationhtml)
8. [FAQ → Qualified Trader](#8-faq--qualified-trader-faq-qualified-traderhtml)
9. [Terms of Service](#9-terms-of-service-termshtml)
10. [Checkout](#10-checkout-checkouthtml)
11. [Already OK / do not change](#11-already-ok-on-the-18-aug-scan)

---

## Do not change

- `https://www.verodus.com/performance-reward.html` and `/locales/*/pages/performance-reward.json`. Scale-to-90/10 copy on that page stays.
- 1-Step Best Day **body** (50%, evaluation pass / 10% target). Do not rewrite it. Do not put Instant 20% on 1-Step.
- Instant leftover-prints / rec prices (do not reopen).
- News included on every plan. Weekend Holding stays a paid add-on.
- Weekly and On-Demand **cannot stack**. Checkout keeps `PAYOUT_ADDON_EXCLUSIVE`.
- Instant is **not refundable**. Eval first-reward refund = challenge fee only, not add-ons.
- Skip 0.5% / Valid Day / “qualifying days” / “green day” on Instant (and everywhere else).
- Do not name Instant on 1-Step.

---

## Locked product (for copy only)

| Plan | Daily DD | Max DD | Best Day | Min days | Sizes |
|---|---|---|---|---|---|
| Instant | 3% from that day’s equity high | 6% trail, **never locks** | **20%** of Positive Days’ Profit at payout request | **None** | $5k–$100k, **no $200k** |
| 1-Step | 4% from equity at 00:00 UTC | 6% hybrid, locks at initial balance | **50%** to pass and to get paid | **None** (eval and QPP) | $5k–$200k |
| 2-Step Lite | 4% | 8% static | — | Eval **5/phase**; QPP **3** | $5k–$200k |
| 2-Step Pro | 5% | 10% static | — | Eval **5/phase**; QPP **3** | $5k–$200k |

- **$100** on every reward cycle. Default **Bi-Weekly 80%**. 90% is the **On-Demand add-on only** (except on `performance-reward.html`, which you leave as live).
- Profitable days are factored into Positive Days’ Profit. Losing days do not count. Closed trades at 00:00 UTC.
- Coupon **VERO35**: 35% off `list + addon stickers`. Shopper pays 65%. Cap 35%.
- Checkout add-on % of list: Weekend **15%**, Weekly 70% **6%**, On Demand 90% **32% Instant / 15% evals**.

### Challenge rec (VERO35 sale / list)

| Plan | $5k | $10k | $25k | $50k | $100k | $200k |
|---|---|---|---|---|---|---|
| Instant | $49 / $75 | $69 / $106 | $149 / $229 | $239 / $368 | $439 / $675 | — |
| 1-Step | $45 / $69 | $69 / $106 | $129 / $198 | $219 / $337 | $379 / $583 | $699 / $1,075 |
| Lite | $39 / $60 | $55 / $85 | $115 / $177 | $169 / $260 | $309 / $475 | $599 / $922 |
| Pro | $45 / $69 | $59 / $91 | $125 / $192 | $199 / $306 | $349 / $537 | $699 / $1,075 |

---

## 1. FAQ → Plans (`faq-plans.html`) — four cards locked

These four cards are **locked**. **Live HTML now matches all four** (Instant `p7` no longer has the 0.5% filter). Paste only if a locale is behind.

Shared note under the cards can stay (news allowed on all four; Weekend still an add-on). Do **not** add 0.5% / Valid Day. Do **not** name Instant on the 1-Step card.

Locale: `locales/*/pages/faq-plans.json`

### Instant — `content.p7` (live now matches)

**Delete:** “A day only qualifies for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.”

```
No evaluation. You start on a funded simulated account. 3% daily drawdown from that day’s equity high (floating losses included). 6% trailing max drawdown that never locks at the starting balance. Best Day must be ≤20% of Positive Days’ Profit to get paid. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000; no $200,000 Instant account.
```

### 1-Step — `content.p1` (keep live)

```
One evaluation phase, then a Qualified Performance account. 10% profit target. 4% daily drawdown from equity at 00:00 UTC (floating losses included). 6% hybrid max drawdown: trails the account peak, then locks at the initial balance. Best Day must be ≤50% of Positive Days’ Profit to pass and to get paid. No minimum trading days in evaluation or Qualified Performance. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.
```

### 2-Step Lite — `content.p3` (keep live)

```
Two evaluation phases, then a Qualified Performance account. Phase I 8% profit target, Phase II 5%. 4% daily drawdown and 8% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.
```

### 2-Step Pro — `content.p5` (keep live)

```
Two evaluation phases, then a Qualified Performance account. Phase I 10% profit target, Phase II 5%. 5% daily drawdown and 10% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.
```

Locale: `locales/*/pages/faq-plans.json`

---

## 2. Instant page (`instant.html`)

### Hero `content.p3` (drop 0.5% / qualifying days)

```
Get instant access to a funded simulated account with no evaluation phases. 6% trailing max drawdown from equity high water mark (the trail never locks). 3% daily drawdown from that day’s equity high, as a fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC. 20% Best Day rule. No minimum trading days. These rules are binding and form part of the Trader Agreement.
```

### Overview — no min days

```
No Minimum Trading Days: There is no minimum number of trading days required. You may trade at your own pace.
```

Delete leftover “5 valid trading days” / “Minimum Trading Days: 5 Days.”

### JSON-LD / meta description (live now matches)

```
Instant access to a funded simulated account with no evaluation phases. 6% trailing max drawdown from equity high water mark (the trail never locks). 3% daily drawdown from that day’s equity high (fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC). 20% Best Day rule, and no minimum trading days. Sizes $5,000–$100,000.
```

### Heading

Live heading is **4. Payouts and Risk Limits** (`content.h24` and the TOC link). HTML comment may still say “risk limits.”

Do **not** add Every Payout, Intervals, or Performance Reward Split on Instant.

### 20% Best Day Rule (live 1-Step wording, Instant facts only)

Do **not** paste a rewritten “A Positive Day is a calendar day…” paragraph. Do **not** use 0.5% / qualifying days.

```
20% Best Day Rule

Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.

Rule: No single trading day can contribute more than 20% of your total Positive Days' Profit at the time you request a payout.

Not a Breach: Exceeding 20% on a single day does not immediately fail your account — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤20%.

Calculation: Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.
```

### Payout frequencies

```
Weekly (Selected Add-on): 70% to trader
Bi-Weekly (Default): 80% to trader
On-Demand (Selected Add-on): 90% to trader
Weekly and On-Demand are separate add-ons; they cannot both apply at once.
```

### Rewards & Payouts

```
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.

Fees: Instant fees are not refundable.
```

**Delete from Eligibility:** “qualifying days only: closed profit ≥ 0.5% of that day’s start-of-day equity” and any “5 valid trading days.”

### Instant modal

```
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit.
```

### News heading on Instant

```
Allowed: News trading is permitted. Expert Advisors (EAs), scripts, and custom indicators are permitted, subject to the restrictions in Section 6 – Restricted Trading Practices (no HFT, no mass-distributed/copy-trading EAs, no server hyperactivity, no arbitrage exploitation, etc.).
```

Locale: `locales/*/pages/instant.json`

---

## 3. 1-Step page (`1-step.html`)

**Keep live Best Day body.** Only strip Instant names.

### Hero `content.p3`

**Delete** `(Instant uses 20%)`.

```
Pass a single evaluation phase to qualify for a Qualified Performance account. 4% daily drawdown from equity at 00:00 UTC (floating losses included). 6% hybrid max drawdown (trails, then locks at initial balance). 50% Best Day rule. These rules are binding and form part of the Challenge Agreement.
```

### Max DD `content.li8`

**Delete** `Instant also trails, but Instant never locks.`

```
Maximum Overall Drawdown: 6% hybrid max drawdown — trailing from your account equity peak (locks at your initial balance when reached). Unique to this plan; see Section 3.
```

### Overview Best Day `content.li9`

**Delete** `(Instant uses 20%)`.

```
50% Best Day Rule: 50% Best Day rule — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.
```

### Keep live 1-Step Best Day body (do not rewrite)

```
50% Best Day Rule

Your single best profit day cannot account for more than 50% of your Positive Days' Profit at the time of passing the evaluation. This is not an immediate breach — you must continue trading until the condition is met.

Rule: No single trading day can contribute more than 50% of your total Positive Days' Profit at the point you hit the 10% target.

Not a Breach: Exceeding 50% on a single day does not immediately fail your evaluation — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤50%.

Calculation: Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.
```

### 1-Step Eligibility (if live still has a 3-day QPP min)

```
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.
```

Weekly / Bi-Weekly / On-Demand on 1-Step (no `$100` on these lines):

```
Weekly (Add-on): 7 calendar days and when eligibility requirements are met.
Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.
On-Demand (Add-on): Available when eligibility requirements are met.
```

Plus the exclusive line: `Weekly and On-Demand are separate add-ons; they cannot both apply at once.`

### News heading

Change **Allowed in Evaluation:** → **Allowed:** (same body as Instant news bullet above).

Locale: `locales/*/pages/1-step.json`

---

## 4. 2-Step Lite / Pro (`2-step-lite.html`, `2-step-pro.html`)

QPP language is already live. Rec pages: `landing/2-step-lite.html`, `landing/2-step-pro.html`.

If payout list still needs a paste:

```
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. The first payout and every payout after use this same rule. A trading day is a calendar day with at least one closed trade.

Weekly (Add-on): 7 calendar days, and 3 trading days.
Bi-Weekly (Standard): 14 calendar days, and 3 trading days.
On-Demand (Add-on): Available when eligibility requirements are met.
```

Change **Allowed in Evaluation:** → **Allowed:** News is permitted in every phase.

Do **not** put Instant 20% / 0.5% on these pages.

---

## 5. Trading Objectives (`trading-objectives.html`)

Rec: `landing/trading-objectives.html` and `landing/to-rec.js`.

Live Instant Best Day modal still appends 0.5% (“Days below this floor are ignored.”). **Delete that sentence.** Instant and 1-Step share this paragraph; only the percent changes (20 Instant / 50 1-Step):

```
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed X% of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤X% of total Positive Days' Profit.
```

Instant payout line (no 0.5%):

```
Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs).
```

1-Step: `$100` + 50% Best Day. 2-Step: `$100` + **3 trading days** (every payout).

Locale: `locales/*/pages/trading-objectives.json`

---

## 6. Home (`index.html`)

Live FAQ / JSON-LD still says Instant has “20% Best Day of **qualifying** Positive Days' Profit (closed profit ≥ **0.5%** …)”. Keep the 1-Step / 2-Step sentences in that answer.

**Replace Instant’s sentence** with the FAQ Instant card (§1), or:

```
No evaluation. Funded simulated account. 3% daily from that day’s equity high. 6% trail that never locks. Best Day ≤20% of Positive Days’ Profit to get paid. No minimum trading days. $100 every cycle. Default 80% (90% with On-Demand). $5k–$100k.
```

Locale: `locales/*/pages/index.json`

SERP (if meta still says “from $18” or leads with 90%):

```
Title: Verodus — Instant from $49. Funded on Day One.
Description: Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.
```

---

## 7. FAQ → Evaluation (`faq-evaluation.html`)

`content.p5` and JSON-LD: Instant still “qualifying days: closed profit ≥ 0.5% …”. Keep 1-Step / 2-Step. Full `p5`:

```
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days in evaluation or Qualified Performance. Best Day ≤50% of Positive Days' Profit. 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no minimum trading days and no profit target to “hit first”; you need $100, Best Day ≤20% of Positive Days' Profit, and the selected payout cycle.
```

**“How many trading days do I need for each program?”** — if Instant is missing from the list:

```
Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. All Positive Days count toward Positive Days’ Profit.
1-Step: No minimum trading days to pass evaluation. Qualified Performance has no minimum trading days. Best Day ≤50% of Positive Days’ Profit.
2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.
2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.
```

Locale: `locales/*/pages/faq-evaluation.json`

---

## 8. FAQ → Qualified Trader (`faq-qualified-trader.html`)

Keep `p3` (start 80/20). 18 Aug scan: `p9` / `p12` / `p28` already match — keep them:

**`p9` (keep):**

```
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: that plan’s payout rule and the selected cycle.
```

**`p12` (keep):**

```
Payout spacing is the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. Every cycle has a $100 minimum. Instant and 1-Step have no minimum trading days. 2-Step Qualified Performance needs 3 trading days on every payout. First and later payouts use the same rule.
```

**Delete** the performance split ladder (“After 6 consecutive profitable months … your split increases to 90/10”). **Do not** send people to rewrite `performance-reward.html`.

```
Default split is 80%. 90% is available only with the On-Demand add-on. Weekly and On-Demand cannot both apply at once. There is no performance scale to 90/10.
```

`content.p4` — drop “permanent increase to your profit share” as a consistency upgrade. Same rule as the line above.

`content.p5` — drop “Once you reach the 85/15 tier, capital scaling is unlocked.” Do not sell scaling off an 85/15 or 90/10 rewards-tier climb.

If `p13` Instant still has Valid Day / 0.5%:

```
On Instant: no minimum trading days; Best Day ≤20% of Positive Days’ Profit
On 1-Step Qualified Performance: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit
On 2-Step Lite / Pro Qualified Performance: 3 trading days
```

`content.p28` (if live still refunds Instant):

```
Yes, on 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Add-ons are not refunded if they were purchased (Weekend Holding, Weekly, On-Demand, or any other add-on). Instant has no challenge-fee refund.
```

Locale: `locales/*/pages/faq-qualified-trader.json`

---

## 9. Terms of Service (`terms.html`)

**`li4` live:** “A minimum number of Trading Days is required both during the evaluation phases and before/between Performance Rewards.”

**Rec:** Keep “Requirements vary by model.” **Delete** the site-wide min-days sentence. Do not add a plan-by-plan day-count line.

**First-reward note live:** “A successful first Performance Reward includes a 100% refund of your original challenge fee.” No Instant exception, add-ons not excluded.

```
On 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Add-ons are not refunded. Instant fees are not refundable.
```

Locale: `locales/*/pages/terms.json`

---

## 10. Checkout (`checkout.html`)

Already aligned on the 18 Aug scan (no 0.5% / stack needles). Keep:

- `PAYOUT_ADDON_EXCLUSIVE = { 'weekly-payout': 1, 'on-demand-payout': 1 }`
- Weekend 15%, Weekly 6%, On Demand 32% Instant / 15% evals
- Rec drop-in if fees still need a full replace: `landing/checkout.html`

---

## 11. Already OK on the 18 Aug afternoon rescan

- FAQ news (`faq-news-trading.html`), FAQ hub (`faq.html`), `restricted-trading.html`
- 2-Step Lite / Pro plan pages (QPP wording)
- FAQ Plans 1-Step / Lite / Pro cards
- FAQ Qualified Trader payout `$100` / Instant no min days / Instant no fee refund (`p9`, `p12`, `p28`) if those keys still match §8
- `performance-reward.html` — **leave as live on purpose**

---

## Locales checklist

| File | Action |
|------|--------|
| `faq-plans.json` | Four locked cards |
| `instant.json` | Best Day + Eligibility + Fees + heading + JSON-LD; no 0.5% |
| `1-step.json` | Drop Instant 20% / Instant never locks |
| `2-step-lite.json` / `2-step-pro.json` | Allowed: (not “in Evaluation”) if still eval-only |
| `index.json` | Instant blurb without 0.5%; SERP if needed |
| `faq-evaluation.json` | Instant sentence without 0.5% |
| `trading-objectives.json` | Instant modal without 0.5% |
| `faq-qualified-trader.json` | No leftover 90/10 / 85/15 split ladder |
| `terms.json` | Drop site-wide min days; Instant not refundable |
| `performance-reward.json` | **Do not change** |

Then the other nine locale folders.
