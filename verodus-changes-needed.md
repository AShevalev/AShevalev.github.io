# Verodus live changes still needed

Scan: 18 Aug 2026 against `https://www.verodus.com/`. Locked wording: `verodus-rule-alignment.md`.

Do **not** change “at least 0.5%” or “≥ 0.5%” to “more than 0.5%.” Exactly 0.5% meets it.

Update **HTML and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` for every key you touch.

---

## 1. Instant Best Day — product error (must fix)

Live still treats 0.5% as a Positive Days’ Profit **filter**. Small profitable days are dropped. That is wrong.

**Locked rule**
- Every **profitable day** is in Positive Days’ Profit and Best Day.
- Best Day ≤ **20%** of that sum. Exceeding 20% is not a breach.
- A profitable day is a day that closes with **at least 0.5% profit** (**≥ 0.5%**).
- Never write “green day,” “0.5% parameter,” or “more than 0.5%.”
- Never write that days under 0.5% are ignored for PDP.
- No listed min trading days. Never write “5 valid days.”

**Delete these live sentences** (they drop chip days from PDP):

> A day counts only when closed profit is at least 0.5% of that day’s start-of-day equity. Smaller green days do not count toward Best Day or Positive Days’ Profit.

> A day only qualifies as a valid Best Day (and counts toward Positive Days’ Profit) when that day’s closed profit is at least 0.5% of that day’s start-of-day equity. Days below this floor are ignored.

> Best Day must be ≤20% of Positive Days' Profit (qualifying days only).

> Days under the 0.5% start-of-day equity floor do not count. … +$400 does not qualify.

**Instant Best Day modal paste** (`instant.html` `#bestDayModal` and `trading-objectives.html` Instant `best-day` branch):

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit at the time you request a payout. Every profitable day is factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit. A profitable day is a day that closes with at least 0.5% profit (≥ 0.5%). Small profitable days still count toward Positive Days' Profit.
```

JS extra sentence (Instant tab only; do **not** add when `bestPctLimit === 50`):

```javascript
if (isInstant) {
  contentEl.innerHTML += `<p>Every profitable day is factored into Positive Days’ Profit. A profitable day is a day that closes with <strong style="color:${gold}">at least 0.5% profit (≥ 0.5%)</strong>. Small profitable days still count toward Positive Days’ Profit and Best Day.</p>`;
}
```

**Where live still has the wrong Instant PDP filter**

| Page | Keys / spot |
|---|---|
| `instant.html` | `p8`, `li12`, `li14`, Eligibility `li23` / `span47`, `#bestDayModal`, JSON-LD description |
| `trading-objectives.html` | Instant `showModal('best-day')` second paragraph |
| `faq-plans.html` | Instant card `p7` |
| `faq-evaluation.html` | Instant list item + `p5` |

Same English string is in **es / fr / pt / zh / ar / id / hi / tl / pa**.

0.5% stays on the **Instant Best Day modal**. Do not put 0.5% on Weekly, Bi-Weekly, the short Trading Objectives Instant payout line, 1-Step, or 2-Step.

---

## 2. Weekly 70% and On Demand 90% cannot stack

**Correct:** Weekly and On-Demand are separate add-ons; they cannot both apply at once. Weekend stays a separate paid add-on. Default remains Bi-Weekly 80%.

Keep the live exclusive bullet. Keep checkout `PAYOUT_ADDON_EXCLUSIVE`. Do not write that they may stack.

---

## 3. Instant page — other copy

| Live | Change to |
|---|---|
| “green day” | **profitable day** |
| “qualifying days only” | every profitable day |
| Eligibility dumps 0.5% as a PDP filter (“qualifying days only”) | Eligibility keeps **Valid Day**: a Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). Valid Day is not a min-day count and does not remove small Positive Days from Positive Days’ Profit. |
| Locale leftovers `span49` / `span51` / `span53` (unused in HTML): “starting from Qualified Performance Account” / “does not skip the trading-day requirement” | Clear or rewrite. Instant is funded from day one — never say QPP account. |
| JSON-LD: “20% Best Day of qualifying days (closed profit ≥ 0.5% of SOD)” | 20% Best Day of Positive Days’ Profit. Every profitable day is included. A profitable day is at least 0.5% profit (≥ 0.5%). No min trading days. |

**Instant Rewards paste**

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. A Valid Day is a day that closes with at least 0.5% profit (≥ 0.5%). Valid Day is not a minimum trading-day count and does not remove small Positive Days from Positive Days’ Profit. Instant has no minimum trading days. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.
```

Do not dump Weekly / Bi-Weekly / On-Demand into Eligibility. Do not repeat `$100` on those three cycle bullets.

---

## 4. 1-Step — drop Instant from the page

| Live | Change to |
|---|---|
| Hero / Best Day: “50% Best Day rule **(Instant uses 20%)**” | 50% Best Day of Positive Days’ Profit. Do not mention Instant. |
| 0.5% anywhere | None. Instant-only. |

1-Step Best Day modal is already correct (every profitable day, no 0.5%). Keep it.

**1-Step Rewards paste**

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.
```

Do not list a 3-day min. Two equal profitable days can pass; the clock is usually 3 days.

---

## 5. 2-Step Lite / Pro — small leftovers

Eval **5 days per phase** and QPP **3 trading days** every payout are already right. On-Demand is already one line.

**Keep / confirm**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. The first payout and every payout after use this same rule. A trading day is a calendar day with at least one closed trade.

