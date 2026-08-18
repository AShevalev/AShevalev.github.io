/**
 * Pure platform / install-guide detection for the Add to Home Screen CTA.
 * No DOM. Safe to unit-test in Node.
 */

/**
 * @typedef {object} Env
 * @property {string} [userAgent]
 * @property {string} [platform]
 * @property {number} [maxTouchPoints]
 * @property {boolean} [standalone] navigator.standalone (iOS Safari)
 * @property {boolean} [displayModeStandalone]
 * @property {boolean} [displayModeFullscreen]
 * @property {boolean} [displayModeMinimalUi]
 * @property {boolean} [hasNativePrompt] true when beforeinstallprompt was captured
 * @property {boolean} [hasWebInstall] true when navigator.install exists
 */

/**
 * @param {Env} [env]
 */
export function detectPlatform(env = {}) {
  const ua = String(env.userAgent || "").toLowerCase();
  const platform = String(env.platform || "");
  const maxTouchPoints = Number(env.maxTouchPoints || 0);

  const ios =
    /iphone|ipad|ipod/.test(ua) ||
    (platform === "MacIntel" && maxTouchPoints > 1);
  const android = /android/.test(ua);
  const mobile = ios || android || /mobile/.test(ua);

  const firefox = /firefox|fxios/.test(ua);
  const samsung = /samsungbrowser/.test(ua);
  const edge = /edg(e|ios|a)?/.test(ua);
  const opera = /opr\/|opt\//.test(ua);
  const chromeIos = /crios/.test(ua);
  const chrome =
    (/chrome/.test(ua) || chromeIos) && !edge && !opera && !samsung;
  const safari =
    ios &&
    /safari/.test(ua) &&
    !/crios|fxios|edgios|opt\//.test(ua) &&
    !chromeIos;
  const safariMac =
    !ios &&
    !android &&
    /macintosh|mac os x/.test(ua) &&
    /safari/.test(ua) &&
    !/chrome|crios|chromium|edg|opr\/|firefox|fxios/.test(ua);

  const installed = Boolean(
    env.standalone ||
      env.displayModeStandalone ||
      env.displayModeFullscreen ||
      env.displayModeMinimalUi
  );

  return {
    ios,
    android,
    mobile,
    firefox,
    samsung,
    edge,
    opera,
    chrome,
    chromeIos,
    safari,
    safariMac,
    installed,
  };
}

/**
 * Which install path the CTA should take.
 *
 * - hidden: already running as an installed app
 * - native: Chromium beforeinstallprompt (or experimental navigator.install)
 * - ios: Share sheet → Add to Home Screen (Safari + every iOS browser)
 * - firefox-android: menu → Install
 * - android: Chrome/Samsung/Edge menu fallback when the prompt is not ready
 * - firefox-desktop: cannot install PWAs
 * - safari-mac: File → Add to Dock (macOS 14+)
 * - generic: last-resort menu instructions
 *
 * @param {Env} [env]
 * @returns {"hidden"|"native"|"ios"|"firefox-android"|"android"|"firefox-desktop"|"safari-mac"|"generic"}
 */
export function getInstallGuide(env = {}) {
  const p = detectPlatform(env);
  if (p.installed) return "hidden";
  if (env.hasNativePrompt || env.hasWebInstall) return "native";
  if (p.ios) return "ios";
  if (p.firefox && p.android) return "firefox-android";
  if (p.android) return "android";
  if (p.firefox) return "firefox-desktop";
  if (p.safariMac) return "safari-mac";
  return "generic";
}

/**
 * Copy for the instruction sheet. `appName` is interpolated as plain text.
 * @param {ReturnType<typeof getInstallGuide>} guide
 * @param {string} [appName]
 */
