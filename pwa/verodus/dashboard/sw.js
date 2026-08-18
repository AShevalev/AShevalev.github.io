/* Network-only fetch handler. Required so Chrome will install the dashboard
   as a standalone app. Do not cache Next.js hashed chunks — that breaks deploys. */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(fetch(event.request));
});
