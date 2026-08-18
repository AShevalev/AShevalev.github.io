# Every browser: install from any Verodus page, no top bar

Install from the landing pills, the Chrome toolbar, Dashboard, TradeHub, or Platform 5. Chrome’s X / URL bar appears only when the **top-level** URL changes host (`www` ↔ `dashboard` ↔ `trade`).

Each origin keeps its own window:

- Installed on **www.verodus.com** → stay on `/app`, iframe the CRM (TradeHub/P5 then navigate **that same iframe**, not a second one).
- Installed on **dashboard.verodus.com** → stay there, iframe TradeHub/P5.
- Installed on **trade.verodus.com** → stay there, iframe Dashboard if they go back to the CRM.

`lock-origin.js` runs only in an **installed** window (`display-mode: standalone`). A normal browser tab on the landing page still navigates as a website.

## Will the iframe slow things down?

A little, once — not on every tick of the chart.

| What | Cost |
|---|---|
| One full-viewport iframe | Extra document + JS world. Usually tens of milliseconds plus the destination load you would pay anyway. |
| Nested iframes (landing shell **and** a PlatformFrame inside it) | Avoided. If we are already in a frame, we navigate that frame to `trade.verodus.com` instead of stacking. |
| Charts / orders inside TradeHub or P5 | Same as opening those apps directly. The iframe is not in the hot path. |

The expensive part is the terminal bundle, not the frame. A reverse proxy onto one host would be slightly leaner and is the long-term option; one iframe is the change that works on every current Verodus host without merging the apps.

Firefox desktop still cannot hide its own URL bar.

Safari on a Mac does not show a URL bar on Verodus pages. Do not iframe TradeHub / Platform 5 there — open `trade.verodus.com` at the top level. Install with File → Add to Dock (macOS 14+).

## Chrome toolbar

Same PWA as the pills. Install while the tab is on that Verodus host. Toolbar on Dashboard installs Dashboard; `lock-origin` then iframes Trade instead of leaving.

## Steps

1. Landing: `start_url: "/app"`, pills, `sw.js`, PNG icons (`www/`).
2. Dashboard + Trade: `frame-ancestors` includes `https://www.verodus.com` and `https://dashboard.verodus.com`.
3. Load `lock-origin-entry.js` on all three origins (no-op in a normal tab).
4. Google login: popup, or return to the **current** origin’s shell — never `window.top` to another Verodus host.
