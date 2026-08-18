import assert from "node:assert/strict";
import test from "node:test";
import { detectPlatform, getGuideCopy, getInstallGuide, getLandingInstallModalCopy, getPlatformsCards, getPlatformsSections, getTradingInstallModalCopy, isAccountScopedPath, landingInstallPathLabel, recommendedInstallSurface, resolveInstallAction } from "../pwa/platform.js";

const UA = {
  iosSafari:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
  iosChrome:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/123.0.6312.52 Mobile/15E148 Safari/604.1",
  iosFirefox:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/124.0 Mobile/15E148 Safari/605.1.15",
  androidChrome:
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
  androidEdge:
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36 EdgA/123.0.0.0",
  androidSamsung:
    "Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
  androidFirefox:
    "Mozilla/5.0 (Android 14; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
  desktopFirefox:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
  desktopChrome:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
  desktopSafari:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
};

test("iOS Safari, Chrome, and Firefox all use the Share-sheet guide", () => {
  for (const userAgent of [UA.iosSafari, UA.iosChrome, UA.iosFirefox]) {
    assert.equal(getInstallGuide({ userAgent }), "ios");
    assert.equal(detectPlatform({ userAgent }).ios, true);
  }
});

test("iPadOS desktop UA with touch is treated as iOS", () => {
  assert.equal(
    getInstallGuide({
      userAgent:
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
      platform: "MacIntel",
      maxTouchPoints: 5,
    }),
    "ios"
  );
});

test("Android Chrome uses native prompt when beforeinstallprompt fired", () => {
  assert.equal(
    getInstallGuide({ userAgent: UA.androidChrome, hasNativePrompt: true }),
    "native"
  );
});

test("Android Chrome falls back to the menu guide before the prompt exists", () => {
  assert.equal(getInstallGuide({ userAgent: UA.androidChrome }), "android");
});

test("Samsung and Edge Android use native when the prompt is captured", () => {
  assert.equal(
    getInstallGuide({ userAgent: UA.androidSamsung, hasNativePrompt: true }),
    "native"
  );
  assert.equal(
    getInstallGuide({ userAgent: UA.androidEdge, hasNativePrompt: true }),
    "native"
  );
});

test("Firefox Android never claims a native prompt path without one", () => {
  assert.equal(getInstallGuide({ userAgent: UA.androidFirefox }), "firefox-android");
});

test("Firefox desktop cannot install and gets a phone-first guide", () => {
  assert.equal(getInstallGuide({ userAgent: UA.desktopFirefox }), "firefox-desktop");
});

test("Safari on a Mac uses Add to Dock, not the iPhone Share sheet", () => {
  assert.equal(getInstallGuide({ userAgent: UA.desktopSafari }), "safari-mac");
  assert.equal(detectPlatform({ userAgent: UA.desktopSafari }).safariMac, true);
  assert.equal(detectPlatform({ userAgent: UA.desktopChrome }).safariMac, false);
  const copy = getGuideCopy("safari-mac", "Verodus");
  assert.match(copy.title, /Dock/i);
  assert.match(copy.steps[1].text, /Add to Dock/i);
});

test("already-installed sessions hide the CTA", () => {
  assert.equal(
    getInstallGuide({ userAgent: UA.iosSafari, standalone: true }),
    "hidden"
  );
  assert.equal(
    getInstallGuide({ userAgent: UA.androidChrome, displayModeStandalone: true }),
    "hidden"
  );
});

test("experimental navigator.install counts as native", () => {
  assert.equal(
    getInstallGuide({ userAgent: UA.desktopChrome, hasWebInstall: true }),
    "native"
  );
});

test("guide copy interpolates the app name as plain text", () => {
  const copy = getGuideCopy("ios", "Verodus");
  assert.match(copy.title, /Verodus/);
  assert.equal(copy.steps.length, 3);
  assert.match(copy.steps[1].text, /Add to Home Screen/i);
});

test("account cuids are detected and must not be start_url", () => {
  assert.equal(
    isAccountScopedPath("/tradehub/cmsu4y2u9000604ju8pad5x4j"),
    true
  );
  assert.equal(
    isAccountScopedPath("/p5/cmswfrqqb000204l7pnxhhj3w"),
    true
  );
  assert.equal(isAccountScopedPath("/tradehub"), false);
  assert.equal(isAccountScopedPath("/dashboard"), false);
});

test("homepage store pills redirect to the dashboard origin", () => {
  assert.equal(
    resolveInstallAction({
      currentHref: "https://www.verodus.com/",
      installUrl: "https://dashboard.verodus.com/dashboard?install=1",
    }),
    "redirect"
  );
  assert.equal(
    resolveInstallAction({
      currentHref: "https://dashboard.verodus.com/dashboard?install=1",
      installUrl: "https://dashboard.verodus.com/dashboard?install=1",
    }),
    "prompt-here"
  );
});

test("landing-page pills install www.verodus.com in place", () => {
  assert.equal(
    resolveInstallAction({
      currentHref: "https://www.verodus.com/",
      installUrl: "",
    }),
    "prompt-here"
  );
});

test("landing modal copy points at Dashboard → Trading Resources → Platforms", () => {
  const copy = getLandingInstallModalCopy();
  assert.equal(landingInstallPathLabel(), "Dashboard → Trading Resources → Platforms");
  assert.match(copy.lead, /Dashboard → Trading Resources → Platforms/);
  assert.match(copy.lead, /Android, Mobile, Desktop, or Safari/);
  assert.equal(copy.href, "https://dashboard.verodus.com/trading-resources/platforms");
});

test("Chrome on iPhone is iOS, not Android", () => {
  assert.equal(recommendedInstallSurface({ userAgent: UA.iosChrome }), "ios");
  assert.equal(recommendedInstallSurface({ userAgent: UA.iosSafari }), "ios");
  assert.equal(recommendedInstallSurface({ userAgent: UA.androidChrome }), "android");
  assert.equal(recommendedInstallSurface({ userAgent: UA.desktopChrome }), "desktop");
  assert.equal(recommendedInstallSurface({ userAgent: UA.desktopSafari }), "desktop");
});

test("Platforms is two apps each with iOS, Android, and Desktop", () => {
  const sections = getPlatformsSections();
  assert.deepEqual(
    sections.map((section) => section.id),
    ["dashboard", "trading"]
  );
  assert.deepEqual(
    sections[0].devices.map((device) => device.id),
    ["ios", "android", "desktop"]
  );
  assert.equal(sections[1].devices[0].href, "https://trade.verodus.com/dashboard");
  const cards = getPlatformsCards();
  assert.deepEqual(
    cards.map((card) => card.id),
    [
      "dashboard-ios",
      "dashboard-android",
      "dashboard-desktop",
      "trading-ios",
      "trading-android",
      "trading-desktop",
    ]
  );
});

test("trading install modal has instructions and a TradeHub link", () => {
  const copy = getTradingInstallModalCopy("ios");
  assert.match(copy.title, /iPhone/i);
  assert.match(copy.lead, /Chrome on iPhone is still iOS/i);
  assert.equal(copy.href, "https://trade.verodus.com/dashboard");
  assert.equal(copy.cta, "Open TradeHub");
});
