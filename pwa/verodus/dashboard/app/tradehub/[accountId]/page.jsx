/**
 * Copy to dashboard Next.js:
 *   app/tradehub/[accountId]/page.jsx
 */
import PlatformFrame from "@/components/PlatformFrame";

export default function TradehubPage({ params }) {
  return <PlatformFrame kind="tradehub" accountId={params.accountId} />;
}
