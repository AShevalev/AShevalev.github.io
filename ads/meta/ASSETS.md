# Asset production — 4-week launch

33 PNGs in [`creatives/launch/`](creatives/launch/), rendered from code so the type,
prices, and rules are exact. Rebuild any time:

```bash
cd ads/meta/build && python3 build_all.py
```

Requires headless `google-chrome` and the Inter family. Editing a price means editing
one Python string, not redrawing a graphic.

---

## House style — from the brand kit, not an invented palette

Tokens come from `verodus.com/brand-kit.html`, so these files match the live site.

| Element | Value |
|---|---|
| Gold (headline / CTA) | `#d4af37` — rendered as a champagne→amber metal gradient |
| Background | `#07003B` → `#1B2B8E` (page start → end blue) |
| Heading / body | `#f5f5f5` / `#cbd5e1` |
| CTA text on gold | `#0f172a` |
| Type | **Inter** (900 uppercase headlines, 300–500 body) |
| Logo | Official `Verodus-logo.png` + `Verodus-logo-only.png`, centered bottom |
| Texture | Faint gold candlesticks in the lower third, ~8% opacity |

Brand-kit rules honored: logos are never stretched, rotated, or filtered; they sit on the
start blue / page gradient with clear space; no colors outside the theme except the blue
plan chip on the comparison table.

Two deliberate deviations from the Atria spec:

1. **Palette.** Atria specified navy `#0A1428` → black and "three descending gold chevrons."
   The real mark is ascending gold bars with an arrow, and the real background is the blue
   gradient above. Brand kit wins.
2. **No stock person** on the Discord card. A composited "confident trader" undercuts the
   anti-hype posture and adds a licensing problem. The card leads with the real channel list.

Formats: **1:1** 1080×1080 · **4:5** 1080×1350 · **9:16** 1080×1920 · overlays transparent PNG.

---

## Copy corrections baked into these assets

Atria's verbatim lines conflict with the live FAQ. The renders use the corrected wording.

| Atria line | Why it is wrong | Rendered instead |
|---|---|---|
| "Static drawdown" as a firm-wide benefit | Instant is 6% **trailing**, never locks; 1-Step is hybrid | Static tiles/diagram are labeled **2-Step Lite & Pro** |
| "Fee back on your first payout" in the offer | **Instant has no refund** | "Fee back on **evaluations**. Instant excluded." |
| "Up to 90% split" | 90% is the **on-demand** cycle; 80% is standard | "80% split · 90% on demand" |
| Code `VERO-FOUND` | A second code stacked on VERO35 destroys Instant margin | Founding offer **is VERO35** |
| Price ladder $5K–$200K with founding prices | Instant $25k+ is at or below break-even | Only the two verified SKUs carry a price; the ladder ships without stickers |

Verified prices used: **Instant $5,000 = $72** (list $110) and **1-Step $5,000 = $36**
(list $55). Both confirmed against the live site.

---

## Week 1 — Founders intro & free trial

| Asset | File | Size | Use |
|---|---|---|---|
| 1.1 Founders-intro open card | `w1-manifesto-open.png` | 9:16 | First frame of the intro Reel |
| 1.1 Founders-intro end card | `w1-manifesto-end.png` | 9:16 | Last frame + standalone Story |
| 1.2 Try-free tile 1 | `w1-tryfree-1.png` | 4:5 | Carousel card 1 / W1 paid hero |
| 1.2 Try-free tile 2 | `w1-tryfree-2.png` | 4:5 | Carousel card 2 |
| 1.2 Try-free tile 3 | `w1-tryfree-3.png` | 4:5 | Carousel card 3 |
| 1.3 Discord welcome | `w1-discord.png` | 1:1 | Feed + Discord (server already open) |
| 1.4 Logo bug | `w1-logo-bug.png` | 520×150, transparent | Corner bug for every founder video |

**Founders intro VO (30–45s)** — full script in [`VIDEO-SCRIPTS.md`](VIDEO-SCRIPTS.md)

Video VO carries **no prices**. The statics carry them.

> Most prop firms make traders feel trapped… So we built Verodus to be the opposite of clever.
> Every objective is published before you pay. No time limit. The rules you start under are the
> rules you keep. Start the free trial, read every rule, and come argue with us in Discord.

Shoot: founder at a real desk, phone on a tripod, window light, chest-up, one take,
burned-in captions with gold keyword highlights.

**"Why we built this" VO (20–25s)**

> I got tired of firms that sell you one set of rules and enforce another. You pay, you pass,
> and suddenly there's a clause that wasn't there on signup day. So every Verodus objective is
> public before you put money down. The rules you start under are the rules you keep. We don't
> do retroactive edits.

**Discord pinned welcome**

> Verodus has been operating since May. This is the founding community for the public intro.
> Instant, 1-Step, Lite, Pro — rules in #rules, same as the site. Founders are in here daily.
> Free trial: verodus.com. Code VERO35. No fake payouts. Certificates go in #payout-proof.

---

## Week 2 — Rules & transparency

