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
- Instant scalping is allowed inside drawdown / trail / consistency / valid-day rules.

### Rewards
- **$100** minimum for **weekly, bi-weekly, and on-demand**.
- **First and subsequent payouts are the same.** No “first after X days, later after Y.” Every request must meet **that plan’s minimum trading days** **and** the **selected cycle**.
- Plan mins (same for every payout on that plan):
  - **Instant:** 5 valid trading days, each +0.5% net vs that day’s start-of-day equity
  - **1-Step:** no minimum trading days
  - **2-Step Lite / Pro:** 5 trading days
- Cycle (same for the first payout and every payout after):
  - **Weekly:** 7 calendar days since the account start or last reward
  - **Bi-weekly:** 14 calendar days since the account start or last reward
  - **On-demand:** `$100` since last reward **and** the plan min trading days. Does not skip days. Do not write “at any time” without the day clause.
- Do not add a third clock (e.g. “3 trading days between payouts” or “first payout after 4 days”). Plan min + cycle is the whole rule.

### Do not change
- `trading-objectives.html` (and `/locales/*/pages/trading-objectives.json`) — **no edits**
- `$200,000` account sizes
- Weekend Holding Addon
- Best Day rules (1-Step 50%, Instant 20%)
- Instant 3% daily from day’s equity high, 6% trail that never locks

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

## 2. Same rule for first and later payouts: plan min days + cycle

Live FAQ under `p9` still splits them:

> First payout: available after 4 trading days  
> Subsequent payouts: available after 3 trading days

That split is wrong. **Delete both bullets.** First and later payouts use the same checklist: **`$100` + that plan’s min trading days + the selected cycle** (weekly 7 calendar days, bi-weekly 14 calendar days, on-demand = `$100` and the plan min days).

**`content.p9` paste:**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: you must meet the minimum trading days for that plan and the selected cycle (weekly, bi-weekly, or on-demand).
```

**Replace the hardcoded list with:**

```html
<ul>
    <li>Same rule for every payout (first and later): $100, the plan’s minimum trading days, and the cycle</li>
    <li>Weekly: 7 calendar days since account start or last reward</li>
    <li>Bi-weekly: 14 calendar days since account start or last reward</li>
    <li>On-demand: $100 and the plan’s minimum trading days (Instant: 5 valid days at +0.5%; 2-Step Lite / Pro: 5 days; 1-Step: no minimum trading days)</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.`

**Replace with:**

```text
Payout spacing follows the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or the plan’s minimum trading days for on-demand. The first payout and later payouts use the same rule.
```

**1-Step / 2-Step Eligibility** still says “at least 3 trading days since QPP / last payout.” Rewrite those to plan min + cycle (2-Step: 5 days; 1-Step: no min days + cycle).

**Instant Eligibility (`instant.html` `li23` / `span47`) — replace the 3-day line.** Live:

> Eligibility: You become eligible for a reward only after both of the following are met: At least 3 trading days have passed since you received your Qualified Performance Account or since your last payout, and …

**Instant paste (`li23` / `span47`):**

```text
Eligibility: You become eligible for a reward when you have met 5 valid trading days (each +0.5% net profit) and the selected cycle (weekly 7 calendar days, bi-weekly 14 calendar days, or on-demand). The first payout and every payout after use this same rule. Do not use a 3-trading-day clock on Instant.
```

Instant `li10` — drop “first.” Same 5 valid days for every Instant payout.

```text
Minimum Trading Days Requirement: You must have met a minimum of 5 valid trading days (each +0.5% net profit) and the selected cycle (weekly, bi-weekly, or on-demand). The first payout and every payout after use this same rule.
```

`performance-reward.html` “First reward after 3 trading days” / “Min. 3 trading days” — replace with plan min + cycle. No first/later split.

`trading-objectives.html` — **do not edit.**

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100, the plan’s minimum trading days, and the selected cycle (same rule for the first payout and every payout after).
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

## 5. Instant Eligibility — 5 valid days, not 3

`instant.html` Eligibility is wrong today. It still uses the QPP **3 trading days** sentence. Instant’s plan min is **5 valid trading days** (each +0.5%).

| Key | Live | Change to |
|---|---|---|
| `li23` / `span47` | At least **3 trading days** since QPP account or last payout | **5 valid trading days** (+0.5% each) **and** the selected cycle |
| `li10` / `span21` | 5 valid days before your **first** reward | 5 valid days for **every** payout, plus the cycle |

Delete the “3 trading days since last payout” Instant extra. Do not keep 5-then-3.

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

| Plan | Eval / pass min days | Payout min days (every payout) | Cycle |
|---|---|---|---|
| Instant | No eval. Funded from day one. | **5 valid days**, each +0.5% net | Weekly 7 calendar / bi-weekly 14 calendar / on-demand = `$100` + those 5 valid days |
| 1-Step | **No** minimum trading days to pass | **No** minimum trading days | Same cycles + `$100` |
| 2-Step Lite | **5** trading days per phase | **5** trading days | Same cycles + `$100` |
| 2-Step Pro | **5** trading days per phase | **5** trading days | Same cycles + `$100` |

A 2-Step “trading day” = open and close on the same calendar day. An Instant “valid day” = that day closes +0.5% net. Do not describe Instant days as open-and-close only.

---

### `faq-evaluation.html`

**“How many trading days do I need for each program?”** — hardcoded list omits Instant.

**Replace the list with:**

```html
<ul>
    <li>Instant: 5 valid trading days (each day must close +0.5% net). No evaluation phase.</li>
    <li>1-Step: No minimum trading days.</li>
    <li>2-Step Lite: 5 trading days per phase (open and close on the same calendar day).</li>
    <li>2-Step Pro: 5 trading days per phase (open and close on the same calendar day).</li>
