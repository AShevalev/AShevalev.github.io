/**
 * Dashboard-only install. Host as /js/install.js on dashboard.verodus.com.
 *
 * [data-install-app][data-install-section="dashboard"|"trading"]
 * [data-install-platform="ios"|"android"|"desktop"]
 *
 * Chrome on iPhone is iOS (Share), never the Android prompt.
 * Trading: modal + link to https://trade.verodus.com/dashboard (no auto-install).
 */
(function () {
  var TRADE = "https://trade.verodus.com/dashboard";
  var deferred = null;
  var sheet = null;

  var COPY = {
    "dashboard-ios": {
      title: "Add Dashboard to iPhone or iPad",
      lead: "Works in Safari, Chrome, Firefox, and Edge on iOS. Chrome on iPhone still uses Share — it is not the Android install.",
      steps: [
        "Stay on this Dashboard page.",
        "Tap Share in the toolbar (the square with the arrow).",
        "Tap Add to Home Screen, then Add.",
      ],
    },
    "dashboard-android": {
      title: "Install Dashboard on Android",
      lead: "Chrome, Edge, or Samsung Internet on your phone or tablet.",
      steps: [
        "Stay on this Dashboard page in Chrome (or Edge / Samsung Internet).",
        "Tap Install, or the browser menu → Install app.",
        "Open Verodus from your home screen.",
      ],
    },
    "dashboard-desktop": {
      title: "Install Dashboard on desktop",
      lead: "Windows, Mac, and Chromebook.",
      steps: [
        "Chrome or Edge: Install in the address bar, or the menu → Install Verodus.",
        "Safari on a Mac (macOS 14+): File → Add to Dock (or Share → Add to Dock).",
        "Firefox on desktop cannot install web apps — use Chrome, Edge, or Safari.",
      ],
    },
    "trading-ios": {
      title: "Install Trading on iPhone or iPad",
      lead: "Chrome on iPhone is still iOS — use Share, not the Android install. Open TradeHub first; this page cannot install it.",
      steps: [
        "Tap Open TradeHub. Use a normal Safari or Chrome tab.",
        "Tap Share → Add to Home Screen → Add.",
        "Open Trading from your home screen. TradeHub and Platform 5 are the same app.",
      ],
      href: TRADE,
      linkCta: "Open TradeHub",
    },
    "trading-android": {
      title: "Install Trading on Android",
      lead: "Open TradeHub in Chrome, Edge, or Samsung Internet, then install there.",
      steps: [
        "Tap Open TradeHub in Chrome (or Edge / Samsung Internet).",
        "Tap Install, or the browser menu → Install app.",
        "Open it from your home screen. TradeHub and Platform 5 are the same app.",
      ],
      href: TRADE,
      linkCta: "Open TradeHub",
    },
    "trading-desktop": {
      title: "Install Trading on desktop",
      lead: "Open TradeHub in a normal browser tab, then install there.",
      steps: [
        "Tap Open TradeHub.",
        "Chrome or Edge: Install in the address bar (or the menu → Install).",
        "Safari on a Mac (macOS 14+): File → Add to Dock.",
        "Firefox on desktop cannot install web apps — use Chrome, Edge, or Safari.",
      ],
      href: TRADE,
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

  function chromeIos() {
    return /CriOS/i.test(navigator.userAgent || "");
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

  function suggestedSurface() {
    if (ios()) return "ios";
    if (android()) return "android";
    return "desktop";
  }

  function normalizePlatform(value) {
    if (value === "mobile") return "ios";
    if (value === "safari") return "desktop";
    if (value === "ios" || value === "android" || value === "desktop") return value;
    return "";
  }

  function sheetKey(section, platform) {
    return section + "-" + platform;
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

  function markSuggested() {
    var surface = suggestedSurface();
    var cards = document.querySelectorAll(".v-platforms__card[data-install-platform]");
    cards.forEach(function (card) {
      card.classList.toggle("is-suggested", card.getAttribute("data-install-platform") === surface);
    });
    var hint = document.querySelector("[data-platforms-hint]");
    if (!hint) return;
    if (ios() && chromeIos()) {
      hint.hidden = false;
      hint.textContent =
        "You are on iPhone Chrome. Use iOS (Share → Add to Home Screen), not Android.";
    } else if (safariMac()) {
      hint.hidden = false;
      hint.textContent = "You are in Safari on a Mac. Use Desktop → Add to Dock.";
    } else {
      hint.hidden = true;
    }
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

  function showCopy(key) {
    var data = COPY[key] || COPY["dashboard-desktop"];
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

  function canNative(section, platform) {
    if (section !== "dashboard") return false;
    if (!deferred) return false;
    if (platform === "ios") return false;
    if (platform === "android") return android() && !ios();
    if (platform === "desktop") return !android() && !ios() && !safariMac();
    return false;
  }

  function promptNative() {
    deferred.prompt();
    return deferred.userChoice.finally(function () {
      deferred = null;
    });
  }

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    if (standalone()) markInstalled();
    markSuggested();
  });

  document.addEventListener("click", function (event) {
    var btn = event.target.closest && event.target.closest("[data-install-app]");
    if (!btn) return;
    event.preventDefault();

    var section = btn.getAttribute("data-install-section") || "dashboard";
    var platform = normalizePlatform(btn.getAttribute("data-install-platform") || "");
    if (btn.getAttribute("data-install-platform") === "trading") {
      section = "trading";
      platform = suggestedSurface();
    }
    if (!platform) platform = suggestedSurface();

    var key = sheetKey(section, platform);
    if (section === "trading") {
      showCopy(key);
      return;
    }
    if (standalone()) return;
    if (canNative(section, platform)) {
      promptNative();
      return;
    }
    showCopy(key);
  });
})();
