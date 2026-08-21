# Verodus website changelog

**Ship this file.** Live site captured 21 August 2026 (`https://www.verodus.com`). Replace the **Find** string with **Put**. Do not rewrite the rest of the block.

Hero and homepage meta description stay locked. Counsel still reviews Terms, Risk, Privacy, AML, and payout wording.

**Facts:** `$49` in meta = Instant at 35% off. `$5k–$200k` in meta = 2-Step sizes. `$1M` = combined cap. **3,000+ traders** is accurate. Verodus LLC and Verodus L.L.C.-FZ are the **same company**. Public legal name: **Verodus L.L.C.-FZ**. Payments: Verodus Capital Inc., an affiliate.

**Formatting:** Keep the same HTML as the string you replace — same tag, classes, inline styles, `data-i18n` / `data-i18n-html`, `<br>`, `<strong>`, lists, and Title Case. Swap words inside the existing node. Do not collapse a value + label into one string, do not drop a `<br>`, and do not restyle the footer, FAQ answers, or rules lists.

**i18n:** Many strings use `data-i18n` / `data-i18n-html`. Change the English source **and** the matching catalog key so Weglot / VerodusI18n does not revert the line. Footer copy lives in `footer.js` (`footer.copyright` and the new payments line).

---

## Locked — do not change

| Location | Keep exactly |
|---|---|
| Homepage H1 | **Funding Traders Worldwide.** |
| Homepage subhead | **Demonstrate consistency through structured evaluation and unlock measured performance rewards** |
| Homepage honesty pill | **— no deposits, no client funds, no brokerage.** |
| Homepage CTAs | **Start Evaluation** / **Free Trial** |
| Homepage meta / og:description / twitter:description | `Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.` |
| Inner-page `<title>`, canonical, hreflang | As live |
| Instant size selector and fee table | Including **$200k**. Leftover fee line. Instant fees stay non-refundable. No new refund sentence. |
| Certificate carousel | Headline **Real traders. Real certificates.** Keep tiles. No IDs, date, country, or rail. Do not hide. Do not substitute quotes. |
| How it works | Four steps, same for Instant / 1-Step / 2-Step |
| Why Verodus | Intro + six cards. No US Platform 5 on Supported Platforms. No “Trading is simulated” on No Personal Capital. |
| Trustpilot | **Rated 4.5 / 5** (already links). Existing quotes. |
| About opening / mission | Do not rewrite. Do not paste bios. Do not rewrite Read Bio modals. |
| `/trading-objectives.html` | Entire page |
| Instant / 1-Step / 2-Step hard rules and simulation disclaimers | Except CHG-07 (48h → under 24 hours) |
| Privacy bans | The three sentences in CHG-09. Keep. |
| Footer | Everything except CHG-02 copyright + payments line. **No** Platform 5 / MT5 restriction in the footer. |
| Homepage order | Do not reorder |
| Plan FAQ bodies (`/faq-plans.html`) | Including Instant “You start on a funded simulated account.” |
| Instant page `<title>` and body blurbs | Except the rows in CHG-04 and CHG-07 |
| Privacy “deliver funded account services” | Keep |

---

## CHG-01 — Homepage title (description unchanged)

**File:** homepage (`index.html` / `/`)

Keep the same `<title>` and meta tags. Change `content` / text only.

| Tag | Find | Put |
|---|---|---|
| `<title>` | `Verodus — Instant from $49. Funded on Day One.` | `Verodus \| Up to $1M capital, 90% reward split` |
| `og:title` | `Verodus — Instant from $49. Funded on Day One.` | `Verodus \| Up to $1M capital, 90% reward split` |
| `twitter:title` | `Verodus — Instant from $49. Funded on Day One.` | `Verodus \| Up to $1M capital, 90% reward split` |
| `name="description"` | `Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.` | **Keep.** |
| `og:description` | same as description | **Keep.** |
| `twitter:description` | same as description | **Keep.** |

Ship:

