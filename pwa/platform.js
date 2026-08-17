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
 * - generic: last-resort menu instructions
 *
 * @param {Env} [env]
 * @returns {"hidden"|"native"|"ios"|"firefox-android"|"android"|"firefox-desktop"|"generic"}
 */
export function getInstallGuide(env = {}) {
  const p = detectPlatform(env);
  if (p.installed) return "hidden";
  if (env.hasNativePrompt || env.hasWebInstall) return "native";
  if (p.ios) return "ios";
  if (p.firefox && p.android) return "firefox-android";
  if (p.android) return "android";
  if (p.firefox) return "firefox-desktop";
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