export function getGuideCopy(guide, appName = "this app") {
  const name = appName.trim() || "this app";

  if (guide === "ios") {
    return {
      title: `Add ${name} to your Home Screen`,
      lead: "Works in Safari, Chrome, Firefox, and Edge on iPhone and iPad.",
      steps: [
        {
          icon: "share",
          text: "Tap Share in the toolbar (the square with the arrow).",
        },
        {
          icon: "plus",
          text: "Scroll the sheet and tap Add to Home Screen.",
        },
        {
          icon: "check",
          text: "Tap Add. The icon lands next to your other apps.",
        },
      ],
    };
  }

  if (guide === "firefox-android") {
    return {
      title: `Install ${name}`,
      lead: "Firefox does not show a one-tap install prompt. Use the menu.",
      steps: [
        {
          icon: "menu",
          text: "Tap the menu (three dots) in the address bar.",
        },
        {
          icon: "plus",
          text: "Tap Install, or More → Add app to Home screen.",
        },
        {
          icon: "check",
          text: "Confirm. Open it from the home screen like any other app.",
        },
      ],
    };
  }

  if (guide === "android") {
    return {
      title: `Install ${name}`,
      lead: "Add it from the browser menu if the install banner does not appear.",
      steps: [
        {
          icon: "menu",
          text: "Tap the browser menu (three dots).",
        },
        {
          icon: "plus",
          text: "Tap Install app, Add to Home screen, or Install.",
        },
        {
          icon: "check",
          text: "Confirm. Launch it from the home screen.",
        },
      ],
    };
  }

  if (guide === "firefox-desktop") {
    return {
      title: `Install ${name} on your phone`,
      lead: "Firefox on desktop cannot install web apps. Use Chrome or Edge here, or open this page on your phone.",
      steps: [
        {
          icon: "share",
          text: "On iPhone or iPad: Share → Add to Home Screen.",
        },
        {
          icon: "plus",
          text: "On Android Chrome: the menu → Install app.",
        },
        {
          icon: "check",
          text: "On this computer: open the page in Chrome or Edge, then install.",
        },
      ],
    };
  }

  if (guide === "safari-mac") {
    return {
      title: `Add ${name} to the Dock`,
      lead: "Safari on a Mac (macOS 14 Sonoma or newer). File → Add to Dock.",
      steps: [
        {
          icon: "share",
          text: "Open this page in Safari (not Chrome).",
        },
        {
          icon: "plus",
          text: "File → Add to Dock. Or the share button in the toolbar → Add to Dock.",
        },
        {
          icon: "check",
          text: "Open it from the Dock like any other Mac app.",
        },
      ],
    };
  }

  return {
    title: `Add ${name} to your Home Screen`,
    lead: "Use the browser menu. Wording varies by browser.",
    steps: [
      {
        icon: "menu",
        text: "Open the browser menu.",
      },
      {
        icon: "plus",
        text: "Choose Add to Home Screen, Install app, or Install.",
      },
      {
        icon: "check",
        text: "Confirm. Open the icon from your home screen.",
      },
    ],
  };
}

/**
 * Snapshot of the current browser. Pass into getInstallGuide().
 * @param {Window & typeof globalThis} [win]
 * @returns {Env}
 */
export function readBrowserEnv(win) {
  const w = win || (typeof globalThis !== "undefined" ? globalThis : {});
  const nav = w.navigator || {};
  const match = (query) => {
    try {
      return Boolean(w.matchMedia && w.matchMedia(query).matches);
    } catch {
      return false;
    }
  };

  return {
    userAgent: nav.userAgent || "",
    platform: nav.platform || "",
    maxTouchPoints: nav.maxTouchPoints || 0,
    standalone: Boolean(nav.standalone),
    displayModeStandalone: match("(display-mode: standalone)"),
    displayModeFullscreen: match("(display-mode: fullscreen)"),
    displayModeMinimalUi: match("(display-mode: minimal-ui)"),
    hasWebInstall: typeof nav.install === "function",
  };
}

/**
 * TradeHub / Platform 5 account ids (CUID). These must never be a PWA start_url —
 * every user would install someone else's account.
 */
export function isAccountScopedPath(pathname) {
  return /\/(tradehub|p5)\/[a-z0-9]{20,}(?:\/|$)/i.test(String(pathname || ""));
}

export function isSameOrigin(urlA, urlB) {
  try {
    return new URL(urlA).origin === new URL(urlB).origin;
  } catch {
    return false;
  }
}

/**
 * Homepage CTAs on verodus.com cannot install dashboard.verodus.com in-place.
 * Send the user to the dashboard origin, then prompt there.
 *
 * @returns {"hidden"|"prompt-here"|"redirect"}
 */
