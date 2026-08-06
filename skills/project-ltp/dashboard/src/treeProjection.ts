import type {
  Confidence,
  EntityStatus,
  LtpEntity,
  LtpLink,
  LtpModel,
  ModelIndex,
  TreeView,
} from "./model";

export interface TreeProjection {
  entities: LtpEntity[];
  links: LtpLink[];
  roots: string[];
  childrenByParent: Map<string, string[]>;
  visibleIds: Set<string>;
}

interface ProjectionOptions {
  model: LtpModel;
  index: ModelIndex;
  view: TreeView;
  statuses: Set<EntityStatus>;
  confidences: Set<Confidence>;
  expandedIds: Set<string>;
}

function addUnique(map: Map<string, string[]>, key: string, value: string) {
  const values = map.get(key) ?? [];
  if (!values.includes(value)) values.push(value);
  map.set(key, values);
}

export function buildTreeProjection({
  model,
  index,
  view,
  statuses,
  confidences,
  expandedIds,
}: ProjectionOptions): TreeProjection {
  const viewDefinition = model.views[view];
  if (!viewDefinition) {
    return {
      entities: [],
      links: [],
      roots: [],
      childrenByParent: new Map(),
      visibleIds: new Set(),
    };
  }

  const availableEntities = viewDefinition.entities
    .map((id) => index.entities.get(id))
    .filter((entity): entity is LtpEntity => Boolean(entity))
    .filter(
      (entity) => statuses.has(entity.status) && confidences.has(entity.confidence),
    );
  const availableIds = new Set(availableEntities.map((entity) => entity.id));
  const availableLinks = viewDefinition.links
    .map((id) => index.links.get(id))
    .filter((link): link is LtpLink => Boolean(link))
    .filter((link) => availableIds.has(link.from) && availableIds.has(link.to));

  // LTP links point from a condition/cause to the outcome it supports. The
  // outcome is therefore the disclosure parent, and its incoming sources are
  // the children revealed when it expands. Conflict links are lateral.
  const childrenByParent = new Map<string, string[]>();
  const parentsByChild = new Map<string, string[]>();
  for (const link of availableLinks) {
    if (link.relation === "conflicts_with" || link.from === link.to) continue;
    addUnique(childrenByParent, link.to, link.from);
    addUnique(parentsByChild, link.from, link.to);
  }

  let roots = availableEntities
    .filter((entity) => !parentsByChild.has(entity.id))
    .map((entity) => entity.id);
  if (!roots.length) {
    // A malformed cyclic view should remain inspectable rather than rendering
    // an empty canvas.
    roots = availableEntities.map((entity) => entity.id);
  }

  const visibleIds = new Set(roots);
  const queue = [...roots];
  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const parentId = queue[cursor];
    if (!expandedIds.has(parentId)) continue;
    for (const childId of childrenByParent.get(parentId) ?? []) {
      if (visibleIds.has(childId)) continue;
      visibleIds.add(childId);
      queue.push(childId);
    }
  }

  return {
    entities: availableEntities.filter((entity) => visibleIds.has(entity.id)),
    links: availableLinks.filter(
      (link) => visibleIds.has(link.from) && visibleIds.has(link.to),
    ),
    roots,
    childrenByParent,
    visibleIds,
  };
}

export interface OrderedTreeEntity {
  entity: LtpEntity;
  depth: number;
}

/** Stable partition: unfinished ids first, completed ones sink to the end,
 * without disturbing relative order within either group. */
function sinkCompleted(ids: string[], completedIds?: Set<string>): string[] {
  if (!completedIds) return ids;
  const pending: string[] = [];
  const done: string[] = [];
  for (const id of ids) (completedIds.has(id) ? done : pending).push(id);
  return [...pending, ...done];
}

export function orderTreeProjection(
  projection: TreeProjection,
  expandedIds: Set<string>,
  completedIds?: Set<string>,
): OrderedTreeEntity[] {
  const entitiesById = new Map(
    projection.entities.map((entity) => [entity.id, entity]),
  );
  const ordered: OrderedTreeEntity[] = [];
  const visited = new Set<string>();

  const visit = (entityId: string, depth: number) => {
    const entity = entitiesById.get(entityId);
    if (!entity || visited.has(entityId)) return;
    visited.add(entityId);
    ordered.push({ entity, depth });
    if (!expandedIds.has(entityId)) return;
    const children = (projection.childrenByParent.get(entityId) ?? []).filter(
      (childId) => projection.visibleIds.has(childId),
    );
    for (const childId of sinkCompleted(children, completedIds)) {
      visit(childId, depth + 1);
    }
  };

  for (const rootId of sinkCompleted(projection.roots, completedIds)) visit(rootId, 0);
  for (const entity of projection.entities) visit(entity.id, 0);
  return ordered;
}
