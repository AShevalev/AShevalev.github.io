# Compliance checklist

Tied to the Meta risks in [01-CAMPAIGN.md](01-CAMPAIGN.md). If an answer is wrong, the ad doesn't ship.

## Pre-launch — once, before any spend

- [ ] Business verified, domain verified in Business Manager
- [ ] **Financial-services authorisation held for every country in targeting** — this is the gate that stops campaigns dead
- [ ] **Financial products and services** Special Ad Category selected
- [ ] Age floor 18+ at ad-set level
- [ ] **Bridge page live**, with the risk and simulated-trading disclosure above the fold
- [ ] Bridge page carries **none** of: reward calculator, "Up to $1M Capital / 90% Profit Split" headline, dollar-value payout certificates, "get funded" framing
- [ ] Pixel + Conversions API firing on the bridge page
- [ ] Site language reconciled with the disclaimer — "simulated capital", not "capital"; "up to 90%, on demand", not "90% profit split"
- [ ] Full disclosure signed off by counsel

## Per ad — every single one

**Destination and structure**

- [ ] Destination is the **bridge page**, not a checkout or affiliate redirect
- [ ] CTA button matches the destination — **Learn More** on all cold traffic
- [ ] UTM set, ad name matches `utm_content`

**Claims**

- [ ] No fee, account size, or discount % **spoken in the video** (statics and ad text may carry them)
- [ ] Any **static max loss** claim carries a 2-Step label, on screen and in VO
- [ ] Instant creative contains **no** fee-refund and **no** static-drawdown claim anywhere
- [ ] 90% appears as the **on-demand add-on**, never as the standard split
- [ ] Weekly cycle, if mentioned, is stated as **70% and an add-on**
- [ ] Payout speed reads "**most** rewards process in under 24 hours" — never "you get paid in 24 hours"
- [ ] No earnings figure, payout screenshot, projection, or income promise
- [ ] Instant $25k and above appears nowhere

**Language traps**

- [ ] No *you* statement about the viewer's losses or money — use third person or a question
- [ ] No **crypto** rail in copy or visible in the creative
- [ ] The words "CFD trading" appear nowhere — this is a simulated evaluation
- [ ] No "we're new", "launching", "day one" as launch phrasing
- [ ] No countdown, "ends tonight", or limited-time framing **unless the price actually changes**

**Disclosure**

- [ ] Burn-in on the final frame: *Demo accounts with fictitious funds. All trading is in a simulated environment only. 18+.*
- [ ] Burn-in is **28px minimum** at 1080×1920, held **3+ seconds**, clear of the bottom 250px, not gold on the blue gradient
- [ ] Caption closes with the disclosure block if it mentions price, rewards, or buying

## Weekly

- [ ] Budget increases held to **20–30% every few days**
- [ ] Comments moderated — delete other people's income claims from under our ads; they become our claims once they sit there
- [ ] Every rejection logged with the ad name before relaunching a variant
- [ ] Spot-check that the landing page hasn't drifted back to earnings language

---

## The four things most likely to get the account banned

Ranked by how often they actually cause it in this category:

1. **Linking straight to a purchase page.** Meta crawls the destination. This is a first-review-cycle ban, not a rejection.
2. **Targeting a market without the authorisation.** Rejections stack into account-level restriction.
3. **An earnings claim on the landing page.** Your ad can be clean and still fail on the destination — the reward calculator is the specific exposure here.
4. **A *you* statement about someone's money.** Personal attributes and financial-distress targeting are separate prohibitions that both catch this.

Nothing in this pack's copy trips these. The funnel and the site are where the risk lives.
