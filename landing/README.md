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

Open [`checkout-addons.html`](checkout-addons.html) for the Add-Ons section, ⓘ tooltips, and billing logic. Classes match live `checkout.css` (`.co-addon`, `.co-toggle`, `#coAddonModal`).

Paste into `checkout.html`:

1. Keep `#coSectionAddons` / `#coAddons` markup — it is unchanged.
2. Replace `var ADDONS = [...]` with the `ADDONS` block in that file (12% / 12% / 6% / 20%).
3. Replace `addonPrice`, `renderAddons`, and `getAddonsTotal` with `addonPct` / `addonPrice` / `addonPriceTag` / `applyAddonToggle` / the new `renderAddons`.
4. Summary addon rows and GA item `price` must call `addonPrice(a)` — not `Math.round(base * a.pct)`. Skip `$0` GA lines (Weekend when Swing is on).
5. Optional: modal foot copy that add-on fees are not part of the first-payout challenge-fee refund.

Locked billing:

| Add-on | % of list | Notes |
|---|---:|---|
| News trading | 12% | Funded news window off |
| Weekend holding | 12% | Friday flatten off |
| Both (Swing) | **20%** | Charge 20%, not 12+12. Weekend tag shows `Incl.` |
| Weekly rewards | 6% | Every 7 days, 70% split |
| On-demand | 20% | Anytime, 90%, min 2% and $200 |
| On-demand Instant | **32%** | Same 90% + anytime |

Weekly **XOR** on-demand — never both. Sticker = `Math.round(list * pct)`. VERO35 is 35% off `list + addon stickers`. Refunds are challenge fee only.
