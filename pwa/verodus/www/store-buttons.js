/**
 * www.verodus.com homepage store pills.
 *
 * Do not install this origin (that makes Dashboard look like a website).
 * Do not send people to Play / App Store.
 * Open a modal: install from Dashboard → Trading Resources → Platforms.
 */
import "../lock-origin-entry.js";

const HREF = "https://dashboard.verodus.com/trading-resources/platforms";
const SELECTOR = ".v-store-pill, [data-install-app], [data-open-platforms-modal]";

let modal = null;
let lastFocus = null;

function ensureModal(doc) {
  if (modal) return modal;
  const wrap = doc.createElement("div");
  wrap.className = "v-platforms-modal";
  wrap.hidden = true;
  wrap.innerHTML = `
    <button type="button" class="v-platforms-modal__backdrop" aria-label="Dismiss"></button>
    <div class="v-platforms-modal__sheet" role="dialog" aria-modal="true" aria-labelledby="v-platforms-title" tabindex="-1">
      <div class="v-platforms-modal__handle" aria-hidden="true"></div>
      <h2 id="v-platforms-title">Install Verodus from the dashboard</h2>
      <p class="v-platforms-modal__lead">Install from Dashboard → Trading Resources → Platforms. Choose Android, Mobile, or Desktop.</p>
      <ol class="v-platforms-modal__path">
        <li>Dashboard</li>
        <li>Trading Resources</li>
        <li>Platforms</li>
      </ol>
      <div class="v-platforms-modal__actions">
        <a class="v-platforms-modal__cta" href="${HREF}">Open dashboard</a>
        <button type="button" class="v-platforms-modal__dismiss">Not now</button>
      </div>
    </div>
  `;
  doc.body.appendChild(wrap);
  wrap.querySelector(".v-platforms-modal__backdrop").addEventListener("click", close);
  wrap.querySelector(".v-platforms-modal__dismiss").addEventListener("click", close);
  doc.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal && !modal.hidden) close();
  });
  modal = wrap;
  return modal;
}

function open(doc) {
  lastFocus = doc.activeElement;
  const el = ensureModal(doc);
  el.hidden = false;
  el.querySelector(".v-platforms-modal__sheet")?.focus();
}

function close() {
  if (!modal) return;
  modal.hidden = true;
  lastFocus?.focus?.();
}

document.addEventListener("click", (event) => {
  const pill = event.target.closest?.(SELECTOR);
  if (!pill) return;
  event.preventDefault();
  open(document);
});
