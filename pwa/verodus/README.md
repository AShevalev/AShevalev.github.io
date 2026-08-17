# Install Verodus from the landing page without the Chrome bar

Most people tap **for android** / **for iOS** on [verodus.com](https://www.verodus.com). That must install **www.verodus.com** and open `/app`. A top-level jump to `dashboard.verodus.com` is what draws the X / URL / Verodus CRM bar (desktop and mobile).

Per-browser matrix: **[BROWSERS.md](BROWSERS.md)**.

```
www.verodus.com          landing + install CTAs
www.verodus.com/app      installed app shell (never leaves this host)
  iframe → dashboard.verodus.com/dashboard
    iframe or in-frame nav → trade.verodus.com/tradehub/{id}
                            → trade.verodus.com/p5/{id}
```

## 1. Landing page (`www.verodus.com`)

| This repo | On verodus.com |
|---|---|
| `www/manifest.json` | `/manifest.json` (`start_url`: `/app`) |
| `www/sw.js` | `/sw.js` |
| `www/images/pwa-icon-192.png` + `512.png` | `/images/` (PNG, not WebP-only) |
| `www/app.html` | **`/app`** or `/app/index.html` |
| `www/head.html` | landing `<head>` |
| `www/store-buttons.html` + `store-buttons.js` | replace Play Store / App Store pills |

Pills `href="/app"`. JS runs the install prompt **on this origin**, then goes to `/app`. Copy the repo `pwa/` folder onto the landing origin so `/pwa/add-to-home-screen.js` and `store-buttons.js` resolve.

The Chrome toolbar install icon is the same PWA: use it only while the tab is on `www.verodus.com`, not after a click-through to Dashboard.

## 2. Let `/app` iframe the CRM and terminals

Dashboard `frame-ancestors`: `https://www.verodus.com`  
Trade `frame-ancestors`: `https://www.verodus.com` and `https://dashboard.verodus.com`  

See `dashboard/frame-headers.js` and `trade/frame-headers.js`. Remove `X-Frame-Options: DENY`.

Google sign-in: popup, or return to `https://www.verodus.com/app`. Do not `window.top` navigate to dashboard.

## 3. Optional: Dashboard-only install

If someone opens `dashboard.verodus.com` directly, keep the same-origin `/p5/{id}` and `/tradehub/{id}` iframe routes (`PlatformFrame.jsx`). That is a fallback, not the main path.

## Check

1. On a phone or desktop Chrome, open verodus.com (not dashboard).
2. Tap **for android** / **for iOS**, install, then open from the home screen / app icon.
3. You should land on `/app` with no X / URL bar.
4. Use the CRM, then Platform5, then TradeHub. The bar must not return.
