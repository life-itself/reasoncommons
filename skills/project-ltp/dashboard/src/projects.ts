import { parse } from "yaml";
import {
  validateModel,
  validateThroughput,
  type LtpModel,
  type ThroughputData,
} from "./model";
import { validateTracking, type TrackingLedger } from "./tracking";
import embeddedProjectFiles from "virtual:embedded-project-files";

/**
 * One project shown in the multi-project picker. Models are loaded from
 * `projects/<slug>/model.yaml` (relative to the page) unless `model` /
 * `throughput` override the path.
 */
export interface ProjectSummary {
  slug: string;
  name: string;
  blurb?: string;
  analysis_mode?: string;
  source?: string;
  updated?: string;
  model?: string;
  throughput?: string;
  tracking?: string;
  /** Declaring the repository lets the dashboard read issue state live, even
   * before any sync has committed a `github-sync.yaml` snapshot. */
  github?: { repo: string; label?: string };
}

/**
 * One source-project → target-project alignment pilot shown alongside the
 * project picker. Suggestions live in `projects/<file>` (default
 * `alignments/<slug>.yaml`) and reference entity IDs in both projects' models.
 */
export interface AlignmentSummary {
  slug: string;
  name: string;
  blurb?: string;
  source_project: string;
  target_project: string;
  file?: string;
}

/**
 * Where the dashboard gets its projects:
 * - "static": a published `projects/manifest.json` (the site, or `vite dev`).
 * - "live":  the local read-only server (serve_dashboard.py), a single project
 *            served at /api/model — the manifest is absent, so we fall back.
 */
export type ProjectSource =
  | { mode: "static"; projects: ProjectSummary[]; alignments: AlignmentSummary[] }
  | { mode: "live"; projects: ProjectSummary[]; alignments: AlignmentSummary[] };

export interface LoadedModel {
  model: LtpModel;
  throughput: ThroughputData | null;
  tracking: TrackingLedger | null;
}

export async function fetchText(url: string): Promise<string | null> {
  // Production builds carry the static catalog in index.html because the
  // published host redirects repository assets to a CORS-incompatible origin.
  // API URLs deliberately miss this map and continue to use the local server.
  const normalizedUrl = url.replace(/^\.\//, "");
  if (normalizedUrl.startsWith("projects/")) {
    return embeddedProjectFiles[normalizedUrl] ?? null;
  }

  const response = await fetch(url, { cache: "no-store" });
  if (response.status === 204 || response.status === 404) return null;
  if (!response.ok) throw new Error(`${url} returned ${response.status}`);
  const contentType = response.headers.get("content-type") ?? "";
  const text = await response.text();
  // Static hosts with SPA fallback answer a missing file with index.html at
  // HTTP 200. Treat an HTML response to a YAML/JSON request as "absent" so an
  // optional file (e.g. throughput.yaml) doesn't get parsed as the page.
  if (contentType.includes("text/html") || /^\s*<(?:!doctype|html)\b/i.test(text)) {
    return null;
  }
  return text;
}

/**
 * Prefer a static manifest; fall back to the single live project served by
 * serve_dashboard.py. Relative paths keep this working at "/" and under a
 * subpath such as "/dashboard/".
 */
export async function resolveProjectSource(): Promise<ProjectSource> {
  let manifestText: string | null = null;
  try {
    manifestText = await fetchText("projects/manifest.json");
  } catch {
    manifestText = null;
  }
  if (manifestText) {
    try {
      const parsed = JSON.parse(manifestText) as {
        projects?: ProjectSummary[];
        alignments?: AlignmentSummary[];
      };
      const projects = (parsed.projects ?? []).filter(
        (project) => project && project.slug && project.name,
      );
      const alignments = (parsed.alignments ?? []).filter(
        (alignment) =>
          alignment && alignment.slug && alignment.name && alignment.source_project && alignment.target_project,
      );
      if (projects.length) return { mode: "static", projects, alignments };
    } catch {
      // Malformed manifest — fall through to the live server.
    }
  }
  return { mode: "live", projects: [{ slug: "__live__", name: "Live model" }], alignments: [] };
}

export async function loadProjectModel(
  source: ProjectSource,
  project: ProjectSummary,
): Promise<LoadedModel> {
  let modelText: string | null;
  let throughputText: string | null;
  let trackingText: string | null;
  if (source.mode === "live") {
    [modelText, throughputText, trackingText] = await Promise.all([
      fetchText("/api/model"),
      fetchText("/api/throughput"),
      fetchText("/api/github-sync"),
    ]);
  } else {
    const base = `projects/${project.slug}/`;
    [modelText, throughputText, trackingText] = await Promise.all([
      fetchText(project.model ?? `${base}model.yaml`),
      fetchText(project.throughput ?? `${base}throughput.yaml`),
      fetchText(project.tracking ?? `${base}github-sync.yaml`),
    ]);
  }
  if (!modelText) throw new Error("The project model file could not be loaded.");
  return {
    model: validateModel(parse(modelText)),
    throughput: throughputText ? validateThroughput(parse(throughputText)) : null,
    // A project with no issue tracking is the normal case, and a malformed
    // ledger must never stop the tree from rendering.
    tracking: trackingText ? safeTracking(trackingText) : null,
  };
}

function safeTracking(text: string): TrackingLedger | null {
  try {
    return validateTracking(parse(text));
  } catch {
    return null;
  }
}
