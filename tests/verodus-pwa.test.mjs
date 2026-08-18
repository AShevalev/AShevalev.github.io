import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { isAccountScopedPath } from "../pwa/platform.js";

function readJson(path) {
  return JSON.parse(readFileSync(new URL(path, import.meta.url), "utf8"));
}

test("dashboard PWA is standalone and does not pin an account id", () => {
  const manifest = readJson("../pwa/verodus/dashboard/manifest.webmanifest");
  assert.equal(manifest.display, "standalone");
  assert.equal(manifest.id, "https://dashboard.verodus.com/");
  assert.equal(manifest.start_url.startsWith("/dashboard"), true);
  assert.equal(isAccountScopedPath(manifest.start_url), false);
  const origins = manifest.scope_extensions.map((item) => item.origin);
  assert.deepEqual(origins, ["https://trade.verodus.com"]);
});

test("trade start_url is /dashboard without a cuid", () => {
  const manifest = readJson("../pwa/verodus/trade/manifest.webmanifest");
  assert.equal(manifest.display, "standalone");
  assert.equal(isAccountScopedPath(manifest.start_url), false);
  assert.match(manifest.start_url, /^\/dashboard/);
});

test("origin association opts trade into the dashboard app id", () => {
  const file = readJson(
    "../pwa/verodus/trade/.well-known/web-app-origin-association"
  );
  assert.ok(file["https://dashboard.verodus.com/"]);
  assert.ok(
    file.web_apps.some((app) => app.web_app_identity === "https://dashboard.verodus.com/")
  );
});

test("landing-page PWA starts at /app on www.verodus.com", () => {
  const manifest = readJson("../pwa/verodus/www/manifest.json");
  assert.equal(manifest.id, "https://www.verodus.com/");
  assert.equal(manifest.display, "standalone");
  assert.match(manifest.start_url, /^\/app/);
  assert.equal(isAccountScopedPath(manifest.start_url), false);
});

test("landing pills open a modal that points at Dashboard Platforms", () => {
  const src = readFileSync(new URL("../pwa/verodus/www/install.js", import.meta.url), "utf8");
  assert.match(src, /Dashboard → Trading Resources → Platforms/);
  assert.match(src, /Android, Mobile, Desktop, or Safari/);
  assert.match(src, /https:\/\/dashboard\.verodus\.com\/trading-resources\/platforms/);
  assert.doesNotMatch(src, /serviceWorker/);
  assert.doesNotMatch(src, /beforeinstallprompt/);
  assert.doesNotMatch(src, /play\.google|apps\.apple/);
});

test("landing store-button markup does not install www or open the stores", () => {
  const html = readFileSync(
    new URL("../pwa/verodus/www/store-buttons.html", import.meta.url),
    "utf8"
  );
  assert.match(html, /data-open-platforms-modal/);
  assert.match(html, /https:\/\/dashboard\.verodus\.com\/trading-resources\/platforms/);
  assert.doesNotMatch(html, /play\.google|apps\.apple|href="\/app"/);
});

test("dashboard sidebar adds Platforms under Trading Resources", () => {
  const src = readFileSync(
    new URL("../pwa/verodus/dashboard/sidebar-trading-resources.jsx", import.meta.url),
    "utf8"
  );
  assert.match(src, /title: "Trading Resources"/);
  assert.match(src, /title: "Economic Calendar"/);
  assert.match(src, /title: "News"/);
  assert.match(src, /title: "Platforms"/);
  assert.match(src, /href: "\/trading-resources\/platforms"/);
});

test("Platforms page has Dashboard and Trading, each with iOS Android Desktop", () => {
  const src = readFileSync(
    new URL("../pwa/verodus/dashboard/PlatformsPage.jsx", import.meta.url),
    "utf8"
  );
  assert.match(src, /id: "dashboard"/);
  assert.match(src, /id: "trading"/);
  assert.match(src, /id: "ios"/);
  assert.match(src, /id: "android"/);
  assert.match(src, /id: "desktop"/);
  assert.match(src, /data-install-section=\{section\.id\}/);
  assert.match(src, /Chrome on iOS has no Android-style install prompt/);
});

test("dashboard install script handles per-platform CTAs", () => {
  const src = readFileSync(
    new URL("../pwa/verodus/dashboard/install.js", import.meta.url),
    "utf8"
  );
  assert.match(src, /data-install-section/);
  assert.match(src, /Add to Home Screen/);
  assert.match(src, /Add to Dock/);
  assert.match(src, /trade\.verodus\.com\/dashboard/);
  assert.match(src, /v-platforms-modal__link/);
  assert.match(src, /CriOS/);
});

test("Safari on a Mac opens trade at the top level instead of an iframe", () => {
  const frame = readFileSync(
    new URL("../pwa/verodus/dashboard/PlatformFrame.jsx", import.meta.url),
    "utf8"
  );
  const intercept = readFileSync(
    new URL("../pwa/verodus/dashboard/intercept-launches.js", import.meta.url),
    "utf8"
  );
  assert.match(frame, /shouldEmbedTrade/);
  assert.match(intercept, /isSafariMac/);
});

test("dashboard-as-app start_url is the CRM not the landing page", () => {
  const manifest = readJson("../pwa/verodus/dashboard/manifest.webmanifest");
  assert.match(manifest.start_url, /^\/dashboard/);
  assert.equal(manifest.scope, "/");
  assert.equal(manifest.display, "standalone");
});
