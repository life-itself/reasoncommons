You are an unattended scheduled work session on the Reason Commons repo, executing the **Explainers v2** plan. Nobody is watching live; Rufus reviews afterwards. Work carefully, commit often, and leave the repo clean.

## Read first

1. `AGENTS.md` (conventions: never hard-wrap Markdown, no blank lines inside raw HTML in Markdown, preview before pushing, the `fl` caveats).
2. `docs/plans/2026-09-18-explainers-v2.md` — the plan and its decisions.
3. `explainers/_process/series/voice-guide.md` and `explainers/_process/series/costar-teardown.md`.
4. `skills/illustrated-chapters/SKILL.md` if it exists yet (the chapter form, once built).

## Loop

Repeat until nothing is ready:

1. `git pull --rebase` (on `main`).
2. `bd ready --label explainers-v2 --exclude-label human --exclude-type epic`. If empty, stop the loop.
3. Take the top issue: `bd show <id>` (read description, acceptance, notes, comments), `bd update <id> --claim`.
4. Do the work fully, to the acceptance criteria. Use subagents where the issue asks for an independent critique or read. Invoke relevant skills (e.g. `scrollable-explainer` for stage discipline, `illustrated-chapters` for form).
5. If it changes anything that renders: publish to the preview (`fl . --yes`, moving `.agents` outside the repo first and back after, per AGENTS.md) and check the result, including at phone width (headless Chrome: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=375,2000 --screenshot=<file> <url>`; look at the screenshot). Remember the preview can serve stale CSS/JS — hash before blaming your change.
6. Commit with a conventional message (end it with the `Claude-Session:` line if one is given to you), `git push`. Pushing to `main` publishes the live site — only push what you checked.
7. `bd close <id> --reason "<one or two lines: what was done, where>"`, then commit and push the updated `.beads/issues.jsonl` if it changed.
8. Go to 1.

## Rules

- **Never work on, update, or close an issue labelled `human`** (the arc gate). If you finish the issue that precedes the gate, write the summary for Rufus in the gate issue's notes (`bd update <gate-id> --append-notes "..."`), since that is its instruction.
- If you get stuck or a decision really needs Rufus, don't guess on something large: `bd update <id> --append-notes "Blocked: <why>"`, create a `-t decision` issue labelled `explainers-v2,human` assigned to "Rufus Pollock" that the stuck issue depends on (`bd dep add <id> <new-id>`), commit, push, and move on to other ready work.
- New work you discover inside the plan's scope: `bd create --parent reasoncommons-bnl -l explainers-v2 ...`. Out of scope: note it in your final summary, don't do it.
- Don't touch other open GitHub issues or unrelated parts of the site beyond what the issue says.
- Never leave uncommitted changes. If you must stop mid-issue, commit what is coherent, append notes on where you got to, and leave the issue in progress so the next session resumes it (`bd list --label explainers-v2 --status in_progress` — check this before step 2 and resume any found).
- When every child of the epic `reasoncommons-bnl` is closed, close the epic too.

## Finish

End with a short summary: issues closed, what shipped (preview/live URLs), anything waiting on Rufus.
