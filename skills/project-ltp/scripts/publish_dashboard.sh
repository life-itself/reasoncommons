#!/usr/bin/env sh
# Build the multi-project dashboard and copy it to the repo-root /dashboard so
# the published (Flowershow) site serves it at /dashboard/.
#
# The dashboard source lives in skills/project-ltp/dashboard/. Its build output
# (dist/) is also what serve_dashboard.py serves locally; this script copies a
# fresh build to the top-level /dashboard directory that the site publishes.
set -eu

repo_root=$(cd "$(dirname "$0")/../../.." && pwd)
dashboard_src="$repo_root/skills/project-ltp/dashboard"
publish_dir="$repo_root/dashboard"

cd "$dashboard_src"

# Refresh the published GitHub issue state for projects that track their
# transition-tree actions as issues. This needs network and an authenticated
# `gh`; when it is unavailable the site still publishes with the issue state
# from the last successful refresh.
if ! npm run sync:github; then
  echo "warning: could not refresh GitHub issue state; publishing the committed ledger." >&2
fi

npm run build

rm -rf "$publish_dir"
mkdir -p "$publish_dir"
cp -R dist/. "$publish_dir/"

echo "Published dashboard to $publish_dir (served at /dashboard/)."
