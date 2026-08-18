/**
 * Dashboard → Trading Resources → Platforms.
 * Two apps (Dashboard, Trading). Each has iOS, Android, Desktop.
 * Chrome on iPhone is iOS (Share sheet), not Android.
 */
import "./platforms.css";

const IOS_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="7" y="3" width="10" height="18" rx="2.2" />
    <path d="M11 18.5h2" strokeLinecap="round" />
  </svg>
);

const ANDROID_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
    <path d="M17.6 9.48 19.1 6.9a.5.5 0 0 0-.86-.5l-1.55 2.68A8.1 8.1 0 0 0 12 8.1a8.1 8.1 0 0 0-4.69.98L5.76 6.4a.5.5 0 1 0-.86.5l1.5 2.58A7.4 7.4 0 0 0 4 15.2v.4h16v-.4a7.4 7.4 0 0 0-2.4-5.72ZM8.2 13.4a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Zm7.6 0a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Z" />
  </svg>
);

const DESKTOP_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="3" y="4" width="18" height="12" rx="2" />
    <path d="M8 20h8M12 16v4" strokeLinecap="round" />
  </svg>
);

const ICONS = { ios: IOS_ICON, android: ANDROID_ICON, desktop: DESKTOP_ICON };

const DEVICES = [
  {
    id: "ios",
    title: "iOS",
    lead: "iPhone and iPad. Safari, Chrome, Firefox, and Edge all use Share → Add to Home Screen. Chrome on iPhone is not Android.",
    cta: "Show iOS steps",
  },
  {
    id: "android",
    title: "Android",
    lead: "Phone or tablet. Chrome, Edge, or Samsung Internet.",
    cta: "Show Android steps",
  },
  {
    id: "desktop",
    title: "Desktop",
    lead: "Chrome or Edge: Install. Safari on a Mac: Add to Dock. Firefox desktop cannot install.",
    cta: "Show desktop steps",
  },
];

const SECTIONS = [
  {
    id: "dashboard",
    title: "Dashboard",
    lead: "The Verodus CRM. Accounts, Journal, Payouts, and settings. Install this site.",
  },
  {
    id: "trading",
    title: "Trading",
    lead: "Optional second app for TradeHub and Platform 5. A short guide plus a link — it cannot install from this page.",
  },
];

export default function PlatformsPage() {
  return (
    <section className="v-platforms">
      <p className="v-platforms__done">Dashboard is already installed on this device. You can still add Trading.</p>
      <h1>Platforms</h1>
      <p className="v-platforms__lede">
        Two apps: Dashboard and Trading. Pick iOS, Android, or Desktop for each. If you are on an
        iPhone in Chrome, use iOS — Chrome on iOS has no Android-style install prompt.
      </p>
      <p className="v-platforms__hint" data-platforms-hint hidden></p>
      {SECTIONS.map((section) => (
        <section key={section.id} className="v-platforms__section" data-install-section={section.id}>
          <h2>{section.title}</h2>
          <p>{section.lead}</p>
          <div className="v-platforms__grid">
            {DEVICES.map((device) => (
              <article key={device.id} className="v-platforms__card" data-install-platform={device.id}>
                <div className="v-platforms__icon">{ICONS[device.id]}</div>
                <h3>{device.title}</h3>
                <p>{device.lead}</p>
                <button
                  type="button"
                  className="v-platforms__cta"
                  data-install-app
                  data-install-section={section.id}
                  data-install-platform={device.id}
                >
                  {device.cta}
                </button>
              </article>
            ))}
          </div>
        </section>
      ))}
    </section>
  );
}
