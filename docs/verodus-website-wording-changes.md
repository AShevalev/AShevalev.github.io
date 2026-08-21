# Verodus website wording changes

**Purpose:** Light, surgical copy fixes. Do not rewrite sections that already work.  
**Hero: do not change.** Leave the homepage hero exactly as it is, including:

- H1: **Funding Traders Worldwide.**
- Hero subhead: **Demonstrate consistency through structured evaluation and unlock measured performance rewards — no deposits, no client funds, no brokerage.**
- Hero CTAs: **Start Evaluation** / **Free Trial**

**Meta: do not change.** Leave document title, meta description, Open Graph, Twitter cards, and canonical tags as they are.

Homepage meta description stays exactly:

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

Use that same `content` on `og:description` and `twitter:description` if those tags exist. Do not rewrite prices, “Funded on day one,” “Keep 80%,” or the $5k–$200k range in meta.

Homepage `<title>` / og:title stays **Instant from $49. Funded on Day One.** (and the live `Verodus —` prefix if present). Inner-page titles and meta stay as they are.

**Scope:** Swap a word or one sentence where listed below. Do **not** rewrite surrounding copy.

**Entity note:** Verodus LLC and Verodus L.L.C.-FZ are the **same company**. Use one public legal name everywhere.

This is a copy brief, not a legal opinion. Counsel should still review Terms, Risk Disclosure, Privacy, and any payout language.

---

## Locked: homepage hero

No copy, price, or “funded” changes in the hero block.

The Instant table currently starts at **$72**, not $49. Do **not** “fix” that by editing the hero or the meta.

Use **funded** less **everywhere else**. The hero already carries the search term.

---

## Locked: meta (all pages)

Do **not** change:

- `<title>`
- `<meta name="description">`
- `og:title`, `og:description`, `og:url`, `og:image`
- `twitter:title`, `twitter:description`, `twitter:image`
- canonical / hreflang

**Homepage description (locked):**

> Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.

Inner-page titles stay as they are even when a single on-page word changes.

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
- Legal (footer, Terms, Privacy, Risk, contracts): **Verodus L.L.C.-FZ** once, then “Verodus”
- Payments line: **Payments are processed by Verodus Capital Inc., an affiliate of Verodus L.L.C.-FZ.**

**Stop using**

- Mixing `Verodus LLC` and `Verodus L.L.C.-FZ` as if they were two firms (they are not)

**Suggested footer legal line (replace the legal-name line only):**

> © 2026 Verodus L.L.C.-FZ.  
> Payments processed by Verodus Capital Inc., an affiliate.

Do not rewrite the rest of the footer.

---

## 2. Remove “discretionary” (FAQ, About, Terms)

Replace the word/sentence. Leave the rest of each answer as it is.

| Location | Cut | Put |
|---|---|---|
| Homepage FAQ “Is Verodus legitimate?” | “Performance rewards are discretionary payments based on simulated results.” | “If you meet the published rules and complete identity checks, we pay the performance reward for that cycle.” |
| Terms | “Performance Reward Rates or incentive remuneration are discretionary and are not liabilities of Verodus L.L.C.-FZ.” | “Performance rewards are paid when you meet the published program rules, remain eligible, and complete required identity checks. Rewards may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy. They are not investment returns.” |
| About → Performance Rewards | “internal evaluation outcomes” | “the published rules, then a compliance review” |

**FAQ “Who Provides Our Liquidity?”** — replace only “retains discretion over” with “operates.” Keep the rest of the sentence.

---

## 3. Use “funded” less (labels and one phrase, not full rewrites)

The hero and meta already say “Funding Traders Worldwide,” “Funded on Day One,” and “Funded on day one from $49.”

Swap the word. Do **not** rewrite Instant blurbs, Instant overview paragraphs, or FAQ answers around it.

| Where | Now | Change to |
|---|---|---|
| Instant card / phase label | Funded | Instant |
| Homepage FAQ Instant line | “Funded simulated account” | “Simulated Instant account” |
| Instant section 2 heading | Funded Account Rules | Instant Account Rules |
| Terms model list | Instant Funded | Instant |
| Dashboard | “funded accounts” | “Qualified Performance accounts” |
| Privacy legal basis | “deliver funded account services” | “deliver evaluation and Qualified Performance services” |

Leave Instant card body copy, Instant rules body, Plan FAQ body, and “Instant Funding” in-page titles as they are except the rows above. Do **not** change Instant page `<title>`.

