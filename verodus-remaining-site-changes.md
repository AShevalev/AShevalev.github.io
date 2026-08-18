# Remaining live-site copy — paste list

**Scan:** 18 Aug 2026 (re-fetched live `www.verodus.com` this pass).  
**Repo rec HTML** (`landing/*.html`) already matches these Instant / 1-Step / 2-Step rules. This file is what still has to change **on the live site + locales**.

**This scan’s still-wrong pages:** Instant FAQ card `p7` (0.5%), Instant page Best Day / Eligibility / JSON-LD / heading case, 1-Step Instant-name asides, index Instant FAQ blurb, FAQ Evaluation Instant 0.5%, Trading Objectives Instant modal, performance-reward scale-to-90/10, FAQ Qualified Trader leftover 90/10 + 85/15 scale, TOS site-wide min days + first-reward refund with no Instant exception.

**Already OK on this scan:** 1-Step / Lite / Pro FAQ-plans cards; checkout exclusive add-ons; FAQ news / FAQ hub / restricted-trading; 2-Step Lite / Pro plan pages (QPP language). FAQ Qualified Trader payout `$100` / Instant no min days / Instant no fee refund (`p9`, `p12`, `p28`) already match rec.

**Do not reopen:** Instant leftover-prints at rec prices. Skip 0.5% / Valid Day on Instant. Do not name Instant on 1-Step. Weekly and On-Demand cannot stack. Instant is not refundable. Default split 80%; 90% is the On-Demand add-on only — **no performance scale to 90/10**.

**After every HTML paste:** the same string in `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`. English JSON currently matches the live HTML errors (Instant 0.5%, Instant-on-1-Step, scale-to-90/10).

---

## Locked: FAQ → Plans (`faq-plans.html`)

Replace the four program cards. Shared note under the cards can stay (news allowed on all four; Weekend still an add-on).

### Instant — `content.p7` (live is wrong — still 0.5%)

**Live (do not keep):** “A day only qualifies for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.” Instant has no $200,000 size — keep that.

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

---

## 1. Instant Best Day — still the main Instant page hole

Live Instant still uses a **0.5% qualifying-days filter**. Rec Instant Best Day is live **1-Step wording** with Instant facts only (20%, payout request, fail your account). Do **not** paste the rewritten “A Positive Day is a calendar day…” paragraph.

**Canonical Instant paste** (also `landing/instant.html`):

```
20% Best Day Rule

Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.

Rule: No single trading day can contribute more than 20% of your total Positive Days' Profit at the time you request a payout.

Not a Breach: Exceeding 20% on a single day does not immediately fail your account — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤20%.

Calculation: Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.
```

**Live Eligibility (do not keep):** “Best Day is ≤20% of Positive Days’ Profit (qualifying days only: closed profit ≥ 0.5% of that day’s start-of-day equity)”

**Eligibility** (drop qualifying-days / 0.5% / “5 valid trading days”):

```
You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.
```

**Instant / 1-Step modal** (`trading-objectives.html` + Instant/1-Step pages). X = **20 Instant / 50 1-Step**. Live Instant modal still appends 0.5%. 1-Step modal body can stay.

```
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed X% of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤X% of total Positive Days' Profit.
```

1-Step page Best Day body stays **live 1-Step** (50%, evaluation pass / 10% target). Do not rewrite it. Do **not** put Instant 20% on the 1-Step page.

**Live Instant heading:** “4. Payouts and **risk** limits” → **4. Payouts and Risk Limits**. Frequencies: Weekly (Selected Add-on), Bi-Weekly (Default), On-Demand (Selected Add-on), plus “Weekly and On-Demand are separate add-ons; they cannot both apply at once.” Rewards card: **Fees:** (not Refund). Do not add Every Payout / Intervals / Performance Reward Split on Instant.

JSON-LD on Instant still repeats 0.5% — replace when HTML is pasted.

---

## 2. 1-Step page — Instant name still on the live page

Live `1-step.html`:

| Key | Live (remove) |
|-----|----------------|
| `hero.p3` | `(Instant uses 20%)` |
| Best Day `li9` | `(Instant uses 20%)` |
| Max DD `li8` | `Instant also trails, but Instant never locks.` |

Paste Instant-free versions from `landing/1-step.html` (hero p3, Best Day block, max DD li8 without Instant).

---

## 3. Home Instant blurb — `index.html`

Live home FAQ / JSON-LD still says Instant has “20% Best Day of **qualifying** Positive Days' Profit (closed profit ≥ **0.5%** of that day's start-of-day equity)”. 1-Step / 2-Step sentences in that same answer can stay.

Replace Instant’s home blurb with the FAQ Instant card (section “Locked: FAQ → Plans” above), or this short form:

