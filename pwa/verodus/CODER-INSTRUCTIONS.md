# Verodus — coder instructions (install from Dashboard)

**Open this first.** Then copy files from the matching folders in the zip.

There are three hosts. Only **Dashboard** is the installed app.

| Host | Role |
|---|---|
| `https://dashboard.verodus.com` | The app. Install here. All CRM routes stay here. |
| `https://www.verodus.com` | Marketing site only. Pills open a modal. Do **not** make this a PWA. |
| `https://trade.verodus.com` | TradeHub + Platform 5. On Chrome / Edge, iframe from Dashboard (never a top-level jump from the installed app). On Safari for Mac, open at the top level — there is no URL bar. |

Chrome’s X / URL / “Verodus CRM” strip appears when the **top-level** URL changes host (`www` ↔ `dashboard` ↔ `trade`). CSS cannot hide it. Same-origin Dashboard routes are fine.

---

## Do not

- Do not link landing pills to Play Store or App Store.
- Do not install a PWA from `www.verodus.com` (no landing `manifest`, no landing `sw.js`). That makes Dashboard look like a website.
- Do not use `href="https://trade.verodus.com/..."`, `target="_blank"`, or `window.open` for Platform 5 / TradeHub **on Chrome / Edge**. Use `/p5/{id}` and `/tradehub/{id}` so Dashboard can iframe them. Safari on a Mac is handled in `PlatformFrame` (top-level trade is OK).
- Do not set a PWA `start_url` that contains an account cuid.
- Do not iframe the CRM around Google login. OAuth stays on `dashboard.verodus.com`.

---

## 1. Landing — `www.verodus.com`

**Goal:** **for android** / **for iOS** open a modal:

> Install from **Dashboard → Trading Resources → Platforms**

Keep the existing pill look (Android / Apple SVGs). Change only the href, attributes, CSS, and script.

### Copy these files

| Zip file | Put on the site |
|---|---|
| `landing/css/platforms-modal.css` | `/css/platforms-modal.css` |
| `landing/js/install.js` | `/js/install.js` |
| `landing/store-buttons.html` | splice into the homepage store-pill markup |

### Markup (keep your existing SVGs and i18n spans)

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

### Copy to `public/` (Next.js static files)

| Zip file | Put here |
|---|---|
| `dashboard/public/manifest.webmanifest` | `public/manifest.webmanifest` |
| `dashboard/public/sw.js` | `public/sw.js` |
| `dashboard/public/js/install.js` | `public/js/install.js` |
| `dashboard/public/css/install.css` | `public/css/install.css` |
| `dashboard/public/icons/*` | `public/icons/` |

Icons must be **PNG** (192 and 512). WebP-only will not install.

### Root layout (`app/layout.tsx` or `.jsx`)

Merge with the existing layout. See `dashboard/app/layout-snippet.jsx`.

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

**Goal:** Sidebar item **Platforms** under **Trading Resources**, next to Economic Calendar and News. Five cards: **Android**, **Mobile**, **Desktop**, **Safari**, **Trading**.

### Sidebar

Edit the existing Trading Resources children. Snippet: `dashboard/sidebar-trading-resources.jsx`.

```js
{ title: "Platforms", href: "/trading-resources/platforms" }
```

If Economic Calendar / News already use a different prefix, match that prefix and put the page on the matching route. The landing modal’s **Open dashboard** button goes to:

`https://dashboard.verodus.com/trading-resources/platforms`

If you change the path, change `landing/js/install.js` (`HREF`) and the pill `href`s to match.

Suggested icon: `MonitorSmartphone` from lucide-react (or equivalent).

### Page files

| Zip file | Put here |
|---|---|
| `dashboard/components/PlatformsPage.jsx` | `components/PlatformsPage.jsx` (or `src/components/`) |
| `dashboard/components/platforms.css` | next to `PlatformsPage.jsx` |
| `dashboard/app/trading-resources/platforms/page.jsx` | `app/trading-resources/platforms/page.jsx` |

If the app uses `@/` → `src/`, keep that alias. Rename to `.tsx` if the repo is TypeScript.

The five buttons use `data-install-app` + `data-install-platform="android|mobile|desktop|safari|trading"`. `/js/install.js` handles the prompt:

