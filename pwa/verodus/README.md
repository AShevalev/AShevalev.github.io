# Hide the Chrome bar on Dashboard, TradeHub, and Platform 5

That X / URL / **Verodus CRM** strip is browser chrome when the window leaves the installed origin, including **desktop Chrome**. CSS cannot hide it.

Per-browser behavior and install steps: **[BROWSERS.md](BROWSERS.md)**.

Keep the window on **one origin**. Embed TradeHub and Platform 5; do not redirect to them.

```
https://dashboard.verodus.com/dashboard              ← CRM (installed app)
https://dashboard.verodus.com/tradehub/{accountId}   ← TradeHub (iframe)
https://dashboard.verodus.com/p5/{accountId}         ← Platform 5 (iframe)
```

The iframe still loads `https://trade.verodus.com/...`. That is a subdocument. Chrome’s bar only cares about the **top-level** URL, which stays on `dashboard.verodus.com`.

## Do this in the dashboard app

### 1. Stop sending Chrome to `trade.verodus.com`

Replace every launch (links, `window.location`, `window.open`, Next `redirect()`):

```js
// before — this is what draws the bar
window.location.href = `https://trade.verodus.com/tradehub/${accountId}`;
window.location.href = `https://trade.verodus.com/p5/${accountId}`;

// after — same app window, no bar
window.location.href = `/tradehub/${accountId}`;
window.location.href = `/p5/${accountId}`;
```

Drop `pwa/verodus/dashboard/intercept-launches.js` on the dashboard layout as a stopgap so existing `https://trade.verodus.com/...` links are rewritten.

### 2. Add same-origin routes that iframe the terminals

Copy:

| This repo | Dashboard Next.js app |
|---|---|
| `dashboard/PlatformFrame.jsx` | `components/PlatformFrame.jsx` |
| `dashboard/app/tradehub/[accountId]/page.jsx` | `app/tradehub/[accountId]/page.jsx` |
| `dashboard/app/p5/[accountId]/page.jsx` | `app/p5/[accountId]/page.jsx` |
| `dashboard/same-origin.js` | helper for link building |
| `dashboard/manifest.webmanifest` + `sw.js` + icons + `head.html` | so Chrome installs Dashboard as standalone |

`start_url` stays `/dashboard`. Account ids stay in `/tradehub/{id}` and `/p5/{id}` after launch, never in `start_url`.

Wire the account-card **Platform5** / **TradeHub** buttons with `AccountLaunchButtons.jsx` (or `href={launchPath('p5', id)}`). Load `InAppLaunches.jsx` from the root layout so leftover `trade.verodus.com` links are rewritten.

### 3. Let Dashboard frame TradeHub / P5

On `trade.verodus.com` (`next.config.mjs`):

```js
async headers() {
  return [{
    source: "/:path*",
    headers: [{
      key: "Content-Security-Policy",
      value: "frame-ancestors 'self' https://dashboard.verodus.com",
    }],
  }];
}
```

Remove `X-Frame-Options: DENY` if it is set. Snippet: `pwa/verodus/trade/frame-headers.js`.

### 4. Homepage Android / iOS pills

Point both at `https://dashboard.verodus.com/dashboard?install=1` — not Play Store / App Store. See `pwa/verodus/www/store-buttons.html`.

Install the PWA **on the dashboard origin**. Opening the marketing site and then redirecting to Dashboard is the same host-change bug.

## What not to do

- HTTP 302/307 from dashboard → `trade.verodus.com`
- `target="_blank"` or Chrome Custom Tabs
- Three separate home-screen shortcuts that bounce between hosts
- Putting a cuid in `start_url`

## Check

1. Install from `https://dashboard.verodus.com/dashboard?install=1`.
2. Open Verodus from the home screen — no X / URL bar on the CRM.
3. Open TradeHub, then Platform 5. The address stays `dashboard.verodus.com/...`. The bar must not return.
