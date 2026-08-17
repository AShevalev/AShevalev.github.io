/**
 * Full-viewport TradeHub / Platform 5 frame.
 * The document URL stays on dashboard.verodus.com, so Chrome keeps standalone UI.
 */
import { toTradeEmbedSrc } from "./same-origin.js";

export function mountPlatformFrame(target, href) {
  const src = toTradeEmbedSrc(href, window.location.origin);
  if (!src) {
    throw new Error("Not a TradeHub or Platform 5 URL");
  }
  const frame = document.createElement("iframe");
  frame.src = src;
  frame.title = src.includes("/p5/") ? "Platform 5" : "TradeHub";
  frame.setAttribute(
    "allow",
    "fullscreen; clipboard-read; clipboard-write; accelerometer; gyroscope"
  );
  frame.setAttribute("allowfullscreen", "");
  Object.assign(frame.style, {
    position: "fixed",
    inset: "0",
    width: "100%",
    height: "100%",
    border: "0",
    background: "#07003B",
  });
  target.replaceChildren(frame);
  return frame;
}

if (document.documentElement.hasAttribute("data-platform-embed")) {
  mountPlatformFrame(document.body, window.location.href);
}
