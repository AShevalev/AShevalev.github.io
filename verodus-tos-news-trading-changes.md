# Verodus Terms of Service — News Allowed; Drop 8(h) Duration Mix

> **Rescan 17 Aug 2026 10:16 UTC:** TOS **news** copy is already live (allowed all phases). On-demand **$200 / 2%** is already gone (now $100). `#onDemandMinEval` / `2% and $200` are gone from trading-objectives. **Still open:** TOS 8(h), Restricted Trading addon/window recopy, plan-page addon bullets + “at any time”, FAQ general holding-time, FAQ news addon naming. Current leftover list: `verodus-domain-leftover-copy-changes.md`.

**Policy:**

1. News trading is allowed in every phase (evaluation, Instant, and Qualified Performance / funded). Remove the ±2-minute high-impact window, the tiered breach model, and the News Trading Addon exemption.
2. **Delete Section 8(h)** — the “50% of profits must come from trades held longer than 2 minutes” payout test. Do not keep it as a payout rule. Keep the HFT / tick-scalp / latency-arb / rollover-abuse bans already in Restricted Trading Practices (Terms 9(b) / plan-page Section 6).
3. **On-demand minimum is $100**, and it **still must meet the minimum trading days for that evaluation**. Drop the extra “2% of account balance” gate and the $200 floor. Do not write “at any time” in a way that skips days.

**Primary file:** `https://www.verodus.com/terms.html`  
**English copy source:** `/locales/en/pages/terms.json`  
**Also update every other language file** under `/locales/{es,fr,pt,zh,ar,id,hi,tl,pa}/pages/terms.json` for the same keys. The live page uses `data-i18n` / `data-i18n-html`, so changing HTML alone is not enough — locale JSON overwrites it.

News bracketing (straddling) and gap trading are **not** the same rule as news trading. This guide keeps those two as separate bans. Drop them only if you also want those practices allowed.

Plan pages do not print 8(h). Do not add it there. Rec leftover already assumes it is off.

---

## 0. Terms of Service (`terms.html`) — delete Section 8(h) entirely

**Where:** Section (8). Verodus Evaluation Program and Qualified Performance Phase, last subsection, immediately before Section (9). Simulation Trading Rules.

**i18n keys to remove (or empty):** `content.h38`, `content.p51`, `content.p52`, `content.p53`

Do not replace 8(h) with a softer mix test, a different minute threshold, or a “guideline.” Delete the whole subsection. Instant is the scalper door; a 2-minute profit-mix check will deny payouts on accounts that are otherwise inside daily DD, trail, consistency, and valid days. Traders will also read “hold 2 minutes” next to “news is allowed” and think the old ±2-minute news window is back. Section 6 / 9(b) already names the real target: HFT, tick scalping, latency/arb, rollover abuse.

**Delete this entire block from `terms.html`:**

```html
<h3 data-i18n="content.h38" style="font-size: 1rem; font-weight: 700; margin: 1.25rem 0 0.5rem;">(h). Minimum Holding Time / Trade Duration Rule</h3>
<p data-i18n="content.p51" style="margin-bottom: 1rem;">To discourage execution patterns that exploit the simulated environment, Verodus requires that at least 50% of gross generated profits (for Qualified Performance Accounts) or total targeted profits (for Evaluation Accounts) must come from trades that exceed two (2) minutes in duration.</p>
<p data-i18n="content.p52" style="margin-bottom: 1rem;">Occasional rapid exits due to genuine errors or market volatility are acceptable. However, if the total profit from trades lasting less than two minutes exceeds 50% of gross generated profits (Qualified Performance Accounts) or 50% of total targeted profits (Evaluation Accounts), this constitutes a breach.</p>
<p data-i18n="content.p53" style="margin-bottom: 1.5rem;">Breaches of this rule may result in trade review, profit adjustment, account suspension, or termination as set out in Section 9(d).</p>
```

**Locale strings to blank or delete:**

| Key | Current | Action |
|---|---|---|
| `content.h38` | `(h). Minimum Holding Time / Trade Duration Rule` | **Delete** |
| `content.p51` | 50% of profits must come from trades longer than two minutes | **Delete** |
| `content.p52` | If short-duration profits exceed 50%, that is a breach | **Delete** |
| `content.p53` | Breaches may result in review, profit adjustment, suspension, or termination | **Delete** |

