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
- On-demand still must meet **that evaluation’s minimum trading days**. It does not skip days. Do not write “at any time” without the day clause.
- **QPP days between rewards (all plans):** 3 trading days since the Qualified Performance account or last payout, **and** one closed profitable trade.
- **Instant extra (first reward only):** 5 valid trading days, each +0.5% net vs that day’s start-of-day equity, **then** the 3-day eligibility above.
- **1-Step evaluation:** no minimum trading days to pass.
- **2-Step Lite / Pro evaluation:** 5 trading days per phase.

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

## 2. Align first-payout **trading days** (4 vs 3)

| Page | Live | Action |
|---|---|---|
| Plan pages Eligibility | **3** trading days since QPP / last payout + 1 profitable trade | Keep 3 |
| `performance-reward.html` | First reward after **3** trading days | Keep 3 |
| `faq-qualified-trader.html` list under `p9` | First payout after **4** trading days / subsequent **3** | **Change 4 → 3** |
| `trading-objectives.html` | — | **Do not edit** |

**Replace the FAQ list under “Is there a minimum target…” with:**

```html
<ul>
    <li>First payout: available after 3 trading days (Instant: also complete 5 valid trading days at +0.5% before the first reward)</li>
    <li>Subsequent payouts: available after 3 trading days</li>
</ul>
```

Update JSON-LD for that question. Keep `content.p12` (“A minimum of 3 trading days is required between payout requests.”).

---

## 3. Align on-demand on `performance-reward.html`

**`content.p12` live:** `Minimum $100 since last reward (all plans).`

**Paste:**

```text
Minimum $100 since last reward and the minimum trading days for that evaluation (all plans).
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

## 5. Instant Eligibility vs 5 valid days

Both stay:

- `li10`: 5 valid +0.5% days before **first** reward
- `li23` / `span47`: 3 trading days since account / last payout + 1 profitable trade

Optional Eligibility clause if support mixes them:

```text
Eligibility: For the first reward, complete 5 valid trading days (each +0.5%) and then the 3 trading-day rule below. After that, you become eligible for a reward only after both: at least 3 trading days since your last payout, and one closed profitable trade in that period.
```

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
| On-demand + min days | n/a | n/a | Yes | n/a | n/a | Yes | n/a | **Add days to p12** |
| First payout 3 days (eval) | via model pages | n/a | 3 | n/a | n/a | **Change 4 → 3** | n/a | 3 |
| Instant 5 valid days first | n/a | n/a | Yes | Yes | n/a | Add to first-payout bullet | n/a | Instant 5 lives on instant.html |

`trading-objectives.html` is **out of this pass**. Do not use this matrix to change it.

---

## Do not merge these clocks

- Instant 5 valid +0.5% days ≠ 2-Step 5 eval days ≠ QPP 3 days between rewards.
- 1-Step Best Day 50% ≠ Instant Best Day 20%.
- Challenge fee refund on first reward is eval plans only, not Instant.
