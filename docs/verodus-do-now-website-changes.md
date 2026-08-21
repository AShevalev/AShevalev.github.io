# Verodus website — do now

**This is the only list to implement now.** Surgical copy plus the operator decisions already made. Do not start Pass B–D, Instant $200k work, certificate IDs, How it works variants, or positioning copy.

**Complete changelog (use this to ship):** [`docs/verodus-website-changelog.md`](verodus-website-changelog.md) — live Find/Put strings, files, order, QA. **Keep the same HTML, Title Case, and sentence shape as the live string.**

Hero and homepage meta description stay locked. Counsel still reviews Terms, Risk, Privacy, and any payout-SLA wording.

Source: [`docs/verodus-website-wording-changes.md`](verodus-website-wording-changes.md) plus operator confirmations recorded in [`docs/verodus-combined-website-changes.md`](verodus-combined-website-changes.md).

---

## Locked — do not change

- Homepage **hero** (H1 **Funding Traders Worldwide.**, subhead, no-deposits pill, **Start Evaluation** / **Free Trial**). No extra line under the CTAs.
- Homepage **meta description** (and og/twitter description if present):

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

- Inner-page `<title>` tags, canonical, hreflang.
- Instant size selector and fee table, including **$200k**. Leftover fee line. No new refund sentence. Instant fees stay non-refundable.
- Certificate carousel — **legitimate Verodus certificates.** Keep headline **Real traders. Real certificates.** and the tiles. Do not add IDs, date, country, or rail. Do not hide the section. Do not substitute quotes.
- How it works four steps (same for Instant, 1-Step, 2-Step).
- Calculator, Rewards-your-way block, bottom CTA.
- Why Verodus intro and six cards (no US Platform 5 on Supported Platforms; no “Trading is simulated” on No Personal Capital).
- Trustpilot **Rated 4.5 / 5** (already links). Existing testimonial quotes.
- About opening / mission. Read Bio modals (Kim Chen, Alexander Vladimirovich).
- `/trading-objectives.html` in full.
- Simulation disclaimers and hard rules on Instant / 1-Step / 2-Step pages, except Instant “within 48 hours” → **&lt;24h** (below).
- Privacy bans (no external commercialization of trading behavior; P&L/strategy not shared externally; no sale of personal information).
- No US Platform 5 / MT5 restriction in the **footer**.
- No payout rail (Rise / crypto) on certificates.
- No internal positioning copy.
- Homepage order. Do not reorder.

**Facts:** `$49` in meta = Instant at 35% off. `$5k–$200k` in meta = 2-Step sizes. `$1M` = combined cap. **3,000+ traders** is accurate. Verodus LLC and Verodus L.L.C.-FZ are the same company.

---

## 1. Homepage title (description unchanged)

```html
<title>Verodus | Up to $1M capital, 90% reward split</title>
<meta property="og:title" content="Verodus | Up to $1M capital, 90% reward split">
<meta name="twitter:title" content="Verodus | Up to $1M capital, 90% reward split">
```

`$1M` = combined cap. `90%` = On-Demand top split. Description still says Keep 80% (default).

---

## 2. One legal name

**Use:** brand **Verodus**. Legal **Verodus L.L.C.-FZ** once, then “Verodus.”

Footer legal line only — same `<p style="margin-bottom:1rem">`. Keep **All Rights Reserved.** Do not rewrite the rest of the footer; do not add Platform 5 / MT5 there:

> © 2026 Verodus L.L.C.-FZ. All Rights Reserved.

Add a sibling `<p>` in that same style:

> Payments processed by Verodus Capital Inc., an affiliate.

Payments line wherever it exists: **Payments are processed by Verodus Capital Inc., an affiliate of Verodus L.L.C.-FZ.**

Privacy data controller and Contact: **Verodus LLC** → **Verodus L.L.C.-FZ**. Same for Terms / Risk legal name. Stop mixing the two names as if they were two firms.

---

## 3. Remove “discretionary” on payouts

Replace the sentence only. Leave the rest of each block.