Section 8 then ends at **(g). Account Limits and Allocation Rules**. Do not renumber (g). Do not add a new (h).

**Keep (do not touch) the HFT / tick-scalp bans** in Terms 9(b)(i) and on each plan page Section 6:

- High-Frequency Trading (HFT)
- Tick Scalping & Rollover Abuse
- Comprehensive Arbitrage / latency / delayed feeds

Those stay. Instant risk is already priced with 3% daily from the day’s equity high, a 6% trail that never locks, 20% consistency, 5 valid days at +0.5% of that day’s start-of-day equity, and a $100 minimum.

**FAQ that still reprints 8(h)** — `faq-general.html` + `/locales/en/pages/faq-general.json`:

| Key | Current | Change to |
|---|---|---|
| `content.q21` | Is There a Minimum Holding Time? | Keep the question |
| `content.p64` | Yes. … 50% of profits … exceed two minutes … | **No.** There is no minimum holding time and no requirement that a share of profits come from trades held longer than two minutes. |
| `content.p65` | Occasional rapid exits… breach… suspension or termination | High-frequency trading, tick scalping, latency/arbitrage, and rollover abuse remain prohibited under Restricted Trading Practices. |

**Ready-to-paste FAQ answer:**

```text
No. There is no minimum holding time and no requirement that a percentage of profits come from trades held longer than two minutes. High-frequency trading, tick scalping, latency/arbitrage, and rollover abuse remain prohibited under Restricted Trading Practices.
```

Plan pages (`1-step.html`, `2-step-lite.html`, `2-step-pro.html`, `instant.html`, `trading-objectives.html`) do **not** print 8(h). Leave them alone for this rule. Do not add a duration-mix line when you edit those pages for news.

---

## 1. Terms of Service (`terms.html`) — news: change these three places

All three sit in **Section (9). Simulation Trading Rules → (b). Prohibited Trading Strategies and Toxic Behavior**.

### Change 1 — Section 9(b)(i) System Exploitation (the “intentionally trading news” clause)

**Where:** paragraph after the HFT / glitch / tick-scalping list  
**i18n key:** `content.p59`

**Current:**

> Furthermore, Participants must trade responsibly and apply standard risk management rules. Exploitative practices include: (i) opening significantly larger positions compared to usual history, (ii) opening significantly smaller or larger numbers of positions compared to history, or **(iii) intentionally trading news events**. The Company reserves the sole right to define Forbidden Trading Practices.

**Replace with:**

> Furthermore, Participants must trade responsibly and apply standard risk management rules. Exploitative practices include: (i) opening significantly larger positions compared to usual history, and (ii) opening significantly smaller or larger numbers of positions compared to history. News trading is permitted in all phases and is not an exploitative practice. The Company reserves the sole right to define Forbidden Trading Practices.

**Ready-to-paste (`content.p59`):**

```text
Furthermore, Participants must trade responsibly and apply standard risk management rules. Exploitative practices include: (i) opening significantly larger positions compared to usual history, and (ii) opening significantly smaller or larger numbers of positions compared to history. News trading is permitted in all phases and is not an exploitative practice. The Company reserves the sole right to define Forbidden Trading Practices.
```

---

### Change 2 — Section 9(b)(ii) heading and intro (the actual restriction)

**Where:** the heading and first paragraph of subsection (ii)  
**i18n keys:** `content.h42`, `content.p60`

**Current heading (`content.h42`):**

> (ii). News Trading Restriction (Tiered Breach Model)

**Replace heading with:**

> (ii). News Trading

**Ready-to-paste (`content.h42`):**

```text
(ii). News Trading
```

**Current intro (`content.p60`):**

> To protect against unrealistic slippage, a ±2-minute restricted window is implemented around high-impact events for funded accounts.

**Replace intro with:**

> News trading is permitted across all phases of the Verodus Evaluation Program and the Qualified Performance Phase, including Instant Funding accounts. There is no restricted time window around high-impact news events. Opening, closing, or holding positions through news is allowed. No profit-removal penalty, soft breach, or hard breach applies solely because a trade was executed during a news event.

