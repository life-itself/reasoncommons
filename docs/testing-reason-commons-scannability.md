# Test the reason-commons conversation update

Use a fresh Claude Code session in the checkout on `codex/reason-commons-scannability`. Both the project skill and the installed user-level skill point to this checkout's `skills/reason-commons/`; an existing session may still hold the earlier instructions. This is a local test branch, not a published skill release.

## Start with the gold fixture

Start Claude Code from the repository root:

```sh
cd /Users/davidjoseph/github/reasoncommons
claude
```

Paste:

```text
/reason-commons Use the updated skill in this checkout at skills/reason-commons/SKILL.md. I’m Avery. Keep this test's working state in /private/tmp/reason-commons-scannability-test/reason-commons.yaml; create its parent directory if needed. The remote-work toy fixture in claim-tree-annotation.md reports a 13% productivity gain on solo call-handling tasks in a call-centre study. Help me decide whether that evidence applies to our team's creative and collaborative work.
```

The reply should lead with a useful inquiry and its reason, make any save and proposal status clear, and ask one focused question. The reported gain must retain its scope: it does not establish the same result for creative or collaborative work. A routine participant banner, empty status box, four-direction menu, or unnecessary diagram should not precede the useful reply. A diagram remains appropriate when it helps inspect relationships or you request one.

Try these follow-ups in ordinary language:

1. **Redirect:** “I’d rather examine what the study does not tell us first.” The conversation should follow your direction and preserve unfinished work.
2. **Capture only:** “Just capture this: most of our work involves several people revising ideas together.” The reply should confirm the save and standing without a menu or another question.
3. **View:** “Show the reasoning we have so far.” The reply should display the relevant tree with its standing clear; seeing it must not require acceptance. With no accepted items, it should default to proposed.
4. **Review:** If a coherent fragment has formed, endorse that clearly identified fragment in your own words. The reply should identify what was accepted for now and distinguish that from proof or completed testing.
5. **Challenge:** Object to one accepted connection. The challenge should be preserved, with the standing and dependent acceptance handled correctly.
6. **Stop:** “Pause here and wait for my next instruction.” The reply should stop inviting more reasoning.

At each step, check whether you can find the next action, what was saved, and what is uncertain or unaccepted by scanning. Note the response where that becomes difficult. The existing automated tests check persistence and rendering invariants; they do not establish that these new instructions improve usability.

## Then test the collaboration

After the toy check, open another fresh session from the same checkout and paste:

```text
/reason-commons Use the updated skill in this checkout at skills/reason-commons/SKILL.md. Resume the collaboration from ltp/rufus-david-collab/reason-commons.yaml and its existing Beads handoff. Recommend one useful next step, say what it rests on, and leave me free to redirect.
```

This second prompt uses the actual branch's collaboration state. It can save new contributions and review decisions, so treat it as a real reasoning session. A recommendation derived only from the handoff should say so; it must not be presented as an established system constraint. Newly captured claims remain proposed unless you explicitly endorse the identified reasoning.

If testing from another worktree, check that its project-level skill resolves to the updated branch; do not assume an older checkout has these instructions. Keep feedback with the branch or the existing skill UX bead, `reasoncommons-zz2`, so observations can be compared with the proposed effects in the reasoning state.
