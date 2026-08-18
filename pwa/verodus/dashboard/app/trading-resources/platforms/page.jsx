/**
 * Copy to dashboard Next.js:
 *   app/trading-resources/platforms/page.jsx
 *
 * Sidebar: add Platforms under Trading Resources (see sidebar-trading-resources.jsx).
 * Load /css/install.css + /js/install.js in the root layout.
 */
import PlatformsPage from "@/components/PlatformsPage";

export const metadata = {
  title: "Platforms",
  description: "Install Dashboard or Verodus Trading from Trading Resources.",
};

export default function TradingResourcesPlatformsPage() {
  return <PlatformsPage />;
}
