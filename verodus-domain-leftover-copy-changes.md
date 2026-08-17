# Verodus.com leftover copy — domain pass

**Policy (same as TOS / FAQ Plans):**

1. News trading is allowed in every phase. Do not mention a News Trading Addon. Do not keep “±2-minute window no longer applies” recopy — that still sounds like a window exists.
2. Delete the 8(h) 50% / 2-minute profit-mix payout test. Keep HFT, tick scalping, latency/arb, rollover abuse.
3. On-demand = **$100** **and** that evaluation’s **minimum trading days**. Drop **$200** and **2%**. Do not write “at any time.”
4. Keep news bracketing (straddling) and gap trading banned.

Scan date: 17 Aug 2026. English pages on `www.verodus.com`. Update matching keys in `/locales/{en,es,fr,pt,zh,ar,id,hi,tl,pa}/pages/…`.

Pages already aligned (no edit): homepage, checkout (News Trading Addon already removed from add-on SKUs), economic calendar, risk disclosure, lot-exposure (those `$200,000` lines are size, not payout), abuse-misuse, key-trading-terms.

---

## 1. `restricted-trading.html` (incorporated into TOS §9)

Locale: `/locales/en/pages/restricted-trading.json`

News is already “allowed,” but the addon bullet and the “window does not apply” recopy are still live. Strip both. Keep HFT / tick-scalp. Keep bracketing / gap.

### Delete `content.p9` (addon bullet)

**Current:**

> • **News Trading Addon:** News trading is included on all plans. The News Trading Addon is not required for news permission.

**Action:** Delete the whole paragraph from HTML and empty/delete the locale key. News is default. Do not name a retired product.

### Rewrite `content.p17`

**Current:**

> • **News Trading:** Allowed on evaluation and funded / Qualified Performance. You may open and close around high-impact news. The ±2-minute window and tiered news-trading breach do not apply.

**Replace with:**

```text
• News Trading: Allowed in every phase (evaluation, Instant, and Qualified Performance / funded). You may open, close, or hold through high-impact news. There is no news time window and no news-trading breach.
```

### Delete `content.p18`

**Current:**

> ◦ The previous funded-only ±2-minute window and first/second news-trading violation model no longer apply.

**Action:** Delete. Recopy. Traders will read “window” and think it still exists.

### Keep `content.p19` and `content.p20`

- `p19`: News bracketing and gap trading remain prohibited.
- `p20`: Bracketing (straddling) banned. Gap trading = opened within 60 minutes of a market close and held through reopen.

Optional split (same as TOS): bracketing one bullet, gap trading one bullet.

### Keep Section (1) HFT / tick-scalp / arb

Do not touch `content.p5`–`p8` (arbitrage, HFT, glitch, tick scalping & rollover abuse).

### Meta description

**Current (page head):** “understand prohibited strategies at Verodus, including arbitrage abuse, collusion, news bracketing, and enforcement actions.”

That is fine. Do not add “news restriction.”

### Drop-in for the news block (after Tick Scalping, before Collusion)

```html
<p data-i18n-html="content.p17" class="indent-1" style="margin-bottom: 0.8rem;">• <strong>News Trading:</strong> Allowed in every phase (evaluation, Instant, and Qualified Performance / funded). You may open, close, or hold through high-impact news. There is no news time window and no news-trading breach.</p>
<p data-i18n-html="content.p19" class="indent-2" style="margin-bottom: 0.8rem;">◦ News bracketing and gap trading remain prohibited (see below).</p>
```

Delete the old `p9` and `p18` nodes. Bump “Effective as of” (`content.p1`) to the publish date.

---

## 2. `faq-news-trading.html`

News is allowed, but Instant is missing from the summary, and the retired addon is still named.

