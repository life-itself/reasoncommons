import { useEffect, useMemo, useRef, type CSSProperties } from "react";
import Dagre from "@dagrejs/dagre";
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  type Edge,
  type Node,
  type NodeProps,
  type ReactFlowInstance,
} from "@xyflow/react";
import type { AlignmentBadge } from "./alignment";
import type {
  Confidence,
  EntityStatus,
  LtpEntity,
  LtpModel,
  ModelIndex,
  TreeView,
} from "./model";
import { buildTreeProjection } from "./treeProjection";

const NODE_WIDTH = 280;
const NODE_HEIGHT = 156;
const DISCLOSURE_DURATION = 460;

function transitionName(entityId: string): string {
  return `ltp-${entityId.replaceAll(/[^a-zA-Z0-9_-]/g, "-")}`;
}

type FlowNodeData = {
  [key: string]: unknown;
  entity: LtpEntity;
  childCount: number;
  expanded: boolean;
  alignmentBadge?: AlignmentBadge;
  onToggle: (entityId: string) => void;
};

type FlowNode = Node<FlowNodeData, "ltp">;

function LtpNode({ data, selected }: NodeProps<FlowNode>) {
  const { entity } = data;
  return (
    <article
      className={`ltp-node ltp-node--${entity.type} ${selected ? "is-selected" : ""}`}
      data-status={entity.status}
    >
      <Handle type="target" position={Position.Top} className="ltp-handle" />
      <header>
        <span className="node-id">{entity.id}</span>
        {data.alignmentBadge && (
          <i
            className={`alignment-node-badge alignment-node-badge--${data.alignmentBadge}`}
            title={
              data.alignmentBadge === "confirmed"
                ? "Alignment suggestion confirmed"
                : data.alignmentBadge === "rejected"
                  ? "Alignment suggestion rejected"
                  : "Has an alignment suggestion"
            }
          />
        )}
        <span className="node-type">{entity.type.replaceAll("_", " ")}</span>
        {data.childCount > 0 && (
          <button
            className="node-disclosure nodrag nopan"
            type="button"
            aria-label={data.expanded ? `Collapse ${entity.id}` : `Expand ${entity.id}`}
            aria-expanded={data.expanded}
            onClick={(event) => {
              event.stopPropagation();
              data.onToggle(entity.id);
            }}
          >
            <span aria-hidden="true">{data.expanded ? "−" : "+"}</span>
          </button>
        )}
      </header>
      <p>{entity.statement}</p>
      <footer>
        <span className={`status-mark status-mark--${entity.status}`} aria-hidden="true" />
        <span>{entity.status}</span>
        {data.childCount > 0 && (
          <span className="node-branches">
            {data.childCount} {data.childCount === 1 ? "branch" : "branches"}
          </span>
        )}
        <span className="node-confidence">{entity.confidence}</span>
      </footer>
      <Handle type="source" position={Position.Bottom} className="ltp-handle" />
    </article>
  );
}

const nodeTypes = { ltp: LtpNode };

function layout(nodes: FlowNode[], edges: Edge[]): FlowNode[] {
  const graph = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  graph.setGraph({
    rankdir: "TB",
    ranksep: 86,
    nodesep: 42,
    marginx: 34,
    marginy: 34,
  });
  for (const node of nodes) {
    graph.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
  }
  for (const edge of edges) graph.setEdge(edge.source, edge.target);
  Dagre.layout(graph);
  return nodes.map((node) => {
    const position = graph.node(node.id);
    return {
      ...node,
      position: {
        x: position.x - NODE_WIDTH / 2,
        y: position.y - NODE_HEIGHT / 2,
      },
      style: {
        width: NODE_WIDTH,
        minHeight: NODE_HEIGHT,
        viewTransitionName: transitionName(node.id),
      } as CSSProperties,
    };
  });
}

interface TreeCanvasProps {
  model: LtpModel;
  index: ModelIndex;
  view: TreeView;
  statuses: Set<EntityStatus>;
  confidences: Set<Confidence>;
  expandedIds: Set<string>;
  collapsingIds: Set<string>;
  selectedId: string | null;
  alignmentBadges?: Map<string, AlignmentBadge>;
  onToggle: (entityId: string) => void;
  onSelect: (entityId: string | null) => void;
}

