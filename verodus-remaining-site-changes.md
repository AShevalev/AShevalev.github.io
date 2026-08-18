# Verodus remaining site changes

Live scan 18 Aug 2026. Only items still wrong on `https://www.verodus.com/`. Do not re-paste rules that already landed.

**Locked Instant / 1-Step Best Day:** same Positive Day definition. Instant cap **20%**. 1-Step cap **50%**. **No 0.5% / Valid Day** on Instant. Do not write “green day” or “profitable day.”

**Already on live (do not redo):** news included / **Allowed:** heading; no min holding time; Instant no listed min days and no “5 valid days”; Instant 6% trail never locks; Instant no `$200k`; Instant fees not refundable on the Instant page; 1-Step no min days + 50% Best Day; 2-Step 5 eval days / 3 QPP days; `$100` every cycle; same first and later payouts; 4-then-3 gone; Trading Objectives Instant payout line already short (`$100`, no min days, Best Day ≤20%, no 0.5%); checkout On-Demand already “when eligibility requirements are met.”

Apply HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`. English locale JSON currently carries the same Instant PDP error as the HTML.

---

## 1. Instant Best Day — every Positive Day is in Positive Days’ Profit (no 0.5%)

Live still treats 0.5% as a **Positive Days’ Profit filter**. Small days in profit are dropped. That is the Instant rule that is still wrong. Do not replace it with a Valid Day sentence. **Skip 0.5% entirely.**

**Names**
- **Positive Day** = a calendar day that **closes in profit** (including a small +0.1% day). That is the unit of **Positive Days’ Profit** and Best Day. Use this, not “green day.”
- Instant has **no** Valid Day and **no** 0.5% line. 1-Step uses the same Positive Day definition at **50%**.

**Locked Instant rule**
- Best Day ≤20% of **Positive Days’ Profit**.
- **All Positive Days** count, including small days.
- Losing days do not count toward Positive Days’ Profit.
- Never write “green day,” “qualifying days only,” “days below this floor are ignored,” or Valid Day.

### `instant.html`

| Key / spot | Live (wrong) | Change to |
|---|---|---|
| `content.p8` | “A day counts only when closed profit is at least 0.5% … **Smaller green days do not count**” | Paste below. |
| `content.li12` | “Best Day must be ≤20% of Positive Days' Profit **(qualifying days only)**.” | Best Day must be ≤20% of Positive Days’ Profit. All Positive Days count. |
| `content.li14` | “Days under the 0.5% … **do not count**.” | Closed trades at 00:00 UTC. Losing days do not count toward Positive Days’ Profit. |
| Eligibility | “**qualifying days only:** closed profit ≥ 0.5%” | `$100` + Best Day ≤20% + cycle. No min days. No 0.5%. |
| `#bestDayModal` | “Days below this floor are ignored” | Paste below. |
| JSON-LD | “20% Best Day of **qualifying days**” | 20% Best Day of Positive Days’ Profit. All Positive Days count. No min trading days. |

**Instant Best Day paste** (`p8` + modal) — same wording as 1-Step, 20% not 50%

```text
Your Best Day (highest profit calendar day) must not exceed 20% of Positive Days’ Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days’ Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 20% is not a breach — continue trading until Best Day is ≤20%.
```

**Instant Eligibility paste** — same wording as 1-Step, 20% not 50%

```text
You are eligible when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and the selected cycle is complete. No minimum trading days required. The same rule applies to every payout.
```

Do **not** keep:

> Smaller green days do not count toward Best Day or Positive Days’ Profit.

> Days below this floor are ignored.

> qualifying days only

> Valid Day / 0.5%

### 1-Step — same Positive Day definition at 50%

**1-Step Best Day paste** — same wording as Instant, 50% not 20%. Do not name Instant.

```text
Your Best Day (highest profit calendar day) must not exceed 50% of Positive Days’ Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days’ Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding 50% is not a breach — continue trading until Best Day is ≤50%.
```

**1-Step Eligibility paste**

```text
You are eligible when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and the selected cycle is complete. No minimum trading days required. The same rule applies to every payout.
```

Do not put Instant 20% or 0.5% on 1-Step. Drop “unique to 1-Step” on the Best Day heading (hybrid 6% lock can stay unique).

### `trading-objectives.html` Instant / 1-Step Best Day modal

Use **one paragraph**. Instant is 20%. 1-Step is 50%. Do not name Instant on the 1-Step tab. Do not add a 0.5% sentence.

```text
The Best Day Rule requires that your Best Day (highest profit calendar day) does not exceed X% of Positive Days' Profit. A Positive Day is a calendar day that closes in profit. All Positive Days count toward Positive Days' Profit. Losing days do not count toward Positive Days' Profit. Profits are calculated from closed trades at 00:00 UTC. Exceeding X% is not a breach — continue trading until Best Day is ≤X%.
```

### FAQs that still copy the Instant PDP filter

**`faq-plans.html` Instant card (`content.p7`)** live:

> A day **only qualifies** for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.

**`faq-plans.html` Instant card (`content.p7`)** — same skeleton as the 1-Step card. Instant rules only: no eval, 3%/6% trail never locks, **20%** Best Day, no `$200k`. Drop the 0.5% “only qualifies” sentence. Do not name 1-Step on Instant.