export function resolveInstallAction({
  currentHref = "",
  installUrl = "",
  installed = false,
} = {}) {
  if (installed) return "hidden";
  if (!installUrl) return "prompt-here";
  if (!currentHref || isSameOrigin(currentHref, installUrl)) return "prompt-here";
  return "redirect";
}

/** Same-origin path of the Dashboard install page (Trading Resources → Platforms). */
export const DASHBOARD_PLATFORMS_PATH = "/trading-resources/platforms";

export const DASHBOARD_PLATFORMS_HREF =
  "https://dashboard.verodus.com/trading-resources/platforms";

export const LANDING_INSTALL_PATH = ["Dashboard", "Trading Resources", "Platforms"];

export function landingInstallPathLabel(separator = " → ") {
  return LANDING_INSTALL_PATH.join(separator);
}

/**
 * Homepage store pills do not install the marketing site and do not open the stores.
 * They open a modal that points at Dashboard → Trading Resources → Platforms.
 */
export function getLandingInstallModalCopy() {
  return {
    title: "Install Verodus from the dashboard",
    lead: `Install from ${landingInstallPathLabel()}. Choose Android, Mobile, Desktop, or Safari.`,
    cta: "Open dashboard",
    dismiss: "Not now",
    href: DASHBOARD_PLATFORMS_HREF,
  };
}

export const TRADE_APP_HREF = "https://trade.verodus.com/dashboard";

/**
 * Dashboard modal: how to install the separate TradeHub app.
 * Chrome can only install the origin you are on — this cannot auto-install.
 */
export function getTradingInstallModalCopy() {
  return {
    title: "Install the trading app",
    lead: "Chrome can only install the site you are on. Open TradeHub in the browser, then install there. This does not happen automatically.",
    steps: [
      "Tap Open TradeHub. Use Chrome or Safari — a normal tab, not only the Dashboard window.",
      "When TradeHub loads: Chrome/Edge → Install in the address bar. iPhone → Share → Add to Home Screen. Safari on a Mac → File → Add to Dock.",
      "Open it from your home screen or Dock. TradeHub and Platform 5 are the same trading app.",
    ],
    cta: "Open TradeHub",
    dismiss: "Not now",
    href: TRADE_APP_HREF,
  };
}
export function getPlatformsCards() {
  const trading = getTradingInstallModalCopy();
  return [
    {
      id: "android",
      title: "Android",
      lead: "Phone or tablet. Chrome, Edge, or Samsung Internet.",
      steps: [
        "Open this page in Chrome (or Edge / Samsung Internet).",
        "Tap Install on Android, or the browser menu → Install app.",
        "Open Verodus from your home screen.",
      ],
      cta: "Install on Android",
    },
    {
      id: "mobile",
      title: "Mobile",
      lead: "iPhone and iPad. Works in Safari and every iOS browser.",
      steps: [
        "Tap Share in the toolbar (the square with the arrow).",
        "Scroll and tap Add to Home Screen.",
        "Tap Add. The icon lands next to your other apps.",
      ],
      cta: "Show iPhone steps",
    },
    {
      id: "desktop",
      title: "Desktop",
      lead: "Windows, Mac, and Chromebook. Use Chrome or Edge.",
      steps: [
        "Open this page in Chrome or Edge (Firefox cannot install web apps).",
        "Click Install Verodus in the address bar, or the menu → Install Verodus.",
        "Open it from your dock, taskbar, or Start menu.",
      ],
      cta: "Install on desktop",
    },
    {
      id: "safari",
      title: "Safari",
      lead: "Mac. Safari 17+ on macOS 14 Sonoma or newer. Creates a Dock web app.",
      steps: [
        "Open this page in Safari on your Mac (not Chrome).",
        "File → Add to Dock. Or the share button in the toolbar → Add to Dock.",
        "Open Verodus from the Dock like any other Mac app.",
      ],
      cta: "Show Safari steps",
    },
    {
      id: "trading",
      title: "Trading",
      lead: "Optional second app. TradeHub and Platform 5 on trade.verodus.com.",
      steps: trading.steps,
      cta: "How to install Trading",
      href: trading.href,
    },
  ];
}
