"use client";

import { useEffect } from "react";
import { shouldEmbedTrade } from "../lock-origin.js";

/**
 * Copy into the dashboard Next.js app as components/PlatformFrame.jsx
 *
 * Chrome / Edge: iframe TradeHub / P5 so the top-level URL stays on Dashboard.
 * Safari on a Mac: no URL bar on Verodus pages — go to trade.verodus.com
 * at the top level (no iframe).
 * Already inside another iframe: navigate that frame to trade (do not nest).
 */
export default function PlatformFrame({ accountId, kind = "tradehub" }) {
  const src = `https://trade.verodus.com/${kind}/${accountId}`;
  const title = kind === "p5" ? "Platform 5" : "TradeHub";
  const nested =
    typeof window !== "undefined" && window.self !== window.top;
  const embed =
    typeof window !== "undefined" ? shouldEmbedTrade(window) : true;

  useEffect(() => {
    if (nested || !embed) window.location.replace(src);
  }, [nested, embed, src]);

  if (nested || !embed) return null;

  return (
    <iframe
      src={src}
      title={title}
      allow="fullscreen; clipboard-read; clipboard-write; accelerometer; gyroscope"
      allowFullScreen
      style={{
        position: "fixed",
        inset: 0,
        width: "100%",
        height: "100%",
        border: 0,
        background: "#07003B",
      }}
    />
  );
}
