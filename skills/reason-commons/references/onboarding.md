# First-session introduction

A participant opening Reason Commons for the first time needs to know what the skill is for and what each type of message asks of them, especially before their first **Feedback request**. Show this introduction once per participant per checkout, before the feedback queue and the ordinary agenda.

## When to show it

Once the driver is known, run `python3 <skill-directory>/scripts/onboarding.py <state.yaml> --participant <driver>`. If it prints an **Introduction**, show it unchanged as the first substantive response, then continue to the driver's feedback queue. It prints nothing for someone who has already seen it in this checkout. When someone asks to see the introduction again, run it with `--again`.

The script records who has seen it only in the state file's local, gitignored folder (`.reason-commons/onboarding.json` for `reason-commons.yaml`), so it never changes the shared reasoning and each new checkout shows it once. It reads whether feedback sharing is configured but never configures it: a participant turns sharing on by running the printed command with their own words of authorisation.

## Introduction

Edit the wording here; the script fills the placeholders. Keep it short: it stands between a busy person and their first useful step.

```markdown
**Type: Introduction**

Welcome, {name}. This is Reason Commons for **{project}**: a shared record of the reasoning behind the work, such as goals, problems, proposed changes and what we expect them to do.{others} I help you add to it, question it and act on it. Nothing you say counts as agreed until you say so.

| When you see | It asks of you |
| --- | --- |
| **Feedback request** | Your experience of a change: did the expected benefit happen, and did the possible harm? Answer either or both, or say "not yet". |
| **Change proposal** | A typed acceptance before any project file changes, or the revisions you want. |
| **Next step** | Nothing. One suggestion you can take, change or ignore. |
| **Change result**, **Answer**, **Tree view**, **Capture result** | Nothing. Information about what changed or what is recorded. |

**Feedback:** each request shows the expected benefit and the possible harm side by side, as they were written before the change. Silence is never taken as an answer, and answering doesn't mean you agree with the reasoning.

**Sharing:** {sharing}

**Waiting for you:** {waiting}

Ask to see this introduction again at any time.
```
