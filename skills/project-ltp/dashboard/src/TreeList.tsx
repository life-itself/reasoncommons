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
import { trackingBadgeLabels, type TrackingBadge } from "./tracking";

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
  const rows = useMemo(
    () => orderTreeProjection(projection, expandedIds),
    [expandedIds, projection],
  );
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

  return (
    <div className="tree-list-scroll">
      <ol className="tree-list">
        {rows.map(({ entity, depth }) => {
          const childCount = projection.childrenByParent.get(entity.id)?.length ?? 0;
          const expanded = expandedIds.has(entity.id);
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
                className={`tree-list-row ${selectedId === entity.id ? "is-selected" : ""}`}
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
                      {trackingBadges?.has(entity.id) && (
                        <i
                          className={`tracking-node-badge tracking-node-badge--${trackingBadges.get(entity.id)}`}
                          title={trackingBadgeLabels[trackingBadges.get(entity.id)!]}
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