```html
<title>Verodus | Up to $1M capital, 90% reward split</title>
<meta property="og:title" content="Verodus | Up to $1M capital, 90% reward split">
<meta name="twitter:title" content="Verodus | Up to $1M capital, 90% reward split">
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

`$1M` = combined cap. `90%` = On-Demand top split. Description still says Keep 80% (default).

---

## CHG-02 — One legal name

**Use:** brand **Verodus**. Legal **Verodus L.L.C.-FZ** once, then “Verodus.” Stop mixing `Verodus LLC` and `Verodus L.L.C.-FZ` as if they were two firms.

### Footer (`footer.js` only — do not rewrite the rest)

Live copyright is one `<p style="margin-bottom:1rem" data-i18n="footer.copyright">`. Keep that tag and style. Keep **All Rights Reserved.**

| Find | Put |
|---|---|
| `© 2026 Verodus. All Rights Reserved.` | `© 2026 Verodus L.L.C.-FZ. All Rights Reserved.` |

Add a **sibling** `<p>` immediately under it, same `style="margin-bottom:1rem"`:

```html
<p style="margin-bottom:1rem" data-i18n="footer.payments">Payments processed by Verodus Capital Inc., an affiliate.</p>
```

Do not put both sentences in one paragraph if that would change wrapping. Do not restyle. Keep the tagline, simulated-trading disclaimer, corporate address, and **Related Entities … Verodus Capital Inc., Canada**. Do **not** add Platform 5 / MT5 to the footer.

### Payments line (wherever that exact idea already exists)

If a marketing/legal line currently names the processor without calling it an affiliate of the public legal name, use:

> Payments are processed by Verodus Capital Inc., an affiliate of Verodus L.L.C.-FZ.

**Do not replace** Terms Supplemental Payment Agreement §1. That sentence stays:

> All registration fees, evaluation access fees, and other platform charges are processed exclusively by and payable solely to Verodus Capital Inc. No payments are processed by or payable to Verodus L.L.C.-FZ.

### Privacy (`/privacy.html`)

| Location | Find | Put |
|---|---|---|
| Data Controller | `Verodus LLC, a company registered in the United Arab Emirates, is the data controller responsible for your personal data.` | `Verodus L.L.C.-FZ, a company registered in the United Arab Emirates, is the data controller responsible for your personal data.` |
| (24) Contact Information | `<strong>Verodus LLC</strong>` | `<strong>Verodus L.L.C.-FZ</strong>` |

Leave Email `support@verodus.com`. Leave every Privacy ban (CHG-09). Live Privacy has **no** “discretionary” payout sentence — skip that swap.

### Risk (`/risk-disclosure.html`)

| Find | Put |
|---|---|
| `Verodus LLC ("Verodus") provides digital evaluation services and related online products.` | `Verodus L.L.C.-FZ ("Verodus") provides digital evaluation services and related online products.` |

Leave the rest of the opening paragraph.

### AML (`/aml-policy.html`) — same opening pattern

| Find | Put |
|---|---|
| `Verodus LLC ("Verodus") provides digital evaluation services and related online products.` | `Verodus L.L.C.-FZ ("Verodus") provides digital evaluation services and related online products.` |

Leave the rest of that paragraph.

### Terms (`/terms.html`)

Legal name is already **Verodus L.L.C.-FZ**. Do not rename. Only CHG-03 (discretionary) and CHG-04 (Instant Funded link text).

### Sweep

After the rows above, search the public site for remaining `Verodus LLC` (not `Verodus L.L.C.-FZ`) and rename those legal-name hits the same way. Do not touch `/trading-objectives.html`.

---

## CHG-03 — Remove “discretionary” on payouts

Replace the sentence only.

Same `<p>` (and `data-i18n`) in every row. Replace the flagged phrase. Leave surrounding sentences.

| # | Page | Find | Put |
|---|---|---|---|
| 3a | Homepage FAQ **Is Verodus legitimate?** (`<p class="_answer">`) | `Performance rewards are discretionary payments based on simulated results.` | `If you meet the published rules and complete identity checks, we pay the performance reward for that cycle.` |
| 3b | Terms §(15) (`<p data-i18n="content.p89" style="margin-bottom: 1.5rem;">`) | `are discretionary and are not liabilities of Verodus L.L.C.-FZ.` | `are paid when you meet the published program rules, remain eligible, and complete required identity checks, and may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy.` |
| 3c | Privacy | Any payout sentence that says **discretionary** | Same clause swap as 3b, inside that existing sentence. Live 21 Feb 2026 Privacy does **not** use the word — skip. |
| 3d | About → Performance Rewards | `internal evaluation outcomes` | `the published rules, then a compliance review` |
| 3e | FAQ **Who Provides Our Liquidity?** (`/faq-general.html`) | `retains discretion over` | `operates` |

**3a full `<p>` after the swap** (same answer class; rest unchanged):

> Verodus is not a brokerage or investment firm. Trading is simulated. Evaluation fees are service fees. If you meet the published rules and complete identity checks, we pay the performance reward for that cycle. Review the Terms, Risk Disclosure, and Trustpilot feedback, and only participate if you understand the model.

**3b full `<p>` after the swap** (same two-sentence paragraph; keep the defined-term subject and the closing sentence):

> Performance Reward Rates or incentive remuneration are paid when you meet the published program rules, remain eligible, and complete required identity checks, and may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy. They do not constitute financial returns, investment profits, or guaranteed compensation.

**3d full sentence after the swap:**

> Participants can become eligible for contractual performance rewards based on measured execution and the published rules, then a compliance review.

**3e full sentence after the swap** (only those three words change):

> All trading activity on the Verodus platform remains simulated. No trades are transmitted to external liquidity venues or exchanges. Verodus operates internal simulation mechanics, order handling logic, risk parameters, and trade validation in order to protect firm capital and maintain operational integrity.

Do **not** edit `/trading-objectives.html` (it still contains a discretionary CTA). Do **not** rewrite other “discretion” uses (restricted practices, strategy types).

---

## CHG-04 — Use “funded” less (below the hero)

Do **not** hunt every “funded” on the site. Only these rows. Hero may keep “Funding.” Meta may keep “Funded on day one from $49.”

Same node, same casing pattern. Instant phase label is a single Title Case word. Instant heading keeps `2.` / `2 &ndash;`. Dashboard lines stay lowercase except the product name **Qualified Performance** (already used that way on Instant/FAQ).

| # | Where | Find | Put |
|---|---|---|---|
| 4a | Instant phase card (`/instant.html` `<div class="phase-card-label">`, and homepage Instant **Show Phases** if it prints the same label) | `Funded` | `Instant` |
| 4b | Homepage FAQ **What evaluation models…?** (`<p class="_answer">`) | `Funded simulated account` | `Simulated Instant account` |
| 4c | Instant TOC (`<a href="#s1">`) | `2 &ndash; Funded Account Rules` | `2 &ndash; Instant Account Rules` |
| 4c | Instant h2 (`<h2 data-i18n="content.h22">`) | `2. Funded Account Rules` | `2. Instant Account Rules` |
| 4d | Terms model list (`<a href="instant.html">`) | `Instant Funded` | `Instant` |
| 4e | Homepage dashboard lead (`<p class="_lead">`) | `every challenge and funded account` | `every challenge and Qualified Performance account` |
| 4f | Homepage dashboard bullet (`<li>`) | `challenges and funded accounts side by side` | `challenges and Qualified Performance accounts side by side` |
| 4g | `dashboard.verodus.com` UI copy | `funded accounts` (same sense) | `Qualified Performance accounts` |

**4b full Instant clause after the swap** (hard rules stay):

> Verodus offers Instant, 1-Step, 2-Step Lite, and 2-Step Pro. Instant: no evaluation. Simulated Instant account. 3% daily from that day’s equity high. 6% trail that never locks. Best Day ≤20% of Positive Days’ Profit to get paid. No minimum trading days. $100 every cycle. Default 80% (90% with On-Demand). $5k–$100k. …

**Leave as-is:** Instant overview / intro (“funded simulated account”), Instant body rules, Plan FAQ Instant body, Instant page `<title>` **Instant Funding Rules \| Verodus**, Privacy “deliver funded account services,” JS ids such as `#fundedLevDesc`.

