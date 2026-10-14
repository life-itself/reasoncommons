# In-conversation diagrams

The change-status diagram is written once as a Mermaid `flowchart`, then shown in whatever form the host can display. The topology rules in `SKILL.md` apply in every form: same nodes, same links, same joint conditions, no invented connections. Tree views are generated from the YAML by `scripts/render_view.py` (see the pan-and-zoom section below) rather than drawn by hand; they follow the same conventions.

## Choose the form

Choose from the actual conversation surface and its rendering guidance. Codex desktop and Codex CLI are different surfaces; likewise, Claude desktop or Claude Code in a desktop app may expose rendering that a plain terminal does not. A missing widget tool does not make a desktop conversation plain text.

1. **Native Mermaid** — in Codex desktop, return a normal fenced ```` ```mermaid ```` block in the response. Use this form on other surfaces with native Mermaid support too, including supporting Claude desktop surfaces, GitHub and Flowershow. No widget tool or HTML file is needed. For a full tree view, use `render_view.py --format markdown` to generate the complete response from the YAML.
2. **Inline widget** — when the host exposes an HTML rendering tool and native Mermaid is unavailable, or an interactive pan-and-zoom view is useful. In Claude apps this may be `show_widget`; follow the host's current rendering guidance rather than assuming the same tool exists in every desktop app. Render the Mermaid source with mermaid.js, as below.
3. **ASCII or text outline** — on a surface without diagram rendering, or after its supported rendering forms fail. A terminal with Mermaid support can use the native form; use text when rendering is unavailable or disabled. If the surface's capabilities are unknown, say so and provide a readable fallback.

In voice, follow the voice rules in `SKILL.md` and do not describe the diagram markup.

## Mermaid conventions

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

## Widget form

Give the opening answer or recommendation in response text, call the widget tool with the diagram only, then place any necessary save result and alternatives before the final question or selection prompt. Do not repeat the diagram's content as a second report. A routine no-change turn needs no diagram; follow SKILL.md for when a diagram helps. Use a fresh render ID for each widget and replace `SOURCE` with the Mermaid source:

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

### Pan and zoom for tree views and larger diagrams

When an inline widget is available, every tree view, and any change-status diagram of more than about ten nodes or too wide to read at chat width, uses a pan-and-zoom frame instead of the plain widget. It opens fitted to the whole diagram. Dragging pans; the buttons, a pinch, or ⌘/Ctrl with the scroll wheel zoom. A plain scroll is left to the conversation so the diagram never traps it. The frame stays near 380px tall so the summary and directions remain in view. On a native Mermaid surface, return the generated Markdown and use the host's diagram inspection controls; lack of the widget frame is not a reason to switch to text.

Do not write the frame by hand. `scripts/render_view.py` prints it complete, ready to pass unchanged to the widget tool:

```bash
# A native Mermaid tree view: return this complete Markdown unchanged in the response
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree <tree> --standing <standing> --format markdown

# A tree view: counts, topology, markers, context endpoints and the “Not shown” line all come from the YAML
python3 <skill-directory>/scripts/render_view.py <state.yaml> --tree current_reality --standing accepted

# A large change-status diagram you have written as Mermaid
python3 <skill-directory>/scripts/render_view.py --wrap --heading "LAST CHANGE: PROPOSED · [P] proposed · [A] accepted" < change.mmd
```

`--format mermaid` produces only the diagram source for callers that need to embed it. `--format markdown` includes the scope heading, relation key, fenced diagram and omitted-standing guidance, so native rendering retains the same context as a widget.

On a plain-text surface, or after supported diagram rendering fails, use `--format text` for a view: an outline that lists every link once under its effect, with joint causes as `AND( … )` and unlinked nodes at the end. `--counts` prints the per-tree counts the view option in the menu needs.

## ASCII form

```text
LAST CHANGE: PROPOSED   [P] proposed

CURRENT REALITY
+----------------------+       +----------------------+
| [P] CAUSE            | ----> | [P] CAUSE            |
| I have a poor diet   |       | I have low energy    |
+----------------------+       +----------------------+
```

Keep ASCII diagrams ASCII-only. For joint causes, join the arrows at an `(AND)` node before the effect.