export function TreeCanvas({
  model,
  index,
  view,
  statuses,
  confidences,
  expandedIds,
  collapsingIds,
  selectedId,
  alignmentBadges,
  onToggle,
  onSelect,
}: TreeCanvasProps) {
  const flowInstance = useRef<ReactFlowInstance<FlowNode, Edge> | null>(null);
  const flow = useMemo(() => {
    const projection = buildTreeProjection({
      model,
      index,
      view,
      statuses,
      confidences,
      expandedIds,
    });
    const settledExpandedIds = new Set(expandedIds);
    for (const entityId of collapsingIds) settledExpandedIds.delete(entityId);
    const settledProjection = buildTreeProjection({
      model,
      index,
      view,
      statuses,
      confidences,
      expandedIds: settledExpandedIds,
    });
    const exitingIds = new Set(
      projection.entities
        .filter((entity) => !settledProjection.visibleIds.has(entity.id))
        .map((entity) => entity.id),
    );
    const edges: Edge[] = projection.links
      .map((link) => ({
        id: link.id,
        source: link.from,
        target: link.to,
        type: link.relation === "conflicts_with" ? "straight" : "smoothstep",
        label: link.relation.replaceAll("_", " "),
        markerEnd: { type: MarkerType.ArrowClosed, width: 16, height: 16 },
        className: [
          link.relation === "conflicts_with" ? "edge-conflict" : "",
          exitingIds.has(link.from) || exitingIds.has(link.to)
            ? "is-collapsing"
            : "",
        ].filter(Boolean).join(" "),
      }));
    const nodes: FlowNode[] = projection.entities.map((entity) => ({
      id: entity.id,
      type: "ltp",
      data: {
        entity,
        childCount: projection.childrenByParent.get(entity.id)?.length ?? 0,
        expanded: expandedIds.has(entity.id),
        alignmentBadge: alignmentBadges?.get(entity.id),
        onToggle,
      },
      selected: selectedId === entity.id,
      className: exitingIds.has(entity.id) ? "is-collapsing" : "",
      position: { x: 0, y: 0 },
    }));
    return { nodes: layout(nodes, edges), edges };
  }, [
    alignmentBadges,
    confidences,
    collapsingIds,
    expandedIds,
    index,
    model,
    onToggle,
    selectedId,
    statuses,
    view,
  ]);
  const visibleNodeKey = flow.nodes.map((node) => node.id).join("|");

  useEffect(() => {
    if (!flowInstance.current) return;
    const frame = window.requestAnimationFrame(() => {
      void flowInstance.current?.fitView({
        padding: 0.22,
        duration: DISCLOSURE_DURATION,
      });
    });
    return () => window.cancelAnimationFrame(frame);
  }, [visibleNodeKey]);

  if (!model.views[view]) {
    return (
      <div className="canvas-empty">
        <strong>This view has not been modelled yet.</strong>
        <span>Add it under <code>views.{view}</code> in ltp-model.yaml.</span>
      </div>
    );
  }
  if (!flow.nodes.length) {
    return (
      <div className="canvas-empty">
        <strong>No nodes match the current filters.</strong>
        <span>Broaden status or confidence under Refine.</span>
      </div>
    );
  }

  return (
    <ReactFlow
      nodes={flow.nodes}
      edges={flow.edges}
      nodeTypes={nodeTypes}
      fitView
      fitViewOptions={{ padding: 0.22 }}
      minZoom={0.15}
      maxZoom={1.8}
      nodesConnectable={false}
      nodesDraggable
      elementsSelectable
      onInit={(instance) => {
        flowInstance.current = instance;
      }}
      onNodeClick={(_, node) => {
        onSelect(node.id);
        if (node.data.childCount) onToggle(node.id);
      }}
      onPaneClick={() => onSelect(null)}
      proOptions={{ hideAttribution: false }}
    >
      <Background gap={28} size={1} color="var(--grid-dot)" />
      <Controls showInteractive={false} />
    </ReactFlow>
  );
}
