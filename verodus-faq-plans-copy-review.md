# Verodus FAQ plan pages — copy review

Reviewed 18 August 2026 against the live pages:

- [Plan FAQs](https://www.verodus.com/faq-plans.html)
- [Instant Funding](https://www.verodus.com/instant.html)
- [1-Step](https://www.verodus.com/1-step.html)
- [2-Step Lite](https://www.verodus.com/2-step-lite.html)
- [2-Step Pro](https://www.verodus.com/2-step-pro.html)

Goal: remove redundancy, make the four plans comparable, and fix wording that is unclear or inconsistent. Replacement copy below is ready to paste. Shared rules that are identical on every plan (news trading allowed, no minimum holding time, weekend/Friday close, restricted practices) should be said once, not restated in every blurb and every section.

---

## Rescan — 18 August 2026 (later pass)

Live pages were fetched again after the copy pass. **The requested Instant 20% Best Day qualifying-day floor is live**, and most of the FAQ/rules rewrites landed.

### Instant 20% Best Day (the follow-up request) — done

Closed profit must be at least **0.5% of that day’s start-of-day equity** now appears in:

| Location | Status |
| --- | --- |
| [Plan FAQs — Instant](https://www.verodus.com/faq-plans.html) | Live, including JSON-LD (no “View rules →” inside the answer) |
| `instant.html` Section 3 body + Rule/Calculation bullets + $100k / $500 example | Live |
| Instant payout eligibility | Live (“qualifying days only: closed profit ≥ 0.5%…”) |
| Instant Best Day modal | Live (replaced “more than 0.5% profit”) |
| [Evaluation FAQs](https://www.verodus.com/faq-evaluation.html) Instant bullets | Live |
| Homepage “What evaluation models…” answer | Live |
| 1-Step | Correctly **not** given this floor |

### Other review items — landed

- FAQ hub: one shared note (“News trading is allowed on all four plans… Weekend Holding add-on”). The four answers no longer repeat news/holding.
- Four FAQ answers use the same fact order; Lite/Pro now include **5 evaluation days**; Instant daily vs trailing drawdown is split; splits/sizes/cycles are consistent.
- Instant: duplicate min-days bullet gone; Section 4 retitled **Payouts and risk limits**; overview line is “Simulated capital from day one.”
- 1-Step: “unique to 1-Step” and “end-of-day equity” gone; intro now says hybrid locks at initial balance and “50% Best Day rule (Instant uses 20%).” Last updated **August 2026**.
- 2-Step Pro H1 is **2-Step Pro Evaluation**. Lite/Pro intros no longer say “balanced / scaling / highest earning.” Payout trading-day definition now matches evaluation (opened **and** closed). Phase 2 min days: “counted the same way as Phase 1.” Last updated August 2026.
- Duplicate 70/80/90 split lists and “may stack” are gone on the plan pages.
- Homepage Instant table no longer shows “5 Days” or “Up to 1:50” in the live HTML (1:30 is present).

### Still open (small leftovers)

- Instant overview still says “There are no profit targets to hit **before funding**” and “sustainable risk rules.”
- Instant still names Section 3 **Unique Instant Funding Rules**.
- Instant news trading is still said twice; Restricted Practices still says “Allowed in **every phase**” (Instant has no phases).
- Evaluation FAQ article dates are still **19 March 2026** even though Instant 0.5% copy inside them was updated.

The original section-by-section notes below are the first-pass review. Use the rescan table above for what is already live.

---

## 1. Cross-plan issues (fix these first)

### 1.1 Shared lines repeated on every FAQ card

Every Instant, 1-Step, Lite, and Pro answer currently ends with:

> News trading is included in every phase. There is no minimum holding time.

Problems:

- Instant has no phases, so “every phase” is wrong.
- The two sentences are not plan-specific. They bury the actual differences.
- “Included” sounds like an add-on. The rules pages say news trading is **allowed**.

**Fix:** Put one shared note at the top of `faq-plans.html`, and drop both sentences from the four answers.

Suggested page note:

> News trading is allowed on all four plans. There is no minimum holding time. Weekend holding still requires the Weekend Holding add-on.

### 1.2 The four FAQ answers do not follow the same shape

A trader comparing plans has to hunt for the same facts in different order, with different labels.

| Fact | Instant | 1-Step | 2-Step Lite | 2-Step Pro |
| --- | --- | --- | --- | --- |
| What the plan is | Yes | Yes (“clear risk limits”) | Missing (starts with numbers) | Yes |
| Evaluation min days | No min | No min | **Omitted** (5 per phase) | **Omitted** (5 per phase) |
| Payout min days | Implied (none) | Stated (none) | 3 days | 3 days |
| Best Day | Stated twice; **missing 0.5% qualifying-day floor** | Named, then explained | None (correct) | None (correct) |
| Default split | 80% only | 80% and 90% On-Demand | Omitted | Omitted |
| Payout cycles named | “selected cycle” | “selected cycle” | weekly / bi-weekly / on-demand | weekly / bi-weekly / on-demand |
| Account sizes | $5k–$100k, no $200k | Omitted | Omitted | Omitted |
| Marketing leftover | None | “clear risk limits” | “balanced… scaling potential” | None on FAQ; “highest earning potential” on rules page |

Use one template for all four answers:

1. What the plan is (one sentence).
2. Targets / phases.
3. Drawdown (type + %).
4. Best Day, if any.
5. Minimum trading days (evaluation and payout).
6. Payout eligibility.
7. Split.
8. Sizes.

### 1.3 “Unique to 1-Step” is no longer true

`1-step.html` still calls the 50% Best Day rule and the hybrid trailing drawdown “unique to 1-Step.” Instant now has a 20% Best Day rule and a trailing (never-locks) max drawdown. Keep “hybrid, locks at initial balance” as the 1-Step distinction. Do not say Best Day is unique.

### 1.4 “Funded” vs simulated capital

All four pages open with a simulation disclaimer, then immediately say “funded account,” “funded capital,” or “Start Trading Funded Capital Immediately.” Instant’s overview line is the worst clash.

Prefer **Qualified Performance account** (the term used in the agreement) or **funded simulated account**. Drop “funded capital.”

### 1.5 Dates and titles out of sync

| Page | H1 | Last updated |
| --- | --- | --- |
| FAQ hub | — | August 2026 (all four) |
| Instant | Instant Funding Plan | August 2026 |
| 1-Step | 1-Step Evaluation | **March 2026** |
| 2-Step Lite | 2-Step Lite Evaluation | August 2026 |
| 2-Step Pro | **2-Step Evaluation** (missing “Pro”) | **March 2026** |

Change the Pro H1 to **2-Step Pro Evaluation**. If 1-Step and Pro were edited in the August pass, update their dates; if not, the FAQ hub should not claim August 2026 for those two.

### 1.6 Homepage still contradicts the new plan FAQs

Not on the FAQ plan pages, but it will undo this work if left as-is. The Instant tab on [verodus.com](https://www.verodus.com/) still shows:

- Minimum trading days: **5 Days** (FAQ/rules: none)
- Leverage: **Up to 1:50** (plan pages: FX 1:30)
- A **$200,000** Instant size (FAQ: no $200k Instant)

`trading-objectives.html` is closer to the new rules (1:30, Instant sizes stop at $100k). The homepage table is the leftover.

---

## 2. FAQ hub — `faq-plans.html`

### Instant — current

> Instant access to a funded simulated account with no evaluation phases. 6% trailing max drawdown, 3% daily drawdown (both from equity high water mark; trail never locks), 20% Best Day of Positive Days' Profit, and no minimum trading days. Every Instant payout needs $100, Best Day ≤20% of Positive Days' Profit, and the selected cycle. Default split is 80%. Sizes $5,000–$100,000 — no $200,000 Instant account. News trading is included in every phase. There is no minimum holding time.

Issues:

- “Both from equity high water mark; trail never locks” glues two different rules together. Daily drawdown **resets** at 00:00 UTC. Only the **max** trail never locks.
- Best Day is stated twice.
- Split omits the 90% On-Demand add-on, which 1-Step includes and the Instant rules page also offers.
- JSON-LD answer is missing “no $200,000 Instant account” and appends “View Instant Funding Rules →” as if it were part of the answer.
- The 20% Best Day rule is missing the qualifying-day floor: a day counts toward Best Day / Positive Days’ Profit only when closed profit is at least **0.5% of that day’s start-of-day equity**. The Instant modal currently says only “more than 0.5% profit,” which is vaguer and easy to misread as 0.5% of starting balance.

**Proposed Instant answer**

> No evaluation. You start on a funded simulated account. 6% trailing max drawdown from equity high water mark (the trail never locks). 3% daily drawdown from that day’s equity high, as a fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC. Best Day must be ≤20% of Positive Days’ Profit to request a payout. A day only qualifies for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000; no $200,000 Instant account.

### 1-Step — current

> Pass a single evaluation phase with clear risk limits to qualify for a funded account. 10% profit target, 4% daily drawdown (equity at server reset), 6% hybrid max drawdown (trailing from account peak), and the 50% Best Day rule. 1-Step Qualified Performance payouts need $100, Best Day ≤50% of Positive Days' Profit, and the selected cycle. 1-Step has no minimum trading days. Default split is 80% (90% with the On-Demand add-on). News trading is included in every phase. There is no minimum holding time.

Issues:

- “Clear risk limits” is filler.
- “The 50% Best Day rule” does not say 50% of what, then the next sentence repeats it properly.
- Does not say the hybrid trail **locks at initial balance** — that is the difference from Instant.
- Intro says “end-of-day equity” on the rules page; the FAQ says “equity at server reset.” Use the rules-page meaning: measured from equity at 00:00 UTC, floating losses included. “End-of-day” sounds like closed trades only.

**Proposed 1-Step answer**

> One evaluation phase, then a Qualified Performance account. 10% profit target. 4% daily drawdown from equity at 00:00 UTC (floating losses included). 6% hybrid max drawdown: trails the account peak, then locks at the initial balance. Best Day must be ≤50% of Positive Days’ Profit to pass and to get paid. No minimum trading days in evaluation or Qualified Performance. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

### 2-Step Lite — current

> 8% profit for phase 1 and 5% profit target for phase 2. 4% daily drawdown and 8% static max drawdown on evaluation and funded. 2-Step Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). A balanced 2-step program with standard risk controls and scaling potential. News trading is included in every phase. There is no minimum holding time.

Issues:

- Drops the **5 minimum trading days per evaluation phase** — the main 2-Step vs 1-Step/Instant difference.
- “A balanced 2-step program with standard risk controls and scaling potential” is leftover marketing. The Lite rules page does not describe a scaling program. Delete it, or add real scaling rules.
- “8% profit for phase 1” vs Pro’s “Phase I 10% profit target” — same fact, two styles.
- JSON-LD Lite answer already omits the marketing sentence; visible copy and schema should match.

**Proposed 2-Step Lite answer**

> Two evaluation phases, then a Qualified Performance account. Phase I 8% profit target, Phase II 5%. 4% daily drawdown and 8% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

### 2-Step Pro — current

> Two-phase evaluation: Phase I 10% profit target, Phase II 5% profit target. 5% daily drawdown and 10% static max drawdown on evaluation and funded. 2-Step Qualified Performance payouts (first and later) need $100, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). News trading is included in every phase. There is no minimum holding time.

Same missing 5-day evaluation minimum and missing split/sizes as Lite. “First and later” is already covered by “every payout.”

**Proposed 2-Step Pro answer**

> Two evaluation phases, then a Qualified Performance account. Phase I 10% profit target, Phase II 5%. 5% daily drawdown and 10% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

After these four replacements, Lite vs Pro is a clean comparison: 8/5 vs 10/5, 4%/8% vs 5%/10%, same days, same payouts, same sizes.

---

## 3. Instant rules — `instant.html`

### Must-fix

**Duplicate min-days bullets in Section 2**

> **No Minimum Trading Days:** There is no minimum number of trading days required. You may trade at your own pace.  
> **Minimum Trading Days:** No minimum trading days.

Keep the first bullet. Delete the second.

**Section 4 heading “Qualified Performance Phase”**

Instant has no evaluation. Traders land in payout rules from day one. Rename to **Payouts and risk limits** (or “Instant payout rules”). Keep “Qualified Performance” only where the legal term is needed.

**Overview line vs disclaimer**

> Instant Activation • No Challenge Phases • Start Trading Funded Capital Immediately

Change to: **Instant activation • No challenge phases • Simulated capital from day one.**

**20% Best Day — add the 0.5% qualifying-day floor (Instant only)**

This is a binding Instant rule. Put it in the FAQ blurb, Section 3 body, the Rule bullet, payout eligibility, and the example modal. Do not leave it in the modal only.

Current modal (too vague):

> A profitable day is a day that closes with more than 0.5% profit.

Required wording:

> A day only qualifies as a valid Best Day (and counts toward Positive Days’ Profit) when that day’s **closed profit is at least 0.5% of that day’s start-of-day equity**. Days below this floor are ignored for the 20% Best Day calculation.

**Proposed Section 3 Best Day block**

> **20% Best Day Rule**  
> Your single best *qualifying* profit day cannot account for more than 20% of Positive Days’ Profit at the time you request a payout.
>
> **Qualifying day:** A day counts only when closed profit is at least 0.5% of that day’s start-of-day equity. Smaller green days do not count toward Best Day or Positive Days’ Profit.
>
> **Rule:** Best Day must be ≤20% of Positive Days’ Profit.
>
> **Not a breach:** Exceeding 20% does not terminate the account. Keep trading until Best Day is ≤20%.
>
> **Calculation:** Closed trades only, at 00:00 UTC. Losing days do not count. Days under the 0.5% floor do not count.
>
> Example ($100,000 start-of-day equity): the floor for that day is $500 closed profit. +$400 does not qualify. +$600 does. If the largest qualifying day is $10,000, Positive Days’ Profit must be at least $50,000 before you can request a payout.

**Proposed Section 4 eligibility line**

> You become eligible for a reward when net profit is at least $100, Best Day is ≤20% of Positive Days’ Profit (qualifying days only: closed profit ≥ 0.5% of that day’s start-of-day equity), and you have met the selected cycle. Instant has no minimum trading days. Exceeding 20% is not a breach. See Section 3.

Do not add this 0.5% floor to 1-Step unless product confirms it there too. 1-Step currently has no such sentence.

### Cut repeated explanations (say once)

The 6% trailing max, 3% daily, 20% Best Day, and “no min days” are each stated in the intro, the stat card, the bullet list, Section 2, Section 3, Section 4 eligibility, and Section 5 Drawdown Type.

Keep:

- Intro: one-sentence overview + pointer to the sections.
- Stat card: numbers only (drop the extra “Minimum Trading Days: None” under the card; the grid already has it).
- Section 3: the full rule + one numbered example.
- Section 4 eligibility: “See Section 3” for the 20% cap, and one short reminder of the 0.5% qualifying-day floor so payout copy is complete.

**Section 3 Best Day** currently repeats “Profitable days are factored in” and never states the 0.5% floor. Use the proposed block above. Drop the duplicate Rule sentence.

### Daily drawdown — write it once, with an example

Three nearby versions:

- “3% of your starting balance below the highest equity point reached during the current trading day”
- “fixed loss limit of 3% of your starting balance, measured from the highest equity point reached during that day”
- Section 5: “fixed dollar limit (3% of starting balance) measured from the highest equity reached during the current day”

They agree, but a reader should not have to assemble them. Replace all three with:

> Daily drawdown is a **fixed dollar** limit equal to 3% of starting balance. Each day it is measured from that day’s **highest equity**. It resets at 00:00 UTC. Floating losses count.  
> Example ($100,000): the daily limit is $3,000. If equity peaks at $102,000 that day, equity must not fall below $99,000 before the reset.

Add a matching max-drawdown example next to it:

> Example ($100,000): 6% = $6,000 trailing. Peak equity $110,000 → floor $104,000. The floor keeps trailing new highs and **does not lock** at $100,000 (that lock is 1-Step only).

### Smaller Instant cleanups

- “There are no profit targets to hit before funding” and “No profit target required to begin” — keep one.
- Instant activation is in the overview heading, the body, and Section 2. Keep Section 2.
- Fees are non-refundable in payouts and again in breach. Keep it in payouts; in breach, say “see Fees.”
- News trading is allowed in Section 4, Section 5 Allowed, and Section 6 (inside Restricted Practices). Keep Section 6’s distinction: news trading allowed, **news bracketing and gap trading banned**. Link the policy once.
- HTML comment still says “50% Best Day Rule Modal.” Change to 20%.
- Replace the modal’s “more than 0.5% profit” with **at least 0.5% of that day’s start-of-day equity**.

---

## 4. 1-Step rules — `1-step.html`

### Must-fix

**Intro daily drawdown**

> 4% daily drawdown based on end-of-day equity at server reset

Section 2/5 say it is measured from equity at 00:00 UTC, **floating losses included**. “End-of-day” reads as closed-trade only. Use:

> 4% daily drawdown from equity at 00:00 UTC (floating losses included)

**“Unique to 1-Step”**

Replace:

- “50% Best Day consistency rule unique to 1-Step” → “50% Best Day rule (Instant uses 20%)”
- “Hybrid max drawdown 6% — unique to 1-Step” → “6% hybrid max drawdown (trails, then locks at initial balance)”
- Section 2 “Unique to this plan; see Section 3” → “See Section 3. Instant also trails, but Instant never locks.”

**Best Day restated in payout eligibility**

Section 4 repeats “Exceeding 50% is not a breach — keep trading until Best Day is ≤50%.” Point back to Section 3.

### Cut repeated explanations

Hybrid drawdown is in the intro, Section 1 bullets, Section 2, Section 3 (with example — keep this), Section 4 Risk Limits, and Section 5 Drawdown Type. Keep Section 3 + the Section 2 one-liner with “see Section 3.” Delete the Section 5 restatement or make it a one-line pointer.

**Payout split listed twice**

“Payout Frequencies & Trader Profit Share” and “Performance Reward Split” say the same 70/80/90. Merge into one list:

- Bi-weekly (default): 80%
- Weekly (add-on): 70%
- On-Demand (add-on): 90%

**“Weekly 70% and On-Demand 90% may stack”**

Unclear. Either they can both be purchased, or they cannot. Write the actual rule in one sentence (for example: “Weekly and On-Demand are separate add-ons; they cannot both apply at once” **or** “If both are purchased, On-Demand 90% applies when you request on-demand”). Same sentence belongs on Instant, Lite, and Pro.

### Smaller 1-Step cleanups

- “strict risk limits” / “sustainable trading rules” — delete.
- Schema description still says “Performance Reward Phase.” Align to Qualified Performance.
- Last updated: March 2026. Update if this pass ships.

---

## 5. 2-Step Lite — `2-step-lite.html`

### Must-fix

**Trading-day definition disagrees with itself**

Evaluation (Phase 1 and 2):

> A trading day counts only when at least one trade is both **opened and closed** on that calendar day.

Qualified Performance payouts:

> A trading day is a calendar day with at least one **closed** trade.

Those are different rules. If overnight trades count for payouts but not for evaluation, say so. If they do not, use the opened-and-closed sentence in both places.

**Phase 1 and Phase 2 copy-paste**

The 5-day definition is pasted in full under both phases. In Phase 2, write: **Minimum trading days: 5, counted the same way as Phase 1.**

**Intro fluff**

> A balanced 2-Step option with standard risk controls.

Delete. The numbers already show how Lite differs from Pro (8%/5% and 8%/4% vs 10%/5% and 10%/5%).

**“Scaling potential”** (FAQ hub only)

Not described on the Lite rules page. Remove from the FAQ, or add a real scaling section here.

### Same payout-block issues as 1-Step

Merge the two split lists. Spell out whether 70% and 90% stack. News trading: once, with bracketing still banned.

---

## 6. 2-Step Pro — `2-step-pro.html`

Almost a clone of Lite, so the same edits apply, plus:

**H1 is wrong**

> 2-Step Evaluation

Change to **2-Step Pro Evaluation** so it matches the breadcrumb, title tag, and Lite’s “2-Step Lite Evaluation.”

**Intro fluff**

> Our most popular 2-step program. … standard risk controls and the highest earning potential.

“Highest earning potential” is unexplained (same 80/90 split as Lite; Pro only has a larger drawdown and a higher Phase I target). Prefer:

> Two-phase evaluation. Phase I 10%, Phase II 5%. 5% daily drawdown and 10% static max drawdown. These rules are binding and form part of the Challenge Agreement.

**Last updated: March 2026** while Lite is August 2026, with the same payout/news copy. Align the date when this ships.

**Schema** still says “the most popular 2-Step program with the highest earning potential.” Match the new intro.

---

## 7. Restricted practices (all four plan pages)

Section 6 is duplicated in full on Instant, 1-Step, Lite, and Pro. That is fine if these pages are the binding rules. Two wording problems inside it:

1. **News Trading** sits under “Unrealistic Market Behavior” but the text is “Allowed in every phase.” Move the allow-rule to General Trading Rules. Leave only the ban (bracketing / gap trading) in Restricted Practices.
2. Instant has no “evaluation process” to be disqualified from. Instant Section 7 still needs “termination of the account,” not “disqualification from the evaluation process.” Instant already uses slightly different breach bullets; keep that split.

---

## 8. Suggested FAQ hub page (full)

Use this as the body of `faq-plans.html` after the H1. JSON-LD `acceptedAnswer` text should match these answers **without** the “View … Rules →” links.

**Shared note**

> News trading is allowed on all four plans. There is no minimum holding time. Weekend holding still requires the Weekend Holding add-on.

**Instant**

> No evaluation. You start on a funded simulated account. 6% trailing max drawdown from equity high water mark (the trail never locks). 3% daily drawdown from that day’s equity high, as a fixed dollar amount equal to 3% of starting balance; resets at 00:00 UTC. Best Day must be ≤20% of Positive Days’ Profit to request a payout. A day only qualifies for Best Day / Positive Days’ Profit when closed profit is at least 0.5% of that day’s start-of-day equity. No minimum trading days. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$100,000; no $200,000 Instant account.

**1-Step**

> One evaluation phase, then a Qualified Performance account. 10% profit target. 4% daily drawdown from equity at 00:00 UTC (floating losses included). 6% hybrid max drawdown: trails the account peak, then locks at the initial balance. Best Day must be ≤50% of Positive Days’ Profit to pass and to get paid. No minimum trading days in evaluation or Qualified Performance. Every payout needs $100 profit, the Best Day rule, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

**2-Step Lite**

> Two evaluation phases, then a Qualified Performance account. Phase I 8% profit target, Phase II 5%. 4% daily drawdown and 8% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

**2-Step Pro**

> Two evaluation phases, then a Qualified Performance account. Phase I 10% profit target, Phase II 5%. 5% daily drawdown and 10% static max drawdown on evaluation and Qualified Performance. 5 minimum trading days per evaluation phase (open and close on the same calendar day). Every payout needs $100 profit, 3 trading days, and the selected cycle (weekly, bi-weekly, or on-demand). Default split 80% (90% with On-Demand). Sizes $5,000–$200,000.

---

## 9. Related pages to fix in the same pass

These are not the FAQ plan pages, but they still publish the old Instant story:

| Page | What to align |
| --- | --- |
| [Homepage Instant tab](https://www.verodus.com/) | Min days none; FX 1:30 not “up to 1:50”; hide $200k for Instant |
| [Evaluation FAQs](https://www.verodus.com/faq-evaluation.html) | Already closer; still dated 19 March 2026; Instant/1-Step Best Day answers overlap the new plan FAQs — keep Evaluation FAQs for *how a day is counted*, and let plan FAQs own the numbers. Add the Instant 0.5% qualifying-day floor wherever Instant Best Day is mentioned. |
| [Trading objectives](https://www.verodus.com/trading-objectives.html) | Mostly aligned; confirm Instant $200k is not selectable |
| Terms of Service Instant/1-Step/Lite/Pro links | Fine; Pro page title should match “2-Step Pro Evaluation” |

---

## 10. Checklist

Rescan 18 August 2026: items marked done are live on verodus.com.

- [x] Shared news / holding note once on the FAQ hub; removed from the four answers
- [x] Four FAQ answers use the same fact order
- [x] 2-Step Lite and Pro FAQ answers include 5 evaluation days
- [x] Instant FAQ: daily vs trailing drawdown not glued into one clause
- [x] Instant Section 2: duplicate min-days bullet removed
- [x] Instant Section 4 retitled so it does not look like an evaluation phase
- [x] 1-Step: “unique” and “end-of-day” corrected
- [x] 2-Step Pro H1 includes “Pro”
- [x] Lite/Pro: one trading-day definition, used in evaluation and payouts
- [x] Split lists merged; stacking 70%/90% explained or removed
- [x] Instant 20% Best Day: qualifying day = closed profit ≥ 0.5% of that day’s start-of-day equity, in FAQ, Section 3, eligibility, and modal (not “more than 0.5% profit”)
- [x] Do not add the Instant 0.5% floor to 1-Step unless product confirms it there
- [x] JSON-LD matches visible FAQ text (no “View rules →” inside answers)
- [x] Homepage Instant table matches the FAQ (5-day / 1:50 Instant leftovers gone from live HTML)
- [ ] Instant leftovers: “before funding,” “sustainable risk rules,” Section 3 still titled “Unique…,” news trading still “every phase”
- [ ] Evaluation FAQ “Last updated” dates still 19 March 2026 after Instant 0.5% edits