**4d:** change the visible link text only. Keep `href="instant.html"`.

---

## CHG-05 — Stat strip

Keep the **value / label split**. Do not merge into one string. Labels stay Title Case like the ones they replace (`Profit Split` → `Reward Split`, `Users Worldwide` → `Traders`).

**Homepage hero stats** (laurel count + three `_stat` cells):

| Node | Find | Put |
|---|---|---|
| `div._usersCount` | `+3,000` | `3,000+` |
| `div._usersLabel` (`content.usersWorldwide`) | `Users Worldwide` | `Traders` |
| `span._statValue` (keep) | `Up to 90%` | `Up to 90%` |
| `span._statLabel` (`content.span5`) | `Profit Split` | `Reward Split` |

Keep **175+** / **Countries** and **$1M** / **Max Capital** as they are.

**Homepage Global reach strip** (later `_stat` cells):

| Node | Find | Put |
|---|---|---|
| value | `+3,000` | `3,000+` |
| label | `Traders` | `Traders` (keep) |
| value | `Up to 90%` | keep |
| label | `Reward Split` | keep (Title Case — this is what the first strip must match) |
| value | `&lt;24h` | keep |
| label | `Reward Processing` | keep |

Visible result: **3,000+** / **Traders**, **Up to 90%** / **Reward Split**, **&lt;24h** / **Reward Processing**. Do not drop or demote the trader count.

