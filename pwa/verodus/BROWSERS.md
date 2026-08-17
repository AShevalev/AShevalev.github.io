# Every browser: Dashboard, TradeHub, Platform 5 without the top bar

That strip with the **X**, the URL, and **Verodus CRM** is browser chrome. It is not a Verodus header. CSS cannot hide it.

It appears when:

1. The app was **not** installed from `dashboard.verodus.com`, or
2. The top-level URL **changes host** (Dashboard → `trade.verodus.com`)

Your screenshot is (1) or (2) on **desktop Chrome**. The same bar appears on Android Chrome. The fix is the same everywhere the browser can run a standalone app: **install Dashboard, then never leave that origin.**

## What each browser can do

| Browser | Hide the normal address bar | Hide the X / URL “website” bar when switching Dashboard ↔ TradeHub ↔ P5 |
|---|---|---|
| **Chrome / Edge / Opera / Brave — Android** | Yes, after Install app | Yes, if top-level URL stays on `dashboard.verodus.com` |
| **Chrome / Edge / Brave — desktop** | Yes, after Install app / Install page as app | Yes, same rule. This is the bar in your screenshot. |
| **Samsung Internet** | Yes, after Add page to Home screen | Yes, same rule |
| **Safari — iPhone / iPad** | Yes, after Share → Add to Home Screen **on dashboard.verodus.com** | Yes, with the iframe routes. A top-level open of `trade.verodus.com` always shows Safari chrome (no `scope_extensions`) |
| **Chrome / Edge / Firefox — iOS** | Same as Safari (Share → Add to Home Screen), iOS 16.4+ | Same as Safari. Install must happen on the dashboard origin |
| **Safari — Mac (Sonoma+)** | File → Add to Dock, on dashboard | Yes, if you never navigate to another host |
| **Firefox — Android** | Menu → Install / Add app to Home screen | Yes, if you stay on dashboard (iframe). No native install prompt |
| **Firefox — desktop** | **No.** Firefox cannot install a PWA. The Firefox URL bar always stays | N/A. Same-origin still avoids a second “out of site” UI, but you cannot make Firefox look like a native app |
| **In-app browsers (Instagram, Telegram, Gmail)** | No. They are Custom Tabs | Do not use them. Open in Chrome or Safari, then install |

There is no API that removes Firefox desktop’s URL bar, or a Custom Tab bar. Those are the host app.

## One code path for every browser that *can* hide chrome

```
Install https://dashboard.verodus.com/dashboard as the app

Account card:
  Platform5  →  /p5/{accountId}          (still dashboard.verodus.com)
  TradeHub   →  /tradehub/{accountId}    (still dashboard.verodus.com)

Those routes render a full-viewport iframe of:
  https://trade.verodus.com/p5/{accountId}
  https://trade.verodus.com/tradehub/{accountId}
```

The iframe is a child document. The standalone window follows the parent URL, so Chrome/Edge/Safari never draw the out-of-scope bar.

## Steps

### 1. Remove the current desktop / phone install

The bar on Dashboard itself means Chrome thinks `dashboard.verodus.com` is **outside** the installed app (usually you installed `www.verodus.com` or TradeHub).

- Desktop Chrome: `chrome://apps` → remove Verodus → reopen from `https://dashboard.verodus.com/dashboard`
- Android: long-press the icon → uninstall / remove
- iOS: long-press the Home Screen icon → Remove App

### 2. Make Dashboard a real standalone app

Copy onto `dashboard.verodus.com`:

- `manifest.webmanifest` (`display: standalone`, `start_url: /dashboard`)
- `sw.js`, PNG icons, `head.html` / `layout-snippet.jsx`

### 3. Change the two account-card buttons

```jsx
import AccountLaunchButtons from "@/components/AccountLaunchButtons";

<AccountLaunchButtons accountId={account.id} />
```

Or keep your existing labels and only change `href`:

```jsx
<a href={`/p5/${account.id}`}>Platform5</a>
<a href={`/tradehub/${account.id}`}>TradeHub</a>
```

Do **not** use:

```js
window.open(`https://trade.verodus.com/p5/${id}`)
window.location.href = `https://trade.verodus.com/tradehub/${id}`
<a href="https://trade.verodus.com/..." target="_blank">
router.push("https://trade.verodus.com/...")
redirect("https://trade.verodus.com/...")
```

### 4. Add the iframe routes

Copy `PlatformFrame.jsx`, `app/tradehub/[accountId]/page.jsx`, `app/p5/[accountId]/page.jsx`.

On `trade.verodus.com` allow framing:

```
Content-Security-Policy: frame-ancestors 'self' https://dashboard.verodus.com
```

### 5. Install from Dashboard, per browser

**Chrome / Edge — desktop:** open `https://dashboard.verodus.com/dashboard` → install icon in the address bar, or ⋮ → **Install Verodus** → open the installed app (not the tab).

**Chrome / Edge / Samsung — Android:** same URL → ⋮ → **Install app** / **Add to Home screen**. Or tap the homepage **for android** pill after it points at `?install=1`.

**Safari iPhone / iPad:** open that URL **in Safari** (not Chrome) → Share → **Add to Home Screen**.

**Firefox Android:** ⋮ → **Install** / **Add app to Home screen**.

**Firefox desktop:** cannot hide the bar. Use Chrome or Edge if you need an app window.

### 6. Confirm

In the installed window, `window.matchMedia('(display-mode: standalone)').matches` is `true`.

Click **Platform5**, then **TradeHub**. The X / URL strip must not return. The address stays `https://dashboard.verodus.com/...`.
