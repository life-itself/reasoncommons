/**
 * GitHub issue tracking for transition-tree actions.
 *
 * Two sources, in order of freshness:
 *
 * 1. GitHub's public issues API, read straight from the browser. This is what
 *    makes a closed issue show as closed without anyone rebuilding the site.
 * 2. `github-sync.yaml`, the ledger written by `scripts/sync_github_issues.py`.
 *    It paints instantly, works offline and for private repositories, and it
 *    is the only source for drift — whether the issue body still matches the
 *    tree node — because that comparison needs the digests recorded at push
 *    time.
 *
 * The model still owns what an action *is*; the issue owns whether it is open,
 * assigned, or done. The dashboard displays the second half and writes neither.
 */

export type SyncStatus =
  | "create"
  | "update"
  | "in-sync"
  | "issue-edited"
  | "conflict"
  | "missing-remote";

/** What a tree node's tracking badge shows at a glance. */
export type TrackingBadge = "open" | "done" | "dropped" | "untracked" | "drifted";

export interface TrackedAction {
  issue?: number;
  url?: string;
  state?: string;
  state_reason?: string;
  assignees?: string[];
  updated_at?: string;
  closed_at?: string;
  pushed_at?: string;
  sync_status?: SyncStatus;
}

export interface UntrackedIssue {
  issue: number;
  url?: string;
  title?: string;
  action?: string;
}

export interface TrackingLedger {
  repo?: string;
  view?: string;
  label?: string;
  synced_at?: string;
  actions: Record<string, TrackedAction>;
  untracked_issues?: UntrackedIssue[];
  orphan_issues?: UntrackedIssue[];
  /** Where the issue state on screen came from. Absent means the ledger file. */
  source?: "live" | "snapshot";
  /** When the live read happened, for the provenance line in the overview. */
  checked_at?: string;
}

export const DEFAULT_TRACKING_LABEL = "ltp-action";
const MARKER = /<!--\s*project-ltp:action=([A-Za-z0-9][\w.-]*)\s*-->/;

/** Mirrors the marker comment that `sync_github_issues.py` writes into each
 * issue body. That comment, not the ledger, is the durable action↔issue link,
 * which is why the browser can rebuild the mapping from the API alone. */
export function markerAction(body: string | null | undefined): string | null {
  return MARKER.exec(body ?? "")?.[1] ?? null;
}

export function validateTracking(value: unknown): TrackingLedger {
  if (!value || typeof value !== "object") {
    throw new Error("github-sync.yaml must contain an object");
  }
  const ledger = value as Partial<TrackingLedger>;
  const actions = ledger.actions ?? {};
  if (typeof actions !== "object" || Array.isArray(actions)) {
    throw new Error("github-sync.actions must be a mapping of action id to issue state");
  }
  for (const [id, action] of Object.entries(actions)) {
    if (!action || typeof action !== "object") {
      throw new Error(`github-sync.actions.${id} must be an object`);
    }
  }
  return { ...ledger, actions: actions as Record<string, TrackedAction> };
}

const driftedStatuses = new Set<SyncStatus>([
  "update",
  "issue-edited",
  "conflict",
  "missing-remote",
]);

/**
 * Drift wins over execution state: an action whose issue no longer matches its
 * tree node should read as needing attention, not as quietly in progress.
 */
export function trackingBadge(action: TrackedAction | undefined): TrackingBadge {
  if (!action || (!action.issue && !action.sync_status)) return "untracked";
  if (action.sync_status && driftedStatuses.has(action.sync_status)) return "drifted";
  if (!action.issue) return "untracked";
  // Case-insensitive: the REST API says "not_planned", the gh CLI "NOT_PLANNED",
  // and older ledgers may hold either.
  if (action.state?.toLowerCase() === "closed") {
    return action.state_reason?.toLowerCase() === "not_planned" ? "dropped" : "done";
  }
  return "open";
}

export const trackingBadgeLabels: Record<TrackingBadge, string> = {
  open: "Open on GitHub",
  done: "Closed as done",
  dropped: "Closed as not planned",
  untracked: "No issue tracks this action",
  drifted: "Issue and tree node are out of step",
};

/** Short enough to sit inline on a tree node without a hover. */
export const trackingBadgeShortLabels: Record<TrackingBadge, string> = {
  open: "Open",
  done: "Done",
  dropped: "Dropped",
  untracked: "Not tracked",
  drifted: "Out of step",
};

