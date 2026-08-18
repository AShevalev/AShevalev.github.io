/**
 * Dashboard → Trading Resources → Platforms.
 * Two sections: Dashboard and Verodus Trading. Same install tables in each.
 */
import "./platforms.css";

const TRADE_HREF = "https://trade.verodus.com/dashboard";

const PHONE_ROWS = [
  {
    id: "android",
    platform: "Android",
    how: "Automatic install prompt + Menu → Install app / Add to Home screen",
    quality: "Excellent (almost native)",
    notes: "Chrome, Edge, Samsung Internet, Brave all support it well. Can become a WebAPK.",
  },
  {
    id: "ios",
    platform: "iOS / iPadOS",
    how: "Safari → Share → Add to Home Screen (also possible from Chrome/Edge on iOS 16.4+)",
    quality: "Good but manual",
    notes:
      "No automatic beforeinstallprompt. You must show clear instructions. Push notifications only work after install.",
  },
];

const DESKTOP_ROWS = [
  {
    id: "windows",
    platform: "Windows",
    how: "Chrome/Edge address bar install icon or Menu → Install app",
    quality: "Excellent",
    notes: "Appears in Start Menu, can pin to taskbar",
  },
  {
    id: "macos",
    platform: "macOS",
    how: "Chrome/Edge install icon → Dock. Safari 17+ → File → Add to Dock",
    quality: "Very good",
    notes: "Works well on Sonoma and later",
  },
  {
    id: "linux",
    platform: "ChromeOS / Linux",
    how: "Same as Chromium browsers",
    quality: "Good",
    notes: "—",
  },
];

function GuideTable({ caption, rows }) {
  return (
    <div className="v-platforms__table-wrap">
      <table className="v-platforms__table">
        <caption>{caption}</caption>
        <thead>
          <tr>
            <th scope="col">Platform</th>
            <th scope="col">How users install</th>
            <th scope="col">Quality of experience</th>
            <th scope="col">Notes</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} data-install-platform={row.id}>
              <th scope="row">{row.platform}</th>
              <td>{row.how}</td>
              <td>{row.quality}</td>
              <td>{row.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function PlatformsPage() {
  return (
    <section className="v-platforms">
      <p className="v-platforms__done">
        Dashboard is already installed on this device. You can still add Verodus Trading.
      </p>
      <h1>Platforms</h1>
      <p className="v-platforms__lede">
        Two apps. <strong>Dashboard</strong> is the CRM — install it on this site.{" "}
        <strong>Verodus Trading</strong> is TradeHub and Platform 5 — open{" "}
        <a href={TRADE_HREF}>https://trade.verodus.com/dashboard</a> in a normal browser tab, then
        install there.
      </p>
      <p className="v-platforms__hint" data-platforms-hint hidden></p>

      <section className="v-platforms__section" data-install-section="dashboard">
        <h2>Dashboard</h2>
        <p>The Verodus CRM. Accounts, Journal, Payouts, and settings. Stay on this site to install.</p>
        <GuideTable caption="Phone and tablet" rows={PHONE_ROWS} />
        <GuideTable caption="Desktop" rows={DESKTOP_ROWS} />
        <button
          type="button"
          className="v-platforms__cta"
          data-install-app
          data-install-section="dashboard"
        >
          Install Dashboard
        </button>
      </section>

      <section className="v-platforms__section" data-install-section="trading">
        <h2>Verodus Trading</h2>
        <p>
          Optional second app for TradeHub and Platform 5. Same install steps as Dashboard, but you
          must be on{" "}
          <a href={TRADE_HREF}>https://trade.verodus.com/dashboard</a>. This page cannot install it
          for you.
        </p>
        <GuideTable caption="Phone and tablet" rows={PHONE_ROWS} />
        <GuideTable caption="Desktop" rows={DESKTOP_ROWS} />
        <button
          type="button"
          className="v-platforms__cta"
          data-install-app
          data-install-section="trading"
        >
          Open Verodus Trading
        </button>
      </section>
    </section>
  );
}
