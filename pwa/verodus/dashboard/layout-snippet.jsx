/**
 * Copy into dashboard app/layout.jsx (or the root layout that wraps Dashboard).
 * Apple tags + manifest belong in <head>; InAppLaunches rewrites TradeHub / P5 clicks.
 */
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
      <body>
        <InAppLaunches />
        {children}
      </body>
    </html>
  );
}
