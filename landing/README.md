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

Open [`checkout-addons.html`](checkout-addons.html) for the Add-Ons section, ⓘ tooltips, bundles, and billing logic. Classes match live `checkout.css` (`.co-addon`, `.co-toggle`, `#coAddonModal`).

### Blue Guardian (do not copy Instant 15%)

BG Instant Standard **includes** on-demand at **80%**. The 90% add-on is **+15%** of the challenge fee. Evals: 90% **+15%**, 7-day **+15%**, **both +25%** (save 5pp). Checkout.blueguardian.com Instant $100k list $623 → 7-day $93.45 / 90% $93.45 / both $155.75.

Verodus Instant default is **biweekly 80%**, so speed is a paid add-on. Do **not** sell Instant 90% + anytime at BG’s 15% — year-1 extra E[X] is ~41% of BE ($116 on Instant $100k). After VERO35 and 20% ads, 15% of $675 leaves ~$53 vs $116 cost.

### Locked billing

| Add-on | Evals | Instant | Notes |
|---|---:|---:|---|
| News trading | 12% | 12% | Funded news window off |
| Weekend holding | 12% | 12% | Friday flatten off |
| **Swing** (both) | **20%** | **20%** | Not 12+12. Weekend `Incl.` |
| Weekly rewards | 6% | 6% | Every 7 days, 70% split |
| On-demand (80%) | 12% | **15%** | Anytime, keep 80%. BG Instant includes this; we charge because default is biweekly |
| 90% split | 12% | **20%** | Keep biweekly unless on-demand is also on |
| **90% On Demand** (both) | **20%** | **32%** | Not 12+12 / 15+20. 90% row `Incl.` |

Weekly **XOR** on-demand and 90% — never with either. On-demand and 90% **may both be on** (that is the bundle). Sticker = `Math.round(list * pct)`. VERO35 is 35% off `list + addon stickers`. Refunds are challenge fee only.

Pro $100k ($445): news $53 / weekend $53 / Swing $89 / weekly $27 / on-demand 80% $53 / 90% $53 / 90% On Demand $89. Instant $100k ($675): on-demand 80% $101 / 90% $135 / 90% On Demand $216 / Swing $135.

Paste into `checkout.html`:

1. Keep `#coSectionAddons` / `#coAddons` markup — it is unchanged.
2. Replace `var ADDONS = [...]` with the `ADDONS` + `BUNDLES` blocks.
3. Replace `addonPrice`, `renderAddons`, and `getAddonsTotal` with `addonPct` / `addonPrice` / `addonPriceTag` / `applyAddonToggle` / the new `renderAddons`.
4. Summary addon rows and GA item `price` must call `addonPrice(a)`. Skip `$0` GA lines (`Incl.` bundle members).
5. Optional: modal foot copy that add-on fees are not part of the first-payout challenge-fee refund.
