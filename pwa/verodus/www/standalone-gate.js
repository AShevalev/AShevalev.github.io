/**
 * On the marketing homepage: if this tab is already the installed app,
 * skip the landing page and open the shell.
 */
try {
  const standalone =
    window.matchMedia("(display-mode: standalone)").matches ||
    window.matchMedia("(display-mode: fullscreen)").matches ||
    window.navigator.standalone === true;
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  if (standalone && (path === "/" || path === "/index.html")) {
    window.location.replace("/app");
  }
} catch {
  // Ignore.
}
