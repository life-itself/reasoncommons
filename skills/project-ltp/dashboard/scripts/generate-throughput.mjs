import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parse, stringify } from "yaml";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const DEFAULT_CONFIG = resolve(SCRIPT_DIR, "..", "throughput.config.json");

function git(repoRoot, args) {
  return execFileSync("git", ["-C", repoRoot, ...args], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trimEnd();
}

function sortByCanonicalValue(values) {
  return [...values].sort((left, right) =>
    JSON.stringify(left).localeCompare(JSON.stringify(right)),
  );
}

/**
 * YAML mapping order and set-like list order are presentation details. Sorting
 * recursively lets formatting-only edits disappear from semantic comparisons.
 */
export function canonicalize(value) {
  if (Array.isArray(value)) {
    return sortByCanonicalValue(value.map(canonicalize));
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([key, child]) => [key, canonicalize(child)]),
    );
  }
  return value;
}

function indexById(items = []) {
  return new Map(items.map((item) => [item.id, item]));
}

/**
 * A node's meaning includes its own fields, its causal neighbourhood, and the
 * tree views in which it appears. This makes a link or membership edit visible
 * as an update to the affected stable node rather than as invisible metadata.
 */
export function nodeProjection(model, entityId) {
  const entity = indexById(model.entities).get(entityId);
  if (!entity) return null;

  const links = (model.links ?? [])
    .filter((link) => link.from === entityId || link.to === entityId)
    .map((link) => canonicalize(link));
  const incidentLinkIds = new Set(links.map((link) => link.id));
  const views = Object.entries(model.views ?? {})
    .map(([viewName, view]) => ({
      name: viewName,
      contains_entity: (view?.entities ?? []).includes(entityId),
      incident_links: (view?.links ?? [])
        .filter((linkId) => incidentLinkIds.has(linkId))
        .sort(),
    }))
    .filter((view) => view.contains_entity || view.incident_links.length > 0);
  const evidenceIndex = indexById(model.evidence);
  const assumptionIndex = indexById(model.assumptions);
  const evidence = (entity.evidence ?? [])
    .map((id) => evidenceIndex.get(id))
    .filter(Boolean);
  const assumptionIds = new Set([
    ...(entity.assumptions ?? []),
    ...links.map((link) => link.assumption).filter(Boolean),
  ]);
  const assumptions = [...assumptionIds]
    .map((id) => assumptionIndex.get(id))
    .filter(Boolean);

  return canonicalize({ entity, links, views, evidence, assumptions });
}

export function diffModels(previousModel, nextModel) {
  const previousIds = new Set((previousModel.entities ?? []).map(({ id }) => id));
  const nextIds = new Set((nextModel.entities ?? []).map(({ id }) => id));
  const created = [...nextIds].filter((id) => !previousIds.has(id)).sort();
  const deleted = [...previousIds].filter((id) => !nextIds.has(id)).sort();
  const updated = [...nextIds]
    .filter((id) => previousIds.has(id))
    .filter(
      (id) =>
        JSON.stringify(nodeProjection(previousModel, id)) !==
        JSON.stringify(nodeProjection(nextModel, id)),
    )
    .sort();

  return {
    created,
    updated,
    deleted,
    throughput: created.length + updated.length + deleted.length,
  };
}

function modelAt(repoRoot, revision, sourceModel) {
  const content = git(repoRoot, ["show", `${revision}:${sourceModel}`]);
  const model = parse(content);
  if (!model || !Array.isArray(model.entities)) {
    throw new Error(`${sourceModel} at ${revision} is not a valid LTP model`);
  }
  return { content: `${content}\n`, model };
}

function revisionMetadata(repoRoot, revision) {
  const [hash, authoredAt, subject] = git(repoRoot, [
    "show",
    "-s",
    "--format=%H%x00%aI%x00%s",
    revision,
  ]).split("\0");
  return { hash, authoredAt, subject };
}

function weekStart(isoTimestamp) {
  const dayText = isoTimestamp.slice(0, 10);
  const date = new Date(`${dayText}T00:00:00Z`);
  const day = date.getUTCDay();
  date.setUTCDate(date.getUTCDate() - ((day + 6) % 7));
  return date.toISOString().slice(0, 10);
}

function emptyPeriod(date) {
  return {
    date,
    throughput: 0,
    created: 0,
    updated: 0,
    deleted: 0,
  };
}

