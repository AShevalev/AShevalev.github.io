/**
 * Dashboard origin. Registers the SW, rewrites TradeHub / P5 launches so they
 * never leave this host. Platforms page CTAs use /js/install.js (classic) so
 * Android / Mobile / Desktop each get the right prompt — do not also bind
 * [data-install-app] here or the cards all share one generic sheet.
 */
import "./intercept-launches.js";
import "../lock-origin-entry.js";

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
