# Ads — what to build in Ads Manager

Paid only. Scripts and captions are in [02-SCRIPTS.md](02-SCRIPTS.md); organic in [04-ORGANIC.md](04-ORGANIC.md).

Destination is the **bridge page** on every ad — never a checkout link. Prices are allowed in ad text (the no-price rule applies to video VO only). Code **VERO35**, never stacked.

Legal line closing every ad's primary text:

> Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

URL: `https://www.verodus.com/<bridge>?utm_source=meta&utm_medium=paid&utm_campaign=founders&utm_content={{ad.name}}` · Display URL: `verodus.com`

## CTA buttons — match the destination

| Campaign | CTA | Destination |
|---|---|---|
| Week 1 — trial | **Sign Up** | Bridge → free trial |
| Week 2 — rules | **Learn More** | Bridge → objectives page |
| Week 3 — product | **Learn More** | Bridge → model card |
| Week 4 — offer, warm | **Learn More** | Bridge → checkout |

**Learn More whenever the destination is the bridge — cold and warm, including week 4.** Shop Now against a bridge page is a mismatch Meta reads as misleading: the button promises a purchase, the page is still an explainer. Never **Get Offer** — it implies a coupon entitlement against a standing discount. Do not test Shop Now until the destination is a real checkout URL and the account has survived review.

---

## Run order

Three ads per week, one hook each. Don't add a new ad until something has 2,000 impressions — at $760 total, more cells than this starves every test before it reaches significance.

| Week | Ads | CTA |
|---|---|---|
| 1 | `W1_WHY`, `W1_TRIAL`, `W1_HERO` | Sign Up |
| 2 | `W2_FLOOR`, `W2_RULES`, `W2_TWOSTEP` | Learn More |
| 3 | `W3_INSTANT`, `W3_ONESTEP`, `W3_WHICH` | Learn More |
| 4 | `W4_OFFER`, `W4_ONESTEP`, `W4_WHICH` — or `W4_LASTCALL` only if pricing ends | Learn More |

| Ad name | Video / creative | Primary text |
|---|---|---|
| `W1_WHY` | Script 2 | **P-WHY** |
| `W1_TRIAL` | Script 7 | **P-TRIAL** |
| `W1_HERO` | Script 1 | **P-HERO** |
| `W2_FLOOR` | Script 4 | **P-FLOOR** |
| `W2_RULES` | Script 5 | **P-RULES** |
| `W2_TWOSTEP` | Script 13 | **P-TWOSTEP** |
| `W3_INSTANT` | Script 11 | **P-INSTANT** |
| `W3_ONESTEP` | Script 12 | **P-ONESTEP** |
| `W3_WHICH` | Script D | **P-WHICH** |
| `W4_OFFER` | Script 8 + `w4-offer-card.png` | **P-OFFER** |
| `W4_ONESTEP` | Script 12 + `w4-pricing.png` | **P-ONESTEP** |
| `W4_WHICH` | Script D + `w2-plans.png` | **P-WHICH** |
| `W4_LASTCALL` | Script 10 + `w4-lastchance.png` | **P-LASTCALL** |

`W3_PROMO` / script C is cut from the run order — it's a second 1-Step ad competing with `W3_ONESTEP`. `P-PROMO` stays below as a swap if `P-ONESTEP` gets rejected.

Statics can run as standalone ads in the same ad sets — see [creatives/README.md](creatives/README.md) for which are paid-eligible.

---

## Primary text

First **125 characters** show before "See more," so the point goes first. Headlines **≤40**, descriptions **≤30**.

### P-WHY — best cold performer
Some firms sell one rulebook and enforce another. Ours are published before you pay.

No time limit. The rules you start with are the rules you finish with. We don't change them after you've paid.

Free trial's on the site — read every objective before you spend anything.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Published before you pay · **Description:** Free trial

### P-TRIAL
You shouldn't have to pay to find out how a firm works.

The Verodus trial is the real thing — the same platforms, the same rules, the same dashboard. No card, nothing to cancel, and you can take another one whenever you want.

Trade it for an afternoon, then pick an evaluation: 1-Step, 2-Step Lite or 2-Step Pro.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** The trial is the real thing · **Description:** No card

