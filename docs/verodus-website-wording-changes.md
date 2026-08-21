# Verodus website wording changes

**Purpose:** Light, surgical copy fixes. Do not rewrite sections that already work.  
**Hero: do not change.** Leave the homepage hero exactly as it is, including:

- H1: **Funding Traders Worldwide.**
- Hero subhead: **Demonstrate consistency through structured evaluation and unlock measured performance rewards — no deposits, no client funds, no brokerage.**
- Hero CTAs: **Start Evaluation** / **Free Trial**

**Meta description: do not change.** It stays exactly:

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

Use that same `content` on `og:description` and `twitter:description` if those tags exist.

**Homepage `<title>` / og:title / twitter:title — this pass only:**

```html
<title>Verodus | Up to $1M capital, 90% reward split</title>
```

Inner-page titles stay as they are.

**Scope:** Swap a word or one sentence where listed below. Do **not** rewrite surrounding copy.

**Entity note:** Verodus LLC and Verodus L.L.C.-FZ are the **same company**. Use one public legal name everywhere.

**Product facts (do not treat these as errors):**

- **$49** in meta is Instant at the **35% discount**, not a different SKU from the Instant table.
- **$5k–$200k** in meta is **2-Step** account sizes. Instant does **not** offer $200k.
- **$1M Max Capital** is the **combined** cap across accounts a trader can hold, not a single-account SKU.
- Trustpilot **4.5 / 5** already **links** to the Trustpilot page. Do not call it unclickable.
- Founder bios already live in **Read Bio** modals (photos + Kim Chen CEO copy + Alexander Vladimirovich COO copy). Do not paste them onto the About page and do not rewrite those modals in this pass.
- Homepage payout certificates are **legitimate Verodus certificates**. Keep the carousel. Prefer unique IDs. Hide only a duplicate tile on this carousel, not the section.

This is a copy brief, not a legal opinion. Counsel should still review Terms, Risk Disclosure, Privacy, and any payout language.

---

## Needed change: homepage title (description locked)

Ship these three tags on the homepage. Do not touch the description.

**Change**

```html
<title>Verodus | Up to $1M capital, 90% reward split</title>
<meta property="og:title" content="Verodus | Up to $1M capital, 90% reward split">
<meta name="twitter:title" content="Verodus | Up to $1M capital, 90% reward split">
```

**Keep**

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

If `og:description` and `twitter:description` exist, they keep that same `content`. Inner-page titles stay as they are.

---

## Locked: homepage hero

Do not edit H1, subhead, the **no deposits / no client funds / no brokerage** pill, or CTAs. Do not change prices or “funded” inside those lines.

The Instant table list/discount pair is the 35% Instant promo. **$49** in meta is that discounted Instant price. Do **not** “fix” $49 by editing the hero.

Use **funded** less **everywhere else**. The hero already carries the search term.

The hero already states **— no deposits, no client funds, no brokerage.** Do **not** add a second line under the CTAs repeating no deposit or adding “Simulated accounts.” That honesty is already on the first screen. Leave simulation detail in FAQ, Instant rules, and legal, as now.

---

## Locked: meta description (all pages)

Do **not** change:

- `<meta name="description">`
- `og:description`, `twitter:description`
- canonical / hreflang
- Inner-page `<title>` tags

**Homepage description (locked):**

> Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.

`$49` = Instant at 35% off. `$5k–$200k` = 2-Step sizes (not Instant). `Keep 80%` = default split.

---

## Homepage title (this pass)

| Tag | Now | Change to |
|---|---|---|
| `<title>` | Instant from $49. Funded on Day One. (and any `Verodus —` prefix) | **Verodus \| Up to $1M capital, 90% reward split** |
| `og:title` | same as current title | **Verodus \| Up to $1M capital, 90% reward split** |
| `twitter:title` | same as current title | **Verodus \| Up to $1M capital, 90% reward split** |
| `name="description"` | Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit. | **Keep. Do not change.** |

Homepage only. `$1M` is the combined-account cap. `90%` is the top reward split (On-Demand). Description still says Keep 80% (default). That pairing is intended.

---

## Principles