| Asset | File | Size | Use |
|---|---|---|---|
| 2.1 Key statement frame | `w2-static-key.png` | 9:16 | Hero frame of the explainer |
| 2.1 Two-panel diagram | `w2-static-diagram.png` | 9:16 | Animate the two panels; also a standalone post |
| 2.2 Rule tiles A–E | `w2-rule-a…e.png` | 4:5 | 5-card carousel |
| 2.3 Plan comparison | `w2-plans.png` | 1:1 | Feed + Discord + link post |
| 2.4 Caption chips 1–3 | `w2-chip-1…3.png` | transparent | Overlays for the screen-share short |

Rule tiles as rendered:

1. **No time limit** — Trade at your own pace.
2. **Static max loss** — Fixed from day one — 2-Step Lite & Pro.
3. **80% split** — 90% on the on-demand cycle.
4. **Fee back on first reward** — 100% refund on evaluations. Instant excluded.
5. **Scale to $1,000,000** — Grow with measured performance.

**Explainer VO (40–60s)** — [`VIDEO-SCRIPTS.md`](VIDEO-SCRIPTS.md) §4

> A trailing drawdown follows your equity high, so you can be green, take a normal pullback,
> and get stopped out in profit. On Verodus 2-Step your max loss is static — fixed from your
> starting balance. Instant trails, and it says so on the card.

The `w2-static-key.png` frame does carry a `$10,000 / $1,000` illustration. That is a
drawdown example, not a fee — fine on a static, and the VO does not read a price.

**Screen-share VO (20–30s)** — scroll the real objectives page, drop a chip on each rule.

> Same page that's been on the site since May. No time limit — right here. Static max
> drawdown on 2-Step — right here. Fee back on your first reward, evaluations — right here.
> Read it yourself. That's the whole pitch.

---

## Week 3 — Trust, founder access & first cohort

| Asset | File | Size | Use |
|---|---|---|---|
| 3.1 AMA question cards | `w3-ama-q1…q3.png` | 9:16 | Cut between answers |
| 3.1 AMA thumbnail | `w3-ama-thumb.png` | 1:1 | Announcement post / video thumb |
| 3.2 Walkthrough end card | `w3-walkthrough-end.png` | 9:16 | Last frame |
| 3.2 Step strip | `w3-step-strip.png` | transparent | Top-of-frame chips during the recording |
| 3.3 Momentum card | `w3-momentum.png` | 1:1 | Weekly activity — swap `[ N ]` |
| 3.4 Promise card | `w3-promise-1.png` | 4:5 | Statement, add the date |
| 3.4 Receipts card | `w3-promise-2.png` | 4:5 | The four rule cards as receipts |

Questions rendered: *Are the rules public? · How do rewards work? · Why is Instant priced differently?*
Do not use “why trust a new firm.”

**AMA** — four Q&As in [`VIDEO-SCRIPTS.md`](VIDEO-SCRIPTS.md) §6. No dollar figures on camera.

> Don't believe us yet. We've been running since May, the rules are public, and I'm in the
> Discord every day. Judge the operation, not the edit.

**Walkthrough VO (30–45s)** — record: free-trial start → dashboard → in-app rules → checkout.

> Start the free trial — same rules engine, same TradeHub or Platform 5. Objectives track
> live on the dashboard. When you're ready, pick the model that matches how you trade.

`[ N ]` on the momentum card is **activity only** — traders joined, challenges started or
passed. Never a payout figure this month.

---

## Week 4 — Founding offer & conversion

| Asset | File | Size | Use |
|---|---|---|---|
| 4.1 Offer card | `w4-offer-card.png` | 9:16 | Overlay in the founding video + Story ad |
| 4.2 Founding pricing | `w4-pricing.png` | 4:5 | Primary paid conversion still |
| 4.2 Size ladder | `w4-sizes.png` | 4:5 | Carousel card 2 — sizes, no stickers |
| 4.3 Montage open | `w4-montage-open.png` | 9:16 | First frame |
| 4.3 Montage end | `w4-montage-end.png` | 9:16 | Last frame |
| 4.4 Last chance | `w4-lastchance.png` | 9:16 | Retargeting Story only |

**Intro-offer VO (30s)** — [`VIDEO-SCRIPTS.md`](VIDEO-SCRIPTS.md) §8. The overlay card carries
the price; the VO says "the code is in the bio."

> There's an intro code running while we do this founders series. It's the only one — we
> don't stack a second discount and call it a sale. Objectives published up front, no time
> limit, static max loss on 2-Step, fee back on first reward on the evaluations. Start free.

Only imply an ending if intro pricing actually ends. Otherwise: *"The rules aren't changing.
Neither is the trial."*

`[DATE]` appears on `w4-offer-card`, `w4-pricing`, `w3-promise-1`. Fill before publishing.

---

## Video checklist

Two shoots cover all nine videos.

| Session | Records | Feeds |
|---|---|---|
| A — week 1 | Founders intro, "why we built this", rules read-through | 1.1, 1.4, 2.4 |
| B — week 3 | AMA, product walkthrough, first-cohort clips | 3.1, 3.2, and the 4.3 montage |

Export H.264 MP4, 1080×1920, 30 fps, burned-in captions, logo bug top-left.
2.1 is a motion build in CapCut/After Effects from `w2-static-diagram.png`.

---

## Before publishing

- Fill every `[DATE]` and `[ N ]`.
- Confirm `$72` and `$36` still match checkout with VERO35.
- Never pair Instant creative with refund or static-drawdown copy.
- No payout figures in any paid asset this month.