**Ready-to-paste (`content.p60`):**

```text
News trading is permitted across all phases of the Verodus Evaluation Program and the Qualified Performance Phase, including Instant Funding accounts. There is no restricted time window around high-impact news events. Opening, closing, or holding positions through news is allowed. No profit-removal penalty, soft breach, or hard breach applies solely because a trade was executed during a news event.
```

---

### Change 3 — Section 9(b)(ii) bullet list (violations, addon)

**Where:** the four-item list under subsection (ii)  
**i18n keys:** `content.li15`, `content.li16`, `content.li17`, `content.li18`

| Key | Current | Action |
|---|---|---|
| `content.li15` | **First Violation:** remove all profits from the restricted window | **Delete** this list item |
| `content.li16` | **Second Violation:** hard breach / account termination | **Delete** this list item |
| `content.li18` | **News Trading Addon:** paid exemption from the restriction | **Delete** this list item |
| `content.li17` | **News Bracketing and Gap Trading:** straddling banned; gap trading defined | **Keep**, but split gap trading onto its own line so it is not mixed with news |

**Delete these two items entirely:**

> - **First Violation:** Any manual trade execution or automated TP/SL fills will result in the removal of all profits generated from the restricted window.  
> - **Second Violation:** A second instance results in a hard breach, leading to immediate account termination.

**Delete this item entirely (addon is obsolete once news is free in all phases):**

> - **News Trading Addon:** Accounts that purchase the News Trading Addon are granted full permission to engage in news trading without any restrictions, time windows, profit-removal penalties, or breach risk tied to news events.

**Keep / rewrite `content.li17` as two remaining bullets:**

**Ready-to-paste HTML for the list (replace the whole `<ul>` under subsection (ii)):**

```html
<ul style="margin: 0 0 1rem 1.25rem;">
    <li data-i18n-html="content.li17" style="margin-bottom: 0.35rem;"><strong>News Bracketing:</strong> News bracketing (straddling — pending or market orders placed on both sides of a news event) remains prohibited.</li>
    <li data-i18n-html="content.li18" style="margin-bottom: 0.75rem;"><strong>Gap Trading:</strong> Gap Trading is defined as any position opened within 60 minutes of a market close and held through the reopen, and remains prohibited.</li>
</ul>
```

**Locale strings for that rewrite:**

`content.li17`:

```html
<strong>News Bracketing:</strong> News bracketing (straddling — pending or market orders placed on both sides of a news event) remains prohibited.
```

`content.li18` (reuse the now-empty addon key for gap trading, or delete `li18` if you drop the second bullet):

```html
<strong>Gap Trading:</strong> Gap Trading is defined as any position opened within 60 minutes of a market close and held through the reopen, and remains prohibited.
```

If you also want bracketing and gap trading allowed, delete the entire list and leave only the new heading + intro paragraph.

---

## 2. HTML block to drop in (full subsection (ii))

Replace the current `(ii)` block in `terms.html` with:

```html
<h4 data-i18n="content.h42" style="font-size: 0.95rem; font-weight: 700; margin: 1rem 0 0.5rem;">(ii). News Trading</h4>
<p data-i18n="content.p60" style="margin-bottom: 0.75rem;">News trading is permitted across all phases of the Verodus Evaluation Program and the Qualified Performance Phase, including Instant Funding accounts. There is no restricted time window around high-impact news events. Opening, closing, or holding positions through news is allowed. No profit-removal penalty, soft breach, or hard breach applies solely because a trade was executed during a news event.</p>
<ul style="margin: 0 0 1rem 1.25rem;">
    <li data-i18n-html="content.li17" style="margin-bottom: 0.35rem;"><strong>News Bracketing:</strong> News bracketing (straddling — pending or market orders placed on both sides of a news event) remains prohibited.</li>
    <li data-i18n-html="content.li18" style="margin-bottom: 0.75rem;"><strong>Gap Trading:</strong> Gap Trading is defined as any position opened within 60 minutes of a market close and held through the reopen, and remains prohibited.</li>
</ul>
```

