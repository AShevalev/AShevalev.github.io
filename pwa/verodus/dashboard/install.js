/**
 * Dashboard-only install. Host as /js/install.js on dashboard.verodus.com.
 */
(function () {
  var deferred = null;

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {});
    });
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferred = event;
  });

  function ios() {
    var ua = navigator.userAgent || "";
    return (
      /iPhone|iPad|iPod/i.test(ua) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1)
    );
  }

  function standalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches ||
      navigator.standalone === true
    );
  }

  document.addEventListener("click", function (event) {
    var btn = event.target.closest && event.target.closest("[data-install-app]");
    if (!btn) return;
    if (standalone()) return;
    if (deferred) {
      event.preventDefault();
      deferred.prompt();
      deferred.userChoice.finally(function () {
        deferred = null;
      });
      return;
    }
    if (ios()) {
      event.preventDefault();
      window.alert(
        "Add Verodus to your Home Screen:\n1. Tap Share\n2. Add to Home Screen\n3. Tap Add"
      );
    }
  });
})();
