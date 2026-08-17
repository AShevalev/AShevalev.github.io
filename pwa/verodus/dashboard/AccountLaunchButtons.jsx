"use client";

import { launchPath } from "./same-origin.js";

/**
 * Drop onto each account card. These must be same-origin <a> tags.
 * window.open / target="_blank" / href="https://trade.verodus.com/..."
 * is what draws the Chrome bar on desktop and mobile.
 */
export default function AccountLaunchButtons({ accountId, className = "" }) {
  return (
    <div className={className}>
      <a href={launchPath("p5", accountId)}>Platform5</a>
      <a href={launchPath("tradehub", accountId)}>TradeHub</a>
    </div>
  );
}
