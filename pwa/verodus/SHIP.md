# Ship this week (the path that works)

Do not merge the apps. Do not rely on `scope_extensions`. Do not iframe twice.

**One installable app:** `https://www.verodus.com`  
**One extra page:** `/app` (iframes the CRM)  
**Inside that iframe:** Platform 5 and TradeHub can keep their current `trade.verodus.com` links. That is not a top-level host change, so Chrome does not draw the bar.

```
verodus.com  →  install
/app         →  iframe dashboard.verodus.com
                 └─ clicks to TradeHub / P5 stay in that iframe
```

Skip `lock-origin.js`, Dashboard `PlatformFrame` routes, and Trade manifests until this is live and verified.

## 1. Landing (`www.verodus.com`) — four files

| Put this on the site | From this repo |
|---|---|
| `/manifest.json` | `www/manifest.json` (`start_url` must be `/app`) |
| `/sw.js` | `www/sw.js` |
| `/app/index.html` | `www/app.html` |
| `/images/pwa-icon-192.png` and `/images/pwa-icon-512.png` | `www/images/` (PNG, not WebP-only) |

In the landing `<head>` (see `www/head.html`):

```html
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#07003B" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-title" content="Verodus" />
<link rel="apple-touch-icon" href="/images/pwa-icon-192.png" />
```

Register the worker once on the landing page:

```html
<script>
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js");
  }
</script>
```

## 2. Change the two pills only

Stop linking to Play Store / App Store / `dashboard.verodus.com`.

```html
<a class="v-store-pill" href="/app">for android</a>
<a class="v-store-pill" href="/app">for iOS</a>
<script src="/js/install.js"></script>
```

Copy `www/install.js` to `/js/install.js`. Chrome/Edge/Samsung: native install, then `/app`. iOS: Share → Add to Home Screen (the page they are already on). Toolbar install on **verodus.com** is the same app.

## 3. Two header lines (Dashboard + Trade)

Without these, `/app` is a blank iframe.

Dashboard and Trade `next.config` headers (or CDN):

```
Content-Security-Policy: frame-ancestors 'self' https://www.verodus.com https://verodus.com
```

Remove `X-Frame-Options: DENY`. Snippets: `dashboard/frame-headers.js`, `trade/frame-headers.js`.

## 4. Google login

Keep **Continue with Google** as a **popup**. If it sets `window.top.location` to `dashboard.verodus.com`, the bar comes back. After OAuth, land in the iframe or on `https://www.verodus.com/app`.

## Verify (15 minutes)

1. Uninstall any old Verodus icon (`chrome://apps`, Android long-press, iOS Remove App).
2. Open `https://www.verodus.com` in Chrome (desktop or Android).
3. Toolbar → **Install Verodus**, or tap **for android**.
4. Open the installed app. Address must be `https://www.verodus.com/app`. No X / URL / Verodus CRM strip.
5. Click **Platform5**, then **TradeHub**. The strip must not appear.
6. iPhone: Safari on verodus.com → Share → Add to Home Screen → same check.

If step 4 still shows the strip, the icon was installed from Dashboard/Trade, or `/app` is not what `start_url` points at.

## Leave for later

- `lock-origin.js` (toolbar install while already on Dashboard)
- Same-origin `/p5/{id}` routes on Dashboard
- Reverse-proxy everything onto one host (fastest long-term, bigger change)

Firefox desktop cannot hide its URL bar. Everything else that can install a PWA follows this.
