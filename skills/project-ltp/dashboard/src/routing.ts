import { viewOrder, type TreeView } from "./model";

/** The overview, or one of the six trees — what a link can point at. */
export type Screen = "overview" | TreeView;

/**
 * A linkable location in the dashboard: which project is open, and which of
 * its screens. `slug` is null for the project picker, and for the single
 * project served by serve_dashboard.py, which has no slug to name.
 */
export interface Route {
  slug: string | null;
  screen: Screen;
}

const viewIds = new Set<string>(viewOrder);

function isView(segment: string | undefined): segment is TreeView {
  return segment !== undefined && viewIds.has(segment);
}

/**
 * Read a route out of a location hash:
 *
 *   #/                      the project picker
 *   #/<project>             that project's overview
 *   #/<project>/<view>      one tree in that project
 *   #/<view>                a tree of the single live model
 *
 * The hash keeps deep links working on a plain static host — the published
 * site serves one file at /dashboard/index.html and has no route table.
 * A leading segment naming a view is read as the live-model form, so a project
 * must not be slugged after one of the six views.
 */
export function parseRoute(hash: string): Route {
  const segments = hash
    .replace(/^#\/?/, "")
    .split("/")
    .filter(Boolean)
    .map(decodeURIComponent);
  if (segments.length === 0) return { slug: null, screen: "overview" };
  if (isView(segments[0])) return { slug: null, screen: segments[0] };
  return { slug: segments[0], screen: isView(segments[1]) ? segments[1] : "overview" };
}

/** The hash that `parseRoute` reads back as this route. */
export function formatRoute(route: Route): string {
  const segments = [route.slug, route.screen === "overview" ? null : route.screen]
    .filter((segment): segment is string => Boolean(segment))
    .map(encodeURIComponent);
  return `#/${segments.join("/")}`;
}

/** The route the address bar is showing. */
export function currentRoute(): Route {
  return parseRoute(window.location.hash);
}

export function sameRoute(a: Route, b: Route): boolean {
  return a.slug === b.slug && a.screen === b.screen;
}
