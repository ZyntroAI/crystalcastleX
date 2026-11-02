#!/usr/bin/env bash
# sync_history.sh — read/write history.json on a dedicated git branch.
#
#   sync_history.sh pull <remote-url> <branch> <out-file>
#       Writes the branch's history.json to <out-file>, or "[]" if the branch/file doesn't exist yet.
#   sync_history.sh push <remote-url> <branch> <in-file> [commit message]
#       Commits <in-file> as history.json on <branch> (creates an orphan branch on first use) and pushes.
set -euo pipefail

mode="${1:?mode: pull|push}"; remote="${2:?remote url}"; branch="${3:?branch}"; file="${4:?file}"
msg="${5:-chore(benchmark): update history}"

branch_exists() { git ls-remote --exit-code --heads "$remote" "$branch" >/dev/null 2>&1; }

case "$mode" in
  pull)
    tmp="$(mktemp -d)"