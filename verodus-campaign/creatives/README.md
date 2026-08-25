# Creatives — 33 PNGs

Rendered from code so type, prices, and rule claims are exact and editable. Rebuild after any change:

```bash
cd ../build && python3 build_all.py
```

Requires headless `google-chrome` and the Inter font family. Changing a price is a one-line edit in `build/week*.py`, not a redraw.

## House style — from the brand kit

Tokens come from `verodus.com/brand-kit.html`, so these match the live site.

| Element | Value |
|---|---|
| Gold | `#d4af37`, rendered as a champagne→amber metal gradient |
| Background | `#07003B` → `#1B2B8E` (page start → end blue) |
| Heading / body | `#f5f5f5` / `#cbd5e1` |
| CTA text on gold | `#0f172a` |
| Type | **Inter** — 900 uppercase headlines, 300–500 body |
| Logo | Official `Verodus-logo.png` and `Verodus-logo-only.png`, centred bottom |
| Texture | Faint gold candlesticks, lower third, ~8% opacity |

Logos are never stretched, rotated, or filtered. No colours outside the theme except the blue plan chip on the comparison table.

Formats: **1:1** 1080×1080 · **4:5** 1080×1350 · **9:16** 1080×1920 · overlays transparent.

## Paid eligibility

| File | Size | Use | Paid? |
|---|---|---|---|
| `w1-manifesto-open.png` | 9:16 | Opening frame, hero video | ✅ |
| `w1-manifesto-end.png` | 9:16 | Standing end card, all videos | ✅ |
| `w1-tryfree-1/2/3.png` | 4:5 | Free-trial carousel | ✅ |
| `w1-discord.png` | 1:1 | Discord announcement | Organic — off-platform CTA |
| `w1-logo-bug.png` | transparent | Corner bug, every video | ✅ |
| `w2-static-key.png` | 9:16 | Explainer hero frame | ✅ |
| `w2-static-diagram.png` | 9:16 | Two-panel diagram, animate or post flat | ✅ |
| `w2-rule-a…e.png` | 4:5 | Five-card rule carousel | ✅ |
| `w2-plans.png` | 1:1 | Four-plan comparison | ✅ |
| `w2-chip-1/2/3.png` | transparent | Overlays for the screen-share | ✅ |
| `w3-ama-q1/q2/q3.png` | 9:16 | AMA question cards | Organic — AMA is organic |
| `w3-ama-thumb.png` | 1:1 | AMA announcement | Organic |
| `w3-walkthrough-end.png` | 9:16 | Walkthrough end frame | ✅ |
| `w3-step-strip.png` | transparent | Step chips during the recording | ✅ |
| `w3-momentum.png` | 1:1 | Weekly activity — swap `[ N ]` | **Organic only** — activity claim we can't substantiate ad-side |
| `w3-promise-1.png` | 4:5 | Dated promise card — fill `[DATE]` | ✅ |
| `w3-promise-2.png` | 4:5 | The four rule cards as receipts | ✅ |
| `w4-offer-card.png` | 9:16 | Offer overlay + Story ad — fill `[DATE]` | ✅ warm only |
| `w4-pricing.png` | 4:5 | Founding pair, primary conversion still | ✅ |
| `w4-sizes.png` | 4:5 | Size ladder, no stickers | ✅ |
| `w4-montage-open.png` | 9:16 | Montage first frame | Organic |
| `w4-montage-end.png` | 9:16 | Montage last frame | Organic |
| `w4-lastchance.png` | 9:16 | Retargeting Story | ✅ **only if pricing actually ends** |

## Before publishing

- Fill every `[DATE]` (`w4-offer-card`, `w4-pricing`, `w3-promise-1`) and `[ N ]` (`w3-momentum`).
- Confirm `$72` and `$36` still match checkout with VERO35.
- Never pair an Instant creative with fee-refund or static-drawdown copy.
- `w2-static-key.png` shows a `$10,000 / $1,000` illustration — that's a **drawdown example, not a fee**, and it's plan-labelled. Fine as-is.
- No payout figures on any paid asset.

## Prices carried in these files

| Plan | Sale | List |
|---|---|---|
| Instant $5,000 | **$72** | $110 |
| 1-Step $5,000 | **$36** | $55 |

Both verified against the live site. Instant $25k and above is at or below break-even and carries no price in any creative — `w4-sizes.png` lists sizes without stickers for that reason, and omits Instant at $200,000 because that tier isn't offered.
