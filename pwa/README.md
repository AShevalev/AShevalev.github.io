# Add to Home Screen CTA

Drop-in code so a mobile visitor can install the browser app on their home screen **from a button**, in every common mobile browser.

There is no single install API. This kit picks the right path:

| Browser | What the CTA does |
|---|---|
| Chrome, Edge, Samsung, Opera (Android + desktop) | Native install dialog via `beforeinstallprompt` |
| Safari, Chrome, Firefox, Edge on iOS / iPadOS | Instruction sheet: Share → Add to Home Screen |
| Firefox Android | Instruction sheet: menu → Install |
| Already running as an installed app | CTA is hidden |

Chromium only shows the native prompt if the page is a real PWA: HTTPS, a web app manifest, and a service worker with a `fetch` handler. Those files are included.

## Wire a CTA on any page

```html
<link rel="manifest" href="/manifest.webmanifest" />
<meta name="theme-color" content="#07003B" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-title" content="Verodus" />
<link rel="apple-touch-icon" href="/pwa/icons/apple-touch-icon.png" />
<link rel="stylesheet" href="/pwa/add-to-home-screen.css" />

<button type="button" data-install-app>Add to Home Screen</button>

<script type="module">
  import { bindInstallCta } from "/pwa/add-to-home-screen.js";
  bindInstallCta({
    selector: "[data-install-app]",
    appName: "Verodus",
    serviceWorkerUrl: "/sw.js",
  });
</script>
```

`bindInstallCta()`:

1. Registers the service worker (needed for Chrome’s prompt).
2. Captures `beforeinstallprompt` and does **not** let Chrome auto-prompt.
3. On tap: calls `prompt()` when the browser supports it; otherwise opens a bottom sheet with the steps for that browser.
4. Hides the button after install and when the app is already in standalone mode.

To skip auto-registering a worker (if the host page already has one):

```js
bindInstallCta({ registerServiceWorker: false, appName: "Verodus" });
```

## Files

| File | Role |
|---|---|
| `index.html` | Demo page with the CTA |
| `manifest.webmanifest` | Name, icons, `standalone` display |
| `sw.js` | Fetch handler so Chromium will install |
| `pwa/add-to-home-screen.js` | CTA + native prompt + instruction sheet |
| `pwa/platform.js` | Browser detection (unit-tested) |
| `pwa/add-to-home-screen.css` | Button + sheet |
| `pwa/icons/` | 192 / 512 / maskable / Apple touch icons |

Copy the `pwa/` folder, `manifest.webmanifest`, and `sw.js` onto the production origin (for example `verodus.com`). Point `start_url`, `id`, and icon paths at that origin.

## Tests

```bash
node --test tests/platform.test.mjs
```
