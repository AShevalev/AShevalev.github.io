# Verodus.com leftover copy — rescan 17 Aug 2026 10:16 UTC

Live English pass of `www.verodus.com` after the latest site updates. Only **still-wrong** copy is listed. Matching `/locales/{lang}/pages/…` keys must move with the HTML.

**Policy**

1. News trading is allowed in every phase. Do not name a News Trading Addon. Do not keep “±2-minute window does not apply” recopy.
2. Delete TOS 8(h) (50% of profits from trades held > 2 minutes). Keep HFT / tick-scalp / latency-arb / rollover.
3. On-demand = **$100** **and** that evaluation’s **minimum trading days**. Do not write “at any time.”
4. Keep news bracketing and gap trading banned.

---

## Already done — do not re-edit

| Item | Live state |
|---|---|
| TOS news (9(b)(ii)) | Allowed all phases. `h42` = News Trading. `p60` has no window. `li15`/`li16` empty. Bracketing `li17` / gap `li18` kept. `p59` no longer calls news an exploit. |
| On-demand **money** | `$200` and `2%` are gone. Plan pages, objectives, rewards, and Qualified Trader FAQ all use **$100**. |
| `trading-objectives.html` | `#onDemandMinEval` / `#onDemandMinInstant` **removed**. On Demand min is `content.span26` = `$100`. Locale `span22` is also `$100` (unused on that card). Weekly/bi-weekly show `$100`. First payout copy already has days (`p8` 3 days / `p8Instant` 5 days). |
| `performance-reward.html` `p12` | `Minimum $100 since last reward (all plans).` |
| Homepage, checkout SKUs | No news addon product. `$200,000` = account size only. |
| Economic calendar, lot-exposure, abuse-misuse, key-trading-terms, responsible-trading | No leftover restriction / 8(h) / $200-2% payout copy. |
| `common.json` news descs | `evalNewsDesc` / `qpfNewsDesc` already say news is permitted. |
| `faq-news-trading.html` meta | Already “allowed on all evaluation and funded accounts.” |

`keltner-bands.html` “±2 ATR” is indicator math. Ignore.

---

## Still leftover

### 1. `restricted-trading.html` — still the main miss

Locale: `/locales/en/pages/restricted-trading.json`

| Key | Live | Action |
|---|---|---|
| `content.p9` | • **News Trading Addon:** …not required | **Delete** the bullet. Do not name the addon. |
| `content.p17` | Allowed… **The ±2-minute window and tiered news-trading breach do not apply.** | Rewrite with no window language. |
| `content.p18` | ◦ The previous funded-only ±2-minute window and first/second news-trading violation model no longer apply. | **Delete.** Recopy. |
| `p5`–`p8` | HFT / tick-scalp / arb | **Keep** |
| `p19`–`p20` | Bracketing / gap | **Keep** |

**Replace `p17` with:**

```text
• News Trading: Allowed in every phase (evaluation, Instant, and Qualified Performance / funded). You may open, close, or hold through high-impact news. There is no news time window and no news-trading breach.
```

---

### 2. Plan pages — addon bullet, window recopy, “at any time”

`$200` / `2%` is already gone. On-demand is `$100` but still **“Available at any time”** with no trading-day clause.

| Page | Delete addon | Window recopy | On-demand “at any time” |
|---|---|---|---|
| `1-step.html` | `li42` | `li48` | `li25` / `span22` |
| `2-step-lite.html` | `li38` | `li44` | `li21` / `li22` / `span18` |
| `2-step-pro.html` | `li38` | `li44` | `li21` / `li22` / `span18` |
| `instant.html` | `li43` | `li49` | `li27` / `span53` |

**Addon line (delete):** `News Trading Addon: News trading is included on all plans. The News Trading Addon is not required for news permission.`

**Window recopy (replace `li48` / `li44` / `li49`):**

```text
News Trading: Allowed in every phase. You may open, close, or hold through high-impact news.
```

**On-demand (replace “at any time if net profit > $100…”):**

