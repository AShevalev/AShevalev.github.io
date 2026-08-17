/**
 * Merge into dashboard app/layout.jsx (or app/layout.tsx).
 * Apple tags + manifest belong in <head>; InAppLaunches rewrites leftover
 * TradeHub / P5 clicks. /js/install.js registers the service worker.
 */
import Script from "next/script";
import InAppLaunches from "@/components/InAppLaunches";

export const metadata = {
  applicationName: "Verodus",
  appleWebApp: {
    capable: true,
    title: "Verodus",
    statusBarStyle: "black-translucent",
  },
  icons: { apple: "/icons/apple-touch-icon.png" },
  manifest: "/manifest.webmanifest",
  other: { "mobile-web-app-capable": "yes" },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#07003B",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="stylesheet" href="/css/install.css" />
      </head>
      <body>
        <InAppLaunches />
        {children}
        <Script src="/js/install.js" strategy="afterInteractive" />
      </body>
    </html>
  );
}
