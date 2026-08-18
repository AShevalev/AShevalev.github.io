/**
 * Drop this on dashboard.verodus.com.
 *
 * Chrome / Edge installed windows: rewrite TradeHub / P5 to same-origin paths.
 * Safari on a Mac: leave trade.verodus.com links alone (no URL bar, no iframe).
 * Already inside www.verodus.com/app (or another shell): do nothing so the
 * existing iframe can navigate to trade.verodus.com without a nested frame.
 */
import { isEmbedded, isSafariMac } from "../lock-origin.js";
import { toInAppUrl } from "./same-origin.js";

if (!isEmbedded() && !isSafariMac()) {
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
}
