/* Network-only. Required so Chrome will install www.verodus.com as a PWA.
   Do not cache the marketing site or Next chunks. */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(fetch(event.request));
});
