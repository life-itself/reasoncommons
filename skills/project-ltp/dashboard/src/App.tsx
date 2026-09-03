import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { DetailsPanel } from "./DetailsPanel";
import { Overview } from "./Overview";
import { ProjectPicker } from "./ProjectPicker";
import { TreeCanvas } from "./TreeCanvas";
import { TreeList } from "./TreeList";
import {
  initAlignmentDecisions,
  isEntityFullyConfirmed,
  isEntityFullyRejected,
  loadAlignment,
  type AlignmentBadge,
  type AlignmentDecision,
  type AlignmentStatus,
  type LoadedAlignment,
} from "./alignment";
import {
  indexModel,
  viewLabels,
  viewOrder,
  type Confidence,
  type DashboardMeta,
  type EntityStatus,
  type LtpModel,
  type ThroughputData,
  type TreeView,
} from "./model";
import {
  loadProjectModel,
  resolveProjectSource,
  type ProjectSource,
  type ProjectSummary,
} from "./projects";
import {
  currentRoute,
  formatRoute,
  sameRoute,
  type Route,
  type Screen,
} from "./routing";
import {
  buildTrackingBadges,
  fetchLiveTracking,
  DEFAULT_TRACKING_LABEL,
  type TrackingBadge,
  type TrackingLedger,
} from "./tracking";

type TreeMode = "graph" | "list";
const allStatuses: EntityStatus[] = ["observed", "confirmed", "inferred", "provisional", "disputed"];
const allConfidences: Confidence[] = ["high", "medium", "low"];
const noExpandedNodes = new Set<string>();
const noAlignmentBadges = new Map<string, AlignmentBadge>();
const noTrackingBadges = new Map<string, TrackingBadge>();
const COLLAPSE_DURATION = 240;

type ViewTransitionDocument = Document & {
  startViewTransition?: (update: () => void) => unknown;
};

function runDisclosureTransition(update: () => void) {
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  const transitionDocument = document as ViewTransitionDocument;
  if (prefersReducedMotion || !transitionDocument.startViewTransition) {
    update();
    return;
  }
  transitionDocument.startViewTransition(update);
}

/**
 * The project a route opens. The live server has a single unnamed model, and a
 * single static project opens straight away; otherwise only a link that names
 * a slug skips the picker.
 */
function projectForRoute(source: ProjectSource, route: Route): ProjectSummary | null {
  if (source.mode === "live") return source.projects[0] ?? null;
  if (route.slug) return source.projects.find((project) => project.slug === route.slug) ?? null;
  return source.projects.length === 1 ? source.projects[0] : null;
}

function fingerprint(meta: DashboardMeta): string {
  return JSON.stringify([
    meta.model.exists,
    meta.model.modified_ns,
    meta.model.size,
    meta.throughput.exists,
    meta.throughput.modified_ns,
    meta.throughput.size,
    meta.tracking?.exists,
    meta.tracking?.modified_ns,
    meta.tracking?.size,
  ]);
}