| Location | Cut | Put |
|---|---|---|
| Homepage FAQ “Is Verodus legitimate?” | “Performance rewards are discretionary payments based on simulated results.” | “If you meet the published rules and complete identity checks, we pay the performance reward for that cycle.” |
| Terms | “are discretionary and are not liabilities of Verodus L.L.C.-FZ.” | “are paid when you meet the published program rules, remain eligible, and complete required identity checks, and may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy.” Keep the subject **Performance Reward Rates or incentive remuneration** and the next sentence **They do not constitute financial returns, investment profits, or guaranteed compensation.** |
| Privacy | Any payout sentence that says **discretionary** | Same as Terms. Live Privacy (21 Feb 2026) may not use the word — then skip. |
| About → Performance Rewards | “internal evaluation outcomes” | “the published rules, then a compliance review” |

FAQ **Who Provides Our Liquidity?** — replace only “retains discretion over” with **“operates.”**

Do **not** edit `/trading-objectives.html`.

---

## 4. Use “funded” less (below the hero)

| Where | Now | Change to |
|---|---|---|
| Instant card / phase label | Funded | Instant |
| Homepage FAQ Instant line | “Funded simulated account” | “Simulated Instant account” |
| Instant section 2 heading | Funded Account Rules | Instant Account Rules |
| Terms model list | Instant Funded | Instant |
| Dashboard | “funded accounts” | “Qualified Performance accounts” |

Do not rewrite Instant body copy, Plan FAQ bodies, Instant page `<title>`, or Privacy “deliver funded account services.”

---

## 5. Stat strip

| Now | Change to |
|---|---|
| `+3,000` / `Users Worldwide` | `3,000+` / `Traders` (keep value + Title Case label; do not merge) |
| `Up to 90%` / `Profit Split` | `Up to 90%` / `Reward Split` (same Title Case as Global reach) |

Keep **175+** / **Countries**, **$1M** / **Max Capital**, **&lt;24h** / **Reward Processing**. Global reach already says **Reward Split** — match that casing. Change its `+3,000` to `3,000+`; leave **Traders**.

---

## 6. About

| Now | Change to |
|---|---|
| `The Architects of Scale<br>Engineering the high-performance…` | `Leadership<br>Engineering the high-performance…` (keep the `<h3>` and `<br>`) |
| “behavioral analysis” | “risk control” |

Do not paste bios onto the page. Do not rewrite modals.

---

## 7. Reward speed: **&lt;24h**

Homepage **&lt;24h Reward Processing** stays.

On Instant rules, keep `<strong>Minimum Reward:</strong> $100 (` and change **within 48 hours** to **in under 24 hours**. Do not use 48h as the SLA.

Do not add a penalty/remedy line in this pass unless counsel already has approved copy.

---

## 8. Homepage FAQ (only these two)

- “Is Verodus legitimate?” — discretionary swap (section 3). Rest of the answer stays.
- “What evaluation models…?” — “Funded simulated account” → **Simulated Instant account.** Hard rules stay.

Do not rewrite the other FAQ answers.

---

## 9. Privacy bans — keep exactly

> Verodus does not use trading behavior data to replicate, commercialize, or exploit user trading strategies externally.

> Trader P&L, trading strategies, and behavior data may be shared internally only with risk management and compliance personnel to assess platform risk exposure, determine margin adjustments, and prevent prohibited trading activity. This information is not shared externally.

> Verodus does not sell personal information in exchange for monetary compensation and does not share personal data for independent third-party marketing without explicit user consent.

This pass: controller name + discretionary payout sentence if one exists. Nothing else.

---

## Words (only where a row above already applies)

| Avoid below the hero | Use |
|---|---|
| Funded (Instant phase label) | Instant |
| Profit Split (stat label) | Reward Split |
| Discretionary (payouts) | Paid under the published rules after eligibility checks |
| Behavioral analysis (About) | Risk control |

Hero may keep “Funding.” Meta may keep “Funded on day one from $49.”

---

## Not now (explicitly skipped or later)

- Instant **$200k** column / selector
- Certificate IDs, dates, country, rail, duplicate-tile hunt, hiding the carousel
- `/trading-objectives.html`
- Instant How it works variant; How it works step 5
- Scaling own URL; $2M–$4M copy
- US Platform 5 / MT5 in the footer
- Internal positioning (Alpha / Fintokei / For Traders blurb)
- Payouts page, Trustpilot review count, filmed bios, photography, Discord homepage block, add-on comparison table, making table prices match locked meta $49, `/about` redirect, sitemap 500, unpublishing the blog — unless you ask for those next
