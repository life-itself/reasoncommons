export const viewOrder = [
  "goal-tree",
  "current-reality",
  "evaporating-cloud",
  "future-reality",
  "prerequisite-tree",
  "transition-tree",
] as const;

export type TreeView = (typeof viewOrder)[number];
export type EntityStatus =
  | "observed"
  | "inferred"
  | "provisional"
  | "confirmed"
  | "disputed";
export type Confidence = "high" | "medium" | "low";

export interface ProjectInfo {
  name: string;
  analyzed_path?: string;
  analysis_mode?: string;
  provisional_goal?: string;
}

export interface AnalysisSummary {
  current_constraint?: string;
  recommended_next_action?: string;
  expected_effect?: string;
  updated_at?: string;
}

export interface LtpEntity {
  [key: string]: unknown;
  id: string;
  type: string;
  statement: string;
  status: EntityStatus;
  confidence: Confidence;
  evidence?: string[];
  assumptions?: string[];
  reasoning?: string;
}

export interface LtpLink {
  id: string;
  from: string;
  to: string;
  relation: string;
  logic?: string;
  assumption?: string;
  confidence?: Confidence;
}

export interface EvidenceItem {
  id: string;
  source: string;
  lines?: string;
  observation: string;
  interpretation?: string;
}

export interface LtpView {
  title?: string;
  purpose?: string;
  entities: string[];
  links: string[];
}

export interface LtpModel {
  project: ProjectInfo;
  analysis?: AnalysisSummary;
  entities: LtpEntity[];
  links: LtpLink[];
  evidence?: EvidenceItem[];
  views: Partial<Record<TreeView, LtpView>>;
  open_questions?: string[];
  contradictions?: string[];
  coverage_gaps?: string[];
}

export interface ThroughputDefinition {
  name: string;
  unit: string;
  period: string;
  goal_entity?: string;
  constraint_entity?: string;
  source?: string;
  source_project?: string;
  source_model?: string;
  baseline_revision?: string;
  counting_rule?: string;
}

export interface ThroughputPeriod {
  date: string;
  throughput?: number;
  created?: number;
  updated?: number;
  deleted?: number;
  completed?: number;
  work_in_progress?: number;
  blocked?: number;
  median_cycle_time_days?: number;
  constraint_queue?: number;
}

export interface ThroughputRevision {
  revision: string;
  date: string;
  subject?: string;
  throughput: number;
  created: string[];
  updated: string[];
  deleted: string[];
}

export interface ThroughputData {
  definition: ThroughputDefinition;
  periods: ThroughputPeriod[];
  revisions?: ThroughputRevision[];
}

export interface DashboardMeta {
  model: FileMeta;
  throughput: FileMeta;
  tracking?: FileMeta;
}

interface FileMeta {
  exists: boolean;
  modified_ns?: number;
  size?: number;
  name: string;
}

export interface ModelIndex {
  entities: Map<string, LtpEntity>;
  links: Map<string, LtpLink>;
  evidence: Map<string, EvidenceItem>;
}

export function indexModel(model: LtpModel): ModelIndex {
  return {
    entities: new Map(model.entities.map((entity) => [entity.id, entity])),
    links: new Map(model.links.map((link) => [link.id, link])),
    evidence: new Map((model.evidence ?? []).map((item) => [item.id, item])),
  };
}

export function validateModel(value: unknown): LtpModel {
  const errors: string[] = [];
  if (!value || typeof value !== "object") {
    throw new Error("The model must be a YAML object.");
  }
  const model = value as Partial<LtpModel>;
  if (!model.project?.name) errors.push("project.name is required");
  if (!Array.isArray(model.entities)) errors.push("entities must be an array");
  if (!Array.isArray(model.links)) errors.push("links must be an array");
  if (!model.views || typeof model.views !== "object") errors.push("views is required");
  if (errors.length) throw new Error(errors.join("; "));

  const entityIds = new Set<string>();
  for (const entity of model.entities!) {
    if (!entity.id || !entity.statement || !entity.type) {
      errors.push("every entity needs id, type, and statement");
      continue;
    }
    if (entityIds.has(entity.id)) errors.push(`duplicate entity id: ${entity.id}`);
    entityIds.add(entity.id);
  }

  const linkIds = new Set<string>();
  for (const link of model.links!) {
    if (!link.id || !link.from || !link.to || !link.relation) {
      errors.push("every link needs id, from, to, and relation");
      continue;
    }
    if (linkIds.has(link.id)) errors.push(`duplicate link id: ${link.id}`);
    linkIds.add(link.id);
    if (!entityIds.has(link.from)) errors.push(`${link.id} references missing entity ${link.from}`);
    if (!entityIds.has(link.to)) errors.push(`${link.id} references missing entity ${link.to}`);
  }

  for (const [viewName, view] of Object.entries(model.views!)) {
    if (!view) continue;
    for (const id of view.entities ?? []) {
      if (!entityIds.has(id)) errors.push(`${viewName} references missing entity ${id}`);
    }
    for (const id of view.links ?? []) {
      if (!linkIds.has(id)) errors.push(`${viewName} references missing link ${id}`);
    }
  }

  if (errors.length) throw new Error(errors.join("; "));
  return model as LtpModel;
}

export function validateThroughput(value: unknown): ThroughputData {
  if (!value || typeof value !== "object") {
    throw new Error("throughput.yaml must contain an object");
  }
  const data = value as Partial<ThroughputData>;
  if (!data.definition?.name || !data.definition.unit || !data.definition.period) {
    throw new Error("throughput.definition needs name, unit, and period");
  }
  if (!Array.isArray(data.periods)) {
    throw new Error("throughput.periods must be an array");
  }
  for (const period of data.periods) {
    if (!period?.date) {
      throw new Error("every throughput period needs a date");
    }
  }
  if (data.revisions !== undefined && !Array.isArray(data.revisions)) {
    throw new Error("throughput.revisions must be an array when present");
  }
  for (const revision of data.revisions ?? []) {
    if (
      !revision?.revision ||
      !revision.date ||
      typeof revision.throughput !== "number" ||
      !Array.isArray(revision.created) ||
      !Array.isArray(revision.updated) ||
      !Array.isArray(revision.deleted)
    ) {
      throw new Error(
        "every throughput revision needs revision, date, throughput, created, updated, and deleted",
      );
    }
  }
  return data as ThroughputData;
}

export const viewLabels: Record<
  TreeView,
  { short: string; title: string; purpose: string; question: string }
> = {
  "goal-tree": {
    short: "Goal",
    title: "What must be true",
    purpose: "Goal Tree",
    question: "What conditions make success possible?",
  },
  "current-reality": {
    short: "Reality",
    title: "Why it is stuck",
    purpose: "Current Reality Tree",
    question: "Which causes explain the effects we see?",
  },
  "evaporating-cloud": {
    short: "Conflict",
    title: "What is in tension",
    purpose: "Evaporating Cloud",
    question: "Which assumptions make both sides seem necessary?",
  },
  "future-reality": {
    short: "Future",
    title: "What resolves it",
    purpose: "Future Reality Tree",
    question: "How should the proposed change produce success?",
  },
  "prerequisite-tree": {
    short: "Sequence",
    title: "What comes first",
    purpose: "Prerequisite Tree",
    question: "Which obstacles must be overcome, and in what order?",
  },
  "transition-tree": {
    short: "Action",
    title: "What to do now",
    purpose: "Transition Tree",
    question: "Which action should create which observable effect?",
  },
};
