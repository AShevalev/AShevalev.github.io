/**
 * Dashboard origin. Registers the SW and, when the URL has ?install=1
 * (homepage store pills), opens the native prompt or the iOS/Firefox sheet.
 */
import { bindInstallCta } from "../../add-to-home-screen.js";

bindInstallCta({
  selector: "[data-install-app]",
  appName: "Verodus",
  serviceWorkerUrl: "/sw.js",
  autoPromptParam: "install",
});