function fillWeeklyPeriods(periods, firstDate, lastDate) {
  const cursor = new Date(`${firstDate}T00:00:00Z`);
  const end = new Date(`${lastDate}T00:00:00Z`);
  while (cursor <= end) {
    const date = cursor.toISOString().slice(0, 10);
    if (!periods.has(date)) periods.set(date, emptyPeriod(date));
    cursor.setUTCDate(cursor.getUTCDate() + 7);
  }
}

function assertTrack(track) {
  for (const field of [
    "recipient_project",
    "source_project",
    "source_model",
    "output",
    "baseline_revision",
  ]) {
    if (!track[field]) throw new Error(`throughput track requires ${field}`);
  }
  if (!track.definition?.name || !track.definition?.unit || !track.definition?.period) {
    throw new Error("throughput track definition requires name, unit, and period");
  }
}

export function generateTrack(repoRoot, track) {
  assertTrack(track);
  const ref = track.ref ?? "HEAD";
  git(repoRoot, ["merge-base", "--is-ancestor", track.baseline_revision, ref]);

  const baseline = modelAt(repoRoot, track.baseline_revision, track.source_model);
  const baselineMetadata = revisionMetadata(repoRoot, track.baseline_revision);
  const revisions = git(repoRoot, [
    "rev-list",
    "--first-parent",
    "--reverse",
    `${track.baseline_revision}..${ref}`,
  ])
    .split("\n")
    .filter(Boolean);

  let previousModel = baseline.model;
  const countedRevisions = [];
  const baselinePeriod = weekStart(baselineMetadata.authoredAt);
  const periods = new Map([
    [baselinePeriod, emptyPeriod(baselinePeriod)],
  ]);

  for (const revision of revisions) {
    const current = modelAt(repoRoot, revision, track.source_model);
    const delta = diffModels(previousModel, current.model);
    previousModel = current.model;
    if (delta.throughput === 0) continue;

    const metadata = revisionMetadata(repoRoot, revision);
    const date = metadata.authoredAt.slice(0, 10);
    const periodDate = weekStart(metadata.authoredAt);
    const period = periods.get(periodDate) ?? emptyPeriod(periodDate);
    period.throughput += delta.throughput;
    period.created += delta.created.length;
    period.updated += delta.updated.length;
    period.deleted += delta.deleted.length;
    periods.set(periodDate, period);
    countedRevisions.push({
      revision: metadata.hash,
      date,
      subject: metadata.subject,
      ...delta,
    });
  }

  const head = modelAt(repoRoot, ref, track.source_model);
  const headMetadata = revisionMetadata(repoRoot, ref);
  fillWeeklyPeriods(
    periods,
    baselinePeriod,
    weekStart(headMetadata.authoredAt),
  );
  const definition = {
    ...track.definition,
    source: `Git first-parent history of ${track.source_model}`,
    source_project: track.source_project,
    source_model: track.source_model,
    baseline_revision: track.baseline_revision,
  };
  const throughput = {
    definition,
    periods: [...periods.values()].sort((left, right) =>
      left.date.localeCompare(right.date),
    ),
    revisions: countedRevisions,
  };

  if (track.published_model) {
    writeFileSync(resolve(repoRoot, track.published_model), head.content, "utf8");
  }
  const outputPath = resolve(repoRoot, track.output);
  writeFileSync(outputPath, stringify(throughput, { lineWidth: 0 }), "utf8");

  return { outputPath, throughput };
}

export function generateAll(configPath = DEFAULT_CONFIG, repoRoot) {
  const root =
    repoRoot ?? git(resolve(configPath, ".."), ["rev-parse", "--show-toplevel"]);
  const config = JSON.parse(readFileSync(configPath, "utf8"));
  if (!Array.isArray(config.tracks)) {
    throw new Error("throughput.config.json needs a tracks array");
  }
  if (config.tracks.length === 0) {
    // Since 2026-09-06 no bundled project defines a throughput track: the 2R
    // Research Circle project, whose track this was, is now measured by the
    // Reason Commons space connected to its repository rather than from Git.
    console.log("no throughput tracks configured; nothing generated");
    return [];
  }
  return config.tracks.map((track) => generateTrack(root, track));
}

const invokedPath = process.argv[1] ? resolve(process.argv[1]) : "";
if (invokedPath === fileURLToPath(import.meta.url)) {
  const results = generateAll(process.argv[2] ? resolve(process.argv[2]) : DEFAULT_CONFIG);
  for (const { outputPath, throughput } of results) {
    const total = throughput.periods.reduce(
      (sum, period) => sum + period.throughput,
      0,
    );
    process.stdout.write(
      `Generated ${outputPath}: ${total} node changes across ${throughput.revisions.length} revisions\n`,
    );
  }
}
