import assert from "node:assert/strict";
import test from "node:test";
import {
  isEmbedded,
  isOtherVerodusUrl,
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
