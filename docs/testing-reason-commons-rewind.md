# Test reasoning rewind and approval recovery

This is the recovery test for the alternative to [PR #56](https://github.com/life-itself/reasoncommons/pull/56), following the typed acceptance of `change-rewind-with-tree-trace-2026-10-14` revision 1. It distinguishes helper evidence from native Claude Code checkpoint behavior. Use the remote-work gold fixture in [claim-tree-annotation.md](../claim-tree-annotation.md) before the collaboration's real state.

## Automated recovery checks

From this checkout, run:

```sh
python3 -m unittest discover -s skills/reason-commons/tests
```

The recovery cases in `test_update_views.py` use the fixture's 13% productivity gain, call-centre population and solo-task scope. They verify accepted states A → B → restored A produce three immutable revisions and refreshed views; proposed-work restoration creates no accepted revision; receipt-only approvals survive between snapshots and without any accepted snapshot; receipt recovery keeps restored reasoning unchanged; exact replies and missing participant identities are recovered; altered receipts, conflicting saved originals and malformed ledger records stop generation; legacy snapshot recovery and a missing ledger have explicitly different limits; custom output directories work; and the recovery CLI changes no files.

These tests simulate restoring the YAML bytes. They do not test Claude Code's native checkpoint capture, menu, file restoration or whether an agent reliably follows the recovery instructions. Record those results separately below.

## Native Claude Code check

Use a fresh Claude Code session with this checkout's skill. Keep all fixture files in a new directory under `/private/tmp`; use regular files, not symlinked or hard-linked working state. Keep the generated `.reason-commons/` directory with the fixture throughout restoration. Select a checkpoint created by a prompt that started a turn; a mid-turn message may have no code restoration checkpoint. Checkpoint retention and current-session tracking are host conditions, not guarantees made by this helper. See [Claude Code checkpointing](https://code.claude.com/docs/en/checkpointing).

1. Start with accepted remote-work observations retaining the study's scope. Ask the skill to save them with Edit/Write and run its views helper. Keep the first snapshot and current diagram available for comparison.
2. In a subsequent turn, revise an accepted observation and explicitly endorse the revision for this isolated test. Confirm the working YAML, a second accepted snapshot and current diagram reflect it.
3. Use `/rewind` and select **Restore code and conversation** at the checkpoint before that revision. Confirm that this option is available and the actual working YAML returns to its earlier contents. Conversation-only restoration intentionally leaves files unchanged and is not this test.
4. Before continuing reasoning, have the skill re-read the restored YAML and run the helper. Verify a third accepted revision records the reversal, the first two snapshots remain byte-for-byte intact, and the current view displays the restored statement. The latest-change view may show the undone wording as previous content; it must not present it as current.
5. Repeat with a proposed-only change. Restoring it must not create a new accepted-reasoning revision or silently endorse the proposal.

Record native evidence: Claude Code version, checkpoint selection, whether Edit/Write captured the YAML, restoration result, regeneration result and snapshot comparison. If native restoration is unavailable, report that limit rather than replacing it with the helper simulation or a screenshot of an untested menu.

## Approval recorded between snapshots

Use an isolated project change with a displayed, bounded proposal and an actual subsequent typed acceptance from the test participant. Never invent consent for a real implementation. An automated fixture may use its clearly labeled simulated test receipt.

1. Record the receipt with exact reply, original timestamp and scope, then run the helper without changing accepted reasoning. Confirm the local `acceptances/` ledger contains it and no new accepted snapshot is created.
2. Restore the working YAML from before the receipt. A normal helper run must stop and request receipt recovery before generating another snapshot or view.
3. Run the same helper with `--recover-acceptances`, keeping the same `--output-dir` if one was configured. Inspect the exact original receipt and any missing participant identities. This command must change neither working state nor local artifacts.
4. Recover only those receipt and participant fields through Edit/Write, then rerun the helper. Verify the restored reasoning and its standing remain unchanged, while the original approval remains available for implementation that already happened. Historical approval does not authorize extending its scope or repeating the implementation.
5. Alter the working copy's receipt scope and repeat the check: recovery must supply the saved original, not endorse the widened scope. Retain both the receipt ledger and accepted history; if the ledger is lost, snapshots cannot recover approvals that were never included in them.

## Report the result against the trees

Current Reality distinguishes untracked YAML, stale views and lost receipts. Future Reality proposes tracked saves, view regeneration and immutable approval recovery operating together. Prerequisite records that checkpoints and recovery artifacts must be available. Transition separates implementation from evidence. The existing Goal remains real people using the tool; persistence checks alone do not establish confidence, usability or adoption.

Keep native-host verification and real-use review open in the reasoning backlog until their evidence exists. Opening the alternative PR, passing tests or completing the implementation bead does not accept the proposed nodes or links.
