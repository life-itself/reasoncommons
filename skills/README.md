# Reason Commons skills

AI skills that turn documents, plans and notes into a Reason Commons reasoning project — goals, current reality, conflicts, and the actions that follow — using the Logical Thinking Process (LTP). They work in Claude Code, Codex and any other agent that supports `SKILL.md` skills.

## Start here

Install the skills once, then paste a prompt from [Try it](#try-it).

```sh
npx skills add life-itself/reasoncommons
```

That lists the skills in this repo and asks which agents to install them into (Claude Code, Codex, Cursor and others). Useful variants:

```sh
npx skills add life-itself/reasoncommons --list                     # see what is available, install nothing
npx skills add life-itself/reasoncommons -s ltp-project             # one skill only
npx skills add life-itself/reasoncommons -s ltp-project -a claude-code -g   # one skill, one agent, for every project
```

Don't want to install anything? Print a skill as a ready-to-paste prompt, or hand your agent the raw file:

```sh
npx skills use life-itself/reasoncommons@ltp-project
```

```text
https://reasoncommons.com/skills/ltp-project/SKILL.md
```

Any page on the site returns its raw Markdown if you add `.md` to the path, so that URL is the skill file itself — paste it into a chat and say "follow this skill". The skill's `references/` folder lives beside it, and an installed copy carries it along, so prefer installing.

## The skills

| Skill | What it does | Use it when |
|-------|--------------|-------------|
| [`ltp-project`](ltp-project/SKILL.md) | Reads a document, repository, plan, issue export or set of notes and writes a candidate `*.ltp.yaml` — the file the Reason Commons app imports — plus a report naming every judgment call it made | You have source material and want a first-draft reasoning model out of it |
| [`ltp-visualize`](ltp-visualize/SKILL.md) | Turns a `*.ltp.yaml` into a standalone HTML dashboard and opens it in your browser | You have a project file and want to see the trees |
| [`scrollable-explainer`](scrollable-explainer/SKILL.md) | Principles and patterns for writing scroll-driven visual explainers, with a teardown of a ProPublica piece as the worked case | You are drafting in [`explainers/`](../explainers/) — contributors only, you can skip this one |

The first two are the working pair: `ltp-project` makes the file, `ltp-visualize` shows it.

### `ltp-visualize` needs a clone of this repo

`ltp-project` works anywhere it is installed. `ltp-visualize` draws with the dashboard that lives in this repository, so `npx skills add` alone is not enough — run it from inside a clone, with PyYAML available:

```sh
git clone https://github.com/life-itself/reasoncommons.git
cd reasoncommons
python3 -m pip install pyyaml
```

Then open your agent in that folder (`claude` or `codex`) and use the visualize prompt below; it picks up the skill from the clone, so no `npx skills add` is needed there. Give it the path to your `.ltp.yaml` — it can be anywhere on your machine. It writes `<project-name>.dashboard-preview.html` beside your file and opens it in your browser.

## Try it

Paste into your agent after installing. Swap the bracketed part for your own material.

**Turn a document into a project file**

```text
Use the ltp-project skill on [path/to/document.pdf]. Write the candidate .ltp.yaml and the report, then summarise the judgment calls I should check first.
```

**Turn a repository's plans and issues into one**

```text
Use the ltp-project skill on this repository. Read the README, plans and docs, treat each planned task as a candidate transition action, and list any task you couldn't trace back to a goal.
```

**Turn meeting notes into one**

```text
Use the ltp-project skill on these notes: [paste notes, or a path]. I'm most interested in the undesirable effects people raised and what they think is causing them. Don't invent links the notes don't state.
```

**See what you made** (run from inside a clone of this repo — [see above](#ltp-visualize-needs-a-clone-of-this-repo))

```text
Use the ltp-visualize skill on [/full/path/to/project.ltp.yaml] and open the result in my browser.
```

**Check and repair a file**

```text
Use the ltp-project skill to check [path/to/project.ltp.yaml] by hand against the format and vocabulary, and fix anything the importer would likely refuse. Don't delete real content to make it look valid.
```

**Just want to see the format first?** The full worked example, across all six trees, is at [`ltp-project/references/example-project.ltp.yaml`](ltp-project/references/example-project.ltp.yaml). Ask your agent to read it and explain it before you start.

## What to expect

- **Every run produces two files**: the `.ltp.yaml` and a `.report.md`. Read the report first — it lists every place the skill had to guess, and what it left out because the source didn't say it plainly.
- **It is conservative on purpose.** It only writes a cause-and-effect link when a single sentence in your source states it without hedging. Expect a sparser tree than you'd draw by hand; that is the skill declining to make things up. Add the links you believe, yourself.
- **Nothing is ratified.** The output is a candidate for a person to review, not a finished model.
- **The file is not machine-validated.** `ltp-project` checks its own output by hand against the format and says so in the report. To find out whether the app would accept it, attach it in the Reason Commons app; the import reports anything it refuses. (A standalone validator is a known gap — see the TODO in `ltp-project/SKILL.md`.)

## For maintainers

- `ltp-project/` mirrors the canonical skill in `Promise-Foundation/reason-commons` (`.claude/skills/ltp-project/`). Edit it there, copy the directory here, and `diff -r` the two before editing either. **Currently diverged**: the `check:import` validation step was removed here (TODO in `ltp-project/SKILL.md`), so the change must be ported upstream before the next copy-over, or it will be overwritten.
- Skills live here, top level, so they work outside Claude Code. To use them while working in this repo, link them into the agent's discovery directory:
  - Claude Code (`.claude/` is gitignored): `mkdir -p .claude/skills && ln -s ../../skills/ltp-project .claude/skills/ltp-project` — likewise `ltp-visualize` and `scrollable-explainer`.
  - Codex: `.agents/skills/ltp-project` and `.agents/skills/ltp-visualize` are already tracked symlinks, so invoke them with `$ltp-project` and `$ltp-visualize`. Restart Codex if they don't appear in the Skills sidebar.
- Retired: `tree-gen`, `annotation-mapping`, `contribution-proposals`, `goal-alignment` and `project-ltp` (its `ltp-model.yaml` format can't be imported into Reason Commons; `ltp-project` replaces it). They remain in git history.