**Paste** (1-Step `p1` with Instant-applicable rules and 20% in place of 50%)

```text
No evaluation. You start on a funded simulated account. 3% daily drawdown from that day’s equity high, as a fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC. 6% trailing max drawdown from equity high water mark (the trail never locks). Best Day must be ≤20% of Positive Days’ Profit to get paid. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000.
```

Keep the 1-Step card as live (`content.p1`). Do not add Instant 20% to that card.

**1-Step `p1` (keep — do not name Instant)**

```text
One evaluation phase, then a Qualified Performance account. 10% profit target. 4% daily drawdown from equity at 00:00 UTC (floating losses included). 6% hybrid max drawdown: trails the account peak, then locks at the initial balance. Best Day must be ≤50% of Positive Days’ Profit to pass and to get paid. No minimum trading days in evaluation or Qualified Performance. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.
```

**`faq-evaluation.html`** live list + `p5` still say “qualifying days: closed profit ≥ 0.5% of SOD.”

**List paste**

```html
<ul>
  <li>Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. A Positive Day is a calendar day that closes in profit. Every Positive Day is included.</li>
  <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance has no minimum trading days. Best Day ≤50% of Positive Days’ Profit.</li>
  <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
  <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

**`p5` paste** — drop Instant “qualifying days.” Instant needs `$100`, Best Day ≤20% of Positive Days’ Profit, and the cycle. 1-Step / 2-Step sentences on that answer can stay.

JSON-LD on `faq-evaluation.html` repeats the same Instant qualifying-days line. Update it with the list.

---

## 2. Weekly 70% and On Demand 90% cannot stack

**Correct rule:** Weekly and On-Demand are separate add-ons; they cannot both apply at once. Weekend stays a separate paid add-on. Default remains Bi-Weekly 80%.

Keep this live bullet on Instant, 1-Step, Lite, and Pro (`instant` `li20`, `1-step` `li18`, Lite/Pro `li15`):

```text
Weekly and On-Demand are separate add-ons; they cannot both apply at once.
```

Do **not** write that they may stack or may be purchased together.

**Checkout** `checkout.html` must keep:

```javascript
var PAYOUT_ADDON_EXCLUSIVE = { 'weekly-payout': 1, 'on-demand-payout': 1 };
```

Selecting Weekly clears On Demand, and selecting On Demand clears Weekly.

---

## 3. Terms of Service

### §8(b) trading days — not every model

**Live `content.li4`**

> A **minimum number of Trading Days is required** both during the evaluation phases and before/between Performance Rewards.

That is false for Instant and 1-Step.

**Paste**

```text
Requirements vary by model and are fully detailed on the linked pages above.
```

Keep the existing “Requirements vary by model” sentence (`p41`). Do not keep a site-wide min-days bullet.

### §8(a) first-reward refund — Instant exception

**Live `content.p40`**

> A successful first Performance Reward includes a 100% refund of your original challenge fee.

No Instant exception. Plan pages already say Instant is not refundable.

**Paste** (end of that note)

```text
On 1-Step, 2-Step Lite, and 2-Step Pro, a successful first Performance Reward includes a 100% refund of the original challenge fee. Add-ons are not refunded. Instant has no challenge-fee refund.
```

---

## 4. Do not name Instant on 1-Step

**Live** on `1-step.html` hero (`p3`), Best Day heading, and `li9` / `span7`:

> 50% Best Day rule **(Instant uses 20%)**

Drop the Instant clause. 1-Step is 50% of Positive Days’ Profit only. Do not mention Instant or 0.5% on 1-Step.

**Paste**

```text
50% Best Day rule — your Best Day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.
```

---

## 5. Leftover locale keys (not visible, can come back)

These English keys are unused in the current HTML but still hold old copy. Clear or rewrite them in every locale so a later bind does not restore them.

| Page | Key | Live leftover |
|---|---|---|
| Instant | `span49` / `span51` | Weekly / Bi-Weekly “starting from the day you receive your Qualified Performance Account” |
| Instant | `span53` | On-Demand “minimum number of trading days for that evaluation. On-demand does not skip…” |
| Instant | `li10` / `span21` | Duplicate “Minimum Trading Days: No minimum trading days.” Instant HTML already dropped this bullet. |
| Instant | `span19` | 2-Step-style “open and close on that calendar day” under Instant no-min-days |
| 1-Step | `span20` / `span21` | Weekly / Bi-Weekly from QPP account |
| 1-Step | `span23` | Refund sentence with no add-on exception (`li27` already has the add-on line) |
| Lite / Pro | `span16` / `span17` | Weekly / Bi-Weekly from QPP account |

---

## Not in this list on purpose

- Changing `at least 0.5%` / `≥ 0.5%` to “more than.”
- Re-adding Instant “5 valid days” or a listed Instant day-count.
- Putting Instant 20% or 0.5% on 1-Step or 2-Step.
- Letting Weekly and On Demand stack.
- Re-splitting first vs later payouts.
- News, holding time, Instant trail, Instant `$200k`, Instant not-refundable on the Instant page, 2-Step 5/3, `$100`, Trading Objectives Instant short payout line.