- **Android** — Chrome / Edge / Samsung `beforeinstallprompt`, else menu → Install app
- **Mobile** — iPhone / iPad Share → Add to Home Screen
- **Desktop** — Chrome / Edge address-bar install (Firefox desktop cannot install PWAs)
- **Safari** — Mac only. File → **Add to Dock** (Safari 17+ / macOS 14 Sonoma or newer). Creates a Dock web app.
- **Trading** — opens a **modal** with steps and a link to `https://trade.verodus.com/tradehub?source=pwa`. Does **not** auto-install. User opens TradeHub in a normal tab, then Install / Add to Dock there.

Do not send these cards to Play or App Store. The iframe change in section 4 is optional and can wait.

---

## 4. Dashboard — TradeHub / Platform 5 (optional later)

Skip this section until you are ready. Live Platform5 / TradeHub buttons can stay as they are.

**If you do it:** On Chrome / Edge, account-card buttons stay on `dashboard.verodus.com` and Dashboard routes **iframe** `trade.verodus.com`.

**Safari on a Mac is different:** there is no URL bar on Verodus pages. `PlatformFrame` and `intercept-launches` skip the iframe and open `trade.verodus.com` at the top level. Do not force an iframe in Safari.

### Account cards — change the hrefs

```jsx
<a href={`/p5/${account.id}`}>Platform5</a>
<a href={`/tradehub/${account.id}`}>TradeHub</a>
```

Drop-in: `dashboard/components/AccountLaunchButtons.jsx`  
If the click is in JS: `dashboard/components/useLaunchPlatform.js` (`router.push`, not `window.open`).

### New Dashboard routes

| Zip file | Put here |
|---|---|
| `dashboard/components/PlatformFrame.jsx` | `components/PlatformFrame.jsx` (if `lock-origin.js` is beside it, the import is `./lock-origin.js`) |
| `dashboard/app/p5/[accountId]/page.jsx` | `app/p5/[accountId]/page.jsx` |
| `dashboard/app/tradehub/[accountId]/page.jsx` | `app/tradehub/[accountId]/page.jsx` |

Next.js 15+: `params` may be a Promise — `const { accountId } = await params`.

If the window is already inside an iframe, `PlatformFrame` navigates that frame to trade (no nested iframes).

On Safari for Mac, `PlatformFrame` uses `location.replace` to `https://trade.verodus.com/...` instead of an iframe.

### Stopgap (until every leftover trade link is gone)

Put these in the **same** `components/` folder:

| Zip file | Put here |
|---|---|
| `dashboard/components/same-origin.js` | `components/same-origin.js` |
| `dashboard/components/intercept-launches.js` | `components/intercept-launches.js` |
| `dashboard/components/lock-origin.js` | `components/lock-origin.js` |
| `dashboard/components/lock-origin-entry.js` | `components/lock-origin-entry.js` |
| `dashboard/components/InAppLaunches.jsx` | `components/InAppLaunches.jsx` |

Mount `<InAppLaunches />` once in the root layout.

---

## 5. Trade — allow the iframe

On **`trade.verodus.com`** (TradeHub + Platform 5):

```
Content-Security-Policy: frame-ancestors 'self' https://dashboard.verodus.com
```

**Remove** `X-Frame-Options: DENY` (it blocks the iframe even if CSP is correct).

Snippet: `trade/frame-headers.js`.

If trade is Cloudflare / nginx / a Node server, set the same header there.

---

## 6. Verify

1. Uninstall old Verodus / “Verodus CRM” home-screen icons.
2. **www.verodus.com** — tap **for android** / **for iOS** → modal with Dashboard → Trading Resources → Platforms. **Open dashboard**.
3. Sidebar: **Trading Resources → Platforms**. Install **Android**, **Mobile**, **Desktop**, or **Safari** (Chrome toolbar Install also works while the tab is on dashboard).
4. Open the installed app: Dashboard, Accounts, Journal — **no** X / URL strip.
5. Platform5, then TradeHub — **no** strip. Address stays `https://dashboard.verodus.com/p5/...` or `/tradehub/...`.
6. iPhone: Safari on **dashboard.verodus.com/trading-resources/platforms** → Share → Add to Home Screen. Not on the marketing site.

Firefox desktop cannot hide its own URL bar and cannot install PWAs. Use Chrome or Edge on desktop.

Safari on a Mac: File → Add to Dock (macOS 14+). TradeHub / Platform 5 stay top-level — do not iframe.

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
dashboard/app/p5/[accountId]/page.jsx
dashboard/app/tradehub/[accountId]/page.jsx
dashboard/components/*                   →  dashboard components/ (or src/components/)
dashboard/sidebar-trading-resources.jsx  →  merge into existing sidebar
dashboard/head.html                      →  reference for <head> tags

trade/frame-headers.js                   →  trade.verodus.com response headers
```