1. **Light edits only.** Keep existing sentences. Replace the flagged phrase. Do not rewrite the rest of the block.
2. **“Funded”** below the hero (Instant labels, Instant rules, FAQ, dashboard) still sounds like live money. Swap the word; do not rewrite the Instant product story.
3. **“Discretionary”** on the legitimacy FAQ tells people you might not pay even if they follow the rules. Replace that sentence only.
4. One public legal name.

---

## 1. Company name (site-wide, not the hero)

**Use**

- Brand: **Verodus**
- Legal (footer, Terms, Privacy data controller, Risk, contracts): **Verodus L.L.C.-FZ** once, then “Verodus”
- Privacy: rename the **data controller** (and the matching Contact line) from Verodus LLC to **Verodus L.L.C.-FZ**. Keep every ban. Discretionary-payout sentence only if one exists (section 12).
- Payments line: **Payments are processed by Verodus Capital Inc., an affiliate of Verodus L.L.C.-FZ.**

**Stop using**

- Mixing `Verodus LLC` and `Verodus L.L.C.-FZ` as if they were two firms (they are not)

**Suggested footer legal line (replace the legal-name line only):**

> © 2026 Verodus L.L.C.-FZ.  
> Payments processed by Verodus Capital Inc., an affiliate.

Do not rewrite the rest of the footer.

---

## 2. Remove “discretionary” (FAQ, About, Terms, Privacy)

Replace the word/sentence. Leave the rest of each answer as it is.

| Location | Cut | Put |
|---|---|---|
| Homepage FAQ “Is Verodus legitimate?” | “Performance rewards are discretionary payments based on simulated results.” | “If you meet the published rules and complete identity checks, we pay the performance reward for that cycle.” |
| Terms | “Performance Reward Rates or incentive remuneration are discretionary and are not liabilities of Verodus L.L.C.-FZ.” | “Performance rewards are paid when you meet the published program rules, remain eligible, and complete required identity checks. Rewards may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy. They are not investment returns.” |
| Privacy | Any sentence that calls performance rewards or incentive pay **discretionary** (same idea as Terms). | Same replacement as Terms. **Do not change any other Privacy sentence except the data-controller name (section 12).** |
| About → Performance Rewards | “internal evaluation outcomes” | “the published rules, then a compliance review” |

**FAQ “Who Provides Our Liquidity?”** — replace only “retains discretion over” with “operates.” Keep the rest of the sentence.

Live Privacy (effective 21 February 2026) does not currently use the word “discretionary.” If a later Privacy draft adds it on payouts, swap that sentence only. Keep every Privacy **ban** (section 12).

---

## 3. Use “funded” less (labels and one phrase, not full rewrites)

The hero already says “Funding Traders Worldwide.” Meta description already says “Funded on day one from $49.”

Swap the word. Do **not** rewrite Instant blurbs, Instant overview paragraphs, or FAQ answers around it.

| Where | Now | Change to |
|---|---|---|
| Instant card / phase label | Funded | Instant |
| Homepage FAQ Instant line | “Funded simulated account” | “Simulated Instant account” |
| Instant section 2 heading | Funded Account Rules | Instant Account Rules |
| Terms model list | Instant Funded | Instant |
| Dashboard | “funded accounts” | “Qualified Performance accounts” |

Leave Instant card body copy, Instant rules body, Plan FAQ body, and “Instant Funding” in-page titles as they are except the rows above. Do **not** change Instant page `<title>`.

**Optional one-line FAQ** (only if you add a new question; do not rewrite existing ones): “Is this a funded account?” — Instant has no evaluation phase. You trade a simulated account from day one. If you meet the published rules and pass identity checks, we pay a cash reward.

---

## 4. Stat strip (below the hero)

| Now | Change to |
|---|---|
| +3,000 Users Worldwide | **3,000+ traders** |
| Up to 90% Profit Split | **Up to 90% reward split** |

Keep 175+ Countries, **$1M Max Capital** (combined cap across accounts), and **&lt;24h Reward Processing** exactly as they are.

The later “Global reach” strip already says **Up to 90% Reward Split**. Make the first strip match it.

---

## 5. “Why Verodus” cards

Keep the section headline and intro as they are.

