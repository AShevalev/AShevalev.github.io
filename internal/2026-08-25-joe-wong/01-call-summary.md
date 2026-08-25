# Call summary — Verodus / World Trader Hub partnership

**Date:** 25 August 2026  
**Duration:** ~56 minutes  
**Attendees:** Joe M. Wong; Alexander; Kim Chen (backend / automations; Director and Manager on the Verodus entities)

This note restates what was actually said on the call. It is not a term sheet and does not create commitments.

## Purpose

Align on Path 1 (B2B): how Joe’s Hong Kong wealth-management ecosystem would use Verodus, how the two sides would integrate, the trial-to-launch sequence, and what each side needs before any merger or majority buy-in.

## Joe’s proposed ecosystem

Joe described a Hong Kong “World Trader Hub” built off a network of roughly 30,000 private equity, family office, and VC firms, with Hong Kong government support after about 9–12 months of work.

**Tax point he described:** approved fund managers and traders working in Hong Kong can seek a tax exemption on the profit-sharing / bonus part of compensation, not on basic salary. He presented that as a recruiting edge.

**Positioning:** do not lead with “prop firm.” Prop trading sits behind the scenes. The public image is education, mentorship, and funding inside a wealth-management ecosystem. Joe and Alexander both treated the prop-firm brand as weak.

**Joe’s three entities**

| Entity | Role on the call |
| --- | --- |
| TradeMap | Education, mentorship, and small-lump funding (example: prop-style credits / challenge funds). Commercial counterparty for the TAMS technical agreement. |
| MoneyMap | Wealth / fund management. Real-money trading after a person is approved. Backs professional / institutional flow. |
| World Trader Hub (Hong Kong) | Public-facing, described as a non-profit / organisation used for credibility, network, and marketing. |

**Two product phases**

1. Retail: “kindergarten to university.” TAMS + Verodus backend. Bookmap / order-flow is not required on day one; Joe said fewer than 30% of current traders know order-flow dynamics.
2. Professional / institutional: “MBA to PhD,” with Bookmap order-flow functions, then funding and institutional services via MoneyMap.

B2B partners (education academies, VCs, PE) are the distribution. Joe said they are competitive with one another and lack institutional-grade product, so TradeMap + funding + order-flow education is the wedge.

## Integration and go-to-market

| Item | What was said |
| --- | --- |
| Technical stack | Line up with **TAMS**. Verodus owns the backend. |
| Commercial contract | Agreement sits with **TradeMap**, not TAMS as a legal entity. |
| Kim’s integration estimate | Need to inspect the TAMS API first. Might be 2–3 weeks if API environments match. |
| Joe’s planning buffer | About **1 to 1.5 months** for integration. Understanding the environment matters more than coding hours. He will connect his tech team to Kim. |
| Trial | After integration, 1–2 interested B2B partners on a **free** trial of **30 days, not more than 45**. Free trial is deliberate: paid users would complain if anything breaks. |
| Combined calendar Joe stated | ~30–45 days integration + ~30–45 days trial → official launch about **three months** out. |
| After launch | Joe expects inbound demand because partners compete and currently only have retail-level education. |
| Branding during trial | Not fully settled. Alexander asked whether partners would see TAMS selling TAMS, with Verodus as the engine. Joe said they will talk to partners after integration; economics should follow an agreed future ownership / profit-share percentage even before a merger. Open book. Do not price aggressively at the start; volume first. Pricing can later sit inside partners’ existing education programmes. |
| Contracting entity | Joe will not pick Verodus Dubai vs Holding vs Capital until he has the org chart and legal has reviewed it. |

Prop models, account sizes, and challenge prices are **not locked**. Joe wants to review existing drawdown rules, limits, and tiers. He expects Hong Kong tickets may start a bit higher because average income is higher.

## What Alexander described about Verodus today

**Operating history**

- Venture started at the beginning of 2026.
- Operational about **4 months** (not 4 years).
- Pre-launch push around May; heavy marketing paused since end of June; plan to restart this week or next, once content is ready.

**Team and operations**

- Kim is the only IT person: backend and automations.
- Manual work today: payout verification after a trader is funded and profitable; customer support (chat / tickets).
- Marketing is in-house: one content creator; one intern nearly onboard for support plus marketing/script work.
- Alexander’s view: 50–100 extra users should not change monitoring workload if the system stays automated.

**Challenge families (current Verodus product)**

| Family | Structure (as described) |
| --- | --- |
| Instant | 5 tiers: $5k / $10k / $25k / $50k / $100k. No minimum trading days. **20% best-day rule.** Trailing drawdown. Hard to pass; attracts gamblers. |
| One-step | 6 tiers: same as instant plus **$200k**. No minimum trading days on paper; **50% best-day rule**, which in practice forces about **3** trading days. Trailing drawdown. Largest revenue source; amateur / retail. |
| Two-step Pro | 6 tiers to $200k. **5% daily / 10% max** drawdown. Phase 2 profit target **5%** (half of phase 1, as described). Professionals tend to sit here. No trailing drawdown (as described). Better payouts. |
| Two-step Light | **4% daily / 8% total** drawdown. Phase 2 profit target **4%**. |

