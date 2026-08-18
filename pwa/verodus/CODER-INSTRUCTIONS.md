# Verodus — coder instructions (install from Dashboard)

**Open this first.** Then copy files from the matching folders in the zip.

**Do not iframe anything.** Live Platform5 / TradeHub buttons stay as they are. This pack only adds install UI.

There are three hosts. Only **Dashboard** is the CRM installed app.

| Host | Role |
|---|---|
| `https://dashboard.verodus.com` | The CRM app. Install here. |
| `https://www.verodus.com` | Marketing site only. Pills open a modal. Do **not** make this a PWA. |
| `https://trade.verodus.com` | TradeHub + Platform 5. Optional second app. Install from a **modal + link** on Dashboard Platforms, not by wrapping trade in the CRM. |

---

## Do not

- Do not iframe TradeHub, Platform 5, or the CRM.
- Do not link landing pills to Play Store or App Store.
- Do not install a PWA from `www.verodus.com` (no landing `manifest`, no landing `sw.js`).
- Do not set a PWA `start_url` that contains an account cuid.
- Do not auto-install the trading app from Dashboard. Chrome can only install the origin you are on.

---

## 1. Landing — `www.verodus.com`

**Goal:** **for android** / **for iOS** open a modal:

> Install from **Dashboard → Trading Resources → Platforms**

Keep the existing pill look (Android / Apple SVGs). Change only the href, attributes, CSS, and script.

| Zip file | Put on the site |
|---|---|
| `landing/css/platforms-modal.css` | `/css/platforms-modal.css` |
| `landing/js/install.js` | `/js/install.js` |
| `landing/store-buttons.html` | splice into the homepage store-pill markup |

```html
<link rel="stylesheet" href="/css/platforms-modal.css" />

<a class="v-store-pill"
   data-open-platforms-modal
   href="https://dashboard.verodus.com/trading-resources/platforms"
   aria-label="Install Verodus on Android from the dashboard">
  <!-- existing Android SVG -->
  <span>for android</span>
</a>

<a class="v-store-pill"
   data-open-platforms-modal
   href="https://dashboard.verodus.com/trading-resources/platforms"
   aria-label="Install Verodus on iPhone from the dashboard">
  <!-- existing Apple SVG -->
  <span>for iOS</span>
</a>

<script src="/js/install.js"></script>
```

No-JS fallback: the `href` opens the Dashboard Platforms page.

Remove any `play.google.com` / `apps.apple.com` hrefs on these pills. Remove any landing-page `manifest.json` / service worker that was added to install `www`.

`landing/home-pills-demo.html` is a local preview of the modal. Not for production.

---

## 2. Dashboard — make it installable

**Goal:** Chrome / Edge can install `https://dashboard.verodus.com` as a standalone app. `start_url` is `/dashboard`. `scope` is `/`.

| Zip file | Put here |
|---|---|
| `dashboard/public/manifest.webmanifest` | `public/manifest.webmanifest` |
| `dashboard/public/sw.js` | `public/sw.js` |
| `dashboard/public/js/install.js` | `public/js/install.js` |
| `dashboard/public/css/install.css` | `public/css/install.css` |
| `dashboard/public/icons/*` | `public/icons/` |

Icons must be **PNG** (192 and 512). WebP-only will not install.

Merge `dashboard/app/layout-snippet.jsx` into the existing root layout.

Required `<head>` (Next metadata API is fine):

- `theme-color`: `#07003B`
- `apple-mobile-web-app-capable`: `yes`
- `apple-mobile-web-app-title`: `Verodus`
- `apple-touch-icon`: `/icons/apple-touch-icon.png`
- `manifest`: `/manifest.webmanifest`
- stylesheet: `/css/install.css`
- script: `/js/install.js` (this file also registers `/sw.js`)

`dashboard/public/js/install.js` is **not** the same file as `landing/js/install.js`. Same path name, different host, different behaviour.

---

## 3. Dashboard — Trading Resources → Platforms

Add **Platforms** under **Trading Resources**, next to Economic Calendar and News. Five cards: **Android**, **Mobile**, **Desktop**, **Safari**, **Trading**.

```js
{ title: "Platforms", href: "/trading-resources/platforms" }
```

If Economic Calendar / News already use a different prefix, match that prefix. The landing modal’s **Open dashboard** button goes to:

`https://dashboard.verodus.com/trading-resources/platforms`

If you change the path, change `landing/js/install.js` (`HREF`) and the pill `href`s to match.

Suggested icon: `MonitorSmartphone` from lucide-react.

| Zip file | Put here |
|---|---|
| `dashboard/components/PlatformsPage.jsx` | `components/PlatformsPage.jsx` (or `src/components/`) |
| `dashboard/components/platforms.css` | next to `PlatformsPage.jsx` |
| `dashboard/app/trading-resources/platforms/page.jsx` | `app/trading-resources/platforms/page.jsx` |

The five buttons use `data-install-app` + `data-install-platform="android|mobile|desktop|safari|trading"`:

- **Android** — Chrome / Edge / Samsung install prompt, else menu → Install app
- **Mobile** — iPhone / iPad Share → Add to Home Screen
- **Desktop** — Chrome / Edge address-bar install (Firefox desktop cannot install PWAs)
- **Safari** — Mac only. File → **Add to Dock** (Safari 17+ / macOS 14 Sonoma or newer)
- **Trading** — opens a **modal** with steps and **Open TradeHub** → `https://trade.verodus.com/dashboard`. Does not auto-install. User installs on that origin in a normal browser tab.

Do not send these cards to Play or App Store.

Leave existing Platform5 / TradeHub account-card buttons unchanged.

---

## 4. Verify

1. Uninstall old Verodus / “Verodus CRM” home-screen icons.
2. **www.verodus.com** — tap **for android** / **for iOS** → modal with Dashboard → Trading Resources → Platforms. **Open dashboard**.
3. Sidebar: **Trading Resources → Platforms**. Install **Android**, **Mobile**, **Desktop**, or **Safari**.
4. Open the installed CRM: Dashboard, Accounts, Journal stay on `dashboard.verodus.com`.
5. **Trading** card → modal → **Open TradeHub** → `https://trade.verodus.com/dashboard`. Then Install / Add to Dock on that page.
6. iPhone: Safari on **dashboard.verodus.com/trading-resources/platforms** → Share → Add to Home Screen. Not on the marketing site.
7. Safari on a Mac: File → Add to Dock on Dashboard for the CRM; same idea on `trade.verodus.com/dashboard` for trading.

Firefox desktop cannot hide its URL bar and cannot install PWAs. Use Chrome or Edge on desktop.

---

## File map (zip → destination)

```
INSTRUCTIONS.md                          ← this document

landing/css/platforms-modal.css          →  www  /css/platforms-modal.css
landing/js/install.js                    →  www  /js/install.js
landing/store-buttons.html               →  www  homepage pills
landing/home-pills-demo.html             →  local preview only

dashboard/public/manifest.webmanifest    →  dashboard public/manifest.webmanifest
dashboard/public/sw.js                   →  dashboard public/sw.js
dashboard/public/js/install.js           →  dashboard public/js/install.js
dashboard/public/css/install.css         →  dashboard public/css/install.css
dashboard/public/icons/*                 →  dashboard public/icons/
dashboard/app/layout-snippet.jsx         →  merge into app/layout
dashboard/app/trading-resources/platforms/page.jsx
dashboard/components/PlatformsPage.jsx
dashboard/components/platforms.css
dashboard/sidebar-trading-resources.jsx  →  merge into existing sidebar
dashboard/head.html                      →  reference for <head> tags
```
