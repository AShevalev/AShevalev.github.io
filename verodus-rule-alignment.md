# Verodus site rule alignment

Apply these rules on **every Verodus page that names them**, including `trading-objectives.html`. Instant Best Day copy is **live 1-Step wording** at **20%** (payout request, not evaluation pass). 1-Step stays live at **50%**. **No Instant 0.5% / Valid Day.** Do not mention 0.5% on Instant, 1-Step, or 2-Step. Do not write “green day.” Live 1-Step Calculation (“Profitable days are factored into Positive Days' Profit”) is the Instant Calculation too. Update HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` **including** `trading-objectives.json` for Instant Best Day / day-count keys.

Canonical source: `1-step.html`, `2-step-lite.html`, `2-step-pro.html`, `instant.html`, `trading-objectives.html` Instant Best Day modal, TOS §9, `restricted-trading.html`.

Do **not** put Instant 20% language on the 1-Step 50% Best Day modal or on 2-Step pages. Do **not** put 0.5% / Valid Day on any plan.

---

## Canonical rules

### News
- Allowed in **every phase**: Instant, 1-Step, 2-Step Lite, 2-Step Pro — evaluation and Qualified Performance / funded.
- Open, close, or hold through high-impact news. **No** news time window. **No** news-trading breach.
- **Banned:** news bracketing (straddling); gap trading (opened within 60 minutes of a market close and held through reopen).
- **Banned (unchanged):** HFT, tick scalping, latency/arbitrage, rollover abuse.
- No News Trading Addon. Do not name it.

### Holding time
- **No** minimum holding time. **No** 50% profit-from-trades-over-2-minutes test.
- Instant scalping is allowed inside drawdown / trail / Best Day rules.

### Rewards
- **$100** is the money minimum on **every payout cycle** — weekly, bi-weekly, and on-demand — on every plan. Same `$100` for the first payout and every payout after.
- **First and subsequent payouts are the same.** No “first after X days, later after Y.” Every request must meet **that plan’s payout rule** **and** the **selected cycle**.
- Plan payout rules (same for every payout on that plan):
  - **Instant:** **No minimum trading days.** Instant Best Day copy is live 1-Step wording at **20%**. Never write “green day,” “5 min trading days,” “5 valid trading days,” Valid Day, or 0.5%. Profitable days are factored into Positive Days' Profit. Best Day must be ≤20% of Positive Days’ Profit at the time you request a payout. Exceeding 20% is not a breach — continue trading until the condition is met. Instant has **no** 3-day QPP min. Same first payout and every payout after.
  - **1-Step Qualified Performance:** **No minimum trading days.** The day rule is **50% Best Day of Positive Days’ Profit**. Same Positive Day definition as Instant. Two equal Positive Days can pass (50/50); that split is rare, so the clock is usually 3 days. Do **not** list a 3-day min. Exceeding 50% is not a breach — continue trading until Best Day is ≤50%. Evaluation also has **no** minimum trading days to pass (same 50% Best Day at the 10% target). Do not mention Instant 20% or 0.5% on 1-Step.
  - **2-Step Lite / Pro Qualified Performance:** **3 minimum trading days** for every payout. Evaluation still needs **5 trading days per phase** (open and close the same calendar day). No Instant 20% / 0.5% language.
- A 2-Step “trading day” = open and close on the same calendar day. The 3-day QPP rule is **2-Step only** — a **count** of trading days in that payout window, not “wait 3 days since last payout.” Do not put it on 1-Step or Instant.
- Cycle (same for the first payout and every payout after). **`$100` lives in Eligibility / Minimum Reward — do not repeat it on Weekly, Bi-Weekly, or On-Demand.**
  - **Weekly (every plan):** 7 calendar days since the account start or last reward, plus that plan’s Eligibility rule (Instant/1-Step Best Day; 2-Step 3 trading days).
  - **Bi-weekly (every plan):** 14 calendar days since the account start or last reward, plus that plan’s Eligibility rule.
  - **On-demand (every plan page):** `Available when eligibility requirements are met.` Do **not** paste Instant / 1-Step / 2-Step On-Demand variants onto each plan page.
- **No Instant 0.5% / Valid Day.** Instant copy is 20% of every Positive Day + `$100` + cycle. Do not write “more than 0.5%,” “qualifying days only,” or “days below this floor are ignored.”
- Do not add a first-vs-later split (e.g. “first after 4 days, later after 3”). Instant and 1-Step have no min trading days. The 3-day QPP min is **2-Step only**.

### Instant Best Day (20%)
Use live 1-Step wording. Do **not** write “green day,” “0.5% parameter,” or Valid Day. Live 1-Step says “Profitable days are factored into Positive Days' Profit.”
- Best Day ≤20% of **Positive Days’ Profit** at the time you request a payout.
- Exceeding 20% is not a breach — continue trading until Best Day is ≤20%.
- Instant-only cap. 1-Step is 50% with the same live wording.

### 1-Step Best Day (50%)
- Same Positive Day definition as Instant. All Positive Days count, including small Positive Days.
- Best Day = the single largest Positive Day. It must be ≤50% of Positive Days’ Profit.
- Exceeding 50% is not a breach — continue trading until Best Day is ≤50%.
- **No listed min trading days** in evaluation or Qualified Performance. Two equal Positive Days can pass (50/50); that split is rare, so the clock is usually 3 days. Do **not** list a 3-day min.
- Same 50% Best Day at the 10% evaluation target and on every QPP payout.
- Do not mention 0.5% or Instant 20% on 1-Step pages or in the 1-Step Best Day modal.

### Do not change
- `$200,000` account sizes
- Weekend Holding Addon
- Instant 3% daily from day’s equity high, 6% trail that never locks
- 1-Step Best Day stays **50% of Positive Days’ Profit** with **no** listed 3-day min. Same Positive Day definition as Instant. Do not mention 0.5% or Instant 20% on 1-Step.
- Instant Best Day stays **20% of Positive Days’ Profit**. A Positive Day is a calendar day that closes in profit. All Positive Days count. **No 0.5% / Valid Day.**
- 2-Step evaluation still **5 trading days per phase**. Do not rewrite the 2-Step “5 Minimum Active Performance Days” eval modal into Instant Best Day language.

---

## 1. Align “Allowed in Evaluation” (news sounds eval-only)

Live on 1-Step `li36` / `span32`, 2-Step Lite & Pro `li32` / `span28`:

> **Allowed in Evaluation:** Full news trading, Expert Advisors (EAs)…

Instant already says **Allowed**. Dedicated news lines already say every phase.

**Change the heading only** to **Allowed:** Keep the rest (EAs still subject to Section 6 HFT / mass-EA / hyperactivity / arb).

**Paste:**

```text
Allowed: Full news trading, Expert Advisors (EAs), scripts, and custom indicators are permitted, subject to the restrictions in Section 6 – Restricted Trading Practices (no HFT, no mass-distributed/copy-trading EAs, no server hyperactivity, no arbitrage exploitation, etc.).
```

Optional: shorter news bullets (`1-step` `li30`/`span26`, lite/pro `li26`/`span22`) may stay “evaluation and Qualified Performance,” or use: `News trading is allowed in every phase.`

---

## 2. Same rule for first and later payouts: plan payout rule + cycle

Live FAQ under `p9` still splits them:

> First payout: available after 4 trading days 
> Subsequent payouts: available after 3 trading days

That split is wrong. **Delete both bullets.** First and later payouts use the same checklist: **`$100` + that plan’s payout rule + the selected cycle** (weekly 7 calendar days, bi-weekly 14 calendar days, on-demand = `$100` and that plan’s rule).

**`content.p9` paste:**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: you must meet that plan’s payout rule and the selected cycle (weekly, bi-weekly, or on-demand).
```

**On-demand paste — same line on every plan page.** Do **not** paste Instant / 1-Step / 2-Step On-Demand variants onto each page. Eligibility already names `$100` and that plan’s payout rule.

```text
On-Demand (Add-on): Available when eligibility requirements are met.
```

Do **not** paste these onto Instant / 1-Step / 2-Step plan pages:

```text
Instant: On-demand: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit.
1-Step: On-demand: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit.
2-Step Lite / Pro: On-demand: $100 and 3 trading days.
```

Those plan-specific lines belong only in Eligibility (and, for Instant 0.5%, the Instant Best Day modal). Skip `$100` on Weekly / Bi-Weekly / On-Demand — Eligibility already has it.

**Hub FAQ only** (Qualified Trader / Evaluation — pages that name every plan). Separate bullets, never one blended Instant sentence:

```html
<ul>
  <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
  <li>Weekly: 7 calendar days since account start or last reward (plus that plan’s Eligibility rule)</li>
  <li>Bi-weekly: 14 calendar days since account start or last reward (plus that plan’s Eligibility rule)</li>
  <li>On-demand: available when eligibility requirements are met</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.`

**Replace with:**

```text
Payout spacing follows the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. Instant and 1-Step have no minimum trading days. On 2-Step Qualified Performance, every payout needs 3 trading days. The first payout and later payouts use the same rule.
```

**1-Step Eligibility** still says “at least 3 trading days since QPP / last payout.” **Delete that 3-day min.** 1-Step QPP uses `$100` + 50% Best Day of Positive Days’ Profit + cycle. Two equal profitable days can pass; do not list a 3-day min. **2-Step Eligibility:** keep **3 trading days** as a count (plus `$100` + cycle), not “wait 3 days since last payout.” 2-Step eval stays 5 days per phase.

**Instant Eligibility (`instant.html` `li23` / `span47`) — replace the 3-day line.** Live:

> Eligibility: You become eligible for a reward only after both of the following are met: At least 3 trading days have passed since you received your Qualified Performance Account or since your last payout, and …

**Instant paste — Rewards & Payouts on `instant.html` (and Instant FAQ).** Keep Eligibility as `$100` + 20% Best Day + cycle. **No Valid Day. No 0.5%.** Do **not** dump Weekly / Bi-Weekly / On-Demand into Eligibility. Skip `$100` on the cycle bullets — Eligibility already has it. On-Demand is one line: available when eligibility requirements are met. Do **not** say “Qualified Performance Account” on Instant. Do **not** write “green day” or “0.5% parameter.”

```text
Minimum Reward: $100 (processed within 48 hours)

Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit, and you have met the selected cycle. Instant has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.

Weekly (Add-on): 7 calendar days and when eligibility requirements are met.

Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.

On-Demand (Add-on): Available when eligibility requirements are met.
```

**1-Step Eligibility paste — 1-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. See Section 3. The first payout and every payout after use this same rule.
```

1-Step Weekly / Bi-Weekly / On-Demand (same page, separate bullets — no `$100` on these; Eligibility already has it):

```text
Weekly (Add-on): 7 calendar days and when eligibility requirements are met.
Bi-Weekly (Standard): 14 calendar days and when eligibility requirements are met.
On-Demand (Add-on): Available when eligibility requirements are met.
```

**2-Step Lite / Pro Eligibility paste — 2-Step only.** One On-Demand line. Do **not** also keep “does not skip the trading-day requirement” / “for that evaluation.”

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. The first payout and every payout after use this same rule. A trading day is a calendar day with at least one closed trade.

Weekly (Add-on): 7 calendar days, and 3 trading days.
Bi-Weekly (Standard): 14 calendar days, and 3 trading days.
On-Demand (Add-on): Available when eligibility requirements are met.
```

Instant `li10` / `span21` — **Delete.** Instant has **no minimum trading days.** Do not leave a leftover **“Minimum Trading Days: No minimum trading days.”** bullet. Keep one card stat (**None**). Do not also print “Minimum Trading Days: None” in the card meta.

`performance-reward.html` “First reward after 3 trading days” / “Min. 3 trading days” — keep **3 trading days** for **2-Step QPP only**. 1-Step and Instant have no min trading days. Drop the first/later split. Add `$100` + cycle.

`trading-objectives.html` — **edit Instant Best Day and Instant day-count copy.** See §8. Do not add Instant 0.5% to the 1-Step 50% Best Day modal.

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100, that plan’s payout rule, and the selected cycle (same rule for the first payout and every payout after).
```

On `trading-objectives.html`, Instant and 1-Step have **no min trading days**. Instant payout line is short — **no 0.5%**:

```text
Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs).
```

1-Step payout lines use `$100` + 50% Best Day of Positive Days’ Profit. 2-Step lines use `$100` + **3 trading days** (every payout, not first-only). Instant has **no 0.5% / Valid Day**. Do not put Instant 20% on the 1-Step Best Day modal.

---

## 4. Soften FAQ “at any time” (on-demand)

**`content.p13` live:** `Payouts can be requested at any time through the dashboard once the following conditions are met:`

The list already has `$100` + min days. Optional paste:

```text
Payouts can be requested through the dashboard once the following conditions are met:
```

---

## 5. Instant — no min trading days; 20% Best Day of Positive Days’ Profit

On Instant pages, say **only** Instant rules. Do not mention 1-Step or 2-Step day counts. Do not put Instant 20% / 0.5% language on 1-Step or 2-Step. Never write “green day,” “5 min trading days,” “5 valid trading days,” or “0.5% parameter.”

`instant.html` Eligibility is wrong today if it still uses the 1-Step / 2-Step QPP **3 trading days** sentence, or it treats 0.5% as a PDP filter. Instant has **no minimum trading days**. Instant’s day rule is **20% Best Day of Positive Days’ Profit**. Same first payout and every payout after. **No Valid Day. No 0.5%.**

| Key | Live | Change to |
|---|---|---|
| Eligibility | At least **3 trading days** since QPP; or “qualifying days only” as a PDP filter | `$100` + Best Day ≤20% of Positive Days’ Profit + cycle. No min days. No 0.5%. Do not dump Weekly / Bi-Weekly / On-Demand into this bullet. |
| Weekly | 7 calendar days, no Best Day; or “starting from Qualified Performance Account” | **`$100`, 7 calendar days, Best Day ≤20% of Positive Days’ Profit.** Instant is funded from day one — do not say QPP account. |
| Bi-Weekly | 14 calendar days, no Best Day | **`$100`, 14 calendar days, Best Day ≤20% of Positive Days’ Profit.** |
| On-Demand | Wordy 0.5% “parameter” + “green day”; or two On-Demand bullets | **One line:** Available when eligibility requirements are met. |
| `li10` / `span21` | 5 valid days before your **first** reward | **No minimum trading days.** Delete the 5-day line. |

Delete the Instant “3 trading days since last payout” extra. Delete Instant 5-valid-day / 5-min-day lines. Do **not** add the 2-Step 3-day QPP min to Instant or 1-Step.

---

## 5b. 2-Step Qualified Performance — 3 trading days; 1-Step has no QPP day min

**1-Step QPP:** no minimum trading days. **50% Best Day of Positive Days’ Profit** is the 1-Step day rule. Two equal profitable days can pass; the clock is usually 3 days. Do not list a 3-day min. Delete the live “3 trading days since QPP / last payout” line on `1-step.html`.

**2-Step Lite / Pro QPP:** **3 trading days** (open and close the same calendar day) for every payout, first and later. Plus `$100` and the selected cycle. Keep **one** On-Demand line: `$100 and 3 trading days.` Do **not** also keep “Available when net profit > $100… On-demand does not skip the trading-day requirement.” Do **not** write this as “3 trading days have passed since last payout” or “for that evaluation.”

Keep evaluation separate:
- **1-Step evaluation:** no minimum trading days to pass.
- **2-Step Lite / Pro evaluation:** 5 trading days per phase. QPP payouts are **3**, not 5.

Do not put Instant Best Day / 0.5% language on these pages. Do not put the 2-Step 3-day min on 1-Step.

---

## 6. Empty locale keys (cleanup, not visible)

Update Instant Best Day / day-count keys in `trading-objectives.json`. Elsewhere, delete or leave blank:

- TOS: `content.h38`, `p51`, `p52`, `p53`
- Restricted trading: `p9`, `p18`
- 1-step `li42`; 2-step lite/pro `li38`; instant `li43`
- `common.json` `pricing.addonFootnote` (already empty)

---

## 7. FAQs — one answer per plan (do not blend clocks)

FAQs that name “the evaluation” or one day number for all accounts are wrong. Split Instant / 1-Step / 2-Step. Apply the same split on `trading-objectives.html` (Instant vs 1-Step vs 2-Step).

### Plan cheat sheet (use in every payout / days FAQ)

| Plan | Eval / pass min days | QPP / payout rule (every payout) | Cycle |
|---|---|---|---|
| Instant | No eval. Funded from day one. | **No min trading days.** **20% Best Day of Positive Days’ Profit.** **No** 3-day QPP min. | Weekly **$100** + 7 calendar + Best Day ≤20% / bi-weekly **$100** + 14 calendar + Best Day ≤20% / on-demand **$100** + Best Day ≤20%. |
| 1-Step | **No** minimum trading days to pass | **No** min days; **50% Best Day of Positive Days’ Profit**. Two equal days can pass; do not list a 3-day min. | Weekly **$100** + 7 calendar + Best Day ≤50% / bi-weekly **$100** + 14 calendar + Best Day ≤50% / on-demand **$100** + Best Day ≤50% |
| 2-Step Lite | **5** trading days per phase | **3 trading days** | Weekly **$100** + 7 calendar + 3 trading days / bi-weekly **$100** + 14 calendar + 3 trading days / on-demand **$100** and 3 trading days (**one** line; do not also say “does not skip”) |
| 2-Step Pro | **5** trading days per phase | **3 trading days** | Same as Lite |

A 2-Step “trading day” = open and close on the same calendar day. Instant and 1-Step have **no min trading days**. Instant and 1-Step use the same Positive Day definition (20% vs 50%). Do not put Instant 20% on 1-Step. Do not put the 2-Step 3-day QPP min on Instant or 1-Step. Do not put 2-Step’s **5 eval days** on 2-Step QPP payouts.

---

### `faq-evaluation.html`

**“How many trading days do I need for each program?”** — hardcoded list omits Instant.

**Replace the list with:**

```html
<ul>
  <li>Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. All Positive Days count toward Positive Days’ Profit.</li>
  <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance has no minimum trading days. Best Day ≤50% of Positive Days’ Profit.</li>
  <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
  <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

**`content.p5` (“What if I hit my targets before the minimum trading days?”)** live: one rule for everyone, open-and-close only. That is wrong for 1-Step eval (no min) and Instant (no min days; 20% Best Day of Positive Days’ Profit). Split eval vs QPP.

**Paste `p5`:**

```text
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days in evaluation or Qualified Performance. Every profitable day is factored into Positive Days’ Profit. Best Day ≤50%. 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no minimum trading days and no profit target to “hit first”; you need $100, Best Day ≤20% of Positive Days’ Profit, and the selected payout cycle.
```

Keep `p6` as the 2-Step / 1-Step calendar-day definition. Instant Best Day / 0.5% math stays on `instant.html`.

---

### `faq-qualified-trader.html`

News (`p1`, `p18`) is already plan-complete. Fix payout answers so they name each plan.

**`content.p9` paste (hub FAQ — separate sentences, not one Instant/1-Step/2-Step mash):**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: that plan’s payout rule and the selected cycle. On Instant, on-demand is $100 with no minimum trading days (Best Day ≤20% of Positive Days’ Profit; a Valid Day is a day that closes with at least 0.5% profit). On 1-Step, on-demand is $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit. On 2-Step Lite and 2-Step Pro Qualified Performance, on-demand is $100 and 3 trading days. Weekly is $100 and 7 calendar days. Bi-weekly is $100 and 14 calendar days. Every cycle has a $100 minimum.
```

**Delete** the hardcoded “First payout after 4 / subsequent after 3” list. Replace with:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Instant: no minimum trading days, Best Day ≤20% of Positive Days’ Profit, plus the cycle</li>
    <li>1-Step Qualified Performance: no minimum trading days, Best Day ≤50% of Positive Days’ Profit, plus the cycle</li>
    <li>2-Step Lite / Pro Qualified Performance: 3 trading days, plus the cycle</li>
    <li>Weekly: $100 and 7 calendar days · Bi-weekly: $100 and 14 calendar days</li>
    <li>On-demand Instant: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit. All Positive Days count toward Positive Days’ Profit</li>
    <li>On-demand 1-Step: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit</li>
    <li>On-demand 2-Step: $100 and 3 trading days</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.` **Replace with:**

```text
Payout spacing is the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. Every cycle has a $100 minimum. Instant and 1-Step have no minimum trading days. 2-Step Qualified Performance needs 3 trading days on every payout. First and later payouts use the same rule.
```

**`content.p13` + on-demand list** — drop “at any time.” Paste list:

```html
<ul>
  <li>$100 since last reward</li>
  <li>On Instant: no minimum trading days; Best Day ≤20% of Positive Days’ Profit (a Valid Day is a day that closes with at least 0.5% profit)</li>
  <li>On 1-Step Qualified Performance: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit</li>
  <li>On 2-Step Lite / Pro Qualified Performance: 3 trading days</li>
</ul>
```

**`content.p28` (fee refund)** live: yes for first reward, no Instant exception. **Paste:**

```text
Yes, on 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Add-ons are not refunded if they were purchased (Weekend Holding, Weekly, On-Demand, or any other add-on). Instant has no challenge-fee refund.
```

---

### `faq-plans.html`

Cards already name news + no holding time. Instant cards that still say 5 valid days must switch to **no min trading days** + 20% Best Day of Positive Days’ Profit. Optional Instant (`p7`):

```text
Instant has no minimum trading days. Every Instant payout (first and later) needs $100, Best Day ≤20% of Positive Days’ Profit, and the selected cycle (weekly, bi-weekly, or on-demand).
```

Do not add the 2-Step 3-day QPP min to Instant or 1-Step cards. Optional 2-Step line:

```text
2-Step Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand).
```

Optional 1-Step line:

```text
1-Step Qualified Performance payouts (first and later) need $100, Best Day ≤50% of Positive Days’ Profit, and the selected cycle. 1-Step has no minimum trading days.
```

---

### `faq-news-trading.html` and `faq-general.html`

Already aligned: news allowed on all four plans; holding time is No. No change required unless a leftover “addon” or “±2-minute” line comes back.

---

## 8. Apply on the rest of the site — including Instant Best Day modals

Live scan 17 Aug 2026. Same Instant sentence everywhere a 20% Best Day modal or Instant day-count appears. 2-Step QPP **3 trading days** only on 2-Step. 1-Step QPP has **no** 3-day min. Do not blend them.

### Instant 20% Best Day modal — same Positive Day as 1-Step

Add this only when the tab / page is Instant. Do not write “0.5% parameter.” Do not add Valid Day.

**`trading-objectives.html` `showModal('best-day')` — Instant and 1-Step share the Positive Day paragraph.** Caps differ: Instant 20% at payout request; 1-Step 50% when you pass evaluation and at every payout request.

Do **not** add a 0.5% sentence when `bestPctLimit === 50` (1-Step). Do not mention 0.5% in Instant or 1-Step copy at all.

### 1-Step 50% Best Day modal — every profitable day

Keep the existing 50% first paragraph. Do **not** copy Instant’s 0.5% sentence onto 1-Step. If the shared modal needs a 1-Step extra line when `bestPctLimit === 50`, use only this:

```text
Every profitable day is factored into Positive Days’ Profit and Best Day.
```

JS paste (1-Step branch only):

```javascript
if (bestPctLimit === 50) {
  contentEl.innerHTML += `<p>Every profitable day is factored into Positive Days’ Profit.</p>`;
}
```

**`1-step.html` Best Day modal** (`#bestDayModal`): keep 50%, not-a-breach, closed trades at 00:00 UTC, losing days do not count. That already means every profitable day is in PDP. Do not mention 0.5%. Optional extra sentence: `Every profitable day is factored into Positive Days' Profit.`

