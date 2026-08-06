import {
  downloadReviewedAlignment,
  tallyAlignmentDecisions,
  type AlignmentDecision,
  type LoadedAlignment,
} from "./alignment";
import type {
  LtpEntity,
  LtpModel,
  ModelIndex,
  ThroughputData,
  ThroughputPeriod,
} from "./model";
import { tallyTracking, type TrackingLedger } from "./tracking";

interface OverviewProps {
  model: LtpModel;
  index: ModelIndex;
  throughput: ThroughputData | null;
  tracking: TrackingLedger | null;
  alignment: LoadedAlignment | null;
  alignmentDecisions: Record<string, AlignmentDecision>;
  onSelect: (entityId: string) => void;
  onExplore: () => void;
  onJumpToEntity: (entityId: string) => void;
}

function Sparkline({ values }: { values: number[] }) {
  if (values.length < 2) return <div className="sparkline-empty" aria-hidden="true" />;
  const width = 180;
  const height = 48;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const points = values
    .map((value, index) => {
      const x = (index / (values.length - 1)) * width;
      const y = height - 5 - ((value - min) / range) * (height - 10);
      return `${x},${y}`;
    })
    .join(" ");
  return (
    <svg className="sparkline" viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`Trend from ${values[0]} to ${values.at(-1)}`}>
      <polyline points={points} fill="none" vectorEffect="non-scaling-stroke" />
      <circle cx={width} cy={Number(points.split(" ").at(-1)?.split(",")[1])} r="3.5" />
    </svg>
  );
}

type ThroughputMetric = Exclude<keyof ThroughputPeriod, "date">;

function metricValue(period: ThroughputPeriod, key: ThroughputMetric): string {
  const value = period[key];
  if (value === undefined) return "—";
  if (key === "median_cycle_time_days") return `${value}d`;
  return String(value);
}

