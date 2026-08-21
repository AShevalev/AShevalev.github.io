# Verodus website — combined change spec

**Purpose:** One implementation list. Merges the surgical copy brief (`docs/verodus-website-wording-changes.md`) with the competitive-research recommendations (`docs/verodus-competitor-research-and-recommendations.md`).

**Not live yet.** Ship in the pass order below. Do not skip Pass 0 to jump to film, scaling, or Discord.

**This is a copy / product / proof spec, not a legal opinion.** Counsel should still review Terms, Risk Disclosure, Privacy, and any payout-guarantee or scaling language.

---

## How to use this file

| Pass | What it is | Feel it buys |
|---|---|---|
| **0** | Wording brief — light, surgical copy | Stops self-owning (discretionary, two LLCs, “Funded” Instant label) |
| **A** | Integrity — live contradictions the brief deferred | Stops SKU / blog / URL contradictions |
| **B** | Proof that can be true | Trustworthy |
| **C** | Commercial objects the category requires | Desirable |
| **D** | Premium layer | Established / premium feel |

Pass 0 keeps surrounding copy. Later passes may add pages, product rules, and proof objects the brief explicitly skipped.

**Where the two source docs disagree, this file wins.** Resolutions are in [Conflicts resolved](#conflicts-resolved).

---

## Locked across every pass (unless a later pass explicitly unlocks)

**Homepage hero — do not change.** Including:

- H1: **Funding Traders Worldwide.**
- Hero subhead: **Demonstrate consistency through structured evaluation and unlock measured performance rewards — no deposits, no client funds, no brokerage.**
- Hero CTAs: **Start Evaluation** / **Free Trial**
- The no-deposits pill. Do not add a second line under the CTAs repeating no deposit or adding “Simulated accounts.”

**Homepage meta description — do not change.** Same string on `og:description` and `twitter:description` if those tags exist:

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

Do not change inner-page `<title>` tags, canonical, or hreflang in Pass 0. Later passes may add new pages with their own titles.

**Privacy bans — keep exactly. Do not replace, soften, or add sale/license language.**

> Verodus does not use trading behavior data to replicate, commercialize, or exploit user trading strategies externally.

> Trader P&L, trading strategies, and behavior data may be shared internally only with risk management and compliance personnel to assess platform risk exposure, determine margin adjustments, and prevent prohibited trading activity. This information is not shared externally.

> Verodus does not sell personal information in exchange for monetary compensation and does not share personal data for independent third-party marketing without explicit user consent.

Do not put “we sell trading data” on the homepage, FAQ, About, or Privacy.

**Do not fake:** awards, $X00M paid, 100k traders, Deloitte/Forbes logos, MT5 wording if unlicensed, 100% split, $4M scale.

**Entity note:** Verodus LLC and Verodus L.L.C.-FZ are the **same company**. One public legal name everywhere.

---

## Product facts (do not treat these as errors)

- **$49** in meta is Instant at the **35% discount**, not a different SKU from the Instant table. Pass 0 does not “fix” $49 in the hero or meta. Pass C must make that price **true on the Instant table** (or introduce a SKU that matches).
- **$5k–$200k** in meta is **2-Step** account sizes. Instant does **not** offer $200k. Pass 0 leaves the Instant selector. **Pass A removes the Instant $200k column.**
- **$1M Max Capital** is the **combined** cap across accounts a trader can hold, not a single-account SKU.
- Trustpilot **4.5 / 5** already **links** to the Trustpilot page. Pass 0 keeps the badge. Pass B adds review **count** or stops leading with the score.
- Founder bios already live in **Read Bio** modals (photos + Kim Chen CEO copy + Alexander Vladimirovich COO copy). Do not paste them onto the About page. Do not rewrite those modals in Pass 0. Pass D may add **one external link each** (LinkedIn) when they exist — still not a bio rewrite.
- Homepage payout certificates are **legitimate Verodus certificates**. Keep the carousel. Do not hide it because some first names or amounts also appear on another firm’s site. Prefer unique certificate IDs (and date / rail / country when you can show them) so a stranger can tell each payout apart. Hide only **internal duplicates** on the Verodus carousel itself — not the section.

---

## Conflicts resolved

| Topic | Wording brief | Research rec | This spec |
|---|---|---|---|
| Instant $200k on homepage | Skip / leave selector | Remove — live contradiction | **Pass A: remove** Instant $200k from selector and table |
| Certificates | Unique IDs or hide if uniqueness cannot be verified; keep headline | Hide until uniquely Verodus; amounts overlap Goat Funded Trader | **Keep the carousel.** Operator confirmation: these are legitimate Verodus certificates. Pass 0: unique IDs if available; hide only duplicate rows **on Verodus**. Do not hide the section because another firm shows similar first names or amounts |
| Blog `best-simulated-prop-firm-2026.html` | Fix body numbers or unpublish; no rewrite; title/meta locked | Unpublish until it is not a launch manifesto | **Pass A: unpublish** unless the body can be corrected **and** “launching in 2026” / future tense / “best” claims are removed without a rewrite. If that needs a rewrite, unpublish |
| Stat strip “+3,000 Users” | Change to **3,000+ traders** | Demote user count; do not pair with $1M | **Pass 0:** 3,000+ traders + reward-split wording. **Pass A:** demote or drop user count from the first strip if still ~3,000 |
| Trustpilot badge | Keep **4.5 / 5**; no widget | Show N, or don’t lead with the score | **Pass 0:** keep. **Pass B:** `4.5 / 5 (N reviews)` if N is honest; otherwise text link without a score |
| Testimonials | Keep existing quotes | Replace with numbered, defensible stories | **Pass 0:** keep. **Pass B:** add or replace only with stories you can defend |
| How it works | Skip | Instant-specific path | **Pass 0:** skip. **Pass C:** Instant variant when Instant tab is selected |
| Pricing module | Skip leftover fee, no refund sentence | Later: $49 must be true on the table | **Pass 0:** skip leftover fee / refund line. **Pass A:** $200k Instant off. **Pass C:** table price earns the locked meta $49 |
| Footer | Legal-name line only | Company number, city, address | **Pass 0:** legal-name + payments affiliate line. **Pass B:** number, city, address, restricted-countries link |
| About | Heading + “behavioral analysis” only | Year, city, LinkedIn | **Pass 0:** heading + risk control. **Pass D:** year, city, one external link per founder |
| Discretionary | FAQ / Terms / About / Privacy if present | Also Trading Objectives leftover | **Pass 0:** listed swaps. **Pass A:** Trading Objectives CTA |

---

## Pass 0 — wording (surgical)

Light edits only. Keep existing sentences. Replace the flagged phrase. Do not rewrite the rest of the block. Do not reorder the homepage.

### 0.1 Homepage title (description locked)

Ship these three tags on the homepage. Do not touch the description.

```html
<title>Verodus | Up to $1M capital, 90% reward split</title>
<meta property="og:title" content="Verodus | Up to $1M capital, 90% reward split">
<meta name="twitter:title" content="Verodus | Up to $1M capital, 90% reward split">
```

Keep:

```html
<meta name="description" content="Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit.">
```

| Tag | Now | Change to |
|---|---|---|
| `<title>` | Instant from $49. Funded on Day One. (and any `Verodus —` prefix) | **Verodus \| Up to $1M capital, 90% reward split** |
| `og:title` | same as current title | **Verodus \| Up to $1M capital, 90% reward split** |
| `twitter:title` | same as current title | **Verodus \| Up to $1M capital, 90% reward split** |
| `name="description"` | Funded on day one from $49. … Keep 80%. No deposit. | **Keep. Do not change.** |

Homepage only. `$1M` is the combined-account cap. `90%` is the top reward split (On-Demand). Description still says Keep 80% (default). That pairing is intended.

### 0.2 Company name (site-wide, not the hero)

**Use**

- Brand: **Verodus**
- Legal (footer, Terms, Privacy data controller, Risk, contracts): **Verodus L.L.C.-FZ** once, then “Verodus”
- Privacy: rename the **data controller** (and the matching Contact line) from Verodus LLC to **Verodus L.L.C.-FZ**
- Payments line: **Payments are processed by Verodus Capital Inc., an affiliate of Verodus L.L.C.-FZ.**

**Stop using** mixing `Verodus LLC` and `Verodus L.L.C.-FZ` as if they were two firms.

**Suggested footer legal line (replace the legal-name line only):**

> © 2026 Verodus L.L.C.-FZ.  
> Payments processed by Verodus Capital Inc., an affiliate.

Do not rewrite the rest of the footer in Pass 0.

### 0.3 Remove “discretionary” (FAQ, About, Terms, Privacy)

Replace the word/sentence. Leave the rest of each answer as it is.

| Location | Cut | Put |
|---|---|---|
| Homepage FAQ “Is Verodus legitimate?” | “Performance rewards are discretionary payments based on simulated results.” | “If you meet the published rules and complete identity checks, we pay the performance reward for that cycle.” |
| Terms | “Performance Reward Rates or incentive remuneration are discretionary and are not liabilities of Verodus L.L.C.-FZ.” | “Performance rewards are paid when you meet the published program rules, remain eligible, and complete required identity checks. Rewards may be withheld, reduced, or clawed back if trading activity breaches those rules or the prohibited-practices policy. They are not investment returns.” |
| Privacy | Any sentence that calls performance rewards or incentive pay **discretionary** | Same replacement as Terms. **Do not change any other Privacy sentence except the data-controller name (0.8).** |
| About → Performance Rewards | “internal evaluation outcomes” | “the published rules, then a compliance review” |

**FAQ “Who Provides Our Liquidity?”** — replace only “retains discretion over” with “operates.” Keep the rest of the sentence.

Live Privacy (effective 21 February 2026) does not currently use the word “discretionary.” If a later Privacy draft adds it on payouts, swap that sentence only. Keep every Privacy **ban**.

### 0.4 Use “funded” less (labels and one phrase)

The hero already says “Funding Traders Worldwide.” Meta already says “Funded on day one from $49.” Swap the word below the hero. Do **not** rewrite Instant blurbs, Instant overview paragraphs, or FAQ answers around it.

| Where | Now | Change to |
|---|---|---|
| Instant card / phase label | Funded | Instant |
| Homepage FAQ Instant line | “Funded simulated account” | “Simulated Instant account” |
| Instant section 2 heading | Funded Account Rules | Instant Account Rules |
| Terms model list | Instant Funded | Instant |
| Dashboard | “funded accounts” | “Qualified Performance accounts” |

Leave Instant card body copy, Instant rules body, Plan FAQ body, and “Instant Funding” in-page titles as they are except the rows above. Do **not** change Instant page `<title>`. Do not change Privacy “deliver funded account services.”

**Optional one-line FAQ** (only if you add a new question; do not rewrite existing ones): “Is this a funded account?” — Instant has no evaluation phase. You trade a simulated account from day one. If you meet the published rules and pass identity checks, we pay a cash reward.

### 0.5 Stat strip (below the hero)

| Now | Change to |
|---|---|
| +3,000 Users Worldwide | **3,000+ traders** |
| Up to 90% Profit Split | **Up to 90% reward split** |

Keep 175+ Countries, **$1M Max Capital** (combined cap), and **&lt;24h Reward Processing** in Pass 0.

The later “Global reach” strip already says **Up to 90% Reward Split**. Make the first strip match it.

### 0.6 “Why Verodus” cards

Keep the section headline and intro. Keep all six cards. Do **not** add the US Platform 5 restriction to Supported Platforms. Do **not** add “Trading is simulated.” to No Personal Capital.

### 0.7 Instant / pricing module, How it works, calculator, bottom CTA

**Pass 0: skip.** Do not change the Instant size selector, leftover fee line, or add a refund sentence. Do not change the four How it works steps, calculator CTA, Rewards-your-way 24h line, or bottom CTA/subline. Dashboard: swap “funded accounts” only (0.4).

### 0.8 Payout / certificate section

Keep the headline **Real traders. Real certificates.** and the existing body sentences. **Keep the carousel.** These are legitimate Verodus certificates.

Operational: no placeholder names. No duplicate certificate **on this carousel** (same ID or same name+amount twice). Prefer unique certificate IDs. Optionally show date, rail, and country on each tile so the payout is easier to verify at a glance. Do not rewrite the section copy. Do not hide the section because another firm’s marketing uses similar first names or amounts.

### 0.9 Testimonials and Trustpilot

Keep **Rated 4.5 / 5 on Trustpilot** as it is. It already links. Do not replace it with a widget. Do not remove the number in Pass 0. Keep the existing quotes.

### 0.10 Homepage FAQ

Do not rewrite “What is Verodus?”, “I'm not a trader”, “When and how do I get paid?”, or “How much can I earn?”.

Only:

- “Is Verodus legitimate?” — swap the discretionary sentence (0.3). Keep the rest of that answer.
- “What evaluation models…?” — swap “Funded simulated account” for “Simulated Instant account.” Keep the hard rules as they are.

### 0.11 About page

Do not rewrite the opening paragraph or “Helping traders prove their edge.” Do not paste bios onto the page. Do not rewrite modal copy.

| Now | Change to |
|---|---|
| “Architects of ScaleEngineering the high-performance…” | **Leadership** (fix the smashed heading only) |
| “behavioral analysis” | “risk control” |

### 0.12 Privacy — controller name + keep the bans

| Location | Now | Change to |
|---|---|---|
| Data Controller | Verodus LLC, a company registered in the United Arab Emirates | **Verodus L.L.C.-FZ**, a company registered in the United Arab Emirates |
| Contact Information | Verodus LLC | **Verodus L.L.C.-FZ** |

Do not rewrite the rest of those paragraphs. Do not change sharing list, subprocessors, cookies, CCPA, or “deliver funded account services.” Discretionary-payout sentence only if one exists (same replacement as Terms).

### 0.13 Blog body (Pass 0 option)

`/best-simulated-prop-firm-2026.html` body numbers that do not match live Instant/1-Step/Lite: update those numbers, **or unpublish**. Do **not** change that page’s `<title>` or meta. Do not rewrite the article in Pass 0. Prefer **Pass A unpublish** if “launching in 2026” / future tense remains.

### 0.14 Words to prefer vs avoid (Pass 0 only)

Use only when a listed swap above already applies. Do not hunt the site to rewrite every instance.

| Avoid below the hero | Use instead |
|---|---|
| Funded (as Instant phase label) | Instant |
| Profit split (stat strip) | Reward split |
| Discretionary (payouts) | Paid under the published rules after eligibility checks |
| Behavioral analysis (About) | Risk control |

**Exception:** hero H1 may keep “Funding.” Meta description may keep “Funded on day one from $49.” Homepage `<title>` is **Verodus | Up to $1M capital, 90% reward split.**

### 0.15 Homepage order (Pass 0)

Do not reorder. Hero (including the no-deposits pill), stat strip, pricing, How it works, Trustpilot, and Why Verodus stay where they are.

### 0.16 Founder bios (keep)

**Kim Chen** — Co-Founder & Chief Executive Officer. Finance graduate; digital-asset background; CEO as strategist / roadmap / infrastructure access. Quote on world-class resources.

**Alexander Vladimirovich** — Co-Founder & Chief Operating Officer. Honors finance graduate; FX / risk-managed trading; COO on UX, infrastructure, payout processing, support. Quote on a reliable ecosystem.

What a stranger still cannot check from those modals: school names, prior employers, years, LinkedIn. That is Pass B/D off-site founder proof, not a Pass 0 copy rewrite. Founder proof is not payout proof.

### 0.17 Pass 0 — do not include

Hero rewrite, a line under the CTAs, meta-description rewrite, pricing-module rewrite, Trustpilot rewrite, bio rewrite, Privacy rewrite beyond the controller name and discretionary, data-sale language, Instant $200k removal (that is Pass A), How it works Instant variant (Pass C).

---

## Pass A — integrity (same sprint as Pass 0 if possible)

Do these even if Pass 0 copy is still landing. They are live contradictions.

1. **Certificates stay up.** If a certificate is missing an ID, add one. If the same name+amount appears twice **on Verodus**, remove the duplicate tile. Do not take the carousel down. Do not substitute anonymous quotes.
2. **Remove Instant $200,000** from the homepage Instant selector and fee table. Instant sizes are **$5k–$100k**. $200k remains a 2-Step size. Leave leftover-fee line and do not add a refund sentence under Instant (Instant fees stay non-refundable).
3. **Unpublish** `/best-simulated-prop-firm-2026.html` until it can be a sourced explainer with **current** Instant / 1-Step / Lite numbers, present tense, and no “best” / “launching in 2026.” If you only patch numbers and leave launch language, unpublish anyway. Do not change that page’s title/meta if it stays up.
4. **Redirect** `/about` → `/about.html`. **Fix `sitemap.xml` 500.**
5. **Trading Objectives** (`/trading-objectives.html`): one model at a time; Instant must not inherit 2-Step 10%/5% defaults. Replace leftover “eligible for discretionary performance rewards following internal review” with the same rules-based payout idea as Pass 0.3 (short: paid when published rules and identity checks are met; withheld on breach).
6. Confirm FAQ liquidity “retains discretion over” → **“operates”** (Pass 0.3) is live.
7. **Stat strip (optional in this pass):** if user count is still ~3,000, demote it. Preferred first strip: `175+ countries` · `<24h typical processing` · `Up to 90% reward split` · `Combined allocation up to $1M`. Do not invent a larger user number. Keep `$1M Max Capital` meaning as combined cap.

Simulation disclaimers and hard rules on Instant / 1-Step / 2-Step pages stay as they are except the discretionary leftover on Trading Objectives.

---

## Pass B — proof that can be true

8. **Public payouts page** (`/rewards` or `/payouts`): running list with certificate ID, date, amount, country, rail (Rise / crypto). Homepage carousel stays; this page is the deeper proof layer, fed by the same legitimate Verodus certificates.
9. **Trustpilot:** display **4.5 / 5 (N reviews)** only if N is honest. If N is tiny, use a text link “See independent reviews” and **do not lead** with the score. Still do not widget-ize unless volume supports it. Keep the existing quotes until numbered stories exist.
10. **Trader stories with numbers you can defend** (example shape: first Instant cycle, $180, Rise, 11 hours, country). Tie a story to a real Verodus certificate when the trader agrees. Existing generic quotes may stay until these exist; do not invent them.
11. **Footer (add, do not rewrite Pass 0 legal lines):** UAE company number / licence, city, postal address; Verodus Capital Inc. jurisdiction on the payments line; link to restricted countries. Keep the Pass 0 legal-name + affiliate lines.
12. **Off-site founder proof, then link:** registry extract, LinkedIn, one filmed AMA or office/support/payout walkthrough. Link from About. Do **not** paste extra bio copy onto About. Do **not** rewrite the Read Bio modals.

---

## Pass C — commercial objects

Hero and meta stay locked. Product/pricing must earn the locked meta.

13. **Reward-speed SLA — pick one number.** Homepage says &lt;24h; Instant rules say within 48 hours. Align to one published clock. Bind it: processed in that window or a published remedy (extra 10% on that cycle, a fixed credit, or 100% split on that reward). Counsel reviews the remedy. Do not claim &lt;24h without a cost to Verodus.
14. **Scaling / VIP page** (risk designs the numbers): example shape — after 2 successful cycles, +25% simulated size **or** +10% split; combined cap still **$1M** until you can raise it. Own URL. Optional How it works step 5. Do not advertise $2M–$4M until operations support it.
15. **Make meta prices true on the table.** Instant 5k at the 35% promo must actually be **$49**, and/or Lite must actually start at **$39**, and 1-Step at **$45**, matching the locked description. Do not edit the meta string. Do not “fix” $49 by changing the hero.
16. **How it works variant when Instant is selected:** Buy → Trade simulated Instant → Hit $100 + Best Day + selected cycle → KYC if not done → Reward. Do not show “Prove consistency” as step 2 for Instant. 1-Step / 2-Step keep the current four steps.
17. **Restricted countries + US Platform 5** linked from footer and FAQ. Do **not** add them to Why Verodus cards (Pass 0.6 still holds).
18. **Add-on comparison table** on Instant / 1-Step pages and checkout: Weekend Holding / Weekly 70% / On-Demand 90% — what each costs, what it changes. Existing add-ons, merchandised.
19. **$100k 2-Step presentation** equal in scan-ability to Instant (phases vs amounts toggle is good; default tab should match the paid-media keyword).

---

## Pass D — premium layer (after A–C)

20. **About (additive, not a rewrite of the opening / mission):** Pass 0 heading **Leadership** and “risk control” already shipped. Add founding year and city; one line that payments affiliate is the same group as Verodus Capital Inc. Leadership stays in Read Bio modals. Add **one** external link per founder when LinkedIn (or equivalent) exists. Do not paste modal copy onto the page.
21. Photography of real operators (office, support, payout ops) — not only dashboard chrome.
22. 60–90s product film: rules → dashboard → Rise payout.
23. Help taxonomy: Objectives (one URL per model), Payouts, Scaling, Platforms, Symbols, Restricted countries. Pages exist; they are not a library yet.
24. **Discord or nothing.** If the server is real, homepage community block with an honest member count. If not, remove Discord from FAQ until it is. FAQ already promises 24/7 Discord.
25. Platform naming: within licence limits, say what traders search for (e.g. industry-standard MT5-class terminal / TradingView-powered TradeHub). Do not invent “Platform 5” as a mystery fifth platform if the licence allows a clearer line. Do not add US Platform 5 restriction to Why Verodus cards.
26. English quality first. Multilingual later. Do not chase FundedNext’s 44-language flex.
27. Optional loop after Free Trial exists: loyalty, competition, or a free micro challenge — only after payout proof and the SLA are live.

---

## What not to change / not to add (all passes)

- Homepage **hero** (H1, subhead, no-deposits pill, CTAs). No second honesty line under the CTAs.
- Homepage **meta description** (locked string). Inner-page titles and descriptions in Pass 0.
- Why Verodus intro and cards, including Supported Platforms (no US Platform 5 add) and No Personal Capital (do not add “Trading is simulated”).
- Simulation disclaimers and hard rules on Instant / 1-Step / 2-Step pages (except Pass A Trading Objectives discretionary leftover).
- Restricted-country and US Platform 5 notes **where they already live**; Pass C only **links** them from footer/FAQ.
- About opening / mission copy.
- About **Read Bio** modal copy and photos (Pass D may add an external URL, not new prose).
- **Privacy Policy bans** (listed at the top). Privacy Pass 0: controller name + discretionary if present. No other Privacy rewrite.
- Marketing pages: no “we sell trading data.”
- Fake awards, fake payout totals, fake trader counts, unlicensed MT5 word, 100% split or $4M scale before proof and SLA exist.

---

## Implementation order (combined)

1. Homepage `<title>` / og:title / twitter:title → **Verodus | Up to $1M capital, 90% reward split.** Description unchanged.
2. FAQ / Terms / Privacy — remove “discretionary” on payouts only. Liquidity FAQ “operates.” Keep every Privacy ban. Privacy controller **Verodus L.L.C.-FZ**.
3. Instant label + FAQ / dashboard / Terms “funded” word swaps. Do not change Privacy “funded account services.”
4. One legal name in footer / Terms / Risk. Privacy controller and Contact: **Verodus LLC → Verodus L.L.C.-FZ.**
5. Stat strip: **Up to 90% reward split** and **3,000+ traders**. Keep $1M (combined cap) and &lt;24h.
6. About: fix “Architects of Scale,” swap “behavioral analysis.” Leave Read Bio modals.
7. Certificates: **keep.** Unique IDs if missing; drop only duplicate tiles on this carousel. No copy rewrite.
8. Pass A in the same sprint: Instant $200k off the Instant grid; unpublish launch blog; `/about` redirect; sitemap 500; Trading Objectives discretionary leftover; demote 3,000 if it still sits beside $1M.
9. Pass B: payouts page, honest Trustpilot N, defensible stories, footer company details, founder links / film.
10. Pass C: one payout clock + guarantee, scaling page, table prices that match locked meta, Instant How it works, footer/FAQ geo links, add-on table.
11. Pass D: About year/city, photography, product film, help IA, Discord-or-nothing.

---

## Internal positioning (do not put in the locked hero)

Win the Alpha Capital / Fintokei / For Traders intersection — not FundedNext volume or FTMO’s decade:

> A simulated evaluation firm that pays under published rules, shows every payout, and treats Instant as a risk product with honest drawdown — not as a lottery ticket.

Until Pass A is done, more marketing spend buys comparison-site skepticism, not prestige.

---

## Source docs

- Copy brief: [`docs/verodus-website-wording-changes.md`](verodus-website-wording-changes.md)
- Competitive research: [`docs/verodus-competitor-research-and-recommendations.md`](verodus-competitor-research-and-recommendations.md)