**Optional one-line FAQ** (only if you add a new question; do not rewrite existing ones): “Is this a funded account?” — Instant has no evaluation phase. You trade a simulated account from day one. If you meet the published rules and pass identity checks, we pay a cash reward.

---

## 4. Stat strip (below the hero)

| Now | Change to |
|---|---|
| +3,000 Users Worldwide | **3,000+ traders** |
| Up to 90% Profit Split | **Up to 90% reward split** |

Keep 175+ Countries, **$1M Max Capital**, and **&lt;24h Reward Processing** exactly as they are.

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

Do **not** change the Instant size selector, the $200k row, the leftover fee line, or add a refund sentence under the table.

Leave the simulation disclaimers on Instant / 1-Step / 2-Step rule pages as they are.

---

## 7. How it works, calculator, bottom CTA — skip

Keep the four steps, calculator CTA, Rewards-your-way 24h line, and bottom CTA/subline as they are.

Dashboard: swap “funded accounts” only (section 3). Do not rewrite the dashboard intro.

---

## 8. Payout / certificate section

Keep the headline **Real traders. Real certificates.** and the existing body sentences.

Operational only: no duplicate amounts, no placeholder names. Prefer unique certificate IDs. If uniqueness cannot be verified, hide the carousel. Do not rewrite the section copy.

---

## 9. Testimonials and Trustpilot

Keep **Rated 4.5 / 5 on Trustpilot** as it is. Do not replace it with a widget, and do not remove the number.

Keep the existing quotes. Do not rewrite them.

---

## 10. Homepage FAQ

Do not rewrite “What is Verodus?”, “I'm not a trader”, “When and how do I get paid?”, or “How much can I earn?”.

Only:

- “Is Verodus legitimate?” — swap the discretionary sentence (section 2). Keep the rest of that answer.
- “What evaluation models…?” — swap “Funded simulated account” for “Simulated Instant account.” Keep the hard rules as they are.

---

## 11. About page

Do not rewrite the opening paragraph or “Helping traders prove their edge.” Bios stay in the existing **Read Bio** modals — do not put them on the page.

| Now | Change to |
|---|---|
| “Architects of ScaleEngineering the high-performance…” | **Leadership** (fix the smashed heading only) |
| “behavioral analysis” | “risk control” |

---

## 12. Privacy (entity name only)

| Now | Change to |
|---|---|
| Data controller / contact: **Verodus LLC** | **Verodus L.L.C.-FZ** |

Also the “funded account services” phrase in section 3. Do not rewrite the rest of Privacy. Do not put data-licensing language on marketing pages.

---

## 13. Blog body (meta stays locked)

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

**Exception:** hero H1 and locked meta may keep “Funding” / “Funded on Day One” / “Funded on day one from $49.”

---

## 15. Homepage order

Do not reorder the page. Hero, meta, pricing module, How it works, Trustpilot score, and Why Verodus cards stay where they are.

---

## 16. What not to change

- **Homepage hero** (H1, subhead, CTAs).
- **Meta on every page.** Homepage description stays **Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.**
- Instant / pricing module (sizes, $200k row, leftover fee line, no new refund sentence).
- Why Verodus intro and cards, including **Supported Platforms** (no US Platform 5 add) and **No Personal Capital** (do not add “Trading is simulated.”).
- How it works steps, calculator, bottom CTA.
- Trustpilot **Rated 4.5 / 5** (do not widget-ize or remove).
- Existing testimonial quotes.
- FAQ answers other than the two phrase swaps in section 10.
- About opening / mission copy.
- About **Read Bio** modals (already in place; do not add on-page bios).
- Stat strip **$1M Max Capital** and **&lt;24h Reward Processing**.
- Simulation disclaimers and hard rules on Instant / 1-Step / 2-Step pages.
- Restricted-country and US Platform 5 notes where they already live.

---

## 17. Implementation order

1. FAQ “Is Verodus legitimate?” — remove “discretionary” only.
2. Instant label + FAQ/dashboard/Terms “funded” word swaps (section 3).
3. One legal name in footer / Privacy / Terms.
4. Stat strip: reward split (and 3,000+ traders if you still want it).
5. About: fix “Architects of Scale,” swap “behavioral analysis.” Skip bios — they are already modals.
6. Certificates: unique IDs or hide duplicates — no copy rewrite.
7. Blog body numbers only, if they are wrong.

Do **not** include a hero rewrite, a meta rewrite, a pricing-module rewrite, or a Trustpilot rewrite in this pass.
