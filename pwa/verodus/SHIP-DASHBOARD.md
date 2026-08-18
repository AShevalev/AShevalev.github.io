# Dashboard is the app (no iframe)

The CRM installed app is **`https://dashboard.verodus.com`**. Landing pills point people at **Dashboard → Trading Resources → Platforms**. Trading is an optional second app: a **modal + link** to `https://trade.verodus.com/dashboard`. **Do not iframe** TradeHub or Platform 5.

Do **not** install from verodus.com. A landing-page PWA makes Dashboard look like a website.

```
chrome toolbar / install on dashboard.verodus.com
  → /dashboard, /accounts, /journal, …     same origin
  → /trading-resources/platforms            Dashboard + Verodus Trading (same install tables)
```

Google login stays on dashboard.verodus.com.

## 1. Make Dashboard installable

| File | Role |
|---|---|
| `dashboard/manifest.webmanifest` → `/manifest.webmanifest` | `start_url`: `/dashboard`, `scope`: `/`, `display`: `standalone` |
| `dashboard/sw.js` → `/sw.js` | so Chrome will install |
| `dashboard/icons/*` → `/icons/` | PNG 192 and 512 |
| `dashboard/head.html` / `layout-snippet.jsx` | Apple tags + manifest link |
| `dashboard/install.js` → `/js/install.js` | Platforms CTAs + Trading modal |
| `dashboard/install.css` → `/css/install.css` | instruction sheet |

## 2. Trading Resources → Platforms

Add **Platforms** under Trading Resources.

Two sections: **Dashboard** and **Verodus Trading**. Each has Android / iOS / iPadOS and Windows / macOS / ChromeOS·Linux tables (how to install, quality, notes).

- **Dashboard** — install this origin
- **Verodus Trading** — same tables; modal + link to `https://trade.verodus.com/dashboard`

Leave account-card Platform5 / TradeHub buttons as they are.

## 3. Landing pills (verodus.com)

Modal: install from **Dashboard → Trading Resources → Platforms**. Copy `www/install.js`, `www/platforms-modal.css`, `www/store-buttons.html`. No Play / App Store. No www PWA.

## Verify

1. Uninstall old Verodus icons.
2. Landing pills → modal → Open dashboard.
3. Trading Resources → Platforms: **Dashboard** and **Verodus Trading** tables; Trading → `https://trade.verodus.com/dashboard`.
