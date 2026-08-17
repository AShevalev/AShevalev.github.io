import assert from "node:assert/strict";
import test from "node:test";
import {
  parsePlatformUrl,
  toInAppUrl,
  toTradeEmbedSrc,
} from "../pwa/verodus/dashboard/same-origin.js";

test("trade.verodus.com TradeHub URL becomes a dashboard path", () => {
  assert.equal(
    toInAppUrl("https://trade.verodus.com/tradehub/cmsu4y2u9000604ju8pad5x4j"),
    "https://dashboard.verodus.com/tradehub/cmsu4y2u9000604ju8pad5x4j"
  );
});

test("trade.verodus.com Platform 5 URL becomes a dashboard path", () => {
  assert.equal(
    toInAppUrl("https://trade.verodus.com/p5/cmswfrqqb000204l7pnxhhj3w"),
    "https://dashboard.verodus.com/p5/cmswfrqqb000204l7pnxhhj3w"
  );
});

test("already in-app URLs stay on the dashboard origin", () => {
  assert.equal(
    toInAppUrl("https://dashboard.verodus.com/p5/cmswfrqqb000204l7pnxhhj3w"),
    "https://dashboard.verodus.com/p5/cmswfrqqb000204l7pnxhhj3w"
  );
});

test("iframe src still points at the trade origin", () => {
  assert.equal(
    toTradeEmbedSrc("/tradehub/cmsu4y2u9000604ju8pad5x4j"),
    "https://trade.verodus.com/tradehub/cmsu4y2u9000604ju8pad5x4j"
  );
  assert.equal(
    toTradeEmbedSrc("/p5/cmswfrqqb000204l7pnxhhj3w"),
    "https://trade.verodus.com/p5/cmswfrqqb000204l7pnxhhj3w"
  );
});

test("unrelated URLs are not rewritten", () => {
  assert.equal(toInAppUrl("https://www.verodus.com/"), null);
  assert.equal(parsePlatformUrl("https://dashboard.verodus.com/dashboard"), null);
});
