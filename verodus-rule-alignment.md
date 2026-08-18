# Verodus site rule alignment

Apply these rules on **every Verodus page that names them**, including `trading-objectives.html` (Instant 20% Best Day modal must say **every green day** is factored into Positive Days’ Profit; a day **meets the 0.5% parameter** only if it closes **more than 0.5% profit of account balance**). Update HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` **including** `trading-objectives.json` for Instant Best Day / day-count keys.

Canonical source: `1-step.html`, `2-step-lite.html`, `2-step-pro.html`, `instant.html`, `trading-objectives.html` Instant Best Day modal, TOS §9, `restricted-trading.html`.

Do **not** put Instant 0.5% language on the 1-Step 50% Best Day modal or on 2-Step pages.

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
  - **Instant:** **No minimum trading days.** Never write “5 min trading days,” “5 valid trading days,” or any Instant day-count. Instant’s day rule is **20% Best Day of every green day**. Every green day is factored into Positive Days’ Profit and Best Day (including small chip days such as +0.1% or +0.4%). A day **meets the 0.5% parameter** only if it closes **more than 0.5% profit of account balance** (not “at least”; exactly 0.5% does not meet the parameter). That 0.5% line is **not** a PDP filter — do **not** say chip days are excluded from Positive Days’ Profit. Best Day must be ≤20% of the sum of **all** green days. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The 20% cap still implies at least five green days (`1 ÷ n`); never list that as a 5-day checkbox. Instant has **no** 3-day QPP min. Same first payout and every payout after.
  - **1-Step Qualified Performance:** **No minimum trading days.** The day rule is **50% Best Day** (no 0.5% floor). Two equal green days can pass (50/50); that split is rare, so the clock is usually 3 days. Do **not** list a 3-day min. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. Evaluation also has **no** minimum trading days to pass. Do not put Instant 0.5% language on 1-Step.
  - **2-Step Lite / Pro Qualified Performance:** **3 minimum trading days** for every payout. Evaluation still needs **5 trading days per phase** (open and close the same calendar day). No Instant 20% / 0.5% language.
- A 2-Step “trading day” = open and close on the same calendar day. The 3-day QPP rule is **2-Step only** — a **count** of trading days in that payout window, not “wait 3 days since last payout.” Do not put it on 1-Step or Instant.
- Cycle (same for the first payout and every payout after). **$100** on every cycle:
  - **Weekly:** `$100` and 7 calendar days since the account start or last reward
  - **Bi-weekly:** `$100` and 14 calendar days since the account start or last reward
  - **On-demand** is **plan-specific**. Write only that plan’s rule. Never put 1-Step or 2-Step rules on Instant, and never put Instant Best Day / 0.5% language on 1-Step or 2-Step.
  - **Instant on-demand:** `$100` and Best Day ≤20% of **every green day**. Every green day is factored. A day meets the 0.5% parameter only if it closes **more than 0.5% profit of account balance**. No min trading days.
  - **1-Step on-demand:** `$100`. No minimum trading days. Best Day ≤50%.
  - **2-Step Lite / Pro on-demand:** `$100` and **3 trading days**.
- Do not add a first-vs-later split (e.g. “first after 4 days, later after 3”). Instant and 1-Step have no min trading days. The 3-day QPP min is **2-Step only**.

### Instant Best Day + 0.5% of account balance
Use **more than 0.5% profit of account balance**, not “at least 0.5%.”
- **Every green day** is factored into Positive Days’ Profit and Best Day, including +0.1% / +0.4% chip days. Chip days **dilute** Best Day and make 20% easier.
- A day **meets the 0.5% parameter** only if it closes **more than 0.5% profit of account balance**. Exactly 0.5% does **not** meet the parameter.
- Do **not** write that a +0.1% day is excluded from Positive Days’ Profit. The 0.5% line is only whether the day meets the parameter — it is **not** which days enter PDP.
- Best Day = the single largest **green** day. It must be ≤20% of the sum of **all** green days.
- Exceeding 20% is not a breach — keep trading until Best Day is ≤20% of total Positive Days’ Profit.
- Instant-only. Do not put this combo on 1-Step (50%, no 0.5% floor) or 2-Step.

### Do not change
- `$200,000` account sizes
- Weekend Holding Addon
- Instant 3% daily from day’s equity high, 6% trail that never locks
- 1-Step Best Day stays **50%** with **no** 0.5% floor and **no** listed 3-day min
- Instant Best Day stays **20% of every green day**. The 0.5% line is only which days **meet the parameter** (more than 0.5% profit of account balance), not which days enter PDP
- 2-Step evaluation still **5 trading days per phase**. Do not rewrite the 2-Step “5 Minimum Active Performance Days” eval modal into Instant 0.5% language.

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

**On-demand paste — use only the line for that page’s plan:**

```text
Instant: On-demand: $100. No minimum trading days. Best Day ≤20% of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance.
1-Step: On-demand: $100. No minimum trading days. Best Day ≤50%.
2-Step Lite / Pro: On-demand: $100 and 3 trading days.
```

Do **not** paste the Instant line onto 1-Step or 2-Step. Do **not** mention 1-Step or 2-Step on `instant.html`.

**Hub FAQ only** (Qualified Trader / Evaluation — pages that name every plan). Separate bullets, never one blended Instant sentence:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Weekly: $100 and 7 calendar days since account start or last reward</li>
    <li>Bi-weekly: $100 and 14 calendar days since account start or last reward</li>
    <li>On-demand on Instant: $100. No minimum trading days. Best Day ≤20% of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance</li>
    <li>On-demand on 1-Step: $100. No minimum trading days. Best Day ≤50%</li>
    <li>On-demand on 2-Step Lite / Pro: $100 and 3 trading days</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.`

