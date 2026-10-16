# In-conversation trees and diagrams

Trees and change fragments are shown by default as text trees read from the top node down. A Mermaid diagram is drawn only when someone asks for one. The topology rules in `SKILL.md` apply in every form: same nodes, same links, same joint conditions, no invented connections. Tree views are generated from the YAML by `scripts/render_view.py` rather than drawn by hand.

## Text trees

Each row is one statement. The word at the start of a row names its relation to the row above, so the tree reads top-down in plain words. A rail between two siblings carries the standing of the link to the sibling below it.

```text
▼ Rufus and David have not yet run a decision through the tool.  ✓R+D
├─ because        ◀ The tool is not finished.  ✓R
┊  └╌ partly because ◁ No one owns the release.
└╌ because        ∧ all of these together
   ├╌                □ Time is split across three projects.
   └╌                ◀ ↑ The tool is not finished.
```

| Mark | Meaning |
|------|---------|
| `◉ ◎` | goal, objective |
| `◆ ◇` | critical success factor, need, intermediate objective |
| `■ □` | necessary condition, observation, existing condition |
| `▼ ▽` | undesirable effect, obstacle |
| `◀ ◁` | cause |
| `★ ☆` | injection |
| `▶ ▷` | action, prerequisite (conflict-cloud action) |
| `▲ △` | desirable effect |
| `● ○` | predicted or expected effect |
| solid / hollow / `✕` | accepted / proposed / disputed statement |
| `│ ─` / `┊ ╌` / `┆ ┄` | accepted / proposed / disputed link |
| `∧ all of these together` | one link from joint conditions; its rows sit under it |
| `↑` | a statement already drawn in full under its first parent |
| `replaces` and struck text | a superseded statement |
| `✓R+D` | accepted by Rufus and David (initials) |
| `⚑ work` | open backlog work on the statement |
| `↗ addresses Reality` | a cross-tree trace; it is a reference, not a causal link |

The relation words are `needs` (necessary for), `because` (causes), `partly because` (contributes to), `supported by`, `challenged by`, `blocked by`, `cleared by` (overcomes), `then` (precedes), `expect` (produces, in the transition tree; `produced by` elsewhere), `replaces` (supersedes) and `conflicts with`. Highlighting a standing, or open work, dims every other row rather than removing it.

### Choose the form

1. **Inline widget** — when the host exposes an HTML rendering tool, pass `render_view.py`'s default output to it unchanged. It holds every tree, opens on the requested one, and has highlight, ID and zoom controls; clicking a statement shows its links, open work and where it was recorded.
2. **Chat reply or other Markdown** — `--format tree-markdown` prints a nested list in which every tree and statement name links to the graphical page opened at that tree or statement. Return it unchanged. Never wrap a tree in a code block: the links become dead text.
3. **Terminal** — `--format tree-text` prints the tree with OSC 8 hyperlinks when it is printing to the terminal itself. Output an agent captures is not a terminal, so links are off there unless `--links always` is given; ANSI colour follows the same rule and `NO_COLOR`.

```bash
# The widget: every tree, opened on one, optionally zoomed to a statement
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree current_reality [--highlight disputed] [--focus <node-id>]

# A linked nested list for a chat reply; writes the page beside the state
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree future_reality --format tree-markdown

# The terminal tree, wrapped to the terminal's width
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree transition --format tree-text

# Write the graphical page and list a link to each tree
python3 <skill-directory>/scripts/render_view.py <state.yaml> --page
```

The page is written to `.<state-stem>/trees.html` beside the state file, with the other generated files described in [views.md](views.md). A link to `trees.html#<tree>` opens that tree; `trees.html#<node-id>` opens the statement's tree zoomed to its path from the top node and its whole branch, centred on it. Pass `--page-url` when the page is published at another address, so the links point there. Links to local files open only where the reader can reach that file; in a cloud session they reach the container, not the reader's machine.

A change fragment whose updates are not saved yet, such as the tree updates in a change proposal, cannot be generated from the YAML. Write it by hand as the same nested list: the glyphs and relation words above, every new item marked with its standing, and existing statements linked to the page when it exists. Show only the changed items and the context needed to read them.

## Mermaid on request

When someone asks for a Mermaid diagram, choose from the actual conversation surface and its rendering guidance. Codex desktop and Codex CLI are different surfaces; likewise, Claude desktop or Claude Code in a desktop app may expose rendering that a plain terminal does not. A missing widget tool does not make a desktop conversation plain text.

1. **Native Mermaid** — in Codex desktop, return a normal fenced ```` ```mermaid ```` block in the response. Use this form on other surfaces with native Mermaid support too, including supporting Claude desktop surfaces, GitHub and Flowershow. No widget tool or HTML file is needed. For a full tree diagram, use `render_view.py --format markdown` to generate the complete response from the YAML.
2. **Inline widget** — when the host exposes an HTML rendering tool and native Mermaid is unavailable, or an interactive pan-and-zoom view is useful. In Claude apps this may be `show_widget`; follow the host's current rendering guidance rather than assuming the same tool exists in every desktop app. Render the Mermaid source with mermaid.js, as below.
3. **ASCII or text outline** — on a surface without diagram rendering, or after its supported rendering forms fail. If the surface's capabilities are unknown, say so and provide a readable fallback.

In voice, follow the voice rules in `SKILL.md` and do not describe the diagram markup.

### Mermaid conventions

- `flowchart LR` for short chains; `flowchart TB` when the fragment is deeper than it is wide.
- One node per statement, with explicit tree and kind above it: `id["[P] CURRENT REALITY · CAUSE<br/>Concise claim"]`. Read both from the YAML; do not infer them from the node ID. Keep the `[P]`, `[A]`, `[D]` markers in the label so standing never depends on colour alone. Mark a revised node `[P] (revised)`. In a mixed-tree diagram, each node names its own tree.
- Links: `-->` accepted, `-.->` proposed, `-. disputed .->` disputed.
- Joint causes: route each cause into a small `AND` junction, `j1(("AND"))`, then one arrow from the junction to the effect. Never draw separate arrows that would imply each cause is sufficient on its own.
- Disconnected proposals stay disconnected; separate chains may each sit in their own `subgraph`.
- Muted neighbouring context uses the `context` class.
- Use node IDs from the YAML when they are valid Mermaid identifiers; otherwise short letters. Write `#quot;` for a double quote inside a label.

