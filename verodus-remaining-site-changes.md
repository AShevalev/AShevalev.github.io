# Verodus remaining site changes

Live scan 18 Aug 2026. Only items still wrong on `https://www.verodus.com/`. Do not re-paste rules that already landed.

**Keep as live:** `at least 0.5%` and `≥ 0.5%`. Do not write “more than 0.5%.” Exactly 0.5% meets it.

**Already on live (do not redo):** news included / **Allowed:** heading; no min holding time; Instant no listed min days and no “5 valid days”; Instant 6% trail never locks; Instant no `$200k`; Instant fees not refundable on the Instant page; 1-Step no min days + 50% Best Day + every profitable day (1-Step modal has no 0.5%); 2-Step 5 eval days / 3 QPP days; `$100` every cycle; same first and later payouts; 4-then-3 gone; Trading Objectives Instant payout line already short (`$100`, no min days, Best Day ≤20%, no 0.5%); checkout On-Demand already “when eligibility requirements are met.”

Apply HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`. English locale JSON currently carries the same Instant PDP error as the HTML.

---

## 1. Instant Best Day — every Positive Day is in Positive Days’ Profit

Live still treats 0.5% as a **Positive Days’ Profit filter**. Small days in profit are dropped. That is the Instant rule that is still wrong.

**Names (do not merge these)**
- **Positive Day** = a calendar day that **closes in profit** (including a small +0.1% day). That is the unit of **Positive Days’ Profit** and Best Day. Use this, not “green day.”
- **Valid Day** (Instant only) = a calendar day that closes with **at least 0.5% profit** (**≥ 0.5%**). Use **Valid Day** for the 0.5% sentence. Do not write “A Positive Day is a day that closes with at least 0.5% profit.” That is the live bug.
- A Valid Day is **not** which days enter Positive Days’ Profit. Small Positive Days still count even if they are not Valid Days.
- Never write “5 Valid Days,” “5 valid trading days,” or any Valid Day count. Instant has **no** minimum trading days.

**Locked Instant rule**
- Best Day ≤20% of **Positive Days’ Profit**.
- **Every Positive Day** is included, including small days.
- Never write “green day,” “qualifying days only,” or “days below this floor are ignored.”
- 0.5% belongs on the **Instant Best Day modal**. Do not use it to exclude days from Positive Days’ Profit on Eligibility, FAQs, or schema.

### `instant.html`

| Key / spot | Live (wrong) | Change to |
|---|---|---|
| `content.p8` | “A day counts only when closed profit is at least 0.5% of that day’s start-of-day equity. **Smaller green days do not count** toward Best Day or Positive Days’ Profit.” | Every Positive Day is included. A Positive Day is a calendar day that closes in profit. Small Positive Days still count. Instant 0.5% is a separate modal line, not this definition. |
| `content.li12` | “Best Day must be ≤20% of Positive Days' Profit **(qualifying days only)**.” | Best Day must be ≤20% of Positive Days’ Profit. |
| `content.li14` | “Days under the 0.5% start-of-day equity floor **do not count**.” Example: +$400 does not qualify. | Closed trades at 00:00 UTC. Losing days do not count. Every Positive Day counts. |
| Eligibility `li23` / `span47` | “**qualifying days only:** closed profit ≥ 0.5% of that day’s start-of-day equity” | `$100` + Best Day ≤20% of Positive Days’ Profit + cycle. No min trading days. **No 0.5% here.** |
| `#bestDayModal` | “A day only qualifies … **at least 0.5%** of SOD. **Days below this floor are ignored** for the 20% Best Day calculation.” | Paste below. |
| JSON-LD `description` | “20% Best Day of **qualifying days** (closed profit ≥ 0.5% of SOD)” | 20% Best Day of Positive Days’ Profit. Every Positive Day is included. No min trading days. |

**Instant Best Day modal paste**

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit at the time you request a payout. A Positive Day is a calendar day that closes in profit. Every Positive Day is included in Positive Days' Profit. A Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). Valid Day is not a minimum trading-day count and does not remove small Positive Days from Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit.
```

**Instant Eligibility paste** (no 0.5% on this bullet)

```text
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.
```

**Instant `p8` paste**

```text
Your single best profit day cannot account for more than 20% of Positive Days’ Profit at the time you request a payout. A Positive Day is a calendar day that closes in profit. Every Positive Day is included in Positive Days’ Profit. Small Positive Days still count.
```

Do **not** keep:

> Smaller green days do not count toward Best Day or Positive Days’ Profit.

> Days below this floor are ignored.

> qualifying days only

### `trading-objectives.html` Instant Best Day modal

Live JS (`showModal('best-day')` when Instant):

> A day only qualifies as a valid Best Day (and counts toward Positive Days’ Profit) when that day’s closed profit is at least 0.5% of that day’s start-of-day equity. **Days below this floor are ignored.**

**Replace the Instant extra paragraph with:**

```javascript
if (isInstant) {
  contentEl.innerHTML += `<p>A Positive Day is a calendar day that closes in profit. Every Positive Day is included in Positive Days’ Profit. A <strong>Valid Day</strong> is a day that closes with <strong style="color:${gold}">at least 0.5% profit (≥ 0.5%)</strong>. Valid Day is not a minimum trading-day count and does not remove small Positive Days from Positive Days’ Profit.</p>`;
}
```

Do **not** add that 0.5% sentence on the 1-Step 50% modal. Live 1-Step extra line (“Profitable days are factored into Positive Days’ Profit”) can stay.

### FAQs that still copy the Instant PDP filter

**`faq-plans.html` Instant card (`content.p7`)** live:

> A day **only qualifies** for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.

**Paste**

```text
No evaluation. You start on a funded simulated account. 6% trailing max drawdown from equity high water mark (the trail never locks). 3% daily drawdown from that day’s equity high, as a fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC. Best Day must be ≤20% of Positive Days’ Profit to request a payout. A Positive Day is a calendar day that closes in profit. Every Positive Day is included. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000; no $200,000 Instant account.
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

## 2. Weekly 70% and On Demand 90% may stack

Locked: they **may stack**. Weekend stays paid. Default remains Bi-Weekly 80%.

**Live (wrong) on Instant, 1-Step, Lite, and Pro**

> Weekly and On-Demand are separate add-ons; they **cannot both apply at once**.

Delete that bullet (`instant` `li20`, `1-step` `li18`, Lite/Pro `li15`).

**Checkout** `checkout.html` still has:

```javascript
var PAYOUT_ADDON_EXCLUSIVE = { 'weekly-payout': 1, 'on-demand-payout': 1 };
```

Remove the exclusive pair so Weekly and On Demand can both be selected.

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

Drop the Instant clause. 1-Step is 50% of Positive Days’ Profit only. Do not mention 0.5% on 1-Step.

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
- Putting Instant 0.5% on 1-Step or 2-Step.
- Re-splitting first vs later payouts.
- News, holding time, Instant trail, Instant `$200k`, Instant not-refundable on the Instant page, 2-Step 5/3, `$100`, Trading Objectives Instant short payout line.
