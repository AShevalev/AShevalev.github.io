# Campaign — policy gate, setup, budget

## Part 1 · Policy gate — clear this before building a single ad

Meta classifies proprietary trading as a **restricted financial product**. Verify each item in Meta's Transparency Center and the **Authorisations and Verifications** tab in Business Settings; these rules moved in 2026 and third-party summaries go stale fast.

### 1 · Financial advertiser verification — the hard gate

Meta expanded mandatory verification for financial-services advertisers from 12 markets to roughly **38 in 2026**, each mapped to a local credential: **FCA** for the UK, **BaFin** for Germany, **SEC/FINRA** for the US, MiFID II authorisation across the EU. There is no single cross-border authorisation.

Verodus operates as a UAE entity (`Verodus L.L.C.-FZ` / `Verodus Capital Inc.`). Where it does not hold the required credential, ads will be rejected and repeated attempts put the ad account at risk.

**Do not run a broad country list on assumption.** Complete business verification, apply for financial-services authorisation, and target only cleared markets. If that list is short, run there and move the rest of the budget into organic and Discord.

### 2 · Special Ad Category — required, not optional

Since **21 Jan 2025** the **Financial products and services** category is mandatory for campaigns targeting the US, and is enforced in Canada and parts of Europe. Omitting it is itself a rejection reason.

It removes granular targeting — no postcode, restricted interests, 18+ floor. That costs nothing here because this plan is broad Advantage+ anyway.

### 3 · Bridge page — never link to checkout

Meta's crawler reads the destination. An ad pointing at a challenge purchase page is the most reliable way to get banned in the first review cycle.

Every ad lands on a **bridge page**: plain-English explanation of the evaluation, the published objectives, and the risk plus simulated-trading disclosure above the fold, then a link on to checkout. The pixel fires on the bridge.

Week 1 sidesteps this entirely — the **free trial is a compliant destination**, which is a reason the trial-first structure is worth keeping.

### 4 · The landing page is the weakest link

The ad copy in this pack is conservative. The homepage is not. Before any spend:

| On `verodus.com` | Why Meta flags it |
|---|---|
| "Get Funded & Trade — **Up to $1M Capital, 90% Profit Split**" | Implied outcome, and 90% headlined instead of presented as the on-demand add-on |
| The **reward calculator** projecting e.g. "$3,600" | An earnings projection — the clearest unrealistic-outcome trigger on the site |
| Payout certificates showing **dollar amounts** | Unsubstantiated performance claims |
| "Get funded" framing | Reads as funding provision, not simulated evaluation |

Keep them on the marketing site if you want. **The bridge page must contain none of them.**

---

## Part 2 · Account setup

1. Meta Pixel + Conversions API on `verodus.com`, including the bridge page.
2. Events by value: `Purchase` (value = fee paid) → `InitiateCheckout` → `CompleteRegistration` (free trial) → `ViewContent`.
3. Verify business and domain in Business Manager.
4. Page and business: **Verodus**. Advantage+ placements on.
5. Select the **Financial products and services** Special Ad Category. Age floor **18+**.
6. Bridge page carries the disclosure from [05-DISCLAIMERS.md](05-DISCLAIMERS.md) above the fold.
7. **No crypto in paid creative or copy.** Crypto wallet/exchange promotion needs separate written permission. Say "Rise — bank transfer or local methods."
8. Scale spend gently: **no more than 20–30% increase every few days.** Aggressive scaling on a new financial account reads as automated abuse.

Week 1 runs no Purchase objective. Weeks 2–4 optimise Purchase on **warm** traffic only. If Purchase events are still under ~20 by week 3, keep those ad sets on `InitiateCheckout`.

Never use the Page **Boost** button — it cannot optimise for Purchase. Duplicate a winning reel into Ads Manager instead.

---

## Part 3 · Budget — 4 weeks, $1,000 CAD

Paid media **$760**. Currency CAD.

| Week | Paid | Objective | Audience | Focus |
|---|---|---|---|---|
| 1 | **$150** | CompleteRegistration (trial) | Cold Advantage+ | Free trial, build the pixel |
| 2 | **$210** | $90 ViewContent (rules) + $120 Purchase | Rules cold/warm; Purchase warm | Rules education → first sales |
| 3 | **$200** | Purchase 70% + trial top-up 30% | Warm first | Product explainers convert trials |
| 4 | **$200** | Purchase | **Warm only, no cold** | Intro-offer close |

| Non-media | Paid |
|---|---|
| Founder content editing | $140 |
| Tools (CapCut / Canva) | $50 |
| Contingency — scale the one winner | $50 |

**Kill rules.** Pause any Purchase ad above **$40 CAD CPA** after 1,000 impressions and 3+ purchases. Cap trial cost at **$8 CAD**. Instant $5k contributes roughly $28 USD before ad cost, so a $40 CPA erases the unit.

Do not spend the contingency on Instant $25k+ or a second discount code.

### Audiences

- **Cold:** Advantage+ broad, age 18+ (category floor), skew 22–44, English. Geos limited to markets where the financial-services authorisation is held.
- **Warm:** 7/14/30-day trial signups, site visitors, IG/FB engagers, 50% video viewers.
- Exclude purchasers 180 days on every Purchase ad set.
- Attribution 7-day click, 1-day view.
- Do not split by interest (Forex, FTMO, crypto) — broad finds buyers cheaper at this budget.

### Placements

On: Facebook Feed, Instagram Feed, Stories, Reels, Explore.
Off: Audience Network, right-hand column, Messenger inbox.

Upload **1:1** for feed and **9:16** for Stories/Reels on every ad.

---

## Part 4 · Measurement

| Metric | Target |
|---|---|
| Cost per free trial | Falling weekly; kill above $8 CAD |
| 3-second hook rate | Kill under 25%, scale over 45% |
| Trial → paid conversion | The core month-1 outcome |
| Purchase CPA | ≤ $40 CAD Instant $5k · ≤ $25 CAD 1-Step $5k |
| Accounts sold | First paying cohort — **0 Instant $25k+ from ads** |
| Warm audience size | Growing every week to feed week 4 |

Tracking: UTM `utm_source=meta&utm_medium=paid&utm_campaign=founders&utm_content={{ad.name}}`. Ad names match `utm_content`.

What success looks like on this budget: a first paying cohort actively trading, a warm audience worth retargeting, and clean creative data. Not mass sales.
