/**
 * One-file landing install. Host as /js/install.js (classic script, no modules).
 * Pills: <a class="v-store-pill" href="/app">
 */
(function () {
  var APP = "/app";
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

  window.addEventListener("appinstalled", function () {
    deferred = null;
    window.location.assign(APP);
  });

  function ios() {
    var ua = navigator.userAgent || "";
    var iPhone = /iPhone|iPad|iPod/i.test(ua);
    var iPadOs = navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1;
    return iPhone || iPadOs;
  }

  function standalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches ||
      navigator.standalone === true
    );
  }

  function onPill(event) {
    if (standalone()) {
      event.preventDefault();
      window.location.assign(APP);
      return;
    }
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
    // Android without a prompt yet: follow href=/app (same origin).
  }

  document.addEventListener("click", function (event) {
    var pill = event.target.closest && event.target.closest(".v-store-pill, [data-install-app]");
    if (pill) onPill(event);
  });
})();
