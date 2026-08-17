/**
 * Copy into the dashboard Next.js app as:
 *   components/PlatformFrame.jsx
 *   app/tradehub/[accountId]/page.jsx
 *   app/p5/[accountId]/page.jsx  (pass kind="p5")
 *
 * Top-level URL: https://dashboard.verodus.com/tradehub/{accountId}
 * iframe src:    https://trade.verodus.com/tradehub/{accountId}
 *
 * Chrome's standalone window follows the top-level URL, so the website bar
 * does not appear.
 */
export default function PlatformFrame({ accountId, kind = "tradehub" }) {
  const src = `https://trade.verodus.com/${kind}/${accountId}`;
  const title = kind === "p5" ? "Platform 5" : "TradeHub";
  return (
    <iframe
      src={src}
      title={title}
      allow="fullscreen; clipboard-read; clipboard-write; accelerometer; gyroscope"
      allowFullScreen
      style={{
        position: "fixed",
        inset: 0,
        width: "100%",
        height: "100%",
        border: 0,
        background: "#07003B",
      }}
    />
  );
}
