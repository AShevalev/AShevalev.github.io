/**
 * www.verodus.com homepage store pills.
 *
 * Most people install from the landing page. Install THIS origin, then open
 * /app (a shell that iframes Dashboard). Never send Chrome to dashboard.verodus.com
 * at the top level — that is the bar.
 */
import { bindInstallCta } from "../../add-to-home-screen.js";
import "./standalone-gate.js";
import "../lock-origin-entry.js";

bindInstallCta({
  selector: ".v-store-pill, [data-install-app]",
  appName: "Verodus",
  registerServiceWorker: true,
  serviceWorkerUrl: "/sw.js",
  styleButtons: false,
  afterInstallHref: "/app",
});
