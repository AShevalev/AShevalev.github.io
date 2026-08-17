"use client";

import { useEffect } from "react";

/** Load once in the dashboard root layout. */
export default function InAppLaunches() {
  useEffect(() => {
    import("./intercept-launches.js");
    import("../lock-origin-entry.js");
  }, []);
  return null;
}
