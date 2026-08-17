"use client";

import { useEffect } from "react";

/**
 * Copy into the dashboard Next.js app as components/PlatformFrame.jsx
 *
 * Top-level Dashboard install: iframe TradeHub / P5 (one extra document).
 * Already inside the landing /app iframe: navigate this frame to trade.verodus.com
 * so we do not stack iframes.
 */
export default function PlatformFrame({ accountId, kind = "tradehub" }) {
  const src = `https://trade.verodus.com/${kind}/${accountId}`;
  const title = kind === "p5" ? "Platform 5" : "TradeHub";
  const nested =
    typeof window !== "undefined" && window.self !== window.top;

  useEffect(() => {
    if (nested) window.location.replace(src);
  }, [nested, src]);

  if (nested) return null;

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
