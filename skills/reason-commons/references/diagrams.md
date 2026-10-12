# In-conversation diagrams

The change-status diagram and small view diagrams are written once as a Mermaid `flowchart`, then shown in whatever form the host can display. The topology rules in `SKILL.md` apply in every form: same nodes, same links, same joint conditions, no invented connections. A view diagram shows one standing at a time, as `SKILL.md` describes, with the view heading in place of the change label; endpoints of another standing drawn only for context use the `context` class and keep their marker.

## Choose the form

1. **Inline widget** — when the host has a tool that renders HTML in the conversation (in the Claude apps, `show_widget` from the visualize tools; load its guidance first if the tool asks for that). Render the Mermaid source with mermaid.js, as below. This is the preferred form.
2. **Fenced Mermaid block** — when there is no widget tool but the surface is known to render ```` ```mermaid ```` blocks (for example a GitHub or Flowershow page). A Claude Code or Codex chat does not render them; do not assume it does.
3. **ASCII** — in a terminal, any other plain-text surface, when unsure, or when the widget fails to render. Use the ASCII form below.

In voice, follow the voice rules in `SKILL.md` and do not describe the diagram markup.

## Mermaid conventions

- `flowchart LR` for short chains; `flowchart TB` when the fragment is deeper than it is wide.
- One node per statement: `id["[P] Concise claim"]`. Keep the `[P]`, `[A]`, `[D]` markers in the label so standing never depends on colour alone. Mark a revised node `[P] (revised)`.
- Links: `-->` accepted, `-.->` proposed, `-. disputed .->` disputed.
- Joint causes: route each cause into a small `AND` junction, `j1(("AND"))`, then one arrow from the junction to the effect. Never draw separate arrows that would imply each cause is sufficient on its own.
- Disconnected proposals stay disconnected; separate chains may each sit in their own `subgraph`.
- Muted neighbouring context uses the `context` class.
- Use node IDs from the YAML when they are valid Mermaid identifiers; otherwise short letters. Write `#quot;` for a double quote inside a label.

```text
flowchart LR
  diet["[P] I have a poor diet"] -.-> energy["[P] I have low energy"]
  sleep["[A] I sleep 5 hours"] --> j1(("AND"))
  energy -.-> j1
  j1 --> late["[D] I miss deadlines"]
  classDef proposed stroke-dasharray:4 3,stroke:#BA7517
  classDef accepted stroke:#1D9E75,stroke-width:2px
  classDef disputed stroke:#E24B4A,stroke-width:2px
  classDef context stroke-dasharray:2 2,opacity:0.6
  class diet,energy proposed
  class sleep accepted
  class late disputed
```

## Widget form

Write the status line in the response text, call the widget tool with the diagram only, then continue with the summary sentence and directions. Use a fresh render ID for each widget and replace `SOURCE` with the Mermaid source:

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

The widget loads mermaid.js from esm.sh, so it needs network access. If it fails to render, show the ASCII form instead in the same response.

### Pan and zoom for larger diagrams

Use the plain widget above for small fragments, which covers most change-status diagrams: it sizes itself to fit and reads at a glance. For a tree view, or any diagram of more than about ten nodes or too wide to read at chat width, use this pan-and-zoom frame instead. It opens fitted to the whole diagram. Dragging pans; the buttons, a pinch, or ⌘/Ctrl with the scroll wheel zoom. A plain scroll is left to the conversation so the diagram never traps it. Use the same heading line, initialisation and `SOURCE` substitution as the plain widget:

