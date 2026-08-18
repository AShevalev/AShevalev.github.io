# Verodus live copy scan — 18 Aug 2026

Scanned `https://www.verodus.com/` plan pages, Trading Objectives, FAQ Plans, FAQ Qualified Trader, FAQ Evaluation, and Performance Reward.

This note is the correction list for the **next site paste**. Rec HTML in this repo already follows the Rewards paste below. Live does not.

Never write “green day” or “0.5% parameter.” Use **profitable day** and **Positive Days’ Profit**. Instant 0.5% belongs on the Instant Best Day modal only.

---

## Paste for plan Rewards & Payouts (this pass)

`$100` stays on **Minimum Reward** and **Eligibility**. Do not repeat `$100` on Weekly, Bi-Weekly, or On-Demand.

On-Demand is the **same line on every plan page**. Do not paste Instant / 1-Step / 2-Step On-Demand variants onto each page.

```text
On-Demand (Add-on): Available when eligibility requirements are met.
```

Do **not** put these on Instant.html / 1-step.html / 2-step-*.html:

```text
Instant: On-demand: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. A profitable day is a day that closes with at least 0.5% profit.
1-Step: On-demand: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit.
2-Step Lite / Pro: On-demand: $100 and 3 trading days.
```

### Instant

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. A Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). Valid Day is not a minimum trading-day count and does not remove small Positive Days from Positive Days’ Profit. Instant has no minimum trading days. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.
```

### 1-Step

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.
```

### 2-Step Lite / Pro

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. The first payout and every payout after use this same rule. A trading day is a calendar day with at least one closed trade.

Weekly (Add-on): 7 calendar days, and 3 trading days.

Bi-Weekly (Standard): 14 calendar days, and 3 trading days.