| Where | Current | Change |
|---|---|---|
| Intro | “No News Trading Addon required.” | Delete that sentence. Keep: allowed on Instant, 1-Step, 2-Step Lite, 2-Step Pro — evaluation and funded. |
| Plan card heading | `1-Step · 2-Step Lite · 2-Step Pro` | Add Instant |
| Plan card bullet | “No News Trading Addon required” | Delete. Optional: “News trading is included.” |
| Summary table | Rows for 1-Step / 2-Step only | Add Instant row: Allowed / None |
| Summary table column | “No-Trade Window” | Rename to **Window** or drop the column (value is None) |
| OG/meta | “understand which accounts are **restricted** during high-impact news events.” | “News trading is allowed on all Verodus plans. Bracketing and gap trading remain prohibited.” |

Keep: bracketing/gap banned, slippage disclaimer, high-impact table as **awareness only** (not a no-trade list).

---

## 3. `faq-qualified-trader.html`

Locale: `/locales/en/pages/faq-qualified-trader.json` plus hardcoded HTML and JSON-LD.

### News answers — stop naming the addon

**`content.p1` current:** “…No ±2-minute window. No News Trading Addon required.”

**Replace with:**

```text
News trading is allowed on Instant, 1-Step, 2-Step Lite, and 2-Step Pro — evaluation and funded. You may open and close around high-impact news.
```

**`content.p18` current:** “Yes. News trading is allowed on funded accounts. No News Trading Addon required.”

**Replace with:**

```text
Yes. News trading is allowed on funded accounts.
```

Hardcoded list under “Can I trade during major news releases?” — keep “No ±2-minute restricted window” only if you want a one-time clarification; prefer deleting it so the window is not reintroduced. Keep bracketing/gap banned.

### On-demand — unify to $100 + min days (eval and Instant)

Live copy still splits eval vs Instant:

> A fixed $100 profit threshold is required for bi-weekly rewards. On-demand (eval plans) requires $200 and 2%. Instant on-demand requires $100 only.

Hardcoded list:

> Eval plans: minimum $200 profit and greater than 2% since last reward  
> Instant: minimum $100 profit since last reward

**`content.p9` replace with:**

```text
A fixed $100 profit threshold is required for bi-weekly and on-demand rewards. On-demand still requires the minimum number of trading days for that evaluation.
```

**Hardcoded list replace with:**

```html
<ul>
    <li>Minimum $100 profit</li>
    <li>Minimum number of trading days for that evaluation (does not skip the published trading-day requirement)</li>
</ul>
```

Update JSON-LD `acceptedAnswer` for both the minimum-target question and “How do on-demand payouts work?” Keep `content.p12` (3 trading days between payout requests).

---

## 4. Plan rule pages (linked from FAQ Plans)

`1-step.html`, `2-step-lite.html`, `2-step-pro.html`, `instant.html`

### Delete leftover addon bullets

| Page | Key | Delete this line |
|---|---|---|
| 1-step | `content.li42` | News Trading Addon: … not required |
| 2-step-lite | `content.li38` | same |
| 2-step-pro | `content.li38` | same |
| instant | `content.li43` | same |

### Instant — drop “subject to restrictions” on news

`content.span71` / `li37` current: “Full news trading **(subject to restrictions)**…”

**Replace “Full news trading (subject to restrictions)”** with **“Full news trading”**. The rest of the sentence (no HFT, no mass-distributed EAs, etc.) stays.

### On-demand money + days

**1-Step / 2-Step Lite / 2-Step Pro** still have:

> Available at any time if both conditions… Net profit > $200, and Net profit > 2% of your account balance.

| Page | Keys |
|---|---|
| 1-step | `li25`, `li26`, `span22` |
| 2-step-lite | `li21`, `li22`, `span18` |
| 2-step-pro | `li21`, `li22`, `span18` |

**Instant** money is already `$100`, but the line still says **“Available at any time”** with no days (`li27` / `span53`). Fix that too.

**Replace all four with:**

```text
On-Demand (Selected Add-on): Available when net profit > $100 since your last reward and you have met the minimum number of trading days for that evaluation. On-demand does not skip the trading-day requirement.
```

Keep Eligibility bullets (3 trading days since QPP / last payout + one profitable trade). Instant also keeps 5 valid +0.5% days before first reward.

Do not add 8(h). Do not change `$200K` size buttons.