### P-HERO
Most prop firms make traders feel trapped. Support is a ticket number, and nobody puts their name next to the rules.

We're the founders. We're in the Discord every day and we answer the hard questions in public — including the ones about our own pricing.

Start the trial, then ask us whatever you want.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Ask the founders directly · **Description:** Start free

Deliberately makes no rules claim — that's `P-WHY`'s job. Running both with the same argument puts two of our own ads in the same auction.

### P-FLOOR
Most challenges aren't lost on the profit target. They're lost on the loss limit.

A trailing limit moves up every time the account hits a new high, so one normal losing trade can close an account that's still in profit. On Verodus 2-Step, the max loss is static — set from your starting balance on day one, and it never moves.

Instant is a different product; that one trails, and the card says so.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** 2-Step: static max loss · **Description:** Read the objectives

### P-RULES
Don't trust a firm's ad. Trust its objectives page.

No time limit. Static max drawdown on 2-Step. Fee back on your first reward, evaluations only. All of it published before you pay.

Read it yourself.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Read it yourself · **Description:** Published objectives

### P-TWOSTEP
Been stopped out while you were still in profit? That's a trailing loss limit.

Verodus 2-Step uses a static max loss — set on day one, and it doesn't move up when the account is winning. Two published phases, no time limit, fee back on your first reward.

1-Step $5,000 is $36 with VERO35. Lite and Pro on the objectives page.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** A fixed limit, not a moving one · **Description:** Use code VERO35

### P-INSTANT
Instant skips the evaluation. No profit target — you trade from day one.

The honest part: the max loss trails, and Instant doesn't refund the fee. The evaluations do. That's the trade.

Instant $5,000 is $72 with VERO35. Full card on the objectives page.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Instant $5k — $72 · **Description:** No profit target

### P-ONESTEP
One phase. One set of published numbers — target, daily loss, max loss.

No time limit, so you pass on your schedule, not a thirty-day clock. And your fee comes back on your first reward.

1-Step $5,000 is $36 with VERO35.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** 1-Step $5k — $36 · **Description:** Fee back on first reward

### P-PROMO
A one-step with every number published before you pay: target, daily loss, max loss.

No time limit — you pass on your schedule. Fee back on your first reward. News and weekend rules are on the objectives page as they actually apply.

Trial first.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Every number, published · **Description:** Trial first

### P-OFFER — warm only
One intro code while we run this founders series. One — we don't stack a second discount and call it a sale.

Instant $5,000 is $72. 1-Step $5,000 is $36 with the fee back on your first reward. The base reward cycle is every two weeks at 80%; weekly (70%) and on-demand (90%) are paid add-ons.

Start with the free trial. If the rules fit, the code's there.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** One code. No stacking. · **Description:** Use code VERO35

### P-WHICH — warm only, no deadline needed
Four ways in, and every number is published.

Instant has no profit target — you trade from day one. The max loss trails and the fee isn't refunded. The evaluations are the other three: one phase on the 1-Step, two on Lite and Pro, static max loss on 2-Step, and your fee back with your first reward.

1-Step $5,000 is $36 with VERO35. No time limit on any of them.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Which one fits how you trade? · **Description:** Four cards, published

Use this instead of P-LASTCALL whenever pricing isn't actually changing. It asks for an evaluation, not another free trial — pair it with warm audiences only.

### P-LASTCALL — warm only, conditional
Intro pricing ends this week. Code VERO35: Instant $5,000 at $72, 1-Step $5,000 at $36.

Trial's still free either way.

Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.

**Headline:** Intro pricing ends · **Description:** Use code VERO35

Run this **only if the price actually changes.** Otherwise swap in P-OFFER — fake urgency on a standing product is a named Meta prohibition.

---

## Comment reply — pin on every ad

> Verodus provides simulated trading and performance evaluation — we're not a broker and don't accept deposits. All accounts are demo accounts with fictitious funds. You pay a one-time fee, trade against published objectives, and become eligible to request a reward. Instant $5k is $72 with VERO35 (no fee refund). 1-Step $5k is $36, fee refunded on your first reward. Free trial's on the site. 18+. Full rules: verodus.com/trading-objectives.html

Never argue pass rates in comments — link the objectives page. Delete other people's income claims from under our ads; they become our claims once they sit there.