On-Demand (Add-on): Available when eligibility requirements are met.
```

Do not dump Weekly / Bi-Weekly / On-Demand into Eligibility. Frequencies = split + clock. Split card = 80% included; 70% and 90% may stack. Rewards = checklist.

---

## Already on live (keep)

| Item | Live |
|---|---|
| Instant no min trading days | Card shows **N/A**. Overview says no min days. **5 valid days is gone.** |
| Instant / 1-Step / 2-Step same first and later payout | Eligibility says first and later use the same rule. The old 4-then-3 split is gone. |
| Instant Eligibility has `$100` + 20% Best Day + cycle | Yes, but still dumps Weekly / Bi-Weekly / On-Demand into the same bullet and still says “green day” / “0.5% parameter.” |
| 1-Step Eligibility has `$100` + 50% Best Day + no min days | Yes, same dump + “green day.” |
| 2-Step QPP **3 trading days** + `$100` | Yes. Eval still **5 days per phase** (correct). |
| 2-Step duplicate On-Demand (“does not skip” + `$100 and 3 trading days`) | **Gone.** One On-Demand line remains: `$100 and 3 trading days.` Shorten it to “when eligibility requirements are met.” |
| **Allowed:** heading (was “Allowed in Evaluation”) | **Done** on Instant, 1-Step, Lite, Pro. |
| News included / no news add-on | Plan news lines and FAQ Plans already say news is included. |
| Instant sizes `$5k–$100k` (no `$200k`) | FAQ Plans Instant card says no `$200,000`. |
| FAQ Qualified Trader payout spacing | Cycle-based. Instant / 1-Step no min days. 2-Step QPP 3 days. |
| Challenge fee refund = evals only | FAQ Qualified Trader: Instant has no challenge-fee refund; add-ons are not refunded. Plan pages still use the older “full refund” sentence (see below). |

---

## Still wrong on live — paste these

### 1. Plan Rewards FAQs are redundant

Live Eligibility **dumps** Weekly / Bi-Weekly / On-Demand into one paragraph, then repeats Weekly / Bi-Weekly / On-Demand as separate bullets, then Frequencies and Split list the same three cycles again.

**Do:** Eligibility short. Weekly / Bi-Weekly = clock + Best Day (or 2-Step 3 days). On-Demand = available when eligibility requirements are met. **No `$100` on those three bullets.**

Live Weekly / Bi-Weekly still say “starting from the day you receive your Qualified Performance Account.” Instant is funded from day one — never say QPP account. 1-Step / 2-Step Weekly / Bi-Weekly should name Best Day / 3 trading days, not “after QPP account.”

### 2. “green day” and “0.5% parameter”

Still on Instant Best Day block + modal, Instant Eligibility, Instant On-Demand, Instant “Every Payout” card, 1-Step Best Day + Eligibility + On-Demand, FAQ Plans, FAQ Evaluation, FAQ Qualified Trader, Trading Objectives Instant / 1-Step payout lines and Best Day modal JS.

**Replace “green day” with “profitable day.”** Drop “0.5% parameter.” Instant modal only: **a profitable day is a day that closes with at least 0.5% profit (≥ 0.5%).** Do not write “more than 0.5%.” Do not put 0.5% on 1-Step or 2-Step. Do not put 0.5% on Instant Eligibility, Weekly, Bi-Weekly, On-Demand, or the short Trading Objectives Instant payout line.

### 3. Instant leftover that contradicts no-min-days

- Min-days stat is **N/A** — use **None**.
- `li9` still defines a 2-Step-style trading day (open and close the same UTC day) even though Instant has no min days.
- Section 3 **Every Payout** card duplicates Eligibility (`$100`, Best Day, cycle, 48 business hours).
- Trail copy does **not** say **never locks**.
- Processing: **48 business hours** → **48 hours** (all plans).

### 4. Split / 90% leftover (all four plan pages)

Still live:

- Frequencies: “80% to trader (can scale according to performance plan)”
- Split: Scales to 85/15 and 90/10
- Hero: “keep up to 90% of performance rewards”
- FAQ Plans 1-Step: “80/20 profit split that scales to 90/10”

**90% is a paid On-Demand add-on.** Default is Bi-Weekly **80%**. Weekly **70%** and On-Demand **90%** may stack.

### 5. Eval refund sentence on plan pages

Live: “You receive a full refund of your original challenge fee with your first successful performance reward.”

**Paste:** The original challenge fee is refunded with the first successful performance reward. Add-on fees are not refunded. Instant: Instant fees are not refundable.

### 6. Hub FAQs still blend Instant 0.5% into every-plan answers

`faq-qualified-trader.html` `p9` still lists Instant / 1-Step / 2-Step On-Demand in one paragraph, then repeats `$100` on Weekly and Bi-Weekly. Hub list should be:

```text
Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle
Weekly: 7 calendar days (plus Eligibility)
Bi-weekly: 14 calendar days (plus Eligibility)
On-demand: available when eligibility requirements are met
```

Plan Eligibility stays on the plan page. Do not re-paste Instant 0.5% into hub On-Demand.

### 7. Trading Objectives

Live Instant `p8Instant` still has green day + 0.5% parameter. Short Instant line:

```text
Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs)
```

1-Step `p8OneStep`: drop green day; no 0.5%. 2-Step `p8` (`$100` and 3 trading days) is already right. On-Demand card can say “Anytime” / available when eligibility is met — do not repeat `$100` on that card if the payout highlight already has it.

### 8. Locales

Live HTML still uses `data-i18n` keys. `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` are **not in this repo**. After HTML paste, the same strings must go into locale JSON or Weglot will put “green day” / “0.5% parameter” / “scales to 90/10” back on translated pages.

---

## Not a copy bug (leave)

- Instant 3% daily from the day’s equity high, 6% trail (add “never locks” only).
- 1-Step 10% target, 50% Best Day, hybrid 6% that **does** lock, 4% daily.
- Lite 4%/8% static. Pro 5%/10% static. 2-Step eval 5 days per phase.
- Weekend Holding Addon. News bracketing / gap bans in §6.
- `$200k` sizes on 1-Step / Lite / Pro.

---

## Rec repo vs live

This repo’s `landing/instant.html`, `1-step.html`, `2-step-lite.html`, `2-step-pro.html` already use the Rewards paste above (Eligibility has `$100`; cycles do not; On-Demand is “when eligibility requirements are met”). Live still has the dump Eligibility + green day + scale-to-90% split. Paste from this scan onto live, then locales.