```text
flowchart LR
  diet["[P] CURRENT REALITY · CAUSE<br/>I have a poor diet"] -.-> energy["[P] CURRENT REALITY · CAUSE<br/>I have low energy"]
  sleep["[A] CURRENT REALITY · CAUSE<br/>I sleep 5 hours"] --> j1(("AND"))
  energy -.-> j1
  j1 --> late["[D] CURRENT REALITY · UNDESIRABLE EFFECT<br/>I miss deadlines"]
  classDef proposed stroke-dasharray:4 3,stroke:#BA7517
  classDef accepted stroke:#1D9E75,stroke-width:2px
  classDef disputed stroke:#E24B4A,stroke-width:2px
  classDef context stroke-dasharray:2 2,opacity:0.6
  class diet,energy proposed
  class sleep accepted
  class late disputed
```

### Widget form

Give the opening answer or recommendation in response text, call the widget tool with the diagram only, then place any necessary save result and alternatives before the final question or selection prompt. Do not repeat the diagram's content as a second report. Use a fresh render ID for each widget and replace `SOURCE` with the Mermaid source:

```html
<h2 class="sr-only">Change-status diagram: LAST CHANGE PROPOSED</h2>
<p style="margin:0 0 8px;font-size:13px;color:var(--text-secondary)">LAST CHANGE: PROPOSED · [P] proposed · [A] accepted · [D] disputed</p>
<div id="rc"></div>
<script type="module">
import mermaid from 'https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs';
const mode = document.documentElement.dataset.mode;
const dark = mode ? mode === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
await document.fonts.ready;
mermaid.initialize({startOnLoad: false, theme: 'base', fontFamily: '"anthropic-sans", sans-serif',
  themeVariables: {darkMode: dark, fontSize: '13px', fontFamily: '"anthropic-sans", sans-serif',
    lineColor: dark ? '#9c9a92' : '#73726c', textColor: dark ? '#c2c0b6' : '#3d3d3a',
    primaryColor: dark ? '#2C2C2A' : '#F1EFE8', primaryBorderColor: dark ? '#888780' : '#5F5E5A'}});
const { svg } = await mermaid.render('rc-1', `SOURCE`);
document.getElementById('rc').innerHTML = svg;
</script>
```

The widget loads mermaid.js from esm.sh, so it needs network access. If it fails to render, use a native Mermaid block when the surface supports one; otherwise show the ASCII form in the same response.

#### Pan and zoom for larger diagrams

When an inline widget is available, a requested Mermaid tree diagram, and any requested diagram of more than about ten nodes or too wide to read at chat width, uses a pan-and-zoom frame instead of the plain widget. It opens fitted to the whole diagram. Dragging pans; the buttons, a pinch, or ⌘/Ctrl with the scroll wheel zoom. A plain scroll is left to the conversation so the diagram never traps it. The frame stays near 380px tall so the summary and directions remain in view. On a native Mermaid surface, return the generated Markdown and use the host's diagram inspection controls; lack of the widget frame is not a reason to switch to text.

Do not write the frame by hand. `scripts/render_view.py` prints it complete, ready to pass unchanged to the widget tool:

```bash
# A native Mermaid tree diagram: return this complete Markdown unchanged in the response
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree <tree> --standing <standing> --format markdown

# A Mermaid tree diagram in the frame: counts, topology, markers, context endpoints and the “Not shown” line all come from the YAML
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree current_reality --standing accepted --format widget

# A large change-status diagram you have written as Mermaid
python3 <skill-directory>/scripts/render_view.py --wrap --heading "LAST CHANGE: PROPOSED · [P] proposed · [A] accepted" < change.mmd
```

`--format mermaid` produces only the diagram source for callers that need to embed it. `--format markdown` includes the scope heading, relation key, fenced diagram and omitted-standing guidance, so native rendering retains the same context as a widget.

Mermaid tree diagrams show one standing at a time, with endpoints of other standings as marked context. On a plain-text surface, or after supported diagram rendering fails, `--format text` gives the same scope as an outline that lists every link once under its effect, with joint causes as `AND( … )` and unlinked nodes at the end. `--counts` prints the per-tree counts the view option in the menu needs.

### ASCII form

```text
LAST CHANGE: PROPOSED   [P] proposed

CURRENT REALITY
+----------------------+       +----------------------+
| [P] CAUSE            | ----> | [P] CAUSE            |
| I have a poor diet   |       | I have low energy    |
+----------------------+       +----------------------+
```

Keep ASCII diagrams ASCII-only. For joint causes, join the arrows at an `(AND)` node before the effect.
