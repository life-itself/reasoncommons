/**
 * GitHub issue tracking for transition-tree actions.
 *
 * Reads `ltp/github-sync.yaml`, the ledger written by
 * `scripts/sync_github_issues.py`. The ledger is derived state: the model still
 * owns what an action *is*, and the issue owns whether it is open, assigned, or
 * done. The dashboard only displays the second half — it never writes either.
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
  if (action.state === "closed") {
    return action.state_reason === "not_planned" ? "dropped" : "done";
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
