# Verodus site rule alignment

Apply these rules on **every Verodus page that names them**, including `trading-objectives.html` (Instant 20% Best Day modal must say a day counts only if it closes **more than 0.5%**). Update HTML **and** `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…` **including** `trading-objectives.json` for Instant Best Day / day-count keys.

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
- **$100** minimum for **weekly, bi-weekly, and on-demand**.
- **First and subsequent payouts are the same.** No “first after X days, later after Y.” Every request must meet **that plan’s payout rule** **and** the **selected cycle**.
- Plan payout rules (same for every payout on that plan):
  - **Instant Qualified Performance:** **5 valid trading days** for every payout (first and later). Say it simply. Never write “5 min trading days” on Instant. Do **not** mash Best Day into that line. Separate rule: **20% Best Day** — only days that close **more than 0.5%** net profit (vs that day’s start-of-day equity) count toward Positive Days’ Profit. Best Day must be ≤20% of that PDP. Exceeding 20% is not a breach — keep trading until Best Day is ≤20%. Instant has **no** 3-day QPP min.
  - **1-Step Qualified Performance:** **3 minimum trading days** for every payout, plus **50% Best Day** (no 0.5% floor). Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. Evaluation still has **no** minimum trading days to pass.
  - **2-Step Lite / Pro Qualified Performance:** **3 minimum trading days** for every payout. Evaluation still needs **5 trading days per phase** (open and close the same calendar day). No Instant 20% / 0.5% language.
- A 1-Step / 2-Step “trading day” = open and close on the same calendar day. The 3-day QPP rule is a **count of trading days** in that payout window, not “wait 3 days since last payout.”
- Cycle (same for the first payout and every payout after):
  - **Weekly:** 7 calendar days since the account start or last reward
  - **Bi-weekly:** 14 calendar days since the account start or last reward
  - **On-demand** is **plan-specific**. Write only that plan’s rule. Never put 1-Step or 2-Step rules on Instant, and never put Instant Best Day / 0.5% language on 1-Step or 2-Step.
  - **Instant on-demand:** `$100` and **5 valid trading days**.
  - **1-Step on-demand:** `$100` and **3 trading days** (50% Best Day still applies).
  - **2-Step Lite / Pro on-demand:** `$100` and **3 trading days**.
- Do not add a first-vs-later split (e.g. “first after 4 days, later after 3”). Instant 5 valid trading days applies to the first reward and every reward after. The 3-day QPP min is 1-Step / 2-Step only.

### Instant Best Day + 0.5% (how the two rules work together)
Use **more than 0.5%**, not “at least 0.5%.”
- A day that closes +0.1% does **not** count toward Positive Days’ Profit.
- A day that closes more than 0.5% **does** count.
- Best Day = the single largest of those counted days. It must be ≤20% of the sum of counted days.
- Even counted days (each more than 0.5%): you typically need **at least 5** such days (4 equal counted days = 25% Best Day). Uneven days need more. A day that closes exactly 0.5% does **not** count.
- Instant-only. Do not put this combo on 1-Step (50%, no 0.5% floor) or 2-Step.

### Do not change
- `$200,000` account sizes
- Weekend Holding Addon
- Instant 3% daily from day’s equity high, 6% trail that never locks
- 1-Step Best Day stays **50%** with **no** 0.5% floor
- Instant Best Day stays **20%**; the new piece is only which days count (more than 0.5%)
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
Instant: On-demand: $100 and 5 valid trading days.
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
    <li>On-demand on Instant: $100 and 5 valid trading days</li>
    <li>On-demand on 1-Step: $100 and 3 trading days</li>
    <li>On-demand on 2-Step Lite / Pro: $100 and 3 trading days</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.`

**Replace with:**

```text
Payout spacing follows the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. On Instant, every payout needs 5 valid trading days. On 1-Step and 2-Step Qualified Performance, every payout needs 3 trading days. The first payout and later payouts use the same rule.
```

**1-Step / 2-Step Eligibility** still says “at least 3 trading days since QPP / last payout.” Keep the **3 trading days**, but rewrite it as a **minimum trading-day count** for Qualified Performance payouts (plus `$100` + cycle), not “wait 3 days since last payout.” Evaluation mins stay separate (1-Step: no min to pass; 2-Step: 5 days per phase).

**Instant Eligibility (`instant.html` `li23` / `span47`) — replace the 3-day line.** Live:

> Eligibility: You become eligible for a reward only after both of the following are met: At least 3 trading days have passed since you received your Qualified Performance Account or since your last payout, and …

**Instant paste (`li23` / `span47`) — Instant only. No 1-Step or 2-Step words:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 5 valid trading days, and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and 5 valid trading days. The first payout and every payout after use this same rule.
```

