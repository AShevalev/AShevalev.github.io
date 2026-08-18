import assert from "node:assert/strict";
import test from "node:test";
import {
  isEmbedded,
  isOtherVerodusUrl,
  isSafariMac,
  shouldEmbedTrade,
  shouldLockOrigin,
} from "../pwa/verodus/lock-origin.js";

test("other Verodus hosts are treated as cross-app URLs", () => {
  assert.equal(
    isOtherVerodusUrl(
      "https://trade.verodus.com/tradehub/abc",
      "https://dashboard.verodus.com"
    ),
    true
  );
  assert.equal(
    isOtherVerodusUrl(
      "https://dashboard.verodus.com/dashboard",
      "https://www.verodus.com"
    ),
    true
  );
  assert.equal(
    isOtherVerodusUrl("https://www.verodus.com/app", "https://www.verodus.com"),
    false
  );
  assert.equal(
    isOtherVerodusUrl("https://accounts.google.com/", "https://www.verodus.com"),
    false
  );
});

test("origin lock is off inside an iframe and off in a normal browser tab", () => {
  const installedTop = {
    matchMedia: (query) => ({ matches: query.includes("standalone") }),
    navigator: { standalone: false },
  };
  installedTop.self = installedTop;
  installedTop.top = installedTop;
  assert.equal(isEmbedded(installedTop), false);
  assert.equal(shouldLockOrigin(installedTop), true);

  const iframe = {
    matchMedia: () => ({ matches: true }),
    navigator: { standalone: true },
  };
  iframe.self = iframe;
  iframe.top = installedTop;
  assert.equal(isEmbedded(iframe), true);
  assert.equal(shouldLockOrigin(iframe), false);

  const tab = {
    matchMedia: () => ({ matches: false }),
    navigator: { standalone: false },
  };
  tab.self = tab;
  tab.top = tab;
  assert.equal(shouldLockOrigin(tab), false);
});

const UA = {
  safariMac:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
  chromeMac:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
};

test("Safari on a Mac is detected and does not iframe trade", () => {
  const safariMac = {
    navigator: { userAgent: UA.safariMac, platform: "MacIntel", maxTouchPoints: 0 },
  };
  const chromeMac = {
    navigator: { userAgent: UA.chromeMac, platform: "MacIntel", maxTouchPoints: 0 },
  };
  const iPadOs = {
    navigator: {
      userAgent:
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
      platform: "MacIntel",
      maxTouchPoints: 5,
    },
  };

  assert.equal(isSafariMac(safariMac), true);
  assert.equal(isSafariMac(chromeMac), false);
  assert.equal(isSafariMac(iPadOs), false);
  assert.equal(shouldEmbedTrade(safariMac), false);
  assert.equal(shouldEmbedTrade(chromeMac), true);
});

test("Safari on a Mac does not lock origin even in a Dock web app", () => {
  const safariDock = {
    matchMedia: (query) => ({ matches: query.includes("standalone") }),
    navigator: {
      userAgent: UA.safariMac,
      platform: "MacIntel",
      maxTouchPoints: 0,
      standalone: false,
    },
  };
  safariDock.self = safariDock;
  safariDock.top = safariDock;
  assert.equal(shouldLockOrigin(safariDock), false);
});
