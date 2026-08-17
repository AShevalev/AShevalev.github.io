# Verodus Terms of Service — News Trading Allowed Across All Phases

**Policy:** News trading is allowed in every phase (evaluation, Instant, and Qualified Performance / funded). Remove the ±2-minute high-impact window, the tiered breach model, and the News Trading Addon exemption.

**Primary file:** `https://www.verodus.com/terms.html`  
**English copy source:** `/locales/en/pages/terms.json`  
**Also update every other language file** under `/locales/{es,fr,pt,zh,ar,id,hi,tl,pa}/pages/terms.json` for the same keys. The live page uses `data-i18n` / `data-i18n-html`, so changing HTML alone is not enough — locale JSON overwrites it.

News bracketing (straddling) and gap trading are **not** the same rule as news trading. This guide keeps those two as separate bans. Drop them only if you also want those practices allowed.

---

## 1. Terms of Service (`terms.html`) — change these three places

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

---

## 5. What you are not changing

These stay as-is unless you separately decide otherwise:

- Gap trading (positions opened within 60 minutes of a market close and held through reopen)
- News bracketing / straddling, if you keep Change 3 as written
- HFT, arbitrage, glitch exploitation, tick scalping, lot-exposure limits, weekend holding addon
- Section 8(h) minimum holding time (50% of profits from trades longer than 2 minutes) — that is a duration rule, not a news rule

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

- `content.p59` — remove “intentionally trading news events”
- `content.h42` — heading
- `content.p60` — permission paragraph
- `content.li15` — delete or empty
- `content.li16` — delete or empty
- `content.li17` — bracketing only
- `content.li18` — gap trading (replaces addon text)

After deploy, bump cache if needed (`last-modified` on `terms.html`) and re-check a non-English language so Weglot / `/locales` is not still serving the old restriction.
