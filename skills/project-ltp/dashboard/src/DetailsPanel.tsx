import { useMemo } from "react";
import {
  type AlignmentDecision,
  type AlignmentStatus,
  type AlignmentSuggestion,
  type LoadedAlignment,
} from "./alignment";
import { indexModel, type LtpEntity, type LtpModel, type ModelIndex } from "./model";
import {
  trackingBadge,
  trackingBadgeLabels,
  type TrackingLedger,
} from "./tracking";

const syncStatusNotes: Record<string, string> = {
  "in-sync": "The issue matches this tree node.",
  update: "This tree node changed after the issue was written. Run a push to update the issue.",
  create: "No issue tracks this action yet. Run a push to open one.",
  "issue-edited": "The issue body was edited on GitHub. The tree node still says what it said before.",
  conflict: "The tree node and the issue body have both changed. Someone has to decide which is right.",
  "missing-remote": "The recorded issue could not be found — deleted, transferred, or unlabelled.",
};

const relationLabels: Record<string, string> = {
  advances: "advances",
  supports: "supports",
  provides_evidence_for: "provides evidence for",
  at_risk_of_conflicting_with: "may conflict with",
  unclear: "unclear relation to",
};

interface DetailsPanelProps {
  entity: LtpEntity | null;
  model: LtpModel;
  index: ModelIndex;
  tracking: TrackingLedger | null;
  alignment: LoadedAlignment | null;
  alignmentSuggestions: AlignmentSuggestion[];
  alignmentDecisions: Record<string, AlignmentDecision>;
  onSetAlignmentStatus: (suggestionId: string, status: AlignmentStatus) => void;
  onSetAlignmentNote: (suggestionId: string, note: string) => void;
  onClose: () => void;
}