And update `content.p59` as in Change 1.

---

## 3. Do not miss: pages incorporated into the Terms

Section 9 of the Terms says detailed definitions live at `https://www.verodus.com/restricted-trading.html`. Section 8(a) incorporates the model rule pages. If those stay unchanged, the old restriction still binds.

### `restricted-trading.html` + `/locales/en/pages/restricted-trading.json`

| Key | Current | Change |
|---|---|---|
| `content.p9` | News Trading Addon exemption | **Delete** |
| `content.p17` | Tiered Breach Model, ±2 min window for funded accounts | **Replace** with the same “allowed in all phases” paragraph used in `content.p60` |
| `content.p20` | News bracketing and gap trading banned | **Keep** (or split as above) |
| `content.p25` | “standard for First News Violations” | **Remove** the news-violation parenthetical |
| `content.p28` | “standard for Second News Violations” | **Remove** the news-violation parenthetical |

### Model pages (same Section 6 language on each)

- `1-step.html` + `/locales/en/pages/1-step.json`
- `2-step-lite.html` + `/locales/en/pages/2-step-lite.json`
- `2-step-pro.html` + `/locales/en/pages/2-step-pro.json`
- `instant.html` + `/locales/en/pages/instant.json`

On each page, change:

| Location | Current | Change to |
|---|---|---|
| Qualified Performance → News Trading | “Full details on News Trading **restrictions**… Tiered Breach Model applies only to Qualified Performance accounts.” | “News trading is **allowed in all phases**, including Qualified Performance. There is no restricted window and no tiered news breach.” |
| General rules → Allowed in Evaluation / Allowed | “Full news trading” (evaluation only) or “Full news trading (subject to restrictions)” | “Full news trading is allowed in all phases, including Qualified Performance.” |
| Section 6(1) | News Trading Addon bullet | **Delete** |
| Section 6(3) | “News Trading (Tiered Breach Model – Qualified Performance accounts only): ±2-minute restricted window…” plus First/Second Violation | **Delete** this whole bullet |
| Section 6(3) | News Bracketing and Gap Trading | **Keep** (unless you are also lifting those) |
| Section 7 consequences | “standard for first News Trading violation” / “standard for second News Trading violation” | **Remove** those parentheticals |

---

## 4. Same-policy pages that are not the Terms, but will contradict them if left alone

| Page | What to change |
|---|---|
| `trading-objectives.html` + `common.json` keys `pricing.newsTrading`, `pricing.evalNewsDesc`, `pricing.qpfNewsDesc`, `pricing.addonFootnote` | Evaluation already says “Allowed”. Qualified Performance currently says “Restricted” / “±2 min… unless News Trading Addon”. Change QPP to **Allowed** in all phases. Delete the addon footnote. Suggested `pricing.qpfNewsDesc`: “News trading is allowed. There is no restricted window around high-impact news events.” |
| `faq-qualified-trader.html` | Answers “Can I Trade News?” and “Can I trade during major news releases?” currently say you cannot, unless the addon is purchased. Rewrite both to: **Yes, in all phases.** |
| `faq-news-trading.html` | Full news policy page. Currently describes a 4-minute no-trade window for 1-Step / 2-Step Lite / 2-Step Pro. Rewrite to allowed in all phases; remove window tables, soft-breach TP/SL language, and addon asterisks. Keep the economic-calendar / affected-instruments tables only if you still want educational context, not as a restriction. |
| Checkout / dashboard News Trading Addon | Remove or retire the paid addon once TOS no longer requires it. |
| `faq-general.html` (`content.q21`, `p64`, `p65`) | “Is There a Minimum Holding Time?” currently reprints 8(h). Change the answer to **No** and point at the HFT / tick-scalp bans. |

---

## 4b. FAQ Plans + plan pages — same policy, and on-demand min = $100

`faq-plans.html` is the Help Center “Verodus Plans” hub. It only has four short cards. The payout math, news line, and on-demand minimum live on the four rule pages it links to, plus Qualified Trader FAQ and the objectives/rewards pages.

Do **not** change “no $200,000 Instant account” on the Instant card — that is account size, not the payout floor.

