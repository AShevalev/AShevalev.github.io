# Landing page meta + fees

Paste `head-meta.html` into the Verodus-4-centered `<head>` (replace the current title / description / OG / Twitter block).

Do **not** keep “from $18” — that was the old Lite $5k VERO35. Floor is **Lite $39**. Instant starts at **$49**. 1-Step starts at **$45**. Pro starts at **$45**.

## SERP copy (locked)

| Field | Text | Chars |
|---|---|---:|
| Title | Verodus — Instant from $49. Funded on Day One. | 47 |
| Description | Funded on day one from $49. Pass a 1-Step from $45 or Lite from $39. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit. | 140 |
| OG title | Verodus — Instant from $49. Funded on Day One. | 47 |

Default split is **80%**. 90% is a paid add-on — do not lead the meta with 90% or $1M.

## Rec sale / list (VERO35)

News-included reprice 17 Aug 2026. Instant and 1-Step doors stay. Lite/Pro $5k–$10k follow the 2-step street door (Hola / TFT / Ment). Leftover stays on $25k and up.

| Plan | $5k | $10k | $25k | $50k | $100k | $200k |
|---|---|---|---|---|---|---|
| Instant | $49 / $75 | $69 / $106 | $149 / $229 | $239 / $368 | $439 / $675 | — |
| 1-Step | $45 / $69 | $69 / $106 | $129 / $198 | $219 / $337 | $379 / $583 | $699 / $1,075 |
| Lite | $39 / $60 | $55 / $85 | $99 / $152 | $149 / $229 | $275 / $423 | $549 / $845 |
| Pro | $45 / $69 | $59 / $91 | $109 / $168 | $169 / $260 | $309 / $475 | $619 / $952 |

JS: `plan-fees.js` — `[sale, list]`. Instant $200k is omitted on purpose.

## Checkout add-ons (drop-in)

