"""Canonical one-standing Mermaid views rendered with the pinned local CLI."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import uuid

from .service import helper_modules
from .store import atomic_write


class Renderer:
    def __init__(self, config):
        self.config = config

    async def render(self, state_path, tree_name, standing, invocation):
        helper, view = helper_modules(str(self.config.scripts))
        state = helper.load(Path(state_path))
        helper.validate(state)
        tree = deepcopy(state["trees"][tree_name])
        standing = standing or view.default_standing(tree)
        if standing not in view.STANDINGS:
            raise ValueError("Standing must be accepted, proposed or disputed.")
        view.PEOPLE.update(state["participants"], assistant="assistant")
        for node in tree["nodes"]:
            # The canonical label already retains tree, kind, full qualifications
            # and standing. Add the stable ID for an attachment's provenance.
            node["text"] = node["id"] + "\n" + node["text"]
        nodes, shown, context, links = view.select(tree, standing)
        if not shown:
            return None, f"No {standing} nodes. " + view.not_shown(tree, standing)
        description = view.heading(tree_name, standing, shown, links, context) + "\n" + view.not_shown(tree, standing)
        fallback = view.text_outline(tree_name, tree, standing)
        artifacts = self.config.runtime / "artifacts"
        artifacts.mkdir(parents=True, exist_ok=True)
        stem = artifacts / uuid.uuid4().hex
        text_path = stem.with_suffix(".txt")
        atomic_write(text_path, description + "\n" + fallback)
        cli = self.config.repo / "apps/discord/node_modules/.bin/mmdc"
        if not cli.exists():
            return text_path, description + "\nPNG renderer unavailable; attached the canonical text view."
        if len(shown) + len(context) > 150:
            return text_path, description + "\nTree exceeds the PNG size limit; attached its complete text view."
        source, _, _, common, _ = view.mermaid(tree_name, tree, standing)
        if common:
            description += "\nEach arrow reads: " + common
        description += "\nLinks: " + (", ".join(link["id"] for link in links) or "none")
        source = "---\ntitle: " + json.dumps(description.split("\n")[0] + (" · arrows: " + common if common else "")) + "\n---\n" + source
        atomic_write(stem.with_suffix(".mmd"), source)
        atomic_write(stem.with_suffix(".json"), json.dumps({
            "htmlLabels": False, "securityLevel": "strict", "theme": "neutral",
            "flowchart": {"htmlLabels": False, "wrappingWidth": 360},
        }))
        png = stem.with_suffix(".png")
        process = await asyncio.create_subprocess_exec(
            str(cli), "-i", str(stem.with_suffix(".mmd")), "-o", str(png),
            "-c", str(stem.with_suffix(".json")), "-b", "white", "-w", "1600", "-s", "1.5",
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        try:
            code = await asyncio.wait_for(process.wait(), timeout=45)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            process.kill()
            await process.wait()
            if asyncio.current_task().cancelling():
                raise
            return text_path, description + "\nPNG rendering timed out; attached the canonical text view."
        if code or not png.exists() or png.stat().st_size > 8_000_000:
            return text_path, description + "\nPNG rendering failed or exceeded 8 MB; attached the canonical text view."
        return png, description
