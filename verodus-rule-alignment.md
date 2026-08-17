# Verodus site rule alignment

**Do not edit `trading-objectives.html`.** Leave that page as it is. This pass aligns the rest of the site to the plan pages and TOS.

Canonical source: `1-step.html`, `2-step-lite.html`, `2-step-pro.html`, `instant.html`, TOS §9, `restricted-trading.html`.

Update HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` except `trading-objectives.json`.

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
- **$100** minimum for **weekly, bi-weekly, and on-demand**.
- **First and subsequent payouts are the same.** No “first after X days, later after Y.” Every request must meet **that plan’s payout rule** **and** the **selected cycle**.
- Plan payout rules (same for every payout on that plan):
  - **Instant:** **20% Best Day.** Only days that close **more than 0.5%** net profit (vs that day’s start-of-day equity) count toward Positive Days’ Profit. Best Day must be ≤20% of that PDP. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. Do **not** keep a separate “5 valid days” checkbox; the 0.5% floor plus 20% Best Day is the Instant day rule. Instant has **no** 3-day QPP min.
  - **1-Step Qualified Performance:** **3 minimum trading days** for every payout, plus **50% Best Day** (no 0.5% floor). Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. Evaluation still has **no** minimum trading days to pass.
  - **2-Step Lite / Pro Qualified Performance:** **3 minimum trading days** for every payout. Evaluation still needs **5 trading days per phase** (open and close the same calendar day). No Instant 20% / 0.5% language.
- A 1-Step / 2-Step “trading day” = open and close on the same calendar day. The 3-day QPP rule is a **count of trading days** in that payout window, not “wait 3 days since last payout.”
- Cycle (same for the first payout and every payout after):
  - **Weekly:** 7 calendar days since the account start or last reward
  - **Bi-weekly:** 14 calendar days since the account start or last reward
  - **On-demand** is **plan-specific**. Write only that plan’s rule. Never put 1-Step or 2-Step rules on Instant, and never put Instant Best Day / 0.5% language on 1-Step or 2-Step.
  - **Instant on-demand:** `$100` and Best Day ≤20% (only days that closed **more than 0.5%** count).
  - **1-Step on-demand:** `$100` and **3 trading days** (50% Best Day still applies).
  - **2-Step Lite / Pro on-demand:** `$100` and **3 trading days**.
- Do not add a first-vs-later split (e.g. “first after 4 days, later after 3”). Plan rule + cycle is the whole rule. The 3-day QPP min is the 1-Step / 2-Step payout day-count, not a separate “days between payouts” clock on Instant.

### Instant Best Day + 0.5% (how the two rules work together)
Use **more than 0.5%**, not “at least 0.5%.”
- A day that closes +0.1% does **not** count toward Positive Days’ Profit.
- A day that closes more than 0.5% **does** count.
- Best Day = the single largest of those counted days. It must be ≤20% of the sum of counted days.
- Even counted days (each more than 0.5%): you typically need **at least 5** such days (4 equal counted days = 25% Best Day). Uneven days need more. A day that closes exactly 0.5% does **not** count.
- Instant-only. Do not put this combo on 1-Step (50%, no 0.5% floor) or 2-Step.

### Do not change
- `trading-objectives.html` (and `/locales/*/pages/trading-objectives.json`) — **no edits**
- `$200,000` account sizes
- Weekend Holding Addon
- Instant 3% daily from day’s equity high, 6% trail that never locks
- 1-Step Best Day stays **50%** with **no** 0.5% floor
- Instant Best Day stays **20%**; the new piece is only which days count (more than 0.5%)

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
Instant: On-demand: $100 and Best Day ≤20% of Positive Days’ Profit (only days that closed more than 0.5% net profit count).
1-Step: On-demand: $100 and 3 trading days.
2-Step Lite / Pro: On-demand: $100 and 3 trading days.
```

Do **not** paste the Instant line onto 1-Step or 2-Step. Do **not** mention 1-Step or 2-Step on `instant.html`.

**Hub FAQ only** (Qualified Trader / Evaluation — pages that name every plan). Separate bullets, never one blended Instant sentence:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Weekly: 7 calendar days since account start or last reward</li>
    <li>Bi-weekly: 14 calendar days since account start or last reward</li>
    <li>On-demand on Instant: $100 and Best Day ≤20% (only days that closed more than 0.5% count)</li>
    <li>On-demand on 1-Step: $100 and 3 trading days</li>
    <li>On-demand on 2-Step Lite / Pro: $100 and 3 trading days</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.`

**Replace with:**

```text
Payout spacing follows the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. On 1-Step and 2-Step Qualified Performance, every payout also needs 3 trading days. Instant uses Best Day, not a 3-day min. The first payout and later payouts use the same rule.
```

**1-Step / 2-Step Eligibility** still says “at least 3 trading days since QPP / last payout.” Keep the **3 trading days**, but rewrite it as a **minimum trading-day count** for Qualified Performance payouts (plus `$100` + cycle), not “wait 3 days since last payout.” Evaluation mins stay separate (1-Step: no min to pass; 2-Step: 5 days per phase).

**Instant Eligibility (`instant.html` `li23` / `span47`) — replace the 3-day line.** Live:

> Eligibility: You become eligible for a reward only after both of the following are met: At least 3 trading days have passed since you received your Qualified Performance Account or since your last payout, and …

**Instant paste (`li23` / `span47`) — Instant only. No 1-Step or 2-Step words:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, your Best Day is ≤20% of Positive Days’ Profit (only days with more than 0.5% net profit count), and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and Best Day ≤20% on days that closed more than 0.5%. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.
```

**1-Step Eligibility paste — 1-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and 3 trading days. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. The first payout and every payout after use this same rule.
```

**2-Step Lite / Pro Eligibility paste — 2-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and 3 trading days. The first payout and every payout after use this same rule.
```

Instant `li10` — drop the standalone “5 valid days” / “first reward” line. Replace with Best Day + 0.5% count (every Instant payout).

```text
Best Day: Your Best Day must be ≤20% of Positive Days’ Profit. Only days that close more than 0.5% net profit count toward Positive Days’ Profit. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. The first payout and every payout after use this same rule.
```

`performance-reward.html` “First reward after 3 trading days” / “Min. 3 trading days” — keep **3 trading days** for **1-Step and 2-Step QPP only**. Drop the first/later split. Add `$100` + cycle. Do not put this 3-day min on Instant.

`trading-objectives.html` — **do not edit.**

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100, that plan’s payout rule, and the selected cycle (same rule for the first payout and every payout after).
```

Do not change on-demand copy on `trading-objectives.html`.

---

## 4. Soften FAQ “at any time” (on-demand)

**`content.p13` live:** `Payouts can be requested at any time through the dashboard once the following conditions are met:`

The list already has `$100` + min days. Optional paste:

```text
Payouts can be requested through the dashboard once the following conditions are met:
```

---

## 5. Instant Eligibility — 20% Best Day; a day counts only if more than 0.5%

On Instant pages, say **only** Instant rules. Do not mention 1-Step or 2-Step day counts. Do not put Instant 20% / 0.5% language on 1-Step or 2-Step.

`instant.html` Eligibility is wrong today. It still uses the QPP **3 trading days** sentence. Instant’s payout rule is **20% Best Day**, and **only days with more than 0.5% net profit count**. Drop the separate “5 valid days” checkbox.

| Key | Live | Change to |
|---|---|---|
| `li23` / `span47` | At least **3 trading days** since QPP account or last payout | `$100` + **Best Day ≤20%** (only days **more than 0.5%** count) **and** the selected cycle |
| `li10` / `span21` | 5 valid days before your **first** reward | **20% Best Day** for **every** payout; only days **more than 0.5%** count |

Delete the “3 trading days since last payout” Instant extra. Do not keep 5-then-3. Do not keep “5 valid days” as a second Instant clock. Do **not** add the 1-Step / 2-Step 3-day QPP min to Instant.

---

## 5b. 1-Step / 2-Step Qualified Performance — 3 trading days for every payout

On 1-Step and 2-Step pages, Qualified Performance payouts need **3 trading days** (open and close the same calendar day). Same number for the first payout and every payout after. Plus `$100` and the selected cycle.

Do **not** write this as “3 trading days have passed since last payout.” It is a **count** of trading days in that payout window.

Keep evaluation separate:
- **1-Step evaluation:** no minimum trading days to pass. **50% Best Day** still applies in QPP.
- **2-Step Lite / Pro evaluation:** 5 trading days per phase. QPP payouts are **3**, not 5.

Do not put Instant Best Day / 0.5% language on these pages.

---

## 6. Empty locale keys (cleanup, not visible)

Leave `trading-objectives.json` alone. Elsewhere, delete or leave blank:

- TOS: `content.h38`, `p51`, `p52`, `p53`
- Restricted trading: `p9`, `p18`
- 1-step `li42`; 2-step lite/pro `li38`; instant `li43`
- `common.json` `pricing.addonFootnote` (already empty)

---

## 7. FAQs — one answer per plan (do not blend clocks)

FAQs that name “the evaluation” or one day number for all accounts are wrong. Split Instant / 1-Step / 2-Step. Skip `trading-objectives.html`.

### Plan cheat sheet (use in every payout / days FAQ)

| Plan | Eval / pass min days | QPP / payout rule (every payout) | Cycle |
|---|---|---|---|
| Instant | No eval. Funded from day one. | **20% Best Day**; only days **more than 0.5%** net count toward PDP. **No** 3-day QPP min. | Weekly 7 calendar / bi-weekly 14 calendar / on-demand = `$100` + that Best Day rule |
| 1-Step | **No** minimum trading days to pass | **3 trading days** + **50% Best Day** (no 0.5% floor) | Same cycles + `$100` |
| 2-Step Lite | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |
| 2-Step Pro | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |

A 1-Step / 2-Step “trading day” = open and close on the same calendar day. An Instant counted day = that day closes **more than 0.5%** net. Do not describe Instant days as open-and-close only. Do not put Instant’s 0.5% floor on 1-Step. Do not put the 3-day QPP min on Instant. Do not put 2-Step’s **5 eval days** on QPP payouts.

---

### `faq-evaluation.html`

**“How many trading days do I need for each program?”** — hardcoded list omits Instant.

**Replace the list with:**

```html
<ul>
    <li>Instant: No evaluation phase. Best Day ≤20% of Positive Days’ Profit; only days that close more than 0.5% net profit count. No separate day-count.</li>
    <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance payouts need 3 trading days.</li>
    <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
    <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

**`content.p5` (“What if I hit my targets before the minimum trading days?”)** live: one rule for everyone, open-and-close only. That is wrong for 1-Step eval (no min) and Instant (Best Day + 0.5% count). Split eval vs QPP.

**Paste `p5`:**

```text
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days to pass evaluation; Qualified Performance payouts need 3 trading days. 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no profit target to “hit first”; you need $100, Best Day ≤20% of Positive Days’ Profit (only days with more than 0.5% net profit count), and the selected payout cycle.
```

Keep `p6` as the 2-Step / 1-Step calendar-day definition. Instant Best Day / 0.5% math stays on `instant.html`.

---

### `faq-qualified-trader.html`

News (`p1`, `p18`) is already plan-complete. Fix payout answers so they name each plan.

**`content.p9` paste (hub FAQ — separate sentences, not one Instant/1-Step/2-Step mash):**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: that plan’s payout rule and the selected cycle. On Instant, on-demand is $100 and Best Day ≤20% (only days that closed more than 0.5% count). On 1-Step and on 2-Step Lite / Pro Qualified Performance, on-demand is $100 and 3 trading days. Weekly is 7 calendar days. Bi-weekly is 14 calendar days.
```

**Delete** the hardcoded “First payout after 4 / subsequent after 3” list. Replace with:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Instant: Best Day ≤20% (only days more than 0.5% count), plus the cycle. No 3-day QPP min.</li>
    <li>1-Step Qualified Performance: 3 trading days, 50% Best Day, plus the cycle</li>
    <li>2-Step Lite / Pro Qualified Performance: 3 trading days, plus the cycle</li>
    <li>Weekly: 7 calendar days · Bi-weekly: 14 calendar days · On-demand: $100 and that plan’s rule</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.` **Replace with:**

```text
Payout spacing is the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. 1-Step and 2-Step Qualified Performance also need 3 trading days on every payout. Instant on-demand still needs Best Day ≤20% on days that closed more than 0.5%, not a 3-day min. First and later payouts use the same rule.
```

**`content.p13` + on-demand list** — drop “at any time.” Paste list:

```html
<ul>
    <li>$100 since last reward</li>
    <li>On Instant: Best Day ≤20% (only days that closed more than 0.5% count)</li>
    <li>On 1-Step Qualified Performance: 3 trading days</li>
    <li>On 2-Step Lite / Pro Qualified Performance: 3 trading days</li>
</ul>
```

**`content.p28` (fee refund)** live: yes for first reward, no Instant exception. **Paste:**

```text
Yes, on 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Add-ons are not refunded if they were purchased (Weekend Holding, Weekly, On-Demand, or any other add-on). Instant has no challenge-fee refund.
```

---

### `faq-plans.html`

Cards already name news + no holding time. Instant cards that still say “5 valid +0.5% days” should switch to 20% Best Day + more-than-0.5% count. Optional Instant (`p7`):

```text
Every Instant payout (first and later) needs $100, Best Day ≤20% of Positive Days’ Profit (only days with more than 0.5% net profit count), and the selected cycle (weekly, bi-weekly, or on-demand).
```

Do not add the 1-Step / 2-Step 3-day QPP min to Instant cards. Optional 1-Step / 2-Step line:

```text
Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand).
```

---

### `faq-news-trading.html` and `faq-general.html`

Already aligned: news allowed on all four plans; holding time is No. No change required unless a leftover “addon” or “±2-minute” line comes back.

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
| Same rule first and later | n/a | n/a | 1-Step / 2-Step QPP: 3 trading days (not “since last payout”); Instant: Best Day, no 3-day min | n/a | n/a | Delete 4-then-3 list; rewrite `p9`/`p12` | n/a | 3 days = 1-Step / 2-Step QPP min, not Instant |

`trading-objectives.html` is **out of this pass**. Do not use this matrix to change it.

---

## Do not merge these clocks

- Instant 20% Best Day + more-than-0.5% count ≠ 1-Step / 2-Step QPP **3 trading days** ≠ 2-Step eval **5 trading days** ≠ 1-Step eval **no min days**. Each plan keeps its own rule; first and later payouts on that plan use **that** rule **plus** the cycle.
- Weekly 7 calendar days and bi-weekly 14 calendar days are the cycle clock. The 3-day QPP min is a trading-day **count** on 1-Step and 2-Step funded payouts. Do not write it as “3 days between payouts,” and do not put it on Instant. Do not keep “first after 4 / later after 3.”
- 1-Step Best Day 50% (no 0.5% floor) ≠ Instant Best Day 20% (only days more than 0.5% count).
- Challenge fee refund on first reward is eval plans only, not Instant. Add-ons are never part of that refund. That refund is not a different day rule.