---

## CHG-06 — About (`/about.html`)

Same `<h3 class="text-h3 leaders-subtitle">`. Keep the `<br>` and the second line. Same `<p>` for the analysis sentence.

| Node | Find | Put |
|---|---|---|
| `h3.leaders-subtitle` (`content.h310`) | `The Architects of Scale<br>Engineering the high-performance technology that supports modern market participants.` | `Leadership<br>Engineering the high-performance technology that supports modern market participants.` |
| About “What We Do” `<p>` | `behavioral analysis` | `risk control` |

**Second row full sentence after the swap:**

> We do not provide brokerage services, manage client funds, or offer investment advice. All activity takes place in simulated environments and is intended solely for performance evaluation and risk control.

Do not paste bios onto the page. Do not rewrite Kim Chen / Alexander Vladimirovich modals. Do not rewrite the opening or “Helping traders prove their edge.”

---

## CHG-07 — Instant reward speed: under 24 hours

Homepage **&lt;24h Reward Processing** stays. Keep the Instant list item, the bullet span, and `<strong>Minimum Reward:</strong>`. Change only the parenthetical clock.

**`/instant.html` §4 Rewards & Payouts** (`content.li22`):

| Find | Put |
|---|---|
| `<strong>Minimum Reward:</strong> $100 (processed within 48 hours)` | `<strong>Minimum Reward:</strong> $100 (processed in under 24 hours)` |

Do not use 48h as the SLA. Do not add a penalty/remedy line unless counsel already has approved copy.

Leave Instant fees non-refundable. Leave `$100` eligibility.

---

## CHG-08 — Homepage FAQ (only these two)

| Question | Change |
|---|---|
| Is Verodus legitimate? | CHG-03a only. Rest of the answer stays. |
| What evaluation models does Verodus offer? | CHG-04b only. Hard rules stay. |

Do **not** rewrite: What is Verodus?, Do I need to risk my own money?, I'm not a trader, How much can I earn?, Can I try Verodus before paying?, When and how do I get paid?

---

## CHG-09 — Privacy bans — keep exactly

Do not replace, soften, or add sale/license language.

> Verodus does not use trading behavior data to replicate, commercialize, or exploit user trading strategies externally.