News-trading restriction was removed because it was not needed for the current book.

**Performance stats given on the call**

- About **3,000** traders.
- **Less than 2%** ongoing winners.
- About **60 payouts** over 4 months (~15/month).
- A few funded accounts lasted ~70 days; only **2–3** accounts have reached a third payout.
- Most flow is **gold / metals**; some crypto.
- Alexander’s characterisation (Joe agreed with the implication): roughly **98.5%** of people lose, so extra risk controls are not the current bottleneck.

**Build history**

- Started on **Exera** white label; left because integration, custom rules, and risk controls were not good enough.
- Current stack designed in-house: mostly **Java**, some Python, server / database / API.
- Market data from **Altix**.
- TradingView logo on the dashboard is layout only; **no TradingView agreement**.

**Money and cost**

- Operating costs about **CAD $20,000/month** (wages and ops, described as generous). **Excludes** ad spend / marketing reinvestment.
- Overall **profitable**; still covering the original cash in.
- Capital injected: ~$80k (Feb–Apr) + ~$20k (May) ≈ **$100k**. Plan is to rebuild company cash and eventually return capital to investors.

**Entity / money flow as Alexander described it**

- **Verodus L.L.C.-FZ (Dubai)** owns the domain, collects data, runs CRM / dashboard.
- **Verodus Capital (Canada)** has the licence to use the domain, must send clients / do marketing for Dubai, and currently takes **~95% of payments**. **5%** can go to Dubai as a discretionary royalty.
- Canada is the **profit centre today**; they are gradually aligning more to Dubai.
- Payment processor exists in the UAE but they currently use the **Canadian** processor.
- Moving money between entities is “not that difficult” because it is internal agreements.
- **White-label / system company:** a **British Columbia** company provides the white label to Verodus Dubai. Alexander said that company is held by **one of the investors**. Kim is Director / CEO of the operating setup “as it stands.”
- Joe flagged system ownership, hosting (e.g. AWS), and database location as things that must be right the first time.

## Merger / listing discussion (indicative only)

Joe’s sequence:

1. Integrate and run the trial.
2. Official go-to-market; **6–12 months** to build volume.
3. Then talk merger / majority buyout.

Joe’s default majority language: **minimum 51%, normally 60%**, Verodus holders keep **40%**. What he would “inject” is network, expert team, IP, mentorship/education, and World Trader Hub — not only cash.

He asked Alexander to come back with a number. Hypothetical he used: if the company is worth **$1 million**, they might inject **$600k for 60%**, and **lock that maths into the day-one agreement** so nobody re-trades valuation after the business has matured. He said a number that is “too small” is also meaningless; the point is to grow the pie.

Alexander: must discuss with other investors. He doubted they would agree immediately to the $1m / 60% example; more plausible **after volume**, around phase two / **4–5 months** out. He will come back with what investors think.

**Joe’s listing sketch (his numbers, not a plan Verodus adopted)**

- CSE listing: at least **~$5 million** annual revenue.
- Within **24–36 months**: ~**$30 million** revenue, or market cap around **$15 million**, then uplist to NASDAQ.
- His NASDAQ multiple colour: **40–50× revenue**. Example: $10 million revenue × 50 = $500 million cap, which he called small for NASDAQ, hence the $30 million revenue ambition.
- He said listing capability already sits on his team (named a CFO with Bank of America / public-company chair background; searchable as “wins online” on the call — spelling not confirmed). Too early to run that workstream now.

**Data:** trial data and data going forward would be **combined** and sit under the company if they grow together. Joe said today’s dataset is too small to be valuable until it is thousands / tens of thousands of accounts.

## Next steps stated on the call

**Alexander / Verodus**

- Send organisation chart: entities, who holds data, who runs sales/marketing, how companies are held (personal vs corporate), banking/financial flow, executive team, employees vs partners vs freelance.
- Send intercompany agreements so Joe can see what each company does and how amounts are offset.
- Come back with a valuation / what Verodus is willing to sell, after internal investor discussion.
- Confirm which company owns the system and where it is hosted.
- Have the TAMS API / environment looked at (Joe’s tech + Kim).
- Target: materials **tonight or tomorrow morning**; try to agree something **early next week**.

**Joe**

- Connect his tech team to Kim on API environment (Java / Python).
- Send his call summary to relevant parties.
- Review valuation internally after Verodus sends a number.
- Decide contracting entity after legal reads the org chart.

---

*Gemini’s auto-summary had several errors (wrong legal name Veritis, “Tub Zits” for Kim, flattened listing numbers, “3,000 active traders,” and treated the $1m / 60% figure as a decided term). Use this note instead of the Gemini recap if circulating internally.*
