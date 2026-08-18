# Verodus remaining site changes

Live scan 18 Aug 2026. Only items still wrong on `https://www.verodus.com/`. Do not re-paste rules that already landed.

**Keep Instant headings.** Do not rename Instant section 4 to “Payouts and risk limits.” Instant stays **4. Qualified Performance Phase**. Keep **20% Best Day Rule**, **Rule**, **Not a Breach**, **Calculation**, **Every Payout**. Only the body copy uses live 1-Step wording.

**Locked Instant Best Day:** use **live 1-Step wording**, Instant-applicable only. Cap **20%**. Payout request, not evaluation pass. Instant has no 10% target. **No 0.5% / Valid Day / qualifying days.** 1-Step stays **live** at **50%**. Do not name Instant on 1-Step. Live 1-Step Calculation (“Profitable days are factored into Positive Days' Profit”) is the Instant Calculation too.

**Already on live (do not redo):** news included / **Allowed:** heading; no min holding time; Instant no listed min days and no “5 valid days”; Instant 6% trail never locks; Instant no `$200k`; Instant fees not refundable on the Instant page; 1-Step no min days + 50% Best Day; 2-Step 5 eval days / 3 QPP days; `$100` every cycle; same first and later payouts; 4-then-3 gone; Trading Objectives Instant payout line already short (`$100`, no min days, Best Day ≤20%, no 0.5%); checkout On-Demand already “when eligibility requirements are met.”

Apply HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`. English locale JSON currently carries the same Instant PDP error as the HTML.

---

## 1. Instant Best Day — live 1-Step wording at 20% (no 0.5%)

Live Instant still treats 0.5% as a **Positive Days’ Profit filter**. Small days in profit are dropped. That is the Instant rule that is still wrong. Do not replace it with a Valid Day sentence. **Skip 0.5% entirely.** Paste live 1-Step Best Day / Eligibility / modal, with Instant swaps only.

**Instant-applicable swaps from live 1-Step**
- 50% → **20%**
- “at the time of passing the evaluation” → **“at the time you request a payout”**
- “at the point you hit the 10% target” → **“at the time you request a payout”**
- “fail your evaluation” → **“fail your account”**
- “1-Step has no minimum trading days” → **“Instant has no minimum trading days”**
- Do **not** keep “A Positive Day is a calendar day…” — live 1-Step does not use that paragraph.

### `instant.html`

| Key / spot | Live (wrong) | Change to |
|---|---|---|
| `content.p8` | “A day counts only when closed profit is at least 0.5% … **Smaller green days do not count**” | Live 1-Step `p7`, 20%, payout request. |
| `content.li12` | “Best Day must be ≤20% of Positive Days' Profit **(qualifying days only)**.” | Live 1-Step Rule at 20%, payout request. |
| `content.li13` | “does not immediately **terminate** your account” | Live 1-Step Not a Breach: **fail your account**, ≤20%. |
| `content.li14` | “Days under the 0.5% … **do not count**.” | Live 1-Step Calculation. |
| Eligibility | “**qualifying days only:** closed profit ≥ 0.5%” | Live 1-Step Eligibility, Instant, 20%. |
| `#bestDayModal` | “Days below this floor are ignored” | Live 1-Step modal, 20%. |
| JSON-LD | “20% Best Day of **qualifying days**” | 20% Best Day rule, and no minimum trading days. |

**Instant Best Day paste** (`p8` + rule cards) — live 1-Step wording under Instant headings

```text
20% Best Day Rule

Your single best profit day cannot account for more than 20% of your Positive Days' Profit at the time you request a payout. This is not an immediate breach — you must continue trading until the condition is met.

Rule: No single trading day can contribute more than 20% of your total Positive Days' Profit at the time you request a payout.

Not a Breach: Exceeding 20% on a single day does not immediately fail your account — you must simply keep trading to grow your total Positive Days' Profit until the Best Day drops to ≤20%.

Calculation: Profits are measured from closed trades at the end of each trading day (00:00 UTC). Profitable days are factored into Positive Days' Profit. Losing days do not count.

Every Payout: Minimum $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle. No minimum trading days required. The same rule applies to every payout. Processed within 48 hours.
```

**Instant Eligibility paste** — live 1-Step Eligibility, Instant-applicable

```text
You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.
```

**Instant modal paste** — live 1-Step modal, 20%

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit.
```

Do **not** keep:

> Smaller green days do not count toward Best Day or Positive Days’ Profit.

> Days below this floor are ignored.

> qualifying days only

> Valid Day / 0.5%

> A Positive Day is a calendar day that closes in profit. All Positive Days count…

### 1-Step — keep live wording at 50%

Do **not** rewrite 1-Step Best Day, Rule, Not a Breach, Calculation, Eligibility, or modal. Keep live. Drop “Instant uses 20%” only.

**1-Step `p7` (keep)**

```text
Your single best profit day cannot account for more than 50% of your Positive Days' Profit at the time of passing the evaluation. This is not an immediate breach — you must continue trading until the condition is met.
```

**1-Step Eligibility (keep)**

```text
You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.
```

Do not put Instant 20% or 0.5% on 1-Step. Drop “unique to 1-Step” on the Best Day heading (hybrid 6% lock can stay unique).

### `trading-objectives.html` Instant / 1-Step Best Day modal

Use the **live 1-Step modal paragraph**. Instant is 20%. 1-Step is 50%. Do not name Instant on the 1-Step tab. Do not add a 0.5% sentence. Do not add “A Positive Day is a calendar day…”.

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed X% of your Positive Days' Profit on the account. Profitable days are factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤X% of total Positive Days' Profit.
```

### FAQs that still copy the Instant PDP filter

**`faq-plans.html` Instant card (`content.p7`)** live:

> A day **only qualifies** for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.

**`faq-plans.html` Instant card (`content.p7`)** — same skeleton as the 1-Step card. Instant rules only: no eval, 3%/6% trail never locks, **20%** Best Day, no `$200k`. Drop the 0.5% “only qualifies” sentence. Do not name 1-Step on Instant.

**Paste** (1-Step `p1` with Instant-applicable rules and 20% in place of 50%)

```text
No evaluation. You start on a funded simulated account. 3% daily drawdown from that day’s equity high (floating losses included). 6% trailing max drawdown that never locks at the starting balance. Best Day must be ≤20% of Positive Days’ Profit to get paid. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000.
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
  <li>Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. Profitable days are factored into Positive Days' Profit.</li>
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

**Live** on `1-step.html` hero (`p3`), Best Day heading, `li8`, and `li9`:

> 50% Best Day rule **(Instant uses 20%)**
>
> Instant also trails, but Instant never locks.

Drop the Instant clause. 1-Step is 50% of Positive Days’ Profit only. Do not mention Instant or 0.5% on 1-Step.

**Paste**

```text
50% Best Day rule — your single best profit day cannot exceed 50% of Positive Days' Profit. See Section 3 for full details.
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