### Hub cards — `faq-plans.html` + `/locales/en/pages/faq-plans.json`

Add one sentence to every card so the hub matches TOS. Do not mention a 2-minute hold.

**Ready-to-paste extra sentence (append to `content.p1`, `p3`, `p5`, `p7`):**

```text
 News trading is included in every phase. There is no minimum holding time.
```

Instant card (`content.p7`) after that sentence, still keep: `Sizes $5,000–$100,000 — no $200,000 Instant account.`

### On-demand minimum: $100, plus that evaluation’s minimum trading days

Old rule (two money gates, reads as skipping days): net profit **> $200 and > 2%**, “available at any time.”  
New rule: net profit **> $100** since last reward, **and** the trader has met the **minimum number of trading days for that evaluation**. On-demand does not skip days.

Do not write “available at any time” without the day requirement. The existing Eligibility bullet (3 trading days since QPP / last payout, plus one closed profitable trade) stays. On-demand adds $100 on top of that plan’s day rule — it does not replace it.

Per-plan day floor (do not invent a new number; use the one already on that page):

| Evaluation | Minimum trading days on-demand must still meet |
|---|---|
| Instant | 5 valid trading days (each +0.5% of that day’s start-of-day equity) before first reward; then the published days-between-rewards rule |
| 1-Step | Evaluation has no min days; QPP still needs the published 3 trading days since account / last payout |
| 2-Step Lite | 5 trading days in evaluation; QPP still needs the published 3 trading days since account / last payout |
| 2-Step Pro | 5 trading days in evaluation; QPP still needs the published 3 trading days since account / last payout |

| File | Keys / HTML | Current | Replace with |
|---|---|---|---|
| `1-step.html` | `content.li25`, `content.li26`, `content.span22` | `Available at any time if both conditions… Net profit > $200, and` / `Net profit > 2%…` | `$100` **and** that evaluation’s min trading days (see paste below) |
| `2-step-lite.html` | `content.li21`, `content.li22`, `content.span18` | same | same |
| `2-step-pro.html` | `content.li21`, `content.li22`, `content.span18` | same | same |
| `instant.html` | `content.li27`, `content.li28`, `content.span53` | same two-gate list | same, Instant still needs 5 valid days |
| `trading-objectives.html` | `content.span22` | `2% and $200` | `$100` (keep `span21` “Anytime” as the cycle label vs weekly/bi-weekly — days still apply) |
| `performance-reward.html` | `content.p12` | `Available if >$200 and >2% profit since last reward` | `Available if >$100 profit and the minimum trading days for that evaluation are met` |
| `faq-qualified-trader.html` | `content.p9` | bi-weekly $100; on-demand $200 | `$100` for bi-weekly **and** on-demand; on-demand still requires that evaluation’s min trading days |
| `faq-qualified-trader.html` | hardcoded `<ul>` under “How do on-demand payouts work?” | `Minimum $200 profit` / `Greater than 2% gain since starting balance` | `$100` **and** min trading days (see FAQ list below) |
| `faq-qualified-trader.html` | JSON-LD for the minimum-target and on-demand questions | `$200` / “at any time” without days | same two conditions |
| Plan pages Eligibility bullets | `1-step` `li21`/`span19`; lite/pro `li17`/`span15`; instant `li23`/`span47` | 3 trading days + one profitable trade | **Keep.** Do not delete. On-demand does not override this. |

**Ready-to-paste on-demand bullet (plan pages):**

```text
On-Demand (Selected Add-on): Available when net profit > $100 since your last reward and you have met the minimum number of trading days for that evaluation. On-demand does not skip the trading-day requirement.
```

**Ready-to-paste Instant HTML (`content.span53` / `li27`):**

```html
<strong>On-Demand (Selected Add-on):</strong> Available when net profit &gt; $100 since your last reward and you have met the minimum number of trading days for that evaluation (Instant: 5 valid trading days at +0.5% before the first reward). On-demand does not skip the trading-day requirement.
```

**Ready-to-paste FAQ `content.p9`:**

```text
A fixed $100 profit threshold is required for bi-weekly and on-demand rewards. On-demand still requires the minimum number of trading days for that evaluation.
```

