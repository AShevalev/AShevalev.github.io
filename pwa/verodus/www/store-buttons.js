/**
 * www.verodus.com homepage store pills.
 *
 * Do not install the marketing site. Do not send people to Play Store / App Store.
 * Send them to dashboard.verodus.com so Chrome can install THAT origin as standalone
 * (no Custom Tab bar). iOS Add to Home Screen must also happen on this origin.
 */
import { bindInstallCta } from "../../add-to-home-screen.js";

bindInstallCta({
  selector: ".v-store-pill, [data-install-app]",
  appName: "Verodus",
  registerServiceWorker: false,
  styleButtons: false,
  installUrl: "https://dashboard.verodus.com/dashboard?install=1",
  manifestId: "https://dashboard.verodus.com/",
});
