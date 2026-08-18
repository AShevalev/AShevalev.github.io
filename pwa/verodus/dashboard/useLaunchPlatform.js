"use client";

import { useRouter } from "next/navigation";
import { launchPath } from "./same-origin.js";

/** Use this instead of window.location or window.open for Platform 5 / TradeHub. */
export function useLaunchPlatform() {
  const router = useRouter();
  return (kind, accountId) => {
    router.push(launchPath(kind, accountId));
  };
}
