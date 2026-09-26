---
name: ltp-visualize
description: Export a Reason Commons `.ltp.yaml` project as a standalone HTML dashboard preview and open it in the browser. Use after `ltp-project` when the user wants to see the generated trees.
---

# LTP visualization

Turn an `ltp-project` YAML output into a standalone HTML file that uses the Reason Commons dashboard interface, then open that file in the browser.

- Use the YAML path the user names or the active `ltp-project` task produced. If neither is explicit, the exporter picks the most recently modified non-fixture `*.ltp.yaml` in the repository.
- From the Reason Commons repository root, run `python3 skills/ltp-project/scripts/preview_dashboard.py [path/to/project.ltp.yaml] --export-html`. The HTML is written beside the YAML as `<project-name>.dashboard-preview.html` and opened automatically.
- To choose an output path, pass it after `--export-html`. Use `--no-open` only when the user asks for an export without opening it.
- The export is a static preview; it does not edit the YAML or import it into a Reason Commons space. Read `skills/ltp-project/references/preview.md` for what the dashboard format omits and which display defaults it adds.

Run the command when this skill is invoked. Report the generated HTML path and open it in the browser; do not stop after explaining the command.