```html
<style>
#rcv{position:relative;height:380px;border:0.5px solid var(--border);border-radius:12px;overflow:hidden;cursor:grab;touch-action:none;background:var(--surface-1)}
#rcv.drag{cursor:grabbing}
#rcv svg{width:100%;height:100%;max-width:none!important}
.rcb{position:absolute;top:8px;right:8px;display:flex;gap:4px}
.rcb button{width:30px;height:30px;border:0.5px solid var(--border-strong);border-radius:var(--radius);background:var(--surface-2);color:var(--text-primary);cursor:pointer;font-size:16px;line-height:1}
</style>
<h2 class="sr-only">Goal tree, proposed only, with pan and zoom</h2>
<p style="margin:0 0 8px;font-size:13px;color:var(--text-secondary)">GOAL — PROPOSED ONLY (12 nodes, 11 links) · drag to pan · pinch or ⌘/Ctrl+scroll to zoom</p>
<div id="rcv"><div id="rc" style="width:100%;height:100%"></div>
<div class="rcb"><button id="zin" aria-label="Zoom in"><i class="ti ti-plus" aria-hidden="true"></i></button><button id="zout" aria-label="Zoom out"><i class="ti ti-minus" aria-hidden="true"></i></button><button id="zfit" aria-label="Fit to view"><i class="ti ti-arrows-maximize" aria-hidden="true"></i></button></div></div>
<script type="module">
// import, theme detection and mermaid.initialize exactly as in the plain widget
const { svg } = await mermaid.render('rc-2', `SOURCE`);
const host = document.getElementById('rc'); host.innerHTML = svg;
const el = host.querySelector('svg'); el.removeAttribute('style'); el.setAttribute('width','100%'); el.setAttribute('height','100%');
const [fx,fy,fw,fh] = el.getAttribute('viewBox').split(/[\s,]+/).map(Number);
const pad = 16, fit = {x:fx-pad,y:fy-pad,w:fw+2*pad,h:fh+2*pad};
let v = {...fit};
const set = () => el.setAttribute('viewBox', `${v.x} ${v.y} ${v.w} ${v.h}`);
const scale = () => { const r = el.getBoundingClientRect(); return Math.max(v.w/r.width, v.h/r.height); };
const zoom = (f, cx, cy) => { const r = el.getBoundingClientRect(); const s = scale();
  const px = cx==null ? v.x+v.w/2 : v.x + (cx-r.left)*s - (s*r.width-v.w)/2;
  const py = cy==null ? v.y+v.h/2 : v.y + (cy-r.top)*s - (s*r.height-v.h)/2;
  const nw = Math.min(Math.max(v.w*f, fit.w/8), fit.w*4); const k = nw/v.w;
  v = {x:px-(px-v.x)*k, y:py-(py-v.y)*k, w:v.w*k, h:v.h*k}; set(); };
set();
const box = document.getElementById('rcv');
document.getElementById('zin').onclick = () => zoom(0.8);
document.getElementById('zout').onclick = () => zoom(1.25);
document.getElementById('zfit').onclick = () => { v = {...fit}; set(); };
box.addEventListener('wheel', e => { if (!(e.ctrlKey || e.metaKey)) return; e.preventDefault(); zoom(Math.exp(e.deltaY*0.01), e.clientX, e.clientY); }, {passive:false});
let last = null;
box.addEventListener('pointerdown', e => { if (e.target.closest('button')) return; last = [e.clientX,e.clientY]; box.setPointerCapture(e.pointerId); box.classList.add('drag'); });
box.addEventListener('pointermove', e => { if (!last) return; const s = scale(); v.x -= (e.clientX-last[0])*s; v.y -= (e.clientY-last[1])*s; last = [e.clientX,e.clientY]; set(); });
const end = () => { last = null; box.classList.remove('drag'); };
box.addEventListener('pointerup', end); box.addEventListener('pointercancel', end);
</script>
```

Keep the frame's height near 380px; a taller frame pushes the summary and directions out of view.

## ASCII form

```text
LAST CHANGE: PROPOSED   [P] proposed

+----------------------+       +----------------------+
| [P] I have a poor    | ----> | [P] I have low      |
| diet                 |       | energy               |
+----------------------+       +----------------------+
```

Keep ASCII diagrams ASCII-only. For joint causes, join the arrows at an `(AND)` node before the effect.
