/**
 * Dashboard → Trading Resources → Platforms.
 * Copy to components/PlatformsPage.jsx next to platforms.css.
 *
 * Android / Mobile / Desktop CTAs use [data-install-app][data-install-platform].
 * Load /css/install.css + /js/install.js in the root layout.
 */
import "./platforms.css";
const ANDROID_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
    <path d="M17.6 9.48 19.1 6.9a.5.5 0 0 0-.86-.5l-1.55 2.68A8.1 8.1 0 0 0 12 8.1a8.1 8.1 0 0 0-4.69.98L5.76 6.4a.5.5 0 1 0-.86.5l1.5 2.58A7.4 7.4 0 0 0 4 15.2v.4h16v-.4a7.4 7.4 0 0 0-2.4-5.72ZM8.2 13.4a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Zm7.6 0a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Z" />
  </svg>
);

const MOBILE_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="7" y="3" width="10" height="18" rx="2.2" />
    <path d="M11 18.5h2" strokeLinecap="round" />
  </svg>
);

const DESKTOP_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="3" y="4" width="18" height="12" rx="2" />
    <path d="M8 20h8M12 16v4" strokeLinecap="round" />
  </svg>
);

const SAFARI_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <circle cx="12" cy="12" r="9" />
    <path d="m15 9-3 6-6 3 3-6 6-3z" />
  </svg>
);

const TRADING_ICON = (
  <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M4 19V9M9 19V5M14 19v-7M19 19V8" strokeLinecap="round" />
  </svg>
);

const CARDS = [
  {
    id: "android",
    title: "Android",
    lead: "Phone or tablet. Chrome, Edge, or Samsung Internet.",
    steps: [
      "Open this page in Chrome (or Edge / Samsung Internet).",
      "Tap Install on Android, or the browser menu → Install app.",
      "Open Verodus from your home screen.",
    ],
    cta: "Install on Android",
    icon: ANDROID_ICON,
  },
  {
    id: "mobile",
    title: "Mobile",
    lead: "iPhone and iPad. Works in Safari and every iOS browser.",
    steps: [
      "Tap Share in the toolbar (the square with the arrow).",
      "Scroll and tap Add to Home Screen.",
      "Tap Add. The icon lands next to your other apps.",
    ],
    cta: "Show iPhone steps",
    icon: MOBILE_ICON,
  },
  {
    id: "desktop",
    title: "Desktop",
    lead: "Windows, Mac, and Chromebook. Use Chrome or Edge.",
    steps: [
      "Open this page in Chrome or Edge (Firefox cannot install web apps).",
      "Click Install Verodus in the address bar, or the menu → Install Verodus.",
      "Open it from your dock, taskbar, or Start menu.",
    ],
    cta: "Install on desktop",
    icon: DESKTOP_ICON,
  },
  {
    id: "safari",
    title: "Safari",
    lead: "Mac. Safari 17+ on macOS 14 Sonoma or newer. Creates a Dock web app.",
    steps: [
      "Open this page in Safari on your Mac (not Chrome).",
      "File → Add to Dock. Or the share button in the toolbar → Add to Dock.",
      "Open Verodus from the Dock like any other Mac app.",
    ],
    cta: "Show Safari steps",
    icon: SAFARI_ICON,
  },
  {
    id: "trading",
    title: "Trading",
    lead: "Optional second app. TradeHub and Platform 5. Opens a short guide with the link.",
    steps: [
      "Tap How to install Trading.",
      "Read the steps, then Open TradeHub in Chrome or Safari.",
      "Install / Add to Dock on trade.verodus.com — not from this page.",
    ],
    cta: "How to install Trading",
    icon: TRADING_ICON,
  },
];

export default function PlatformsPage() {
  return (
    <section className="v-platforms">
      <p className="v-platforms__done">Verodus is already installed on this device.</p>
      <h1>Platforms</h1>
      <p className="v-platforms__lede">
        Install Verodus from Dashboard → Trading Resources → Platforms. Choose Android, Mobile,
        Desktop, or Safari for the CRM. Trading is a separate optional app — a modal shows the
        steps and the TradeHub link.
      </p>
      <div className="v-platforms__grid">
        {CARDS.map((card) => (
          <article key={card.id} className="v-platforms__card">
            <div className="v-platforms__icon">{card.icon}</div>
            <h2>{card.title}</h2>
            <p>{card.lead}</p>
            <ol>
              {card.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
            <button
              type="button"
              className="v-platforms__cta"
              data-install-app
              data-install-platform={card.id}
            >
              {card.cta}
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
