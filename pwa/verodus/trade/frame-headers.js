/**
 * Allow the landing-page app shell (www.verodus.com/app) and the dashboard
 * origin to iframe TradeHub / Platform 5.
 */
export const FRAME_HEADERS = [
  {
    key: "Content-Security-Policy",
    value: "frame-ancestors 'self' https://dashboard.verodus.com",
  },
];
