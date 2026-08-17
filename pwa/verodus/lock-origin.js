/**
 * Keep an installed Verodus window on whatever origin it was installed from.
 *
 * Chrome's X / URL bar appears on a top-level jump between
 * www / dashboard / trade. Iframe that jump instead.
 *
 * Safari on a Mac does not show that bar on Verodus pages. Skip the lock and
 * open TradeHub / Platform 5 at the top level.
 *
 * If this document is already inside an iframe (landing /app shell), do nothing
 * so we never nest frames. The parent origin is already locked.
 */

export const VERODUS_HOSTS = new Set([
  "www.verodus.com",
  "verodus.com",
  "dashboard.verodus.com",
  "trade.verodus.com",
]);

/**
 * Safari on macOS (not iPhone / iPad). Chrome on Mac includes "Safari" in the
 * UA, so Chrome/Edge/Firefox must be excluded.
 *
 * @param {Window & typeof globalThis} [win]
 */
export function isSafariMac(win = globalThis) {
  const nav = win.navigator || {};
  const ua = String(nav.userAgent || "");
  const platform = String(nav.platform || "");
  const maxTouchPoints = Number(nav.maxTouchPoints || 0);
  const ios =
    /iPhone|iPad|iPod/i.test(ua) ||
    (platform === "MacIntel" && maxTouchPoints > 1);
  if (ios) return false;
  if (/Android/i.test(ua)) return false;
  const safari =
    /Safari/i.test(ua) &&
    !/Chrome|CriOS|Chromium|Edg|OPR|FxiOS|Firefox/i.test(ua);
  return Boolean(safari && /Macintosh/i.test(ua));
}

/** Chrome/Edge need an iframe for trade. Safari on a Mac does not. */
export function shouldEmbedTrade(win = globalThis) {
  return !isSafariMac(win);
}

export function isEmbedded(win = globalThis) {
  try {
    return win.self !== win.top;
  } catch {
    return true;
  }
}

export function isStandaloneApp(win = globalThis) {
  try {
    const standalone =
      (win.matchMedia &&
        (win.matchMedia("(display-mode: standalone)").matches ||
          win.matchMedia("(display-mode: fullscreen)").matches ||
          win.matchMedia("(display-mode: minimal-ui)").matches)) ||
      win.navigator?.standalone === true;
    return Boolean(standalone);
  } catch {
    return false;
  }
}

export function isOtherVerodusUrl(href, currentOrigin) {
  let url;
  try {
    url = new URL(String(href), currentOrigin || "https://www.verodus.com/");
  } catch {
    return false;
  }
  const current = currentOrigin || url.origin;
  if (url.origin === current) return false;
  if (url.protocol !== "http:" && url.protocol !== "https:") return false;
  return VERODUS_HOSTS.has(url.hostname);
}

/**
 * Only lock top-level windows that are already the installed app.
 * A normal browser tab on the landing page must still navigate as a website.
 */
export function shouldLockOrigin(win = globalThis) {
  return isStandaloneApp(win) && !isEmbedded(win) && !isSafariMac(win);
}

const FRAME_ID = "verodus-lock-frame";

export function showLockFrame(href, doc = globalThis.document) {
  if (!doc?.body) return;
  let frame = doc.getElementById(FRAME_ID);
  if (!frame) {
    frame = doc.createElement("iframe");
    frame.id = FRAME_ID;
    frame.title = "Verodus";
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
      zIndex: "2147483646",
      background: "#07003B",
    });
    doc.body.appendChild(frame);
  }
  frame.src = href;
}

export function bindOriginLock(win = globalThis) {
  if (!shouldLockOrigin(win)) return () => {};
  const doc = win.document;

  const intercept = (href) => {
    if (!isOtherVerodusUrl(href, win.location.origin)) return false;
    showLockFrame(String(new URL(href, win.location.href)), doc);
    return true;
  };

  const onClick = (event) => {
    const link = event.target.closest && event.target.closest("a[href]");
    if (!link) return;
    if (intercept(link.href)) event.preventDefault();
  };
  doc.addEventListener("click", onClick, true);

  let restoreOpen = () => {};
  try {
    const originalOpen = win.open.bind(win);
    win.open = (url, target, features) => {
      if (url && intercept(url)) return win;
      return originalOpen(url, target, features);
    };
    restoreOpen = () => {
      win.open = originalOpen;
    };
  } catch {
    // window.open may be non-writable.
  }

  return () => {
    doc.removeEventListener("click", onClick, true);
    restoreOpen();
  };
}