**1-Step Eligibility paste — 1-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, your Best Day is ≤50% of Positive Days’ Profit, and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and 3 trading days. Exceeding 50% is not a breach — keep trading until Best Day is ≤50%. The first payout and every payout after use this same rule.
```

**2-Step Lite / Pro Eligibility paste — 2-Step only:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met 3 trading days in Qualified Performance, and you have met the selected cycle. Weekly: 7 calendar days. Bi-weekly: 14 calendar days. On-demand: $100 and 3 trading days. The first payout and every payout after use this same rule.
```

Instant `li10` / `span21` — **keep 5 valid trading days.** Drop only “before your first reward.” Same 5 for every Instant payout. Do not put Best Day in this line.

```text
Minimum Trading Days: 5 valid trading days.
```

Best Day stays in the Best Day block / modal (20%, only days more than 0.5% count). Do not merge it into `li10`.

`performance-reward.html` “First reward after 3 trading days” / “Min. 3 trading days” — keep **3 trading days** for **1-Step and 2-Step QPP only**. Drop the first/later split. Add `$100` + cycle. Do not put this 3-day min on Instant.

`trading-objectives.html` — **edit Instant Best Day and Instant day-count copy.** See §8. Do not add Instant 0.5% to the 1-Step 50% Best Day modal.

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100, that plan’s payout rule, and the selected cycle (same rule for the first payout and every payout after).
```

On `trading-objectives.html`, Instant payout / on-demand lines use **5 valid trading days** (every payout, not first-only). 1-Step / 2-Step lines use **3 trading days** (every payout, not first-only). Instant Best Day modal still gets the 0.5% day-count sentence.

---

## 4. Soften FAQ “at any time” (on-demand)

**`content.p13` live:** `Payouts can be requested at any time through the dashboard once the following conditions are met:`

The list already has `$100` + min days. Optional paste:

```text
Payouts can be requested through the dashboard once the following conditions are met:
```

---

## 5. Instant QPP — 5 valid trading days (simple); Best Day stays separate

On Instant pages, say **only** Instant rules. Do not mention 1-Step or 2-Step day counts. Do not put Instant 20% / 0.5% language on 1-Step or 2-Step.

`instant.html` Eligibility is wrong today. It still uses the 1-Step / 2-Step QPP **3 trading days** sentence. Instant QPP is **5 valid trading days**, first reward and every reward after. Say that simply. Best Day (20%, more than 0.5% counts) stays in the Best Day block / modal — not inside `li10`.

| Key | Live | Change to |
|---|---|---|
| `li23` / `span47` | At least **3 trading days** since QPP account or last payout | `$100` + **5 valid trading days** + the selected cycle. Same first and later. |
| `li10` / `span21` | 5 valid days before your **first** reward | **5 valid trading days.** Drop “first reward” only. |

Delete the Instant “3 trading days since last payout” extra. Do **not** add the 1-Step / 2-Step 3-day QPP min to Instant.

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
| Instant | No eval. Funded from day one. | **5 valid trading days** (same first and later). Separate: **20% Best Day**; only days **more than 0.5%** count toward PDP. **No** 3-day QPP min. | Weekly 7 calendar / bi-weekly 14 calendar / on-demand = `$100` + 5 valid trading days |
| 1-Step | **No** minimum trading days to pass | **3 trading days** + **50% Best Day** (no 0.5% floor) | Same cycles + `$100` |
| 2-Step Lite | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |
| 2-Step Pro | **5** trading days per phase | **3 trading days** | Same cycles + `$100` |

A 1-Step / 2-Step “trading day” = open and close on the same calendar day. Instant QPP min days = **5 valid trading days** (simple). Instant Best Day counted day = closes **more than 0.5%** net. Do not put Instant’s 0.5% floor on 1-Step. Do not put the 3-day QPP min on Instant. Do not put 2-Step’s **5 eval days** on 2-Step QPP payouts.

---

### `faq-evaluation.html`

**“How many trading days do I need for each program?”** — hardcoded list omits Instant.

**Replace the list with:**

```html
<ul>
    <li>Instant: No evaluation phase. Qualified Performance: 5 valid trading days (first payout and every payout after). Best Day ≤20%; only days that close more than 0.5% net profit count toward that rule.</li>
    <li>1-Step: No minimum trading days to pass evaluation. Qualified Performance payouts need 3 trading days.</li>
    <li>2-Step Lite: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
    <li>2-Step Pro: 5 trading days per evaluation phase (open and close on the same calendar day). Qualified Performance payouts need 3 trading days.</li>
