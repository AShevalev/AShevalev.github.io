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
    lead: `Install from ${landingInstallPathLabel()}. Two sections — Dashboard and Verodus Trading.`,
    cta: "Open dashboard",
    dismiss: "Not now",
    href: DASHBOARD_PLATFORMS_HREF,
  };
}

export const TRADE_APP_HREF = "https://trade.verodus.com/dashboard";

/**
 * Sheet copy id for a Platforms row. Chrome on iPhone stays on iOS
 * (Share → Add to Home Screen). The Android row is Chromium on Android.
 */
export function resolveInstallSheetKey(section, platform, env = {}) {
  const p = detectPlatform(env);
  if (platform === "android" && p.chromeIos) {
    return `${section}-android-chrome`;
  }
  return `${section}-${platform}`;
}

export function getTradingInstallModalCopy(platform = "desktop", env = {}) {
  const href = TRADE_APP_HREF;
  const shared = {
    cta: "Open TradeHub",
    dismiss: "Not now",
    href,
  };
  const key = resolveInstallSheetKey("trading", platform, env).replace(/^trading-/, "");

  if (key === "ios") {
    return {
      ...shared,
      title: "Install Verodus Trading on iPhone or iPad",
      lead: "Safari, Chrome, Firefox, or Edge on iPhone and iPad. Chrome and Edge on iOS 16.4+ also use Share → Add to Home Screen.",
      steps: [
        "Tap Open TradeHub in Safari (or Firefox / Edge).",
        "Tap Share (the square with the arrow) → Add to Home Screen → Add.",
        "Open Verodus Trading from your home screen. TradeHub and Platform 5 are the same app.",
      ],
    };
  }

  if (key === "android-chrome") {
    return {
      ...shared,
      title: "Install Verodus Trading from Chrome on iPhone",
      lead: "Chrome on iPhone is listed under Android. It still uses Add to Home Screen — there is no Install app prompt.",
      steps: [
        "Tap Open TradeHub in Chrome.",
        "Tap Share (the square with the arrow) → Add to Home Screen → Add.",
        "Open Verodus Trading from your home screen. TradeHub and Platform 5 are the same app.",
      ],
    };
  }

  if (key === "android") {
    return {
      ...shared,
      title: "Install Verodus Trading on Android",
      lead: "Open TradeHub in Chrome, Edge, or Samsung Internet, then install there. This does not happen automatically.",
      steps: [
        "Tap Open TradeHub in Chrome (or Edge / Samsung Internet).",
        "Tap Install, or the browser menu → Install app.",
        "Open it from your home screen. TradeHub and Platform 5 are the same app.",
      ],
    };
  }

  return {
    ...shared,
    title: "Install Verodus Trading on desktop",
    lead: "Open TradeHub in a normal browser tab, then install there. This does not happen automatically.",
    steps: [
      "Click Open TradeHub.",
      "Windows or Chromebook — Chrome or Edge: Install in the address bar (or the menu → Install).",
      "Mac — Chrome or Edge: same Install control. Safari (macOS 14+): File → Add to Dock.",
      "Firefox on desktop cannot install web apps — use Chrome, Edge, or Safari.",
    ],
  };
}

/**
 * Which table row to highlight.
 * Chrome on iPhone is iOS / iPadOS (Share sheet), not Android.
 */
export function recommendedInstallSurface(env = {}) {
  const p = detectPlatform(env);
  if (p.ios) return "ios";
  if (p.android) return "android";
  if (p.safariMac) return "macos";
  if (/win/i.test(String(env.userAgent || env.platform || ""))) return "windows";
  if (/linux|cros|chromium os/i.test(String(env.userAgent || ""))) return "linux";
  return "macos";
}

/**
 * Banner above the two sections. Empty string = hide.
 */
export function getPlatformsHint(env = {}) {
  const p = detectPlatform(env);
  if (p.chromeIos) {
    return "You are in Chrome on iPhone. Use iOS / iPadOS → Share → Add to Home Screen.";
  }
  if (p.ios) {
    return "You are on iOS. Use iOS / iPadOS in each section.";
  }
  if (p.android) {
    return "You are on Android. Use the Android row in each section.";
  }
  if (p.safariMac) {
    return "You are in Safari on a Mac. Use macOS → File → Add to Dock.";
  }
  if (p.firefox) {
    return "Firefox on desktop cannot install. Use Chrome or Edge (Windows/macOS tables), or Safari Add to Dock.";
  }
  return "Use the Desktop tables for Windows, macOS, or ChromeOS / Linux.";
}

