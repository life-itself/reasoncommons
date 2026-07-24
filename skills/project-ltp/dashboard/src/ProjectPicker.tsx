import type { AlignmentSummary, ProjectSummary } from "./projects";

interface ProjectPickerProps {
  projects: ProjectSummary[];
  alignments?: AlignmentSummary[];
  onOpen: (project: ProjectSummary) => void;
  loadingSlug?: string | null;
  error?: string | null;
}

export function ProjectPicker({
  projects,
  alignments = [],
  onOpen,
  loadingSlug,
  error,
}: ProjectPickerProps) {
  return (
    <main className="overview project-picker">
      <section className="overview-hero">
        <div>
          <span className="eyebrow">Project LTP</span>
          <h1>Choose a project</h1>
          <p>
            Each project is an evidence-backed Logical Thinking Process model. Open one to
            explore its goal, reality, conflict, and action trees.
          </p>
        </div>
      </section>

      {error && (
        <div className="empty-panel" role="alert">
          <span aria-hidden="true">!</span>
          <div>
            <strong>That could not be opened.</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      <section className="project-grid" aria-label="Projects">
        {projects.map((project) => {
          const isLoading = loadingSlug === project.slug;
          const alignment = alignments.find((a) => a.source_project === project.slug);
          return (
            <button
              type="button"
              key={project.slug}
              className="project-card"
              onClick={() => onOpen(project)}
              disabled={Boolean(loadingSlug)}
              aria-busy={isLoading}
            >
              {project.analysis_mode && <span className="project-card__mode">{project.analysis_mode}</span>}
              <strong>{project.name}</strong>
              {project.blurb && <p>{project.blurb}</p>}
              {alignment && (
                <span className="project-card__alignment-tag">◆ Has alignment suggestions</span>
              )}
              <span className="project-card__cta">{isLoading ? "Opening…" : "Open"} <span aria-hidden="true">→</span></span>
            </button>
          );
        })}
      </section>
    </main>
  );
}
