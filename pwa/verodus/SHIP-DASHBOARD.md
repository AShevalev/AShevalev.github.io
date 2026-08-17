# Dashboard is the app (the practical path)

The installed app is **`https://dashboard.verodus.com`**. Every CRM route is the same host, so Accounts, Journal, Payouts, Settings, etc. never draw the Chrome bar.

The only other host is **`https://trade.verodus.com`** (TradeHub + Platform 5). Those two buttons must not top-level-redirect there. Iframe them from Dashboard.

Do **not** install from verodus.com. A landing-page PWA makes Dashboard look like a website (the X / URL strip). Landing pills open a **modal**: install from **Dashboard → Trading Resources → Platforms**.

```
chrome toolbar / install on dashboard.verodus.com
  → /dashboard, /accounts, /journal, …                    same origin, no bar
  → /trading-resources/platforms                          Android / Mobile / Desktop
  → /tradehub/{accountId}                                 iframe trade.verodus.com/tradehub/{id}
  → /p5/{accountId}                                       iframe trade.verodus.com/p5/{id}
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
| `dashboard/install.js` → `/js/install.js` | Platforms CTAs + `beforeinstallprompt` |
| `dashboard/install.css` → `/css/install.css` | install instruction sheet |

```html
<link rel="stylesheet" href="/css/install.css" />
<script>
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
</script>
<script src="/js/install.js"></script>
```

Chrome toolbar **Install Verodus** on any `dashboard.verodus.com/...` page is the same app (`scope: "/"`).

## 2. Trading Resources → Platforms

Add **Platforms** under Trading Resources (next to Economic Calendar and News).

| File | Role |
|---|---|
| `dashboard/sidebar-trading-resources.jsx` | nav child `{ title: "Platforms", href: "/trading-resources/platforms" }` |
| `dashboard/PlatformsPage.jsx` + `platforms.css` | Android / Mobile / Desktop cards |
| `dashboard/app/trading-resources/platforms/page.jsx` | Next.js route |

The three cards call `[data-install-app][data-install-platform]`:

- **Android** — Chrome/Edge/Samsung install prompt (or menu → Install app)
- **Mobile** — iPhone/iPad Share → Add to Home Screen
- **Desktop** — Chrome/Edge address-bar install (Firefox desktop cannot install PWAs)

Stay on `dashboard.verodus.com`. Do not send people to Play or App Store.

## 3. TradeHub / Platform 5 — same-origin hrefs

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

## 4. Landing pills (verodus.com)

They cannot install Dashboard (wrong host). They open a modal that says to install from **Dashboard → Trading Resources → Platforms**.

```html
<link rel="stylesheet" href="/css/platforms-modal.css" />
<a class="v-store-pill" data-open-platforms-modal
   href="https://dashboard.verodus.com/trading-resources/platforms">for android</a>
<a class="v-store-pill" data-open-platforms-modal
   href="https://dashboard.verodus.com/trading-resources/platforms">for iOS</a>
<script src="/js/install.js"></script>
```

Copy `www/install.js` → `/js/install.js` and `www/platforms-modal.css` → `/css/platforms-modal.css`. Markup: `www/store-buttons.html`.

No-JS fallback: the `href` opens the dashboard Platforms page.

Do not ship a PWA on www for this model (no `start_url: /`, no install of the marketing site). Do not link the pills to Play or App Store.

## Verify

1. Uninstall old Verodus icons.
2. On verodus.com, tap **for android** / **for iOS** → modal with Dashboard → Trading Resources → Platforms. Open dashboard.
3. In the CRM sidebar: Trading Resources → Platforms. Install Android, Mobile, or Desktop.
4. Open the installed app: CRM with no X / URL strip. Click Journal, Accounts — still no strip.
5. Click Platform5, then TradeHub — still no strip. URL stays `https://dashboard.verodus.com/p5/...` or `/tradehub/...`.

iPhone: Safari on **dashboard.verodus.com/trading-resources/platforms** → Share → Add to Home Screen (not on the marketing site).
