# Verodus.com review — 17 Aug 2026 21:28 UTC

Full English rescan of `www.verodus.com` after the adjustments. **The policy is live.** No remaining `$200` / `2%` on-demand floor, no news-window rule, no 8(h) payout test, no News Trading Addon.

**Policy check**

| Rule | Status |
|---|---|
| News allowed every phase | **Done** |
| No ±2-minute window / no tiered news breach / no “window no longer applies” recopy | **Done** |
| News Trading Addon unnamed / retired | **Done** |
| TOS 8(h) 50% / 2-minute profit mix deleted | **Done** |
| FAQ holding time = No | **Done** |
| On-demand **$100** all plans | **Done** |
| On-demand still requires that evaluation’s **min trading days** | **Done** on plan pages + Qualified Trader FAQ |
| Weekly named in the $100 threshold | **Done** (`content.p9`) |
| Bracketing + gap still banned | **Done** |
| HFT / tick-scalp / latency-arb / rollover kept | **Done** |

---

## What is live (spot checks)

**Terms** — Section 8 ends at (g). No Minimum Holding Time heading. News is `(ii). News Trading`, allowed all phases, no window. Bracketing `li17` / gap `li18` kept. `p59` does not call news an exploit.

**Restricted trading** — Addon bullet gone. `p17`: allowed every phase, no news time window, no news-trading breach. `p18` (“previous funded-only ±2-minute…”) **gone**. Bracketing/gap kept. HFT/tick-scalp kept.

**Plan pages** (1-step, 2-step lite/pro, instant) — Addon bullets empty/removed. News: allowed every phase. On-demand: `$100` **and** min trading days; no “at any time.” Instant no longer says “Full news trading (subject to restrictions).”

**FAQ**

- Plans hub: “News trading is included in every phase. There is no minimum holding time.”
- General: holding time **No**; points at HFT / tick-scalp.
- Qualified Trader `p9`: “A fixed $100 profit threshold is required for **weekly, bi-weekly, and on-demand** rewards. On-demand still requires the minimum number of trading days for that evaluation.” On-demand list: `$100` + min days.
- News trading: allowed; Instant in the table; column renamed **Window** (None); no addon; no ±2.

**Objectives / rewards** — On Demand min `$100`. Request: “Anytime after min trading days.” First payout: `$100` after 3 days (eval) / 5 days (Instant). Performance-reward: `$100` all plans.

**common.json** `pricing.addonFootnote` emptied. Checkout has no news-addon SKU.

`keltner-bands.html` “±2 ATR” is indicator math. Ignore.

---

## Optional polish only (not policy blockers)

1. **“Allowed in Evaluation”** on 1-step / 2-step lite / 2-step pro (`li36` / `li32`) still groups “full news trading, EAs…” under an evaluation-only heading. The dedicated News Trading line already says every phase. Optional: rename to “Allowed” so it does not sound like news is eval-only.
2. **`performance-reward.html` `p12`** is “Minimum $100 since last reward (all plans).” It does not repeat the min-days clause. Plan pages and Qualified Trader FAQ already do. Optional: add “and min trading days for that evaluation.”
3. **Qualified Trader FAQ** still says first payout after **4** trading days; plan pages say **3**. Pre-existing mismatch, not part of this news/8(h)/$100 pass. Align if you want one number.
4. Empty locale keys (`restricted-trading` `p9`/`p18`, plan-page addon `li42`/`li38`/`li43`, TOS `h38`/`p51`–`p53`) are blank. Harmless if the HTML nodes are gone. Can delete the keys in a cleanup.

No further correction required for the news / 8(h) / on-demand-$100 policy.
