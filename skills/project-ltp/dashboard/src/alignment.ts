import { parse, stringify } from "yaml";
import { validateModel, type LtpModel } from "./model";
import { fetchText, type AlignmentSummary } from "./projects";

export type AlignmentRelation =
  | "advances"
  | "supports"
  | "provides_evidence_for"
  | "at_risk_of_conflicting_with"
  | "unclear";

export type AlignmentStatus = "suggested" | "confirmed" | "rejected" | "edited";

/** Aggregate state for a tree node's alignment badge: "open" covers
 * suggested/edited/mixed — anything that still needs a reviewer's eyes. */
export type AlignmentBadge = "open" | "confirmed" | "rejected";

export interface AlignmentSuggestion {
  [key: string]: unknown;
  id: string;
  source_entity: string;
  target_entity: string;
  relation: AlignmentRelation;
  rationale: string;
  confidence: "high" | "medium" | "low";
  status: AlignmentStatus;
  reviewer_note?: string;
}

export interface AlignmentInfo {
  source_project: string;
  source_model: string;
  target_project: string;
  target_model: string;
  method: string;
  generated_at?: string | null;
  note?: string;
}

/** The shape of an `alignments/<slug>.yaml` file — see
 * `skills/goal-alignment/references/alignment-suggestions.schema.json`. */
export interface AlignmentDoc {
  alignment: AlignmentInfo;
  suggestions: AlignmentSuggestion[];
  open_questions?: string[];
}

export interface LoadedAlignment {
  doc: AlignmentDoc;
  sourceModel: LtpModel;
  targetModel: LtpModel;
}

export function validateAlignment(value: unknown): AlignmentDoc {
  if (!value || typeof value !== "object") {
    throw new Error("The alignment file must be a YAML object.");
  }
  const doc = value as Partial<AlignmentDoc>;
  if (!doc.alignment?.source_project || !doc.alignment.target_project) {
    throw new Error("alignment.source_project and alignment.target_project are required");
  }
  if (!Array.isArray(doc.suggestions)) {
    throw new Error("suggestions must be an array");
  }

  const ids = new Set<string>();
  for (const suggestion of doc.suggestions) {
    if (
      !suggestion.id ||
      !suggestion.source_entity ||
      !suggestion.target_entity ||
      !suggestion.relation ||
      !suggestion.confidence ||
      !suggestion.status
    ) {
      throw new Error(
        "every suggestion needs id, source_entity, target_entity, relation, confidence, and status",
      );
    }
    if (ids.has(suggestion.id)) throw new Error(`duplicate suggestion id: ${suggestion.id}`);
    ids.add(suggestion.id);
  }
  return doc as AlignmentDoc;
}

async function requireText(url: string): Promise<string> {
  const text = await fetchText(url);
  if (!text) throw new Error(`${url} could not be loaded`);
  return text;
}

export async function loadAlignment(summary: AlignmentSummary): Promise<LoadedAlignment> {
  const file = summary.file ?? `alignments/${summary.slug}.yaml`;
  const [alignmentText, sourceText, targetText] = await Promise.all([
    requireText(`projects/${file}`),
    requireText(`projects/${summary.source_project}/model.yaml`),
    requireText(`projects/${summary.target_project}/model.yaml`),
  ]);
  return {
    doc: validateAlignment(parse(alignmentText)),
    sourceModel: validateModel(parse(sourceText)),
    targetModel: validateModel(parse(targetText)),
  };
}

/** A reviewer's live (unsaved) decision on one suggestion — starts from the
 * suggestion's own `status`/`reviewer_note` and is edited in the tree UI. */
export interface AlignmentDecision {
  status: AlignmentStatus;
  note: string;
}

export function initAlignmentDecisions(doc: AlignmentDoc): Record<string, AlignmentDecision> {
  return Object.fromEntries(
    doc.suggestions.map((s) => [s.id, { status: s.status, note: s.reviewer_note ?? "" }]),
  );
}

export function tallyAlignmentDecisions(
  doc: AlignmentDoc,
  decisions: Record<string, AlignmentDecision>,
): Record<AlignmentStatus, number> {
  const tally: Record<AlignmentStatus, number> = { suggested: 0, confirmed: 0, rejected: 0, edited: 0 };
  for (const suggestion of doc.suggestions) {
    const status = decisions[suggestion.id]?.status ?? suggestion.status;
    tally[status] += 1;
  }
  return tally;
}

/** True once every suggestion touching this entity is `rejected` — used to
 * fade its tree-node badge rather than showing it as still-open. */
export function isEntityFullyRejected(
  entityId: string,
  doc: AlignmentDoc,
  decisions: Record<string, AlignmentDecision>,
): boolean {
  const matching = doc.suggestions.filter((s) => s.source_entity === entityId);
  return matching.length > 0 && matching.every((s) => (decisions[s.id]?.status ?? s.status) === "rejected");
}

export function isEntityFullyConfirmed(
  entityId: string,
  doc: AlignmentDoc,
  decisions: Record<string, AlignmentDecision>,
): boolean {
  const matching = doc.suggestions.filter((s) => s.source_entity === entityId);
  return matching.length > 0 && matching.every((s) => (decisions[s.id]?.status ?? s.status) === "confirmed");
}

export function downloadReviewedAlignment(
  doc: AlignmentDoc,
  decisions: Record<string, AlignmentDecision>,
): void {
  const reviewed = {
    alignment: { ...doc.alignment, method: "steward-reviewed" },
    suggestions: doc.suggestions.map((s) => ({
      ...s,
      status: decisions[s.id]?.status ?? s.status,
      reviewer_note: decisions[s.id]?.note || undefined,
    })),
    open_questions: doc.open_questions,
  };
  const blob = new Blob([stringify(reviewed)], { type: "text/yaml" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${doc.alignment.source_project}__${doc.alignment.target_project}.reviewed.yaml`;
  link.click();
  URL.revokeObjectURL(url);
}