export function Overview({
  model,
  index,
  throughput,
  tracking,
  alignment,
  alignmentDecisions,
  onSelect,
  onExplore,
  onJumpToEntity,
}: OverviewProps) {
  const constraint = model.analysis?.current_constraint
    ? index.entities.get(model.analysis.current_constraint)
    : undefined;
  const action = model.analysis?.recommended_next_action
    ? index.entities.get(model.analysis.recommended_next_action)
    : undefined;
  const effect = model.analysis?.expected_effect
    ? index.entities.get(model.analysis.expected_effect)
    : undefined;
  const story: Array<{ label: string; entity?: LtpEntity; fallback: string }> = [
    { label: "Current constraint", entity: constraint, fallback: "Not identified" },
    { label: "Next move", entity: action, fallback: "Not selected" },
    { label: "Expected shift", entity: effect, fallback: "Not modelled" },
  ];
  const latest = throughput?.periods.at(-1);
  const countedRevisions = throughput?.revisions ?? [];
  const hasNodeDeltaBreakdown =
    latest &&
    ["created", "updated", "deleted"].some(
      (key) => typeof latest[key as ThroughputMetric] === "number",
    );
  const metricCards: Array<{ key: ThroughputMetric; label: string }> =
    hasNodeDeltaBreakdown
      ? [
          { key: "throughput", label: "Throughput" },
          { key: "created", label: "Nodes created" },
          { key: "updated", label: "Nodes updated" },
          { key: "deleted", label: "Nodes deleted" },
        ]
      : [
          { key: "throughput", label: "Throughput" },
          { key: "work_in_progress", label: "Work in progress" },
          { key: "blocked", label: "Blocked" },
          { key: "median_cycle_time_days", label: "Cycle time" },
          { key: "constraint_queue", label: "Constraint queue" },
        ];
  const trends: Array<{ key: ThroughputMetric; label: string }> =
    hasNodeDeltaBreakdown
      ? [
          { key: "throughput", label: "Goal throughput" },
          { key: "created", label: "Nodes created" },
          { key: "updated", label: "Nodes updated" },
          { key: "deleted", label: "Nodes deleted" },
        ]
      : [
          { key: "throughput", label: "Goal throughput" },
          { key: "work_in_progress", label: "Work in progress" },
          { key: "median_cycle_time_days", label: "Cycle time" },
        ];
  const alignmentTally = alignment ? tallyAlignmentDecisions(alignment.doc, alignmentDecisions) : null;
  const firstSuggestion = alignment?.doc.suggestions[0];
  // Actions of the transition tree, in the order the view lists them — the
  // same set the sync tracks, so the tally counts untracked nodes too.
  const actionIds = (model.views["transition-tree"]?.entities ?? []).filter(
    (id) => index.entities.get(id)?.type === "action",
  );
  const trackingTally = tracking ? tallyTracking(tracking, actionIds) : null;
  const firstUntrackedAction = actionIds.find((id) => !tracking?.actions[id]?.issue);

  return (
    <main className="overview">
      <section className="overview-hero">
        <div>
          <span className="eyebrow">The system at a glance</span>
          <h1>{model.project.name}</h1>
          <p>Follow the limiting condition to the next action and the effect it is meant to create.</p>
        </div>
        <button type="button" className="primary-button" onClick={onExplore}>Explore the logic <span>→</span></button>
      </section>

      <section className="logic-story" aria-label="Constraint to action story">
        {story.map((step, indexValue) => (
          <div className="story-step-wrap" key={step.label}>
            <button
              type="button"
              className={`story-step story-step--${indexValue + 1}`}
              disabled={!step.entity}
              onClick={() => step.entity && onSelect(step.entity.id)}
            >
              <span>{step.label}</span>
              <strong>{step.entity?.statement ?? step.fallback}</strong>
              {step.entity && <small>{step.entity.id} · {step.entity.confidence} confidence</small>}
            </button>
            {indexValue < story.length - 1 && <span className="story-arrow" aria-hidden="true">→</span>}
          </div>
        ))}
      </section>

      {alignment && alignmentTally && (
        <section className="overview-alignment" aria-label="Alignment suggestions">
          <div>
            <span className="eyebrow">Alignment · suggested, not merged</span>
            <p>
              <strong>{alignment.doc.suggestions.length}</strong> suggestions to{" "}
              <strong>{alignment.targetModel.project.name}</strong> — {alignmentTally.confirmed} confirmed,{" "}
              {alignmentTally.rejected} rejected, {alignmentTally.suggested + alignmentTally.edited} still open.
              Look for <i className="alignment-node-badge" /> on nodes in the tree.
            </p>
          </div>
          <div className="overview-alignment__actions">
            {firstSuggestion && (
              <button
                type="button"
                className="switch-project"
                onClick={() => onJumpToEntity(firstSuggestion.source_entity)}
              >
                Review in the tree <span aria-hidden="true">→</span>
              </button>
            )}
            <button
              type="button"
              className="switch-project"
              onClick={() => downloadReviewedAlignment(alignment.doc, alignmentDecisions)}
            >
              Export decisions <span aria-hidden="true">↓</span>
            </button>
          </div>
        </section>
      )}

      {tracking && trackingTally && (
        <section className="overview-tracking" aria-label="Tracked work">
          <div>
            <span className="eyebrow">
              Tracked work{tracking.repo ? ` · ${tracking.repo}` : ""}
              {tracking.synced_at ? ` · synced ${tracking.synced_at.slice(0, 10)}` : ""}
            </span>
            <p>
              <strong>{trackingTally.tracked}</strong> of {actionIds.length} actions have an issue —{" "}
              {trackingTally.open} open, {trackingTally.done} done
              {trackingTally.dropped > 0 && `, ${trackingTally.dropped} dropped`}
              {trackingTally.untracked > 0 && `, ${trackingTally.untracked} not yet tracked`}
              {trackingTally.drifted > 0 && `, ${trackingTally.drifted} out of step with the tree`}. Look for{" "}
              <i className="tracking-node-badge tracking-node-badge--open" /> on action nodes.
            </p>
            {trackingTally.loose > 0 && (
              <p className="muted">
                {trackingTally.loose} tracked {trackingTally.loose === 1 ? "issue does" : "issues do"} not
                trace to any node in this tree.
              </p>
            )}
          </div>
          <div className="overview-alignment__actions">
            {firstUntrackedAction && (
              <button
                type="button"
                className="switch-project"
                onClick={() => onJumpToEntity(firstUntrackedAction)}
              >
                See what is untracked <span aria-hidden="true">→</span>
              </button>
            )}
            {tracking.repo && (
              <a
                className="switch-project"
                href={`https://github.com/${tracking.repo}/issues?q=is%3Aissue+label%3A${encodeURIComponent(tracking.label ?? "ltp-action")}`}
                target="_blank"
                rel="noreferrer noopener"
              >
                Open on GitHub <span aria-hidden="true">↗</span>
              </a>
            )}
          </div>
        </section>
      )}

      <section className="throughput-section">
        <header className="section-heading">
          <div>
            <span className="eyebrow">What counts</span>
            <h2>{throughput?.definition.name ?? "Throughput is not defined yet"}</h2>
            <p>
              {throughput
                ? `${throughput.definition.unit} per ${throughput.definition.period}`
                : "Add ltp/throughput.yaml only when the project has a defensible goal unit."}
            </p>
          </div>
          {latest && <time dateTime={latest.date}>Latest · {latest.date}</time>}
        </header>

        {latest ? (
          <>
            <div className="metric-grid">
              {metricCards.map(({ key, label }) => (
                <article className={key === "throughput" ? "metric-card metric-card--primary" : "metric-card"} key={key}>
                  <span>{label}</span>
                  <strong>{metricValue(latest, key)}</strong>
                </article>
              ))}
            </div>
            <details className="trend-disclosure">
              <summary>See trends <span>{trends.length} signals over time</span></summary>
              <div className="trend-grid">
                {trends.map(({ key, label }) => {
                  const values = throughput!.periods
                    .map((period) => period[key])
                    .filter((value): value is number => typeof value === "number");
                  return (
                    <article className="trend-card" key={key}>
                      <span>{label}</span>
                      <Sparkline values={values} />
                      <small>{values[0] ?? "—"} → {values.at(-1) ?? "—"}</small>
                    </article>
                  );
                })}
              </div>
            </details>
            {countedRevisions.length > 0 && (
              <details className="throughput-revisions">
                <summary>
                  Counted revisions <span>{countedRevisions.length} semantic changesets</span>
                </summary>
                <ol>
                  {countedRevisions.map((revision) => (
                    <li key={revision.revision}>
                      <div>
                        <code>{revision.revision.slice(0, 12)}</code>
                        <time dateTime={revision.date}>{revision.date}</time>
                        {revision.subject && <strong>{revision.subject}</strong>}
                      </div>
                      <span>{revision.throughput} node changes</span>
                      <dl>
                        <div><dt>Created</dt><dd>{revision.created.join(", ") || "—"}</dd></div>
                        <div><dt>Updated</dt><dd>{revision.updated.join(", ") || "—"}</dd></div>
                        <div><dt>Deleted</dt><dd>{revision.deleted.join(", ") || "—"}</dd></div>
                      </dl>
                    </li>
                  ))}
                </ol>
              </details>
            )}
          </>
        ) : (
          <div className="empty-panel">
            <span aria-hidden="true">○</span>
            <div><strong>No invented metrics.</strong><p>The tree still works; measurement appears when real data does.</p></div>
          </div>
        )}
      </section>

      <section className="model-health">
        <article><strong>{model.entities.length}</strong><span>conditions in the shared model</span></article>
        <article><strong>{model.evidence?.length ?? 0}</strong><span>evidence items attached</span></article>
        <article><strong>{model.open_questions?.length ?? 0}</strong><span>open questions</span></article>
        <article><strong>{model.contradictions?.length ?? 0}</strong><span>contradictions visible</span></article>
      </section>
    </main>
  );
}