export default function App() {
  const [source, setSource] = useState<ProjectSource | null>(null);
  const [activeProject, setActiveProject] = useState<ProjectSummary | null>(null);
  const [model, setModel] = useState<LtpModel | null>(null);
  const [throughput, setThroughput] = useState<ThroughputData | null>(null);
  const [tracking, setTracking] = useState<TrackingLedger | null>(null);
  const [alignment, setAlignment] = useState<LoadedAlignment | null>(null);
  const [alignmentDecisions, setAlignmentDecisions] = useState<Record<string, AlignmentDecision>>({});
  const [screen, setScreen] = useState<Screen>("overview");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [treeMode, setTreeMode] = useState<TreeMode>("graph");
  const [expandedByView, setExpandedByView] = useState<
    Partial<Record<TreeView, Set<string>>>
  >({});
  const [collapsingByView, setCollapsingByView] = useState<
    Partial<Record<TreeView, Set<string>>>
  >({});
  const [statuses, setStatuses] = useState<Set<EntityStatus>>(new Set(allStatuses));
  const [confidences, setConfidences] = useState<Set<Confidence>>(new Set(allConfidences));
  const [showCompleted, setShowCompleted] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncState, setSyncState] = useState<"loading" | "ready" | "updated" | "error">("loading");
  const fingerprintRef = useRef<string | null>(null);
  const collapseTimersRef = useRef<Map<string, number>>(new Map());
  const routeWrittenRef = useRef(false);

  const isLive = source?.mode === "live";
  const canSwitch = source?.mode === "static" && source.projects.length > 1;

  const resetViewState = useCallback(() => {
    setScreen("overview");
    setSelectedId(null);
    setExpandedByView({});
    setCollapsingByView({});
  }, []);

  // Resolve where projects come from (static manifest, or the live /api server).
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const resolved = await resolveProjectSource();
        if (cancelled) return;
        setSource(resolved);
        // Honour the incoming link: it can name both the project to open and
        // the tree to land on. Without one, a single project (or the live
        // server) still opens straight away and two or more land on the picker.
        const route = currentRoute();
        const opening = projectForRoute(resolved, route);
        if (opening) setActiveProject(opening);
        if (opening && route.screen !== "overview") setScreen(route.screen);
      } catch (caught) {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "Could not load projects");
        setSyncState("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Load the active project's model whenever it changes.
  useEffect(() => {
    if (!source || !activeProject) return;
    let cancelled = false;
    setModel(null);
    setThroughput(null);
    setTracking(null);
    setSyncState("loading");
    (async () => {
      try {
        const loaded = await loadProjectModel(source, activeProject);
        if (cancelled) return;
        setModel(loaded.model);
        setThroughput(loaded.throughput);
        setTracking(loaded.tracking);
        setError(null);
        setSyncState("ready");
      } catch (caught) {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "Could not load the model");
        setSyncState("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [source, activeProject]);

  // Issue state goes stale the moment someone closes something, so refresh it
  // from GitHub after the snapshot has painted. Public repositories only; any
  // failure silently leaves the committed snapshot on screen.
  useEffect(() => {
    if (!activeProject) return;
    const repo = tracking?.repo ?? activeProject.github?.repo;
    if (!repo) return;
    if (tracking?.source === "live") return;
    const label = tracking?.label ?? activeProject.github?.label ?? DEFAULT_TRACKING_LABEL;
    let cancelled = false;
    (async () => {
      const live = await fetchLiveTracking(tracking, repo, label);
      if (!cancelled && live) setTracking(live);
    })();
    return () => {
      cancelled = true;
    };
  }, [activeProject, tracking]);

  // If this project has a pilot alignment to a collective tree, load it in the
  // background — its suggestions surface as badges on tree nodes, not as a
  // separate screen. Missing or broken alignment data never blocks the tree.
  useEffect(() => {
    setAlignment(null);
    setAlignmentDecisions({});
    if (!source || source.mode !== "static" || !activeProject) return;
    const summary = source.alignments.find((a) => a.source_project === activeProject.slug);
    if (!summary) return;
    let cancelled = false;
    (async () => {
      try {
        const loaded = await loadAlignment(summary);
        if (cancelled) return;
        setAlignment(loaded);
        setAlignmentDecisions(initAlignmentDecisions(loaded.doc));
      } catch {
        // No alignment pilot for this project, or it failed to load — the
        // tree still works fine without it.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [source, activeProject]);

  // Live mode only: poll file metadata and hot-reload the model on change.
  useEffect(() => {
    if (source?.mode !== "live" || !activeProject) return;
    let cancelled = false;
    const poll = async () => {
      try {
        const response = await fetch("/api/meta", { cache: "no-store" });
        if (!response.ok) return;
        const meta = (await response.json()) as DashboardMeta;
        const nextFingerprint = fingerprint(meta);
        if (fingerprintRef.current && fingerprintRef.current !== nextFingerprint) {
          try {
            const loaded = await loadProjectModel(source, activeProject);
            if (cancelled) return;
            setModel(loaded.model);
            setThroughput(loaded.throughput);
            setTracking(loaded.tracking);
            setError(null);
            setSyncState("updated");
            window.setTimeout(() => setSyncState("ready"), 1600);
          } catch {
            // The next successful poll will restore the model.
          }
        }
        fingerprintRef.current = nextFingerprint;
      } catch {
        // The next successful poll will restore the sync indicator.
      }
    };
    const timer = window.setInterval(() => {
      if (!cancelled) void poll();
    }, 2000);
    void poll();
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [source, activeProject]);

  useEffect(
    () => () => {
      for (const timer of collapseTimersRef.current.values()) {
        window.clearTimeout(timer);
      }
    },
    [],
  );

  const openProject = useCallback(
    (project: ProjectSummary) => {
      resetViewState();
      setActiveProject(project);
    },
    [resetViewState],
  );

  const backToProjects = useCallback(() => {
    resetViewState();
    setActiveProject(null);
    setModel(null);
    setThroughput(null);
    setTracking(null);
    setError(null);
  }, [resetViewState]);

  // Move to a route that arrived from outside React — currently the back and
  // forward buttons, which walk the entries the sync effect below pushed.
  const goToRoute = useCallback(
    (route: Route) => {
      if (!source) return;
      const project = projectForRoute(source, route);
      if (project?.slug !== activeProject?.slug) {
        if (project) openProject(project);
        else backToProjects();
      }
      // With no project open there is nothing to show a tree of, and
      // backToProjects has already returned to the picker.
      if (project) setScreen(route.screen);
    },
    [source, activeProject, openProject, backToProjects],
  );

  // Mirror the open project and screen in the address bar, so any view can be
  // linked to directly. The first write replaces the entry the page loaded
  // with; later ones push, which is what makes Back walk the views visited.
  useEffect(() => {
    if (!source) return;
    const route: Route = {
      // The live server holds one unnamed model, so its links carry the view only.
      slug: source.mode === "live" ? null : activeProject?.slug ?? null,
      screen,
    };
    if (!sameRoute(currentRoute(), route)) {
      const url = formatRoute(route);
      if (routeWrittenRef.current) window.history.pushState(null, "", url);
      else window.history.replaceState(null, "", url);
    }
    routeWrittenRef.current = true;
  }, [source, activeProject, screen]);

  useEffect(() => {
    const onPopState = () => goToRoute(currentRoute());
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, [goToRoute]);

  // A link can name a tree this project has not modelled — the nav disables
  // those buttons, but a URL bypasses the nav. Fall back to the overview
  // rather than rendering an empty canvas.
  useEffect(() => {
    if (model && screen !== "overview" && !model.views[screen]) setScreen("overview");
  }, [model, screen]);

  const index = useMemo(() => (model ? indexModel(model) : null), [model]);
  const selected = selectedId && index ? index.entities.get(selectedId) ?? null : null;

  const chooseScreen = (next: Screen) => {
    setScreen(next);
    setSelectedId(null);
  };

  const jumpToEntity = useCallback(
    (entityId: string) => {
      if (!model) return;
      const targetView = viewOrder.find((view) => model.views[view]?.entities.includes(entityId));
      setScreen(targetView ?? "goal-tree");
      setSelectedId(entityId);
    },
    [model],
  );

  const setAlignmentStatus = useCallback((suggestionId: string, status: AlignmentStatus) => {
    setAlignmentDecisions((current) => ({
      ...current,
      [suggestionId]: { ...current[suggestionId], status },
    }));
  }, []);

  const setAlignmentNote = useCallback((suggestionId: string, note: string) => {
    setAlignmentDecisions((current) => ({
      ...current,
      [suggestionId]: { ...current[suggestionId], note },
    }));
  }, []);

  const alignmentBadges = useMemo(() => {
    if (!alignment) return noAlignmentBadges;
    const map = new Map<string, AlignmentBadge>();
    for (const suggestion of alignment.doc.suggestions) {
      if (map.has(suggestion.source_entity)) continue;
      if (isEntityFullyConfirmed(suggestion.source_entity, alignment.doc, alignmentDecisions)) {
        map.set(suggestion.source_entity, "confirmed");
      } else if (isEntityFullyRejected(suggestion.source_entity, alignment.doc, alignmentDecisions)) {
        map.set(suggestion.source_entity, "rejected");
      } else {
        map.set(suggestion.source_entity, "open");
      }
    }
    return map;
  }, [alignment, alignmentDecisions]);

  const trackingBadges = useMemo(
    () => (tracking ? buildTrackingBadges(tracking) : noTrackingBadges),
    [tracking],
  );

  const toggleExpanded = useCallback(
    (view: TreeView, entityId: string, expanded: boolean) => {
      const updateExpanded = () => {
        setExpandedByView((current) => {
          const nextForView = new Set(current[view] ?? []);
          if (expanded) nextForView.delete(entityId);
          else nextForView.add(entityId);
          return { ...current, [view]: nextForView };
        });
      };

      if (!expanded) {
        runDisclosureTransition(updateExpanded);
        return;
      }

      setCollapsingByView((current) => {
        const nextForView = new Set(current[view] ?? []);
        nextForView.add(entityId);
        return { ...current, [view]: nextForView };
      });
      const timerKey = `${view}:${entityId}`;
      const existingTimer = collapseTimersRef.current.get(timerKey);
      if (existingTimer) window.clearTimeout(existingTimer);
      const timer = window.setTimeout(() => {
        runDisclosureTransition(updateExpanded);
        setCollapsingByView((current) => {
          const nextForView = new Set(current[view] ?? []);
          nextForView.delete(entityId);
          return { ...current, [view]: nextForView };
        });
        collapseTimersRef.current.delete(timerKey);
      }, COLLAPSE_DURATION);
      collapseTimersRef.current.set(timerKey, timer);
    },
    [],
  );

  const toggleFilter = <T extends string>(value: T, set: Set<T>, update: (next: Set<T>) => void) => {
    const next = new Set(set);
    if (next.has(value)) {
      if (next.size > 1) next.delete(value);
    } else {
      next.add(value);
    }
    update(next);
  };

  // Still resolving where projects come from.
  if (!source) {
    return (
      <main className="load-state">
        <div className={error ? "load-mark load-mark--error" : "load-mark"}>{error ? "!" : ""}</div>
        <h1>{error ? "The dashboard needs attention" : "Finding projects…"}</h1>
        <p>{error ?? "Locating the shared causal models to explore."}</p>
        {error && <button className="primary-button" onClick={() => window.location.reload()}>Try again</button>}
      </main>
    );
  }

  // Multi-project (static) mode with nothing loaded yet: the picker.
  if (source.mode === "static" && !model) {
    return (
      <ProjectPicker
        projects={source.projects}
        alignments={source.alignments}
        onOpen={openProject}
        loadingSlug={activeProject && !error ? activeProject.slug : null}
        error={error}
      />
    );
  }

  if (!model || !index) {
    return (
      <main className="load-state">
        <div className={error ? "load-mark load-mark--error" : "load-mark"}>{error ? "!" : ""}</div>
        <h1>{error ? "The model needs attention" : "Tracing the logic…"}</h1>
        <p>{error ?? "Loading the shared causal model and its evidence."}</p>
        {error && <button className="primary-button" onClick={() => window.location.reload()}>Try again</button>}
      </main>
    );
  }

  const activeView = screen === "overview" ? null : screen;
  const activeViewDefinition = activeView ? model.views[activeView] : null;
  const activeLabel = activeView ? viewLabels[activeView] : null;
  // The toggle only means anything on a view that actually contains actions —
  // gating on the view's own membership rather than hardcoding a view name
  // keeps this correct if a project ever tracks actions somewhere else.
  const viewHasActions =
    activeViewDefinition?.entities.some((id) => index.entities.get(id)?.type === "action") ?? false;
  const expandedIds = activeView
    ? expandedByView[activeView] ?? noExpandedNodes
    : noExpandedNodes;
  const collapsingIds = activeView
    ? collapsingByView[activeView] ?? noExpandedNodes
    : noExpandedNodes;
  const onToggleActiveNode = (entityId: string) => {
    if (activeView && !collapsingIds.has(entityId)) {
      toggleExpanded(activeView, entityId, expandedIds.has(entityId));
    }
  };
  const selectedSuggestions = selected
    ? alignment?.doc.suggestions.filter((s) => s.source_entity === selected.id) ?? []
    : [];

  return (
    <div className={`app-shell ${selected ? "has-details" : ""}`}>
      <header className="app-header">
        <div className="header-identity">
          <button className="brand" type="button" onClick={() => chooseScreen("overview")}>
            Project LTP
          </button>
          <span className="project-tag">{model.project.name}</span>
        </div>
        <div className="header-state">
          {isLive ? (
            <>
              <span className={`sync-state sync-state--${syncState}`}>
                <i />{syncState === "updated" ? "Model updated" : syncState === "error" ? "Sync issue" : "Live model"}
              </span>
              <span className="read-only">Local · read only</span>
            </>
          ) : (
            canSwitch && (
              <button type="button" className="switch-project" onClick={backToProjects}>
                <span aria-hidden="true">←</span> Projects
              </button>
            )
          )}
        </div>
      </header>

      <nav className="view-nav" aria-label="LTP views">
        <span className="view-nav__label">The logic, as it unfolds</span>
        <button className={screen === "overview" ? "is-active" : ""} onClick={() => chooseScreen("overview")}>
          <span>Overview</span><small>The whole story</small>
        </button>
        {viewOrder.map((view) => (
          <button
            key={view}
            className={screen === view ? "is-active" : ""}
            onClick={() => chooseScreen(view)}
            disabled={!model.views[view]}
          >
            <span>{viewLabels[view].short}</span><small>{viewLabels[view].title}</small>
          </button>
        ))}
      </nav>

      <div className="app-content">
        {screen === "overview" ? (
          <Overview
            model={model}
            index={index}
            throughput={throughput}
            tracking={tracking}
            alignment={alignment}
            alignmentDecisions={alignmentDecisions}
            onSelect={setSelectedId}
            onExplore={() => chooseScreen("goal-tree")}
            onJumpToEntity={jumpToEntity}
          />
        ) : (
          <main className="tree-screen">
            <header className="tree-heading">
              <div>
                <span className="eyebrow">{activeLabel!.purpose}</span>
                <h1>{activeViewDefinition?.title ?? activeLabel!.title}</h1>
                <p>{activeViewDefinition?.purpose ?? activeLabel!.question}</p>
              </div>
              <div className="tree-tools">
                <div className="tree-mode-switch" role="group" aria-label="Tree display">
                  <button
                    type="button"
                    className={treeMode === "graph" ? "is-active" : ""}
                    aria-pressed={treeMode === "graph"}
                    onClick={() => setTreeMode("graph")}
                  >
                    <span className="graph-icon" aria-hidden="true"><i /><i /><i /></span>
                    Graph
                  </button>
                  <button
                    type="button"
                    className={treeMode === "list" ? "is-active" : ""}
                    aria-pressed={treeMode === "list"}
                    onClick={() => setTreeMode("list")}
                  >
                    <span className="list-icon" aria-hidden="true"><i /><i /><i /></span>
                    List
                  </button>
                </div>
                {tracking && viewHasActions && (
                  <label className="completed-toggle">
                    <input
                      type="checkbox"
                      checked={showCompleted}
                      onChange={(event) => setShowCompleted(event.target.checked)}
                    />
                    Show completed
                  </label>
                )}
                <details className="filter-disclosure">
                  <summary>Refine <span>{statuses.size + confidences.size}/{allStatuses.length + allConfidences.length}</span></summary>
                  <div className="filter-panel">
                    <fieldset>
                      <legend>Status</legend>
                      {allStatuses.map((status) => (
                        <label key={status}>
                          <input
                            type="checkbox"
                            checked={statuses.has(status)}
                            onChange={() => toggleFilter(status, statuses, setStatuses)}
                          />
                          <i className={`status-mark status-mark--${status}`} />{status}
                        </label>
                      ))}
                    </fieldset>
                    <fieldset>
                      <legend>Confidence</legend>
                      {allConfidences.map((confidence) => (
                        <label key={confidence}>
                          <input
                            type="checkbox"
                            checked={confidences.has(confidence)}
                            onChange={() => toggleFilter(confidence, confidences, setConfidences)}
                          />
                          {confidence}
                        </label>
                      ))}
                    </fieldset>
                  </div>
                </details>
              </div>
            </header>
            <section
              className={`tree-stage tree-stage--${treeMode}`}
              aria-label={`${activeLabel!.purpose} ${treeMode}`}
            >
              {treeMode === "graph" ? (
                <TreeCanvas
                  key={activeView}
                  model={model}
                  index={index}
                  view={activeView!}
                  statuses={statuses}
                  confidences={confidences}
                  expandedIds={expandedIds}
                  collapsingIds={collapsingIds}
                  selectedId={selectedId}
                  alignmentBadges={alignmentBadges}
                  trackingBadges={trackingBadges}
                  showCompleted={showCompleted}
                  onToggle={onToggleActiveNode}
                  onSelect={setSelectedId}
                />
              ) : (
                <TreeList
                  model={model}
                  index={index}
                  view={activeView!}
                  statuses={statuses}
                  confidences={confidences}
                  expandedIds={expandedIds}
                  collapsingIds={collapsingIds}
                  selectedId={selectedId}
                  alignmentBadges={alignmentBadges}
                  trackingBadges={trackingBadges}
                  showCompleted={showCompleted}
                  onToggle={onToggleActiveNode}
                  onSelect={setSelectedId}
                />
              )}
              <details className="legend-disclosure">
                <summary>How to read this</summary>
                <div>
                  <span><i className="status-mark status-mark--observed" />Observed or confirmed</span>
                  <span><i className="status-mark status-mark--inferred" />Inferred or provisional</span>
                  <span><i className="status-mark status-mark--disputed" />Disputed</span>
                  {alignment && <span><i className="alignment-node-badge" />Has alignment suggestions</span>}
                  {tracking && (
                    <>
                      <span><i className="tracking-chip tracking-chip--open"><i className="tracking-node-badge tracking-node-badge--open" />Open</i>on an action node — issue open</span>
                      <span><i className="tracking-chip tracking-chip--done"><i className="tracking-node-badge tracking-node-badge--done" />Done</i>on an action node — closed as done</span>
                      <span><i className="tracking-chip tracking-chip--drifted"><i className="tracking-node-badge tracking-node-badge--drifted" />Out of step</i>issue no longer matches the tree</span>
                      <span><i className="tracking-rollup tracking-rollup--pending">1/3 done</i>on any other node — actions tracked in its branch, expanded or not</span>
                      <span>A struck-through label has settled — nothing left to do — and sinks below its unfinished siblings. "Show completed" hides it entirely.</span>
                    </>
                  )}
                  <small>Use + and −, or select a parent node, to reveal and hide its upstream logic. Selecting a node also opens its evidence and assumptions.</small>
                </div>
              </details>
            </section>
          </main>
        )}
      </div>

      <DetailsPanel
        entity={selected}
        model={model}
        index={index}
        tracking={tracking}
        alignment={alignment}
        alignmentSuggestions={selectedSuggestions}
        alignmentDecisions={alignmentDecisions}
        onSetAlignmentStatus={setAlignmentStatus}
        onSetAlignmentNote={setAlignmentNote}
        onClose={() => setSelectedId(null)}
      />
    </div>
  );
}