```text
On-Demand (Selected Add-on): Available when net profit > $100 since your last reward and you have met the minimum number of trading days for that evaluation. On-demand does not skip the trading-day requirement.
```

Keep Eligibility (3 trading days since QPP / last payout). Instant also keeps 5 valid +0.5% days before first reward.

**Instant only** — `li37` / `span71` still say “Full news trading **(subject to restrictions)**”. Drop “(subject to restrictions)”. Keep the Section 6 HFT / EA bans.

---

### 3. `faq-news-trading.html`

News is allowed. Leftovers:

- Intro and plan-card bullet still say **“No News Trading Addon required.”** Delete those sentences.
- Intro / bullets still say **“No ±2-minute window.”** Prefer deleting so the window is not reintroduced. Optional keep one “there is no news time window.”
- Summary table still lists only **1-Step · 2-Step Lite · 2-Step Pro**. **Add Instant.**
- Column still named **No-Trade Window** (value None). Rename to Window or drop the column.

Keep bracketing/gap banned and the awareness calendar.

---

### 4. `faq-qualified-trader.html`

Money is already `$100` on all plans. Days are only on the *other* FAQ (first payout 4 days / subsequent 3 days), not on the on-demand list.

| Where | Live | Change |
|---|---|---|
| `content.p1` | …No ±2-minute window. No News Trading Addon required. | Drop both leftover clauses. |
| `content.p18` | …No News Trading Addon required. | Drop addon sentence. |
| Hardcoded news list | “No ±2-minute restricted window” | Delete that bullet. Keep bracketing/gap. |
| `content.p9` | `$100` for weekly, bi-weekly, and on-demand on all four plans | **Keep weekly, bi-weekly, and on-demand at $100.** Add: on-demand still requires that evaluation’s min trading days. |

**Ready-to-paste `content.p9`:**

```text
A fixed $100 profit threshold is required for weekly, bi-weekly, and on-demand rewards. On-demand still requires the minimum number of trading days for that evaluation.
```
| On-demand `<ul>` | only `Minimum $100 profit since last reward (all plans)` | Add a second bullet: min trading days for that evaluation. |
| `content.p13` | “requested **at any time** … once the following conditions are met” | Fine if the list includes days. Do not leave “at any time” as the only gate. |

---

### 5. `faq-general.html` — 8(h) still **Yes**

| Key | Live | Change |
|---|---|---|
| `q21` | Is There a Minimum Holding Time? | Keep question |
| `p64` | **Yes.** 50% of profits from trades > two minutes | **No.** No min hold. No 50% mix. |
| `p65` | breach / suspension | Point at HFT / tick-scalp / latency-arb / rollover in Restricted Trading Practices |

Rewrite JSON-LD for that question too.

---

### 6. `terms.html` — 8(h) still live

News subsection is done. **Still delete** `(h). Minimum Holding Time / Trade Duration Rule`:

- `content.h38`, `content.p51`, `content.p52`, `content.p53`

Section 8 then ends at (g). Do not renumber. Do not replace with a softer mix test.

---

### 7. Small leftovers (optional)

| Page | Live | Action |
|---|---|---|
| `faq-plans.html` `p1`/`p3`/`p5`/`p7` | No news / holding-time line | Optional: append “News trading is included in every phase. There is no minimum holding time.” Do not change “no $200,000 Instant account.” |
| `trading-objectives.html` `span21` | Request **Anytime** | Optional: “Anytime after min trading days.” Money is already $100. |
| `common.json` `pricing.addonFootnote` | `* Unless News Trading Addon purchased.` | **Delete** or stop rendering. Not currently on the objectives page, but it is a landmine. Keep `pricing.addonWeekendFootnote`. |

---

## Do not touch

- `$200,000` account sizes
- Weekend Holding Addon
- HFT, tick scalping, latency/arb, rollover abuse
- News bracketing / gap trading
- Instant 5 valid days, 3% daily from day’s equity high, 6% trail, 20% Best Day
- 1-Step Best Day
- Weekly/bi-weekly $100 (already correct)
