# Landing page meta + fees

Paste `head-meta.html` into the Verodus-4-centered `<head>` (replace the current title / description / OG / Twitter block).

Do **not** keep “from $18” — that was the old Lite $5k VERO35. Floor is **1-Step $36**. Instant starts at **$49**. Lite starts at **$42**.

## SERP copy (locked)

| Field | Text | Chars |
|---|---|---:|
| Title | Verodus — Instant from $49. Funded on Day One. | 47 |
| Description | Funded on day one from $49. Pass a 1-Step from $36 or Lite from $42. Trade Forex, indices and crypto on $5k–$200k. Keep 80%. No deposit. | 136 |
| OG title | Verodus — Instant from $49. Funded on Day One. | 47 |

Default split is **80%**. 90% is a paid add-on — do not lead the meta with 90% or $1M.

## Rec sale / list (VERO35)

| Plan | $5k | $10k | $25k | $50k | $100k | $200k |
|---|---|---|---|---|---|---|
| Instant | $49 / $75 | $69 / $106 | $139 / $214 | $239 / $368 | $439 / $675 | — |
| 1-Step | $36 / $55 | $60 / $92 | $120 / $185 | $193 / $297 | $335 / $515 | $654 / $1,006 |
| Lite | $42 / $65 | $55 / $85 | $94 / $145 | $149 / $229 | $269 / $414 | $499 / $768 |
| Pro | $45 / $69 | $59 / $91 | $95 / $146 | $159 / $245 | $289 / $445 | $577 / $888 |

JS: `plan-fees.js` — `[sale, list]`. Instant $200k is omitted on purpose.

## Checkout add-ons (drop-in)

Complete working page: [`checkout.html`](checkout.html). Chrome (nav, footer, CSS, icons, payment marks, mobile breakpoints) is loaded from [verodus.com/checkout.html](https://www.verodus.com/checkout.html). Quantity sits in the order summary like Blue Guardian (`1st Account` … `4th Account`), not as a left-column section. US-citizen term is removed. Rebuild with `python3 landing/stitch_checkout.py`.

Street vs 19 peers: [`../results/COMPETITOR_ADDONS.md`](../results/COMPETITOR_ADDONS.md) and PDF [`../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf`](../results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf). 90% street is 10–20% of fee (Alpha 10, BG 15, FXIFY 20). Rec evals sit in that band; Instant 32% for On Demand 90% is the year-1 floor, not a street match.

Reward cycles match [trading-objectives](https://www.verodus.com/trading-objectives.html) for Instant, 1-Step, Lite, and Pro:

| Cycle | Split | Request | Min | Checkout |
|---|---|---|---|---|
| Weekly | 70% | every 7 calendar days | $100 | add-on, 6% of list |
| **Bi-Weekly (default)** | **80%** | every **14** calendar days | $100 | not a toggle |
| On Demand | 90% | Anytime | 2% and $200 | add-on, 20% evals / **32% Instant** |

First payout: min $100 after 3 trading days (within 48 hrs). Intervals are calendar days. Weekly **XOR** On Demand.

### Blue Guardian (do not copy Instant 15%)

BG Instant Standard **includes** on-demand at **80%**. The 90% add-on is **+15%** of the challenge fee. Evals: 90% **+15%**, 7-day **+15%**, **both +25%** (save 5pp). Checkout.blueguardian.com Instant $100k list $623 → 7-day $93.45 / 90% $93.45 / both $155.75.

Verodus Instant default is **biweekly 80%**, so speed+90% is a paid add-on. Do **not** sell Instant On Demand 90% at live’s 20% or BG’s 15% — year-1 extra E[X] is ~41% of BE ($116 on Instant $100k). After VERO35 and 20% ads, 15% of $675 leaves ~$53 vs $116 cost.

### Locked billing

| Add-on | Evals | Instant | Notes |
|---|---:|---:|---|
| News trading | 12% | 12% | Funded news window off |
| Weekend holding | 12% | 12% | Friday flatten off |
| **Swing** (both) | **20%** | **20%** | Not 12+12. Weekend `Incl.` |
| Weekly 70% | 6% | 6% | Every 7 calendar days, min $100. XOR On Demand |
| On Demand 90% | 20% | **32%** | Anytime, min 2% and $200. Instant 32% is the year-1 floor |

Sticker = `Math.round(list * pct)`. VERO35 is 35% off `list + addon stickers`. Refunds are challenge fee only.

Pro $100k ($445): news $53 / weekend $53 / Swing $89 / weekly $27 / On Demand 90% $89. Instant $100k ($675): weekly $41 / On Demand 90% $216 / Swing $135.

### Multi-account (up to 4)

Blue Guardian checkout: 1st at the site code (BG25 = 25% off), 2nd **30%**, 3rd **35%**, 4th **40%**, and a 5th-free promo on some futures SKUs. Cap for Verodus: **4**. No 5th free — four Instant $100k on the same strategy is 4× year-1 E[X].

Do **not** copy the 30/35/40 ladder. VERO35 is already **35% off every copy**, which beats BG’s 25% on the 1st and BG’s ~32.5% average on a 4-pack. Extra cuts on the 2nd–4th do not print:

| SKU | Rec leftover after 20% ads | Max extra off the VERO35 sale |
|---|---:|---:|
| Instant $100k | ~$13 | ~4% |
| Lite $100k | ~$14 | ~6% |
| Pro $100k | ~$33 | ~14% |
| 1-Step $100k | ~$108 | ~40% |

Instant and Lite cannot fund a visible extra %. A 10% extra on Instant $100k copy 2 is about **−$22** after ads. Offer **qty 1–4 at VERO35, same add-ons on every copy, no extra ladder**.

Paste into `checkout.html`:

1. Keep `#coSectionAddons` / `#coAddons` markup — it is unchanged.
2. Replace `var ADDONS = [...]` with the `ADDONS` + `BUNDLES` blocks. Add `QTY_MAX = 4` and the Accounts tabs (`#coQty`).
3. Replace `addonPrice`, `renderAddons`, and `getAddonsTotal` with `addonPct` / `addonPrice` / `addonPriceTag` / `applyAddonToggle` / the new `renderAddons`.
4. Cart total = `unitPay() × qty`. Summary addon rows and GA item `price` must call `addonPrice(a)`. Skip `$0` GA lines (`Incl.` bundle members).
5. Optional: modal foot copy that add-on fees are not part of the first-payout challenge-fee refund. Tooltips stay product/rules — no “X% of list” copy.