Do **not** keep this Instant modal line (it wrongly drops small profitable days from PDP):

> Only days that close at least 0.5% profit of account balance count toward Positive Days’ Profit and count as a day. A day that closes 0.5% or less does not count.

**`instant.html` Best Day modal** (hardcoded under `#bestDayModal`). Live first paragraph is the 20% rule only. Insert the Instant 0.5% sentence after it:

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit at the time you request a payout. Every profitable day is factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit. All Positive Days count toward Positive Days’ Profit. Small profitable days still count toward Positive Days' Profit.
```

Also on `instant.html` body copy (not only the modal):
- `content.li10` / `span21`: **No minimum trading days.** Delete 5-valid-day / first-reward copy.
- `content.p8` / `li12`–`li14`: every profitable day counts toward Positive Days’ Profit. Best Day ≤20% of that sum.
- `content.li15`: 0.5% is Instant On-Demand only: a Valid Day is a day that closes with at least 0.5% profit.
- Hero / `li4` / `li9`: drop “5 valid trading days.” Instant has no min trading days. Best Day stays 20% of Positive Days’ Profit.
- Eligibility `li23`: `$100` + Best Day ≤20% of Positive Days’ Profit + cycle + **Valid Day** (at least 0.5% / ≥ 0.5%; not a min-day count; does not drop small Positive Days). **No** 3-day QPP min.

### `trading-objectives.html` — other Instant / QPP lines (same pass)

| Live | Change to |
|---|---|
| Instant card “Minimum Trading Days” = **5 Days** (`instantCardHTML` / `pricing.fiveDays`) | **Remove.** Instant has no min trading days. Show Best Day 20% only, or “None.” |
| Instant data `minDays:'5'` | Drop or unused. |
| `content.p8Instant`: First Payout after **5 trading days** | `Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs).` Drop “first only.” No 0.5% on this line. |
| `content.p8`: First Payout after **3 trading days** (eval tabs) | **2-Step only:** every QPP payout `$100` + **3 trading days**. **1-Step:** `$100` + 50% Best Day of Positive Days’ Profit; no min trading days. Drop “first only.” Not for Instant (`p8Instant` stays Instant-only). |
| Instant on-demand / “Anytime after min trading days” | Instant: `$100`. No min trading days. Best Day ≤20% of Positive Days’ Profit. All Positive Days count toward Positive Days’ Profit. 1-Step: `$100`. No minimum trading days. Best Day ≤50% of Positive Days’ Profit. 2-Step: `$100` + 3 trading days. |
| 1-Step Best Day modal (same `best-day` type, `bestPctLimit === 50`) | Every profitable day in PDP. Do not mention 0.5%. |
| 2-Step `trading-days` modal: 5 active days in **evaluation** | Keep as **eval** 5 days. Do not turn it into Instant 0.5%. QPP payouts on 2-Step are **3** days — say that on Eligibility / rewards, not in the eval modal. |

Locale: `/locales/*/pages/trading-objectives.json` and `common.json` keys used by the Instant card / `p8Instant` / Best Day strings.

### Site-wide apply list (where the same rules appear)

| Page | Apply |
|---|---|
| `instant.html` | **No min trading days.** 20% Best Day of Positive Days’ Profit in the Best Day block **and** modal. Eligibility: `$100` + Best Day ≤20% + cycle. **No 0.5% / Valid Day.** Weekly / Bi-Weekly: clock + eligibility. Drop 5-valid-day lines and the 3-day QPP Eligibility sentence. |
| `1-step.html` | QPP Eligibility: **no min trading days** + `$100` + 50% Best Day of Positive Days’ Profit + cycle. Weekly / Bi-Weekly: `$100` + Best Day ≤50% + clock. Delete the 3-day QPP line. Eval: no min days, same 50% Best Day. Do not mention 0.5%. |
| `2-step-lite.html` / `2-step-pro.html` | Eval: **5** trading days per phase. QPP Eligibility: **3 trading days** + `$100` + cycle. Weekly / Bi-Weekly / On-Demand each name `$100` and 3 trading days. **One** On-Demand line. **No** Instant 20% / 0.5%. |
| `trading-objectives.html` | Instant Best Day modal + Instant card / `p8Instant` as above. 1-Step `p8` = no min days. 2-Step `p8` = 3 QPP days every payout. |
| `faq-plans.html` `p7` | Instant: no min trading days. 20% Best Day of Positive Days’ Profit. All Positive Days count toward Positive Days’ Profit. |
| `faq-plans.html` 1-Step / 2-Step cards | 1-Step QPP: no min days; 50% Best Day of Positive Days’ Profit. 2-Step QPP: 3 trading days. Do not put Instant 0.5% on those cards. |
| `faq-qualified-trader.html` | Delete 4-then-3. Instant = no min days + Best Day of every profitable day. 1-Step QPP = no min days + 50% Best Day of Positive Days’ Profit. 2-Step QPP = 3 trading days. Same first and later. |
| `faq-evaluation.html` | Add Instant: no eval; no min trading days; Best Day of every profitable day. 1-Step: no min in eval or QPP; 50% Best Day of Positive Days’ Profit. 2-Step: 5 per eval phase; QPP 3 days. |
| `performance-reward.html` | Instant and 1-Step = **no min trading days**. “3 trading days” = **2-Step QPP only**. Drop first-only. |
| `terms.html` §8(b)/(c) | Keep “requirements vary by model.” Do not add a plan-by-plan day-count line. |
| `restricted-trading.html` | No day-count change unless a leftover 5-valid-day / 3-day Instant line appears. |
| `faq-news-trading.html` / `faq-general.html` | No day-count change unless a leftover Instant 5-valid-day line appears. |

---

## Alignment matrix

| Rule | TOS | Restricted trading | Plan pages | FAQ Plans | FAQ General | FAQ Qualified | FAQ News | Rewards |
|---|---|---|---|---|---|---|---|---|
| News every phase | Yes | Yes | Fix “Allowed in Evaluation” | Yes | n/a | Yes | Yes + Instant in table | n/a |
| No news window | Yes | Yes | Yes | Yes | n/a | Yes | Yes | n/a |
| No addon | Yes | Yes | Yes | Yes | n/a | Yes | Yes | n/a |
| Bracketing / gap banned | Yes | Yes | Yes | n/a | n/a | Yes | Yes | n/a |
| No 8(h) mix | Deleted | n/a | Not printed | “no min holding time” | **No** | n/a | n/a | n/a |
| $100 weekly / bi-weekly / on-demand | n/a | n/a | Yes | n/a | n/a | Yes (`p9`) | n/a | Yes |
| On-demand + plan min + cycle | n/a | n/a | Rewrite Eligibility | n/a | n/a | Yes (`p9`) + cycle list | n/a | **Rewrite p12** |
| Same rule first and later | n/a | n/a | Instant and 1-Step: no min days + Best Day; 2-Step QPP: 3 trading days | n/a | n/a | Delete 4-then-3 list; rewrite `p9`/`p12` | n/a | Instant / 1-Step no min days; 2-Step 3 |

`trading-objectives.html` is **in this pass** for Instant Best Day of every profitable day, 1-Step Best Day of every profitable day (do not mention 0.5%), Instant / 1-Step no-min-days stats, and 2-Step QPP **3 trading days**. Do not put Instant 0.5% on the 1-Step Best Day modal.

---

## Do not merge these clocks

- Instant **no min trading days** + **20% Best Day of Positive Days’ Profit** (0.5% is Instant-only) ≠ 1-Step **no min trading days** + **50% Best Day of Positive Days’ Profit** ≠ 2-Step QPP **3 trading days** ≠ 2-Step eval **5 trading days**. Never write “5 min trading days” or “5 valid trading days” on Instant. Do not put a 3-day min on 1-Step. First and later payouts on that plan use **that** rule **plus** the cycle.
- Weekly 7 calendar days and bi-weekly 14 calendar days are the cycle clock. The 3-day QPP min is a trading-day **count** on **2-Step** funded payouts only. Do not write it as “3 days between payouts,” and do not put it on Instant or 1-Step. Do not keep “first after 4 / later after 3.”
- 1-Step Best Day 50% of Positive Days’ Profit ≠ Instant Best Day 20% of Positive Days’ Profit. Instant’s 0.5% line stays on Instant only. Do not mention 0.5% on 1-Step.
- Challenge fee refund on first reward is eval plans only, not Instant. Add-ons are never part of that refund. That refund is not a different day rule.
