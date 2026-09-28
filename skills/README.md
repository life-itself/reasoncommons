# Reason Commons skills

AI skills for turning source material into Logical Thinking Process (LTP) trees and developing those trees with people. They work in Claude Code, Codex and other agents that support `SKILL.md` skills.

<div class="rc-cards rc-cards-2">
<a class="rc-card" href="#start-here"><span class="rc-card-title">1 · Install</span><p>One command puts the skills in your agent.</p></a>
<a class="rc-card" href="#start-a-reasoning-conversation"><span class="rc-card-title">2 · Think together</span><p>Build and challenge a tree through conversation.</p></a>
<a class="rc-card" href="#turn-existing-material-into-a-project-file"><span class="rc-card-title">3 · Convert source material</span><p>Turn a document, repository or notes into an importable draft.</p></a>
<a class="rc-card" href="#send-this-to-a-colleague"><span class="rc-card-title">Pass it on</span><p>A short message to send a colleague.</p></a>
</div>

## Start here

Install the skills once:

```sh
npx skills add life-itself/reasoncommons
```

That lists the skills in this repository and asks which agents to install them into. To install just the conversational skill:

```sh
npx skills add life-itself/reasoncommons -s reason-commons
```

To install it for one agent in every project:

```sh
npx skills add life-itself/reasoncommons -s reason-commons -a claude-code -g
```

Replace `claude-code` with the agent you use. Run `npx skills add life-itself/reasoncommons --list` to see the available skills without installing them.

Don't want to install anything? Print a skill as a ready-to-paste prompt, or give your agent the raw file:

```sh
npx skills use life-itself/reasoncommons@reason-commons
```

```text
https://reasoncommons.com/skills/reason-commons/SKILL.md
```

An installed copy includes the skill's helper script and references, so installation is the best option.

## The skills

| Skill | What it does | Use it when |
|-------|--------------|-------------|
| [`reason-commons`](reason-commons/SKILL.md) | Helps people build and challenge LTP trees through conversation, while keeping attribution, unfinished reasoning, accepted history and diagrams | You want to think through a goal, problem, conflict, proposed change, obstacle or action with one person or a group |
| [`ltp-project`](ltp-project/SKILL.md) | Reads a document, repository, plan, issue export or notes and writes a candidate `*.ltp.yaml` that the Reason Commons app imports, plus a report naming every judgment call | You already have source material and want a first-draft app project from it |
| [`ltp-visualize`](ltp-visualize/SKILL.md) | Turns an app-compatible `*.ltp.yaml` into a standalone HTML dashboard and opens it in your browser | You have an `ltp-project` file and want to see its six trees |
| [`scrollable-explainer`](scrollable-explainer/SKILL.md) | Gives contributors principles and patterns for writing scroll-driven visual explainers | You are drafting in [`explainers/`](../explainers/) |

`reason-commons` is a candidate to replace `ltp-project` as the main way people create and develop reasoning. It starts from conversation, keeps work in progress visible, and records only explicitly accepted reasoning in its diagrams. It does not yet replace `ltp-project` for every job: its conversational YAML is independent of the Reason Commons app's import/export format. Use `ltp-project` when you need to extract a first draft from existing material or create a file for the app.

## Start a reasoning conversation

After installing, open your agent in the folder where you want the working state to live and paste a prompt like this:

```text
Use the reason-commons skill to help me think through why customer quotes are late. My name is Alice. Keep the working state in reason-commons.yaml.
```

You can begin with a goal, a problem, a conflict, a proposed change, an obstacle or a sequence of actions. You do not need to know the LTP tree names or prepare a document. The agent will capture useful statements, keep contributors' names attached to their ideas, and ask one focused question at a time.

To resume later, open the same folder and say:

```text
Use the reason-commons skill and resume from reason-commons.yaml. Show me the most useful unfinished reasoning to work on next.
```

For a group, name people as they contribute. If speaker labels come from a transcript or voice system, give those labels to the agent; the skill does not guess who spoke.

### What the backlog is for

The backlog is the reasoning that still needs attention: an observation that has not been connected or explained, a causal link that needs testing, an assumption to examine, or an objection to resolve. It is not a second task manager and it is not a list of every possible question. The agent keeps a small active subset, preserves the rest, and prefers working through existing reasoning before asking the group for more material.

Acceptance and backlog are separate. A person can accept a useful statement or connection while leaving a question about it in the backlog. Drawing an arrow does not by itself finish the reasoning.

### How accepted reasoning becomes diagrams

New statements and connections begin as proposals. They become accepted only when a person explicitly endorses the identified item or fragment; silence and moving on do not count. A substantive objection marks the item disputed until it is resolved.

After an accepted change, the helper validates the working YAML and saves one numbered snapshot of that turn's accepted state. It then updates two SVG diagrams for each affected tree:

- The full view shows all currently accepted statements and accepted connections.
- The latest-change view highlights what was added, changed or removed, with enough neighboring context to review the change.

Proposals, disputes and backlog-only edits stay in the working YAML but do not create a new accepted snapshot. The YAML is the source of truth; the diagrams are derived views. The skill normally runs the helper and links both diagrams when accepted reasoning changes. Python with PyYAML is required, plus Graphviz or the supported JavaScript renderer; see [`reason-commons/references/views.md`](reason-commons/references/views.md) for details.

## Turn existing material into a project file

Use `ltp-project` when your starting point is a document, repository, plan, issue export or meeting notes and you want a candidate file for the Reason Commons app.

```text
Use the ltp-project skill on [path/to/document.pdf]. Write the candidate .ltp.yaml and the report, then summarise the judgment calls I should check first.
```

For a repository:

```text
Use the ltp-project skill on this repository. Read the README, plans and docs, treat each planned task as a candidate transition action, and list any task you couldn't trace back to a goal.
```

Every run produces a `.ltp.yaml` and a `.report.md`. Read the report first: it lists guesses and omissions. The output is a candidate, not ratified reasoning, and is checked by hand rather than by a standalone validator. Attach it in the Reason Commons app to run the app's import checks.

### See the imported format as a dashboard

`ltp-visualize` draws with the dashboard in this repository, so it needs a clone and PyYAML:

```sh
git clone https://github.com/life-itself/reasoncommons.git
cd reasoncommons
python3 -m pip install pyyaml
```

Then open your agent in that folder and paste:

```text
Use the ltp-visualize skill on [/full/path/to/project.ltp.yaml] and open the result in my browser.
```

This visualization flow is for app-compatible files made by `ltp-project`; it is separate from the accepted/change diagrams maintained by `reason-commons`.

## Send this to a colleague

```text
Try the Reason Commons skill to think through a goal, problem, conflict or plan together. Install it with `npx skills add life-itself/reasoncommons -s reason-commons`, then ask your agent: "Use the reason-commons skill to help me think through [topic]. My name is [name]." The agent keeps unfinished reasoning in a backlog and turns explicitly accepted reasoning into full and latest-change diagrams. More: https://reasoncommons.com/skills
```

## For maintainers

- This repository is the canonical home of `ltp-project`; the copy in `Promise-Foundation/reason-commons` may be older and must not be copied over this one. A standalone validator remains a tracked gap.
- Skills live at top level so they work outside one agent runtime. Link the skills you use into `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. This repository tracks the Codex links for `reason-commons`, `ltp-project` and `ltp-visualize`.
- `tree-gen`, `annotation-mapping`, `contribution-proposals`, `goal-alignment` and `project-ltp` are retired and remain in Git history.
