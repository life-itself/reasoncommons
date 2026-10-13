#!/usr/bin/env python3
"""Render each Mermaid block in a Markdown file to a standalone SVG, for places that
show images but not Mermaid, such as pull request descriptions shown as <img>.

    python3 scripts/mermaid-svg.py blog/post.md blog/images/first.svg blog/images/second.svg

One output path per ```mermaid block, in order. Labels are SVG text rather than HTML,
and the image gets a white ground and an intrinsic size, so it reads the same in an
<img> tag, in dark mode and opened on its own. Needs Google Chrome, and network access
to load Mermaid from jsdelivr. Don't name a classDef `root`: Mermaid's own top-level
group has that class, so the style would paint every edge.
"""

import html
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs"
CONFIG = {"startOnLoad": False, "theme": "neutral", "securityLevel": "strict", "fontFamily": "Arial, Helvetica, sans-serif",
          "themeVariables": {"edgeLabelBackground": "#ffffff"}, "flowchart": {"htmlLabels": False, "wrappingWidth": 230, "curve": "basis"}}


def page(blocks):
    sources = "".join(f'<pre id="d{i}">{html.escape(block)}</pre>' for i, block in enumerate(blocks))
    return f"""<!doctype html><meta charset="utf-8"><body>{sources}<script type="module">
import mermaid from "{MERMAID}";
mermaid.initialize({json.dumps(CONFIG)});
for (let i = 0; i < {len(blocks)}; i++) {{
  const out = document.createElement("textarea");
  try {{ out.id = "out" + i; out.textContent = (await mermaid.render("svg" + i, document.getElementById("d" + i).textContent)).svg; }}
  catch (error) {{ out.id = "err" + i; out.textContent = String(error); }}
  document.body.appendChild(out);
}}
</script>"""


def standalone(svg):
    svg = svg.replace("&nbsp;", "&#160;").replace("<br>", "<br/>")
    _, _, width, height = (float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split())
    svg = re.sub(r'<svg ([^>]*?)width="100%"', rf'<svg \1width="{width:g}" height="{height:g}"', svg, count=1)
    svg = re.sub(r'style="max-width: [^"]*"', 'style="background-color: #ffffff"', svg, count=1)
    ET.fromstring(svg)  # fail here, not in someone's browser, if it isn't well-formed
    return svg + "\n"


def main(markdown, *outputs):
    blocks = re.findall(r"^```mermaid\n(.*?)^```", Path(markdown).read_text(), re.S | re.M)
    if len(blocks) != len(outputs):
        sys.exit(f"{markdown} has {len(blocks)} Mermaid blocks; give one output path for each.")
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp, "render.html")
        source.write_text(page(blocks))
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=20000", "--dump-dom", source.as_uri()],
                             capture_output=True, text=True, check=True).stdout
    for i, output in enumerate(outputs):
        found = re.search(rf'<textarea id="(out|err){i}">(.*?)</textarea>', dom, re.S)
        if not found or found.group(1) == "err":
            sys.exit(f"Block {i + 1} did not render: {html.unescape(found.group(2)) if found else 'no output'}")
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(standalone(html.unescape(found.group(2))))
        print(output)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
