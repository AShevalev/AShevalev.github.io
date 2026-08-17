/**
 * Drop into the dashboard sidebar under Trading Resources.
 *
 * Live nav today: Economic Calendar, News.
 * Add Platforms as a third child. href must stay on dashboard.verodus.com
 * (same origin as the rest of the CRM) so the installed app never draws the
 * Chrome X / URL strip.
 *
 * Typical shape (lucide-react icons):
 *
 *   import { BarChart3, Calendar, Newspaper, MonitorSmartphone } from "lucide-react";
 *
 *   {
 *     title: "Trading Resources",
 *     icon: BarChart3,
 *     children: [
 *       { title: "Economic Calendar", href: "/trading-resources/economic-calendar", icon: Calendar },
 *       { title: "News", href: "/trading-resources/news", icon: Newspaper },
 *       { title: "Platforms", href: "/trading-resources/platforms", icon: MonitorSmartphone },
 *     ],
 *   }
 */

export const TRADING_RESOURCES_PLATFORMS_HREF = "/trading-resources/platforms";

export const tradingResourcesNav = {
  title: "Trading Resources",
  children: [
    { title: "Economic Calendar", href: "/trading-resources/economic-calendar" },
    { title: "News", href: "/trading-resources/news" },
    { title: "Platforms", href: TRADING_RESOURCES_PLATFORMS_HREF },
  ],
};
