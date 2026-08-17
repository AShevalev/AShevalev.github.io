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

test("trade start_url is TradeHub without a cuid (covers Platform 5 on the same origin)", () => {
  const manifest = readJson("../pwa/verodus/trade/manifest.webmanifest");
  assert.equal(manifest.display, "standalone");
  assert.equal(isAccountScopedPath(manifest.start_url), false);
  assert.match(manifest.start_url, /^\/tradehub/);
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

test("practical install script stays on /app", () => {
  const src = readFileSync(new URL("../pwa/verodus/www/install.js", import.meta.url), "utf8");
  assert.match(src, /var APP = "\/app"/);
  assert.match(src, /beforeinstallprompt/);
});

test("dashboard-as-app start_url is the CRM not the landing page", () => {
  const manifest = readJson("../pwa/verodus/dashboard/manifest.webmanifest");
  assert.match(manifest.start_url, /^\/dashboard/);
  assert.equal(manifest.scope, "/");
  assert.equal(manifest.display, "standalone");
});