export function DetailsPanel({
  entity,
  model,
  index,
  tracking,
  alignment,
  alignmentSuggestions,
  alignmentDecisions,
  onSetAlignmentStatus,
  onSetAlignmentNote,
  onClose,
}: DetailsPanelProps) {
  const targetIndex = useMemo(
    () => (alignment ? indexModel(alignment.targetModel) : null),
    [alignment],
  );
  if (!entity) return null;
  const evidence = (entity.evidence ?? [])
    .map((id) => index.evidence.get(id))
    .filter(Boolean);
  const incoming = model.links.filter((link) => link.to === entity.id);
  const outgoing = model.links.filter((link) => link.from === entity.id);
  const views = Object.entries(model.views)
    .filter(([, view]) => view?.entities.includes(entity.id))
    .map(([name]) => name.replaceAll("-", " "));
  // Only actions are tracked, and only once a sync has run for this project.
  const tracked = tracking?.actions[entity.id] ?? null;
  const badge = tracked ? trackingBadge(tracked) : null;

  return (
    <aside className="details-panel" aria-label={`Details for ${entity.id}`}>
      <div className="details-panel__topline">
        <span className="eyebrow">Selected node</span>
        <button className="icon-button" type="button" onClick={onClose} aria-label="Close details">
          ×
        </button>
      </div>
      <div className="entity-identity">
        <strong>{entity.id}</strong>
        <span>{entity.type.replaceAll("_", " ")}</span>
      </div>
      <h2>{entity.statement}</h2>
      <div className="fact-row">
        <span><i className={`status-mark status-mark--${entity.status}`} />{entity.status}</span>
        <span>{entity.confidence} confidence</span>
      </div>

      {tracked && badge && (
        <section className={`tracking-card tracking-card--${badge}`}>
          <div className="tracking-card__head">
            <span className="eyebrow">Tracked work</span>
            <span className={`tracking-node-badge tracking-node-badge--${badge}`} aria-hidden="true" />
            <strong>{trackingBadgeLabels[badge]}</strong>
          </div>
          <p className="tracking-card__line">
            {tracked.url ? (
              <a href={tracked.url} target="_blank" rel="noreferrer noopener">
                {tracking?.repo ? `${tracking.repo}#${tracked.issue}` : `#${tracked.issue}`}
              </a>
            ) : (
              <span className="muted">No issue</span>
            )}
            {tracked.assignees?.length ? <span> · {tracked.assignees.map((a) => `@${a}`).join(", ")}</span> : null}
            {tracked.updated_at ? <span> · updated {tracked.updated_at.slice(0, 10)}</span> : null}
          </p>
          {tracked.sync_status && syncStatusNotes[tracked.sync_status] && (
            <p className="muted">{syncStatusNotes[tracked.sync_status]}</p>
          )}
        </section>
      )}

      {entity.reasoning && (
        <section className="detail-section">
          <h3>Why this is in the model</h3>
          <p>{entity.reasoning}</p>
        </section>
      )}

      {alignmentSuggestions.length > 0 && (
        <details className="detail-disclosure alignment-disclosure" open>
          <summary>
            Alignment suggestions <span>{alignmentSuggestions.length}</span>
          </summary>
          <div className="disclosure-body">
            <p className="muted alignment-disclosure__hint">
              AI-proposed links to <strong>{alignment!.targetModel.project.name}</strong> — suggested,
              not merged. Review each one below.
            </p>
            {alignmentSuggestions.map((suggestion) => {
              const targetEntity = targetIndex?.entities.get(suggestion.target_entity);
              const decision = alignmentDecisions[suggestion.id] ?? {
                status: suggestion.status,
                note: suggestion.reviewer_note ?? "",
              };
              return (
                <article
                  key={suggestion.id}
                  className={`alignment-suggestion-card alignment-suggestion-card--${decision.status}`}
                >
                  <div className="alignment-suggestion-card__target">
                    <span
                      className={`alignment-relation__badge alignment-relation__badge--${suggestion.relation}`}
                    >
                      {relationLabels[suggestion.relation] ?? suggestion.relation}
                    </span>
                    <strong>{targetEntity?.id ?? suggestion.target_entity}</strong>
                    <small>{suggestion.confidence} confidence</small>
                  </div>
                  <p>{targetEntity?.statement ?? "Entity not found in target model."}</p>
                  <p className="muted">{suggestion.rationale}</p>
                  <div className="alignment-suggestion-card__actions">
                    <button
                      type="button"
                      className={decision.status === "confirmed" ? "is-active" : ""}
                      onClick={() => onSetAlignmentStatus(suggestion.id, "confirmed")}
                    >
                      Confirm
                    </button>
                    <button
                      type="button"
                      className={decision.status === "rejected" ? "is-active" : ""}
                      onClick={() => onSetAlignmentStatus(suggestion.id, "rejected")}
                    >
                      Reject
                    </button>
                    <button
                      type="button"
                      disabled={decision.status === "suggested"}
                      onClick={() => onSetAlignmentStatus(suggestion.id, "suggested")}
                    >
                      Reset
                    </button>
                  </div>
                  <input
                    type="text"
                    className="alignment-note-input"
                    placeholder="Reviewer note (optional)"
                    value={decision.note}
                    onChange={(event) => onSetAlignmentNote(suggestion.id, event.target.value)}
                  />
                </article>
              );
            })}
          </div>
        </details>
      )}

      <details className="detail-disclosure" open={evidence.length > 0}>
        <summary>Evidence <span>{evidence.length}</span></summary>
        <div className="disclosure-body">
          {!evidence.length && <p className="muted">No evidence attached.</p>}
          {evidence.map((item) => (
            <article className="evidence-card" key={item!.id}>
              <div><strong>{item!.id}</strong><code>{item!.source}{item!.lines ? `:${item!.lines}` : ""}</code></div>
              <p>{item!.observation}</p>
              {item!.interpretation && <small>{item!.interpretation}</small>}
            </article>
          ))}
        </div>
      </details>

      <details className="detail-disclosure">
        <summary>Assumptions <span>{entity.assumptions?.length ?? 0}</span></summary>
        <div className="disclosure-body">
          {!entity.assumptions?.length ? (
            <p className="muted">No assumptions attached.</p>
          ) : (
            <ul>{entity.assumptions.map((item) => <li key={item}>{item}</li>)}</ul>
          )}
        </div>
      </details>

      <details className="detail-disclosure">
        <summary>Causal connections <span>{incoming.length + outgoing.length}</span></summary>
        <div className="disclosure-body connection-list">
          {incoming.map((link) => (
            <p key={link.id}><code>{link.from}</code><span>→ {link.relation.replaceAll("_", " ")} →</span><strong>{entity.id}</strong></p>
          ))}
          {outgoing.map((link) => (
            <p key={link.id}><strong>{entity.id}</strong><span>→ {link.relation.replaceAll("_", " ")} →</span><code>{link.to}</code></p>
          ))}
        </div>
      </details>

      <div className="view-membership">
        <span className="eyebrow">Appears in</span>
        <p>{views.join(" · ") || "No view"}</p>
      </div>
    </aside>
  );
}
