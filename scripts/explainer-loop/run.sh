#!/bin/bash
# Scheduled work session for the Explainers v2 plan (docs/plans/2026-09-18-explainers-v2.md).
# Fired by launchd every 5.5h; see com.lifeitself.reasoncommons-explainers.plist.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin"

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LABEL=com.lifeitself.reasoncommons-explainers
EPIC=reasoncommons-bnl
LOCK="${TMPDIR:-/tmp}/reasoncommons-explainers.lock"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
cd "$REPO" || exit 1

if ! mkdir "$LOCK" 2>/dev/null; then
  pid=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then log "another session running (pid $pid); skipping"; exit 0; fi
  log "removing stale lock"; rm -rf "$LOCK"; mkdir "$LOCK" || exit 1
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT

if [ "$(bd show "$EPIC" --json 2>/dev/null | grep -o '"status": *"[a-z_]*"' | head -1 | grep -c closed)" = 1 ]; then
  log "epic $EPIC closed; unloading $LABEL"
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
  exit 0
fi

if [ -n "$(git status --porcelain)" ] && [ -z "$(git status --porcelain | grep -v ' \.beads/')" ]; then
  log "committing leftover beads export"; git add .beads && git commit -q -m "chore(beads): sync export" && git push -q
fi
if [ -n "$(git status --porcelain)" ]; then log "working tree dirty; skipping"; git status --short; exit 0; fi
git pull --rebase --quiet || { log "git pull failed; skipping"; exit 0; }

ready=$(bd ready --label explainers-v2 --exclude-label human --exclude-type epic --json --brief 2>/dev/null | grep -c '"id"')
inprog=$(bd list --label explainers-v2 --status in_progress --json 2>/dev/null | grep -c '"id"')
if [ "$ready" = 0 ] && [ "$inprog" = 0 ]; then
  log "nothing ready (waiting on: $(bd list --label human --status open --json 2>/dev/null | grep -o '"title": *"[^"]*"' | head -3 | tr '\n' ' '))"
  exit 0
fi

log "starting session: $ready ready, $inprog in progress"
[ -n "${DRY_RUN:-}" ] && { log "DRY_RUN set; not launching claude"; exit 0; }
notify() { osascript -e "display notification \"$1\" with title \"Reason Commons explainers\"" 2>/dev/null; }

# launchd can't refresh the interactive OAuth login, so use a long-lived token
# from `claude setup-token`, kept outside the repo.
TOKEN_FILE="$HOME/.config/reasoncommons-explainers/oauth-token"
if [ -r "$TOKEN_FILE" ]; then
  export CLAUDE_CODE_OAUTH_TOKEN="$(tr -d '[:space:]' < "$TOKEN_FILE")"
else
  log "no token at $TOKEN_FILE; trying the interactive login"
fi

out=$(mktemp)
claude -p "$(cat scripts/explainer-loop/session-prompt.md)" \
  --model opus \
  --effort high \
  --dangerously-skip-permissions 2>&1 | tee "$out"
status=${PIPESTATUS[0]}
log "session ended (exit $status)"
if grep -qi "authenticate\|OAuth\|login" "$out" && [ "$status" != 0 ]; then
  notify "Session failed to authenticate — run claude setup-token (see docs/plans/2026-09-18-explainers-v2.md)"
elif [ "$status" != 0 ]; then
  notify "Session exited with status $status — see ~/Library/Logs/reasoncommons-explainers.log"
fi
rm -f "$out"
exit "$status"
