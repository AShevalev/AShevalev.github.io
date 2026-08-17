/**
 * Landing-page app shell. Keep this document on www.verodus.com/app.
 * If Dashboard or a login flow tries to break out to the top window,
 * send it back here instead of letting Chrome show the website bar.
 */
const FRAME_ORIGINS = new Set([
  "https://dashboard.verodus.com",
  "https://trade.verodus.com",
]);

const frame = document.getElementById("verodus-app");

window.addEventListener("message", (event) => {
  if (!FRAME_ORIGINS.has(event.origin)) return;
  const data = event.data || {};
  if (data.type === "verodus:navigate" && typeof data.src === "string") {
    try {
      const next = new URL(data.src, event.origin);
      if (FRAME_ORIGINS.has(next.origin)) frame.src = next.href;
    } catch {
      // Ignore malformed messages.
    }
  }
});