export function getDashboardInstallCopy(platform = "desktop", env = {}) {
  const key = resolveInstallSheetKey("dashboard", platform, env).replace(/^dashboard-/, "");

  if (key === "ios") {
    return {
      title: "Add Dashboard to iPhone or iPad",
      lead: "Safari, Chrome, Firefox, or Edge on iPhone and iPad. Chrome and Edge on iOS 16.4+ also use Share → Add to Home Screen.",
      steps: [
        "Stay on this Dashboard page.",
        "Tap Share in the toolbar (the square with the arrow).",
        "Tap Add to Home Screen, then Add.",
      ],
    };
  }
  if (key === "android-chrome") {
    return {
      title: "Add Dashboard from Chrome on iPhone",
      lead: "Chrome on iPhone is listed under Android. It still uses Add to Home Screen — there is no Install app prompt.",
      steps: [
        "Stay on this Dashboard page in Chrome.",
        "Tap Share in the Chrome toolbar (the square with the arrow).",
        "Tap Add to Home Screen, then Add.",
      ],
    };
  }
  if (key === "android") {
    return {
      title: "Install Dashboard on Android",
      lead: "Chrome, Edge, or Samsung Internet on your phone or tablet.",
      steps: [
        "Stay on this Dashboard page in Chrome (or Edge / Samsung Internet).",
        "Tap Install, or the browser menu → Install app.",
        "Open Verodus from your home screen.",
      ],
    };
  }
  return {
    title: "Install Dashboard on desktop",
    lead: "Windows, Mac, and Chromebook.",
    steps: [
      "Windows or Chromebook — Chrome or Edge: Install in the address bar, or the menu → Install Verodus.",
      "Mac — Chrome or Edge: same Install control. Safari (macOS 14+): File → Add to Dock (or Share → Add to Dock).",
      "Firefox on desktop cannot install web apps — use Chrome, Edge, or Safari.",
    ],
  };
}

/** Rows for the Platforms guide tables (Dashboard and Verodus Trading). */
export function getInstallGuideRows() {
  return {
    phone: [
      {
        id: "android",
        platform: "Android",
        how: "Automatic install prompt + Menu → Install app / Add to Home screen",
        quality: "Excellent (almost native)",
        notes:
          "Chrome, Edge, Samsung Internet, Brave all support it well. Can become a WebAPK.",
      },
      {
        id: "ios",
        platform: "iOS / iPadOS",
        how: "Safari → Share → Add to Home Screen (also possible from Chrome/Edge on iOS 16.4+)",
        quality: "Good but manual",
        notes:
          "No automatic beforeinstallprompt. You must show clear instructions. Push notifications only work after install.",
      },
    ],
    desktop: [
      {
        id: "windows",
        platform: "Windows",
        how: "Chrome/Edge address bar install icon or Menu → Install app",
        quality: "Excellent",
        notes: "Appears in Start Menu, can pin to taskbar",
      },
      {
        id: "macos",
        platform: "macOS",
        how: "Chrome/Edge install icon → Dock. Safari 17+ → File → Add to Dock",
        quality: "Very good",
        notes: "Works well on Sonoma and later",
      },
      {
        id: "linux",
        platform: "ChromeOS / Linux",
        how: "Same as Chromium browsers",
        quality: "Good",
        notes: "—",
      },
    ],
  };
}

export function getPlatformsSections() {
  const rows = getInstallGuideRows();
  return [
    {
      id: "dashboard",
      title: "Dashboard",
      lead: "The Verodus CRM. Accounts, Journal, Payouts, and settings. Install this site — stay on dashboard.verodus.com.",
      cta: "Install Dashboard",
      href: "",
      phone: rows.phone,
      desktop: rows.desktop,
    },
    {
      id: "trading",
      title: "Verodus Trading",
      lead: "Optional second app for TradeHub and Platform 5. Open trade.verodus.com/dashboard in a normal tab, then follow the same steps. This page cannot install it for you.",
      cta: "Open Verodus Trading",
      href: TRADE_APP_HREF,
      phone: rows.phone,
      desktop: rows.desktop,
    },
  ];
}

/** @deprecated flattened view — prefer getPlatformsSections() */
export function getPlatformsCards() {
  return getPlatformsSections().flatMap((section) =>
    [...section.phone, ...section.desktop].map((row) => ({
      id: `${section.id}-${row.id}`,
      section: section.id,
      title: `${section.title} · ${row.platform}`,
      lead: row.how,
      href: section.href || undefined,
    }))
  );
}
