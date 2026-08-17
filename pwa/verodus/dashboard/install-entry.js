/**
 * Dashboard origin. Registers the SW, rewrites TradeHub / P5 launches so they
 * never leave this host, and opens the install prompt when ?install=1.
 */
import { bindInstallCta } from "../../add-to-home-screen.js";
import "./intercept-launches.js";
import "../lock-origin-entry.js";

bindInstallCta({
  selector: "[data-install-app]",
  appName: "Verodus",
  serviceWorkerUrl: "/sw.js",
  autoPromptParam: "install",
});