| Card | Change |
|---|---|
| Transparent Rules | Keep |
| Measured Rewards | Keep |
| Supported Platforms | **Keep.** Do not add the US Platform 5 restriction here. |
| Global Availability | Keep |
| No Personal Capital | **Keep as-is.** Do not add “Trading is simulated.” |
| Free Trial | Keep |

---

## 6. Instant / pricing module — skip

Do **not** change the Instant size selector, the leftover fee line, or add a refund sentence under the table. Instant **$200k is not a live SKU** (that range is 2-Step). Leave the selector as-is in this pass.

Leave the simulation disclaimers on Instant / 1-Step / 2-Step rule pages as they are.

---

## 7. How it works, calculator, bottom CTA — skip

Keep the four steps, calculator CTA, Rewards-your-way 24h line, and bottom CTA/subline as they are.

Dashboard: swap “funded accounts” only (section 3). Do not rewrite the dashboard intro.

---

## 8. Payout / certificate section

Keep the headline **Real traders. Real certificates.** and the existing body sentences.

Operational only: no placeholder names. Prefer unique certificate IDs. These are **legitimate Verodus certificates** — keep the carousel. Hide only a duplicate tile on this carousel (same ID or same name+amount twice). Do not rewrite the section copy.

---

## 9. Testimonials and Trustpilot

Keep **Rated 4.5 / 5 on Trustpilot** as it is. It already **links** to Trustpilot. Do not replace it with a widget, and do not remove the number.

Keep the existing quotes. Do not rewrite them.

---

## 10. Homepage FAQ

Do not rewrite “What is Verodus?”, “I'm not a trader”, “When and how do I get paid?”, or “How much can I earn?”.

Only:

- “Is Verodus legitimate?” — swap the discretionary sentence (section 2). Keep the rest of that answer.
- “What evaluation models…?” — swap “Funded simulated account” for “Simulated Instant account.” Keep the hard rules as they are.

---

## 11. About page

Do not rewrite the opening paragraph or “Helping traders prove their edge.” Bios already exist in the **Read Bio** modals (photos, Kim Chen CEO text, Alexander Vladimirovich COO text). Do not put them on the page. Do not rewrite the modal copy in this pass.

| Now | Change to |
|---|---|
| “Architects of ScaleEngineering the high-performance…” | **Leadership** (fix the smashed heading only) |
| “behavioral analysis” | “risk control” |

---

## 12. Privacy — controller name + keep the bans

**Change the data controller name only** (same company; one public legal name):

| Location | Now | Change to |
|---|---|---|
| Data Controller | Verodus LLC, a company registered in the United Arab Emirates | **Verodus L.L.C.-FZ**, a company registered in the United Arab Emirates |
| Contact Information | Verodus LLC | **Verodus L.L.C.-FZ** |

Do not rewrite the rest of those paragraphs.

**Keep these bans exactly. Do not replace, soften, or add sale/license language.**

> Verodus does not use trading behavior data to replicate, commercialize, or exploit user trading strategies externally.

> Trader P&L, trading strategies, and behavior data may be shared internally only with risk management and compliance personnel to assess platform risk exposure, determine margin adjustments, and prevent prohibited trading activity. This information is not shared externally.

> Verodus does not sell personal information in exchange for monetary compensation and does not share personal data for independent third-party marketing without explicit user consent.

**Do not change in Privacy this pass:** “deliver funded account services,” sharing list, subprocessors, cookies, CCPA, or any other clause.

**Also:** if Privacy calls performance rewards or incentive pay **discretionary**, replace that sentence with the same rules-based payout line as Terms (section 2). Live Privacy (21 February 2026) does not currently use that word.

Do not put “we sell trading data” on the homepage, FAQ, About, or Privacy.

---

## 13. Blog body (homepage description stays locked)

`/best-simulated-prop-firm-2026.html` **body** numbers that do not match live Instant/1-Step/Lite: update those numbers, or unpublish. Do **not** change that page’s `<title>` or meta. Do not rewrite the article.

---

## 14. Words to prefer vs avoid

Use only when a listed swap above already applies. Do not hunt the site to rewrite every instance.

