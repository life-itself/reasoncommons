"""Local diagnostics, explicit task snapshot refresh, and opt-in live runner."""
import argparse
import json
import logging
import subprocess
import time

from .config import Config
from .store import atomic_write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "refresh-tasks", "run"])
    parser.add_argument("--sync-commands", action="store_true",
                        help="With run, register the commands in the configured guild.")
    args = parser.parse_args()
    try:
        config = Config.from_env()
        if args.command == "check":
            from .agent import package_version
            print(json.dumps({"state_valid": True, "skill_sha256": package_version(config.skill),
                              "task_snapshot_present": config.tasks.exists(),
                              "live_ready": bool(config.token and config.api_key and config.model and config.budget_usd > 0)}))
        elif args.command == "refresh-tasks":
            output = subprocess.run(["bd", "--sandbox", "list", "--all", "--limit", "0", "--json"],
                                    cwd=config.repo, capture_output=True, text=True, check=True, timeout=30)
            issues = json.loads(output.stdout)
            if not isinstance(issues, list):
                raise ValueError("Beads did not return an issue list.")
            # Snapshot is separate from canonical reasoning and never edits Beads.
            atomic_write(config.tasks, json.dumps({"source": "bd --sandbox list --all --limit 0 --json",
                         "refreshed_unix": time.time(), "issues": issues}, ensure_ascii=False))
            print(f"Refreshed {len(issues)} task records.")
        else:
            config.validate(live=True)
            from .agent import Agent
            from .bot import make_client
            from .diagrams import Renderer
            from .service import Service
            logging.basicConfig(level=logging.INFO)
            client = make_client(Service(config, Agent(config), Renderer(config)),
                                 sync_commands=args.sync_commands)
            client.run(config.token, log_handler=None)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
