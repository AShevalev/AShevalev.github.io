/**
 * Drop this on dashboard.verodus.com.
 *
 * Rewrites TradeHub / Platform 5 launches so the top-level URL stays on
 * dashboard.verodus.com. Chrome then never treats the session as a website.
 */
import { toInAppUrl } from "./same-origin.js";

function rewrite(url) {
  return toInAppUrl(String(url), window.location.origin) || url;
}

document.addEventListener(
  "click",
  (event) => {
    const link = event.target.closest && event.target.closest("a[href]");
    if (!link) return;
    const next = toInAppUrl(link.href, window.location.origin);
    if (!next || next === link.href) return;
    event.preventDefault();
    window.location.assign(next);
  },
  true
);

try {
  const originalOpen = window.open.bind(window);
  window.open = (url, target, features) => {
    if (url) {
      const next = toInAppUrl(String(url), window.location.origin);
      if (next) {
        window.location.assign(next);
        return window;
      }
    }
    return originalOpen(url, target, features);
  };
} catch {
  // window.open may be non-writable in some WebViews.
}