**Replace with:**

```text
Payout spacing follows the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. Instant and 1-Step have no minimum trading days. On 2-Step Qualified Performance, every payout needs 3 trading days. The first payout and later payouts use the same rule.
```

**1-Step Eligibility** still says “at least 3 trading days since QPP / last payout.” **Delete that 3-day min.** 1-Step QPP uses `$100` + 50% Best Day + cycle. Two equal green days can pass; do not list a 3-day min. **2-Step Eligibility:** keep **3 trading days** as a count (plus `$100` + cycle), not “wait 3 days since last payout.” 2-Step eval stays 5 days per phase.

**Instant Eligibility (`instant.html` `li23` / `span47`) — replace the 3-day line.** Live:

> Eligibility: You become eligible for a reward only after both of the following are met: At least 3 trading days have passed since you received your Qualified Performance Account or since your last payout, and …

**Instant paste (`li23` / `span47`) — Instant only. No 1-Step or 2-Step words:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit from every green day, and you have met the selected cycle. Instant has no minimum trading days. Every green day is factored into Positive Days’ Profit. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. Weekly: $100 and 7 calendar days. Bi-weekly: $100 and 14 calendar days. On-demand: $100. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.
```

**1-Step Eligibility paste — 1-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. 1-Step has no minimum trading days. Weekly: $100 and 7 calendar days. Bi-weekly: $100 and 14 calendar days. On-demand: $100. No minimum trading days. Best Day ≤50%. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. The first payout and every payout after use this same rule.
```

**2-Step Lite / Pro Eligibility paste — 2-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. Weekly: $100 and 7 calendar days. Bi-weekly: $100 and 14 calendar days. On-demand: $100 and 3 trading days. The first payout and every payout after use this same rule.
```

Instant `li10` / `span21` — Instant has **no minimum trading days.** Delete the 5-valid-day / first-reward line. Do not replace it with “5 min trading days” or “5 valid trading days.”

```text
Minimum Trading Days: No minimum trading days.
```

Best Day stays in the Best Day block / modal (20% of **every green day**; a day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance).

`performance-reward.html` “First reward after 3 trading days” / “Min. 3 trading days” — keep **3 trading days** for **2-Step QPP only**. 1-Step and Instant have no min trading days. Drop the first/later split. Add `$100` + cycle.

`trading-objectives.html` — **edit Instant Best Day and Instant day-count copy.** See §8. Do not add Instant 0.5% to the 1-Step 50% Best Day modal.

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100, that plan’s payout rule, and the selected cycle (same rule for the first payout and every payout after).
```

On `trading-objectives.html`, Instant and 1-Step have **no min trading days**. Instant payout lines use `$100` + 20% Best Day of **every green day**. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. 1-Step payout lines use `$100` + 50% Best Day. 2-Step lines use **3 trading days** (every payout, not first-only). Instant Best Day modal still gets the 0.5% **parameter** sentence — not a PDP exclusion.

---

## 4. Soften FAQ “at any time” (on-demand)

**`content.p13` live:** `Payouts can be requested at any time through the dashboard once the following conditions are met:`

The list already has `$100` + min days. Optional paste:

```text
Payouts can be requested through the dashboard once the following conditions are met:
```

---

## 5. Instant — no min trading days; 20% Best Day of every green day

On Instant pages, say **only** Instant rules. Do not mention 1-Step or 2-Step day counts. Do not put Instant 20% / 0.5% language on 1-Step or 2-Step. Never write “5 min trading days,” “5 valid trading days,” or any Instant day-count.

