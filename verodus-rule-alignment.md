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

**Plan pages — Eligibility** still says “at least 3 trading days since QPP / last payout.” That is a first-vs-later clock. **Rewrite:**

```text
Eligibility: You become eligible for a reward when net profit is at least $100, you have met the minimum number of trading days for that plan, and you have met the selected cycle (weekly 7 calendar days, bi-weekly 14 calendar days, or on-demand). The same rule applies to the first payout and every payout after.
```

Instant `li10` (“5 valid days before your first performance reward”) — drop “first.” Same 5 valid days for every Instant payout.

```text
Minimum Trading Days Requirement: You must complete a minimum of 5 valid trading days (each +0.5% net profit) to be eligible for a performance reward. This applies to every payout, not only the first. You must also meet the selected cycle (weekly, bi-weekly, or on-demand).
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

## 5. Instant — plan min + cycle, not 5-then-3

Do **not** keep 5 valid days for the first reward and 3 days after that. Instant’s plan min is **5 valid +0.5% days on every payout**, plus the selected cycle (weekly 7 / bi-weekly 14 / on-demand).

Rewrite `li10` as in §2. Rewrite Eligibility (`li23` / `span47`) to the same sentence. Delete “3 trading days since last payout” if it makes first and later differ.

---

## 6. Empty locale keys (cleanup, not visible)

Leave `trading-objectives.json` alone. Elsewhere, delete or leave blank:

- TOS: `content.h38`, `p51`, `p52`, `p53`
- Restricted trading: `p9`, `p18`
- 1-step `li42`; 2-step lite/pro `li38`; instant `li43`
- `common.json` `pricing.addonFootnote` (already empty)

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