Complete working page: [`checkout.html`](checkout.html). Add-on tooltip copy by plan: [`checkout-addon-tooltips.txt`](checkout-addon-tooltips.txt). Diff vs live verodus.com/checkout: [`checkout-vs-live.txt`](checkout-vs-live.txt). Chrome (nav, footer, CSS, icons, payment marks, mobile breakpoints) is loaded from [verodus.com/checkout.html](https://www.verodus.com/checkout.html). Quantity sits in the order summary like Blue Guardian (`1st Account` … `4th Account`), not as a left-column section. US-citizen term is removed. Rebuild with `python3 landing/stitch_checkout.py`.

Complete trading-objectives page: [`trading-objectives.html`](trading-objectives.html). Diff vs live verodus.com/trading-objectives: [`trading-objectives-vs-live.txt`](trading-objectives-vs-live.txt). Same live chrome via `<base href>`. Plan tabs, size buttons, drawdown modals, and the five Reward Cycle cards (80% On Demand / Weekly / Bi-Weekly, 90% On Demand / Bi-Weekly). 90% Weekly is not offered. On Demand still has to meet Instant 5 valid days or eval 3 trading days. Rec Instant has no $200k, 5 valid days at +0.5% SOD, and a 6% trail that never locks. **News is Allowed** on eval and funded. Rebuild with `python3 landing/stitch_trading_objectives.py`.

Plan-rule pages (live chrome, rec §4 payout copy): [`instant.html`](instant.html), [`1-step.html`](1-step.html), [`2-step-lite.html`](2-step-lite.html), [`2-step-pro.html`](2-step-pro.html). Rebuild with `python3 landing/stitch_plan_pages.py`. Instant also patches valid-day SOD equity, 6% trail never locks, and not-refundable-at-all. Evals keep the first-payout challenge-fee refund and add that add-ons are not refunded. **News is included** on every phase and funded account (not an add-on). Friday 22:00 flatten stays unless Weekend is paid.

Street vs 19 peers: [`../results/COMPETITOR_ADDONS.md`](../results/COMPETITOR_ADDONS.md) and PDF [`../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf`](../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf). 90% street is 10–20% of fee (Alpha 10, BG 15, FXIFY 20). Rec evals sit in that band; Instant **35%** for 90% On Demand is the year-1 floor, not a street match.

Reward cycles for Instant, 1-Step, Lite, and Pro:

| Cycle | Split | Request | Min | Checkout |
|---|---|---|---|---|
| On Demand | **80%** | Anytime after plan min days | $100 | add-on, **15%** evals / **18% Instant** |
| Weekly | **80%** | every 7 calendar days | $100 | add-on, **10%** of list |
| **Bi-Weekly (default)** | **80%** | every **14** calendar days | $100 | not a toggle |
| On Demand | **90%** | Anytime after plan min days | $100 | On Demand + 90% bundle, **25%** evals / **35% Instant** |
| Bi-Weekly | **90%** | every 14 calendar days | $100 | 90% add-on, **15%** evals / **18% Instant** |

Possible combinations (the five reward-cycle cards): **80% On Demand** · **80% Weekly** · **80% Bi-Weekly** included · **90% On Demand** · **90% Bi-Weekly**. Weekly XOR On Demand and XOR 90%. 90% Weekly is not offered.

On Demand still has to meet the plan trading-day rule: Instant **5 valid days** (0.5% SOD), 1-Step / Lite / Pro **3 trading days**. Then you may request anytime. Minimum reward is **$100** on every combination — not live’s On Demand 2% and $200.

First payout: Instant min $100 after 5 valid days; evals min $100 after 3 trading days (within 48 hrs). Intervals are calendar days.

### Blue Guardian (do not copy Instant 15%)

BG Instant Standard **includes** on-demand at **80%**. The 90% add-on is **+15%** of the challenge fee. Evals: 90% **+15%**, 7-day **+15%**, **both +25%** (save 5pp). Checkout.blueguardian.com Instant $100k list $623 → 7-day $93.45 / 90% $93.45 / both $155.75.

Verodus Instant default is **biweekly 80%**, so speed and 90% are paid add-ons. Do **not** sell Instant 90% On Demand at live’s 20% or BG’s 15% — year-1 extra E[X] is ~41% of BE ($112 on Instant $100k news-on). After VERO35 and 20% ads, 15% of $675 leaves ~$53 vs $112 cost. Rec Instant 90% On Demand is **35%** (~$11 leftover).

### Locked billing

| Add-on | Evals | Instant | Notes |
|---|---:|---:|---|
| News trading | **included** | **included** | Not an add-on. Allowed on evals and funded. |
| Weekend holding | 15% | 15% | Friday flatten off. Street live was 18% |
| Swing | **drop** | **drop** | News is already in the fee; do not charge 20% |
| Weekly 80% | 10% | 10% | Every 7 calendar days, same 80% as default. XOR On Demand and XOR 90%. BG 7-day 15% evals |
| On Demand 80% | 15% | **18%** | After plan min days, anytime. Instant 5 valid days; evals 3 trading days |
| 90% split | 15% | **18%** | Bi-Weekly unless On Demand is also on. Min $100. XOR Weekly. Alpha 10, BG 15, FXIFY 20 |
| **90% On Demand** (both) | **25%** | **35%** | Instant 35% is the year-1 floor. BG evals both 25% |

Sticker = `Math.round(list * pct)`. VERO35 is 35% off `list + addon stickers`. Refunds are challenge fee only.

Pro $100k ($475): weekend $71 / weekly $48 / On Demand 80% $71 / 90% $71 / 90% On Demand $119. Instant $100k ($675): weekend $101 / weekly $68 / On Demand 80% $122 / 90% $122 / 90% On Demand $236. News is included (no sticker). Swing is dropped.

### Multi-account (up to 4)

Blue Guardian checkout: 1st at the site code (BG25 = 25% off), 2nd **30%**, 3rd **35%**, 4th **40%**, and a 5th-free promo on some futures SKUs. Cap for Verodus: **4**. No 5th free — four Instant $100k on the same strategy is 4× year-1 E[X].

Do **not** copy the 30/35/40 ladder. VERO35 is already **35% off every copy**, which beats BG’s 25% on the 1st and BG’s ~32.5% average on a 4-pack. Extra cuts on the 2nd–4th do not print:

| SKU | Rec leftover after 20% ads | Max extra off the VERO35 sale |
|---|---:|---:|
| Instant $100k | ~$26 | ~8% |
| Lite $100k | ~$15 | ~7% |
| Pro $100k | ~$36 | ~15% |
| 1-Step $100k | ~$123 | ~40% |

Instant and Lite cannot fund a visible extra %. A 10% extra on Instant $100k copy 2 is about **−$9** after ads. Offer **qty 1–4 at VERO35, same add-ons on every copy, no extra ladder**.

Paste into `checkout.html`:

1. Keep `#coSectionAddons` / `#coAddons` markup — it is unchanged.
2. Replace `var ADDONS = [...]` with the `ADDONS` + `BUNDLES` blocks. Add `QTY_MAX = 4` and the Accounts tabs (`#coQty`).
3. Replace `addonPrice`, `renderAddons`, and `getAddonsTotal` with `addonPct` / `addonPrice` / `addonPriceTag` / `applyAddonToggle` / the new `renderAddons`.
4. Cart total = `unitPay() × qty`. Summary addon rows and GA item `price` must call `addonPrice(a)`. Skip `$0` GA lines (`Incl.` bundle members).
5. Optional: modal foot copy that add-on fees are not part of the first-payout challenge-fee refund. Tooltips stay product/rules — no “X% of list” copy.