</ul>
```

**`content.p5` (“What if I hit my targets before the minimum trading days?”)** live: one rule for everyone, open-and-close only. That is wrong for 1-Step eval (no min) and Instant (5 valid trading days + Best Day). Split eval vs QPP.

**Paste `p5`:**

```text
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days to pass evaluation; Qualified Performance payouts need 3 trading days. 2-Step Lite and 2-Step Pro need 5 trading days per evaluation phase (open and close the same calendar day); Qualified Performance payouts need 3 trading days. Instant has no profit target to “hit first”; you need $100, 5 valid trading days, and the selected payout cycle.
```

Keep `p6` as the 2-Step / 1-Step calendar-day definition. Instant Best Day / 0.5% math stays on `instant.html`.

---

### `faq-qualified-trader.html`

News (`p1`, `p18`) is already plan-complete. Fix payout answers so they name each plan.

**`content.p9` paste (hub FAQ — separate sentences, not one Instant/1-Step/2-Step mash):**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: that plan’s payout rule and the selected cycle. On Instant, on-demand is $100 and 5 valid trading days. On 1-Step and on 2-Step Lite / Pro Qualified Performance, on-demand is $100 and 3 trading days. Weekly is 7 calendar days. Bi-weekly is 14 calendar days.
```

**Delete** the hardcoded “First payout after 4 / subsequent after 3” list. Replace with:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, that plan’s payout rule, and the cycle</li>
    <li>Instant: 5 valid trading days, plus the cycle. No 3-day QPP min.</li>
    <li>1-Step Qualified Performance: 3 trading days, 50% Best Day, plus the cycle</li>
    <li>2-Step Lite / Pro Qualified Performance: 3 trading days, plus the cycle</li>
    <li>Weekly: 7 calendar days · Bi-weekly: 14 calendar days · On-demand: $100 and that plan’s rule</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.` **Replace with:**

```text
Payout spacing is the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or that plan’s payout rule for on-demand. Instant also needs 5 valid trading days on every payout. 1-Step and 2-Step Qualified Performance also need 3 trading days on every payout. First and later payouts use the same rule.
```

**`content.p13` + on-demand list** — drop “at any time.” Paste list:

```html
<ul>
    <li>$100 since last reward</li>
    <li>On Instant: 5 valid trading days</li>
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

Cards already name news + no holding time. Instant QPP min days stay **5 valid trading days** (simple). Best Day / 0.5% stays on the Instant rules page and modal, not in this min-days line. Optional Instant (`p7`):

```text
Every Instant payout (first and later) needs $100, 5 valid trading days, and the selected cycle (weekly, bi-weekly, or on-demand).
```

