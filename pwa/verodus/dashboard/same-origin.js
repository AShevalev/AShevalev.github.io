/**
 * Keep TradeHub and Platform 5 inside the dashboard origin.
 * Chrome shows the website bar on any top-level navigation to another host.
 */

export const APP_ORIGIN = "https://dashboard.verodus.com";
export const TRADE_ORIGIN = "https://trade.verodus.com";

const PLATFORM = /\/(tradehub|p5)(?:\/([^/?#]*))?/i;

/**
 * @param {string} href
 * @param {string} [appOrigin]
 * @returns {{ kind: "tradehub"|"p5", accountId: string, search: string, hash: string } | null}
 */
export function parsePlatformUrl(href, appOrigin = APP_ORIGIN) {
  let url;
  try {
    url = new URL(String(href), appOrigin);
  } catch {
    return null;
  }
  if (url.origin !== TRADE_ORIGIN && url.origin !== new URL(appOrigin).origin) {
    return null;
  }
  const match = url.pathname.match(PLATFORM);
  if (!match) return null;
  return {
    kind: match[1].toLowerCase() === "p5" ? "p5" : "tradehub",
    accountId: match[2] || "",
    search: url.search,
    hash: url.hash,
  };
}

/**
 * Convert a trade.verodus.com (or already-local) platform URL into a path on
 * the dashboard origin. Returns null if the URL is not TradeHub / Platform 5.
 *
 * @param {string} href
 * @param {string} [appOrigin]
 */
export function toInAppUrl(href, appOrigin = APP_ORIGIN) {
  const parsed = parsePlatformUrl(href, appOrigin);
  if (!parsed) return null;
  const account = parsed.accountId ? `/${parsed.accountId}` : "";
  return `${new URL(appOrigin).origin}/${parsed.kind}${account}${parsed.search}${parsed.hash}`;
}

/**
 * iframe src on the trade origin for a dashboard in-app path.
 *
 * @param {string} href
 * @param {string} [appOrigin]
 */
export function toTradeEmbedSrc(href, appOrigin = APP_ORIGIN) {
  const parsed = parsePlatformUrl(href, appOrigin);
  if (!parsed) return null;
  const account = parsed.accountId ? `/${parsed.accountId}` : "";
  return `${TRADE_ORIGIN}/${parsed.kind}${account}${parsed.search}${parsed.hash}`;
}

/**
 * Path for the Platform 5 / TradeHub buttons on an account card.
 * Always a same-origin path. Never trade.verodus.com.
 *
 * @param {"p5"|"tradehub"|string} kind
 * @param {string} accountId
 */
export function launchPath(kind, accountId) {
  const platform = String(kind).toLowerCase() === "p5" ? "p5" : "tradehub";
  const id = String(accountId || "").replace(/^\/+|\/+$/g, "");
  return id ? `/${platform}/${id}` : `/${platform}`;
}
