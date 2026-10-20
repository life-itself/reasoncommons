from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from reasoncommons_discord.config import Config
from reasoncommons_discord.diagrams import Renderer

REPO = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).parent / "fixtures/remote-work.yaml"


class DiagramTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "reason-commons.yaml"
        self.state.write_bytes(FIXTURE.read_bytes())
        self.config = Config(REPO, self.state, self.root / "runtime", 10, frozenset({20}), {"100": "alice"})

    def tearDown(self):
        self.temp.cleanup()

    async def test_missing_renderer_gives_complete_text_without_changing_state(self):
        before = self.state.read_bytes()
        exists = Path.exists
        with patch("reasoncommons_discord.diagrams.Path.exists", lambda p: False if p.name == "mmdc" else exists(p)):
            path, description = await Renderer(self.config).render(self.state, "current_reality", "proposed", "one")
        self.assertEqual(path.suffix, ".txt")
        text = path.read_text()
        self.assertIn("AND", text)
        self.assertIn("under its studied conditions", text)
        self.assertIn("r-productivity-gain", text)
        self.assertIn("PROPOSED", description)
        self.assertEqual(before, self.state.read_bytes())

    async def test_empty_standing_returns_explanation(self):
        path, description = await Renderer(self.config).render(self.state, "current_reality", "disputed", "one")
        self.assertIsNone(path)
        self.assertIn("No disputed", description)

    async def test_mermaid_source_preserves_ids_and_joint_conditions(self):
        class Process:
            returncode = 1
            async def wait(self):
                return 1
        async def fake_process(*args, **kwargs):
            return Process()
        exists = Path.exists
        with patch("reasoncommons_discord.diagrams.asyncio.create_subprocess_exec", fake_process), patch(
                "reasoncommons_discord.diagrams.Path.exists", lambda p: True if p.name == "mmdc" else exists(p)):
            await Renderer(self.config).render(self.state, "current_reality", "proposed", "one")
        source = next((self.config.runtime / "artifacts").glob("*.mmd")).read_text()
        self.assertIn('(("AND"))', source)
        self.assertIn("r-productivity-gain", source)
        self.assertIn("CURRENT REALITY", source)
        self.assertIn("PROPOSED ONLY", source)
        self.assertIn("[Proposed]<br/>Observation", source)
        self.assertIn("[Accepted]<br/>Observation", source)
        self.assertIn("jointly qualify", source)