| Avoid below the hero | Use instead |
|---|---|
| Funded (as Instant phase label) | Instant |
| Profit split (stat strip) | Reward split |
| Discretionary (payouts) | Paid under the published rules after eligibility checks |
| Behavioral analysis (About) | Risk control |

**Exception:** hero H1 may keep “Funding.” Meta description may keep “Funded on day one from $49.” Homepage `<title>` in this pass is **Verodus | Up to $1M capital, 90% reward split.**

---

## 15. Homepage order

Do not reorder the page. Hero (including the no-deposits pill), stat strip, pricing, How it works, Trustpilot, and Why Verodus stay where they are.

---

## 16. What not to change

- **Homepage hero** (H1, subhead, **— no deposits, no client funds, no brokerage.** pill, CTAs). Do not add another line under the CTAs.
- **Homepage meta description** (locked string above). Inner-page titles and descriptions.
- Instant / pricing module (selector, leftover fee line, no new refund sentence). Instant $200k is not sold; leave the module in this pass.
- Why Verodus intro and cards, including **Supported Platforms** (no US Platform 5 add) and **No Personal Capital** (do not add “Trading is simulated.”).
- How it works steps, calculator, bottom CTA.
- Trustpilot **Rated 4.5 / 5** (already links; do not widget-ize or remove).
- Existing testimonial quotes.
- FAQ answers other than the two phrase swaps in section 10.
- About opening / mission copy.
- About **Read Bio** modals (existing Kim Chen and Alexander Vladimirovich copy and photos). Do not paste onto the page. Do not rewrite in this pass.
- Stat strip **$1M Max Capital** (combined cap) and **&lt;24h Reward Processing**.
- Simulation disclaimers and hard rules on Instant / 1-Step / 2-Step pages.
- Restricted-country and US Platform 5 notes where they already live.
- Marketing pages (homepage, FAQ, About): no “we sell trading data” line.
- **Privacy Policy bans** (no external commercialization of trading behavior; P&L/strategy/behavior not shared externally; no sale of personal information). Do not replace them. Privacy this pass: data controller **Verodus L.L.C.-FZ**, plus a discretionary-payout sentence if one exists.

---

## 17. Implementation order

1. Homepage `<title>` / og:title / twitter:title → **Verodus | Up to $1M capital, 90% reward split.** Description unchanged.
2. FAQ / Terms / Privacy — remove “discretionary” on payouts only. Keep every Privacy ban (section 12).
3. Instant label + FAQ/dashboard/Terms “funded” word swaps (section 3). Do not change Privacy “funded account services.”
4. One legal name in footer / Terms / Risk. Privacy data controller and Contact line: **Verodus LLC → Verodus L.L.C.-FZ.**
5. Stat strip: reward split (and 3,000+ traders if you still want it). Keep $1M (combined cap).
6. About: fix “Architects of Scale,” swap “behavioral analysis.” Leave Read Bio modals as they are.
7. Certificates: keep. Unique IDs if missing; hide only duplicate tiles on this carousel — no copy rewrite.
8. Blog body numbers only, if they are wrong.

Do **not** include a hero rewrite, a line under the CTAs, a meta-description rewrite, a pricing-module rewrite, a Trustpilot rewrite, a bio rewrite, or a Privacy rewrite beyond the controller name and discretionary in this pass. Do **not** put data-sale language on marketing pages or in Privacy.

---

## 18. Founder bios (already in modals — keep)

The live modals already have photos, names, titles, and full copy. **Keep them.** Do not paste onto About. Do not rewrite in this pass.

**Kim Chen** — Co-Founder & Chief Executive Officer. Finance graduate; digital-asset background; CEO as strategist / roadmap / infrastructure access. Quote on world-class resources.

**Alexander Vladimirovich** — Co-Founder & Chief Operating Officer. Honors finance graduate; FX / risk-managed trading; COO on UX, infrastructure, payout processing, support. Quote on a reliable ecosystem.

What a stranger still cannot check from those modals: school names, prior employers, years, LinkedIn. That is off-site founder proof (registry, LinkedIn, one filmed AMA), not a copy rewrite this pass. Founder proof is not payout proof.