Do not add the 1-Step / 2-Step 3-day QPP min to Instant cards. Optional 1-Step / 2-Step line:

```text
Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand).
```

---

### `faq-news-trading.html` and `faq-general.html`

Already aligned: news allowed on all four plans; holding time is No. No change required unless a leftover “addon” or “±2-minute” line comes back.

---

## 8. Apply on the rest of the site — including Instant Best Day modals

Live scan 17 Aug 2026. Same Instant sentence everywhere a 20% Best Day modal or Instant day-count appears. Same 1-Step / 2-Step QPP **3 trading days** everywhere those plans name payout days. Do not blend them.

### Instant 20% Best Day modal — add the 0.5% day-count (required)

Use **more than 0.5%**. Add this only when the tab / page is Instant. Leave the 1-Step 50% Best Day modal unchanged (no 0.5% floor).

**`trading-objectives.html` `showModal('best-day')` — Instant branch.** Live first paragraph does not say which days count. After that paragraph, when `currentTab === 'instant'`, append:

```text
Only days that close more than 0.5% net profit (vs that day’s start-of-day equity) count toward Positive Days’ Profit and count as a day. A day that closes 0.5% or less does not count.
```

JS paste for the Instant extra sentence (keep the existing first paragraph; add the second only if `isInstant`):

```javascript
if (isInstant) {
    contentEl.innerHTML += `<p>Only days that close <strong style="color:${gold}">more than 0.5%</strong> net profit (vs that day’s start-of-day equity) count toward Positive Days’ Profit and count as a day. A day that closes 0.5% or less does not count.</p>`;
}
```

Do **not** add that sentence when `bestPctLimit === 50` (1-Step).

**`instant.html` Best Day modal** (hardcoded under `#bestDayModal`). Live first paragraph is the 20% rule only. Insert the same 0.5% sentence after it:

```text
The Best Day Rule requires that your most profitable day ("Best Day") does not exceed 20% of your Positive Days' Profit at the time you request a payout. Profits are calculated from closed trades at the end of each trading day (00:00 UTC). Exceeding this is not a breach — you must continue trading to add more profit until the Best Day is ≤20% of total Positive Days' Profit. Only days that close more than 0.5% net profit (vs that day’s start-of-day equity) count toward Positive Days’ Profit and count as a day. A day that closes 0.5% or less does not count.
```

Also on `instant.html` body copy (not only the modal):
- `content.li10` / `span21`: **5 valid trading days.** Drop “before your first reward.” Same 5 for every payout. Do not add Best Day to this line.
- `content.p8` / `li12`–`li14`: add that only days **more than 0.5%** count toward Positive Days’ Profit.
- `content.li15`: 0.5% is the Best Day day-count, not a second min-days speech. Keep `li10` as the simple 5 valid trading days line.
- Hero / `li4` / `li9`: Instant QPP min is **5 valid trading days**. Best Day stays 20%.
- Eligibility `li23`: `$100` + **5 valid trading days** + cycle. **No** 3-day QPP min.

### `trading-objectives.html` — other Instant / QPP lines (same pass)

| Live | Change to |
|---|---|
| Instant card “Minimum Trading Days” = **5 Days** (`instantCardHTML` / `pricing.fiveDays`) | **Keep.** Instant QPP is 5 valid trading days. Drop “first only” if the card implies first payout only. |
| Instant data `minDays:'5'` | Keep. |
| `content.p8Instant`: First Payout after **5 trading days** | Every Instant payout: `$100` + **5 valid trading days**. Drop “first only.” |
| `content.p8`: First Payout after **3 trading days** (1-Step / 2-Step) | Every 1-Step / 2-Step QPP payout: `$100` + **3 trading days**. Drop “first only.” This 3-day line is **not** for Instant (`p8Instant` stays Instant-only). |
| Instant on-demand / “Anytime after min trading days” | Instant: `$100` + 5 valid trading days. 1-Step / 2-Step: `$100` + 3 trading days. |
| 1-Step Best Day modal (same `best-day` type, `bestPctLimit === 50`) | **No** 0.5% sentence. |
| 2-Step `trading-days` modal: 5 active days in **evaluation** | Keep as **eval** 5 days. Do not turn it into Instant 0.5%. QPP payouts on 2-Step are **3** days — say that on Eligibility / rewards, not in the eval modal. |

