import { useMemo, type CSSProperties } from "react";
import type { AlignmentBadge } from "./alignment";
import type {
  Confidence,
  EntityStatus,
  LtpModel,
  ModelIndex,
  TreeView,
} from "./model";
import { buildTreeProjection, orderTreeProjection } from "./treeProjection";
import {
  buildActionRollups,
  buildCompletedIds,
  rollupLabel,
  rollupTone,
  trackingBadgeShortLabels,
  type TrackingBadge,
} from "./tracking";

interface TreeListProps {
  model: LtpModel;
  index: ModelIndex;
  view: TreeView;
  statuses: Set<EntityStatus>;
  confidences: Set<Confidence>;
  expandedIds: Set<string>;
  collapsingIds: Set<string>;
  selectedId: string | null;
  alignmentBadges?: Map<string, AlignmentBadge>;
  trackingBadges?: Map<string, TrackingBadge>;
  /** Settled actions still sink to the bottom either way; this only decides
   * whether they render at all. Defaults to shown. */
  showCompleted?: boolean;
  onToggle: (entityId: string) => void;
  onSelect: (entityId: string | null) => void;
}

export function TreeList({
  model,
  index,
  view,
  statuses,
  confidences,
  expandedIds,
  collapsingIds,
  selectedId,
  alignmentBadges,
  trackingBadges,
  showCompleted = true,
  onToggle,
  onSelect,
}: TreeListProps) {
  const projection = useMemo(
    () =>
      buildTreeProjection({
        model,
        index,
        view,
        statuses,
        confidences,
        expandedIds,
      }),
    [confidences, expandedIds, index, model, statuses, view],
  );
  // Built over the whole subtree, not just what's expanded, so a collapsed
  // ancestor can announce "1/4 actions done" before anyone opens it.
  const rollups = useMemo(
    () => buildActionRollups(projection.childrenByParent, index.entities, trackingBadges),
    [projection, index, trackingBadges],
  );
  const completedIds = useMemo(
    () => buildCompletedIds(index.entities, rollups, trackingBadges),
    [index, rollups, trackingBadges],
  );
  const rows = useMemo(
    () => orderTreeProjection(projection, expandedIds, completedIds),
    [expandedIds, projection, completedIds],
  );
  const visibleRows = showCompleted
    ? rows
    : rows.filter((row) => !completedIds.has(row.entity.id));
  const settledVisibleIds = useMemo(() => {
    const settledExpandedIds = new Set(expandedIds);
    for (const entityId of collapsingIds) settledExpandedIds.delete(entityId);
    return buildTreeProjection({
      model,
      index,
      view,
      statuses,
      confidences,
      expandedIds: settledExpandedIds,
    }).visibleIds;
  }, [
    collapsingIds,
    confidences,
    expandedIds,
    index,
    model,
    statuses,
    view,
  ]);

  if (!model.views[view]) {
    return (
      <div className="canvas-empty">
        <strong>This view has not been modelled yet.</strong>
        <span>Add it under <code>views.{view}</code> in ltp-model.yaml.</span>
      </div>
    );
  }
  if (!rows.length) {
    return (
      <div className="canvas-empty">
        <strong>No nodes match the current filters.</strong>
        <span>Broaden status or confidence under Refine.</span>
      </div>
    );
  }
  if (!visibleRows.length) {
    return (
      <div className="canvas-empty">
        <strong>Everything here is marked complete.</strong>
        <span>Turn "Show completed" back on to see it.</span>
      </div>
    );
  }

  return (
    <div className="tree-list-scroll">
      <ol className="tree-list">
        {visibleRows.map(({ entity, depth }) => {
          const isCompleted = completedIds.has(entity.id);
          const childCount = (projection.childrenByParent.get(entity.id) ?? []).filter(
            (childId) => showCompleted || !completedIds.has(childId),
          ).length;
          const expanded = expandedIds.has(entity.id);
          const badge = entity.type === "action" ? trackingBadges?.get(entity.id) : undefined;
          const rollup = entity.type !== "action" ? rollups.get(entity.id) : undefined;
          const style = {
            "--tree-depth": depth,
            viewTransitionName: `ltp-${entity.id.replaceAll(/[^a-zA-Z0-9_-]/g, "-")}`,
          } as CSSProperties;
          const toggleLabel = expanded
            ? `Collapse ${entity.id}`
            : `Expand ${entity.id} to show ${childCount} connected ${childCount === 1 ? "node" : "nodes"}`;

          return (
            <li
              key={entity.id}
              className={settledVisibleIds.has(entity.id) ? "" : "is-collapsing"}
              style={style}
            >
              <div
                className={`tree-list-row ${selectedId === entity.id ? "is-selected" : ""} ${isCompleted ? "is-completed" : ""}`}
                data-status={entity.status}
              >
                <button
                  className="tree-disclosure-button"
                  type="button"
                  aria-label={childCount ? toggleLabel : `${entity.id} has no hidden nodes`}
                  aria-expanded={childCount ? expanded : undefined}
                  disabled={!childCount}
                  onClick={() => onToggle(entity.id)}
                >
                  <span aria-hidden="true">{childCount ? (expanded ? "−" : "+") : "·"}</span>
                </button>
                <button
                  className="tree-list-summary"
                  type="button"
                  onClick={() => {
                    onSelect(entity.id);
                    if (childCount) onToggle(entity.id);
                  }}
                >
                  <span className="tree-list-identity">
                    <strong>
                      {entity.id}
                      {alignmentBadges?.has(entity.id) && (
                        <i
                          className={`alignment-node-badge alignment-node-badge--${alignmentBadges.get(entity.id)}`}
                          title="Has an alignment suggestion"
                        />
                      )}
                    </strong>
                    <small>{entity.type.replaceAll("_", " ")}</small>
                  </span>
                  <span className="tree-list-statement">{entity.statement}</span>
                  <span className="tree-list-facts">
                    <i className={`status-mark status-mark--${entity.status}`} />
                    <span>{entity.status}</span>
                    <span>{entity.confidence} confidence</span>
                    {childCount > 0 && (
                      <span>{childCount} {childCount === 1 ? "branch" : "branches"}</span>
                    )}
                    {badge && (
                      <span className={`tracking-chip tracking-chip--${badge}`}>
                        <i className={`tracking-node-badge tracking-node-badge--${badge}`} />
                        {trackingBadgeShortLabels[badge]}
                      </span>
                    )}
                    {rollup && rollup.total > 0 && (
                      <span
                        className={`tracking-rollup tracking-rollup--${rollupTone(rollup)}`}
                        title="Tracked actions inside this branch, expanded or not"
                      >
                        {rollupLabel(rollup)}
                      </span>
                    )}
                  </span>
                </button>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
