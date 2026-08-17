/**
 * Copy to dashboard Next.js:
 *   app/trading-resources/platforms/page.jsx
 *
 * Sidebar: add Platforms under Trading Resources (see sidebar-trading-resources.jsx).
 * Load /js/install.js once in the root layout so the three CTAs can prompt.
 */
import PlatformsPage from "@/components/PlatformsPage";

export const metadata = {
  title: "Platforms",
  description: "Install Verodus on Android, iPhone, or desktop from Trading Resources.",
};

export default function TradingResourcesPlatformsPage() {
  return <PlatformsPage />;
}
