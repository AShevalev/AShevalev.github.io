# Meta tags for verodus.com

Paste-ready `<head>` tags for [verodus.com](https://www.verodus.com/). The live homepage already has a title, description, and basic Open Graph tags, but two things block Meta ads and a clean share card:

1. There is **no** `facebook-domain-verification` tag (Business Manager cannot verify the domain).
2. `og:image` is the **400×81** wordmark. Meta wants **1200×630**.

## 1. The domain-verification tag

This is the tag Meta Business Suite gives you. Copy it from **Settings → Brand safety → Domains → Add `verodus.com` → Add a meta-tag to your HTML source code**.

```html
<meta name="facebook-domain-verification" content="FACEBOOK_DOMAIN_VERIFICATION_CODE">
```

Put it in the shared header (homepage is enough for verification; every public page is better). Publish, then click **Verify**. Leave the tag in place — Meta re-checks it.

## 2. Full `<head>` block

Ready to paste: [`head.html`](head.html). It keeps the live title and description, then adds:

| Tag | Why |
|---|---|
| `facebook-domain-verification` | Domain verify in Business Manager |
| `og:image` 1200×630 + width/height/alt | Link previews in Facebook, Instagram, Slack, iMessage |
| `og:locale` + alternates | Matches Weglot (`es`, `zh`, `ar`, `fr`, `pt`) |
| `twitter:card` `summary_large_image` + `@VerodusOfficial` | X/Twitter large card |
| `robots` `max-image-preview:large` | Lets Google show the large share image |

Replace `FACEBOOK_DOMAIN_VERIFICATION_CODE` before shipping. Do not invent a code.

## 3. Upload the share image

Files in this folder:

- [`og-default.png`](og-default.png) — 1200×630, brand gradient, official wordmark
- [`og-default.webp`](og-default.webp) — same card, drop-in for the live path

Upload to **`https://www.verodus.com/images/og-default.webp`** (replace the current file). PNG is the fallback if you cannot serve WebP.

Rebuild after copy changes:

```bash
cd ads/meta/tags && python3 build_og.py
```

## 4. Pixel (separate from the meta tag)

Domain verification is a `<meta>` tag. Conversion tracking is the Pixel. Paste [`pixel.html`](pixel.html) after `<head>` opens, replace `PIXEL_ID`, then fire:

| Event | When |
|---|---|
| `PageView` | every page (in the snippet) |
| `ViewContent` | evaluation plan viewed |
| `CompleteRegistration` | free-trial signup |
| `InitiateCheckout` | checkout started |
| `Purchase` | fee paid — `value` = fee, `currency` = USD or CAD |

Pair with Conversions API from the server. Event order: `Purchase` (fee paid) → `InitiateCheckout` → `CompleteRegistration` (free trial) → `ViewContent`.

## 5. Confirm

1. View source on https://www.verodus.com/ and find `facebook-domain-verification`.
2. [Sharing Debugger](https://developers.facebook.com/tools/debug/) → scrape `https://www.verodus.com/` → image should be 1200×630.
3. Business Manager → Domains → **Verify**.
4. Events Manager → Test events → load the homepage → `PageView`.
