/**
 * Cross-browser Add to Home Screen from a CTA.
 *
 * Chromium (Chrome / Edge / Samsung / Opera): native beforeinstallprompt.
 * iOS (Safari and every other browser on iOS 16.4+): Share → Add to Home Screen.
 * Firefox Android: menu → Install.
 * Everywhere else: instruction sheet.
 *
 * Usage:
 *   import { bindInstallCta } from "./add-to-home-screen.js";
 *   bindInstallCta({ selector: "[data-install-app]", appName: "Verodus" });
 */

import {
  getGuideCopy,
  getInstallGuide,
  readBrowserEnv,
  resolveInstallAction,
} from "./platform.js";

const ICONS = {
  share: `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4"/><path d="m8 8 4-4 4 4"/><path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"/></svg>`,
  menu: `<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><circle cx="12" cy="5" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="12" cy="19" r="1.8"/></svg>`,
  plus: `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/></svg>`,
  check: `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg>`,
};

const HOME_ICON = `<svg class="aths-cta__icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1z"/></svg>`;

/**
 * @typedef {object} BindOptions
 * @property {string} [selector] Buttons to bind. Default `[data-install-app]`
 * @property {string} [appName]
 * @property {string} [serviceWorkerUrl] Register this SW so Chromium will install. Default `/sw.js`
 * @property {boolean} [registerServiceWorker]
 * @property {string} [installUrl] If set to another origin (the dashboard), the CTA redirects there instead of installing the current site.
 * @property {string} [manifestId] Passed to navigator.install() when installing another origin.
 * @property {boolean} [styleButtons] Add gold CTA chrome. Default true. Set false for existing store pills.
 * @property {string} [autoPromptParam] Query param that auto-opens the prompt. Default `install`
 * @property {string} [afterInstallHref] Where to go after a successful install (landing → `/app`)
 * @property {ParentNode} [root]
 * @property {Window} [win]
 */