</ul>
```

**`content.p5` (“What if I hit my targets before the minimum trading days?”)** live: one rule for everyone, open-and-close only. That is wrong for 1-Step (no min) and Instant (valid +0.5% days).

**Paste `p5`:**

```text
If that plan has a minimum, you must still meet it before you pass or get paid. 1-Step has no minimum trading days. 2-Step Lite and 2-Step Pro need 5 trading days per phase (open and close the same calendar day). Instant has no profit target to “hit first”; you need 5 valid days at +0.5% net and the selected payout cycle.
```

Keep `p6` as the 2-Step / 1-Step calendar-day definition. Instant valid-day math stays on `instant.html`.

---

### `faq-qualified-trader.html`

News (`p1`, `p18`) is already plan-complete. Fix payout answers so they name each plan.

**`content.p9` paste:**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. The first payout and every payout after use the same rule: you must meet that plan’s minimum trading days and the selected cycle. Instant: 5 valid days at +0.5%. 2-Step Lite and 2-Step Pro: 5 trading days. 1-Step: no minimum trading days. Weekly is 7 calendar days. Bi-weekly is 14 calendar days. On-demand is $100 plus that plan’s minimum days.
```

**Delete** the hardcoded “First payout after 4 / subsequent after 3” list. Replace with:

```html
<ul>
    <li>Same rule for every payout (first and later): $100, the plan’s minimum trading days, and the cycle</li>
    <li>Instant: 5 valid days at +0.5% net, plus the cycle</li>
    <li>1-Step: no minimum trading days, plus the cycle</li>
    <li>2-Step Lite / Pro: 5 trading days, plus the cycle</li>
    <li>Weekly: 7 calendar days · Bi-weekly: 14 calendar days · On-demand: $100 and the plan min days</li>
</ul>
```

**`content.p12` live:** `A minimum of 3 trading days is required between payout requests.` **Replace with:**

```text
Payout spacing is the cycle you selected: 7 calendar days for weekly, 14 calendar days for bi-weekly, or the plan’s minimum trading days for on-demand. Instant on-demand still needs 5 valid days. First and later payouts use the same rule.
```

**`content.p13` + on-demand list** — drop “at any time.” Paste list:

```html
<ul>
    <li>$100 since last reward (all plans)</li>
    <li>That plan’s minimum trading days (Instant: 5 valid at +0.5%; 2-Step Lite / Pro: 5 days; 1-Step: none)</li>
</ul>
```

**`content.p28` (fee refund)** live: yes for first reward, no Instant exception. **Paste:**

```text
Yes, on 1-Step, 2-Step Lite, and 2-Step Pro: 100% of the original challenge fee is refunded with your first successful performance reward. Instant has no challenge-fee refund.
```

---

### `faq-plans.html`

Cards already name news + no holding time. Instant already names 5 valid +0.5% days. Optional one line on Instant (`p7`) if you want payouts explicit:

```text
Every Instant payout (first and later) needs those 5 valid days and the selected cycle (weekly, bi-weekly, or on-demand).
```

Do not add a 3-day QPP clock to any card.

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
| Same rule first and later | n/a | n/a | Drop “3 days since last payout”; Instant drop “first only” | n/a | n/a | Delete 4-then-3 list; rewrite `p9`/`p12` | n/a | Drop “first reward after 3 days” |

`trading-objectives.html` is **out of this pass**. Do not use this matrix to change it.

---

## Do not merge these clocks

- Instant 5 valid +0.5% days ≠ 2-Step 5 trading days ≠ 1-Step no min days. Each plan keeps its own min; first and later payouts on that plan use **that** min **plus** the cycle.
- Weekly 7 calendar days and bi-weekly 14 calendar days are the cycle clock. Do not add a separate “3 days between payouts” or “first after 4 / later after 3” clock on top.
- 1-Step Best Day 50% ≠ Instant Best Day 20%.
- Challenge fee refund on first reward is eval plans only, not Instant. That refund is not a different day rule.