Locale: `/locales/*/pages/trading-objectives.json` and `common.json` keys used by the Instant card / `p8Instant` / Best Day strings.

### Site-wide apply list (where the same rules appear)

| Page | Apply |
|---|---|
| `instant.html` | QPP: **5 valid trading days** (simple, first and later) in `li10` / Eligibility. 20% Best Day + more-than-0.5% count in the Best Day block **and** modal. Drop the 3-day QPP Eligibility sentence. `$100` + cycle. |
| `1-step.html` | QPP Eligibility: **3 trading days** (count, not “since last payout”) + `$100` + 50% Best Day + cycle. Eval: no min days. **No** Instant 0.5%. |
| `2-step-lite.html` / `2-step-pro.html` | Eval: **5** trading days per phase. QPP Eligibility: **3 trading days** + `$100` + cycle. **No** Instant 20% / 0.5%. |
| `trading-objectives.html` | Instant Best Day modal + Instant card / `p8Instant` as above. 1-Step / 2-Step `p8` = 3 QPP days every payout. |
| `faq-plans.html` `p7` | Instant QPP: **5 valid trading days** (simple). Best Day / 0.5% on the Instant rules page, not mashed into this line. |
| `faq-plans.html` 1-Step / 2-Step cards | Optional: QPP payouts need 3 trading days. Do not put Instant 0.5% on those cards. |
| `faq-qualified-trader.html` | Delete 4-then-3. Instant QPP = 5 valid trading days. 1-Step / 2-Step QPP = 3 trading days. Same first and later. |
| `faq-evaluation.html` | Add Instant: no eval; QPP 5 valid trading days. 1-Step: no min to pass; QPP 3 days. 2-Step: 5 per eval phase; QPP 3 days. |
| `performance-reward.html` | Instant = **5 valid trading days**. “3 trading days” = **1-Step / 2-Step QPP only**. Drop first-only. |
| `terms.html` §8(b)/(c) | Keep “requirements vary by model.” Optional one line: Instant QPP needs 5 valid trading days; Instant Best Day counted days need more than 0.5% net; 1-Step / 2-Step QPP payouts need 3 trading days; 2-Step eval needs 5. |
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
| Same rule first and later | n/a | n/a | Instant QPP: 5 valid trading days (drop “first only”); 1-Step / 2-Step QPP: 3 trading days | n/a | n/a | Delete 4-then-3 list; rewrite `p9`/`p12` | n/a | Instant 5; 1-Step / 2-Step 3 |

`trading-objectives.html` is **in this pass** for Instant Best Day + 0.5% count, Instant first-payout / min-days stats, and 1-Step / 2-Step QPP **3 trading days**. Do not put Instant 0.5% on the 1-Step Best Day modal.

---

## Do not merge these clocks

- Instant QPP **5 valid trading days** ≠ Instant **20% Best Day** (0.5% day-count) ≠ 1-Step / 2-Step QPP **3 trading days** ≠ 2-Step eval **5 trading days** ≠ 1-Step eval **no min days**. Do not mash Instant Best Day into the 5 valid trading days line. First and later payouts on that plan use **that** rule **plus** the cycle.
- Weekly 7 calendar days and bi-weekly 14 calendar days are the cycle clock. The 3-day QPP min is a trading-day **count** on 1-Step and 2-Step funded payouts. Do not write it as “3 days between payouts,” and do not put it on Instant. Do not keep “first after 4 / later after 3.”
- 1-Step Best Day 50% (no 0.5% floor) ≠ Instant Best Day 20% (only days more than 0.5% count).
- Challenge fee refund on first reward is eval plans only, not Instant. Add-ons are never part of that refund. That refund is not a different day rule.
