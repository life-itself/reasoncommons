import { useMemo } from "react";
import {
  type AlignmentDecision,
  type AlignmentStatus,
  type AlignmentSuggestion,
  type LoadedAlignment,
} from "./alignment";
import { indexModel, type LtpEntity, type LtpModel, type ModelIndex } from "./model";

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
