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

News-included reprice 17 Aug 2026. Instant and 1-Step doors stay. Lite/Pro $5k–$10k follow the 2-step street door (Hola / TFT / Ment). Leftover on Lite/Pro **$25k and up** sits under Ment / Alpha 6% (Lite) and Hola / Alpha 10% (Pro) — not Maven $151 / $279.

| Plan | $5k | $10k | $25k | $50k | $100k | $200k |
|---|---|---|---|---|---|---|
| Instant | $49 / $75 | $69 / $106 | $149 / $229 | $239 / $368 | $439 / $675 | — |
| 1-Step | $45 / $69 | $69 / $106 | $129 / $198 | $219 / $337 | $379 / $583 | $699 / $1,075 |
| Lite | $39 / $60 | $55 / $85 | $115 / $177 | $169 / $260 | $309 / $475 | $599 / $922 |
| Pro | $45 / $69 | $59 / $91 | $125 / $192 | $199 / $306 | $349 / $537 | $699 / $1,075 |

JS: `plan-fees.js` — `[sale, list]`. Instant $200k is omitted on purpose.

## Checkout add-ons (drop-in)

Complete working page: [`checkout.html`](checkout.html). Add-on tooltip copy by plan: [`checkout-addon-tooltips.txt`](checkout-addon-tooltips.txt). Diff vs live verodus.com/checkout: [`checkout-vs-live.txt`](checkout-vs-live.txt). Chrome (nav, footer, CSS, icons, payment marks, mobile breakpoints) is loaded from [verodus.com/checkout.html](https://www.verodus.com/checkout.html). Quantity sits in the order summary like Blue Guardian (`1st Account` … `4th Account`), not as a left-column section. US-citizen term is removed. Rebuild with `python3 landing/stitch_checkout.py`.

Complete trading-objectives page: [`trading-objectives.html`](trading-objectives.html). Diff vs live verodus.com/trading-objectives: [`trading-objectives-vs-live.txt`](trading-objectives-vs-live.txt). Same live chrome via `<base href>`. Plan tabs, size buttons, drawdown modals, and three Reward Cycle cards like live: Weekly 70% · Bi-Weekly 80% (featured) · On Demand 90% (min $100, not live’s 2% / $200). On Demand still has to meet Instant 5 valid days or eval 3 trading days. Rec Instant has no $200k, 5 valid days at +0.5% SOD, and a 6% trail that never locks. **News is Allowed** on eval and funded. Rebuild with `python3 landing/stitch_trading_objectives.py`.

Plan-rule pages (live chrome, rec §4 payout copy): [`instant.html`](instant.html), [`1-step.html`](1-step.html), [`2-step-lite.html`](2-step-lite.html), [`2-step-pro.html`](2-step-pro.html). Rebuild with `python3 landing/stitch_plan_pages.py`. Instant also patches valid-day SOD equity, 6% trail never locks, and not-refundable-at-all. Evals keep the first-payout challenge-fee refund and add that add-ons are not refunded. **News is included** on every phase and funded account (not an add-on): the live News Trading Addon SKU, ±2-minute window, and tiered news-breach copy are stripped. Friday 22:00 flatten stays unless Weekend is paid. Minimum reward is **$100** on Bi-Weekly 80%, Weekly 70%, and On Demand 90%.

Street vs 19 peers: [`../results/COMPETITOR_ADDONS.md`](../results/COMPETITOR_ADDONS.md) and PDF [`../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf`](../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf). Checkout: Weekly 70% at **6% of list**, On Demand 90% at **32% Instant / 15% evals**. News is included (no SKU).

Reward cycles for Instant, 1-Step, Lite, and Pro:

| Cycle | Split | Request | Min | Checkout |
|---|---|---|---|---|
| Weekly Rewards with 70% Reward Split | **70%** | every 7 calendar days | $100 | add-on, **6%** of list |
| **Bi-Weekly (default)** | **80%** | every **14** calendar days | $100 | not a toggle |
| On Demand Rewards with 90% Split | **90%** | Anytime after plan min days | $100 | add-on, **32% Instant / 15% evals** |

News is included (no SKU). Weekend Holding is 15% of list. Weekly and On Demand can be selected together (same as live). There is no separate 90% Bi-Weekly SKU — On Demand is the 90% product.

On Demand still has to meet the plan trading-day rule: Instant **5 valid days** (0.5% SOD), 1-Step / Lite / Pro **3 trading days**. Then you may request anytime. Minimum reward is **$100** on every combination — not live’s On Demand 2% and $200.

First payout: Instant min $100 after 5 valid days; evals min $100 after 3 trading days (within 48 hrs). Intervals are calendar days.

### Blue Guardian (do not copy Instant 15%)

BG Instant Standard **includes** on-demand at **80%**. The 90% add-on is **+15%** of the challenge fee. Evals: 90% **+15%**, 7-day **+15%**, **both +25%** (save 5pp). Checkout.blueguardian.com Instant $100k list $623 → 7-day $93.45 / 90% $93.45 / both $155.75.

Verodus Instant default is **biweekly 80%**, so Weekly 70% and On Demand 90% are paid add-ons. Do not copy BG Instant 15% for 90%+anytime. Instant On Demand is **32% of list** so year-1 leftover prints. Evals are **15%**.

### Locked billing

| Add-on | Evals | Instant | Notes |
|---|---:|---:|---|
| News trading | **included** | **included** | Not an add-on. Allowed on evals and funded. |
| Weekend holding | 15% | 15% | Friday flatten off. Street live was 18% |
| Swing | **drop** | **drop** | News is already in the fee; do not charge 20% |
| Weekly Rewards with 70% Reward Split | **6%** | **6%** | Withdraw your profit share weekly. Same % on every size. |
| On Demand Rewards with 90% Split | **15%** | **32%** | Withdraw anytime after the plan trading-day rule. Min $100. Instant 32% prints year-1. |

Sticker = `Math.round(list * pct)`. VERO35 is 35% off `list + addon stickers`. Refunds are challenge fee only.

Pro $100k ($537): weekend $81 / weekly $32 / On Demand 90% $81. Instant $100k ($675): weekend $101 / weekly $41 / On Demand 90% $216. News is included (no sticker). Swing is dropped.

### Multi-account (up to 4)

Blue Guardian checkout: 1st at the site code (BG25 = 25% off), 2nd **30%**, 3rd **35%**, 4th **40%**, and a 5th-free promo on some futures SKUs. Cap for Verodus: **4**. No 5th free — four Instant $100k on the same strategy is 4× year-1 E[X].

Do **not** copy the 30/35/40 ladder. VERO35 is already **35% off every copy**, which beats BG’s 25% on the 1st and BG’s ~32.5% average on a 4-pack. Extra cuts on the 2nd–4th do not print:

| SKU | Rec leftover after 20% ads | Max extra off the VERO35 sale |
|---|---:|---:|
| Instant $100k | ~$26 | ~8% |
| Lite $100k | ~$42 | ~14% |
| Pro $100k | ~$68 | ~20% |
| 1-Step $100k | ~$123 | ~40% |

Instant cannot fund a visible extra %. Lite $100k leftover is now about **$42**, so a 10% extra would still print, but skip the ladder — VERO35 is already 35% on every copy. Offer **qty 1–4 at VERO35, same add-ons on every copy, no extra ladder**.

Paste into `checkout.html`:

1. Keep `#coSectionAddons` / `#coAddons` markup — it is unchanged.
2. Replace `var ADDONS = [...]` with the `ADDONS` block (Weekend 15%, Weekly 70% at 6%, On Demand 90% at 32% Instant / 15% evals). Add `QTY_MAX = 4` and the Accounts tabs (`#coQty`).
3. Replace `addonPrice`, `renderAddons`, and `getAddonsTotal` with `addonPct` / `addonPrice` / `addonPriceTag` / `applyAddonToggle` / the new `renderAddons`. Weekly and On Demand may both be on.
4. Cart total = `unitPay() × qty`. Summary addon rows and GA item `price` must call `addonPrice(a)`. Skip `$0` GA lines (`Incl.` bundle members).
5. Optional: modal foot copy that add-on fees are not part of the first-payout challenge-fee refund. Tooltips stay product/rules — no “X% of list” copy.
