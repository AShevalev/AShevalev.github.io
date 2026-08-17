# Dashboard is the app (the practical path)

The installed app is **`https://dashboard.verodus.com`**. Every CRM route is the same host, so Accounts, Journal, Payouts, Settings, etc. never draw the Chrome bar.

The only other host is **`https://trade.verodus.com`** (TradeHub + Platform 5). Those two buttons must not top-level-redirect there. Iframe them from Dashboard.

Do **not** install from verodus.com. A landing-page PWA makes Dashboard look like a website (the X / URL strip). Landing pills should **open Dashboard**; install happens there (toolbar or a button on `/dashboard`).

```
chrome toolbar / install on dashboard.verodus.com
  → /dashboard, /accounts, /journal, …     same origin, no bar
  → /tradehub/{accountId}                  iframe trade.verodus.com/tradehub/{id}
  → /p5/{accountId}                        iframe trade.verodus.com/p5/{id}
```

Google login stays on dashboard.verodus.com (no iframe around the CRM), so OAuth is normal.

## 1. Make Dashboard installable

On `dashboard.verodus.com`:

| File | Role |
|---|---|
| `dashboard/manifest.webmanifest` → `/manifest.webmanifest` | `start_url`: `/dashboard`, `scope`: `/`, `display`: `standalone` |
| `dashboard/sw.js` → `/sw.js` | so Chrome will install |
| `dashboard/icons/*` → `/icons/` | PNG 192 and 512 |
| `dashboard/head.html` / `layout-snippet.jsx` | Apple tags + manifest link |

```html
<script>
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script src="/js/install.js"></script>
```

Copy `dashboard/install.js` to `/js/install.js`. Chrome toolbar **Install Verodus** on any `dashboard.verodus.com/...` page is the same app (`scope: "/"`).

## 2. TradeHub / Platform 5 — same-origin hrefs

On each account card, stop using `https://trade.verodus.com/...` and `target="_blank"`:

```jsx
<a href={`/p5/${account.id}`}>Platform5</a>
<a href={`/tradehub/${account.id}`}>TradeHub</a>
```

Copy:

- `dashboard/PlatformFrame.jsx` → `components/PlatformFrame.jsx`
- `dashboard/app/p5/[accountId]/page.jsx`
- `dashboard/app/tradehub/[accountId]/page.jsx`

On `trade.verodus.com`:

```
Content-Security-Policy: frame-ancestors 'self' https://dashboard.verodus.com
```

Remove `X-Frame-Options: DENY`. Snippet: `trade/frame-headers.js`.

Optional stopgap until the buttons are changed: `dashboard/intercept-launches.js` rewrites leftover trade links.

## 3. Landing pills (verodus.com)

They cannot install Dashboard (wrong host). They should only send people there:

```html
<a class="v-store-pill" href="https://dashboard.verodus.com/dashboard">for android</a>
<a class="v-store-pill" href="https://dashboard.verodus.com/dashboard">for iOS</a>
```

Do not ship a PWA on www for this model (no `start_url: /`, no install of the marketing site).

## Verify

1. Uninstall old Verodus icons.
2. Open `https://dashboard.verodus.com/dashboard` in Chrome → Install Verodus.
3. Open the app: CRM with no X / URL strip. Click Journal, Accounts — still no strip.
4. Click Platform5, then TradeHub — still no strip. URL stays `https://dashboard.verodus.com/p5/...` or `/tradehub/...`.

iPhone: Safari on **dashboard.verodus.com** → Share → Add to Home Screen (not on the marketing site).
