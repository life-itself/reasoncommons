# Beads and conversational reasoning

The Rufus–David collaboration resumes from **`reasoncommons-a4l` — START HERE: continue the Rufus–David collaboration tree**. That bead points to the current reasoning work and records the next useful question. Use the existing handoff rather than creating a new START HERE bead each session.

## What lives where

| State | Owner |
| --- | --- |
| Where to resume, work priority, ownership, task status and implementation dependencies | Beads |
| Claims, links, contributions, explicit endorsement, challenges and unfinished reasoning | [Conversational YAML](../ltp/rufus-david-collab/reason-commons.yaml) |
| Original app interchange model and conversion evidence | [Original model](../ltp/rufus-david-collab/rufus-david-collab.ltp.yaml), [SCQH](../ltp/rufus-david-collab/scqh.md) and [report](../ltp/rufus-david-collab/rufus-david-collab.report.md) |
| Friction encountered during use | [Friction log](../ltp/rufus-david-collab/friction-log.md), with build work tracked in separate beads |

The conversational YAML is the working reasoning state for these sessions. The original `.ltp.yaml` remains the conversion baseline; the two formats are not automatically synchronized. Read older documents as context, not as instructions to overwrite newer conversational state. A requested app export is a separate conversion step using `ltp-project`. Funder assessments and application drafts retain their existing private locations.

## Resume

1. Read `bd --sandbox show reasoncommons-a4l`, then the current work bead named there. Follow an explicit user change of focus when supplied.
2. Read [the reason-commons skill](../skills/reason-commons/SKILL.md) and the working YAML. Use its `work_tracking` pointers and the linked backlog entries to locate the relevant reasoning by stable node/link ID.
3. Read the relevant source context, unresolved challenges and friction before proposing changes. The driver is the current operator; do not assume that a prior participant's endorsement includes the driver.
4. Work through one useful question at a time. Selecting a work bead does not claim it or change its status automatically. Preserve existing owners and human gates.

The initial integration resumes `reasoncommons-5lo` (review drafted reasoning with David). `reasoncommons-i2b` holds remaining proposed additions. Both remain open; integrating their references does not complete their work.

## References in the YAML

These optional, repository-specific fields are coordination metadata alongside the conversational version 1 schema:

```yaml
work_tracking:
  system: beads
  handoff: reasoncommons-a4l
  current: reasoncommons-5lo
```

Each relevant backlog entry may have a `beads` list of existing issue IDs. Its `ref` still names a node or link in that tree; `work` still describes the reasoning left to do. Several entries can share a work bead. Leave other backlog entries unlinked until there is a reason to schedule them; do not create a bead for every node or arrow. The handoff owns the current work selection; `work_tracking.current` mirrors it for navigation. If they disagree, inspect the latest user direction and handoff before reconciling them.

The standard views helper validates reasoning and ignores these coordination fields. Check linked bead IDs with `bd show` when adding or changing them. Changing only these references does not create an accepted-history revision.

## Finish or hand off

1. Save the reasoning YAML atomically and run `python3 skills/reason-commons/scripts/update_views.py ltp/rufus-david-collab/reason-commons.yaml` as the skill requires. Keep generated `.reason-commons/` history and diagrams local.
2. Update the relevant work bead with what was addressed, what remains and the stable YAML IDs. Complete only work actually finished. A completed task does not make a statement true or accepted; an endorsed statement may still need further testing.
3. Refresh `reasoncommons-a4l` with the working file, current work bead, next question or step, and any blocker. Update `work_tracking.current` if the selection changed. Keep the handoff open for later sessions and avoid duplicate priority lists.
4. Record friction when encountered. Reuse or create separate beads for implementation work arising from the reasoning; handle those in separate sessions. Keep issues labelled `human` for Rufus to close.
5. Export a fresh local fallback with `bd --sandbox export -o .beads/issues.jsonl`. Auto-export is throttled, so use this explicit checkpoint after the last update. Exporting records does not push or synchronize the Dolt remote; use the team's normal sync workflow when authorized.

Use `bd --sandbox update <id> --body-file <file>` for multiline descriptions and `--append-notes` for short session outcomes. Preserve unrelated content and fields when updating a handoff.

## When local Beads is unavailable

The saved `.beads/issues.jsonl` contains full issue records, including the handoff. Read it as a fallback, stating that it is a saved export rather than live database state. Do not edit the export while a working Beads database owns the records.

For a fresh checkout with no database, back up the saved export before running `bd --sandbox init --skip-agents --skip-hooks --non-interactive --prefix reasoncommons`, which restores the configured remote. Check that the collaboration records are present. If they are missing, preview an import of the saved export with `bd --sandbox import <backup.jsonl> --dry-run --json`, then import the missing records without `--allow-stale`. Preserve any newer database rows. Never discard remote history to make initialization succeed.

The integration session on 2026-09-28 restored the configured remote and recovered the 29 missing issue records from the pre-existing export. This recovered issue records, not any historical Dolt commits absent from the remote.