`instant.html` Eligibility is wrong today. It still uses the 1-Step / 2-Step QPP **3 trading days** sentence. Instant has **no minimum trading days**. Instant’s day rule is **20% Best Day of every green day**. A day meets the 0.5% parameter only if it closes **more than 0.5% profit of account balance**. Do **not** say only those days count toward Positive Days’ Profit. Same first payout and every payout after.

| Key | Live | Change to |
|---|---|---|
| `li23` / `span47` | At least **3 trading days** since QPP account or last payout | `$100` + **Best Day ≤20% of every green day** + the selected cycle. A day meets the 0.5% parameter only if it closes **more than 0.5% profit of account balance**. No min trading days. |
| `li10` / `span21` | 5 valid days before your **first** reward | **No minimum trading days.** Delete the 5-day line. |

Delete the Instant “3 trading days since last payout” extra. Delete Instant 5-valid-day / 5-min-day lines. Do **not** add the 2-Step 3-day QPP min to Instant or 1-Step.

---

## 5b. 2-Step Qualified Performance — 3 trading days; 1-Step has no QPP day min

**1-Step QPP:** no minimum trading days. 50% Best Day is the 1-Step day rule. Two equal green days can pass; the clock is usually 3 days. Do not list a 3-day min. Delete the live “3 trading days since QPP / last payout” line on `1-step.html`.

**2-Step Lite / Pro QPP:** **3 trading days** (open and close the same calendar day) for every payout, first and later. Plus `$100` and the selected cycle. Do **not** write this as “3 trading days have passed since last payout.”

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
| Instant | No eval. Funded from day one. | **No min trading days.** **20% Best Day of every green day.** A day meets the 0.5% parameter only if it closes **more than 0.5% profit of account balance**. Chip days still count toward PDP. **No** 3-day QPP min. | Weekly 7 calendar / bi-weekly 14 calendar / on-demand = `$100` + Best Day |
| 1-Step | **No** minimum trading days to pass | **No** min days; **50% Best Day** (no 0.5% floor). Two equal days can pass; do not list a 3-day min. | Same cycles + `$100` |
| 2-Step Lite | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |
| 2-Step Pro | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |

A 2-Step “trading day” = open and close on the same calendar day. Instant and 1-Step have **no min trading days**. Instant: every green day is in PDP; a day meets the 0.5% parameter only if it closes **more than 0.5% profit of account balance**. Do not put Instant’s 0.5% language on 1-Step. Do not put the 2-Step 3-day QPP min on Instant or 1-Step. Do not put 2-Step’s **5 eval days** on 2-Step QPP payouts.

---

### `faq-evaluation.html`

**“How many trading days do I need for each program?”** — hardcoded list omits Instant.

**Replace the list with:**

```html
<ul>
    <li>Instant: No evaluation phase. No minimum trading days. Best Day ≤20% of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance.</li>
    <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance has no minimum trading days (50% Best Day applies).</li>
    <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
    <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

**`content.p5` (“What if I hit my targets before the minimum trading days?”)** live: one rule for everyone, open-and-close only. That is wrong for 1-Step eval (no min) and Instant (no min days; 20% Best Day of every green day). Split eval vs QPP.

**Paste `p5`:**

```text
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days in evaluation or Qualified Performance (50% Best Day applies). 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no minimum trading days and no profit target to “hit first”; you need $100, Best Day ≤20% of Positive Days’ Profit from every green day, and the selected payout cycle. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance.
```

Keep `p6` as the 2-Step / 1-Step calendar-day definition. Instant Best Day / 0.5% math stays on `instant.html`.

---

### `faq-qualified-trader.html`

News (`p1`, `p18`) is already plan-complete. Fix payout answers so they name each plan.

**`content.p9` paste (hub FAQ — separate sentences, not one Instant/1-Step/2-Step mash):**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: that plan’s payout rule and the selected cycle. On Instant, on-demand is $100 with no minimum trading days (Best Day ≤20% of every green day; a day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance). On 1-Step, on-demand is $100. No minimum trading days. Best Day ≤50%. On 2-Step Lite and 2-Step Pro Qualified Performance, on-demand is $100 and 3 trading days. Weekly is $100 and 7 calendar days. Bi-weekly is $100 and 14 calendar days. Every cycle has a $100 minimum.
```

