/**
 * Dashboard-only install. Host as /js/install.js on dashboard.verodus.com.
 *
 * Trading Resources → Platforms cards:
 *   [data-install-app][data-install-platform="android"|"mobile"|"desktop"|"safari"|"trading"]
 *
 * Android / Desktop on Chromium: native beforeinstallprompt when available.
 * Mobile (iPhone): Share → Add to Home Screen.
 * Safari (Mac): File → Add to Dock.
 * Trading: modal with instructions + link to trade.verodus.com (cannot auto-install).
 */
(function () {
  var deferred = null;
  var sheet = null;

  var COPY = {
    android: {
      title: "Install on Android",
      lead: "Chrome, Edge, or Samsung Internet on your phone or tablet.",
      steps: [
        "Tap Install on Android if Chrome shows a prompt.",
        "Or open the browser menu (three dots) → Install app.",
        "Open Verodus from your home screen.",
      ],
    },
    mobile: {
      title: "Add to iPhone or iPad",
      lead: "Works in Safari, Chrome, Firefox, and Edge on iOS.",
      steps: [
        "Tap Share in the toolbar (the square with the arrow).",
        "Scroll and tap Add to Home Screen.",
        "Tap Add. The icon lands next to your other apps.",
      ],
    },
    desktop: {
      title: "Install on desktop",
      lead: "Use Chrome or Edge on Windows, Mac, or Chromebook.",
      steps: [
        "Click Install Verodus in the address bar.",
        "Or open the browser menu → Install Verodus.",
        "Open it from your dock, taskbar, or Start menu.",
      ],
    },
    safari: {
      title: "Add to the Dock in Safari",
      lead: "Safari on a Mac. macOS 14 Sonoma or newer (Safari 17+).",
      steps: [
        "Open this page in Safari (not Chrome).",
        "File → Add to Dock. Or the share button in the toolbar → Add to Dock.",
        "Open Verodus from the Dock like any other Mac app.",
      ],
    },
    trading: {
      title: "Install the trading app",
      lead: "Chrome can only install the site you are on. Open TradeHub in the browser, then install there. This does not happen automatically.",
      steps: [
        "Tap Open TradeHub. Use Chrome or Safari — a normal tab, not only the Dashboard window.",
        "When TradeHub loads: Chrome/Edge → Install in the address bar. iPhone → Share → Add to Home Screen. Safari on a Mac → File → Add to Dock.",
        "Open it from your home screen or Dock. TradeHub and Platform 5 are the same trading app.",
      ],
      href: "https://trade.verodus.com/dashboard",
      linkCta: "Open TradeHub",
    },
  };

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {});
    });
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferred = event;
  });

  window.addEventListener("appinstalled", function () {
    deferred = null;
    markInstalled();
  });

  function ios() {
    var ua = navigator.userAgent || "";
    return (
      /iPhone|iPad|iPod/i.test(ua) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1)
    );
  }

  function safariMac() {
    var ua = navigator.userAgent || "";
    if (ios()) return false;
    if (/android/i.test(ua)) return false;
    var safari =
      /Safari/i.test(ua) &&
      !/Chrome|CriOS|Chromium|Edg|OPR|FxiOS|Firefox/i.test(ua);
    return Boolean(safari && /Macintosh/i.test(ua));
  }

  function android() {
    return /android/i.test(navigator.userAgent || "");
  }

  function standalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches ||
      navigator.standalone === true
    );
  }

  function markInstalled() {
    var root = document.querySelector(".v-platforms");
    if (root) root.classList.add("is-installed");
  }

  function ensureSheet() {
    if (sheet) return sheet;
    var wrap = document.createElement("div");
    wrap.className = "v-platforms-modal";
    wrap.hidden = true;
    wrap.innerHTML =
      '<button type="button" class="v-platforms-modal__backdrop" aria-label="Dismiss"></button>' +
      '<div class="v-platforms-modal__sheet" role="dialog" aria-modal="true" aria-labelledby="v-install-title" tabindex="-1">' +
      '<div class="v-platforms-modal__handle" aria-hidden="true"></div>' +
      '<h2 id="v-install-title"></h2>' +
      '<p class="v-platforms-modal__lead"></p>' +
      '<ol class="v-platforms-modal__steps"></ol>' +
      '<div class="v-platforms-modal__actions">' +
      '<a class="v-platforms-modal__cta v-platforms-modal__link" hidden target="_blank" rel="noopener noreferrer">Open TradeHub</a>' +
      '<button type="button" class="v-platforms-modal__done">Got it</button>' +
      "</div></div>";
    document.body.appendChild(wrap);
    wrap.querySelector(".v-platforms-modal__backdrop").addEventListener("click", closeSheet);
    wrap.querySelector(".v-platforms-modal__done").addEventListener("click", closeSheet);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && sheet && !sheet.hidden) closeSheet();
    });
    sheet = wrap;
    return wrap;
  }

  function closeSheet() {
    if (sheet) sheet.hidden = true;
  }

  function showCopy(kind) {
    var data = COPY[kind] || COPY.desktop;
    var el = ensureSheet();
    el.querySelector("#v-install-title").textContent = data.title;
    el.querySelector(".v-platforms-modal__lead").textContent = data.lead;
    var list = el.querySelector(".v-platforms-modal__steps");
    list.innerHTML = "";
    data.steps.forEach(function (step) {
      var li = document.createElement("li");
      li.textContent = step;
      list.appendChild(li);
    });
    var link = el.querySelector(".v-platforms-modal__link");
    var done = el.querySelector(".v-platforms-modal__done");
    if (data.href) {
      link.hidden = false;
      link.setAttribute("href", data.href);
      link.textContent = data.linkCta || "Open TradeHub";
      done.textContent = "Not now";
      done.classList.add("v-platforms-modal__dismiss");
    } else {
      link.hidden = true;
      link.removeAttribute("href");
      done.textContent = "Got it";
      done.classList.remove("v-platforms-modal__dismiss");
    }
    el.hidden = false;
    var dialog = el.querySelector(".v-platforms-modal__sheet");
    if (dialog && dialog.focus) dialog.focus();
  }

  function canNative(kind) {
    if (!deferred) return false;
    if (kind === "mobile" || kind === "safari" || kind === "trading") return false;
    if (kind === "android") return android() && !ios();
    if (kind === "desktop") return !android() && !ios() && !safariMac();
    return !safariMac();
  }

  function promptNative() {
    deferred.prompt();
    return deferred.userChoice.finally(function () {
      deferred = null;
    });
  }

  if (standalone()) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", markInstalled);
    } else {
      markInstalled();
    }
  }

  document.addEventListener("click", function (event) {
    var btn = event.target.closest && event.target.closest("[data-install-app]");
    if (!btn) return;
    event.preventDefault();

    var kind = btn.getAttribute("data-install-platform") || "";
    if (kind === "trading") {
      showCopy("trading");
      return;
    }
    if (standalone()) return;

    if (canNative(kind) || (!kind && deferred)) {
      promptNative();
      return;
    }
    if (kind) {
      showCopy(kind);
      return;
    }
    if (ios()) {
      showCopy("mobile");
      return;
    }
    if (safariMac()) {
      showCopy("safari");
      return;
    }
    if (deferred) {
      promptNative();
      return;
    }
    showCopy(android() ? "android" : "desktop");
  });
})();
