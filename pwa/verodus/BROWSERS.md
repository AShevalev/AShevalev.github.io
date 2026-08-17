# Every browser: install from verodus.com, no top bar

Most people tap **for android** / **for iOS** on the landing page. That must install **`https://www.verodus.com`**, then open `/app`. Sending them to `dashboard.verodus.com` is what draws the X / URL / Verodus CRM bar.

```
Landing pills  →  install www.verodus.com
Home screen    →  https://www.verodus.com/app
                  iframe → dashboard.verodus.com/dashboard
                    (inside the frame) TradeHub / Platform 5
```

The standalone window’s URL never leaves `www.verodus.com`. Chrome, Edge, and Safari do not show the out-of-scope bar for iframe navigations.

## What each browser does

| Browser | Landing-page install | Bar when opening Dashboard / TradeHub / P5 |
|---|---|---|
| Chrome / Edge — **desktop** | Install icon / ⋮ → Install Verodus | Gone if they stay in `/app` |
| Chrome / Edge / Samsung — **Android** | Pill → native prompt or ⋮ → Install app | Gone if they stay in `/app` |
| Safari **iPhone / iPad** | Pill → Share → Add to Home Screen **on verodus.com** | Gone if `start_url` is `/app` |
| Chrome / Firefox **on iOS** | Same share sheet (iOS 16.4+) | Same as Safari |
| Safari **Mac** | Add to Dock on verodus.com | Gone if they stay in `/app` |
| Firefox **Android** | ⋮ → Install | Gone if they stay in `/app` |
| Firefox **desktop** | Cannot install | Firefox URL bar always stays |
| Instagram / Gmail in-app browsers | Custom Tab — cannot install | Open in Chrome or Safari first |

## Steps

1. On `www.verodus.com`: PNG 192/512 icons, `manifest.json` with `start_url: "/app"`, `sw.js`, Apple tags (`www/head.html`).
2. Replace Play Store / App Store `href`s with `/app` and load `store-buttons.js`.
3. Ship `www/app.html` as **`/app`** (or `/app/index.html`). It iframes `https://dashboard.verodus.com/dashboard`.
4. Dashboard + Trade CSP: `frame-ancestors 'self' https://www.verodus.com` (see `frame-headers.js` on both apps).
5. Google login must stay in a **popup** or return to `/app`. A top-level redirect to `dashboard.verodus.com` brings the bar back.
6. Uninstall any old icon that was installed from Dashboard or TradeHub, then install again from the landing pills.

Platform 5 / TradeHub buttons inside the CRM can still point at `trade.verodus.com` **inside the iframe**. That does not move the top-level URL. Same-origin `/p5/{id}` routes on Dashboard remain a plus if someone opens the CRM in a normal tab.