**Ready-to-paste FAQ on-demand list:**

```html
<ul>
    <li>Minimum $100 profit</li>
    <li>Minimum number of trading days for that evaluation (does not skip the published trading-day requirement)</li>
</ul>
```

**Ready-to-paste `performance-reward.html` `content.p12`:**

```text
Available if >$100 profit and the minimum trading days for that evaluation are met
```

Leave **Minimum Reward: $100** on weekly/bi-weekly as-is. Leave **$200K** account-size buttons as-is. Leave Eligibility (3 trading days between rewards) as-is.

### Plan-page leftovers (same news / 8(h) pass)

News copy on the four plan pages is already mostly “allowed.” Finish these:

| Location | Current leftover | Action |
|---|---|---|
| Instant `content.span71` / `li37` | “Full news trading **(subject to restrictions)**” | Drop “(subject to restrictions)”. News is allowed. HFT / tick-scalp bans stay in Section 6. |
| All four plan pages `News Trading Addon` bullet | “News trading is included… Addon is not required” | **Delete** the addon bullet. News is default, not an add-on. |
| All four plan pages Section 6 | HFT, tick scalping, latency/arb, rollover abuse | **Keep** |
| All four plan pages | 8(h) 50% / 2-minute profit mix | **Not printed.** Do not add it. |

Also update the same keys in `/locales/{lang}/pages/` for `faq-plans`, `1-step`, `2-step-lite`, `2-step-pro`, `instant`, `trading-objectives`, `performance-reward`, and `faq-qualified-trader`.

---

## 5. What you are not changing

These stay as-is unless you separately decide otherwise:

- Gap trading (positions opened within 60 minutes of a market close and held through reopen)
- News bracketing / straddling, if you keep Change 3 as written
- **HFT, tick scalping, latency/arbitrage, rollover abuse** in Terms 9(b) / plan-page Section 6 — keep these; they replace 8(h)
- Lot-exposure limits, weekend holding addon
- Instant’s existing risk stack: 3% daily from the day’s equity high, 6% trail that never locks, 20% consistency, 5 valid days at +0.5% of that day’s start-of-day equity, $100 minimum
- 1-Step / Instant **Best Day** consistency rules (those are not 8(h))

---

## 6. Locale files to touch for the Terms themselves

Update the same keys in every language:

```text
/locales/en/pages/terms.json
/locales/es/pages/terms.json
/locales/fr/pages/terms.json
/locales/pt/pages/terms.json
/locales/zh/pages/terms.json
/locales/ar/pages/terms.json
/locales/id/pages/terms.json
/locales/hi/pages/terms.json
/locales/tl/pages/terms.json
/locales/pa/pages/terms.json
```

Keys:

- `content.h38`, `content.p51`, `content.p52`, `content.p53` — **delete** (Section 8(h) duration mix)
- `content.p59` — remove “intentionally trading news events”
- `content.h42` — heading
- `content.p60` — permission paragraph
- `content.li15` — delete or empty
- `content.li16` — delete or empty
- `content.li17` — bracketing only
- `content.li18` — gap trading (replaces addon text)

FAQ keys (`/locales/{lang}/pages/faq-general.json`): `content.q21`, `content.p64`, `content.p65` — answer becomes **No**, point at the Section 6 HFT / tick-scalp bans.

On-demand $100 keys:

- Plan pages: `1-step` `li25`/`li26`/`span22`; `2-step-lite` and `2-step-pro` `li21`/`li22`/`span18`; `instant` `li27`/`li28`/`span53`
- `trading-objectives` `content.span22` → `$100`
- `performance-reward` `content.p12` → `Available if >$100 profit and the minimum trading days for that evaluation are met`
- `faq-qualified-trader` `content.p9` plus the hardcoded `$200` / `2%` list in the HTML — $100 **and** min trading days
- `faq-plans` `content.p1`, `p3`, `p5`, `p7` — append news-included / no minimum holding time

After deploy, bump cache if needed (`last-modified` on `terms.html`) and re-check a non-English language so Weglot / `/locales` is not still serving the old restriction.