export function buildTrackingBadges(
  ledger: TrackingLedger | null,
): Map<string, TrackingBadge> {
  const badges = new Map<string, TrackingBadge>();
  if (!ledger) return badges;
  for (const [actionId, action] of Object.entries(ledger.actions)) {
    badges.set(actionId, trackingBadge(action));
  }
  return badges;
}

export interface TrackingTally {
  tracked: number;
  open: number;
  done: number;
  dropped: number;
  drifted: number;
  untracked: number;
  loose: number;
}

/** One issue as the GitHub REST API returns it, narrowed to what we display. */
interface ApiIssue {
  number: number;
  title: string;
  body: string | null;
  state: string;
  state_reason: string | null;
  html_url: string;
  updated_at: string;
  closed_at: string | null;
  assignees: Array<{ login: string }> | null;
  pull_request?: unknown;
}

/**
 * Fold live issues into whatever the ledger already said. Execution state
 * always comes from GitHub; `sync_status` and the push digests stay with the
 * ledger, because only the ledger knows what was last pushed.
 */
export function mergeLiveIssues(
  base: TrackingLedger | null,
  issues: ApiIssue[],
  repo: string,
  label: string,
  checkedAt: string,
): TrackingLedger {
  const actions: Record<string, TrackedAction> = {};
  const untracked: UntrackedIssue[] = [];
  const claimed = new Set<string>();

  for (const issue of issues) {
    if (issue.pull_request) continue;
    const actionId = markerAction(issue.body);
    if (!actionId) {
      untracked.push({ issue: issue.number, url: issue.html_url, title: issue.title });
      continue;
    }
    // Two issues on one node: keep the lower number, matching the CLI.
    const existing = actions[actionId];
    if (existing?.issue !== undefined && existing.issue <= issue.number) continue;
    claimed.add(actionId);
    actions[actionId] = {
      ...base?.actions[actionId],
      issue: issue.number,
      url: issue.html_url,
      state: issue.state,
      state_reason: issue.state_reason ?? undefined,
      assignees: (issue.assignees ?? []).map((person) => person.login),
      updated_at: issue.updated_at,
      closed_at: issue.closed_at ?? undefined,
    };
  }

  // Ledger entries GitHub did not return: keep what the snapshot knew, minus
  // any issue number it claimed, so a deleted or unlabelled issue does not go
  // on showing as open.
  for (const [actionId, entry] of Object.entries(base?.actions ?? {})) {
    if (claimed.has(actionId)) continue;
    actions[actionId] = entry.issue
      ? { ...entry, issue: undefined, url: undefined, state: undefined, sync_status: "missing-remote" }
      : entry;
  }

  return {
    ...base,
    repo,
    label,
    actions,
    untracked_issues: untracked,
    orphan_issues: base?.orphan_issues,
    source: "live",
    checked_at: checkedAt,
  };
}

/**
 * Read issue state for a public repository straight from the browser. Returns
 * null on any failure — offline, rate-limited, private, renamed — so the
 * caller simply keeps the snapshot it already has.
 */
export async function fetchLiveTracking(
  base: TrackingLedger | null,
  repo: string,
  label: string = DEFAULT_TRACKING_LABEL,
): Promise<TrackingLedger | null> {
  const url =
    `https://api.github.com/repos/${repo}/issues` +
    `?state=all&per_page=100&labels=${encodeURIComponent(label)}`;
  try {
    const response = await fetch(url, {
      headers: { Accept: "application/vnd.github+json" },
      cache: "no-store",
    });
    if (!response.ok) return null;
    const issues = (await response.json()) as ApiIssue[];
    if (!Array.isArray(issues)) return null;
    return mergeLiveIssues(base, issues, repo, label, new Date().toISOString());
  } catch {
    return null;
  }
}

export interface ActionRollup {
  total: number;
  open: number;
  done: number;
  dropped: number;
  drifted: number;
  untracked: number;
}

function emptyRollup(): ActionRollup {
  return { total: 0, open: 0, done: 0, dropped: 0, drifted: 0, untracked: 0 };
}

function addRollup(a: ActionRollup, b: ActionRollup): ActionRollup {
  return {
    total: a.total + b.total,
    open: a.open + b.open,
    done: a.done + b.done,
    dropped: a.dropped + b.dropped,
    drifted: a.drifted + b.drifted,
    untracked: a.untracked + b.untracked,
  };
}