---

## 5. `trading-objectives.html`

On-Demand card still has two mins:

- `#onDemandMinEval` `content.span22` = `2% and $200`
- `#onDemandMinInstant` `content.span26` = `$100`

**Set both to `$100`.** Days still apply; “Anytime” (`span21`) is the cycle label vs weekly/bi-weekly — do not let it mean skip days.

Optional: change `span21` from `Anytime` to `Anytime after min trading days`.

---

## 6. `performance-reward.html`

**`content.p12` current:** `Eval plans: >$200 and >2% since last reward. Instant: >$100.`

**Replace with:**

```text
Available if >$100 profit and the minimum trading days for that evaluation are met
```

---

## 7. `faq-general.html` — 8(h) still live

| Key | Current | Change |
|---|---|---|
| `content.q21` | Is There a Minimum Holding Time? | Keep the question |
| `content.p64` | Yes. 50% of profits from trades longer than two minutes… | **No.** There is no minimum holding time and no 50% duration mix. |
| `content.p65` | …breach… suspension or termination | HFT, tick scalping, latency/arbitrage, and rollover abuse remain prohibited under Restricted Trading Practices. |

Also rewrite the JSON-LD answer for that question.

---

## 8. `terms.html` — 8(h) still live

News subsection is already allowed. **Still delete Section 8(h)** (`content.h38`, `p51`, `p52`, `p53`). Full HTML block is in `verodus-tos-news-trading-changes.md`. Section 8 ends at (g). Keep 9(b) HFT / tick-scalp. Keep bracketing (`li17`) and gap (`li18`).

---

## 9. `faq-plans.html`

Append to each card (`content.p1`, `p3`, `p5`, `p7`):

```text
 News trading is included in every phase. There is no minimum holding time.
```

Do not change “no $200,000 Instant account.”

---

## 10. `common.json` landmine

`pricing.addonFootnote` is still:

> `* Unless News Trading Addon purchased.`

News descs are already allowed (`pricing.evalNewsDesc`, `pricing.qpfNewsDesc`). **Delete or stop rendering `pricing.addonFootnote`.** Keep `pricing.addonWeekendFootnote` (weekend holding addon is still real).

---

## 11. `responsible-trading.html`

`content.li1` already: “News bracketing and gap trading remain prohibited.” **Keep.** Optional one clause: “News trading is allowed.”

No 8(h), no $200/2%, no addon. No required edit.

---

## 12. What not to change

- `$200,000` account sizes (homepage, plan buttons, lot-exposure tables)
- Weekend Holding Addon
- HFT, tick scalping, latency/arb, rollover abuse
- News bracketing / gap trading bans
- Instant 5 valid days, 3% daily from day’s equity high, 6% trail, 20% consistency
- 1-Step / Instant Best Day rules
- Checkout SKUs: weekend-holding, weekly-payout, on-demand-payout (no news addon left to remove)

---

## Locale files for this pass

```text
/locales/{lang}/pages/restricted-trading.json     p9 delete, p17 rewrite, p18 delete
/locales/{lang}/pages/faq-news-trading.json       (mostly hardcoded HTML + meta)
/locales/{lang}/pages/faq-qualified-trader.json   p1, p9, p18 + HTML list + JSON-LD
/locales/{lang}/pages/1-step.json                 li42 delete; li25/li26/span22
/locales/{lang}/pages/2-step-lite.json            li38 delete; li21/li22/span18
/locales/{lang}/pages/2-step-pro.json             li38 delete; li21/li22/span18
/locales/{lang}/pages/instant.json                li43 delete; span71; li27/span53
/locales/{lang}/pages/trading-objectives.json     span22 (and span26) → $100
/locales/{lang}/pages/performance-reward.json     p12
/locales/{lang}/pages/faq-general.json            q21/p64/p65
/locales/{lang}/pages/terms.json                  h38/p51/p52/p53 delete
/locales/{lang}/pages/faq-plans.json              p1/p3/p5/p7
/locales/{lang}/common.json                       pricing.addonFootnote
```
