# Hide the browser bar on Verodus (Dashboard, TradeHub, Platform 5)

The gray bar with the **X**, **Verodus CRM**, and `dashboard.verodus.com` is Chrome’s **out-of-scope / Custom Tab chrome**. It is not a Verodus header. It appears when the page is opened as a website, not as an installed standalone app.

## What is going wrong today

| Piece | Live today | Effect |
|---|---|---|
| Homepage pills | `https://play.google.com` and `https://apps.apple.com` | Those are store homepages, not Verodus. |
| `www.verodus.com` PWA | `start_url: "/"`, WebP icons, **no service worker** | Home-screen icon opens the **marketing site**. |
| `dashboard.verodus.com` | **No manifest, no Apple tags, no SW** | Android cannot install it as standalone, so you get the bar. |
| `trade.verodus.com` | Has a TradeHub manifest | Fine as a terminal, but the CRM bar is a dashboard-origin problem. |
| `scope_extensions` | Declared on www | Association file id is `https://verodus.com/` while people use `https://www.verodus.com/` — association fails, so Dashboard/Trade look out of scope. |
| Account URLs | `/tradehub/{cuid}`, `/p5/{cuid}` | Must **not** be `start_url`. Every user would pin one account. |

## The rule

Install **one** app: **Dashboard**.

```
Home screen icon
  → https://dashboard.verodus.com/dashboard
      → TradeHub  https://trade.verodus.com/tradehub/{accountId}
      → Platform 5 https://trade.verodus.com/p5/{accountId}
```

- `display: standalone` removes the top bar on Dashboard.
- `scope_extensions` + origin association keeps TradeHub and Platform 5 **in the same Android window** (same origin `trade.verodus.com`, different paths).
- Account ids stay in the path after login. The PWA `start_url` is always `/dashboard`.

iOS does not support `scope_extensions`. Add to Home Screen **on dashboard.verodus.com**. Opening Trade/P5 on iOS may still use Safari unless you later proxy those routes onto the dashboard origin.

## Deploy

### 1. Dashboard (`dashboard.verodus.com`) — this removes the CRM bar

Copy into the Next app `public/` folder:

| This repo | On dashboard |
|---|---|
| `pwa/verodus/dashboard/manifest.webmanifest` | `/manifest.webmanifest` |
| `pwa/verodus/dashboard/sw.js` | `/sw.js` |
| `pwa/verodus/dashboard/icons/*` | `/icons/` |
| `pwa/verodus/dashboard/.well-known/web-app-origin-association` | `/.well-known/web-app-origin-association` |

Paste `pwa/verodus/dashboard/head.html` into the root layout. Register the worker and CTA with `pwa/verodus/dashboard/install-entry.js` (or the same `bindInstallCta` call).

Serve the association file as `application/json` from the **origin root**, not behind a locale prefix.

### 2. Trade (`trade.verodus.com`) — TradeHub **and** Platform 5

Both products are on this origin, so one association covers:

- `/tradehub/{accountId}`
- `/p5/{accountId}`

Put `pwa/verodus/trade/.well-known/web-app-origin-association` at `/.well-known/web-app-origin-association`.

Optional: replace the live TradeHub manifest `start_url` with `/tradehub?source=pwa` (see `pwa/verodus/trade/manifest.webmanifest`). Never use a cuid in `start_url`. After install, redirect `/tradehub` to the signed-in user’s last account.

### 3. Homepage pills (`www.verodus.com`)

Replace the Play / App Store `href`s. Keep the pill CSS.

See `pwa/verodus/www/store-buttons.html` and `store-buttons.js`.

Both buttons go to:

`https://dashboard.verodus.com/dashboard?install=1`

That page owns the real install prompt (Android) or the Share → Add to Home Screen sheet (iOS).

Also replace `/.well-known/web-app-origin-association` and, if you keep a marketing manifest, use `pwa/verodus/www/manifest.json` (`id` must be `https://www.verodus.com/`, PNG icons). People who already installed the marketing PWA should delete it and install from Dashboard.

### 4. Launch TradeHub / P5 from the CRM **in the same window**

```html
<a href="https://trade.verodus.com/tradehub/ACCOUNT_ID">TradeHub</a>
<a href="https://trade.verodus.com/p5/ACCOUNT_ID">Platform 5</a>
```

Do **not** use `target="_blank"`, `window.open`, or a Chrome Custom Tab Intent. Those recreate the bar even when the PWA is installed.

## Check that the bar is gone

1. On Android Chrome, open `https://dashboard.verodus.com/dashboard?install=1` and install.
2. Close Chrome. Open **Verodus** from the home screen.
3. There should be no X / URL row. Status bar only.
4. From an account, tap TradeHub, then Platform 5. Android should stay in the app window.
5. iOS: Safari → Share → Add to Home Screen **while on dashboard.verodus.com**.
