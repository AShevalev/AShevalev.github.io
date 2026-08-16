# Verodus Meta ads — $1,000 campaign

Run this in **Meta Ads Manager** (Facebook + Instagram). Do not boost posts from the Page. Boosted posts cannot optimize for Purchase.

**Hero SKUs only**

| Plan | Size | Street (VERO35) | Why it is in the ads |
|---|---|---|---|
| Instant | $5,000 | **$72** | Prints (~+39%). No profit target. |
| Instant | $10,000 | **$121** | Prints (~+28%). Secondary Instant only. |
| 1-Step | $5,000 | **$36** | Highest margin per impression (~+76%). |
| 1-Step | $10,000–$25,000 | $60 / $120 | Still prints. Do not pin in ads. |

**Never put in ads, pins, or Instant Forms**

- Instant $25,000 / $50,000 / $100,000 / $200,000 (live Instant $50k+ is below break-even)
- “Cheapest Instant” / matching Blue Guardian $54
- Income promises, “get funded and get rich,” fake payout screenshots
- A second discount on top of VERO35

Landing pages

- Instant: `https://www.verodus.com/?utm_source=meta&utm_medium=paid&utm_campaign=print_skus&utm_content={{ad.name}}`
- 1-Step: same URL (homepage tabs). If a dedicated 1-Step checkout exists, swap it in.
- Free trial: homepage **Free Trial** CTA, same UTM with `utm_content=trial`
- Code: **VERO35** (already 35% sitewide). Put it in copy. Do not stack another code.

---

## Before you spend $1

1. Install the Meta Pixel + Conversions API on `verodus.com`.
2. Events, in this order of value: `Purchase` (value = fee paid) → `InitiateCheckout` → `CompleteRegistration` (free trial) → `ViewContent`.
3. Verify domain in Business Manager.
4. Business + Page: use **Verodus**. Turn on **Advantage+ placements** (Feed, Stories, Reels, Explore).
5. Special Ad Categories: leave **off** unless Meta flags it. This is a simulated evaluation fee, not housing/credit/employment. If Meta forces **Financial products**, accept it and keep claims conservative (copy below already is).
6. Landing page must say **simulated**, fee ≠ trading capital, rewards **discretionary / not guaranteed**. Homepage already does this — do not send ads to a hype page that strips the disclaimer.

If the pixel has **fewer than 50 purchases in 7 days**, optimize Campaign A for `InitiateCheckout` for 3 days, then switch to `Purchase`.

---

## Budget — 14 days, $1,000

Daily budget **$71.43**. Campaign budget optimization **on**.

| Campaign | Objective | $ | Days | Daily |
|---|---|---|---|---|
| A — Print SKUs | Sales / Purchase | **$700** | 14 | $50 |
| B — Free trial | Sales / CompleteRegistration (or Lead) | **$150** | 14 | $11 |
| C — Retargeting | Sales / Purchase | **$150** | 14 | $11 |

Do **not** run a cold traffic campaign. $1,000 is too small to pay for clicks that never check out.

Kill rule: pause any ad with **CPA > $40** after 1,000 impressions **and** 3+ purchases (or 8+ checkouts if still on InitiateCheckout). Instant $5k contribution is ~$28 before CPA; a $40 ad CPA wipes the unit.

---

## Campaign A — Print SKUs ($700)

**Advantage+ Sales**, CBO, Advantage+ placements, Advantage+ audience.

### Ad set A1 — Instant $5k (60% of A ≈ $420)

- Conversion: Purchase
- Attribution: 7-day click, 1-day view
- Audience: Advantage+ (broad). Age **22–44**. Languages: English.
- Geos (start here): United States, United Kingdom, Canada, Australia, UAE, Germany, Netherlands, Singapore, South Africa, Nigeria, Philippines, India, Brazil. Remove any country that declines checkout or triggers chargebacks.
- Exclusions: purchasers last 180 days (pixel `Purchase`).
- Creatives: `instant-5k-feed.png`, `instant-5k-story.png`, carousel 01–04, copy set **INSTANT**.

### Ad set A2 — 1-Step $5k (40% of A ≈ $280)

- Same targeting as A1.
- Creatives: `onestep-5k-feed.png`, `onestep-5k-story.png`, carousel 02 + 04, copy set **ONESTEP**.

Do not split by interest (Forex, FTMO, crypto). Meta will find traders cheaper on broad than you will with 2019 interest stacks.

---

## Campaign B — Free trial ($150)

Cold audience, same geos, optimize for **CompleteRegistration** (trial signup).

Purpose: cheap pixel data + retargeting pool. Trial users who never buy are the cheapest warm traffic you can own.

Creatives: `freetrial-story.png`, `clarity-feed.png`, copy set **TRIAL**.

Cap: if trial CPA > $8, pause B and move remainder into C.

---

## Campaign C — Retargeting ($150)

**Manual** sales campaign (not Advantage+), so you can force the audience.

Ad set C1 — 7-day website visitors who viewed Instant or checkout but did not Purchase.  
Ad set C2 — 14-day Instagram/Facebook engagers + video 50% viewers + trial signups who did not Purchase.

Exclude purchasers 180 days.

Creatives: `vero35-feed.png`, `payouts-feed.png`, `instant-5k-feed.png`, copy set **RETARGET**.

---

## Placements

On: Facebook Feed, Instagram Feed, Instagram Stories, Instagram Reels, Facebook Stories, Instagram Explore, Reels overlay.

Off: Audience Network, right-hand column, Messenger inbox (low quality for this offer).

Use **1:1** for feed, **9:16** for Stories/Reels. Upload both on every ad; Meta will pick.

---

## Tracking checklist

| Item | Value |
|---|---|
| Pixel | Verodus Purchase with `value` + `currency` |
| UTM | `utm_source=meta&utm_medium=paid&utm_campaign=print_skus` |
| Code | VERO35 |
| Ad names | `A1_INSTANT5K_FEED_01` style — matches `utm_content` |
| Offer | Do not add Instant-only extra % |

---

## What “good” looks like on $1,000

| Metric | Target |
|---|---|
| CPM | $8–18 (EN geos) |
| CTR (all) | ≥ 1.2% |
| CPC | ≤ $1.20 |
| Checkout rate | ≥ 8% of landing sessions |
| Purchase CPA | **≤ $28** Instant $5k · **≤ $18** 1-Step $5k |
| Purchases | 25–45 mixed Instant $5k / 1-Step $5k |
| Instant $25k+ share | **0%** of attributed sales |

If Meta’s algorithm starts converting Instant $50k/$100k from the homepage picker, add a dedicated Instant $5k checkout URL or hide $50k+ Instant from the default Instant tab on the ad landing page.

---

## Meta policy — copy you must not run

- “Guaranteed payout / guaranteed funding / risk-free profits”
- “Make $X per week” or lifestyle (cars, jets, cash guns)
- Personal attributes: “Still failing FTMO?” as a *you* statement
- Hiding that trading is **simulated**
- Before/after income graphics

Allowed: published rules, one-time fee, VERO35, free trial, “performance rewards are discretionary,” payout rails (Rise / crypto), under-24h processing **as an operations claim**, not an earnings claim.