Weekly (Add-on): 7 calendar days, and 3 trading days.
Bi-Weekly (Standard): 14 calendar days, and 3 trading days.
On-Demand (Add-on): Available when eligibility requirements are met.
```

Clear unused locale leftovers that still say “Every 7 calendar days, starting from the day you receive your Qualified Performance Account” if those keys can come back.

No Instant 20% / 0.5% language.

---

## 6. Trading Objectives

| Live | Change to |
|---|---|
| Instant Best Day modal: days under 0.5% “are ignored” | Modal paste in §1. Every profitable day counts. At least / ≥ 0.5% defines a profitable day. |
| Instant `p8Instant` | `Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs).` No 0.5% on this line. |
| 1-Step Best Day modal | Keep “Profitable days are factored into Positive Days’ Profit.” Do not add 0.5%. |
| 2-Step `p8` | Already `$100` and 3 trading days. Keep. |
| Instant card min days | Already empty / not shown. Keep. Third rule on Instant tab is 20% Best Day, not 5 days. Keep. |

---

## 7. FAQs

### `faq-plans.html` Instant `p7`

**Delete:** “A day only qualifies for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity.”

**Paste:**

```text
Instant has no minimum trading days. Every Instant payout (first and later) needs $100, Best Day ≤20% of Positive Days’ Profit, and the selected cycle (weekly, bi-weekly, or on-demand). A profitable day is a day that closes with at least 0.5% profit (≥ 0.5%). Small profitable days still count toward Positive Days’ Profit.
```

1-Step and 2-Step cards are already split correctly. Do not put Instant 0.5% on those cards.

### `faq-evaluation.html`

**Replace Instant bullets / `p5` “qualifying days” with:**

```html
<ul>
  <li>Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. A profitable day is a day that closes with at least 0.5% profit (≥ 0.5%).</li>
  <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance has no minimum trading days. Best Day ≤50% of Positive Days’ Profit.</li>
  <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
  <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

### `faq-qualified-trader.html`

4-then-3 is already gone. On-demand list can stay:

```text
$100 since last reward
On-demand: available when eligibility requirements are met
```

Do not re-paste Instant 0.5% into this hub answer. Fee refund `p28` is already correct (evals only; add-ons not refunded; Instant has no challenge-fee refund).

---

## 8. TOS

| Live | Change to |
|---|---|
| §8(b) `li4`: “A minimum number of Trading Days is required both during the evaluation phases and before/between Performance Rewards.” | Keep “Requirements vary by model.” Delete the site-wide min-days sentence. Instant and 1-Step have no min trading days. |
| §8(a) `p40`: first Performance Reward includes a 100% challenge-fee refund, no Instant exception | Challenge-fee refund is eval plans only. Instant is not refundable. Add-ons are never part of that refund. |

News TOS §9(b)(ii) is already aligned. Empty keys `h38` / `p51`–`p53` can stay blank.

---

## 9. Checkout

| Live | Change to |
|---|---|
| `PAYOUT_ADDON_EXCLUSIVE` blocks Weekly + On Demand | Allow both. They may stack. |
| On-Demand tooltip | Already “Available when eligibility requirements are met.” Keep. |
| Instant On Demand 32% / evals 15% / Weekend 15% / Weekly 6% | Keep. |
| Instant sizes stop at $100k | Keep. |

---

## 10. Locales (after HTML)

Same Instant Best Day / Eligibility / FAQ / 1-Step “Instant uses 20%” / “cannot both apply at once” strings in:

`/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/instant.json`, `1-step.json`, `2-step-lite.json`, `2-step-pro.json`, `trading-objectives.json`, `faq-plans.json`, `faq-evaluation.json`, `faq-qualified-trader.json`, `terms.json`

Clear unused Instant leftovers: `li10`, `span49`, `span51`, `span53`.

---

## Already correct — do not reopen

- News included on Instant, 1-Step, Lite, Pro — eval and funded. Heading is **Allowed:** not “Allowed in Evaluation.” Bracketing and gap banned. No news addon. No ±2-minute window.
- No minimum holding time. No 50% profit-from-trades-over-2-minutes test.
- Instant: no listed min trading days, no “5 valid days,” 6% trail never locks, 3% daily from that day’s equity high, no $200k, Instant fees not refundable.
- Instant 0.5% threshold wording: **at least** / **≥**. Keep it. Do not switch to “more than.”
- 1-Step: no min days, 50% Best Day, every profitable day in PDP, no 0.5% on the 1-Step modal.
- 2-Step Lite / Pro: 5 eval days per phase, QPP 3 trading days every payout, one On-Demand line.
- $100 on every cycle. First and later payouts are the same. Old 4-then-3 split is gone.
- Eval first-payout refund = challenge fee only on plan / rewards / Qualified FAQ. Add-ons not refunded.
- Trading-objectives Instant short payout line (no 0.5%). Instant tab third rule is 20% Best Day, not 5 days.
- Weekend Holding Addon. `$200k` on 1-Step / Lite / Pro.

---

## Paste order

1. Instant Best Day body + modal + Trading Objectives Instant JS + Instant JSON-LD + FAQ Plans / Evaluation Instant lines.
2. Instant / 1-Step / 2-Step Rewards bullets (Eligibility short; On-Demand = when eligibility is met).
3. Delete “cannot both apply at once” on all four plans; unlock checkout stack.
4. Strip “Instant uses 20%” from 1-Step.
5. TOS §8(b) min-days sentence and §8(a) refund Instant exception.
6. Locales for every key you changed.