**Delete** the hardcoded “First payout after 4 / subsequent after 3” list. Replace with:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Instant: no minimum trading days, Best Day ≤20% of every green day (a day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance), plus the cycle</li>
    <li>1-Step Qualified Performance: no minimum trading days, 50% Best Day, plus the cycle</li>
    <li>2-Step Lite / Pro Qualified Performance: 3 trading days, plus the cycle</li>
    <li>Every cycle: $100 · Weekly: 7 calendar days · Bi-weekly: 14 calendar days · On-demand: $100 and that plan’s rule</li>
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
    <li>On Instant: no minimum trading days; Best Day ≤20% of every green day (a day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance)</li>
    <li>On 1-Step Qualified Performance: $100. No minimum trading days. Best Day ≤50%</li>
    <li>On 2-Step Lite / Pro Qualified Performance: 3 trading days</li>
</ul>
```

**`content.p28` (fee refund)** live: yes for first reward, no Instant exception. **Paste:**

```text
Yes, on 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Add-ons are not refunded if they were purchased (Weekend Holding, Weekly, On-Demand, or any other add-on). Instant has no challenge-fee refund.
```

---

### `faq-plans.html`

Cards already name news + no holding time. Instant cards that still say 5 valid days must switch to **no min trading days** + 20% Best Day of every green day. Optional Instant (`p7`):

```text
Instant has no minimum trading days. Every Instant payout (first and later) needs $100, Best Day ≤20% of Positive Days’ Profit from every green day, and the selected cycle (weekly, bi-weekly, or on-demand). A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance.
```

Do not add the 2-Step 3-day QPP min to Instant or 1-Step cards. Optional 2-Step line:

```text
2-Step Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand).
```

Optional 1-Step line:

```text
1-Step Qualified Performance payouts (first and later) need $100, Best Day ≤50%, and the selected cycle. 1-Step has no minimum trading days.
```

---

### `faq-news-trading.html` and `faq-general.html`

Already aligned: news allowed on all four plans; holding time is No. No change required unless a leftover “addon” or “±2-minute” line comes back.

---

## 8. Apply on the rest of the site — including Instant Best Day modals

Live scan 17 Aug 2026. Same Instant sentence everywhere a 20% Best Day modal or Instant day-count appears. 2-Step QPP **3 trading days** only on 2-Step. 1-Step QPP has **no** 3-day min. Do not blend them.

### Instant 20% Best Day modal — 0.5% is the parameter, not a PDP filter

Use **more than 0.5% profit of account balance**. Add this only when the tab / page is Instant. Leave the 1-Step 50% Best Day modal unchanged (no 0.5% floor).

**`trading-objectives.html` `showModal('best-day')` — Instant branch.** Live first paragraph does not say which days enter PDP. After that paragraph, when `currentTab === 'instant'`, append:

```text
Every green day is factored into Positive Days’ Profit and Best Day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. Exactly 0.5% does not meet the parameter. Small green days still count toward Positive Days’ Profit.
```

JS paste for the Instant extra sentence (keep the existing first paragraph; add the second only if `isInstant`):

```javascript
if (isInstant) {
    contentEl.innerHTML += `<p>Every green day is factored into Positive Days’ Profit. A day meets the <strong style="color:${gold}">0.5% parameter</strong> only if it closes <strong style="color:${gold}">more than 0.5% profit of account balance</strong>. Exactly 0.5% does not meet the parameter. Small green days still count toward Positive Days’ Profit and Best Day.</p>`;
}
```

Do **not** add that sentence when `bestPctLimit === 50` (1-Step).

Do **not** keep this Instant modal line (it wrongly drops chip days from PDP):

> Only days that close more than 0.5% profit of account balance count toward Positive Days’ Profit and count as a day. A day that closes 0.5% or less does not count.

**`instant.html` Best Day modal** (hardcoded under `#bestDayModal`). Live first paragraph is the 20% rule only. Insert the same 0.5% **parameter** sentence after it:

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit at the time you request a payout. Every green day is factored into Positive Days' Profit. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. Exactly 0.5% does not meet the parameter. Small green days still count toward Positive Days' Profit.
```

Also on `instant.html` body copy (not only the modal):
- `content.li10` / `span21`: **No minimum trading days.** Delete 5-valid-day / first-reward copy.
- `content.p8` / `li12`–`li14`: every green day counts toward Positive Days’ Profit. Best Day ≤20% of that sum.
- `content.li15`: 0.5% is which days **meet the parameter**, not a min-days requirement and not a PDP exclusion.
- Hero / `li4` / `li9`: drop “5 valid trading days.” Instant has no min trading days. Best Day stays 20% of every green day.
- Eligibility `li23`: `$100` + Best Day ≤20% of every green day + cycle. **No** min trading days. **No** 3-day QPP min.

### `trading-objectives.html` — other Instant / QPP lines (same pass)

| Live | Change to |
|---|---|
| Instant card “Minimum Trading Days” = **5 Days** (`instantCardHTML` / `pricing.fiveDays`) | **Remove.** Instant has no min trading days. Show Best Day 20% only, or “None.” |
| Instant data `minDays:'5'` | Drop or unused. |
| `content.p8Instant`: First Payout after **5 trading days** | Every Instant payout: `$100` + Best Day ≤20% of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. No min trading days. Drop “first only.” |
| `content.p8`: First Payout after **3 trading days** (eval tabs) | **2-Step only:** every QPP payout `$100` + **3 trading days**. **1-Step:** `$100` + 50% Best Day; no min trading days. Drop “first only.” Not for Instant (`p8Instant` stays Instant-only). |
| Instant on-demand / “Anytime after min trading days” | Instant: `$100`. No min trading days. Best Day ≤20% of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. 1-Step: `$100`. No minimum trading days. Best Day ≤50%. 2-Step: `$100` + 3 trading days. |
| 1-Step Best Day modal (same `best-day` type, `bestPctLimit === 50`) | **No** 0.5% sentence. |
| 2-Step `trading-days` modal: 5 active days in **evaluation** | Keep as **eval** 5 days. Do not turn it into Instant 0.5%. QPP payouts on 2-Step are **3** days — say that on Eligibility / rewards, not in the eval modal. |

Locale: `/locales/*/pages/trading-objectives.json` and `common.json` keys used by the Instant card / `p8Instant` / Best Day strings.

### Site-wide apply list (where the same rules appear)

| Page | Apply |
|---|---|
| `instant.html` | **No min trading days.** 20% Best Day of every green day in the Best Day block **and** modal. 0.5% is the parameter only — do not exclude chip days from PDP. Drop 5-valid-day lines and the 3-day QPP Eligibility sentence. `$100` + cycle. |
| `1-step.html` | QPP Eligibility: **no min trading days** + `$100` + 50% Best Day + cycle. Delete the 3-day QPP line. Eval: no min days. **No** Instant 0.5%. |
| `2-step-lite.html` / `2-step-pro.html` | Eval: **5** trading days per phase. QPP Eligibility: **3 trading days** + `$100` + cycle. **No** Instant 20% / 0.5%. |
| `trading-objectives.html` | Instant Best Day modal + Instant card / `p8Instant` as above. 1-Step `p8` = no min days. 2-Step `p8` = 3 QPP days every payout. |
| `faq-plans.html` `p7` | Instant: no min trading days. 20% Best Day of every green day. A day meets the 0.5% parameter only if it closes more than 0.5% profit of account balance. |
| `faq-plans.html` 1-Step / 2-Step cards | 1-Step QPP: no min days. 2-Step QPP: 3 trading days. Do not put Instant 0.5% on those cards. |
| `faq-qualified-trader.html` | Delete 4-then-3. Instant = no min days + Best Day of every green day + 0.5% parameter. 1-Step QPP = no min days + 50% Best Day. 2-Step QPP = 3 trading days. Same first and later. |
| `faq-evaluation.html` | Add Instant: no eval; no min trading days; Best Day of every green day + 0.5% parameter. 1-Step: no min in eval or QPP. 2-Step: 5 per eval phase; QPP 3 days. |
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

`trading-objectives.html` is **in this pass** for Instant Best Day of every green day + 0.5% parameter, Instant / 1-Step no-min-days stats, and 2-Step QPP **3 trading days**. Do not put Instant 0.5% on the 1-Step Best Day modal.

---

## Do not merge these clocks

- Instant **no min trading days** + **20% Best Day of every green day** (0.5% is the parameter only) ≠ 1-Step **no min trading days** + **50% Best Day** ≠ 2-Step QPP **3 trading days** ≠ 2-Step eval **5 trading days**. Never write “5 min trading days” or “5 valid trading days” on Instant. Do not put a 3-day min on 1-Step. First and later payouts on that plan use **that** rule **plus** the cycle.
- Weekly 7 calendar days and bi-weekly 14 calendar days are the cycle clock. The 3-day QPP min is a trading-day **count** on **2-Step** funded payouts only. Do not write it as “3 days between payouts,” and do not put it on Instant or 1-Step. Do not keep “first after 4 / later after 3.”
- 1-Step Best Day 50% (no 0.5% floor) ≠ Instant Best Day 20% of every green day. Instant’s 0.5% line is which days **meet the parameter**, not which days enter PDP.
- Challenge fee refund on first reward is eval plans only, not Instant. Add-ons are never part of that refund. That refund is not a different day rule.