/**
 * Sums tracked-action state over every node's full subtree — including
 * collapsed, not-yet-rendered branches — so a node can announce "3 actions,
 * 1 done" before anyone expands it. `childrenByParent` already spans the
 * whole view regardless of expand state, which is what makes this possible.
 *
 * Entities is a plain `{id: {type}}` map rather than the full `LtpEntity` type
 * so this stays decoupled from model.ts; callers already have `index.entities`
 * on hand and pass it through as-is.
 */
export function buildActionRollups(
  childrenByParent: Map<string, string[]>,
  entities: Map<string, { type: string }>,
  trackingBadges: Map<string, TrackingBadge> | undefined,
): Map<string, ActionRollup> {
  const memo = new Map<string, ActionRollup>();
  const inProgress = new Set<string>();

  const visit = (id: string): ActionRollup => {
    const cached = memo.get(id);
    if (cached) return cached;
    if (inProgress.has(id)) return emptyRollup(); // cycle guard
    inProgress.add(id);

    let tally = emptyRollup();
    if (entities.get(id)?.type === "action") {
      const badge = trackingBadges?.get(id) ?? "untracked";
      tally = { ...tally, total: 1, [badge]: 1 };
    }
    for (const childId of childrenByParent.get(id) ?? []) {
      tally = addRollup(tally, visit(childId));
    }

    inProgress.delete(id);
    memo.set(id, tally);
    return tally;
  };

  const allIds = new Set<string>();
  for (const [parentId, childIds] of childrenByParent) {
    allIds.add(parentId);
    for (const childId of childIds) allIds.add(childId);
  }
  for (const id of allIds) visit(id);
  return memo;
}

export type RollupTone = "done" | "attention" | "pending";

/** How urgently a rollup chip should read, distinct from any single badge. */
export function rollupTone(rollup: ActionRollup): RollupTone {
  if (rollup.total === 0) return "pending";
  if (rollup.drifted > 0) return "attention";
  if (rollup.done + rollup.dropped === rollup.total) return "done";
  return "pending";
}

export function rollupLabel(rollup: ActionRollup): string {
  const settled = rollup.done + rollup.dropped;
  const noun = rollup.total === 1 ? "action" : "actions";
  return `${settled}/${rollup.total} ${noun} done`;
}

/** Closed and done, or closed as not planned — either way, nothing left to do. */
export function isActionSettled(badge: TrackingBadge): boolean {
  return badge === "done" || badge === "dropped";
}

export function isRollupSettled(rollup: ActionRollup): boolean {
  return rollup.total > 0 && rollup.done + rollup.dropped === rollup.total;
}

/**
 * Every entity — action or not — whose tracked work is fully settled: an
 * action closed as done or not-planned, or a node whose entire subtree of
 * actions is. Drives sinking finished work to the bottom of a list and
 * letting it be hidden outright. A node with no actions under it at all is
 * never "complete" in this sense — there's nothing to have finished.
 */
export function buildCompletedIds(
  entities: Map<string, { type: string }>,
  rollups: Map<string, ActionRollup>,
  trackingBadges: Map<string, TrackingBadge> | undefined,
): Set<string> {
  const completed = new Set<string>();
  for (const [id, entity] of entities) {
    if (entity.type === "action") {
      const badge = trackingBadges?.get(id);
      if (badge && isActionSettled(badge)) completed.add(id);
    } else {
      const rollup = rollups.get(id);
      if (rollup && isRollupSettled(rollup)) completed.add(id);
    }
  }
  return completed;
}

/** `actionIds` is every action in the tree, so nodes with no ledger entry at
 * all still count as untracked rather than vanishing from the tally. */
export function tallyTracking(
  ledger: TrackingLedger | null,
  actionIds: string[],
): TrackingTally {
  const tally: TrackingTally = {
    tracked: 0,
    open: 0,
    done: 0,
    dropped: 0,
    drifted: 0,
    untracked: 0,
    loose: (ledger?.untracked_issues?.length ?? 0) + (ledger?.orphan_issues?.length ?? 0),
  };
  for (const actionId of actionIds) {
    const badge = trackingBadge(ledger?.actions[actionId]);
    tally[badge] += 1;
    if (badge !== "untracked") tally.tracked += 1;
  }
  return tally;
}