```
No evaluation. Funded simulated account. 3% daily from that day’s equity high. 6% trail that never locks. Best Day ≤20% of Positive Days’ Profit to get paid. No minimum trading days. $100 every cycle. Default 80% (90% with On-Demand). $5k–$100k.
```

---

## 4. FAQ → Evaluation — Instant sentence only

`faq-evaluation.html` `content.p5` (and JSON-LD): Instant still “qualifying days: closed profit ≥ 0.5% of that day’s start-of-day equity.”

**Keep** the 1-Step / 2-Step sentences. Full paste for `p5` (Instant sentence cleaned):

```
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days in evaluation or Qualified Performance. Best Day ≤50% of Positive Days' Profit. 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no minimum trading days and no profit target to “hit first”; you need $100, Best Day ≤20% of Positive Days' Profit, and the selected payout cycle.
```

---

## 5. Performance reward — still sells scale-to-90/10

Live `performance-reward.html` still has **Start at 80/20, scale to 90/10** (`h31`, `h32`) and **85/15 capital scaling** (`p5`). Rec: default **80%**; **90% only with On-Demand add-on**; **no** performance scale ladder.

Replace those headings/body with:

```
Default split is 80%. 90% is available only with the On-Demand add-on. Weekly and On-Demand cannot both apply at once. There is no performance scale to 90/10.
```

`$100` minimum (`p12`) can stay.

---

## 6. FAQ → Qualified Trader — leftover 90/10 + 85/15 scale

Visible split line (`p3`) already says start **80/20**. Live leftovers:

| Live | Rec |
|------|-----|
| List item: “After 6 consecutive profitable months … your split increases to **90/10**” | Delete the performance scale ladder. 90% is the On-Demand add-on only. |
| `p5`: “Once you reach the **85/15** tier, capital scaling is unlocked.” | No 85/15 split ladder. Do not sell capital scaling off a rewards-tier climb. |
| `p4`: “permanent increase to your profit share” | Drop or rewrite so 90% is On-Demand, not a consistency upgrade. |

Payout `$100` / 3-day QPP / Instant no min days / first-reward refund **evals only** (`p9`, `p12`, `p28`) already match rec.

---

## 7. Terms of Service

Live `li4`: “A minimum number of Trading Days is required both during the evaluation phases and before/between Performance Rewards.” That is false for Instant and 1-Step.

Live first-reward note: “A successful first Performance Reward includes a 100% refund of your original challenge fee.” No Instant exception, and it does not say add-ons are excluded.

| Live | Rec |
|------|-----|
| Site-wide min trading days (`li4`) | Instant and 1-Step have **no** min days. 2-Step eval **5 days/phase**. 2-Step QPP **3 days**. |
| First-reward challenge-fee refund, no Instant exception | Instant is **not refundable**. Eval first-reward refund = **challenge fee only**, not add-ons. |

---

## 8. Checkout, news, restricted trading — already aligned on this scan

- `checkout.html`: no 0.5% / stack needles. Keep `PAYOUT_ADDON_EXCLUSIVE`. Add-on %: Weekend 15%, Weekly 6%, On Demand 32% Instant / 15% evals.
- `faq-news-trading.html`, `faq.html`, `restricted-trading.html`: news included; Weekend still an add-on. No Instant 0.5% on this scan.

---

## 9. 2-Step Lite / Pro plan pages

Live already uses Qualified Performance (not Instant). Rec pages in `landing/2-step-lite.html` and `landing/2-step-pro.html` if you want the payout-list wording from stitch. Not a 0.5% / Instant-name hole.

---

## Locales (same strings as HTML)

| File | What to match |
|------|----------------|
| `locales/en/pages/faq-plans.json` | Four locked cards above |
| `locales/en/pages/instant.json` | Instant Best Day + Eligibility + Fees + heading |
| `locales/en/pages/1-step.json` | Drop Instant 20% / Instant never locks |
| `locales/en/pages/index.json` | Instant home blurb without 0.5% |
| `locales/en/pages/faq-evaluation.json` | Instant sentence without 0.5% |
| `locales/en/pages/trading-objectives.json` | Instant modal without 0.5% |
| `locales/en/pages/performance-reward.json` | No scale-to-90/10 |
| `locales/en/pages/faq-qualified-trader.json` | No leftover 90/10 scale |
| `locales/en/pages/terms.json` | Min days + Instant not refundable |

Then the other nine locale folders.

---

## Rec HTML already in this repo

`landing/instant.html`, `landing/1-step.html`, `landing/2-step-lite.html`, `landing/2-step-pro.html`, `landing/trading-objectives.html`. Standalone Instant preview: `landing/instant-preview.html`.