> Trader P&L, trading strategies, and behavior data may be shared internally only with risk management and compliance personnel to assess platform risk exposure, determine margin adjustments, and prevent prohibited trading activity. This information is not shared externally.

> Verodus does not sell personal information in exchange for monetary compensation and does not share personal data for independent third-party marketing without explicit user consent.

This pass on Privacy: controller name (CHG-02) + discretionary payout sentence **if one exists** (CHG-03c). Nothing else. Do not put “we sell trading data” on marketing pages.

---

## Words (only where a row above already applies)

| Avoid below the hero | Use |
|---|---|
| Funded (Instant phase label) | Instant |
| Profit Split (stat label) | Reward Split |
| Discretionary (payouts) | Paid under the published rules after eligibility checks |
| Behavioral analysis (About) | Risk control |

---

## Not in this changelog (explicitly skipped)

- Instant **$200k** column / selector / fee-table cell
- Certificate IDs, dates, country, rail, duplicate-tile hunt, hiding the carousel
- `/trading-objectives.html`
- Instant How it works variant; How it works step 5
- Scaling own URL; $2M–$4M copy
- US Platform 5 / MT5 in the footer
- Internal positioning (Alpha / Fintokei / For Traders)
- Payouts page, Trustpilot review count, filmed bios, photography, Discord homepage block, add-on comparison table, making table prices match locked meta `$49`, `/about` → `/about.html` redirect, sitemap 500, unpublishing `/best-simulated-prop-firm-2026.html`
- New FAQ “Is this a funded account?”
- Rewriting Instant / Plan FAQ body “funded simulated account”

---

## Implement in this order

1. CHG-01 homepage title
2. CHG-03 FAQ / Terms / Privacy-if-present / About / liquidity FAQ
3. CHG-04 Instant label + FAQ / dashboard / Terms “funded” swaps
4. CHG-02 one legal name (footer, Privacy, Risk, AML, leftover `Verodus LLC`)
5. CHG-05 stat strips
6. CHG-06 About heading + risk control
7. CHG-07 Instant 48h → under 24 hours
8. CHG-08 confirm only those two homepage FAQ answers moved
9. CHG-09 confirm Privacy bans untouched

---

## QA

- [ ] Homepage `<title>` / og:title / twitter:title = **Verodus | Up to $1M capital, 90% reward split**
- [ ] Homepage description still the locked `$49` / `$5k–$200k` / Keep 80% string
- [ ] Hero H1, subhead, pill, CTAs unchanged
- [ ] Instant table still has **$200k**
- [ ] Certificates still on the homepage, same tiles
- [ ] Footer copyright is still one `margin-bottom:1rem` line: `© 2026 Verodus L.L.C.-FZ. All Rights Reserved.` plus a sibling payments `<p>` in the same style; rest of footer unchanged; no MT5
- [ ] No remaining public **Verodus LLC** (without L.L.C.-FZ) on Privacy, Risk, AML
- [ ] Terms still Verodus L.L.C.-FZ; same two-sentence `<p>`; Performance Reward Rates subject kept; closing “They do not constitute…” kept; Instant link text is Instant
- [ ] Homepage FAQ legitimate + models answers swapped; other FAQ answers untouched
- [ ] `/faq-general.html` liquidity line says **operates**
- [ ] Instant phase label Instant; TOC `2 &ndash; Instant Account Rules`; h2 `2. Instant Account Rules`; payout line still `<strong>Minimum Reward:</strong> $100 (processed in under 24 hours)`
- [ ] Stat strips still value + Title Case label: **3,000+** / **Traders**, **Up to 90%** / **Reward Split**, **&lt;24h** / **Reward Processing**
- [ ] About h3 still two lines: **Leadership** then `<br>` then the Engineering sentence; “risk control”; modals unchanged
- [ ] `/trading-objectives.html` byte-identical
- [ ] Privacy bans still exact
- [ ] i18n catalogs updated for every `data-i18n` string you changed
- [ ] No new font, color, heading level, or layout on any swapped line