export function bindInstallCta(options = {}) {
  const win = options.win || window;
  const doc = win.document;
  const root = options.root || doc;
  const appName = options.appName || "Verodus";
  const selector = options.selector || "[data-install-app]";
  const registerSw = options.registerServiceWorker !== false;
  const swUrl = options.serviceWorkerUrl || "/sw.js";
  const installUrl = options.installUrl || "";
  const manifestId = options.manifestId || "";
  const styleButtons = options.styleButtons !== false;
  const autoPromptParam = options.autoPromptParam || "install";
  const afterInstallHref = options.afterInstallHref || "";

  /** @type {any} */
  let deferredPrompt = null;
  let sheetEl = null;
  let lastFocus = null;

  const buttons = () => [...root.querySelectorAll(selector)];

  function env() {
    const snapshot = readBrowserEnv(win);
    snapshot.hasNativePrompt = Boolean(deferredPrompt);
    return snapshot;
  }

  function syncButtons() {
    const snapshot = env();
    const guide = getInstallGuide(snapshot);
    const action = resolveInstallAction({
      currentHref: win.location && win.location.href,
      installUrl,
      installed: snapshot.standalone || snapshot.displayModeStandalone || snapshot.displayModeFullscreen,
    });
    const hide = guide === "hidden" && action !== "redirect";
    for (const btn of buttons()) {
      btn.hidden = hide;
      btn.classList.toggle("is-hidden", hide);
      btn.setAttribute("aria-hidden", hide ? "true" : "false");
      if (!btn.dataset.athsBound) decorateButton(btn);
    }
  }

  function decorateButton(btn) {
    btn.dataset.athsBound = "1";
    if (styleButtons) {
      btn.classList.add("aths-cta");
      if (!btn.querySelector(".aths-cta__icon")) {
        btn.insertAdjacentHTML("afterbegin", HOME_ICON);
      }
    }
    btn.addEventListener("click", (event) => {
      event.preventDefault();
      void promptInstall();
    });
  }

  function ensureSheet() {
    if (sheetEl) return sheetEl;
    const wrap = doc.createElement("div");
    wrap.className = "aths-root";
    wrap.hidden = true;
    wrap.innerHTML = `
      <button type="button" class="aths-backdrop" aria-label="Dismiss"></button>
      <div class="aths-sheet" role="dialog" aria-modal="true" aria-labelledby="aths-title" tabindex="-1">
        <div class="aths-handle" aria-hidden="true"></div>
        <h2 id="aths-title"></h2>
        <p class="aths-lead"></p>
        <ol class="aths-steps"></ol>
        <button type="button" class="aths-done">Got it</button>
      </div>
    `;
    doc.body.appendChild(wrap);
    wrap.querySelector(".aths-backdrop").addEventListener("click", closeSheet);
    wrap.querySelector(".aths-done").addEventListener("click", closeSheet);
    wrap.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeSheet();
    });
    sheetEl = wrap;
    return wrap;
  }

  function renderSheet(guide) {
    const copy = getGuideCopy(guide, appName);
    const wrap = ensureSheet();
    wrap.querySelector("#aths-title").textContent = copy.title;
    wrap.querySelector(".aths-lead").textContent = copy.lead;
    const list = wrap.querySelector(".aths-steps");
    list.replaceChildren();
    for (const step of copy.steps) {
      const li = doc.createElement("li");
      const icon = ICONS[step.icon] || ICONS.plus;
      li.innerHTML = `<span class="aths-step-icon">${icon}</span><p></p>`;
      li.querySelector("p").textContent = step.text;
      list.appendChild(li);
    }
  }

  function openSheet(guide) {
    renderSheet(guide);
    lastFocus = doc.activeElement;
    const wrap = ensureSheet();
    wrap.hidden = false;
    wrap.querySelector(".aths-sheet").focus();
  }

  function closeSheet() {
    if (!sheetEl) return;
    sheetEl.hidden = true;
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  async function promptInstall() {
    const guide = getInstallGuide(env());
    if (guide === "hidden") return "dismissed";

    const action = resolveInstallAction({
      currentHref: win.location && win.location.href,
      installUrl,
      installed: guide === "hidden",
    });

    if (action === "redirect") {
      const nav = win.navigator;
      if (typeof nav.install === "function") {
        try {
          if (manifestId) await nav.install(installUrl, manifestId);
          else await nav.install(installUrl);
          return "accepted";
        } catch {
          // Fall through to a same-window navigation on the dashboard origin.
        }
      }
      win.location.assign(installUrl);
      return "redirect";
    }

    if (deferredPrompt) {
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      deferredPrompt = null;
      syncButtons();
      if (choice.outcome === "accepted") goAfterInstall();
      return choice.outcome;
    }

    const nav = win.navigator;
    if (typeof nav.install === "function") {
      try {
        await nav.install();
        return "accepted";
      } catch {
        // Origin trial / user cancel — fall through to the sheet.
      }
    }

    openSheet(guide === "native" ? "android" : guide);
    return "instructions";
  }

  function goAfterInstall() {
    if (!afterInstallHref) return;
    try {
      win.location.assign(afterInstallHref);
    } catch {
      // Ignore if navigation is blocked.
    }
  }

  win.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredPrompt = event;
    syncButtons();
  });

  win.addEventListener("appinstalled", () => {
    deferredPrompt = null;
    closeSheet();
    syncButtons();
    goAfterInstall();
  });

  if (registerSw && navSupportsSw(win)) {
    const register = () => {
      win.navigator.serviceWorker.register(swUrl).catch(() => {});
    };
    if (doc.readyState === "complete") register();
    else win.addEventListener("load", register, { once: true });
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", syncButtons, { once: true });
  } else {
    syncButtons();
  }

  try {
    const params = new URLSearchParams(win.location.search);
    if (params.has(autoPromptParam) && getInstallGuide(env()) !== "hidden") {
      win.setTimeout(() => void promptInstall(), 400);
    }
  } catch {
    // Ignore missing location in tests.
  }

  return {
    promptInstall,
    getGuide: () => getInstallGuide(env()),
    syncButtons,
  };
}

function navSupportsSw(win) {
  return Boolean(win.navigator && win.navigator.serviceWorker);
}

export {
  getGuideCopy,
  getInstallGuide,
  readBrowserEnv,
  resolveInstallAction,
};
