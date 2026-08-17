/**
 * Allow www.verodus.com/app to iframe the CRM after a landing-page install.
 */
export const FRAME_HEADERS = [
  {
    key: "Content-Security-Policy",
    value: "frame-ancestors 'self' https://www.verodus.com https://verodus.com",
  },
];
