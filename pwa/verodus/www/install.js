/**
 * Homepage store pills on www.verodus.com.
 * Do not install this origin. Do not open Play / App Store.
 * Open a modal: install from Dashboard → Trading Resources → Platforms.
 *
 * Host as /js/install.js (classic script, no modules).
 * Pills: <a class="v-store-pill" href="https://dashboard.verodus.com/trading-resources/platforms">
 */
(function () {
  var HREF = "https://dashboard.verodus.com/trading-resources/platforms";
  var SELECTOR = ".v-store-pill, [data-install-app], [data-open-platforms-modal]";
  var modal = null;
  var lastFocus = null;

  function ensureModal() {
    if (modal) return modal;
    var wrap = document.createElement("div");
    wrap.className = "v-platforms-modal";
    wrap.hidden = true;
    wrap.innerHTML =
      '<button type="button" class="v-platforms-modal__backdrop" aria-label="Dismiss"></button>' +
      '<div class="v-platforms-modal__sheet" role="dialog" aria-modal="true" aria-labelledby="v-platforms-title" tabindex="-1">' +
      '<div class="v-platforms-modal__handle" aria-hidden="true"></div>' +
      '<h2 id="v-platforms-title">Install Verodus from the dashboard</h2>' +
      '<p class="v-platforms-modal__lead">Install from Dashboard → Trading Resources → Platforms. Choose Android, Mobile, Desktop, or Safari.</p>' +
      '<ol class="v-platforms-modal__path">' +
      "<li>Dashboard</li>" +
      "<li>Trading Resources</li>" +
      "<li>Platforms</li>" +
      "</ol>" +
      '<div class="v-platforms-modal__actions">' +
      '<a class="v-platforms-modal__cta" href="' +
      HREF +
      '">Open dashboard</a>' +
      '<button type="button" class="v-platforms-modal__dismiss">Not now</button>' +
      "</div></div>";
    document.body.appendChild(wrap);
    wrap.querySelector(".v-platforms-modal__backdrop").addEventListener("click", close);
    wrap.querySelector(".v-platforms-modal__dismiss").addEventListener("click", close);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && modal && !modal.hidden) close();
    });
    modal = wrap;
    return modal;
  }

  function open() {
    lastFocus = document.activeElement;
    var el = ensureModal();
    el.hidden = false;
    var sheet = el.querySelector(".v-platforms-modal__sheet");
    if (sheet && sheet.focus) sheet.focus();
  }

  function close() {
    if (!modal) return;
    modal.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener("click", function (event) {
    var pill = event.target.closest && event.target.closest(SELECTOR);
    if (!pill) return;
    event.preventDefault();
    open();
  });
})();
