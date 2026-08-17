# Verodus home-screen app

**Chosen model: Dashboard is the app.** Follow **[SHIP-DASHBOARD.md](SHIP-DASHBOARD.md)**.

**Hand this to the dashboard/landing coder:** [CODER-INSTRUCTIONS.md](CODER-INSTRUCTIONS.md) plus the zip [verodus-platforms-for-coder.zip](verodus-platforms-for-coder.zip).

CRM routes stay on `dashboard.verodus.com` (no bar). Install lives at **Trading Resources → Platforms** (Android / Mobile / Desktop). TradeHub / Platform 5 are iframed from `/tradehub/{id}` and `/p5/{id}`.

Landing pills on verodus.com open a modal that points at that path — they do not install the marketing site and do not open the stores.

The landing-page `/app` shell ([SHIP.md](SHIP.md)) is the other model — use it only if you insist on installing from verodus.com. Do not run both PWAs.
