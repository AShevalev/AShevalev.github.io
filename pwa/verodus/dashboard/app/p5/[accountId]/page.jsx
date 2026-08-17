/**
 * Copy to dashboard Next.js:
 *   app/p5/[accountId]/page.jsx
 */
import PlatformFrame from "@/components/PlatformFrame";

export default function Platform5Page({ params }) {
  return <PlatformFrame kind="p5" accountId={params.accountId} />;
}
