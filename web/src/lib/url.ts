/**
 * Prepend Astro's BASE_URL to an internal path so links and static-asset
 * references resolve correctly when the site is served from a subpath
 * (production: /qnetinfo/...). Dev mode has BASE_URL = "/" so this is
 * a no-op locally.
 *
 *   url("/qubits")            → "/qnetinfo/qubits"  (prod)
 *   url("/icons/foo.svg")     → "/qnetinfo/icons/foo.svg"
 *   url("/")                  → "/qnetinfo/"
 */
export function url(path: string): string {
  const rawBase = import.meta.env.BASE_URL; // "/" in dev, "/qnetinfo" in prod
  const base = rawBase.endsWith("/") ? rawBase : rawBase + "/";
  const cleaned = path.replace(/^\/+/, "");
  return cleaned ? base + cleaned : base;
}
