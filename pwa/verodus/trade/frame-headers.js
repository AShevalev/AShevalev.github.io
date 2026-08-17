/**
 * Add to trade.verodus.com next.config.mjs so Dashboard can iframe TradeHub / P5.
 * Do not use X-Frame-Options: DENY.
 *
 * async headers() {
 *   return [{ source: "/:path*", headers: FRAME_HEADERS }];
 * }
 */
export const FRAME_HEADERS = [
  {
    key: "Content-Security-Policy",
    value: "frame-ancestors 'self' https://dashboard.verodus.com",
  },
];
