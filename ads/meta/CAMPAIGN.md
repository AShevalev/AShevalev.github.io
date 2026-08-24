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

## Policy gate — clear this before you build a single ad

Meta treats proprietary trading as a **restricted financial product**, and the copy is not what gets accounts banned — the funnel and the destination are. Four blockers, in order. Verify each in Meta's Transparency Center and the **Authorisations and Verifications** tab in Business Settings, because these rules moved in 2026 and secondary write-ups go stale.

**1 · Financial advertiser verification (hard gate).** Meta expanded mandatory verification for financial-services advertisers from 12 markets to roughly **38 in 2026**, and each market is mapped to a local credential — **FCA** for the UK, **BaFin** for Germany, **SEC/FINRA** for the US, MiFID II authorisation across the EU. There is no single cross-border authorisation. Verodus operates as a UAE entity (`Verodus L.L.C.-FZ` / `Verodus Capital Inc.`); if it does not hold the credential for a market, ads to that market will be rejected and repeated attempts risk the ad account.

→ **Do not launch the 13-country list below as written.** Complete business verification, then apply for financial-services authorisation and target **only** the markets you are cleared for. If that is a short list, run there and put the rest of the budget into organic and Discord.

**2 · Special Ad Category is required, not optional.** Since 21 Jan 2025 the **Financial products and services** category is mandatory for any campaign targeting the US, and it is enforced in Canada and parts of Europe. Select it. Ads may be rejected for omitting it. It costs you granular targeting — no zip/postcode, restricted interests, age floor — which is fine, because this plan is broad Advantage+ anyway.

**3 · No direct link to a purchase page.** Meta's crawler reads the destination. An ad pointing at a challenge checkout is the most reliable way to get banned in the first review cycle. Route every ad through a **bridge page** on `verodus.com`: plain-English explanation of the evaluation, the published objectives, the risk and simulated-trading disclosure above the fold, then a link on to checkout. The pixel fires on the bridge. Week 1 (free trial) is the easiest version of this — the trial *is* a compliant destination.

**4 · The landing page is the weakest link in this whole plan.** The ad copy is conservative; the homepage is not. Before any spend, fix:

| On `verodus.com` | Why Meta flags it |
|---|---|
| "Get Funded & Trade — **Up to $1M Capital, 90% Profit Split**" | Implied outcome + 90% presented as headline, not the on-demand add-on |
| The **reward calculator** projecting e.g. "$3,600" | An earnings projection tool — the clearest unrealistic-outcome trigger on the site |
| Payout certificates with **dollar amounts** | Unsubstantiated performance claims |
| "Get funded" framing | Reads as funding provision, not simulated evaluation |

Keep them for organic if you want. The **bridge page must not contain any of them.**

## Then the build

1. Install the Meta Pixel + Conversions API on `verodus.com`, including the bridge page.
2. Events, in this order of value: `Purchase` (value = fee paid) → `InitiateCheckout` → `CompleteRegistration` (free trial) → `ViewContent`.
3. Verify domain and business in Business Manager.
4. Business + Page: use **Verodus**. Turn on **Advantage+ placements** (Feed, Stories, Reels, Explore).
5. Select the **Financial products and services** Special Ad Category. Age 18+ minimum at ad-set level.
6. Bridge page must say **simulated**, fee ≠ trading capital, and carry the risk disclosure above the fold.
7. **No crypto in paid creative.** Crypto exchange/wallet promotion needs separate written permission. Our reward rails mention crypto — strip it from ads and keep "bank transfer or local methods." `payouts-feed.png` needs a crypto-free variant before it runs.
8. Scale spend gently: **no more than 20–30% budget increase every few days.** Aggressive scaling on a new financial account reads as an automated-abuse signal.

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

- **Cold:** Advantage+ broad. Age **18+** (Special Ad Category floor), skew 22–44. Geos: **only markets where Verodus holds the financial-services authorisation Meta requires** — see the policy gate above. The old 13-country list (US, UK, CA, AU, UAE, DE, NL, SG, ZA, NG, PH, IN, BR) assumed no verification and is not safe to run as-is; US/UK/DE/CA/AU are all credential-gated.
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
- Personal attributes: any *you* statement about the viewer's losses or money. **“You did everything right. You were up. Then the floor moved.”** (reel 20-A) is the riskiest hook in our set — it asserts the viewer's trading loss. Safer: *“A trailing floor ends green accounts.”* Same point, no personal claim.
- Hiding that trading is **simulated**
- Before/after income graphics
- **Fake urgency.** Deceptive countdowns and limited-time framing on a standing product are named prohibitions. Week 4's “ends tonight” and any countdown sticker only run if the price genuinely changes; otherwise use *“The rules aren't changing. Neither is the trial.”*
- **CFD framing.** CFDs are a prohibited product with no compliance path. Never describe Verodus as CFD trading — it is a simulated evaluation. Keep instrument talk generic.

Allowed: published rules, one-time fee, VERO35, free trial, “rewards are rule-based and paid on the published objectives,” payout rails (Rise / crypto).

**Payout speed is allowed** as an operations claim: “most rewards process in under 24 hours,” matching the homepage. Keep “most” and never present it as guaranteed or as an earnings claim. Do not imply a trader is paid within 24 hours of purchase — the first reward also requires a **$100 minimum and 3 trading days**, and the objectives page quotes a **48-hour** window for that first payout.
