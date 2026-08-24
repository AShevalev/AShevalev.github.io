# Verodus Meta ads — $1,000 CAD · 4 weeks

Master plan: [`LAUNCH-PLAN.md`](LAUNCH-PLAN.md) (Atria funnel + operator-book SKU rules).

Run this in **Meta Ads Manager** (Facebook + Instagram). Do not use the Page **Boost** button. Duplicate a winning Reel into Ads Manager if you want to pay to amplify it.

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

- Instant: `https://www.verodus.com/?utm_source=meta&utm_medium=paid&utm_campaign=launch4w&utm_content={{ad.name}}`
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
6. Landing page must say **simulated** and fee ≠ trading capital. Homepage already does this — do not send ads to a hype page that strips the disclaimer.

**Fix the site wording first.** Our copy says rewards are **rule-based** — you meet the published objectives, the reward is due. The live site currently says the opposite in two places: the FAQ ("performance rewards are **discretionary** payments") and the objectives page ("eligible for **discretionary** performance rewards following internal review"). Ads that promise rule-based rewards while the linked page says discretionary is the exact inconsistency traders screenshot and chargeback teams flag. Update the FAQ, objectives page, and Terms to rule-based language before this campaign goes live, or the ads will contradict the landing page.

Week 1 has no Purchase objective. Weeks 2–4 optimize Purchase only on **warm** traffic. If Purchase events stay under ~20 by week 3, keep optimizing W2/W3 Purchase sets for `InitiateCheckout` until they do.

---

## Budget — 4 weeks, $1,000 CAD

Paid media **$760 CAD**. Rest is edit/tools/contingency (`LAUNCH-PLAN.md`).

| Week | CAD | Objective | Audience | Creatives |
|---|---|---|---|---|
| 1 | **$150** | CompleteRegistration (trial) | Cold Advantage+ | `tryfree-feed.png`, `freetrial-story.png`, `clarity-feed.png`, manifesto video |
| 2 | **$210** | $90 ViewContent (rules) + $120 Purchase | Rules = cold/warm; Purchase = trial + 50% video | `static-dd-feed.png`, Instant $5k, 1-Step $5k |
| 3 | **$200** | Purchase (70%) + trial top-up (30%) | Warm first | AMA video, walkthrough, `payouts-feed.png` (rails only) |
| 4 | **$200** | Purchase | Warm only — no cold | `founding-feed.png`, `lastchance-story.png`, Instant/1-Step $5k |

Geos, age 22–44, EN, Advantage+ placements: same as below. Exclude purchasers 180 days on every Purchase ad set.

Kill rule: pause any **Purchase** ad with CPA **> $40 CAD** after 1,000 impressions and 3+ purchases. Cap trial CPA at **$8 CAD**. Instant $5k contribution is ~$28 USD before ads.

Do not split by interest (Forex, FTMO, crypto).

### Always-on audiences (reuse each week)

- **Cold:** Advantage+ broad. Age 22–44. US, UK, CA, AU, UAE, DE, NL, SG, ZA, NG, PH, IN, BR.
- **Warm:** 7/14/30-day trial signups, site visitors, IG/FB engagers, video 50% viewers.
- Attribution: 7-day click, 1-day view.

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
| UTM | `utm_source=meta&utm_medium=paid&utm_campaign=launch4w` |
| Code | VERO35 |
| Ad names | `A1_INSTANT5K_FEED_01` style — matches `utm_content` |
| Offer | Do not add Instant-only extra % |

---

## What “good” looks like on $1,000 CAD

| Metric | Target |
|---|---|
| Cost per free trial | Drive down weekly; kill > $8 CAD |
| Hook rate (3s) | Kill <25%; scale >45% |
| Trial → paid | Core month-1 outcome |
| Purchase CPA | **≤ $40 CAD** Instant $5k · **≤ $25 CAD** 1-Step $5k |
| Accounts sold | First cohort; **0 Instant $25k+ from ads** |
| Warm audience | Grow every week for week 4 |

If Meta’s algorithm starts converting Instant $50k/$100k from the homepage picker, add a dedicated Instant $5k checkout URL or hide $50k+ Instant from the default Instant tab on the ad landing page.

---

## Meta policy — copy you must not run

- “Guaranteed payout / guaranteed funding / risk-free profits”
- “Make $X per week” or lifestyle (cars, jets, cash guns)
- Personal attributes: “Still failing FTMO?” as a *you* statement
- Hiding that trading is **simulated**
- Before/after income graphics

Allowed: published rules, one-time fee, VERO35, free trial, “rewards are rule-based and paid on the published objectives,” payout rails (Rise / crypto).

**Payout speed is allowed** as an operations claim: “most rewards process in under 24 hours,” matching the homepage. Keep “most” and never present it as guaranteed or as an earnings claim. Do not imply a trader is paid within 24 hours of purchase — the first reward also requires a **$100 minimum and 3 trading days**, and the objectives page quotes a **48-hour** window for that first payout.
